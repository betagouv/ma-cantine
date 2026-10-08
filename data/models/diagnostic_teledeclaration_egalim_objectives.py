from data.models.geo import REGION_HEXAGONE_LIST, Region

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
