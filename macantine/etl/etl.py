import logging
from abc import ABC, abstractmethod

from data.department_choices import Department
from data.region_choices import Region
from macantine.etl.utils import format_geo_name

logger = logging.getLogger(__name__)


class ETL(ABC):
    """
    Interface for the different ETL
    """

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

    @abstractmethod
    def extract_dataset(self):
        pass

    @abstractmethod
    def transform_dataset(self):
        pass

    @abstractmethod
    def load_dataset(self):
        pass
