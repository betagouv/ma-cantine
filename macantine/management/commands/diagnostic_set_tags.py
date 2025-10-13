import logging
from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import F, Func, Q

from data.models import Diagnostic
from macantine.utils import CAMPAIGN_DATES

# from simple_history.utils import update_change_reason


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py diagnostic_set_tags --year 2024
    - python manage.py diagnostic_set_tags --year 2024 --apply
    """

    help = "Set tags on diagnostics for a given year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            choices=[2021, 2022, 2023, 2024],
            help="Year to process.",
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
        logger.info(f"Start task: diagnostic_set_tags for year {year}")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        logger.info("Step 1: Stats")
        queryset = Diagnostic.objects.select_related("canteen").in_year(year).teledeclared()
        logger.info(f"Found {queryset.count()} teledeclared diagnostics for year {year}")
        diagnostic_with_tags = queryset.has_tags()
        logger.info(f"has_tags: Found {diagnostic_with_tags.count()} diagnostics")
        diagnostic_with_tags_unnest = diagnostic_with_tags.annotate(
            tags_unnest=Func(F("tags"), function="unnest")
        ).values_list("tags_unnest", flat=True)
        logger.info(f"Tags count: {Counter(diagnostic_with_tags_unnest)}")

        logger.info("Step 2: Clear existing tags")
        if apply:
            queryset.update(tags=None)

        logger.info("Step 3: Set tags")
        self.set_tag_value_total_ht_vide(queryset, apply)
        self.set_tag_value_bio_ht_vide(queryset, apply)
        self.set_tag_cantine_supprimee_pendant_campagne(queryset, year, apply)
        self.set_tag_cantine_sans_siret_ou_siren(queryset, apply)
        self.set_tag_valeurs_aberrantes(queryset, apply)
        self.set_tag_doublon_satellite_centrale(queryset, apply)
        self.set_tag_valeurs_incoherentes(queryset, apply)
        self.set_tag_rapport(queryset, apply)

    def set_tag_value_total_ht_vide(self, queryset, apply):
        # TODO: check
        queryset = queryset.filter(value_total_ht__isnull=True)
        logger.info(f"value_total_ht_vide: Found {queryset.count()} diagnostics")

    def set_tag_value_bio_ht_vide(self, queryset, apply):
        # TODO: check
        queryset = queryset.filter(value_bio_ht__isnull=True)
        logger.info(f"value_bio_ht_vide: Found {queryset.count()} diagnostics")

    def set_tag_cantine_supprimee_pendant_campagne(self, queryset, year, apply):
        queryset = queryset.filter(
            canteen__deletion_date__range=(
                CAMPAIGN_DATES[year]["teledeclaration_start_date"],
                CAMPAIGN_DATES[year]["teledeclaration_end_date"],
            )
        )
        logger.info(f"cantine_supprimee_pendant_campagne: Found {queryset.count()} diagnostics")

    def set_tag_cantine_sans_siret_ou_siren(self, queryset, apply):
        # TODO: check
        queryset = queryset.annotate(
            canteen_siret=F("canteen_snapshot__siret"),
            canteen_siren_unite_legale=F("canteen_snapshot__siren_unite_legale"),
        ).exclude(
            ~Q(canteen_siret=None) & ~Q(canteen_siret="")
            | ~Q(canteen_siren_unite_legale=None) & ~Q(canteen_siren_unite_legale="")
        )
        logger.info(f"cantine_sans_siret_ou_siren: Found {queryset.count()} diagnostics")

    def set_tag_valeurs_aberrantes(self, queryset, apply):
        queryset = queryset.with_meal_price().filter(
            meal_price__isnull=False, meal_price__gt=20, value_total_ht__gt=1000000
        )
        logger.info(f"valeurs_aberrantes: Found {queryset.count()} diagnostics")

    def set_tag_doublon_satellite_centrale(self, queryset, apply):
        # TODO
        pass

    def set_tag_valeurs_incoherentes(self, queryset, apply):
        queryset = queryset.filter(year=2022, teledeclaration_id__in=[9656, 8037])
        logger.info(f"valeurs_incoherentes: Found {queryset.count()} diagnostics")

    def set_tag_rapport(self, queryset, apply):
        # TODO
        pass
