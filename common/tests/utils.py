import zoneinfo
from datetime import date, datetime, time, timedelta

from data.models.diagnostic_teledeclaration_dates import CAMPAIGN_DATES

# Dates to freeze time in tests, derived from CAMPAIGN_DATES (instead of hardcoded strings)
# - year: the year of the diagnostics (e.g. the 2024 campaign takes place in 2025)
# - always at noon (Paris time), to avoid any timezone edge case


def _at_noon(day):
    return datetime.combine(day, time(12), tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))


def date_before_campaign(year):
    """
    Same calendar year as the campaign, but before its start
    """
    frozen_date = _at_noon(date(year + 1, 1, 1))
    assert frozen_date < CAMPAIGN_DATES[year]["teledeclaration_start_date"], f"No date before the {year} campaign"
    return frozen_date


def date_in_campaign(year):
    return _at_noon(CAMPAIGN_DATES[year]["teledeclaration_start_date"] + timedelta(days=1))


def date_between_campaign_and_campaign_correction(year):
    frozen_date = _at_noon(CAMPAIGN_DATES[year]["teledeclaration_end_date"] + timedelta(days=1))
    assert CAMPAIGN_DATES[year]["correction_start_date"], f"No correction for the {year} campaign"
    assert frozen_date < CAMPAIGN_DATES[year]["correction_start_date"], f"No gap before the {year} correction"
    return frozen_date


def date_in_campaign_correction(year):
    """
    During the correction, but outside of the teledeclaration (they can overlap, e.g. in 2023)
    """
    assert CAMPAIGN_DATES[year]["correction_start_date"], f"No correction for the {year} campaign"
    frozen_date = _at_noon(
        max(CAMPAIGN_DATES[year]["correction_start_date"], CAMPAIGN_DATES[year]["teledeclaration_end_date"])
        + timedelta(days=1)
    )
    assert frozen_date < CAMPAIGN_DATES[year]["correction_end_date"]
    return frozen_date


def date_after_campaign(year):
    """
    After the campaign (and its correction, if any)
    """
    end_date = CAMPAIGN_DATES[year]["correction_end_date"] or CAMPAIGN_DATES[year]["teledeclaration_end_date"]
    return _at_noon(end_date + timedelta(days=1))
