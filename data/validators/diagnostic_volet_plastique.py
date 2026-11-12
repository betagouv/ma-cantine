from common.utils import utils as utils_utils
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_required


def validate_plastique_fields_required(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] the volet has required fields
        - the volet is skipped if not started (none of its fields filled)
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year:
        # Skip validation if volet is not filled
        if not instance.is_filled_plastique:
            return errors
        for field in get_teledeclaration_fields_required(instance.year, "PLASTIQUE"):
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                )
    return errors


def validate_plastique_contenant_emporter_fields(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] plastique_contenant_emporter_remplace is required if vente_emporter is True
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        field = "plastique_contenant_emporter_remplace"
        if instance.vente_emporter is True:
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors,
                    field,
                    "Ce champ est obligatoire si l'établissement propose des repas à emporter.",
                )
    return errors
