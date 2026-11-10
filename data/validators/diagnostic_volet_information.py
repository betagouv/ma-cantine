from common.utils import utils as utils_utils
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_required
from data.models.sector import SECTOR_INFORMATION_CONSULTATION_QUALITE_LIST


def validate_information_fields_required(instance):
    """
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] the volet has required fields
        - [NEW in 2026] the volet is skipped if not started (none of its fields filled)
        - [NEW in 2026] information_part_pat is optional if the canteen doesn't belong to a PAT (empty pat_list)
        - [NEW in 2026] information_consultation_qualite is optional if none of the canteen's sectors is concerned
          (see SECTOR_INFORMATION_CONSULTATION_QUALITE_LIST)
    NOTE: not called in clean(): to avoid blocking teledeclaration, but in is_clean()
    """
    errors = {}
    if instance.year and int(instance.year) >= 2026:
        # Skip validation if volet is not filled
        if not instance.is_filled_information:
            return errors
        canteen_has_pat = bool(instance.canteen and instance.canteen.pat_list)
        canteen_has_sector_consultation_qualite = bool(
            instance.canteen
            and set(instance.canteen.sector_list or []).intersection(SECTOR_INFORMATION_CONSULTATION_QUALITE_LIST)
        )
        for field in get_teledeclaration_fields_required(instance.year, "INFORMATION"):
            if field == "information_part_pat" and not canteen_has_pat:
                continue
            if field == "information_consultation_qualite" and not canteen_has_sector_consultation_qualite:
                continue
            if getattr(instance, field) is None:
                utils_utils.add_validation_error(
                    errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                )
    return errors
