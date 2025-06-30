from django.core.management.base import BaseCommand

from macantine.tasks import (
    datasets_export_analysis_canteens,
    datasets_export_analysis_td,
    datasets_export_opendata_canteens,
    datasets_export_opendata_td,
)


class Command(BaseCommand):
    help = "Export datasets"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dataset",
            dest="export_type",
            type=int,
            required=True,
            help="Choose the type of dataset you want to extract \n 1. Cantines (opendata)\n 2. Cantines (Metabase)\n 3. Ensemble des TD (Metabase)\n 4. TD par années (opendata)",
        )

    def handle(self, *args, **options):
        export_type = options["export_type"]
        if export_type == 1:
            datasets_export_opendata_canteens()
        elif export_type == 2:
            datasets_export_analysis_canteens()
        elif export_type == 3:
            datasets_export_analysis_td()
        elif export_type == 4:
            datasets_export_opendata_td()
        else:
            print("Invalid argument. Choose 1,2 or 3")
