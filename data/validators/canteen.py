from common.utils import utils as utils_utils


def validate_canteen_siret_or_siren_unite_legale(instance):
    """
    - clean_fields() (called by full_clean()) already checks that
    the siret and siren_unite_legale fields are the correct length and format
    - extra validation:
        - siret or siren_unite_legale must be filled
        - both cannot be filled at the same time
        - central: only the siret field should be filled
    """
    errors = {}
    siret = instance.siret
    siren_unite_legale = instance.siren_unite_legale
    if siret and siren_unite_legale:
        utils_utils.add_validation_error(
            errors,
            "siret",
            "Le champ SIRET et le champ SIREN unité légale ne peuvent pas être remplis en même temps.",
        )
        utils_utils.add_validation_error(
            errors,
            "siren_unite_legale",
            "Le champ SIRET et le champ SIREN unité légale ne peuvent pas être remplis en même temps.",
        )
    elif not siret and not siren_unite_legale:
        utils_utils.add_validation_error(
            errors,
            "siret",
            "Le champ SIRET ou le champ SIREN unité légale ne peuvent pas être vides en même temps.",
        )
        utils_utils.add_validation_error(
            errors,
            "siren_unite_legale",
            "Le champ SIRET ou le champ SIREN unité légale ne peuvent pas être vides en même temps.",
        )
    if instance.is_central_cuisine:
        if not siret:
            utils_utils.add_validation_error(
                errors,
                "siret",
                "Cuisine centrale : le champ ne peut pas être vide.",
            )
        if siren_unite_legale:
            utils_utils.add_validation_error(
                errors,
                "siren_unite_legale",
                "Cuisine centrale : le champ ne peut pas être rempli.",
            )
    return errors


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
