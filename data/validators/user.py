from common.utils import utils as utils_utils


def validate_user_non_staff(instance):
    """
    - extra validation:
        - a user cannot have a TOTP device if they are not staff
    """
    errors = {}
    field_name = "is_staff"
    if not instance.is_staff:
        if instance.pk:
            if instance.totpdevice_set.exists():
                utils_utils.add_validation_error(
                    errors,
                    field_name,
                    "Un utilisateur ne peut pas avoir d'appareil 2FA (TOTP) s'il n'est pas staff.",
                )
    return errors


def validate_user_superuser(instance):
    """
    - extra validation:
        - a user cannot become superuser if they are not staff
        - a user cannot become superuser if they don't have a confirmed TOTP device
    """
    errors = {}
    field_name = "is_superuser"
    if instance.is_superuser:
        if not instance.is_staff:
            utils_utils.add_validation_error(
                errors,
                field_name,
                "Un utilisateur ne peut pas devenir superuser s'il n'est pas staff.",
            )
    return errors
