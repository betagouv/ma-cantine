from django.core.exceptions import ValidationError

from data.models.diagnostic_teledeclaration_dates import is_in_teledeclaration_or_correction


def validate_is_in_teledeclaration_or_correction_period(action):
    """
    action: "teledeclare" or "cancel"
    """
    if is_in_teledeclaration_or_correction():
        return
    if action == "teledeclare":
        raise ValidationError("Ce n'est pas possible de télédéclarer hors de la période de la campagne")
    elif action == "cancel":
        raise ValidationError("Ce n'est pas possible d'annuler une télédéclaration hors de la période de la campagne")


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
