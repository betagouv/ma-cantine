import logging
import warnings
from typing import Dict

import numpy as np
import pandas as pd

from data.models import Sector, Teledeclaration
from data.models.sector import SECTEURS_SPE
from macantine.etl.data_ware_house import DataWareHouse

warnings.filterwarnings("ignore", message="SparkPandasCompare currently only supports Numpy < 2")  # Needed for the CI
logger = logging.getLogger(__name__)

# Source : query Resytal dec 2023
ESTIMATED_NUMBER_CANTEENS_REGION = {
    1: 625,
    2: 554,
    3: 161,
    4: 900,
    6: 203,
    11: 13235,
    24: 4171,
    27: 3623,
    28: 4360,
    32: 7061,
    44: 7324,
    52: 4545,
    53: 4279,
    75: 8854,
    76: 7336,
    84: 10842,
    93: 5991,
    94: 395,
}


def get_nbre_cantines_region(region: int):
    if region in ESTIMATED_NUMBER_CANTEENS_REGION.keys():
        return ESTIMATED_NUMBER_CANTEENS_REGION[region]
    else:
        return np.nan


def get_objectif_zone_geo(department: int):
    if department and department != "nan" and not pd.isna(department):
        # Dealing with two string codes
        if department == "2A" or department == "2B":
            return "France métropolitaine"
        department = int(department)
        if department >= 1 and department <= 95:
            return "France métropolitaine"
        elif department == 976:
            return "DROM (Mayotte)"
        elif department >= 971 and department <= 978:
            return "DROM (hors Mayotte)"
    return "non renseigné"


def sum_int_and_none(values_to_sum: list):
    values_to_sum = [x or 0 for x in values_to_sum]
    return int(np.sum(values_to_sum))


def common_members(a, b):
    return set(a) & set(b)


def compute_ratio(valueKey, totalKey):
    if totalKey and valueKey:
        if totalKey > 0 and valueKey >= 0:
            return 100 * valueKey / totalKey


def map_canteens_td(year):
    """
    Populate mapper for a given year. The mapper indicates if one canteen has participated in campaign
    """
    # Check and fetch Teledeclaration data from the database
    tds = Teledeclaration.objects.submitted_for_year(year).values("canteen_id", "declared_data")

    # Populate the mapper for the given year
    participation = []
    for td in tds:
        participation.append(td["canteen_id"])
        if "satellites" in td["declared_data"]:
            for satellite in td["declared_data"]["satellites"]:
                participation.append(satellite["id"])
    return participation


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


def extract_sectors(
    df: pd.DataFrame, extract_spe: bool, split_category_and_sector: bool, only_one_value: bool
) -> pd.DataFrame:
    """
    This function processes the 'sectors' data in the input DataFrame by:
    1. Mapping each sector to its corresponding value.
    2. Aggregating sectors per canteen (one row per canteen).
    3. Merging the aggregated sector information back into the original DataFrame.

    Args:
    - df (pd.DataFrame): The input DataFrame that contains canteen data, including a 'sectors' column.
    - extract_spe (boolean): Add the 'spe' column that indicates if the canteen is part of Secteur Public Ecoresponsable
    - split_category_and_sector (boolean):
    - only_one_value (boolean):

    Returns:
    - pd.DataFrame: The updated DataFrame with the sectors aggregated per canteen.
    """

    sector_mapping = map_sectors()
    if extract_spe:
        df["spe"] = df["sectors"].apply(lambda x: True if x in SECTEURS_SPE else False)
        aggregated_sectors_spe = df.groupby("id")["spe"].max()
        df = df.drop(columns=["spe"])
        df = df.merge(aggregated_sectors_spe, on="id")

    if split_category_and_sector:
        df["categories"] = df["sectors"].apply(lambda sector: fetch_category(sector, sector_mapping))
        if only_one_value:
            aggregated_categories = (
                df.groupby("id")["categories"]
                .apply(list)
                .apply(lambda x: format_list_to_single_value(x, "Catégories"))
            )
        else:
            aggregated_categories = df.groupby("id")["categories"].apply(list).apply(format_list)
        df = df.drop(columns=["categories"])
        df = df.merge(aggregated_categories, on="id")

    df["sectors"] = df["sectors"].apply(lambda sector: fetch_sector(sector, sector_mapping))
    if only_one_value:
        aggregated_sectors = (
            df.groupby("id")["sectors"].apply(list).apply(lambda x: format_list_to_single_value(x, "Secteurs"))
        )
    else:
        aggregated_sectors = df.groupby("id")["sectors"].apply(list).apply(format_list)

    df = df.drop(columns=["sectors"])
    df = df.merge(aggregated_sectors, on="id")

    return df


def map_sectors():
    """
    Populate the details of a sector, given its id
    """

    from api.serializers import SectorSerializer  # avoid circular import

    sectors = Sector.objects.all()
    sectors_mapper = {}
    for sector in sectors:
        sector = SectorSerializer(sector).data
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


def filter_dataframe_with_schema_cols(df, schema: Dict):
    columns = [i["name"] for i in schema["fields"]]
    df = df.loc[:, ~df.columns.duplicated()].copy()
    df = df[columns]
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
    compare = datacompy.Compare(dfA, dfB, on_index=True)
    print(compare.report())
