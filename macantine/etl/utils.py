import logging
import warnings
from typing import Dict

import numpy as np
import pandas as pd

from macantine.etl.data_ware_house import DataWareHouse

warnings.filterwarnings("ignore", message="SparkPandasCompare currently only supports Numpy < 2")  # Needed for the CI
logger = logging.getLogger(__name__)


def compute_percentage(valueKey, totalKey, ratio=False):
    """
    Compute a percentage (between 0 and 100) or a ratio (between 0 and 1).
    """
    if totalKey and valueKey:
        if totalKey > 0 and valueKey >= 0:
            if ratio:
                return float(valueKey / totalKey)
            return float(100 * valueKey / totalKey)


def format_td_sector_column(row: pd.Series, sector_col_name: str):
    """
    Splitting sectors information into two new columns, one for the sector, one for the category
    If there are multiple sectors, we
    """
    x = row[sector_col_name]
    if type(x) is list:
        if len(x) > 1:
            return "Secteurs multiples", "Catégories multiples"
        elif len(x) == 1:
            return x[0]["name"], x[0]["category"]
    return np.nan, np.nan


def map_sectors():
    """
    Populate the details of a sector, given its id
    """

    from api.serializers import SectorM2MSerializer  # avoid circular import
    from data.models import SectorM2M

    sectors = SectorM2M.objects.all()
    sectors_mapper = {}
    for sector in sectors:
        sector = SectorM2MSerializer(sector).data
        sectors_mapper[sector["id"]] = sector
    return sectors_mapper


def filter_empty_values(df: pd.DataFrame, col_name) -> pd.DataFrame:
    """
    Filtering out the teledeclarations for wich a certain field is empty
    """
    return df.dropna(subset=col_name)


def format_geo_name(geo_code: int, geo_names: Dict[int, str]):
    """
    Format the name of a region or department from its code
    """
    if isinstance(geo_code, str) and geo_code not in ["978", "987", "975", "988"]:
        geo_name = geo_names[geo_code].split(" - ")[1].lstrip()
        return geo_name


def format_sector(sector: dict) -> str:
    return f'""{sector["name"]}""'


def format_category(sector: dict) -> str:
    return f'""{sector["category"]}""'


def format_list(sectors) -> str:
    return f'"[{", ".join(sectors)}]"'


def format_list_to_single_value(values, col_name) -> str:
    """
    Splitting sectors information into two new columns, one for the sector, one for the category
    If there are multiple sectors, we
    """
    if type(values) is list:
        if len(values) > 1:
            return f"{col_name} multiples"
        elif len(values) == 1:
            return values[0].replace('"', "")
    return np.nan


def fetch_sector(sector_id, sectors):
    if sector_id and sector_id in sectors.keys():
        sector = sectors[sector_id]
        return format_sector(sector)
    else:
        return ""


def fetch_category(sector_id, sectors):
    if sector_id and sector_id in sectors.keys():
        sector = sectors[sector_id]
        return format_category(sector)
    else:
        return ""


def datetimes_to_str(df):
    date_columns = df.select_dtypes(include=["datetime64[ns, UTC]"]).columns
    for date_column in date_columns:
        df[date_column] = df[date_column].apply(lambda x: x.strftime("%Y-%m-%d %H:%M"))
    return df


def compare_datasets(table_version_A, table_version_B):
    """
    Prints an evaluation report that compares two versions of a dataset stored in the data-warehouse.
    """
    import datacompy

    warehouse = DataWareHouse()

    print("\n###### Evaluation Report #######\n")
    print(f"Version A: {table_version_A} \n")
    print(f"Version B: {table_version_B} \n")
    dfA = warehouse.read_dataframe(table_version_A)
    dfB = warehouse.read_dataframe(table_version_B)
    compare = datacompy.PandasCompare(dfA, dfB, on_index=True)
    print(compare.report())
