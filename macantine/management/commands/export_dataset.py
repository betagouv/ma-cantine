import logging
from django.core.management.base import BaseCommand
from macantine.tasks import export_datasets

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Export datasets TD and canteens to the 'media/open_data' folder of the configured file system (local or s3)"

    def handle(self, *args, **options):
        export_datasets()
