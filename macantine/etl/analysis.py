import json
import logging
import tempfile
import time
from datetime import datetime

import pandas as pd
from django.contrib.postgres.fields import ArrayField
from django.db import connection

from api.views.canteen import CanteenAnalysisListView
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclaredAnalysisListView
from data.models import Canteen
from data.models.sector import get_category_lib_list_from_canteen_snapshot, get_sector_lib_list_from_canteen_snapshot
from macantine.etl import etl, utils
from macantine.etl.data_ware_house import DataWareHouse, get_column_types
from data.models.diagnostic_teledeclaration_dates import CAMPAIGN_DATES
from data.models.geo import Department, Region

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
                    satellite_row["siret"] = satellite["siret"]
                    satellite_row["production_type"] = Canteen.ProductionType.ON_SITE_CENTRAL
                    satellite_row["satellite_canteens_count"] = 0
                    # since 2025: override more fields
                    if satellite_row["year"] >= 2025:
                        satellite_row["production_type"] = satellite["production_type"]
                        satellite_row["management_type"] = satellite["management_type"]
                        satellite_row["modele_economique"] = satellite["economic_model"]
                        satellite_row["code_insee_commune"] = satellite.get("city_insee_code", None)
                        satellite_row["epci"] = satellite.get("epci", None)
                        satellite_row["pat_list"] = ",".join(satellite.get("pat_list", []))
                        department = satellite.get("department", None)
                        satellite_row["departement"] = department
                        satellite_row["lib_departement"] = (
                            Department(department).label.split(" - ")[1].lstrip() if department else None
                        )
                        region = satellite.get("region", None)
                        satellite_row["region"] = region
                        satellite_row["lib_region"] = Region(region).label.split(" - ")[1].lstrip() if region else None
                        satellite_row["objectif_zone_geo"] = utils.get_objectif_zone_geo(department)
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


class ETL_ANALYSIS_RAW(ANALYSIS):
    """
    Copy a table as-is to the analysis Data Warehouse (used as a dbt source).
    * Extract: Postgres COPY of the queryset rows into a temporary file on disk (no pandas)
    * Load: Postgres COPY of the file into the Data Warehouse table (see DataWareHouse.copy_file)

    Column types are the ones of the source table, except arrays which are converted to jsonb.
    Columns listed in exclude_columns are not exported (e.g. sensitive data).
    """

    def __init__(self, dataset_name, queryset, exclude_columns=None):
        super().__init__()
        self.dataset_name = dataset_name
        self.queryset = queryset
        self.exclude_columns = exclude_columns or []
        self.column_types = {}
        self.file = None

    def extract_dataset(self):
        start = time.time()
        model = self.queryset.model
        unknown_columns = set(self.exclude_columns) - {field.column for field in model._meta.concrete_fields}
        if unknown_columns:
            # fail instead of silently exporting a column because of a typo
            raise ValueError(
                f"Unknown columns to exclude from {self.dataset_name}: {', '.join(sorted(unknown_columns))}"
            )
        fields = [field for field in model._meta.concrete_fields if field.column not in self.exclude_columns]

        sql, params = self.queryset.order_by().values(*[field.attname for field in fields]).query.sql_with_params()
        select = ", ".join(
            f'to_jsonb("{field.column}") AS "{field.column}"' if isinstance(field, ArrayField) else f'"{field.column}"'
            for field in fields
        )

        self.file = tempfile.TemporaryFile()
        with connection.cursor() as cursor:
            source_column_types = get_column_types(cursor, model._meta.db_table)
            copy_sql = cursor.mogrify(f"COPY (SELECT {select} FROM ({sql}) AS source) TO STDOUT", params).decode()
            cursor.copy_expert(copy_sql, self.file)
        self.column_types = {
            field.column: "jsonb" if isinstance(field, ArrayField) else source_column_types[field.column]
            for field in fields
        }

        end = time.time()
        logger.info(
            f"Time spent on {self.dataset_name} extraction: {end - start:.2f} seconds ({self.file.tell() / 1024 / 1024:.1f} MB)"
        )

    def transform_dataset(self):
        pass

    def load_dataset(self):
        try:
            self.file.seek(0)
            self.warehouse.copy_file(self.file, self.dataset_name, self.column_types)
        finally:
            self.file.close()
