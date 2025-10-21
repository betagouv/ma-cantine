from common.utils import utils as utils_utils


def validate_canteen_siret_or_siren_unite_legale(instance):
    """
    - clean_fields() (called by full_clean()) already checks that
    the siret and siren_unite_legale fields are the correct length and format
    - extra validation:
        - siret or siren_unite_legale must be filled
        - both cannot be filled at the same time
        - central: only the siret field should be filled
        - if siret & new canteen: check that siret is not already used by another canteen
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
    if siret and not instance.pk:
        from data.models import Canteen

        if Canteen.objects.filter(siret=siret).exists():
            utils_utils.add_validation_error(
                errors,
                "siret",
                "Le SIRET est déjà utilisé par une autre cantine.",
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
        - daily_meal_count < yearly_meal_count
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
    if not errors:
        if int(instance.daily_meal_count) >= int(instance.yearly_meal_count):
            utils_utils.add_validation_error(
                errors,
                "daily_meal_count",
                "Le nombre de repas servis quotidiennement doit être inférieur au nombre de repas servis annuellement.",
            )
            utils_utils.add_validation_error(
                errors,
                "yearly_meal_count",
                "Le nombre de repas servis annuellement doit être supérieur au nombre de repas servis quotidiennement.",
            )
    return errors


def validate_canteen_central_producer_siret_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that
    the central_producer_siret field is the correct length and format
    - extra validation:
        - satellite: central_producer_siret must be filled
        - not satellite: central_producer_siret must be empty
    """
    errors = {}
    field_name = "central_producer_siret"
    value = getattr(instance, field_name)
    if instance.is_satellite:
        if not value:
            utils_utils.add_validation_error(
                errors,
                "central_producer_siret",
                "Cantine satellite : le champ ne peut pas être vide.",
            )
    else:
        if value:
            utils_utils.add_validation_error(
                errors,
                "central_producer_siret",
                "Le champ ne peut être rempli que pour les cantines satellites.",
            )
    return errors
