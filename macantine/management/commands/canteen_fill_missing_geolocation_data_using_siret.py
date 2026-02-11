import logging

from django.core.management.base import BaseCommand

from macantine.tasks import fill_missing_insee_code_using_siret

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_missing_geolocation_data_using_siret
    """

    help = "Fill missing geolocation data for canteens using SIRET and API Recherche Entreprises"

    def handle(self, *args, **options):
        logger.info("Start task : canteen_fill_missing_geolocation_data_using_siret")
        fill_missing_insee_code_using_siret()
