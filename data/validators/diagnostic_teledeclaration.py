from django.core.exceptions import ValidationError

from data.models.diagnostic_teledeclaration_dates import is_in_teledeclaration_or_correction
from data.models.diagnostic_teledeclaration_fields import get_fields_editable_when_is_teledeclared_already


OUT_OF_CAMPAIGN_ERROR_MESSAGES = {
    "edit": "Ce n'est pas possible de modifier un bilan télédéclaré hors de la période de la campagne",
    "teledeclare": "Ce n'est pas possible de télédéclarer hors de la période de la campagne",
    "cancel": "Ce n'est pas possible d'annuler une télédéclaration hors de la période de la campagne",
    "import": "Ce n'est pas possible d'importer des bilans hors de la période de la campagne",
}
OUT_OF_CAMPAIGN_ERROR_MESSAGE_DEFAULT = "Cette action n'est pas possible hors de la période de la campagne"


def validate_is_in_teledeclaration_or_correction_period(action=None):
    """
    action: "edit", "teledeclare", "cancel" or "import" for a specific error message, else a generic error message
    """
    if not is_in_teledeclaration_or_correction():
        raise ValidationError(OUT_OF_CAMPAIGN_ERROR_MESSAGES.get(action, OUT_OF_CAMPAIGN_ERROR_MESSAGE_DEFAULT))


def validate_diagnostic_year_in_teledeclaration_period(instance):
    if not is_in_teledeclaration_or_correction(instance.year):
        raise ValidationError("Ce diagnostic n'est pas dans la bonne année de télédéclaration")


def validate_not_already_teledeclared(instance):
    if instance.is_teledeclared:
        raise ValidationError("Ce diagnostic a déjà été télédéclaré")


def validate_is_teledeclared(instance):
    if not instance.is_teledeclared:
        raise ValidationError("Ce diagnostic doit avoir été télédéclaré")


def validate_diagnostic_is_filled(instance):
    uses_central_kitchen_appro = instance._should_use_central_kitchen_appro()
    if not instance.is_filled and not uses_central_kitchen_appro:
        raise ValidationError("Ce diagnostic n'est pas rempli")


def validate_canteen_is_filled(instance):
    if not instance.canteen.is_filled:
        raise ValidationError("La cantine associée à ce diagnostic n'est pas remplie")


def validate_canteen_groupe_satellites(instance):
    if instance.canteen.is_groupe:
        if instance.canteen.satellites_count == 0:
            raise ValidationError("Le groupe associe à ce diagnostic n'a pas de cantine satellite")
        if instance.canteen.satellites_missing_data_count > 0:
            raise ValidationError(
                f"{instance.canteen.satellites_missing_data_count} satellites du groupe associée à ce diagnostic ne sont pas remplis"
            )


def validate_applicant_is_canteen_manager(instance, applicant):
    if applicant not in instance.canteen.managers.all():
        raise ValidationError("Le déclarant n'est pas un gestionnaire de la cantine associée à ce diagnostic")


def validate_submitted_diagnostic_update(instance):
    """
    Rules when updating an already teledeclared diagnostic (see Diagnostic.is_teledeclared_already)
    - only the fields of some volets can be edited (opt-in, see get_fields_editable_when_is_teledeclared_already)
    - only during the campaign (teledeclaration or correction) of the diagnostic's year
    The changes are detected with django-dirtyfields.
    """
    changed_fields = instance.get_dirty_fields(check_relationship=True)  # {field_name: value_in_db}
    if not changed_fields:
        return

    editable_fields = get_fields_editable_when_is_teledeclared_already(instance.year)
    locked_fields_changed = [field_name for field_name in changed_fields if field_name not in editable_fields]
    if locked_fields_changed:
        raise ValidationError(
            {
                field_name: "Ce champ n'est pas modifiable sur un bilan télédéclaré."
                for field_name in locked_fields_changed
            }
        )

    validate_is_in_teledeclaration_or_correction_period("edit")
    validate_diagnostic_year_in_teledeclaration_period(instance)
