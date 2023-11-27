import pandas as pd
import datetime
import math
import logging
import requests
import json
import os

from abc import ABC, abstractmethod
from data.department_choices import Department
from data.region_choices import Region
from data.models import Canteen, Teledeclaration, Sector
from api.serializers import SectorSerializer
from api.views.utils import camelize
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class ETL(ABC):
    def __init__(self):
        self.df = None
        self.schema = None
        self.schema_url = ""
        self.dataset_name = ""

    def _fill_geo_name(self, geo_zoom="department"):
        """
        Given a dataframe with a column 'department' or 'region', this method maps the name of the location, based on the INSEE code
        Returns:
            pd.Series: The names of the location corresponding to an INSEE code, for each line of the dataset
        """
        if geo_zoom == "department":
            geo = {i.value: i.label for i in Department}
        elif geo_zoom == "region":
            geo = {i.value: i.label for i in Region}
        else:
            logger.warning(
                "The desired geo zoom for the method _fill_geo_zoom() is not possible. Please choose between 'department' and 'region'"
            )
            return 0

        if "department" not in self.df.columns:  # TD dataset
            geo_zoom = "canteen_" + geo_zoom

        # Cleaning col that were created empty from schema
        del self.df[f"{geo_zoom}_lib"]

        self.df[f"{geo_zoom}_lib"] = self.df[geo_zoom].apply(
            lambda x: geo[x].split(" - ")[1].lstrip() if isinstance(x, str) else None
        )

        return self.df[f"{geo_zoom}_lib"]

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
        return self.df

    def _extract_sectors(self):
        # Fetching sectors information and aggreting in list in order to have only one row per canteen
        self.df["sectors"] = self.df["sectors"].apply(
            lambda x: camelize(SectorSerializer(Sector.objects.get(id=x)).data) if (x and not math.isnan(x)) else ""
        )
        canteens_sectors = self.df.groupby("id")["sectors"].apply(list).apply(lambda x: x if x != [""] else [])
        del self.df["sectors"]

        return self.df.merge(canteens_sectors, on="id")

    def _filter_by_sectors(self):
        sector_col_name = "sectors" if "sectors" in self.df.columns else "canteen_sectors"
        return self.df[
            self.df.apply(
                lambda x: "Restaurants des armées/police/gendarmerie" not in str(x[sector_col_name]),
                axis=1,
            )
        ]

    @abstractmethod
    def extract_dataset(self):
        pass

    def get_schema(self):
        return self.schema

    def get_dataset(self):
        return self.df

    def len_dataset(self):
        if isinstance(self.df, pd.DataFrame):
            return len(self.df)
        else:
            return 0

    def is_valid(self) -> bool:
        dataset_to_validate_url = f"{os.environ['CELLAR_HOST']}/{os.environ['CELLAR_BUCKET_NAME']}/media/open_data/{self.dataset_name}_to_validate.csv"
        schema_url = "https://github.com/betagouv/ma-cantine/blob/staging/data/schemas/schema_teledeclaration.json"

        res = requests.get(
            f"https://api.validata.etalab.studio/validate?schema={schema_url}&url={dataset_to_validate_url}&header_case=true"
        )
        report = json.loads(res.text)["report"]
        if len(report["errors"]) > 0:
            logger.error(f"The dataset {self.dataset_name} extraction has errors : ")
            logger.error(report["errors"])
            return 0
        else:
            return 1

    def export_dataset(self, stage="to_validate"):
        if stage == "to_validate":
            filename = f"open_data/{self.dataset_name}_to_validate.csv"
        else:
            filename = f"open_data/{self.dataset_name}.csv"
        with default_storage.open(filename, "w") as file:
            self.df.to_csv(file, sep=";", index=False, na_rep="")


class ETL_CANTEEN(ETL):
    def __init__(self):
        super().__init__()
        self.dataset_name = "registre_cantines"
        self.schema = json.load(open("data/schemas/schema_cantine.json"))
        self.schema_url = (
            "https://raw.githubusercontent.com/betagouv/ma-cantine/staging/data/schemas/schema_cantine.json"
        )

    def extract_dataset(self):
        all_canteens_col = [i["name"] for i in self.schema["fields"]]
        canteens_col_from_db = all_canteens_col.copy()
        canteens_col_from_db.remove("active_on_ma_cantine")
        canteens_col_from_db.remove("department_lib")
        canteens_col_from_db.remove("region_lib")

        all_canteens = Canteen.objects.filter(deletion_date__isnull=True)
        if all_canteens.count() == 0:
            return pd.DataFrame(columns=canteens_col_from_db)

        active_canteens_id = Canteen.objects.exclude(managers=None).values_list("id", flat=True)

        # Creating a dataframe with all canteens. The canteens can have multiple lines if they have multiple sectors
        self.df = pd.DataFrame(all_canteens.values(*canteens_col_from_db))

        # Adding the active_on_ma_cantine column
        self.df["active_on_ma_cantine"] = self.df["id"].apply(lambda x: x in active_canteens_id)

        logger.info("Canteens : Extract sectors...")
        self.df = self._extract_sectors()
        logger.info("Canteens : Filter by sectors...")
        self.df = self._filter_by_sectors()

        bucket_url = os.environ.get("CELLAR_HOST")
        bucket_name = os.environ.get("CELLAR_BUCKET_NAME")
        self.df["logo"] = self.df["logo"].apply(lambda x: f"{bucket_url}/{bucket_name}/media/{x}" if x else "")

        logger.info("Canteens : Clean dataset...")
        self.df = self._clean_dataset()
        logger.info("Canteens : Fill geo name...")
        self.df["department_lib"] = self._fill_geo_name(geo_zoom="department")
        self.df["region_lib"] = self._fill_geo_name(geo_zoom="region")


class ETL_TD(ETL):
    def __init__(self, year: int):
        super().__init__()
        self.year = year
        self.dataset_name = f"campagne_td_{year}"
        self.schema = json.load(open("data/schemas/schema_teledeclaration.json"))
        self.schema_url = (
            "https://raw.githubusercontent.com/betagouv/ma-cantine/staging/data/schemas/schema_teledeclaration.json"
        )
        self.categories_to_aggregate = {
            "bio": ["_bio"],
            "sustainable": ["_sustainable", "_label_rouge", "_aocaop_igp_stg"],
            "egalim_others": ["_egalim_others", "_hve", "_peche_durable", "_rup", "_fermier", "_commerce_equitable"],
            "externality_performance": ["_externality_performance", "_performance", "_externalites"],
        }

    def extract_dataset(self):
        if self.year == 2021:
            self.df = pd.DataFrame(
                Teledeclaration.objects.filter(
                    year=self.year,
                    creation_date__range=(
                        datetime.date(2022, 7, 17),
                        datetime.date(2022, 12, 15),
                    ),
                    status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
                    canteen_id__isnull=False,
                ).values()
            )
        else:
            self.df = pd.DataFrame(
                Teledeclaration.objects.filter(
                    year=self.year,
                    status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
                ).values()
            )
        if len(self.df) == 0:
            logger.warning(f"TD campagne dataset is empty for year : {self.year}")
            return self.df

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
        self.df["teledeclaration_type"] = self.df["teledeclaration.diagnostic_type"]  # Renaming to match schema

        logger.info("TD campagne : Clean dataset...")
        self.df = self._clean_dataset()
        logger.info("TD campagne : Filter by sector...")
        self.df = self._filter_by_sectors()
        logger.info("TD campagne : Fill geo name...")
        self.df["canteen_department_lib"] = self._fill_geo_name(geo_zoom="department")
        self.df["canteen_region_lib"] = self._fill_geo_name(geo_zoom="region")

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
