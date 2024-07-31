import pandas as pd
import logging
import json

from macantine.etl.data_warehouse import DataWareHouse
from macantine.etl import etl
logger = logging.getLogger(__name__)


def get_management_type(value):
    if value == "direct":
        return "A) directe"
    elif value == "conceded":
        return "B) concédée"
    else:
        return "C) non renseigné"


def get_cuisine_centrale(value):
    if value in ["site", "site_cooked_elsewhere"]:
        return "B) non"
    elif value in ["central", "central_serving"]:
        return "A) oui"
    else:
        return "C) non renseigné"


def get_economic_model(value):
    if value == "private":
        return "A) privé"
    elif value == "public":
        return "B) oui"
    else:
        return "C) non renseigné"


def get_diagnostic_type(value):
    if value == "COMPLETE":
        return "A) détaillée"
    elif value == "SIMPLE":
        return "B) simple"
    else:
        return "C) non renseigné"


def campaign_participation(row, year):
    return True


class ETL_ANALYSIS(etl.ETL):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        self.df = None
        self.years = etl.CAMPAIGN_DATES.keys()
        self.extracted_table_name = "teledeclarations_extracted"
        self.warehouse = DataWareHouse()
        self.schema = json.load(open("data/schemas/schema_analysis.json"))

    def extract_dataset(self):
        # Load teledeclarations from prod database into the Data Warehouse
        self.df = etl.fetch_teledeclarations(self.years)

    def transform_dataset(self):
        # Flatten json 'declared_data' column
        df_json = pd.json_normalize(self.df["declared_data"])
        del df_json["year"]
        self.df = self.df.loc[~self.df.index.duplicated(keep="first")]
        self.df = pd.concat([self.df.drop("declared_data", axis=1), df_json], axis=1)

        # Calculate columns
        self.df["management_type"] = self.df["canteen.management_type"].apply(get_management_type)
        self.df["cuisine_centrale"] = self.df["canteen.production_type"].apply(get_management_type)
        self.df["modele_economique"] = self.df["canteen.economic_model"].apply(get_economic_model)
        self.df["diagnostic_type"] = self.df["teledeclaration.diagnostic_type"].apply(get_economic_model)

        # Convert types
        self.df["daily_meal_count"] = pd.to_numeric(self.df["canteen.daily_meal_count"], errors="coerce")
        self.df["yearly_meal_count"] = pd.to_numeric(self.df["canteen.yearly_meal_count"], errors="coerce")
        self.df["satellite_canteens_count"] = pd.to_numeric(
            self.df["canteen.satellite_canteens_count"], errors="coerce"
        )

        # Fill geo data
        for geo in ["department", "region"]:
            geo = f"canteen.{geo}"
            logger.info("Start filling geo_name")
            self.fill_geo_names(geo_zoom=geo)
            col_geo = self.df.pop(f"{geo}_lib")
            self.df.insert(self.df.columns.get_loc(geo) + 1, f"{geo}_lib", col_geo)

        # Fill campaign participation
        logger.info("Canteens : Fill campaign participations...")
        for year in CAMPAIGN_DATES.keys():
            campaign_participation = map_canteens_td(year)
            col_name_campaign = f"declared_{year}"
            self.df[col_name_campaign] = self.df["id"].apply(lambda x: x in campaign_participation)

        columns = [i["name"] for i in self.schema["fields"]]
        self.df = self.df[columns]

    def load_dataset(self):
        """
        Load in database
        """
        pass
