import math
import pandas as pd
import json
import logging
import os
import datetime

from validata_core import validate
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
        self.dataset_name = ""

    def _fill_geo_name(self):
        departments = {i.value: i.label for i in Department}
        regions = {i.value: i.label for i in Region}

        if "department" in self.df.columns:  # Registre cantine dataset
            dep_col_name = "department"
            region_col_name = "region"
        else:  # Td dataset
            dep_col_name = "canteen_department"
            region_col_name = "canteen_region"

        # Cleaning col that were created empty from schema
        del self.df[f"{dep_col_name}_lib"], self.df[f"{region_col_name}_lib"]

        self.df.insert(
            self.df.columns.get_loc(dep_col_name) + 1,
            f"{dep_col_name}_lib",
            self.df[dep_col_name].apply(lambda x: departments[x].split("-")[1].lstrip() if isinstance(x, str) else None),
        )
        self.df.insert(
            self.df.columns.get_loc(region_col_name) + 1,
            f"{region_col_name}_lib",
            self.df[region_col_name].apply(lambda x: regions[x].split("-")[1].lstrip() if isinstance(x, str) else None),
        )
        return self.df

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
            self.df.apply(lambda x: "Restaurants des armées/police/gendarmerie" not in str(x[sector_col_name]), axis=1)
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
        # We should be able to pass directly the dataframe but there is currently a bug in validata
        # link to the issue here : https://gitlab.com/validata-table/validata-table/-/issues/138
        report = validate(f"media/open_data/{self.dataset_name}_to_validate.csv", self.schema)
        if len(report["errors"]) > 0:
            logger.error(f'The dataset {self.dataset_name} extraction has errors : ')
            logger.error(report['errors'])
            return 0
        else:
            return 1

    def export_dataset(self, stage='to_validate'):
        if stage == 'to_validate':
            filename = f"open_data/{self.dataset_name}_to_validate.csv"
        else:
            filename = f"open_data/{self.dataset_name}.csv"
        with default_storage.open(filename, "w") as file:
            self.df.to_csv(file, sep=";", index=False, na_rep="")


class ETL_CANTEEN(ETL):
    def __init__(self):
        super().__init__()
        self.dataset_name = 'registre_cantines'
        self.schema = json.load(open("data/schemas/schema_cantine.json"))

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
        self.df = self._fill_geo_name()


class ETL_TD(ETL):
    def __init__(self, year: int):
        super().__init__()
        self.year = year
        self.dataset_name = f'campagne_td_{year}'
        self.schema = json.load(open("data/schemas/schema_teledeclaration.json"))

    def extract_dataset(self):
        if self.year == 2021:
            self.df = pd.DataFrame(
                Teledeclaration.objects.filter(
                    year=self.year,
                    creation_date__range=(datetime.date(2022, 7, 17), datetime.date(2022, 12, 15)),
                    status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
                    canteen_id__isnull=False,
                ).values()
            )
        else:
            self.df = pd.DataFrame(
                Teledeclaration.objects.filter(
                    year=self.year, status=Teledeclaration.TeledeclarationStatus.SUBMITTED
                ).values()
            )
        if len(self.df) == 0:
            logger.warning(f"TD campagne dataset is empty for year : {self.year}")
            return self.df
        logger.info("TD campagne : Flatten declared data...")
        self.df = self._flatten_declared_data()
        self.df["teledeclaration_ratio_bio"] = self.df["teledeclaration.value_bio_ht"] / self.df["teledeclaration.value_total_ht"]
        self.df["teledeclaration_ratio_egalim_hors_bio"] = (
            self.df["teledeclaration.value_sustainable_ht"] / self.df["teledeclaration.value_total_ht"]
        )
        logger.info("TD campagne : Clean dataset...")
        self.df = self._clean_dataset()
        logger.info("TD campagne : Filter by sector...")
        self.df = self._filter_by_sectors()
        logger.info("TD campagne : Fill geo name...")
        self.df = self._fill_geo_name()

    def _flatten_declared_data(self):
        tmp_df = pd.json_normalize(self.df["declared_data"])
        self.df = pd.concat([self.df.drop("declared_data", axis=1), tmp_df], axis=1)
        return self.df
