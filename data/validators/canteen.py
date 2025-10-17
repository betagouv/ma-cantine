from common.utils import utils as utils_utils


def validate_canteen_choice_fields(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is in the choices
    - extra validation:
        - some choice fields cannot be blank
    """
    errors = {}
    for field_name in ["management_type", "production_type", "economic_model"]:
        value = getattr(instance, field_name)
        if not value:
            utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    return errors
