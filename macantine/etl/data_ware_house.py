import logging
import os
import time

import psycopg2
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_column_types(cursor, table) -> dict:
    """
    Return {column_name: sql_type} of an existing table (empty dict if the table doesn't exist).
    Types are normalized by Postgres (format_type), so they can be compared between databases.
    """
    cursor.execute(
        """
        SELECT attname, format_type(atttypid, atttypmod)
        FROM pg_attribute
        WHERE attrelid = to_regclass(%s) AND attnum > 0 AND NOT attisdropped
        ORDER BY attnum
        """,
        [f'"{table}"'],
    )
    return dict(cursor.fetchall())


def copy_into_table(cursor, table, column_types: dict, file):
    """
    Replace the content of a table with a Postgres COPY (text format) file.
    - the table is kept (TRUNCATE) to preserve the objects that depend on it (dbt views)
    - new columns are added
    - if a column was removed or changed type, the table is recreated (dependent views are dropped,
      dbt run recreates them)
    The caller is responsible for the transaction: the reload is atomic if it is committed at once.
    """
    existing_column_types = get_column_types(cursor, table)
    changed_columns = [col for col, col_type in existing_column_types.items() if column_types.get(col) != col_type]

    if existing_column_types and changed_columns:
        logger.warning(f"Schema of table {table} changed (columns: {', '.join(changed_columns)}). Recreating it")
        cursor.execute(f'DROP TABLE "{table}" CASCADE')
        existing_column_types = {}

    if existing_column_types:
        for col, col_type in column_types.items():
            if col not in existing_column_types:
                logger.info(f"Adding column {col} to table {table}")
                cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN "{col}" {col_type}')
        cursor.execute(f'TRUNCATE TABLE "{table}"')
    else:
        column_defs = ", ".join(f'"{col}" {col_type}' for col, col_type in column_types.items())
        cursor.execute(f'CREATE TABLE "{table}" ({column_defs})')

    columns = ", ".join(f'"{col}"' for col in column_types)
    cursor.copy_expert(f'COPY "{table}" ({columns}) FROM STDIN', file)
    return cursor.rowcount


class DataWareHouse:
    def __init__(self):
        load_dotenv()
        # no connection here: it is opened (and closed) by each load
        self.connection_params = {
            "user": os.environ.get("DATA_WARE_HOUSE_USER"),
            "password": os.environ.get("DATA_WARE_HOUSE_PASSWORD"),
            "host": os.environ.get("DATA_WARE_HOUSE_HOST"),
            "port": os.environ.get("DATA_WARE_HOUSE_PORT"),
            "dbname": os.environ.get("DATA_WARE_HOUSE_DB"),
        }

    def copy_file(self, file, table, column_types: dict):
        """
        Replace the content of a table with a Postgres COPY (text format) file, in a single transaction
        """
        start = time.time()
        connection = psycopg2.connect(**self.connection_params)
        try:
            with connection.cursor() as cursor:
                row_count = copy_into_table(cursor, table, column_types, file)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
        end = time.time()
        logger.info(f"Copied {row_count} rows into table {table} in {end - start:.2f} seconds")
