from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os


class DataWareHouse:

    def __init__(self):
        load_dotenv()
        url_object = URL.create(
            "postgresql+psycopg2",
            username=os.environ.get("DATA_WAREHOUSE_USER"),
            password=os.environ.get("DATA_WAREHOUSE_PASSWORD"),
            host=os.environ.get("DATA_WAREHOUSE_HOST"),
            port=os.environ.get("DATA_WAREHOUSE_PORT"),
            database=os.environ.get("DATA_WAREHOUSE_DB"),
        )
        self.engine = create_engine(
            url_object,
            echo=False,
        )

    def insert_dataframe(self, dataframe, table, dtype=None):
        dataframe.to_sql(name=table, con=self.engine, if_exists="replace", index=False, dtype=dtype)
