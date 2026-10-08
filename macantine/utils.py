import logging

from data.utils import to_decimal

logger = logging.getLogger(__name__)


# increment this when the teledeclaration format changes
# and update docs/teledeclaration_versions.md
TELEDECLARATION_CURRENT_VERSION = 16
YEARS_WITH_1TD1SITE = [2024, 2025]


def set_satellite_common_fields_from_groupe_diagnostic(diagnostic, satellite_dict) -> dict:
    """
    Generate a dict with common fields values for a satellite from a groupe diagnostic

    Rules:
    - before 2025, we override the satellite with the groupe's values: geo data, sector_list, line_ministry. We also change the yearly_meal_count (divided by the number of satellites)
    - in 2025, we stop overriding fields
    """
    from data.models import Canteen  # avoid circular import

    updated_common_fields = {}

    # some hard-coded rules
    updated_common_fields["production_type"] = Canteen.ProductionType.ON_SITE_CENTRAL
    updated_common_fields["satellite_canteens_count"] = 0

    # rules depending on the campaign year
    if diagnostic.year <= 2024:
        fields_overridden_by_groupe = [
            "city_insee_code",
            "epci",
            "pat_list",
            "department",
            "region",
            "sector_list",
            "line_ministry",
        ]
    elif diagnostic.year == 2025:
        fields_overridden_by_groupe = []

    # build dict
    for field in fields_overridden_by_groupe:
        if field in diagnostic.canteen_snapshot:
            updated_common_fields[field] = diagnostic.canteen_snapshot[field]

    # yearly_meal_count (before 2025)
    if diagnostic.year <= 2024:
        divisor = len(diagnostic.satellites_snapshot) if diagnostic.satellites_snapshot else 0
        try:
            updated_common_fields["yearly_meal_count"] = int(
                diagnostic.canteen_snapshot["yearly_meal_count"] / divisor
            )
        except (TypeError, ZeroDivisionError):
            updated_common_fields["yearly_meal_count"] = None

    return updated_common_fields


def set_satellite_diagnostic_appro_values_from_groupe_diagnostic(diagnostic, satellite_dict) -> dict:
    """
    Generate a dict with appro values distributed to satellites from a groupe diagnostic

    Note:
    - we divide only the APPRO values
    - the APPRO_STATS_FIELDS (pourcentage_* & objectifs_egalim_atteints) stay the same
    - the other fields (WASTE_FIELDS, DIVERSIFICATION_FIELDS, PLASTIC_FIELDS, INFO_FIELDS) stay the same

    Rules:
    - before 2025, we divide by the number of satellites
    - in 2025, we divide by the satellite's yearly_meal_count (ratio)
        - Note: requires with_satellites_snapshot_stats() queryset
    """
    from data.models import Diagnostic  # avoid circular import

    appro_fields_satellite = {}

    # get the divisor
    if diagnostic.year <= 2024:
        divisor = len(diagnostic.satellites_snapshot) if diagnostic.satellites_snapshot else 0
        # no +1 for central_serving? we already added it in canteen_migrate_central_to_groupe.py
    elif diagnostic.year == 2025:
        divisor = (
            diagnostic.satellites_snapshot_yearly_meal_count_sum / satellite_dict.get("yearly_meal_count")
            if satellite_dict.get("yearly_meal_count")
            else 0
        )

    # build dict
    for field in Diagnostic.APPRO_1TD1SITE_FIELDS:
        value = getattr(diagnostic, field)
        try:
            appro_fields_satellite[field] = (
                None if value is None else round(to_decimal(value) / to_decimal(divisor), 2)
            )
        except ZeroDivisionError:
            appro_fields_satellite[field] = None

    return appro_fields_satellite
