"""
Badges of the volets thématiques.
The rules are versioned by their first year (2021, 2022, 2026...): the Diagnostic badge properties pick the
function to use depending on the year of the diagnostic
Each badge returns:
- True: the objectives are reached
- False: the objectives are not reached (and the volet has been visited in the tunnel)
- None: not enough information
"""

from dataclasses import dataclass
from data.models.canteen import get_is_administration
from data.models.diagnostic_volet_diversification import DiagnosticVoletDiversificationMixin
from data.models.sector import (
    EDUCATION_SECTOR_LIST,
    HEALTH_SECTOR_LIST,
    SOCIAL_SECTOR_LIST,
    Sector,
)

MenuVegetarienFrequence = DiagnosticVoletDiversificationMixin.MenuVegetarienFrequence
ServiceType = DiagnosticVoletDiversificationMixin.ServiceType


def is_volet_completed(diagnostic, volet) -> bool:
    """
    The 2026 badges are only computed if the diagnostic is teledeclared, and the volet is filled without errors
    """
    volet_name = volet.lower()
    return (
        diagnostic.is_teledeclared
        and getattr(diagnostic, f"is_filled_{volet_name}")
        and getattr(diagnostic, f"is_clean_{volet_name}")
    )


@dataclass
class CanteenSnapshot:
    """
    The canteen data at the time of the teledeclaration
    """

    daily_meal_count: int | None
    sector_list: list[str]
    economic_model: str | None
    line_ministry: str | None

    @property
    def is_administration(self) -> bool:
        return get_is_administration(self.sector_list, self.economic_model, self.line_ministry)


def get_canteen_snapshot(diagnostic) -> CanteenSnapshot:
    canteen_snapshot = diagnostic.canteen_snapshot or {}
    return CanteenSnapshot(
        daily_meal_count=canteen_snapshot.get("daily_meal_count"),
        sector_list=canteen_snapshot.get("sector_list") or [],
        economic_model=canteen_snapshot.get("economic_model"),
        line_ministry=canteen_snapshot.get("line_ministry"),
    )


# Gaspillage
def waste_badge_2021(diagnostic) -> None:
    """
    Not available yet: the 2021 canteen_snapshot doesn't have the canteen data needed (daily_meal_count, sectors)
    (see docs/teledeclaration_versions.md)
    """
    return None


def waste_badge_2022(diagnostic) -> bool | None:
    """
    Computed with the canteen data at the time of the teledeclaration (canteen_snapshot)
    """
    if not diagnostic.is_teledeclared:
        return None
    canteen = get_canteen_snapshot(diagnostic)
    if (
        diagnostic.diagnostic_gaspillage_realise
        and diagnostic.actions_gaspillage_realisees
        and len(diagnostic.actions_gaspillage_realisees) > 0
    ):
        if diagnostic.dons_convention or (canteen.daily_meal_count and canteen.daily_meal_count < 3000):
            return True
    if diagnostic.tunnel_waste:
        return False


def waste_badge_2026(diagnostic) -> bool | None:
    if not is_volet_completed(diagnostic, "GASPILLAGE"):
        return None
    canteen = get_canteen_snapshot(diagnostic)
    has_diagnostic_and_actions = bool(
        diagnostic.diagnostic_gaspillage_realise
        and diagnostic.actions_gaspillage_realisees
        and len(diagnostic.actions_gaspillage_realisees) > 0
    )
    has_dons_or_less_than_3000_meals = bool(
        diagnostic.dons_convention or (canteen.daily_meal_count and canteen.daily_meal_count < 3000)
    )
    return has_diagnostic_and_actions and has_dons_or_less_than_3000_meals


# Diversification
def diversification_badge_2021(diagnostic) -> None:
    """
    Not available yet: the 2021 canteen_snapshot doesn't have the canteen data needed (daily_meal_count, sectors)
    (see docs/teledeclaration_versions.md)
    """
    return None


def diversification_badge_2022(diagnostic) -> bool | None:
    """
    Computed with the canteen data at the time of the teledeclaration (canteen_snapshot)
    """
    if not diagnostic.is_teledeclared:
        return None
    canteen = get_canteen_snapshot(diagnostic)
    has_daily_frequency = diagnostic.menu_vegetarien_frequence == MenuVegetarienFrequence.QUOTIDIEN
    has_weekly_or_more_frequency = diagnostic.menu_vegetarien_frequence in [
        MenuVegetarienFrequence.QUOTIDIEN,
        MenuVegetarienFrequence.HEBDO,
        MenuVegetarienFrequence.PLUS_HEBDO,
    ]
    # Only the canteens with more than 200 daily meals with a diversification plan
    if canteen.daily_meal_count and canteen.daily_meal_count >= 200 and diagnostic.plan_diversification_en_place:
        return True
    # Only the canteens in the administration sector must have a daily frequency
    if canteen.is_administration and has_daily_frequency:
        return True
    if not canteen.is_administration and has_weekly_or_more_frequency:
        return True
    if diagnostic.tunnel_diversification:
        return False


def diversification_badge_2026(diagnostic) -> bool | None:
    """
    True if all the obligations that apply to the canteen are met
    If no obligation applies: True if a diversification plan with actions, or a vegetarian menu
    """
    if not is_volet_completed(diagnostic, "DIVERSIFICATION"):
        return None
    canteen = get_canteen_snapshot(diagnostic)
    frequence = diagnostic.menu_vegetarien_frequence
    obligations = []
    # Diversification plan: canteens with 200 daily meals or more
    if canteen.daily_meal_count and canteen.daily_meal_count >= 200:
        obligations.append(diagnostic.plan_diversification_en_place is True)
    # Weekly vegetarian menu: school canteens (from primaire to lycée, including enseignement agricole)
    school_sectors = [
        Sector.EDUCATION_PRIMAIRE,
        Sector.EDUCATION_SECONDAIRE_COLLEGE,
        Sector.EDUCATION_SECONDAIRE_LYCEE,
        Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE,
    ]
    if set(canteen.sector_list).intersection(school_sectors):
        obligations.append(
            frequence
            in [MenuVegetarienFrequence.HEBDO, MenuVegetarienFrequence.PLUS_HEBDO, MenuVegetarienFrequence.QUOTIDIEN]
        )
    # Daily vegetarian option: administration canteens with a multiple choice service
    multiple_choice_services = [ServiceType.CHOIX_MULTIPLE_LIBRE_SERVICE, ServiceType.CHOIX_MULTIPLE_RESERVATION]
    if canteen.is_administration and diagnostic.service_type in multiple_choice_services:
        obligations.append(frequence == MenuVegetarienFrequence.QUOTIDIEN)

    if obligations:
        is_reached = all(obligations)
    else:
        # No obligation: a diversification plan with actions, or a vegetarian menu
        has_plan_with_actions = bool(
            diagnostic.plan_diversification_en_place and diagnostic.plan_diversification_actions
        )
        has_vegetarian_menu = frequence is not None and frequence != MenuVegetarienFrequence.JAMAIS
        is_reached = has_plan_with_actions or has_vegetarian_menu

    return is_reached


# Plastique
def plastic_badge_2021(diagnostic) -> None:
    """
    Not available yet for 2021
    """
    return None


def plastic_badge_2022(diagnostic) -> bool | None:
    if (
        diagnostic.plastique_contenant_cuisson_remplace
        and diagnostic.plastique_contenant_service_remplace
        and diagnostic.plastique_bouteille_remplace
        and diagnostic.plastique_ustensile_remplace
    ):
        return True
    if diagnostic.tunnel_plastic:
        return False


def plastic_badge_2026(diagnostic) -> bool | None:
    """
    For all the canteens: plastic drink bottles replaced
    Education: plastic water bottles replaced
    20 daily meals or more: disposable tableware replaced
    Education, crèches and health: cooking, reheating and serving containers replaced
    """
    if not is_volet_completed(diagnostic, "PLASTIQUE"):
        return None
    canteen = get_canteen_snapshot(diagnostic)
    sectors = set(canteen.sector_list)
    obligations = [diagnostic.plastique_bouteille_boisson_remplace]
    if sectors.intersection(EDUCATION_SECTOR_LIST):
        obligations.append(diagnostic.plastique_bouteille_remplace)
    if canteen.daily_meal_count and canteen.daily_meal_count >= 20:
        obligations.append(diagnostic.plastique_vaisselle_jetable_remplace)
    if sectors.intersection(EDUCATION_SECTOR_LIST + [Sector.SOCIAL_CRECHE] + HEALTH_SECTOR_LIST):
        obligations.append(diagnostic.plastique_contenant_remplace)

    return all(obligation is True for obligation in obligations)


# Information
def info_badge_2021(diagnostic) -> None:
    """
    Not available yet for 2021
    """
    return None


def info_badge_2022(diagnostic) -> bool | None:
    if diagnostic.information_qualite_durable:
        return True
    if diagnostic.tunnel_info:
        return False


def info_badge_2026(diagnostic) -> bool | None:
    """
    For all the canteens: part EGalim, permanent display and annual electronic communication
    For some sectors (education, health, social, prisons): regular consultation on the food quality
    """
    if not is_volet_completed(diagnostic, "INFORMATION"):
        return None
    canteen = get_canteen_snapshot(diagnostic)
    is_reached = bool(
        diagnostic.information_part_egalim
        and diagnostic.information_affichage_permanent
        and diagnostic.information_electronique_annuelle
    )
    sectors_quality_required = (
        EDUCATION_SECTOR_LIST + HEALTH_SECTOR_LIST + SOCIAL_SECTOR_LIST + [Sector.ADMINISTRATION_PRISON]
    )
    if set(canteen.sector_list).intersection(sectors_quality_required):
        is_reached = is_reached and bool(diagnostic.information_consultation_qualite)

    return is_reached
