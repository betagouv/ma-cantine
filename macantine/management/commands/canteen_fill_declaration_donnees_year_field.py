import logging

from django.core.management.base import BaseCommand

from data.models import Canteen, Diagnostic

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_declaration_donnees_year_field --year 2025
    """

    help = "Fill canteen declaration_donnees_YEAR field"

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
        logger.info(f"Start task: canteen_fill_declaration_donnees_year_field for year {year}")
        field_name = f"declaration_donnees_{year}"

        logger.info("Step 1: reset the field for all the canteens")
        Canteen.all_objects.all().update(**{field_name: False})

        logger.info("Step 2: find the canteens that have a teledeclaration for the specified year")
        diagnostics_teledeclared = Diagnostic.objects.teledeclared_for_year(year)
        logger.info(f"Found {len(diagnostics_teledeclared)} teledeclarations for year {year}")
        # v2: filter on the canteen_id & declared_data (satellites) of Teledeclarations
        canteens_with_teledeclarations = []
        for dtd in diagnostics_teledeclared.values("canteen_snapshot", "satellites_snapshot"):
            canteens_with_teledeclarations.append(dtd["canteen_snapshot"]["id"])
            if dtd["satellites_snapshot"] and len(dtd["satellites_snapshot"]) > 0:
                for satellite in dtd["satellites_snapshot"]:
                    canteens_with_teledeclarations.append(satellite["id"])

        logger.info("Step 3: update the field")
        Canteen.all_objects.filter(id__in=canteens_with_teledeclarations).update(**{field_name: True})

        # Done!
        logger.info(
            f"Task completed: {Canteen.all_objects.filter(**{field_name: True}).count()} canteens teledeclared for year {year}"
        )
