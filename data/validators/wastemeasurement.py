from datetime import datetime

from common.utils import utils as utils_utils


def validate_dates(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the date fields are the correct format
    - extra validation:
        - period_end_date cannot be in the futur
        - period_start_date must be before period_end_date
        - period_start_date and period_end_date cannot overlap with other WasteMeasurement for the same canteen
    """
    from data.models import WasteMeasurement

    errors = {}

    if instance.period_end_date:
        if instance.period_end_date > datetime.now().date():
            utils_utils.add_validation_error(
                errors, "period_end_date", "La date de fin ne peut pas être dans le futur"
            )

        if instance.period_start_date:
            if instance.period_start_date > instance.period_end_date:
                utils_utils.add_validation_error(
                    errors, "period_start_date", "La date de début ne peut pas être après la date de fin"
                )

            canteen_wm_within_period_qs = WasteMeasurement.objects.filter(canteen=instance.canteen)
            if instance.id:
                canteen_wm_within_period_qs = canteen_wm_within_period_qs.exclude(id=instance.id)
            canteen_wm_within_period_qs = canteen_wm_within_period_qs.filter(
                period_end_date__gte=instance.period_start_date, period_start_date__lte=instance.period_end_date
            )
            if canteen_wm_within_period_qs.exists():
                wm_count = canteen_wm_within_period_qs.count()
                if wm_count > 1:
                    utils_utils.add_validation_error(
                        errors,
                        "_All__",
                        f"Il existe déjà {wm_count} autres évaluations dans la période {instance.period_start_date} à {instance.period_end_date}. Veuillez modifier les évaluations existantes ou corriger les dates de la période.",
                    )
                utils_utils.add_validation_error(
                    errors,
                    "_All__",
                    f"Il existe déjà une autre évaluation dans la période {instance.period_start_date} à {instance.period_end_date}. Veuillez modifier l'évaluation existante ou corriger les dates de la période.",
                )

    return errors
