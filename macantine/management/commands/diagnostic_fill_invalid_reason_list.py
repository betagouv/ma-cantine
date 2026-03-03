import logging

from django.core.management.base import BaseCommand
from django.db.models import F, Func, Value

from data.models import Diagnostic
from data.models.diagnostic import canteen_deleted_during_campaign_query, canteen_has_siret_or_siren_unite_legale_query
from macantine.utils import CAMPAIGN_DATES

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py diagnostic_fill_invalid_reason_list
    """

    def handle(self, *args, **options):
        logger.info("Start task: diagnostic_fill_invalid_reason_list")

        fill_invalid_reason_VALUE_BIO_HT_VIDE()
        fill_invalid_reason_CANTINE_SANS_SIRET_OU_SIREN()
        fill_invalid_reason_VALUE_TOTAL_HT_VIDE()

        for year in CAMPAIGN_DATES.keys():
            fill_invalid_reason_CANTINE_SUPPRIMEE_PENDANT_CAMPAGNE(year)


def _remove_invalid_reason_item(invalid_reason):
    Diagnostic.objects.filter(invalid_reason_list__contains=[invalid_reason]).update(
        invalid_reason_list=Func(
            F("invalid_reason_list"),
            Value(invalid_reason),
            function="array_remove",
        )
    )


def _append_invalid_reason_item(qs, invalid_reason):
    qs.update(
        invalid_reason_list=Func(
            F("invalid_reason_list"),
            Value(invalid_reason),
            function="array_append",
        )
    )


def fill_invalid_reason_VALUE_TOTAL_HT_VIDE():
    invalid_reason = "VALUE_TOTAL_HT_VIDE"

    # Step 1: cleanup
    _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    logger.info(f"Start filling invalid_reason_list for {invalid_reason}")
    diagnostic_qs = Diagnostic.objects.filter(valeur_total_ht=0)
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with valeur_total_ht = 0")

    # Step 3: update
    _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_VALUE_BIO_HT_VIDE():
    invalid_reason = "VALUE_BIO_HT_VIDE"

    # Step 1: cleanup
    _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    logger.info(f"Start filling invalid_reason_list for {invalid_reason}")
    diagnostic_qs = Diagnostic.objects.filter(valeur_bio_ht=0)
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with valeur_bio_ht = 0")

    # Step 3: update
    _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_CANTINE_SANS_SIRET_OU_SIREN():
    invalid_reason = "CANTINE_SANS_SIRET_OU_SIREN"

    # Step 1: cleanup
    _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    logger.info(f"Start filling invalid_reason_list for {invalid_reason}")
    diagnostic_qs = Diagnostic.objects.filter(canteen_has_siret_or_siren_unite_legale_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen_siret null")

    # Step 3: update
    _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_CANTINE_SUPPRIMEE_PENDANT_CAMPAGNE(year):
    invalid_reason = "CANTINE_SUPPRIMEE_PENDANT_CAMPAGNE"

    # Step 1: cleanup
    _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    logger.info(f"Start filling invalid_reason_list for {invalid_reason} for the year {year}")
    diagnostic_qs = Diagnostic.objects.filter(canteen_deleted_during_campaign_query(year))
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen deleted during campaign for the year {year}")

    # Step 3: update
    _append_invalid_reason_item(diagnostic_qs, invalid_reason)
