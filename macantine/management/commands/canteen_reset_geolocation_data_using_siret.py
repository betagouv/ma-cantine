import logging
import time

from django.core.management.base import BaseCommand

from common.api.recherche_entreprises import fetch_geo_data_from_siret
from data.models import Canteen

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Script to cleanup the canteen geolocation data (using the SIRET) (API Recherche Entreprises)
    - empty API response: canteen SIRET is probably unknown, reset geolocation data (siret_inconnu will be updated)
    - API response with etat_administratif != "A": canteen SIRET is probably closed, reset geolocation data (siret_etat_administratif will be updated)
    - API response with cityInseeCode different from canteen city_insee_code: reset geolocation data
    - API response with cityInseeCode identical to canteen city_insee_code: update siret_etat_administratif

    Usage:
    - python manage.py canteen_reset_geolocation_data_using_siret
    """

    help = "Reset canteen geolocation data if their SIRET doesn't match with API Recherche Entreprises data"

    def handle(self, *args, **options):
        results = {
            "canteen_siret_unknown": [],
            "canteen_siret_closed": [],
            "canteen_siret_city_insee_code_mismatch": [],
            "canteen_siret_city_insee_code_ok": 0,
        }
        logger.info("Start task: canteen_reset_geolocation_data_using_siret")
        canteen_qs = Canteen.all_objects.has_siret()
        logger.info(f"Found {canteen_qs.count()} canteens with SIRET to process")

        for index, canteen in enumerate(canteen_qs):
            canteen_reset_geolocation_data = False
            response = fetch_geo_data_from_siret(canteen.siret)
            print(f"Canteen {canteen.id} - {canteen.siret} - API response: {response}")
            if not response:
                logger.warning(f"Canteen {canteen.id} - {canteen.siret} - city_insee_code absent")
                canteen_reset_geolocation_data = True
                results["canteen_siret_unknown"].append(canteen.id)
            elif response["etat_administratif"] != "A":
                logger.warning(f"Canteen {canteen.id} - {canteen.siret} - établissement fermé")
                canteen_reset_geolocation_data = True
                results["canteen_siret_closed"].append(canteen.id)
            elif response["cityInseeCode"] != canteen.city_insee_code:
                logger.warning(
                    f"Canteen {canteen.id} - {canteen.siret} - mismatch (API: {response['cityInseeCode']} / Canteen: {canteen.city_insee_code})"
                )
                canteen_reset_geolocation_data = True
                results["canteen_siret_city_insee_code_mismatch"].append(canteen.id)
            else:  # all good
                Canteen.objects.filter(id=canteen.id).update(siret_etat_administratif=response["etat_administratif"])
                results["canteen_siret_city_insee_code_ok"] += 1

            if canteen_reset_geolocation_data:
                time.sleep(0.1)  # avoid calling the API too much (post_save signal will also call the API)
                canteen.reset_geo_fields(with_city_insee_code=True, with_save=True)

            if index % 10 == 0:
                time.sleep(1)  # avoid hitting API rate limits

        logger.info("canteen_siret_unknown", len(results["canteen_siret_unknown"]))
        logger.info("canteen_siret_closed", len(results["canteen_siret_closed"]))
        logger.info("canteen_siret_city_insee_code_mismatch", len(results["canteen_siret_city_insee_code_mismatch"]))
        logger.info("canteen_siret_city_insee_code_ok", results["canteen_siret_city_insee_code_ok"])
        logger.info("End of task: canteen_reset_geolocation_data_using_siret")
