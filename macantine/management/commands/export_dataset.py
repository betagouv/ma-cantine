import logging

from django.core.management.base import CommandError

from common.utils.commands import MaCantineBaseCommand
from macantine.etl.datasets import (
    export_datasets,
    get_canteen_opendata_datasets,
    get_raw_analysis_datasets,
    get_teledeclaration_opendata_datasets,
)

logger = logging.getLogger(__name__)

# (model, destination) -> function returning the datasets to export
DATASETS = {
    ("Canteen", "opendata"): get_canteen_opendata_datasets,
    ("Teledeclaration", "opendata"): get_teledeclaration_opendata_datasets,
    ("Raw", "analysis"): get_raw_analysis_datasets,
}


class Command(MaCantineBaseCommand):
    """
    Export datasets (see macantine/etl/datasets.py)
    - Canteen (opendata): the canteens, to data.gouv.fr
    - Teledeclaration (opendata): the teledeclarations by year, to data.gouv.fr
    - Raw (analysis): the raw tables, to the analytics data warehouse (Metabase, dbt sources)

    Usage:
    - python manage.py export_dataset --model Canteen --destination opendata
    - python manage.py export_dataset --model Teledeclaration --destination opendata
    - python manage.py export_dataset --model Raw --destination analysis
    """

    help = "Export datasets. 3 choices: Cantines (opendata) ; TD par années (opendata) ; Raw (analysis)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            dest="model",
            type=str,
            choices=["Canteen", "Teledeclaration", "Raw"],
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

        get_datasets = DATASETS.get((model, destination))
        if get_datasets is None:
            choices = ", ".join(f"{m} ({d})" for m, d in DATASETS)
            raise CommandError(f"No dataset for {model} ({destination}). Choices: {choices}")

        logger.info(f"Start task: export_dataset {model} ({destination})")
        export_datasets(get_datasets())
