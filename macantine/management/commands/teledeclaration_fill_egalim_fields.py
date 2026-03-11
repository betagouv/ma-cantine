import logging

from django.core.management.base import BaseCommand

from data.models import Diagnostic

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Goal: after adding the Diagnostic.TELEDECLARATION_EGALIM_FIELDS, command to fill those fields

    Usage:
    - python manage.py teledeclaration_fill_egalim_fields --year 2025
    """

    help = "Fill diagnostic teledeclared egalim fields for a given year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            dest="year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )

    def handle(self, *args, **options):
        year = options["year"]
        logger.info(f"Start task: teledeclaration_fill_egalim_fields for year {year}")
        fields = Diagnostic.TELEDECLARATION_EGALIM_FIELDS

        logger.info("Step 1: reset the field for all the diagnostics")
        Diagnostic.all_objects.all().update(**{field_name: None for field_name in fields})

        logger.info("Step 2: find the diagnostics that have a teledeclaration for the specified year")
        diagnostics_teledeclared = Diagnostic.objects.teledeclared_for_year(year)
        logger.info(f"Found {diagnostics_teledeclared.count()} teledeclarations for year {year}")

        logger.info("Step 3: update the egalim fields for the diagnostics with teledeclaration")
        counter = 0
        for diagnostic in diagnostics_teledeclared:
            diagnostic.populate_egalim_stats()
            diagnostic.save(update_fields=fields)
            counter += 1
            if counter % 5000 == 0:
                logger.info(f"Updated {counter} diagnostics teledeclared for year {year}")

        # Done!
        logger.info(
            f"Task completed: updated {diagnostics_teledeclared.count()} diagnostics teledeclared for year {year}"
        )
