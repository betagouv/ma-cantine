from common.utils import utils as utils_utils
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_required


def validate_gaspillage_fields_required(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] the volet has required fields
        - [NEW in 2026] the volet is skipped if not started (none of its fields filled)
        - [NEW in 2026] dons_convention is optional if the canteen serves less than 3000 meals per day
          (loi EGalim: the obligation only applies above 3000 meals per day)
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        # Skip validation if volet is not filled
        if not instance.is_filled_gaspillage:
            return errors
        canteen_has_dons_convention_obligation = bool(
            instance.canteen and instance.canteen.daily_meal_count and instance.canteen.daily_meal_count >= 3000
        )
        for field in get_teledeclaration_fields_required(instance.year, "GASPILLAGE"):
            if field == "dons_convention" and not canteen_has_dons_convention_obligation:
                continue
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                )
    return errors


def validate_gaspillage_dons_fields(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] dons_frequence, dons_quantite & dons_type_denrees can only be filled if dons_convention is True
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        if instance.dons_convention is not True:
            for field in ["dons_frequence", "dons_quantite", "dons_type_denrees"]:
                if getattr(instance, field) not in [None, ""]:
                    utils_utils.add_validation_error(
                        errors, field, "Ce champ ne peut être renseigné que si une convention de dons est en place."
                    )
    return errors
