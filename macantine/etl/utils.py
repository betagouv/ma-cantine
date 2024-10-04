import logging
import os
import zoneinfo
from datetime import date, datetime
from typing import Dict

import numpy as np
import pandas as pd
import requests

from api.serializers import SectorSerializer
from data.models import Sector, Teledeclaration

logger = logging.getLogger(__name__)

CAMPAIGN_DATES = {
    2021: {
        "start_date": datetime(2022, 7, 16, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2022, 12, 5, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2022: {
        "start_date": datetime(2023, 2, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2023, 7, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2023: {
        "start_date": datetime(2024, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2024, 6, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
}


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
    if os.environ.get("ENVIRONMENT") != "prod":
        return
    dataset_id = os.getenv("DATAGOUV_DATASET_ID", "")
    api_key = os.getenv("DATAGOUV_API_KEY", "")
    if not (dataset_id and api_key):
        logger.error("Datagouv resource update : API key or dataset id incorrect values")
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
        return count_updated_resources
    except requests.HTTPError as e:
        logger.error(f"Datagouv resource update : Error while updating dataset : {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


def map_communes_infos():
    """
    Create a dict that maps cities with their EPCI code
    """
    commune_details = {}
    try:
        logger.info("Starting communes dl")
        response_commune = requests.get("https://geo.api.gouv.fr/communes", timeout=50)
        response_commune.raise_for_status()
        communes = response_commune.json()
        for commune in communes:
            commune_details[commune["code"]] = {}
            if "codeDepartement" in commune.keys():
                commune_details[commune["code"]]["department"] = commune["codeDepartement"]
            if "codeRegion" in commune.keys():
                commune_details[commune["code"]]["region"] = commune["codeRegion"]
            if "codeEpci" in commune.keys():
                commune_details[commune["code"]]["epci"] = commune["codeEpci"]
    except requests.exceptions.HTTPError as e:
        logger.info(e)
        return None
    return commune_details


def map_epcis_code_name():
    try:
        epci_names = {}
        response = requests.get("https://geo.api.gouv.fr/epcis/?fields=nom", timeout=50)
        response.raise_for_status()
        epcis = response.json()
        for epci in epcis:
            epci_names[epci["code"]] = epci["nom"]
        return epci_names
    except requests.exceptions.HTTPError as e:
        logger.info(e)
        return {}


def map_canteens_td(year):
    """
    Populate mapper for a given year. The mapper indicates if one canteen has participated in campaign
    """
    # Check and fetch Teledeclaration data from the database
    tds = Teledeclaration.objects.filter(
        year=year,
        creation_date__range=(
            CAMPAIGN_DATES[year]["start_date"],
            CAMPAIGN_DATES[year]["end_date"],
        ),
        status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
    ).values("canteen_id", "declared_data")

    # Populate the mapper for the given year
    participation = []
    for td in tds:
        participation.append(td["canteen_id"])
        if "satellites" in td["declared_data"]:
            for satellite in td["declared_data"]["satellites"]:
                participation.append(satellite["id"])
    return participation


def map_sectors():
    """
    Populate the details of a sector, given its id
    """
    sectors = Sector.objects.all()
    sectors_mapper = {}
    for sector in sectors:
        sector = SectorSerializer(sector).data
        sectors_mapper[sector["id"]] = sector
    return sectors_mapper


def fetch_teledeclarations(years: list) -> pd.DataFrame:
    df = pd.DataFrame()
    for year in years:
        if year in CAMPAIGN_DATES.keys():
            df_year = pd.DataFrame(
                Teledeclaration.objects.filter(
                    year=year,
                    creation_date__range=(
                        CAMPAIGN_DATES[year]["start_date"],
                        CAMPAIGN_DATES[year]["end_date"],
                    ),
                    status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
                    canteen_id__isnull=False,
                ).values()
            )
            df = pd.concat([df, df_year])
        else:
            logger.warning(f"TD dataset does not exist for year : {year}")
        if len(df) == 0:
            logger.warning("TD dataset is empty for all the specified years")
    return df


def fetch_commune_detail(code_insee_commune, commune_details, geo_detail_type):
    """
    Provide EPCI code/ Department code/ Region code for a city, given the insee code of the city
    """
    if (
        code_insee_commune
        and code_insee_commune in commune_details.keys()
        and geo_detail_type in commune_details[code_insee_commune].keys()
    ):
        return commune_details[code_insee_commune][geo_detail_type]


def fetch_epci_name(code_insee_epci, epcis_names):
    """
    Provide EPCI code for an epci, given its insee code
    """
    if code_insee_epci and code_insee_epci in epcis_names.keys():
        return epcis_names[code_insee_epci]


def format_geo_name(geo_code: int, geo_names: Dict[int, str]):
    """
    Format the name of a region or department from its code
    """
    if isinstance(geo_code, str) and geo_code not in ["978", "987", "975", "988"]:
        geo_name = geo_names[geo_code].split(" - ")[1].lstrip()
        return geo_name


def format_sector(sector: dict) -> str:
    return f'""{sector["name"]}""'


def format_list_sectors(sectors) -> str:
    return f'"[{", ".join(sectors)}]"'


def fetch_sector(sector_id, sectors):
    """
    Provide EPCI code for a city, given the insee code of the city
    """
    if sector_id and sector_id in sectors.keys():
        sector = sectors[sector_id]
        return format_sector(sector)
    else:
        return ""


def datetimes_to_str(df):
    date_columns = df.select_dtypes(include=["datetime64[ns, UTC]"]).columns
    for date_column in date_columns:
        df[date_column] = df[date_column].apply(lambda x: x.strftime("%Y-%m-%d %H:%M"))
    return df
