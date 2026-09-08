import logging
from decimal import Decimal

import redis as r
from django.conf import settings

from data.models.geo import REGION_HEXAGONE_LIST, Region

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


# increment this when the teledeclaration format changes
# and update docs/teledeclaration_versions.md
TELEDECLARATION_CURRENT_VERSION = 16
YEARS_WITH_1TD1SITE = [2024, 2025]


# https://ma-cantine.agriculture.gouv.fr/blog/16/
# TODO: improve (depends on the year)
HEXAGONE_LIST = REGION_HEXAGONE_LIST + [
    Region.saint_barthelemy,
    Region.terres_australes_et_antarctiques_francaises,
    Region.wallis_et_futuna,
    Region.polynesie_francaise,
    Region.nouvelle_caledonie,
    Region.ile_de_clipperton,
]
GROUP_1_LIST = [Region.guadeloupe, Region.martinique, Region.guyane, Region.la_reunion, Region.saint_martin]
GROUP_2_LIST = [Region.mayotte]
GROUP_3_LIST = [Region.saint_pierre_et_miquelon]
EGALIM_OBJECTIVES = {
    "hexagone": {
        "region_list": HEXAGONE_LIST,
        "bio_percent": 20,
        "egalim_percent": 50,
    },
    "groupe_1": {
        "region_list": GROUP_1_LIST,
        "bio_percent": 5,
        "egalim_percent": 20,
    },
    "groupe_3": {"region_list": GROUP_3_LIST, "bio_percent": 10, "egalim_percent": 30},
    "groupe_2": {"region_list": GROUP_2_LIST, "bio_percent": 2, "egalim_percent": 5},
}


# TODO: prendre en compte les department, epci, pat & city_insee_code
def get_egalim_group(region_list):
    if region_list and len(region_list):
        # first check if one of the regions is in "hexagone"
        if any(region in HEXAGONE_LIST for region in region_list):
            return "hexagone"
        # then check if one of the regions is in any of the other groups
        for group_name, details in EGALIM_OBJECTIVES.items():
            if any(region in details["region_list"] for region in region_list):
                return group_name
    return "hexagone"  # default


def objectifs_egalim_atteints(pourcentage_bio, pourcentage_egalim, canteen_region):
    """
    Determine if the EGALIM objectives are met.

    Args:
        pourcentage_bio (float): The percentage of organic products.
        pourcentage_egalim (float): The percentage of EGALIM-compliant products.
        canteen_region (str): The region of the canteen.

    Returns:
        bool: True if the objectives are met, False otherwise.
    """
    # default thresholds
    bio_threshold = EGALIM_OBJECTIVES["hexagone"]["bio_percent"]
    egalim_threshold = EGALIM_OBJECTIVES["hexagone"]["egalim_percent"]

    # override thresholds for specific regions
    if canteen_region:
        if canteen_region in EGALIM_OBJECTIVES["groupe_1"]["region_list"]:
            bio_threshold = EGALIM_OBJECTIVES["groupe_1"]["bio_percent"]
            egalim_threshold = EGALIM_OBJECTIVES["groupe_1"]["egalim_percent"]
        elif canteen_region in EGALIM_OBJECTIVES["groupe_2"]["region_list"]:
            bio_threshold = EGALIM_OBJECTIVES["groupe_2"]["bio_percent"]
            egalim_threshold = EGALIM_OBJECTIVES["groupe_2"]["egalim_percent"]
        elif canteen_region in EGALIM_OBJECTIVES["groupe_3"]["region_list"]:
            bio_threshold = EGALIM_OBJECTIVES["groupe_3"]["bio_percent"]
            egalim_threshold = EGALIM_OBJECTIVES["groupe_3"]["egalim_percent"]

    return pourcentage_bio >= bio_threshold and pourcentage_egalim >= egalim_threshold


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
    - the EGALIM_STATS_FIELDS (pourcentage_* & objectifs_egalim_atteints) stay the same
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
        try:
            value = getattr(diagnostic, field) / Decimal(divisor)
            appro_fields_satellite[field] = round(value, 2)
        except (TypeError, ZeroDivisionError):
            appro_fields_satellite[field] = None

    return appro_fields_satellite
