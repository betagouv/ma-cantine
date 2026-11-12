import logging

from django.core.management import CommandError

from common.utils.commands import MaCantineBaseCommand
from data.models import Canteen
from data.models.diagnostic import Diagnostic

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Goal: pre-fill the satellites_nombre_repas_an field of the groupes' diagnostics
    - the list of the groupe's satellites, with an empty value for the new ones (see Diagnostic.sync_satellites_nombre_repas_an)
    - only the diagnostics not teledeclared (the teledeclared ones are frozen)

    Usage:
    - python manage.py diagnostic_fill_satellites_nombre_repas_an --year 2026
    - python manage.py diagnostic_fill_satellites_nombre_repas_an --year 2026 --apply
    """

    help = "Pre-fill the satellites_nombre_repas_an field of the groupes' diagnostics for a given year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the diagnostics to process (2026 or later)",
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
        logger.info(f"Start task: diagnostic_fill_satellites_nombre_repas_an for year {year} (apply={apply})")

        if year < 2026:
            raise CommandError("The field satellites_nombre_repas_an only exists since 2026.")

        logger.info("Step 1: find the groupes' diagnostics (not teledeclared) for the specified year")
        qs = (
            Diagnostic.objects.in_year(year)
            .not_teledeclared()
            .filter(canteen__production_type=Canteen.ProductionType.GROUPE)
            .select_related("canteen")
        )
        logger.info(f"Found {qs.count()} diagnostics for year {year}")

        logger.info("Step 2: sync the satellites list (and the total)")
        updated_count = 0
        for diagnostic in qs:
            value_before = diagnostic.satellites_nombre_repas_an
            diagnostic.sync_satellites_nombre_repas_an()
            diagnostic.populate_satellites_nombre_repas_an_total()
            if diagnostic.satellites_nombre_repas_an == value_before:
                continue
            updated_count += 1
            if apply:
                # no need for a historical record
                diagnostic.save_without_historical_record(
                    update_fields=["satellites_nombre_repas_an", "satellites_nombre_repas_an_total"],
                    skip_validations=True,
                )

        if apply:
            logger.info(f"Task completed: updated {updated_count} diagnostics for year {year}")
        else:
            logger.info(f"Dry run: {updated_count} diagnostics would be updated for year {year}")
