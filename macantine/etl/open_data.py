import csv
import json
import os
from io import BytesIO

import pandas as pd
from django.core.files.storage import default_storage

import macantine.etl.utils
from common.api.datagouv import (
    MA_CANTINE_DATAGOUV_CANTEEN_DATASET_ID,
    MA_CANTINE_DATAGOUV_CANTEEN_SCHEMA_FILE_PATH,
    MA_CANTINE_DATAGOUV_CANTEEN_SCHEMA_URL,
    MA_CANTINE_DATAGOUV_TELEDECLARATION_DATASET_ID,
    MA_CANTINE_DATAGOUV_TELEDECLARATION_SCHEMA_FILE_PATH,
    MA_CANTINE_DATAGOUV_TELEDECLARATION_SCHEMA_URL,
)
from api.views.canteen import CanteenOpenDataListView
from api.views.diagnostic import DiagnosticTeledeclaredOpenDataListView
from common.api.datagouv import update_dataset_resources
from common.api.decoupage_administratif import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)
from data.models import Canteen
from macantine.etl import etl
from macantine.etl.etl import logger


class OPEN_DATA(etl.TRANSFORMER_LOADER):
    """
    Abstract class implementing the specifity for open data export
    """

    def transform_canteen_choicefields(self, prefix=""):
        # line_ministry
        self.df[prefix + "line_ministry"] = self.df[prefix + "line_ministry"].apply(
            lambda x: Canteen.Ministries(x).label if (x in Canteen.Ministries) else None
        )

    def transform_canteen_arrayfields(self, prefix=""):
        # sector_list, pat_list & pat_lib_list
        for col in [prefix + "sector_list", prefix + "pat_list", prefix + "pat_lib_list"]:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(lambda x: ",".join(x))

    def transform_canteen_geo_data(self, prefix=""):
        """
        Only for (old) TD datasets
        TODO: don't run this on new TD datasets (we store geo data now)
        """
        logger.info("Start fetching communes details")
        communes_infos = map_communes_infos()

        if "campagne_td" in self.dataset_name:
            # Get canteen geo data as most of TD don't have this info
            self.df["canteen_department"] = self.df["canteen_city_insee_code"].apply(
                lambda x: fetch_commune_detail(x, communes_infos, "department")
            )
            self.df["canteen_region"] = self.df["canteen_city_insee_code"].apply(
                lambda x: fetch_commune_detail(x, communes_infos, "region")
            )
            self.df["canteen_epci"] = self.df["canteen_epci"].apply(
                lambda x: fetch_commune_detail(x, communes_infos, "epci")
            )
            epcis_names = map_epcis_code_name()
            self.df["canteen_epci_lib"] = self.df["canteen_epci"].apply(lambda x: fetch_epci_name(x, epcis_names))

        logger.info("Start filling geo_name")
        self.fill_geo_names(prefix)

    def _clean_dataset(self):
        columns = [i["name"] for i in self.schema["fields"]]

        self.df = self.df.loc[:, ~self.df.columns.duplicated()]

        self.df = self.df.reindex(columns, axis="columns")
        self.df.columns = self.df.columns.str.replace(".", "_")
        self.df = self.df.drop_duplicates(subset=["id"])
        self.df = self.df.reset_index(drop=True)

        for col_int in self.schema["fields"]:
            if col_int["type"] == "integer":
                # Force column o Int64 to maintain an integer column despite the NaN values
                self.df[col_int["name"]] = self.df[col_int["name"]].astype("Int64")
            if col_int["type"] == "float":
                self.df[col_int["name"]] = self.df[col_int["name"]].round(decimals=4)
        self.df = self.df.replace("<NA>", "")

    def _load_data_csv(self, filename):
        df_csv = self.df.copy()
        with default_storage.open(filename + ".csv", "w") as csv_file:
            df_csv.to_csv(
                csv_file,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
                quoting=csv.QUOTE_NONE,
                escapechar="\\",
            )

    def _load_data_xlsx(self, filename):
        chunk_size = 1000
        start_row = 0

        # Create an in-memory bytes buffer
        output = BytesIO()

        # Create ExcelWriter with the actual file path
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            dataframe_chunks = [self.df[i : i + chunk_size] for i in range(0, len(self.df), chunk_size)]
            for chunk in dataframe_chunks:
                # Convert datetime to string and create copy to avoid modifications on the original dataframe
                chunk = macantine.etl.utils.datetimes_to_str(chunk.copy())

                # Write chunk to the sheet, accumulating data
                chunk.to_excel(
                    writer,
                    startrow=start_row,
                    index=False,
                    header=True if start_row == 0 else False,
                )
                start_row += len(chunk)  # Update starting row for next chunk

        # Ensure the buffer is ready for reading
        output.seek(0)

        # Save the in-memory bytes buffer to the storage backend
        with default_storage.open(filename + ".xlsx", "wb") as f:
            f.write(output.getvalue())

    def load_dataset(self):
        filepath = f"open_data/{self.dataset_name}"
        if (
            os.environ.get("STATICFILES_STORAGE") == "storages.backends.s3.S3Storage"
            and os.environ.get("DEFAULT_FILE_STORAGE") == "storages.backends.s3.S3Storage"
        ):
            if not self.is_valid():
                logger.error(f"The dataset {self.name} is invalid and therefore will not be exported to s3")
                return
        try:
            self._load_data_csv(filepath)
            self._load_data_xlsx(filepath)

            update_dataset_resources(self.datagouv_dataset_id)
        except Exception as e:
            logger.error(f"Error saving validated data: {e}")


class ETL_OPEN_DATA_CANTEEN(etl.EXTRACTOR, OPEN_DATA):
    def __init__(self):
        super().__init__()
        self.dataset_name = "registre_cantines"
        self.datagouv_dataset_id = MA_CANTINE_DATAGOUV_CANTEEN_DATASET_ID
        self.schema = json.load(open(MA_CANTINE_DATAGOUV_CANTEEN_SCHEMA_FILE_PATH))
        self.schema_url = MA_CANTINE_DATAGOUV_CANTEEN_SCHEMA_URL
        self.columns = [field["name"] for field in self.schema["fields"]]
        self.view = CanteenOpenDataListView

    def transform_dataset(self):
        logger.info("Canteens: Clean dataset...")
        self._clean_dataset()
        logger.info("Canteens: Transform ChoiceFields...")
        self.transform_canteen_choicefields()
        logger.info("Canteens: Transform ArrayFields...")
        self.transform_canteen_arrayfields()


class ETL_OPEN_DATA_TELEDECLARATIONS(etl.EXTRACTOR, OPEN_DATA):
    def __init__(self, year: int):
        super().__init__()
        self.years = [year]
        self.year = year
        self.dataset_name = f"campagne_td_{year}"
        self.datagouv_dataset_id = MA_CANTINE_DATAGOUV_TELEDECLARATION_DATASET_ID
        self.schema = json.load(open(MA_CANTINE_DATAGOUV_TELEDECLARATION_SCHEMA_FILE_PATH))
        self.schema_url = MA_CANTINE_DATAGOUV_TELEDECLARATION_SCHEMA_URL
        self.view = DiagnosticTeledeclaredOpenDataListView
        self.df = None

    def transform_dataset(self):
        logger.info("TD campagne: Clean dataset...")
        self._clean_dataset()
        logger.info("TD campagne: Format the decimals...")
        self._format_decimals(["teledeclaration_ratio_bio", "teledeclaration_ratio_egalim_hors_bio"])
        logger.info("TD campagne: Transform ChoiceFields...")
        self.transform_canteen_choicefields(prefix="canteen_")
        logger.info("TD campagne: Transform Canteen ArrayFields...")
        self.transform_canteen_arrayfields(prefix="canteen_")
        logger.info("TD campagne: Fill geo name...")
        self.transform_canteen_geo_data(prefix="canteen_")
        # TODO: self.flatten_central_kitchen_td()
