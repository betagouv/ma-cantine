import logging

from django.core.management.base import BaseCommand
from django.db.models import F, Func, Value

from data.models import Diagnostic
from data.models.diagnostic import (
    aberrant_values_query,
    canteen_deleted_query,
    canteen_has_siret_or_siren_unite_legale_query,
    canteen_soft_deleted_during_campaign_query,
    circuit_court_gt_france_query,
    commerce_equitable_gt_bio_query,
    incoherent_values_query,
    local_gt_france_query,
    teledeclaration_mode_satellite_without_appro_query,
    valeur_bio_agg_is_filled_query,
    valeur_totale_is_filled_query,
)
from data.utils import has_arrayfield_missing_query

logger = logging.getLogger(__name__)


def _remove_reason_item(field_prefix, reason_item):
    """
    field: "invalid" or "warning"
    """
    Diagnostic.objects.filter(**{f"{field_prefix}_reason_list__contains": [reason_item]}).update(
        **{
            f"{field_prefix}_reason_list": Func(
                F(f"{field_prefix}_reason_list"),
                Value(reason_item),
                function="array_remove",
            )
        }
    )


def _append_reason_item(qs, field_prefix, reason_item):
    qs.update(
        **{
            f"{field_prefix}_reason_list": Func(
                F(f"{field_prefix}_reason_list"),
                Value(reason_item),
                function="array_append",
            )
        }
    )


class Command(BaseCommand):
    """
    Goal: fill the invalid_reason_list & warning_reason_list fields

    Usage:
    - python manage.py diagnostic_fill_invalid_warning_reason_list --year 2024
    - python manage.py diagnostic_fill_invalid_warning_reason_list --year 2024 --apply
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

        logger.info(f"Starting task: diagnostic_fill_invalid_warning_reason_list, campaign {year}")
        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        diagnostic_qs = Diagnostic.objects.teledeclared_for_year(year=year).filter(
            generated_from_groupe_diagnostic=False
        )

        #########################################################
        # invalid_reason_list
        fill_invalid_reason_CANTINE_SUPPRIMEE(diagnostic_qs, apply)
        fill_invalid_reason_CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE(diagnostic_qs, year, apply)
        fill_invalid_reason_CANTINE_SANS_SIRET_OU_SIREN(diagnostic_qs, apply)
        fill_invalid_reason_TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO(diagnostic_qs, apply)
        fill_invalid_reason_VALEUR_TOTALE_VIDE(diagnostic_qs, apply)
        fill_invalid_reason_VALEUR_BIO_AGG_VIDE(diagnostic_qs, apply)
        fill_invalid_reason_VALEURS_ABERRANTES(diagnostic_qs, apply)
        fill_invalid_reason_VALEURS_INCOHERENTES(diagnostic_qs, apply)
        # fill_invalid_reason_DOUBLON_1TD1SITE()  # done in teledeclaration_generate_1td1site.py

        #########################################################
        # warning_reason_list
        fill_warning_reason_CIRCUIT_COURT_GT_FRANCE(diagnostic_qs, apply)
        fill_warning_reason_LOCAL_GT_FRANCE(diagnostic_qs, apply)
        fill_warning_reason_COMMERCE_EQUITABLE_GT_BIO(diagnostic_qs, apply)

        logger.info("Task completed: diagnostic_fill_invalid_warning_reason_list")
        diagnostic_invalid_qs = diagnostic_qs.exclude(has_arrayfield_missing_query("invalid_reason_list"))
        logger.info(f"Found {diagnostic_invalid_qs.count()} diagnostics with an invalid reason")
        diagnostic_warning_qs = diagnostic_qs.exclude(has_arrayfield_missing_query("warning_reason_list"))
        logger.info(f"Found {diagnostic_warning_qs.count()} diagnostics with a warning reason")


def fill_invalid_reason_CANTINE_SUPPRIMEE(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.CANTINE_SUPPRIMEE
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(canteen_deleted_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen deleted")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE(diagnostic_qs, year, apply):
    reason_item = Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(canteen_soft_deleted_during_campaign_query(year))
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen deleted during campaign for the year {year}")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_CANTINE_SANS_SIRET_OU_SIREN(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.CANTINE_SANS_SIRET_OU_SIREN
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.exclude(canteen_has_siret_or_siren_unite_legale_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with canteen siret or siren_unite_legale null")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.TELEDECLARATION_MODE_SATELLITE_WITHOUT_APPRO
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(teledeclaration_mode_satellite_without_appro_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with mode teledeclaration satellite without appro")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_VALEUR_TOTALE_VIDE(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.VALEUR_TOTALE_VIDE
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.exclude(valeur_totale_is_filled_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with valeur_totale null")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_VALEUR_BIO_AGG_VIDE(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.VALEUR_BIO_AGG_VIDE
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.exclude(valeur_bio_agg_is_filled_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with valeur_bio_agg null")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_VALEURS_ABERRANTES(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.VALEURS_ABERRANTES
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.with_meal_price().filter(aberrant_values_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with aberrant values")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_invalid_reason_VALEURS_INCOHERENTES(diagnostic_qs, apply):
    reason_item = Diagnostic.InvalidReason.VALEURS_INCOHERENTES
    logger.info(f"fill_invalid_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("invalid", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(incoherent_values_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with incoherent values")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "invalid", reason_item)


def fill_warning_reason_CIRCUIT_COURT_GT_FRANCE(diagnostic_qs, apply):
    reason_item = Diagnostic.WarningReason.CIRCUIT_COURT_GT_FRANCE
    logger.info(f"fill_warning_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("warning", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(circuit_court_gt_france_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with circuit court > origine France")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "warning", reason_item)


def fill_warning_reason_LOCAL_GT_FRANCE(diagnostic_qs, apply):
    reason_item = Diagnostic.WarningReason.LOCAL_GT_FRANCE
    logger.info(f"fill_warning_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("warning", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(local_gt_france_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with local > origine France")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "warning", reason_item)


def fill_warning_reason_COMMERCE_EQUITABLE_GT_BIO(diagnostic_qs, apply):
    reason_item = Diagnostic.WarningReason.COMMERCE_EQUITABLE_GT_BIO
    logger.info(f"fill_warning_reason: {reason_item}")

    # Step 1: cleanup
    if apply:
        _remove_reason_item("warning", reason_item)

    # Step 2: queryset
    diagnostic_qs = diagnostic_qs.filter(commerce_equitable_gt_bio_query())
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with commerce equitable > bio")

    # Step 3: update
    if apply:
        _append_reason_item(diagnostic_qs, "warning", reason_item)
