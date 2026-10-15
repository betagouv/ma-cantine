import logging

from data.models import Diagnostic
from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


FIELD_LIST = Diagnostic.APPRO_AGGREGATED_FIELDS + Diagnostic.APPRO_STATS_FIELDS + Diagnostic.OTHER_COMPUTED_FIELDS


class Command(MaCantineBaseCommand):
    """
    Goal: command to fill Diagnostic "computed" fields (see FIELD_LIST)

    Usage:
    - python manage.py diagnostic_fill_computed_fields --year 2025
    - python manage.py diagnostic_fill_computed_fields --year 2025 --field pourcentage_bio --field pourcentage_egalim
    """

    help = "Fill diagnostic teledeclared egalim fields for a given year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )
        parser.add_argument(
            "--field",
            action="append",
            choices=FIELD_LIST,
            dest="field_list",
            help="Only fill this computed field (can be repeated). Default: all the computed fields",
        )

    def handle(self, *args, **options):
        year = options["year"]
        field_list = options["field_list"] or FIELD_LIST
        logger.info(f"Start task: diagnostic_fill_computed_fields for year {year} (fields: {field_list})")

        # all_objects: also include the diagnostics generated from a groupe diagnostic
        qs = Diagnostic.all_objects.in_year(year)

        logger.info("Step 1: find the diagnostics for the specified year")
        logger.info(f"Found {qs.count()} diagnostics for year {year}")

        logger.info(
            "Step 2: reset the fields for all the diagnostics (both draft & teledeclared) for the specified year"
        )
        qs.update(**{field_name: None for field_name in field_list})

        logger.info("Step 3: fill the fields (and save)")
        for index, diagnostic in enumerate(qs):
            # called in save()
            # diagnostic.populate_aggregated_values()
            # diagnostic.populate_stats_values()
            # diagnostic.populate_cout_repas()
            # computed fields only: no need for a historical record
            diagnostic.save_without_historical_record(update_fields=field_list)
            if index % 5000 == 0:
                logger.info(f"Updated {index} diagnostics")

        # Done!
        logger.info(f"Task completed: updated {qs.count()} diagnostics for year {year}")
