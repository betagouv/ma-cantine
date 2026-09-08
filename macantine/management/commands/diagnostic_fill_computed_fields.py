import logging

from data.models import Diagnostic
from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


FIELD_LIST = Diagnostic.AGGREGATED_APPRO_FIELDS + Diagnostic.EGALIM_STATS_FIELDS + Diagnostic.OTHER_COMPUTED_FIELDS


class Command(MaCantineBaseCommand):
    """
    Goal: command to fill Diagnostic "computed" fields (see FIELD_LIST)

    Usage:
    - python manage.py diagnostic_fill_computed_fields --year 2025
    """

    help = "Fill diagnostic teledeclared egalim fields for a given year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )

    def handle(self, *args, **options):
        year = options["year"]
        logger.info(f"Start task: diagnostic_fill_computed_fields for year {year}")

        qs = Diagnostic.objects.in_year(year)

        logger.info("Step 1: find the diagnostics for the specified year")
        logger.info(f"Found {qs.count()} diagnostics for year {year}")

        logger.info(
            "Step 2: reset the fields for all the diagnostics (both draft & teledeclared) for the specified year"
        )
        qs.update(**{field_name: None for field_name in FIELD_LIST})

        logger.info("Step 3: fill the fields (and save)")
        for index, diagnostic in enumerate(qs):
            # called in save()
            # diagnostic.populate_aggregated_values()
            # diagnostic.populate_egalim_stats()
            # diagnostic.populate_cout_repas()
            diagnostic.save(update_fields=FIELD_LIST)
            if index % 5000 == 0:
                logger.info(f"Updated {index} diagnostics")

        # Done!
        logger.info(f"Task completed: updated {qs.count()} diagnostics for year {year}")
