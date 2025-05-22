from django.core.management.base import BaseCommand

from macantine.etl.utils import compare_datasets


class Command(BaseCommand):
    help = "Compare two versions of the dataset Teledeclaration stored in the datawarehouse"

    def add_arguments(self, parser):
        parser.add_argument(
            "--version-A",
            dest="dataset_A",
            type=str,
            required=True,
            help="The name of the table in the Datawarehouse that stores the version A of the dataset to compare",
        )
        parser.add_argument(
            "--version-B",
            dest="dataset_B",
            type=str,
            required=True,
            help="The name of the table in the Datawarehouse that stores the version A of the dataset to compare",
        )

    def handle(self, *args, **options):
        compare_datasets(options["dataset_A"], options["dataset_B"])
