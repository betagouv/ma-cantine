from django.utils import timezone
import zoneinfo
from datetime import datetime

from django.conf import settings

from common.utils.dates import convert_date_string_to_datetime


CAMPAIGN_DATES = {
    2021: {
        "teledeclaration_start_date": datetime(2022, 7, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2022, 12, 4, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "correction_start_date": None,
        "correction_end_date": None,
        "legifrance_url": "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000046335035/2022-09-29",
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/rapport-bilan-statistique-EGALIM_2022.pdf",
    },
    2022: {
        "teledeclaration_start_date": datetime(2023, 2, 12, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2023, 6, 30, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "correction_start_date": None,
        "correction_end_date": None,
        "legifrance_url": "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000046335035/2022-09-29",
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/rapport-bilan-statistique-EGALIM_2023.pdf",
    },
    2023: {
        "teledeclaration_start_date": datetime(2024, 1, 8, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2024, 6, 11, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "correction_start_date": datetime(2024, 6, 3, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": datetime(2024, 6, 12, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "legifrance_url": "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000046335035/2024-04-13",
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/rapport-bilan-statistique-EGALIM_2024.pdf",
    },
    2024: {
        "teledeclaration_start_date": datetime(2025, 1, 7, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(2025, 4, 6, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_start_date": datetime(2025, 4, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": datetime(2025, 4, 30, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "legifrance_url": "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000046335035/2024-04-13",
        "rapport_parlement_url": "https://ma-cantine.agriculture.gouv.fr/static/documents/rapport-bilan-statistique-EGALIM_2025.pdf",
    },
    2025: {
        "teledeclaration_start_date": datetime(2026, 1, 12, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2026, 4, 15, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "correction_start_date": datetime(2026, 4, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": datetime(2026, 4, 29, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "legifrance_url": "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000046335035/2025-12-04",
        "rapport_parlement_url": None,
    },
    # NOTE: dates approximates ! on en a besoin pour les tests.
    2026: {
        "teledeclaration_start_date": (
            convert_date_string_to_datetime(settings.TELEDECLARATION_START_DATE_OVERRIDE)
            or datetime(2027, 1, 1, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "teledeclaration_end_date": (
            convert_date_string_to_datetime(settings.TELEDECLARATION_END_DATE_OVERRIDE, "end")
            or datetime(2027, 3, 31, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "correction_start_date": convert_date_string_to_datetime(settings.CORRECTION_START_DATE_OVERRIDE) or None,
        "correction_end_date": convert_date_string_to_datetime(settings.CORRECTION_END_DATE_OVERRIDE, "end") or None,
        "legifrance_url": None,
        "rapport_parlement_url": None,
    },
    # Note: au moment d'ajouter une nouvelle année :
    # - penser à y ajouter les settings (pour override dans les environnements non-prod)
    # - et enlever les settings de l'année précédente
}


def is_in_teledeclaration(year=None):
    """
    Check if the current date is within a teledeclaration period.
    If year is passed, double check that it corresponds to the current campaign year.
    """
    now = timezone.now()
    campaign_year = settings.TELEDECLARATION_YEAR_OVERRIDE or now.year - 1
    if year is not None:
        if year != campaign_year:
            return False
    if campaign_year in CAMPAIGN_DATES:
        start_date = CAMPAIGN_DATES[campaign_year]["teledeclaration_start_date"]
        end_date = CAMPAIGN_DATES[campaign_year]["teledeclaration_end_date"]
        return start_date <= now <= end_date
    return False


def is_in_correction(year=None):
    """
    Check if the current date is within a correction period.
    If year is passed, double check that it corresponds to the current campaign year.
    """
    now = timezone.now()
    campaign_year = settings.TELEDECLARATION_YEAR_OVERRIDE or now.year - 1
    if year is not None:
        if year != campaign_year:
            return False
    if campaign_year in CAMPAIGN_DATES:
        if CAMPAIGN_DATES[campaign_year]["correction_start_date"]:
            start_date = CAMPAIGN_DATES[campaign_year]["correction_start_date"]
            end_date = CAMPAIGN_DATES[campaign_year]["correction_end_date"]
            return start_date <= now <= end_date
    return False


def is_in_teledeclaration_or_correction(year=None):
    """
    Check if the current date is within the teledeclaration or correction period.
    """
    return is_in_teledeclaration(year) or is_in_correction(year)


def get_year_campaign_start_date(year):
    year = int(year)
    if year in CAMPAIGN_DATES:
        return CAMPAIGN_DATES[year]["teledeclaration_start_date"]
    else:
        return None


def get_year_campaign_end_date_or_today_date(year):
    """
    Return the year's campaign end date
    """
    year = int(year)
    now = timezone.now()
    if year in CAMPAIGN_DATES.keys():
        return CAMPAIGN_DATES[year]["teledeclaration_end_date"]
    elif year >= now.year:
        return now
    else:
        return None


def get_year_correction_end_date_or_campaign_end_date_or_today_date(year):
    """
    Return the year's correction end date
    Fallback to the year's campaign end date if it doens't exist
    """
    year = int(year)
    now = timezone.now()
    if year in CAMPAIGN_DATES.keys():
        if CAMPAIGN_DATES[year]["correction_end_date"]:
            return CAMPAIGN_DATES[year]["correction_end_date"]
        else:
            return get_year_campaign_end_date_or_today_date(year)
    elif year >= now.year:
        return now
    else:
        return None
