import json
import logging
import re
from datetime import datetime

import numpy as np
import pandas as pd

from api.views.canteen import CanteenAnalysisListView
from api.views.teledeclaration import TeledeclarationAnalysisListView
from macantine.etl import etl, utils
from macantine.etl.data_ware_house import DataWareHouse
from macantine.utils import CAMPAIGN_DATES

logger = logging.getLogger(__name__)

# Source : query Resytal dec 2023
ESTIMATED_NUMBER_CANTEENS_REGION = {
    1: 625,
    2: 554,
    3: 161,
    4: 900,
    6: 203,
    11: 13235,
    24: 4171,
    27: 3623,
    28: 4360,
    32: 7061,
    44: 7324,
    52: 4545,
    53: 4279,
    75: 8854,
    76: 7336,
    84: 10842,
    93: 5991,
    94: 395,
}


def get_nbre_cantines_region(region: int):
    if region in ESTIMATED_NUMBER_CANTEENS_REGION.keys():
        return ESTIMATED_NUMBER_CANTEENS_REGION[region]
    else:
        return np.nan


def get_objectif_zone_geo(department: int):
    if department and department != "nan" and not pd.isna(department):
        # Dealing with two string codes
        if department == "2A" or department == "2B":
            return "France métropolitaine"
        department = int(department)
        if department >= 1 and department <= 95:
            return "France métropolitaine"
        elif department == 976:
            return "DROM (Mayotte)"
        elif department >= 971 and department <= 978:
            return "DROM (hors Mayotte)"
    return "non renseigné"


def check_column_matches_substring(df, sub_categ: str):
    for substring in sub_categ:
        pattern = rf".*{re.escape(substring)}.*"
        matching_cols = df.filter(regex=pattern).columns.tolist()
        if len(matching_cols) == 0:
            logger.error("The sub categ {substring} doesn't match any columns from the dataframe")
            raise KeyError


def aggregate_col(df, categ, sub_categ):
    """
    Aggregating into a new column all the values of a category for complete TD
    """
    check_column_matches_substring(df, sub_categ)
    regex_pattern = rf"^(?!value_{categ}_ht$).*(" + "|".join(sub_categ) + ")"
    df[f"teledeclaration.value_{categ}_ht"] = df.filter(regex=regex_pattern).sum(
        axis=1, numeric_only=True, skipna=True, min_count=1
    )
    return df


class ANALYSIS(etl.TRANSFORMER_LOADER):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        super().__init__()
        self.extracted_table_name = ""
        self.schema = ""
        self.warehouse = DataWareHouse()

    def load_dataset(self):
        """
        Load in database
        """
        logger.info(f"Loading {len(self.df)} objects in db")
        self.warehouse.insert_dataframe(self.df, self.extracted_table_name)

    def _clean_dataset(self):
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]
        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)
        self.df = self.df.drop_duplicates(subset=["id"])


class ETL_ANALYSIS_TELEDECLARATIONS(ANALYSIS, etl.EXTRACTOR):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        super().__init__()
        self.years = CAMPAIGN_DATES.keys()
        self.extracted_table_name = "teledeclarations"
        self.warehouse = DataWareHouse()
        self.schema = json.load(open("data/schemas/export_metabase/schema_teledeclarations.json"))
        self.columns = [field["name"] for field in self.schema["fields"]]
        self.view = TeledeclarationAnalysisListView

    def transform_dataset(self):
        if self.df.empty:
            logger.warning("Dataset is empty. Skipping transformation")
            return

        # Use id as index
        self.df.index = self.df.id

        # Flatten json 'declared_data' column
        df_json = pd.json_normalize(self.df["declared_data"])
        del df_json["year"]
        del df_json["canteen.id"]

        # Making sure those fields now come from the serializer by dropping them in the decalared_data field
        df_json = df_json[df_json.columns.drop(list(df_json.filter(regex="canteen.")))]
        df_json = df_json[df_json.columns.drop(list(df_json.filter(regex="teledeclaration.")))]

        df_json.index = self.df.id
        self.df = self.df.loc[~self.df.index.duplicated(keep="first")]
        self.df = pd.concat([self.df.drop("declared_data", axis=1), df_json], axis=1)

        # Aggregate columns for complete TD - Must occur before other transformations
        # remove already aggregated column
        # TODO : when fixed, we can use directly the aggregated columns
        # del self.df["value_total_ht"]
        # del self.df["value_bio_ht_agg"]
        # del self.df["value_sustainable_ht_agg"]
        # del self.df["value_externality_performance_ht_agg"]
        # del self.df["value_egalim_others_ht_agg"]
        # self.df = aggregate(self.df)

        self.compute_miscellaneous_columns()

        # Fill campaign participation
        logger.info("TD : Fill campaign participations...")
        for year in CAMPAIGN_DATES.keys():
            campaign_participation = utils.map_canteens_td(year)
            col_name_campaign = f"declaration_{year}"
            self.df[col_name_campaign] = self.df["id"].apply(lambda x: x in campaign_participation)

        # Rename columns
        self.df = self.df.rename(
            columns={
                "teledeclaration.id": "id",
                "diagnostic_id": "diagnostic_id",
            }
        )
        self.df.columns = self.df.columns.str.replace("teledeclaration.", "")
        self.df.columns = self.df.columns.str.replace("applicant.", "")

        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)

    def compute_miscellaneous_columns(self):
        # Add geo data
        self.df["nbre_cantines_region"] = self.df["region"].apply(get_nbre_cantines_region)
        self.df["objectif_zone_geo"] = self.df["departement"].apply(get_objectif_zone_geo)

    def load_dataset(self, versionning=True):
        """
        Load in database with versionning. This function is called by a manually launched task
        """
        if versionning:
            logger.info(
                f"Loading {len(self.df)} objects in db. Version {self.extracted_table_name + '_' + datetime.today().strftime('%Y_%m_%d')}"
            )
            self.warehouse.insert_dataframe(
                self.df, self.extracted_table_name + "_" + datetime.today().strftime("%Y_%m_%d")
            )
        else:
            super().load_dataset()


class ETL_ANALYSIS_CANTEEN(etl.EXTRACTOR, ANALYSIS):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse

    How to add a new field ? Add it to the corresponding schema : schema_analysis_cantines.json
    - If it's a extracted field : Add it to the columns_mapper with its translation
    - If it's a generated field : Add it in the transform_dataset()
    """

    def __init__(self):
        super().__init__()
        self.extracted_table_name = "canteens"
        self.warehouse = DataWareHouse()
        self.schema = json.load(open("data/schemas/export_metabase/schema_cantines.json"))
        self.view = CanteenAnalysisListView

    def transform_dataset(self):
        # Calling this method is still needed to respect the structure of the code
        # TODO : Make it possible to stop calling transform_dataset()
        logger.info("No more transformation needed here !")
