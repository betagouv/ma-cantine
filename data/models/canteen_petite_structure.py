"""
Expérimentation « Petites structures »

Une cantine est éligible (is_petite_structure) si elle respecte simultanément :
- critère 1 : un seul secteur, éligible & nombre de couverts/jour <= seuil
- critère 2 : gestion directe
- critère 3 : restaurant avec cuisine sur place

Note : être éligible ne signifie pas participer à l'expérimentation.
"""

from data.models.sector import Sector

# seuil (inclus) de couverts/jour par secteur éligible
PETITE_STRUCTURE_SECTOR_DAILY_MEAL_COUNT_THRESHOLD = {
    # education
    Sector.EDUCATION_PRIMAIRE: 30,
    Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE: 30,
    # sante
    Sector.SANTE_HOPITAL: 70,
    Sector.SANTE_CLINIQUE: 70,
    Sector.SANTE_AUTRE: 70,
    # social
    Sector.SOCIAL_CRECHE: 30,
    Sector.SOCIAL_IME: 70,
    Sector.SOCIAL_ESAT: 70,
    Sector.SOCIAL_EHPAD: 70,
    Sector.SOCIAL_PJJ: 70,
    Sector.SOCIAL_AUTRE: 70,
    # loisir
    Sector.LOISIR_CENTRE_VACANCES: 70,
    Sector.LOISIR_AUTRE: 70,
}


def get_petite_structure_daily_meal_count_threshold(sector_list: list[str]) -> int | None:
    """
    La cantine doit avoir un seul secteur, et ce secteur doit être éligible (sinon None)
    """
    if not sector_list or len(sector_list) != 1:
        return None
    return PETITE_STRUCTURE_SECTOR_DAILY_MEAL_COUNT_THRESHOLD.get(sector_list[0])


def compute_is_petite_structure(canteen) -> bool:
    # critère 2 : gestion directe
    if canteen.management_type != canteen.ManagementType.DIRECT:
        return False
    # critère 3 : restaurant avec cuisine sur place
    if canteen.production_type != canteen.ProductionType.ON_SITE:
        return False
    # critère 1 : un seul secteur, éligible & nombre de couverts/jour <= seuil
    if not canteen.daily_meal_count:
        return False
    threshold = get_petite_structure_daily_meal_count_threshold(canteen.sector_list)
    return bool(threshold) and canteen.daily_meal_count <= threshold
