from macantine.etl.data_warehouse import DataWareHouse
from macantine.etl.etl import CAMPAIGN_DATES, ETL, fetch_teledeclarations
from sqlalchemy import types


class ETL_ANALYSIS(ETL):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod 
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        self.df = None
        self.years = CAMPAIGN_DATES.keys()
        self.extracted_table_name = "teledeclarations_extracted"
        self.warehouse = DataWareHouse()

    def extract_dataset(self):
        # Load teledeclarations from prod database into the Data Warehouse
        self.df = fetch_teledeclarations(self.years)

    def transform_dataset(self):
        # Flatten json 'declared_data' column
        df_json = pd.json_normalize(self.df["declared_data"])
        del df_json["year"]
        self.df = self.df.loc[~self.df.index.duplicated(keep="first")]
        self.df = pd.concat([self.df.drop("declared_data", axis=1), df_json], axis=1)

    def load_dataset(self):
        """
        Load in database
        """
        pass
