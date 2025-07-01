import logging

from django.core.management.base import BaseCommand

from data.models import Canteen, Teledeclaration

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fill canteen teledeclared_YEAR field"

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
        logger.info(f"Start task: fill_canteen_teledeclared_year_field for year {year}")
        field_name = f"teledeclared_{year}"

        # Step 1: reset the field for all the canteens
        Canteen.objects.all().update(**{field_name: None})

        # Step 2: find the canteens that have a teledeclaration for the specified year
        teledeclarations = Teledeclaration.objects.submitted_for_year(year)
        logger.info(f"Found {len(teledeclarations)} teledeclarations for year {year}")
        # v1: filter only on the canteen_id of Teledeclarations
        # canteens_with_teledeclarations = teledeclarations.values_list("canteen_id", flat=True).distinct()
        # v2: filter on the canteen_id & declared_data (satellites) of Teledeclarations
        canteens_with_teledeclarations = []
        for td in teledeclarations.values("canteen_id", "declared_data"):
            canteens_with_teledeclarations.append(td["canteen_id"])
            if "satellites" in td["declared_data"]:
                for satellite in td["declared_data"]["satellites"]:
                    canteens_with_teledeclarations.append(satellite["id"])

        # Step 3: update the field for all the canteens
        Canteen.objects.filter(id__in=canteens_with_teledeclarations).update(**{field_name: True})
        Canteen.objects.exclude(**{field_name: True}).update(**{field_name: False})

        # Done!
        logger.info(
            f"Task completed: {Canteen.objects.filter(**{field_name: True}).count()} canteens teledeclared for year {year}"
        )
