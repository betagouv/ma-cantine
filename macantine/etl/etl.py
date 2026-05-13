import logging
import time
from abc import ABC, abstractmethod

import pandas as pd
from django.core.files.storage import default_storage

from common.api import validata
from data.models.geo import Department, Region
from macantine.etl.utils import format_geo_name

logger = logging.getLogger(__name__)


class ETL(ABC):
    """
    Interface for the different ETL
    """

    def __init__(self):
        self.df = None
        self.dataset_name = ""
        self.schema = None
        self.schema_url = ""
        self.columns = []
        self.view = None

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
        """
        Validates the dataset against the schema using Validata API.
        It creates a temporary csv file with only 1000 rows (to avoid sending too big files to Validata) and checks the response.
        """
        to_validate_path = f"{filepath}_to_validate.csv"
        df_to_validate = self.df.head(1000).copy()
        with default_storage.open(to_validate_path, "w") as file:
            df_to_validate.to_csv(
                file,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
            )
        with default_storage.open(to_validate_path, "rb") as file:
            validata_response = validata.validate_file_against_schema(file, self.schema_url)
        if "error" in validata_response:
            logger.error(validata_response["error"])
            return False
        report = validata_response["report"]
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
    def extract_dataset(self):
        start = time.time()
        view = self.view()
        if hasattr(self, "year"):  # For Analysis Telececlarations
            queryset = view.get_queryset(self.year)
        else:
            queryset = view.get_queryset()
        serializer = view.get_serializer_class()
        data = serializer(queryset, many=True).data
        self.df = pd.DataFrame(data)
        if self.df.empty:
            logger.warning("Dataset is empty. Creating an empty dataframe with columns from the schema")
            self.df = pd.DataFrame(columns=self.columns)
        end = time.time()
        logger.info(f"Time spent on {self.dataset_name} extraction: {end - start:.2f} seconds")


class TRANSFORMER_LOADER(ETL):
    @abstractmethod
    def transform_dataset(self):
        pass

    @abstractmethod
    def load_dataset(self):
        pass
