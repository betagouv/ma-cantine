from common.utils import utils as utils_utils
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_required
from data.models.sector import SECTOR_PLASTIQUE_BOUTEILLE_LIST, SECTOR_PLASTIQUE_CONTENANT_LIST


def validate_plastique_fields_required(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] the volet has required fields
        - [NEW in 2026] the volet is skipped if not started (none of its fields filled)
        - [NEW in 2026] plastique_bouteille_remplace is optional if none of the canteen's sectors is concerned
          (see SECTOR_PLASTIQUE_BOUTEILLE_LIST)
        - [NEW in 2026] plastique_contenant_remplace is optional if none of the canteen's sectors is concerned
          (see SECTOR_PLASTIQUE_CONTENANT_LIST)
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        # Skip validation if volet is not filled
        if not instance.is_filled_plastique:
            return errors
        canteen_sector_list = set(instance.canteen.sector_list or []) if instance.canteen else set()
        canteen_has_sector_plastique_bouteille = bool(
            canteen_sector_list.intersection(SECTOR_PLASTIQUE_BOUTEILLE_LIST)
        )
        canteen_has_sector_plastique_contenant = bool(
            canteen_sector_list.intersection(SECTOR_PLASTIQUE_CONTENANT_LIST)
        )
        for field in get_teledeclaration_fields_required(instance.year, "PLASTIQUE"):
            if field == "plastique_bouteille_remplace" and not canteen_has_sector_plastique_bouteille:
                continue
            if field == "plastique_contenant_remplace" and not canteen_has_sector_plastique_contenant:
                continue
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                )
    return errors


def validate_plastique_contenant_emporter_fields(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] plastique_contenant_emporter_remplace is required if vente_emporter is True
        - [NEW in 2026] plastique_contenant_emporter_remplace can only be filled if vente_emporter is True
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
        else:
            if getattr(instance, field) is not None:
                utils_utils.add_validation_error(
                    errors,
                    field,
                    "Ce champ ne peut être renseigné que si l'établissement propose des repas à emporter.",
                )
    return errors
