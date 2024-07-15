from macantine.etl.data_warehouse import DataWareHouse
from macantine.etl.etl import CAMPAIGN_DATES, ETL, fetch_teledeclarations
from sqlalchemy import types


class ETL_ANALYSIS(ETL):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod to the data warehouse
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        self.df = None
        self.years = CAMPAIGN_DATES.keys()
        self.extracted_table_name = "teledeclarations_extracted"

    def extract_dataset(self):
        # Load teledeclarations from prod database into the Data Warehouse
        self.df = fetch_teledeclarations(self.years)
        warehouse = DataWareHouse()
        df_as_str = self.df.astype(str)  # Handle errors during conversion
        warehouse.insert_dataframe(
            df_as_str, table=self.extracted_table_name, dtype={col_name: types.Text for col_name in self.df}
        )

    def transform_dataset(self):
        pass

    def load_dataset(self):
        """
        Load in database
        """
        pass
