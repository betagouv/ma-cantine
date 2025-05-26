import csv
import json
import os
import time
from io import BytesIO

import pandas as pd
from django.core.files.storage import default_storage
from django.db.models import Q

import macantine.etl.utils
from api.views.teledeclaration import TeledeclarationOpenDataListView
from common.api.decoupage_administratif import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)
from data.models import Canteen
from macantine.etl import etl
from macantine.etl.etl import logger
from macantine.etl.utils import common_members, extract_sectors


class OPEN_DATA(etl.TRANSFORMER_LOADER):
    """
    Abstract class implementing the specifity for open data export
    """

    def transform_canteen_choice_fields(self, prefix=""):
        # line_ministry
        self.df[prefix + "line_ministry"] = self.df[prefix + "line_ministry"].apply(
            lambda x: Canteen.Ministries(x).label if (x in Canteen.Ministries) else None
        )

    def transform_canteen_geo_data(self, prefix=""):
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
        columns = [i["name"].replace("canteen_", "canteen.") for i in self.schema["fields"]]

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

    def _load_data_parquet(self, filename):
        with default_storage.open(filename + ".parquet", "wb") as parquet_file:
            if "sectors" in self.df.columns:
                self.df.sectors = self.df.sectors.astype(str)
            self.df.to_parquet(parquet_file)

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
            os.environ.get("STATICFILES_STORAGE") == "dstorages.backends.s3boto3.S3StaticStorage"
            and os.environ.get("DEFAULT_FILE_STORAGE") == "storages.backends.s3boto3.S3Boto3Storage"
        ):
            if not self.is_valid():
                logger.error(f"The dataset {self.name} is invalid and therefore will not be exported to s3")
                return
        try:
            self._load_data_csv(filepath)
            self._load_data_parquet(filepath)
            self._load_data_xlsx(filepath)

            macantine.etl.utils.update_datagouv_resources()
        except Exception as e:
            logger.error(f"Error saving validated data: {e}")


class ETL_OPEN_DATA_CANTEEN(etl.EXTRACTOR, OPEN_DATA):
    def __init__(self):
        super().__init__()
        self.dataset_name = "registre_cantines"
        self.schema = json.load(open("data/schemas/export_opendata/schema_cantines.json"))
        self.schema_url = "https://raw.githubusercontent.com/betagouv/ma-cantine/staging/data/schemas/export_opendata/schema_cantines.json"
        self.columns = [field["name"] for field in self.schema["fields"]]
        self.canteens = None
        self.exclude_filter = Q(sectors__id=22) | Q(line_ministry="armee")  # Filtering out the police / army sectors

    def extract_dataset(self):
        start = time.time()
        canteens = Canteen.objects.all()
        if self.exclude_filter:
            canteens = Canteen.objects.exclude(self.exclude_filter)
        if canteens.count() == 0:
            self.df = pd.DataFrame(columns=self.columns)
        else:
            # Creating a dataframe with all canteens. The canteens can have multiple lines if they have multiple sectors
            columns_model = [field.name for field in Canteen._meta.get_fields()]
            columns_to_extract = common_members(self.columns, columns_model)
            self.df = pd.DataFrame(canteens.values(*columns_to_extract))
        end = time.time()
        logger.info(f"Time spent on canteens extraction : {end - start}")

    def transform_dataset(self):
        all_canteens_col = [i["name"] for i in self.schema["fields"]]
        self.canteens_col_from_db = all_canteens_col
        for col_processed in [
            "active_on_ma_cantine",
            "declaration_donnees_2021",
            "declaration_donnees_2022",
            "declaration_donnees_2023",
            "declaration_donnees_2024_en_cours",
        ]:
            self.canteens_col_from_db.remove(col_processed)

        # Adding the active_on_ma_cantine column
        start = time.time()
        non_active_canteens = Canteen.objects.filter(managers=None).values_list("id", flat=True)
        end = time.time()
        logger.info(f"Time spent on active canteens : {end - start}")
        self.df["active_on_ma_cantine"] = self.df["id"].apply(lambda x: x not in non_active_canteens)

        logger.info("Canteens : Extract sectors...")
        self.df = extract_sectors(self.df, extract_spe=False, split_category_and_sector=False, only_one_value=False)

        bucket_url = os.environ.get("CELLAR_HOST")
        bucket_name = os.environ.get("CELLAR_BUCKET_NAME")

        if "logo" in self.df.columns:
            self.df["logo"] = self.df["logo"].apply(lambda x: f"{bucket_url}/{bucket_name}/media/{x}" if x else "")

        logger.info("Canteens : Clean dataset...")
        self._clean_dataset()

        logger.info("Canteens : Transform choice fields...")
        self.transform_canteen_choice_fields()

        logger.info("Canteens : Fill geo name...")
        start = time.time()
        self.transform_canteen_geo_data()
        end = time.time()
        logger.info(f"Time spent on geo data : {end - start}")

        logger.info("Canteens : Fill campaign participations...")
        start = time.time()
        for year in [2021, 2022, 2023, 2024]:
            campaign_participation = macantine.etl.utils.map_canteens_td(year)
            if year == 2024:
                col_name_campaign = f"declaration_donnees_{year}_en_cours"
            else:
                col_name_campaign = f"declaration_donnees_{year}"
            self.df[col_name_campaign] = self.df["id"].apply(lambda x: x in campaign_participation)
        end = time.time()
        logger.info(f"Time spent on campaign participations : {end - start}")


class ETL_OPEN_DATA_TELEDECLARATIONS(etl.EXTRACTOR, OPEN_DATA):
    def __init__(self, year: int):
        super().__init__()
        self.years = [year]
        self.year = year
        self.dataset_name = f"campagne_td_{year}"
        self.schema = json.load(open("data/schemas/export_opendata/schema_teledeclarations.json"))
        self.schema_url = "https://raw.githubusercontent.com/betagouv/ma-cantine/staging/data/schemas/export_opendata/schema_teledeclarations.json"
        self.view = TeledeclarationOpenDataListView

        self.categories_to_aggregate = {
            "bio": ["_bio"],
            "sustainable": ["_sustainable", "_label_rouge", "_aocaop_igp_stg"],
            "egalim_others": [
                "_egalim_others",
                "_hve",
                "_peche_durable",
                "_rup",
                "_fermier",
                "_commerce_equitable",
            ],
            "externality_performance": [
                "_externality_performance",
                "_performance",
                "_externalites",
            ],
        }
        self.df = None

    def transform_sectors(self) -> pd.Series:
        sectors = self.df["canteen_sectors"]
        if not sectors.isnull().all():
            sectors = sectors.apply(lambda x: list(map(lambda y: macantine.etl.utils.format_sector(y), x)))
            sectors = sectors.apply(macantine.etl.utils.format_list)
        return sectors

    def transform_dataset(self):
        logger.info("TD campagne : Flatten declared data...")
        self.df = self._flatten_declared_data()

        logger.info("TD campagne : Aggregate appro data for complete TD...")
        self._aggregate_complete_td()

        self.df["teledeclaration_ratio_bio"] = (
            self.df["teledeclaration.value_bio_ht"] / self.df["teledeclaration.value_total_ht"]
        )
        self.df["teledeclaration_ratio_egalim_hors_bio"] = (
            self.df["teledeclaration.value_sustainable_ht"] / self.df["teledeclaration.value_total_ht"]
        )

        # Renaming to match schema
        if "teledeclaration.diagnostic_type" in self.df.columns:
            self.df["teledeclaration_type"] = self.df["teledeclaration.diagnostic_type"]
        if "central_kitchen_siret" in self.df.columns:
            self.df["canteen.central_kitchen_siret"] = self.df["central_kitchen_siret"]

        logger.info("TD campagne : Clean dataset...")
        self._clean_dataset()
        logger.info("TD campagne : Format the decimals...")
        self._format_decimals(["teledeclaration_ratio_bio", "teledeclaration_ratio_egalim_hors_bio"])
        logger.info("TD campagne : Filter by ministry...")
        self._filter_by_ministry()
        logger.info("TD campagne : Filter errors...")
        self._filter_outsiders()
        logger.info("TD campagne : Transform choice fields...")
        self.transform_canteen_choice_fields(prefix="canteen_")
        logger.info("TD campagne : Transform sectors...")
        self.df["canteen_sectors"] = self.transform_sectors()
        logger.info("TD Campagne : Fill geo name...")
        self.transform_canteen_geo_data(prefix="canteen_")

    def _flatten_declared_data(self):
        tmp_df = pd.json_normalize(self.df["declared_data"])
        self.df = pd.concat([self.df.drop("declared_data", axis=1), tmp_df], axis=1)
        return self.df

    def _aggregation_col(self, categ="bio", sub_categ=["_bio"]):
        pattern = "|".join(sub_categ)
        self.df[f"teledeclaration.value_{categ}_ht"] = self.df.filter(regex=pattern).sum(
            axis=1, numeric_only=True, skipna=True, min_count=1
        )

    def _aggregate_complete_td(self):
        """
        Aggregate the columns of a complete TD for an appro category if the total value of this category is not specified.
        """
        for categ, elements_in_categ in self.categories_to_aggregate.items():
            self._aggregation_col(categ, elements_in_categ)

    def _filter_null_values(self):
        "We have decided not take into accounts the TD where the value total or the value bio are null"
        self.df = self.df[~self.df["teledeclaration_ratio_bio"].isnull()]

    def _filter_outsiders(self):
        """
        For the campaign 2023, after analyses, we decided to exclude two TD because their value were impossible
        """
        if self.year == 2022:
            td_with_errors = [9656, 8037]
            self.df = self.df[~self.df["id"].isin(td_with_errors)]

    def _filter_by_ministry(self):
        """
        Filtering the ministry of Armees so they do not appear publicly
        """
        canteens_to_filter = Canteen.objects.filter(line_ministry="armee")
        canteens_id_to_filter = [canteen.id for canteen in canteens_to_filter]
        self.df = self.df[~self.df["canteen_id"].isin(canteens_id_to_filter)]
