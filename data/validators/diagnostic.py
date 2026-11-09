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
