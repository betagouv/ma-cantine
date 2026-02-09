import json
import logging
from datetime import datetime

import pandas as pd

from data.models.sector import get_sector_lib_list_from_canteen_snapshot, get_category_lib_list_from_canteen_snapshot
from api.views.canteen import CanteenAnalysisListView
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclaredAnalysisListView
from data.models import Canteen
from macantine.etl import etl, utils
from macantine.etl.data_ware_house import DataWareHouse
from macantine.utils import CAMPAIGN_DATES

logger = logging.getLogger(__name__)


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
        self.schema = json.load(open("data/schemas/export_analysis/schema_teledeclarations.json"))
        self.columns = [field["name"] for field in self.schema["fields"]]
        self.view = DiagnosticTeledeclaredAnalysisListView

    def transform_dataset(self):
        if self.df.empty:
            logger.warning("Dataset is empty. Skipping transformation")
            return

        self.flatten_central_kitchen_td()
        self.delete_duplicates_cc_csat()
        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)

    def load_dataset(self, versionning=False):
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

    def delete_duplicates_cc_csat(self):
        """
        Remove duplicate rows for central kitchens and their satellites based on unique identifiers.
        Keep the row where production type is central kitchen if duplicates exist.
        """
        if "canteen_id" in self.df.columns and "genere_par_cuisine_centrale" in self.df.columns:
            self.df = self.df.sort_values(
                by=["genere_par_cuisine_centrale"],
                ascending=False,
            )
            self.df = self.df.drop_duplicates(subset=["canteen_id", "year"], keep="first")
        else:
            logger.warning(
                "Required columns 'canteen_id' or 'genere_par_cuisine_centrale' not found in dataframe. Skipping duplicate removal."
            )

    def flatten_central_kitchen_td(self):
        """
        1TD1Site: split rows of central kitchen into a row for each satellite
        NOTE: following the migration to groupes, we added the central_serving extra satellite in their snapshots
        """
        self.df = self.df.set_index("id", drop=False)
        satellite_rows = []

        for _, row in self.df.iterrows():
            if row["production_type"] in {
                Canteen.ProductionType.GROUPE,
                Canteen.ProductionType.CENTRAL,
                Canteen.ProductionType.CENTRAL_SERVING,
            }:
                nbre_satellites = len(row["tmp_satellites"] or [])
                for satellite in row["tmp_satellites"] or []:
                    # duplicate the row
                    satellite_row = row.copy()
                    # override with satellite data
                    satellite_row["canteen_id"] = satellite["id"]
                    satellite_row["name"] = satellite["name"]
                    satellite_row["production_type"] = Canteen.ProductionType.ON_SITE_CENTRAL
                    satellite_row["siret"] = satellite["siret"]
                    satellite_row["satellite_canteens_count"] = 0
                    # since 2025: override more fields
                    if satellite_row["year"] >= 2025:
                        satellite_row["production_type"] = satellite["production_type"]
                        satellite_row["management_type"] = satellite["management_type"]
                        satellite_row["modele_economique"] = satellite["economic_model"]
                        satellite_row["code_insee_commune"] = satellite.get("city_insee_code", None)
                        satellite_row["departement"] = satellite.get("department", None)
                        satellite_row["region"] = satellite.get("region", None)
                        satellite_row["secteur"] = ",".join(get_sector_lib_list_from_canteen_snapshot(satellite))
                        satellite_row["categorie"] = ",".join(get_category_lib_list_from_canteen_snapshot(satellite))
                    # split numerical values
                    satellite_row = self.split_cc_values(satellite_row, nbre_satellites)
                    # append
                    satellite_rows.append(satellite_row)

        # Append all new rows at once
        if satellite_rows:
            self.df = pd.concat([self.df, pd.DataFrame(satellite_rows)], ignore_index=True)

        # Delete lines of central kitchen
        self.df = self.df[
            ~self.df.production_type.isin(
                [Canteen.ProductionType.GROUPE, Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]
            )
        ]

    def split_cc_values(self, row, nbre_satellites):
        """
        Divide numerical values of a central kitchen to split into satellites
        """
        appro_columns = [col_appro for col_appro in self.columns if "valeur" in col_appro]
        for col in appro_columns + ["yearly_meal_count"]:
            if col in row and row[col] not in (None, "nan") and nbre_satellites:
                row[col] = row[col] / nbre_satellites
            else:
                row[col] = None
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
        self.schema = json.load(open("data/schemas/export_analysis/schema_cantines.json"))
        self.view = CanteenAnalysisListView

    def transform_dataset(self):
        # Calling this method is still needed to respect the structure of the code
        # TODO : Make it possible to stop calling transform_dataset()
        logger.info("No more transformation needed here !")
