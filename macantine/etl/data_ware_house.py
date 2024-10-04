import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine


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

    def insert_dataframe(self, dataframe, table, dtype=None):
        dataframe.to_sql(name=table, con=self.engine, if_exists="replace", index=False, dtype=dtype)
