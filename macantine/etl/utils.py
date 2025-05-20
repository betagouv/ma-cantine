import logging
import os
from datetime import date
from typing import Dict

import numpy as np
import pandas as pd
import requests

from data.models import Sector, Teledeclaration
from data.models.sector import SECTEURS_SPE

logger = logging.getLogger(__name__)


def common_members(a, b):
    return set(a) & set(b)


def get_ratio(row, valueKey, totalKey):
    tdTotalKey = f"teledeclaration.{totalKey}"
    tdValueKey = f"teledeclaration.{valueKey}"
    if row[tdTotalKey] > 0 and row[tdValueKey] >= 0:
        return 100 * row[tdValueKey] / row[tdTotalKey]
    else:
        return np.nan


def update_datagouv_resources():
    """
    Updating the URL of the different resources dsiplayed on data.gouv.fr in order to force their cache reload and display the correct update dates
    Returns : Number of updated resources
    """
    dataset_id = os.getenv("DATAGOUV_DATASET_ID", "")
    api_key = os.getenv("DATAGOUV_API_KEY", "")
    if not (dataset_id and api_key):
        logger.warning("Datagouv resource update : API key or dataset id incorrect values")
        return

    header = {"X-API-KEY": api_key}
    try:
        response = requests.get(f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}", headers=header)
        response.raise_for_status()
        resources = response.json()["resources"]
        count_updated_resources = 0
        for resource in resources:
            if resource["format"] in ["xlsx", "csv"]:
                today = date.today()
                updated_url = resource["url"].split("?v=")[0] + "?v=" + today.strftime("%Y%m%d")
                response = requests.put(
                    f'https://www.data.gouv.fr/api/1/datasets/{dataset_id}/resources/{resource["id"]}',
                    headers=header,
                    json={"url": updated_url},
                )
                response.raise_for_status()
                count_updated_resources += 1
        logger.info(f"{count_updated_resources} datagouv's ressources have been updated")
        return count_updated_resources
    except requests.HTTPError as e:
        logger.error(f"Datagouv resource update : Error while updating dataset : {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


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
