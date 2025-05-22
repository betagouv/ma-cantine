import csv
import json
import logging
import os
import time
from abc import ABC, abstractmethod

import pandas as pd
import requests
from django.core.files.storage import default_storage

from data.department_choices import Department
from data.models import Canteen, Teledeclaration
from data.region_choices import Region
from macantine.etl.utils import common_members, filter_empty_values, format_geo_name
from macantine.utils import CAMPAIGN_DATES

logger = logging.getLogger(__name__)


class ETL(ABC):
    """
    Interface for the different ETL
    """

    def __init__(self):
        self.df = None
        self.schema = None
        self.schema_url = ""
        self.dataset_name = ""

    def fill_geo_names(self, prefix=""):
        """
        Given a dataframe with columns 'department' and 'region', this method maps the name of the location, based on the INSEE code
        Returns:
            pd.DataFrame: The dataset with two new columns : department_lib and region_lib
        """
        geo_data = {"department": {i.value: i.label for i in Department}, "region": {i.value: i.label for i in Region}}
        for geo_zoom in ["department", "region"]:
            col_geo_zoom = f"{prefix}{geo_zoom}"
            col_to_insert = self.df[col_geo_zoom].apply(lambda x: format_geo_name(x, geo_data[geo_zoom]))
            if f"{col_geo_zoom}_lib" in self.df.columns:
                del self.df[f"{col_geo_zoom}_lib"]
            self.df.insert(self.df.columns.get_loc(col_geo_zoom) + 1, f"{col_geo_zoom}_lib", col_to_insert)

    def get_schema(self):
        return self.schema

    def get_dataset(self):
        return self.df

    def len_dataset(self):
        if isinstance(self.df, pd.DataFrame):
            return len(self.df)
        else:
            return 0

    def is_valid(self, filepath) -> bool:
        # In order to validate the dataset with the validata api, must first convert to CSV then save online
        with default_storage.open(filepath + "_to_validate.csv", "w") as file:
            self.df.to_csv(
                file,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
                quoting=csv.QUOTE_NONE,
            )
        dataset_to_validate_url = (
            f"{os.environ['CELLAR_HOST']}/{os.environ['CELLAR_BUCKET_NAME']}/media/{filepath}_to_validate.csv"
        )

        res = requests.get(
            f"https://api.validata.etalab.studio/validate?schema={self.schema_url}&url={dataset_to_validate_url}&header_case=true"
        )
        report = json.loads(res.text)["report"]
        if len(report["errors"]) > 0 or report["stats"]["errors"] > 0:
            logger.error(f"The dataset {self.dataset_name} extraction has errors : ")
            logger.error(report["errors"])
            logger.error(report["tasks"])
            return False
        else:
            return True

    def _format_decimals(self, columns):
        for col in columns:
            self.df[col] = self.df[col].apply(lambda x: round(x, 4) if not pd.isnull(x) else x)


class EXTRACTOR(ETL):
    @abstractmethod
    def extract_dataset(self):
        pass


class TRANSFORMER_LOADER(ETL):
    @abstractmethod
    def transform_dataset(self):
        pass

    @abstractmethod
    def load_dataset(self):
        pass


class TELEDECLARATIONS(EXTRACTOR):
    def __init__(self):
        self.years = []
        self.columns = []

    def filter_aberrant_td(self):
        """
        Filtering out the teledeclarations that :
        *  products > 1 million €
        AND
        * an avg meal cost > 20 €
        """
        mask = (self.df["teledeclaration.value_total_ht"] > 1000000) & (
            self.df["teledeclaration.value_total_ht"] / self.df["yearly_meal_count"] > 20
        )
        self.df = self.df[~mask]

    def filter_teledeclarations(self):
        """
        Filter teledeclarations for empty values."""

        self.df = filter_empty_values(self.df, col_name="teledeclaration.value_total_ht")
        self.df = filter_empty_values(self.df, col_name="teledeclaration.value_bio_ht")
        self.filter_aberrant_td()

    def extract_dataset(self) -> pd.DataFrame:
        self.df = pd.DataFrame()
        for year in self.years:
            if year in CAMPAIGN_DATES.keys():
                df_year = pd.DataFrame(Teledeclaration.objects.for_stat(year).values())
                self.df = pd.concat([self.df, df_year])
            else:
                logger.warning(f"TD dataset does not exist for year : {year}")
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe with columns from the schema")
            self.df = pd.DataFrame(columns=self.columns)


class CANTEENS(EXTRACTOR):
    def __init__(self):
        super().__init__()
        self.exclude_filter = None
        self.columns = []

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
