from common.utils import utils as utils_utils


def validate_user_non_staff(instance):
    """
    - extra validation:
        - a user cannot have a TOTP device if they are not staff
    """
    errors = {}
    if not instance.is_staff:
        if instance.pk:
            if instance.totpdevice_set.exists():
                utils_utils.add_validation_error(
                    errors,
                    "is_staff",
                    "Un utilisateur ne peut pas avoir d'appareil 2FA (OTP) s'il n'est pas staff.",
                )
    return errors


def validate_user_superuser(instance):
    """
    - extra validation:
        - a user cannot become superuser if they are not staff
        - a user cannot become superuser if they don't have a confirmed TOTP device
    """
    errors = {}
    if instance.is_superuser:
        if not instance.is_staff:
            utils_utils.add_validation_error(
                errors,
                "is_superuser",
                "Un utilisateur ne peut pas devenir superuser s'il n'est pas staff.",
            )
        if not instance.pk:
            utils_utils.add_validation_error(
                errors,
                "is_superuser",
                "Créer d'abord un utilisateur staff, puis configurer un appareil 2FA (OTP), avant de pouvoir devenir superuser.",
            )
        elif not instance.totpdevice_set.filter(confirmed=True).exists():
            utils_utils.add_validation_error(
                errors,
                "is_superuser",
                "Un utilisateur ne peut devenir superuser que s'il a déjà configuré un appareil 2FA (OTP).",
            )
    return errors
