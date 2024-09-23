import logging

from django.core.management.base import BaseCommand

from macantine.tasks import fill_missing_geolocation_data_using_siret

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Export datasets TD and canteens to the 'media/open_data' folder of the configured file system (local or s3)"
    )

    def handle(self, *args, **options):
        logger.info("Start task : fill_missing_geolocation_data")
        fill_missing_geolocation_data_using_siret()
