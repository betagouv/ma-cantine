import logging
import zoneinfo
from datetime import datetime

import redis as r
from django.conf import settings

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)

CAMPAIGN_DATES = {
    2021: {
        "teledeclaration_start_date": datetime(2022, 7, 16, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(2022, 12, 5, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2022: {
        "teledeclaration_start_date": datetime(2023, 2, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(2023, 7, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2023: {
        "teledeclaration_start_date": datetime(2024, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "teledeclaration_end_date": datetime(2024, 6, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_start_date": datetime(2024, 6, 3, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": datetime(2024, 6, 13, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2024: {
        "teledeclaration_start_date": settings.TELEDECLARATION_START_DATE or "2025-01-07 00:00:00+01:00",
        "teledeclaration_end_date": settings.TELEDECLARATION_END_DATE
        or datetime(2025, 4, 7, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_start_date": settings.CORRECTION_START_DATE
        or datetime(2025, 4, 16, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "correction_end_date": settings.CORRECTION_END_DATE
        or datetime(2025, 5, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    # Note: au moment d'ajouter une nouvelle année :
    # - penser à y ajouter les settings (pour override)
    # - et enlever les settings de l'année précédente
}
