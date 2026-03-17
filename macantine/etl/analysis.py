import json
import logging
import time
from datetime import datetime

import pandas as pd

from api.views.canteen import CanteenAnalysisListView
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclaredAnalysisListView
from data.models import Canteen, Diagnostic, Purchase, User
from data.models.sector import get_category_lib_list_from_canteen_snapshot, get_sector_lib_list_from_canteen_snapshot
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
        self.warehouse = DataWareHouse()
        self.dataset_name = ""
        self.schema = ""

    def load_dataset(self):
        """
        Load in database
        """
        logger.info(f"Loading {len(self.df)} objects in db")
        self.warehouse.insert_dataframe(self.df, self.dataset_name)


class ETL_ANALYSIS_TELEDECLARATIONS(etl.EXTRACTOR, ANALYSIS):
    """
    Create a dataset for analysis in a Data Warehouse
    * Extract data from prod
    * Run a SQL query using Metabase API to transform the dataset
    * Load the transformed data in a new table within the Data WareHouse
    """

    def __init__(self):
        super().__init__()
        self.warehouse = DataWareHouse()
        self.years = CAMPAIGN_DATES.keys()
        self.dataset_name = "teledeclarations"
        self.schema = json.load(open("data/schemas/export_analysis/schema_teledeclarations.json"))
        self.columns = [field["name"] for field in self.schema["fields"]]
        self.view = DiagnosticTeledeclaredAnalysisListView

    def transform_dataset(self):
        if self.df.empty:
            logger.warning("Dataset is empty. Skipping transformations.")
            return

        self.flatten_central_kitchen_td()
        self.delete_duplicates_cc_csat()
        self.df = utils.filter_dataframe_with_schema_cols(self.df, self.schema)

    def load_dataset(self, versionning=False):
        """
        Load in database with versionning. This function is called by a manually launched task
        """
        if versionning:
            self.dataset_name = self.dataset_name + "_" + datetime.today().strftime("%Y_%m_%d")
            logger.info(f"Loading {len(self.df)} objects in db. Version {self.dataset_name}")
            self.warehouse.insert_dataframe(self.df, self.dataset_name)
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
                        satellite_row["epci"] = satellite.get("epci", None)
                        satellite_row["pat_list"] = ",".join(satellite.get("pat_list", []))
                        satellite_row["departement"] = satellite.get("department", None)
                        satellite_row["region"] = satellite.get("region", None)
                        satellite_row["secteur"] = ",".join(get_sector_lib_list_from_canteen_snapshot(satellite))
                        satellite_row["categorie"] = ",".join(get_category_lib_list_from_canteen_snapshot(satellite))
                        satellite_row["is_filled"] = satellite.get("is_filled", None)
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


class ETL_ANALYSIS_DIAGNOSTIC_RAW(ANALYSIS):
    """
    Export raw diagnostic/teledeclaration table to analysis warehouse without transformations.
    Uses pandas to_sql for loading.
    """

    def __init__(self):
        super().__init__()
        self.warehouse = DataWareHouse()
        self.dataset_name = "diagnostics_raw"

    def extract_dataset(self):
        """
        Load raw table into a dataframe.
        """
        start = time.time()
        queryset = Diagnostic.objects.all().values()
        self.df = pd.DataFrame(list(queryset))
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe")
        end = time.time()
        logger.info(f"Time spent on raw teledeclaration extraction: {end - start:.2f} seconds")

    def transform_dataset(self):
        """Convert array fields to JSON strings to avoid pandas to_sql type errors."""
        logger.info("Converting array fields to JSON strings for safe export")
        if not self.df.empty:
            self.df = utils.arrays_to_json(self.df)

    def load_dataset(self):
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
        self.warehouse = DataWareHouse()
        self.dataset_name = "canteens"
        self.schema = json.load(open("data/schemas/export_analysis/schema_cantines.json"))
        self.view = CanteenAnalysisListView

    def transform_dataset(self):
        # Calling this method is still needed to respect the structure of the code
        # TODO : Make it possible to stop calling transform_dataset()
        logger.info("No more transformation needed here !")


class ETL_ANALYSIS_CANTEEN_RAW(ANALYSIS):
    """
    Export raw canteen table to analysis warehouse without transformations.
    Uses pandas to_sql for loading.
    """

    def __init__(self):
        super().__init__()
        self.dataset_name = "canteens_raw"
        self.warehouse = DataWareHouse()

    def extract_dataset(self):
        """
        Load raw table into a dataframe.
        """
        start = time.time()
        queryset = Canteen.all_objects.all().values()
        self.df = pd.DataFrame(list(queryset))
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe")
        end = time.time()
        logger.info(f"Time spent on extraction: {end - start:.2f} seconds")

    def transform_dataset(self):
        """Convert array fields to JSON strings to avoid pandas to_sql type errors."""
        logger.info("Converting array fields to JSON strings for safe export")
        if not self.df.empty:
            self.df = utils.arrays_to_json(self.df)

    def load_dataset(self):
        super().load_dataset()


class ETL_ANALYSIS_PURCHASE_RAW(ANALYSIS):
    """
    Export raw purchase table to analysis warehouse without transformations.
    Uses pandas to_sql for loading.
    """

    def __init__(self):
        super().__init__()
        self.warehouse = DataWareHouse()
        self.dataset_name = "purchases_raw"

    def extract_dataset(self):
        """
        Load raw table into a dataframe.
        """
        start = time.time()
        queryset = Purchase.all_objects.all().values()
        self.df = pd.DataFrame(list(queryset))
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe")
        end = time.time()
        logger.info(f"Time spent on raw purchase extraction: {end - start:.2f} seconds")

    def transform_dataset(self):
        """Convert array fields to JSON strings to avoid pandas to_sql type errors."""
        logger.info("Converting array fields to JSON strings for safe export")
        if not self.df.empty:
            self.df = utils.arrays_to_json(self.df)

    def load_dataset(self):
        super().load_dataset()


class ETL_ANALYSIS_USER_RAW(ANALYSIS):
    """
    Export raw user table to analysis warehouse without transformations.
    Uses pandas to_sql for loading.
    """

    def __init__(self):
        super().__init__()
        self.warehouse = DataWareHouse()
        self.dataset_name = "users_raw"

    def extract_dataset(self):
        """
        Load raw table into a dataframe.
        """
        start = time.time()
        queryset = User.objects.all().values()
        self.df = pd.DataFrame(list(queryset))
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe")
        end = time.time()
        logger.info(f"Time spent on raw user extraction: {end - start:.2f} seconds")

    def transform_dataset(self):
        """Convert array fields to JSON strings to avoid pandas to_sql type errors."""
        logger.info("Converting array fields to JSON strings for safe export")
        if not self.df.empty:
            self.df = utils.arrays_to_json(self.df)

    def load_dataset(self):
        super().load_dataset()


class ETL_ANALYSIS_CANTEEN_MANAGER_RAW(ANALYSIS):
    """
    Export raw canteen manager table to analysis warehouse without transformations.
    Uses pandas to_sql for loading.
    """

    def __init__(self):
        super().__init__()
        self.warehouse = DataWareHouse()
        self.dataset_name = "canteen_managers_raw"

    def extract_dataset(self):
        """
        Load raw table into a dataframe.
        """
        start = time.time()
        queryset = Canteen.managers.through.objects.values("canteen_id", "user_id")
        self.df = pd.DataFrame(list(queryset))
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe")
        end = time.time()
        logger.info(f"Time spent on raw canteen manager extraction: {end - start:.2f} seconds")

    def transform_dataset(self):
        """Convert array fields to JSON strings to avoid pandas to_sql type errors."""
        logger.info("Converting array fields to JSON strings for safe export")
        if not self.df.empty:
            self.df = utils.arrays_to_json(self.df)

    def load_dataset(self):
        super().load_dataset()
