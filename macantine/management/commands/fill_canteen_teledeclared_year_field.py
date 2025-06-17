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
        logger.info(f"Start task : fill_canteen_teledeclared_year_field for year {year}")
        field_name = f"teledeclared_{year}"

        # Reset the field for all canteens
        Canteen.objects.all().update(**{field_name: None})

        # Update the field for canteens that have a teledeclaration for the specified year
        teledeclarations = Teledeclaration.objects.submitted_for_year(year)
        canteens_with_teledeclarations = teledeclarations.values_list("canteen_id", flat=True).distinct()
        Canteen.objects.filter(id__in=canteens_with_teledeclarations).update(**{field_name: True})
        Canteen.objects.exclude(**{field_name: True}).update(**{field_name: False})

        logger.info(
            f"Task completed: {Canteen.objects.filter(**{field_name: True}).count()} canteens teledeclared for year {year}"
        )
