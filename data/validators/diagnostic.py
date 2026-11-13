from django.utils import timezone

from data.models.diagnostic_teledeclaration_dates import (
    CAMPAIGN_DATES,
    get_current_campaign_year,
    get_year_campaign_end_date_or_today_date,
    get_year_correction_end_date_or_campaign_end_date_or_today_date,
)
from common.utils import utils as utils_utils


def validate_year(instance):
    """
    - extra validation:
        - year must be filled
        - year must be an integer
        - year must be in CAMPAIGN_DATES
    """
    errors = {}
    field_name = "year"
    value = getattr(instance, field_name)
    if value in [None, ""]:
        utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
    elif not (isinstance(value, int) or (isinstance(value, str) and value.isdigit())):
        utils_utils.add_validation_error(errors, field_name, "Le champ doit être un nombre entier.")
    else:
        # year is an integer
        if not isinstance(value, int) or value not in CAMPAIGN_DATES:
            utils_utils.add_validation_error(
                errors, field_name, f"L'année doit être parmi {', '.join(map(str, CAMPAIGN_DATES.keys()))}."
            )
    return errors


def validate_satellites_nombre_repas_an_list(instance):
    """
    [NEW in 2026] Groupe: the nombre_repas_an of each satellite must be empty or a positive integer
    - the structure (one item per satellite of the groupe) is rebuilt in save() (see sync_satellites_nombre_repas_an_list)
    """
    errors = {}
    field_name = "satellites_nombre_repas_an_list"
    value = getattr(instance, field_name)
    error_message = (
        'Format attendu : [{"id": <id de la cantine satellite>, "nombre_repas_an": <nombre entier positif ou null>}]'
    )
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        utils_utils.add_validation_error(errors, field_name, error_message)
        return errors
    for item in value:
        nombre_repas_an = item.get("nombre_repas_an")
        if nombre_repas_an is not None and (
            not isinstance(nombre_repas_an, int)
            or isinstance(nombre_repas_an, bool)
            or not (0 <= nombre_repas_an <= 999999999)
        ):
            utils_utils.add_validation_error(errors, field_name, error_message)
            return errors
    return errors


def validate_groupe_satellites_nombre_repas_an(instance):
    """
    [NEW in 2026] Groupe: the nombre_repas_an of each satellite (see satellites_nombre_repas_an_list)
    - each satellite must have a value
    - the groupe's nombre_repas_an must be equal to the sum of the satellites' values
    NOTE: not checked in save() (drafts can be filled progressively), but by is_clean() (/check & teledeclaration)
    """
    errors = {}
    if validate_year(instance) or int(instance.year) < 2026:
        return errors
    if not instance.canteen_id or not instance.canteen.is_groupe:
        return errors
    if validate_satellites_nombre_repas_an_list(instance):
        return errors  # invalid format: already reported

    from data.models import Canteen  # avoid circular import

    satellite_dict = Canteen.all_objects.in_bulk([item["id"] for item in instance.satellites_nombre_repas_an_list])
    for item in instance.satellites_nombre_repas_an_list:
        satellite_name = getattr(satellite_dict.get(item["id"]), "name", item["id"])
        if item["nombre_repas_an"] is None:
            utils_utils.add_validation_error(
                errors,
                "satellites_nombre_repas_an_list",
                f"Le nombre de repas par an du satellite « {satellite_name} » est obligatoire.",
            )

    satellites_nombre_repas_an_sum = instance.satellites_nombre_repas_an_sum
    if (
        instance.nombre_repas_an is not None
        and satellites_nombre_repas_an_sum is not None
        and instance.nombre_repas_an != satellites_nombre_repas_an_sum
    ):
        utils_utils.add_validation_error(
            errors,
            "nombre_repas_an",
            f"Le nombre de repas par an du groupe ({instance.nombre_repas_an}) doit être égal à la somme "
            f"des nombres de repas par an des satellites ({satellites_nombre_repas_an_sum}).",
        )
    return errors


def validate_year_and_can_edit(instance):
    """
    - extra validation:
        - year must be in the current campaign year (campaign year & the next one, e.g. 2026 & 2027 during the 2026 campaign)
          (see get_current_campaign_year: the previous year, or TELEDECLARATION_YEAR_OVERRIDE)
        - if year is valid:
            - after teledeclaration end date, DRAFT diagnostic cannot be edited anymore
            - after correction end date, any diagnostic cannot be edited anymore
    """
    errors = {}
    field_name = "year"
    value = getattr(instance, field_name)
    now = timezone.now()
    campaign_year = get_current_campaign_year()
    current_campaign_years = [campaign_year, campaign_year + 1]
    if int(value) not in current_campaign_years:
        utils_utils.add_validation_error(
            errors,
            field_name,
            f"L'année doit être dans l'année de campagne en cours ({', '.join(map(str, current_campaign_years))}).",
        )
    # year is valid, check can_edit validation
    else:
        if instance.pk:
            if now > get_year_campaign_end_date_or_today_date(value):
                if instance.status == instance.DiagnosticStatus.DRAFT:
                    utils_utils.add_validation_error(
                        errors,
                        field_name,
                        f"Le diagnostic de l'année {value} ne peut plus être modifié car la campagne de télédéclaration est terminée.",
                    )
            if now > get_year_correction_end_date_or_campaign_end_date_or_today_date(value):
                utils_utils.add_validation_error(
                    errors,
                    field_name,
                    f"Le diagnostic de l'année {value} ne peut plus être modifié car la période de correction est terminée.",
                )
    return errors


def validate_diagnostic_type(instance):
    """
    - extra validation:
        - diagnostic_type must be filled
        - diagnostic_type must be among the allowed values
    """
    errors = {}
    field_name = "diagnostic_type"
    value = getattr(instance, field_name)
    if value not in instance.DiagnosticType.values:
        utils_utils.add_validation_error(
            errors,
            field_name,
            f"Le type de diagnostic doit être parmi {instance.DiagnosticType.values}.",
        )
    return errors


def validate_canteen_fields_required(instance):
    """
    - clean_fields() (called by full_clean()) already does some checks
    - extra validation: depending on the year of the diagnostic
        - [NEW in 2026] nombre_repas_an is required
    """
    errors = {}
    if instance.year:
        if int(instance.year) >= 2026:
            required_fields = instance.CANTEEN_FIELDS
            for field in required_fields:
                if getattr(instance, field) is None:
                    utils_utils.add_validation_error(
                        errors, field, f"Ce champ est obligatoire pour l'année {instance.year}."
                    )
    return errors
