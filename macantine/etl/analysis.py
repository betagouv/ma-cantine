import json
import logging
import re
from datetime import datetime

import pandas as pd

from api.views.canteen import CanteenAnalysisListView
from api.views.teledeclaration import TeledeclarationAnalysisListView
from data.models import Canteen
from macantine.etl import etl, utils
from macantine.etl.data_ware_house import DataWareHouse
from macantine.utils import CAMPAIGN_DATES

logger = logging.getLogger(__name__)


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
        self.flatten_central_kitchen_td()
        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)

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

    def flatten_central_kitchen_td(self):
        """
        Split rows of central kitchen into a row for each satellite
        """
        for index, row in self.df.iterrows():
            if (
                row["production_type"] == Canteen.ProductionType.CENTRAL
                or row["production_type"] == Canteen.ProductionType.CENTRAL_SERVING
            ):
                for satellite in row["tmp_satellites"]:
                    satellite_row = row.copy()
                    satellite_row["id"] = satellite["id"]
                    satellite_row["name"] = satellite["name"]
                    satellite_row["production_type"] = Canteen.ProductionType.ON_SITE_CENTRAL
                    satellite_row["siret"] = satellite["siret"]
                    satellite_row["yearly_meal_count"] = satellite["yearly_meal_count"]
                    satellite_row = self.split_appro_values(index, satellite_row, len(row["tmp_satellites"]))
                    self.df = pd.concat([self.df, pd.DataFrame(satellite_row).T])

            # if row["production_type"] == Canteen.ProductionType.CENTRAL_SERVING:
            #     self.df = self.split_appro_values(index, row)
        # Delete lines of central kitchen
        self.df = self.df[self.df.production_type != Canteen.ProductionType.CENTRAL]

    def split_appro_values(self, index, row, nbre_satellites):
        """
        Divide numerical values of a central kitchen to split into satellites
        """
        appro_columns = [col_appro for col_appro in self.columns if "value" in col_appro]
        for appro_column in appro_columns:
            try:
                row[appro_column] = row[appro_column] / nbre_satellites
                # self.df.at[index, appro_column] = row[appro_column] * 0
            except KeyError:
                logging.warning("Column not found while splitting numerical value from central kitchen to satellites")
        return row


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
