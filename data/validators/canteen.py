from common.utils import utils as utils_utils


def validate_canteen_choice_fields(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is in the choices
    - extra validation:
        - some choice fields must be filled
    """
    errors = {}
    for field_name in ["management_type", "production_type", "economic_model"]:
        value = getattr(instance, field_name)
        if value in [None, ""]:
            utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    return errors


def validate_canteen_meal_count_fields(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is an integer >= 0
    - extra validation:
        - daily_meal_count & yearly_meal_count must be filled
        - daily_meal_count & yearly_meal_count must be integers
        - daily_meal_count & yearly_meal_count must be > 0
    - notes:
        - django will convert strings to integers
        - django will convert floats to integers by truncating the decimal part (e.g. 10.5 -> 10)
    """
    errors = {}
    for field_name in ["daily_meal_count", "yearly_meal_count"]:
        value = getattr(instance, field_name)
        if value in [None, ""]:
            utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
        elif not (isinstance(value, int) or (isinstance(value, str) and value.isdigit())):
            utils_utils.add_validation_error(errors, field_name, "Le champ doit être un nombre entier.")
        elif int(value) <= 0:
            utils_utils.add_validation_error(errors, field_name, "Le champ doit être un nombre entier supérieur à 0.")
    return errors
