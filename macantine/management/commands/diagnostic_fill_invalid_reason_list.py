import logging

from django.core.management.base import BaseCommand
from django.db.models import F, Func, Value

from data.utils import has_arrayfield_missing_query
from data.models import Diagnostic
from data.models.diagnostic import (
    canteen_deleted_query,
    canteen_has_siret_or_siren_unite_legale_query,
    canteen_soft_deleted_during_campaign_query,
    teledeclaration_mode_satellite_without_appro_query,
    aberrant_values_query,
    incoherent_values_query,
    valeur_bio_agg_is_filled_query,
    valeur_totale_is_filled_query,
)

logger = logging.getLogger(__name__)


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


class Command(BaseCommand):
    """
    Goal: fill the invalid_reason_list field

    Usage:
    - python manage.py diagnostic_fill_invalid_reason_list --year 2024
    - python manage.py diagnostic_fill_invalid_reason_list --year 2024 --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        year = options["year"]
        apply = options["apply"]

        logger.info(f"Starting task: diagnostic_fill_invalid_reason_list, campaign {year}")
        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        diagnostic_qs = Diagnostic.objects.teledeclared_for_year(year=year).filter(
            generated_from_groupe_diagnostic=False
        )

        fill_invalid_reason_CANTINE_SUPPRIMEE(diagnostic_qs, apply)
        fill_invalid_reason_CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE(diagnostic_qs, year, apply)
        fill_invalid_reason_CANTINE_SANS_SIRET_OU_SIREN(diagnostic_qs, apply)
        fill_invalid_reason_TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO(diagnostic_qs, apply)
        fill_invalid_reason_VALEUR_TOTALE_VIDE(diagnostic_qs, apply)
        fill_invalid_reason_VALEUR_BIO_AGG_VIDE(diagnostic_qs, apply)
        fill_invalid_reason_VALEURS_ABERRANTES(diagnostic_qs, apply)
        fill_invalid_reason_VALEURS_INCOHERENTES(diagnostic_qs, apply)
        # fill_invalid_reason_DOUBLON_1TD1SITE()  # done in teledeclaration_generate_1td1site.py

        diagnostic_qs = diagnostic_qs.exclude(has_arrayfield_missing_query("invalid_reason_list"))
        logger.info("Task completed: diagnostic_fill_invalid_reason_list")
        logger.info(f"Found {diagnostic_qs.count()} diagnostics with an invalid reason")


def fill_invalid_reason_CANTINE_SUPPRIMEE(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: CANTINE_SUPPRIMEE")
    invalid_reason = Diagnostic.InvalidReason.CANTINE_SUPPRIMEE

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(canteen_deleted_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen deleted")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE(diagnostic_qs, year, apply):
    logger.info("fill_invalid_reason: CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE")
    invalid_reason = Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(canteen_soft_deleted_during_campaign_query(year))
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen deleted during campaign for the year {year}")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_CANTINE_SANS_SIRET_OU_SIREN(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: CANTINE_SANS_SIRET_OU_SIREN")
    invalid_reason = Diagnostic.InvalidReason.CANTINE_SANS_SIRET_OU_SIREN

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.exclude(canteen_has_siret_or_siren_unite_legale_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen siret or siren_unite_legale null")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO")
    invalid_reason = Diagnostic.InvalidReason.TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(teledeclaration_mode_satellite_without_appro_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with mode teledeclaration satellite without appro")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_VALEUR_TOTALE_VIDE(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: VALEUR_TOTALE_VIDE")
    invalid_reason = Diagnostic.InvalidReason.VALEUR_TOTALE_VIDE

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.exclude(valeur_totale_is_filled_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with valeur_totale null")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_VALEUR_BIO_AGG_VIDE(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: VALEUR_BIO_AGG_VIDE")
    invalid_reason = Diagnostic.InvalidReason.VALEUR_BIO_AGG_VIDE

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.exclude(valeur_bio_agg_is_filled_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with valeur_bio_agg null")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_VALEURS_ABERRANTES(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: VALEURS_ABERRANTES")
    invalid_reason = Diagnostic.InvalidReason.VALEURS_ABERRANTES

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.with_meal_price().filter(aberrant_values_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with aberrant values")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)


def fill_invalid_reason_VALEURS_INCOHERENTES(diagnostic_qs, apply):
    logger.info("fill_invalid_reason: VALEURS_INCOHERENTES")
    invalid_reason = Diagnostic.InvalidReason.VALEURS_INCOHERENTES

    # Step 1: cleanup
    if apply:
        _remove_invalid_reason_item(invalid_reason)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(incoherent_values_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with incoherent values")

    # Step 3: update
    if apply:
        _append_invalid_reason_item(diagnostic_qs, invalid_reason)
