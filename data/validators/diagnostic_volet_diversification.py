from common.utils import utils as utils_utils
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_required


def validate_diversification_fields_required(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] the volet has required fields
        - [NEW in 2026] the volet is skipped if not started (none of its fields filled)
        - [NEW in 2026] plan_diversification_en_place is optional if the canteen serves 200 meals or less per day
          (loi EGalim: the plan is only mandatory above 200 meals per day)
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        # Skip validation if volet is not filled
        if not instance.is_filled_diversification:
            return errors
        canteen_has_plan_diversification_obligation = bool(
            instance.canteen and instance.canteen.daily_meal_count and instance.canteen.daily_meal_count > 200
        )
        for field in get_teledeclaration_fields_required(instance.year, "DIVERSIFICATION"):
            if field == "plan_diversification_en_place" and not canteen_has_plan_diversification_obligation:
                continue
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                )
    return errors


def validate_diversification_plan_fields(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] plan_diversification_actions can only be filled if plan_diversification_en_place is True
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        if instance.plan_diversification_en_place is not True:
            if instance.plan_diversification_actions:
                utils_utils.add_validation_error(
                    errors,
                    "plan_diversification_actions",
                    "Ce champ ne peut être renseigné que si un plan de diversification est en place.",
                )
    return errors


def validate_diversification_menu_vegetarien_fields(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] menu_vegetarien_bases can only be filled if a menu végétarien is proposed
          (menu_vegetarien_frequence filled & not JAMAIS)
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        if instance.menu_vegetarien_frequence in [None, "", instance.MenuVegetarienFrequence.JAMAIS]:
            if instance.menu_vegetarien_bases:
                utils_utils.add_validation_error(
                    errors,
                    "menu_vegetarien_bases",
                    "Ce champ ne peut être renseigné que si un menu végétarien est proposé.",
                )
    return errors
