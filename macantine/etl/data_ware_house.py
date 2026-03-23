import logging
import os
import time
from datetime import date, datetime
from decimal import Decimal
from io import StringIO
from uuid import UUID

import pandas as pd
from django.contrib.postgres.fields import ArrayField
from django.db import models
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

logger = logging.getLogger(__name__)


class DataWareHouse:
    def __init__(self):
        load_dotenv()
        url_object = URL.create(
            "postgresql+psycopg2",
            username=os.environ.get("DATA_WARE_HOUSE_USER"),
            password=os.environ.get("DATA_WARE_HOUSE_PASSWORD"),
            host=os.environ.get("DATA_WARE_HOUSE_HOST"),
            port=os.environ.get("DATA_WARE_HOUSE_PORT"),
            database=os.environ.get("DATA_WARE_HOUSE_DB"),
        )
        self.engine = create_engine(
            url_object,
            echo=False,
        )

    def read_dataframe(self, table_name):
        return pd.read_sql(sql=table_name, index_col="id", con=self.engine)

    def insert_dataframe(self, dataframe, table, dtype=None):
        start = time.time()
        dataframe.to_sql(
            name=table,
            con=self.engine,
            if_exists="delete_rows",  # "replace" (drops and recreates the table)
            index=False,
            dtype=dtype,
            chunksize=1000,
            # method="multi",  # Batch INSERTs for 2-3x speedup
        )
        end = time.time()
        logger.info(f"Inserted {len(dataframe)} rows into table {table} in {end - start:.2f} seconds")

    def insert_records(self, records: list, table: str, model):
        """
        Bulk-insert a list of dicts into a warehouse table using PostgreSQL text COPY.
        The table is created if missing, then truncated before each load.
        SQL types are derived from Django model field metadata.
        """
        import json

        if not records:
            logger.warning(f"No records to insert into {table}")
            return

        if model is None:
            raise ValueError("insert_records requires a Django model to determine SQL column types")

        start = time.time()
        columns = list(records[0].keys())

        def _field_to_pg_type(field):
            if isinstance(field, models.BooleanField):
                return "BOOLEAN"
            if isinstance(field, (models.SmallIntegerField, models.IntegerField, models.BigIntegerField)):
                return "BIGINT"
            if isinstance(field, (models.FloatField, models.DecimalField)):
                return "DOUBLE PRECISION"
            if isinstance(field, (models.DateTimeField,)):
                return "TIMESTAMPTZ"
            if isinstance(field, (models.DateField,)):
                return "DATE"
            if isinstance(field, (models.TimeField,)):
                return "TIME"
            if isinstance(field, (models.UUIDField,)):
                return "UUID"
            if isinstance(field, (models.JSONField,)):
                return "TEXT"
            if isinstance(field, ArrayField):
                return "TEXT"
            if isinstance(field, (models.BinaryField,)):
                return "BYTEA"
            if isinstance(
                field, (models.CharField, models.TextField, models.EmailField, models.URLField, models.SlugField)
            ):
                return "TEXT"
            return "TEXT"

        field_map = {field.name: field for field in model._meta.get_fields() if hasattr(field, "attname")}
        attname_map = {field.attname: field for field in model._meta.get_fields() if hasattr(field, "attname")}
        col_types = {}
        for col in columns:
            field = field_map.get(col) or attname_map.get(col)
            col_types[col] = _field_to_pg_type(field) if field is not None else "TEXT"

        def _serialize(val):
            if val is None:
                return None
            if isinstance(val, (list, dict)):
                return json.dumps(val, default=str)
            if isinstance(val, bytes):
                return f"\\x{val.hex()}"
            if isinstance(val, UUID):
                return str(val)
            if isinstance(val, Decimal):
                return float(val)
            if isinstance(val, (datetime, date)):
                return val.isoformat()
            return str(val)

        buffer = StringIO()
        for record in records:
            row = []
            for col in columns:
                value = _serialize(record[col])
                if value is None:
                    row.append(r"\N")
                    continue
                text = str(value)
                text = text.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
                row.append(text)
            buffer.write("\t".join(row) + "\n")
        buffer.seek(0)

        raw_conn = self.engine.raw_connection()
        try:
            cur = raw_conn.cursor()
            col_defs = ", ".join(f'"{col}" {col_types[col]}' for col in columns)
            # CREATE TABLE IF NOT EXISTS preserves dbt metadata (views, grants, etc.) on the table.
            # Caveat: if the Django model gains new columns, they won't appear here until the table
            # is manually altered or dropped. TRUNCATE clears rows without dropping the table.
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS "{table}" ({col_defs});
                """
            )

            # Keep table identity for dbt, but ensure it can store current extract types.
            # This widens existing columns when needed and adds newly introduced columns.
            for col in columns:
                pg_type = col_types[col]
                cur.execute(f'ALTER TABLE "{table}" ADD COLUMN IF NOT EXISTS "{col}" {pg_type}')
                cur.execute(f'ALTER TABLE "{table}" ALTER COLUMN "{col}" TYPE {pg_type} USING "{col}"::{pg_type}')

            cur.execute(f'TRUNCATE TABLE "{table}"')

            quoted_columns = ", ".join(f'"{col}"' for col in columns)
            cur.copy_expert(
                sql=f'COPY "{table}" ({quoted_columns}) FROM STDIN WITH (FORMAT text)',
                file=buffer,
            )
            raw_conn.commit()
        finally:
            raw_conn.close()

        end = time.time()
        logger.info(f"Inserted {len(records)} rows into table {table} in {end - start:.2f} seconds")
