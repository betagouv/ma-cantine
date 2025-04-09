import logging
import zoneinfo
from datetime import datetime

import redis as r
from django.conf import settings
from django.utils import timezone

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


CAMPAIGN_DATES = {
    2021: {
        "teledeclaration_start_date": datetime(2022, 7, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2022, 12, 4, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
    },
    2022: {
        "teledeclaration_start_date": datetime(2023, 2, 12, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2023, 6, 30, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
    },
    2023: {
        "teledeclaration_start_date": datetime(2024, 1, 8, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(
            2024, 6, 11, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")
        ),
        "correction_start_date": datetime(2024, 6, 3, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": datetime(2024, 6, 12, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2024: {
        "teledeclaration_start_date": (
            convert_date_string_to_datetime(settings.TELEDECLARATION_START_DATE)
            or datetime(2025, 1, 7, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "teledeclaration_end_date": (
            convert_date_string_to_datetime(settings.TELEDECLARATION_END_DATE, "end")
            or datetime(2025, 4, 6, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "correction_start_date": (
            convert_date_string_to_datetime(settings.CORRECTION_START_DATE)
            or datetime(2025, 4, 16, 0, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
        "correction_end_date": (
            convert_date_string_to_datetime(settings.CORRECTION_END_DATE, "end")
            or datetime(2025, 4, 30, 23, 59, 59, 999999, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
        ),
    },
    # Note: au moment d'ajouter une nouvelle année :
    # - penser à y ajouter les settings (pour override)
    # - et enlever les settings de l'année précédente
}


def is_in_teledeclaration():
    """
    Check if the current date is within the teledeclaration period for the given year.
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
    Check if the current date is within the correction period for the given year.
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
    Check if the current date is within the teledeclaration or correction period for the given year.
    """
    return is_in_teledeclaration() or is_in_correction()
