from common.utils import utils as utils_utils

CANTEEN_DAILY_MEAL_COUNT_MIN = 3
CANTEEN_YEARLY_MEAL_COUNT_MIN = 420


def validate_canteen_siret_or_siren_unite_legale(instance):
    """
    - clean_fields() (called by full_clean()) already checks that
    the siret and siren_unite_legale fields are the correct length and format
    - extra validation:
        - siret & siren_unite_legale: at least one must be filled
        - siret & siren_unite_legale: both cannot be filled at the same time
        - if groupe: only the siren_unite_legale field must be filled
        - if central: only the siret field must be filled
        - if siret: must be unique (NOTE: check is done on all, NOT on all_objects)
    """
    errors = {}
    siret = instance.siret
    siren_unite_legale = instance.siren_unite_legale
    if siret and siren_unite_legale:
        utils_utils.add_validation_error(
            errors, "siret", "Le champ SIRET et le champ SIREN unité légale ne peuvent pas être remplis en même temps."
        )
        utils_utils.add_validation_error(
            errors,
            "siren_unite_legale",
            "Le champ SIRET et le champ SIREN unité légale ne peuvent pas être remplis en même temps.",
        )
    elif not siret and not siren_unite_legale:
        utils_utils.add_validation_error(
            errors, "siret", "Le champ SIRET ou le champ SIREN unité légale ne peuvent pas être vides en même temps."
        )
        utils_utils.add_validation_error(
            errors,
            "siren_unite_legale",
            "Le champ SIRET ou le champ SIREN unité légale ne peuvent pas être vides en même temps.",
        )
    if instance.is_groupe:
        if not siren_unite_legale:
            utils_utils.add_validation_error(errors, "siren_unite_legale", "Groupe : le champ ne peut pas être vide.")
        if siret:
            utils_utils.add_validation_error(errors, "siret", "Groupe : le champ ne peut pas être rempli.")
    if instance.is_central_cuisine:
        if not siret:
            utils_utils.add_validation_error(errors, "siret", "Cuisine centrale : le champ ne peut pas être vide.")
        if siren_unite_legale:
            utils_utils.add_validation_error(
                errors, "siren_unite_legale", "Cuisine centrale : le champ ne peut pas être rempli."
            )
    if siret:
        from data.models import Canteen

        canteen_with_siret_qs = Canteen.objects.filter(siret=siret)
        if instance.id:
            canteen_with_siret_qs = canteen_with_siret_qs.exclude(pk=instance.id)
        if canteen_with_siret_qs.exists():
            utils_utils.add_validation_error(errors, "siret", "Le SIRET est déjà utilisé par une autre cantine.")
    return errors


def validate_canteen_management_type_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is in the choices
    - extra validation:
        - the field must be filled
    """
    errors = {}
    field_name = "management_type"
    value = getattr(instance, field_name)
    if value in [None, ""]:
        utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    return errors


def validate_canteen_production_type_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is in the choices
    - extra validation:
        - the field must be filled
        - CENTRAL and CENTRAL_SERVING types are no longer allowed (only on change for now, to avoid breaking tests)
    """
    errors = {}
    field_name = "production_type"
    value = getattr(instance, field_name)
    if value in [None, ""]:
        utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    if instance.id:
        if field_name in instance.get_dirty_fields():
            if value in [instance.ProductionType.CENTRAL, instance.ProductionType.CENTRAL_SERVING]:
                utils_utils.add_validation_error(
                    errors, field_name, "Les types CENTRAL et CENTRAL_SERVING ne sont plus autorisées."
                )
    return errors


def validate_canteen_economic_model_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is in the choices
    - extra validation:
        - if groupe: the field must be empty
        - if not groupe: the field must be filled
    """
    errors = {}
    field_name = "economic_model"
    value = getattr(instance, field_name)
    if instance.is_groupe:
        if value not in [None, ""]:
            utils_utils.add_validation_error(errors, field_name, "Groupe : le champ doit être vide.")
    else:
        if value in [None, ""]:
            utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    return errors


def validate_canteen_meal_count_fields(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is an integer >= 0
    - extra validation:
        - daily_meal_count & yearly_meal_count must be filled
        - daily_meal_count & yearly_meal_count must be integers
        - daily_meal_count < yearly_meal_count
        - daily_meal_count >= 3
        - yearly_meal_count >= 420
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
    if not errors:
        if int(instance.daily_meal_count) < CANTEEN_DAILY_MEAL_COUNT_MIN:
            utils_utils.add_validation_error(
                errors, "daily_meal_count", f"Le champ doit être au moins égal à {CANTEEN_DAILY_MEAL_COUNT_MIN}."
            )
        if int(instance.yearly_meal_count) < CANTEEN_YEARLY_MEAL_COUNT_MIN:
            utils_utils.add_validation_error(
                errors, "yearly_meal_count", f"Le champ doit être au moins égal à {CANTEEN_YEARLY_MEAL_COUNT_MIN}."
            )
    if not errors:
        if int(instance.daily_meal_count) >= int(instance.yearly_meal_count):
            utils_utils.add_validation_error(
                errors, "daily_meal_count", "Le champ doit être inférieur au nombre de repas servis annuellement."
            )
            utils_utils.add_validation_error(
                errors, "yearly_meal_count", "Le champ doit être supérieur au nombre de repas servis quotidiennement."
            )
    return errors


def validate_canteen_sector_list_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the value is a list (empty or with Sectors)
    - extra validation:
        - if groupe/central: the sector_list should be empty
        - if not groupe/central: the sector_list should be between 1 & 3
    """
    errors = {}
    field_name = "sector_list"
    value = getattr(instance, field_name)
    if value is not None:  # check done in clean_fields()
        if instance.is_groupe or instance.is_central:
            if len(value):
                utils_utils.add_validation_error(errors, field_name, "Cuisine centrale : le champ doit être vide.")
        else:
            if (len(value) == 0) or (len(value) > 3):
                utils_utils.add_validation_error(errors, field_name, "Le champ doit contenir entre 1 et 3 secteurs.")
    return errors


def validate_canteen_line_ministry_field(instance):
    """
    Rule: line_ministry must be filled if at least one sector has has_line_ministry=True
    - clean_fields() (called by full_clean()) already checks that the value is in the choices
    - extra validation:
        - if groupe: the sector_list should be empty, so line_ministry should be empty too
        - if not groupe:
            - if at least one sector has has_line_ministry=True: line_ministry must be filled and if economic_model is public
            - else: line_ministry must be empty
    """
    errors = {}
    field_name = "line_ministry"
    value = getattr(instance, field_name)
    if instance.is_groupe:
        if value:
            utils_utils.add_validation_error(errors, field_name, "Groupe : le champ doit être vide.")
    elif not instance.is_public:
        if value:
            utils_utils.add_validation_error(
                errors, field_name, "Le champ doit être vide car le modèle modèle économique n'est pas 'Public'."
            )
    else:
        if instance.sector_list:
            from data.models.sector import SECTOR_HAS_LINE_MINISTRY_LIST

            sectors_with_line_ministry = [
                sector for sector in instance.sector_list if sector in SECTOR_HAS_LINE_MINISTRY_LIST
            ]

            if len(sectors_with_line_ministry) > 0 and not value:
                utils_utils.add_validation_error(
                    errors,
                    field_name,
                    "Le champ doit être rempli car vous avez sélectionné au moins un secteur nécessitant un ministère de tutelle.",
                )
            elif len(sectors_with_line_ministry) == 0 and value:
                utils_utils.add_validation_error(
                    errors,
                    field_name,
                    "Le champ doit être vide car vous n'avez pas sélectionné de secteur nécessitant un ministère de tutelle.",
                )
    return errors


def validate_canteen_groupe_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the groupe field is a valid Canteen or empty
    - extra validation:
        - if groupe: canteen must be a satellite
        - if groupe: related canteen must be a groupe
        - if groupe: must not be self
    """
    errors = {}
    field_name = "groupe"
    try:
        value = getattr(instance, field_name)
        if value:
            if not instance.is_satellite:
                utils_utils.add_validation_error(
                    errors, field_name, "Le champ ne peut être rempli que pour les restaurants satellites."
                )
            elif not value.is_groupe:
                utils_utils.add_validation_error(
                    errors, field_name, "Le champ doit être une cantine de type 'Groupe'."
                )
            elif instance.id:
                if value.id == instance.id:
                    utils_utils.add_validation_error(
                        errors, field_name, "Le champ ne peut pas être égal à la cantine elle-même."
                    )
    except instance.DoesNotExist:
        utils_utils.add_validation_error(errors, field_name, "Cette cantine groupe n'existe pas.")
    return errors


def validate_canteen_central_producer_siret_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that
    the central_producer_siret field is the correct length and format
    - extra validation:
        - if groupe or satellite: central_producer_siret is not mandatory
        - if satellite & central_producer_siret: must be different from the satellite siret
        - if not groupe or satellite: central_producer_siret must be empty
    """
    errors = {}
    field_name = "central_producer_siret"
    value = getattr(instance, field_name)
    if instance.is_groupe or instance.is_satellite:
        if value:
            if instance.siret == value:
                utils_utils.add_validation_error(
                    errors, field_name, "Restaurant satellite : le champ ne peut pas être égal au SIRET du satellite."
                )
    else:
        if value:
            utils_utils.add_validation_error(
                errors, field_name, "Le champ ne peut être rempli que pour les groupes ou les restaurants satellites."
            )
    return errors
