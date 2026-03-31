import logging
import os
import time

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

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

    def _drop_table_with_cascade(self, table):
        with self.engine.begin() as connection:
            connection.execute(text("DROP VIEW IF EXISTS dbt_dev_staging.stg_diagnostics CASCADE;"))
        with self.engine.begin() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))

    def _insert_dataframe_delete_rows(self, dataframe, table):
        dataframe.to_sql(
            name=table,
            con=self.engine,
            if_exists="delete_rows",
            index=False,
            chunksize=1000,
            # method="multi",  # Batch INSERTs for 2-3x speedup
        )

    def _insert_dataframe_replace(self, dataframe, table):
        dataframe.to_sql(
            name=table,
            con=self.engine,
            if_exists="replace",
            index=False,
            chunksize=1000,
            # method="multi",  # Batch INSERTs for 2-3x speedup
        )

    def insert_dataframe(self, dataframe, table):
        start = time.time()
        try:
            self._insert_dataframe_delete_rows(dataframe, table)
        except:  # noqa
            self._drop_table_with_cascade(table)
            self._insert_dataframe_replace(dataframe, table)
        end = time.time()
        logger.info(f"Inserted {len(dataframe)} rows into table {table} in {end - start:.2f} seconds")

    def read_dataframe(self, table_name):
        return pd.read_sql(sql=table_name, index_col="id", con=self.engine)
