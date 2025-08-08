import logging
import zoneinfo
from datetime import datetime

import redis as r
from django.conf import settings
from django.utils import timezone

from data.region_choices import REGION_HEXAGONE_LIST, Region

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


def convert_date_string_to_datetime(date_string, time_start_or_end="start"):
    """
    Input: 2025-01-07, "start"
    Output: 2025-01-07 00:00:00+01:00
    """
    if date_string:
        try:
            datetime_object = datetime.strptime(date_string, "%Y-%m-%d")
            if time_start_or_end == "end":
                datetime_object = datetime_object.replace(hour=23, minute=59, second=59, microsecond=999999)
            datetime_object = datetime_object.replace(tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
            return datetime_object
        except ValueError:
            logger.warning(f"Invalid date string format: {date_string}")
            return None
    return None


# https://ma-cantine.agriculture.gouv.fr/blog/16/
# TODO: improve (depends on the year)
# groupe 0 : hexagone
# groupe 1 : Guadeloupe, Guyane, Martinique, La Réunion, Saint-Martin
# groupe 2 : Mayotte
# groupe 3 : Saint-Pierre-et-Miquelon
EGALIM_OBJECTIVES = {
    "hexagone": {
        "region_list": REGION_HEXAGONE_LIST
        + [
            Region.saint_barthelemy,
            Region.terres_australes_et_antarctiques_francaises,
            Region.wallis_et_futuna,
            Region.polynesie_francaise,
            Region.nouvelle_caledonie,
            Region.ile_de_clipperton,
        ],
        "bio_percent": 20,
        "egalim_percent": 50,
    },
    "groupe_1": {
        "region_list": [Region.guadeloupe, Region.martinique, Region.guyane, Region.la_reunion, Region.saint_martin],
        "bio_percent": 5,
        "egalim_percent": 20,
    },
    "groupe_3": {"region_list": [Region.saint_pierre_et_miquelon], "bio_percent": 10, "egalim_percent": 30},
    "groupe_2": {"region_list": [Region.mayotte], "bio_percent": 2, "egalim_percent": 5},
}


# TODO: prendre en compte les department, epci, pat & city_insee_code
def get_egalim_group(region_list):
    if region_list and len(region_list):
        for group_name, details in EGALIM_OBJECTIVES.items():
            if any(region in details["region_list"] for region in region_list):
                return group_name
    return "hexagone"  # default


CAMPAIGN_DATES = {
    2021: {
        "teledeclaration_start_date": datetime(2022, 7, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2022, 12, 4, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/Rapport_Bilan_Statistique_EGALIM_2022.pdf",
    },
    2022: {
        "teledeclaration_start_date": datetime(2023, 2, 12, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2023, 6, 30, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/Rapport_Bilan_Statistique_EGALIM_2023.pdf",
    },
    2023: {
        "teledeclaration_start_date": datetime(2024, 1, 8, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2024, 6, 11, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "correction_start_date": datetime(2024, 6, 3, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": datetime(2024, 6, 12, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/Rapport_Bilan_Statistique_EGALIM_2024.pdf",
    },
    2024: {
        "teledeclaration_start_date": (
            convert_date_string_to_datetime(settings.TELEDECLARATION_START_DATE_OVERRIDE)
            or datetime(2025, 1, 7, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "teledeclaration_end_date": (
            convert_date_string_to_datetime(settings.TELEDECLARATION_END_DATE_OVERRIDE, "end")
            or datetime(2025, 4, 6, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "correction_start_date": (
            convert_date_string_to_datetime(settings.CORRECTION_START_DATE_OVERRIDE)
            or datetime(2025, 4, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "correction_end_date": (
            convert_date_string_to_datetime(settings.CORRECTION_END_DATE_OVERRIDE, "end")
            or datetime(2025, 4, 30, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "rapport_parlement_url": None,  # not published yet
    },
    # Note: au moment d'ajouter une nouvelle année :
    # - penser à y ajouter les settings (pour override)
    # - et enlever les settings de l'année précédente
}


def is_in_teledeclaration():
    """
    Check if the current date is within the teledeclaration period.
    """
    now = timezone.now()
    now_campaign_year = now.year - 1
    if now_campaign_year in CAMPAIGN_DATES:
        start_date = CAMPAIGN_DATES[now_campaign_year]["teledeclaration_start_date"]
        end_date = CAMPAIGN_DATES[now_campaign_year]["teledeclaration_end_date"]
        return start_date <= now <= end_date
    return False


def is_in_correction():
    """
    Check if the current date is within the correction period.
    """
    now = timezone.now()
    now_campaign_year = now.year - 1
    if now_campaign_year in CAMPAIGN_DATES:
        if "correction_start_date" in CAMPAIGN_DATES[now_campaign_year]:
            start_date = CAMPAIGN_DATES[now_campaign_year]["correction_start_date"]
            end_date = CAMPAIGN_DATES[now_campaign_year]["correction_end_date"]
            return start_date <= now <= end_date
    return False


def is_in_teledeclaration_or_correction():
    """
    Check if the current date is within the teledeclaration or correction period.
    """
    return is_in_teledeclaration() or is_in_correction()


def get_year_campaign_end_date_or_today_date(year):
    year = int(year)
    if year in CAMPAIGN_DATES.keys():
        return CAMPAIGN_DATES[year]["teledeclaration_end_date"]
    elif year >= timezone.now().year:
        return timezone.now()
    else:
        return None
