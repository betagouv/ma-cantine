from data.models.geo import REGION_HEXAGONE_LIST, Region

# https://ma-cantine.agriculture.gouv.fr/blog/16/
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
EGALIM_REGION_GROUPS = {
    "hexagone": HEXAGONE_LIST,
    "groupe_1": GROUP_1_LIST,
    "groupe_2": GROUP_2_LIST,
    "groupe_3": GROUP_3_LIST,
}

EGALIM_OBJECTIVES = {
    2021: {
        "APPRO": {
            "hexagone": {"bio_percent": 20, "egalim_percent": 50},
            "groupe_1": {"bio_percent": 5, "egalim_percent": 20},
            "groupe_2": {"bio_percent": 2, "egalim_percent": 5},
            "groupe_3": {"bio_percent": 10, "egalim_percent": 30},
        },
    },
    2022: {
        "APPRO": {
            "hexagone": {"bio_percent": 20, "egalim_percent": 50},
            "groupe_1": {"bio_percent": 5, "egalim_percent": 20},
            "groupe_2": {"bio_percent": 2, "egalim_percent": 5},
            "groupe_3": {"bio_percent": 10, "egalim_percent": 30},
        },
    },
    2023: {
        "APPRO": {
            "hexagone": {"bio_percent": 20, "egalim_percent": 50},
            "groupe_1": {"bio_percent": 5, "egalim_percent": 20},
            "groupe_2": {"bio_percent": 2, "egalim_percent": 5},
            "groupe_3": {"bio_percent": 10, "egalim_percent": 30},
        },
    },
    2024: {
        "APPRO": {
            "hexagone": {"bio_percent": 20, "egalim_percent": 50},
            "groupe_1": {"bio_percent": 5, "egalim_percent": 20},
            "groupe_2": {"bio_percent": 2, "egalim_percent": 5},
            "groupe_3": {"bio_percent": 10, "egalim_percent": 30},
        },
    },
    2025: {
        "APPRO": {
            "hexagone": {"bio_percent": 20, "egalim_percent": 50},
            "groupe_1": {"bio_percent": 5, "egalim_percent": 20},
            "groupe_2": {"bio_percent": 2, "egalim_percent": 5},
            "groupe_3": {"bio_percent": 10, "egalim_percent": 30},
        },
    },
    2026: {
        "APPRO": {
            "hexagone": {"bio_percent": 20, "egalim_percent": 50},
            "groupe_1": {"bio_percent": 5, "egalim_percent": 20},
            "groupe_2": {"bio_percent": 2, "egalim_percent": 5},
            "groupe_3": {"bio_percent": 10, "egalim_percent": 30},
        },
    },
}


def get_egalim_objectives(year, label):
    """
    Years before the first defined year use the first year's objectives,
    years after the last defined year use the last year's objectives.
    """
    year = min(max(int(year), min(EGALIM_OBJECTIVES)), max(EGALIM_OBJECTIVES))
    if label not in EGALIM_OBJECTIVES[year]:
        raise ValueError(f"Field 'label' expected one of {list(EGALIM_OBJECTIVES[year].keys())} but got '{label}'.")
    return EGALIM_OBJECTIVES[year][label]


# TODO: prendre en compte les department, epci, pat & city_insee_code
def get_egalim_group(region_list):
    if region_list and len(region_list):
        # first check if one of the regions is in "hexagone"
        if any(region in HEXAGONE_LIST for region in region_list):
            return "hexagone"
        # then check if one of the regions is in any of the other groups
        for group_name, group_region_list in EGALIM_REGION_GROUPS.items():
            if any(region in group_region_list for region in region_list):
                return group_name
    return "hexagone"  # default


def get_egalim_objectives_appro(year, canteen_region):
    """
    Return the year's appro thresholds (bio_percent & egalim_percent) for the canteen's region
    """
    return get_egalim_objectives(year, "APPRO")[get_egalim_group([canteen_region])]


def get_egalim_objectives_notes(year, egalim_group):
    """
    Return the year's appro thresholds for the egalim group
    """
    egalim_objectives_appro = get_egalim_objectives(year, "APPRO")[egalim_group]
    return {
        "egalim_group": egalim_group,
        "bio_percent_objective": egalim_objectives_appro["bio_percent"],
        "egalim_percent_objective": egalim_objectives_appro["egalim_percent"],
    }


def objectifs_egalim_atteints(year, canteen_region, pourcentage_bio, pourcentage_egalim):
    """
    Determine if the EGALIM objectives are met.

    Args:
        year (int): The diagnostic year.
        canteen_region (str): The region of the canteen.
        pourcentage_bio (float | None): The percentage of organic products.
        pourcentage_egalim (float | None): The percentage of EGALIM-compliant products.

    Returns:
        bool | None: True if the objectives are met, False otherwise.
            None if a percentage is missing (e.g. no valeur_totale).
    """
    if pourcentage_bio is None or pourcentage_egalim is None:
        return None
    objectives = get_egalim_objectives_appro(year, canteen_region)
    return pourcentage_bio >= objectives["bio_percent"] and pourcentage_egalim >= objectives["egalim_percent"]
