import logging
import zoneinfo
from datetime import datetime

logger = logging.getLogger(__name__)


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
