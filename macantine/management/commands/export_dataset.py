from django.core.management.base import BaseCommand

from macantine.tasks import (
    export_dataset_canteen_analysis,
    export_dataset_canteen_opendata,
    export_dataset_td_analysis,
    export_dataset_td_opendata,
)


class Command(BaseCommand):
    """
    Exemples:
    - python manage.py export_dataset --model Canteen --destination analysis
    - python manage.py export_dataset --model Canteen --destination opendata
    - python manage.py export_dataset --model Teledeclaration --destination analysis
    - python manage.py export_dataset --model Teledeclaration --destination opendata
    """

    help = "Command to export datasets. 4 choices: Cantines (analysis) ; Cantines (opendata) ; Toutes les TD (analysis) ; TD par années (opendata)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            dest="model",
            type=str,
            choices=["Canteen", "Teledeclaration"],
            required=True,
            help="Choose the model to export",
        )
        parser.add_argument(
            "--destination",
            dest="destination",
            type=str,
            choices=["analysis", "opendata"],
            required=True,
            help="Choose the destination of the export",
        )

    def handle(self, *args, **options):
        model = options["model"]
        destination = options["destination"]

        if model == "Canteen":
            if destination == "analysis":
                export_dataset_canteen_analysis()
            elif destination == "opendata":
                export_dataset_canteen_opendata()
        elif model == "Teledeclaration":
            if destination == "analysis":
                export_dataset_td_analysis()
            elif destination == "opendata":
                export_dataset_td_opendata()
