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
    - python manage.py canteen_update_geolocation_data_using_siret
    """

    help = "Update canteen geolocation data if their SIRET doesn't match with API Recherche Entreprises data"

    def handle(self, *args, **options):
        results = {
            "canteen_siret_unknown": [],
            "canteen_siret_closed": [],
            "canteen_siret_city_insee_code_mismatch": [],
            "canteen_siret_city_insee_code_ok": 0,
            "canteen_updated": 0,
        }
        logger.info("Start task: canteen_update_geolocation_data_using_siret")
        canteen_qs = Canteen.all_objects.has_siret()
        logger.info(f"Found {canteen_qs.count()} canteens with SIRET to process")

        for index, canteen in enumerate(canteen_qs):
            updated = False
            response = fetch_geo_data_from_siret(canteen.siret)
            if not response:
                logger.warning(f"Canteen {canteen.id} - {canteen.siret} - city_insee_code absent")
                if not canteen.siret_inconnu:
                    canteen.siret_inconnu = True
                    canteen.siret_etat_administratif = None
                    updated = True
                results["canteen_siret_unknown"].append(canteen.id)
            else:
                # check if city_insee_code from API matches canteen city_insee_code
                if response["cityInseeCode"] != canteen.city_insee_code:
                    logger.warning(
                        f"Canteen {canteen.id} - {canteen.siret} - mismatch (API: {response['cityInseeCode']} / Canteen: {canteen.city_insee_code})"
                    )
                    # TODO: reset_geo_fields
                    results["canteen_siret_city_insee_code_mismatch"].append(canteen.id)
                else:  # all good
                    results["canteen_siret_city_insee_code_ok"] += 1
                # check if etat_administratif is not "A" (active)
                if response["etat_administratif"] != "A":
                    logger.warning(f"Canteen {canteen.id} - {canteen.siret} - établissement fermé")
                    results["canteen_siret_closed"].append(canteen.id)
                # check if etat_administratif has changed
                if canteen.siret_etat_administratif != response["etat_administratif"]:
                    canteen.siret_etat_administratif = response["etat_administratif"]
                    updated = True

            if updated:
                canteen._change_reason = "Données de localisation MAJ"
                canteen.save(skip_validations=True)
                results["canteen_updated"] += 1

            if index % 10 == 0:
                time.sleep(1)  # avoid hitting API rate limits

        logger.info(f"canteen_siret_unknown: {len(results['canteen_siret_unknown'])}")
        logger.info(f"canteen_siret_closed: {len(results['canteen_siret_closed'])}")
        logger.info(
            f"canteen_siret_city_insee_code_mismatch: {len(results['canteen_siret_city_insee_code_mismatch'])}"
        )
        logger.info(f"canteen_siret_city_insee_code_ok: {results['canteen_siret_city_insee_code_ok']}")
        logger.info(f"canteen_updated: {results['canteen_updated']}")
        logger.info("End of task: canteen_update_geolocation_data_using_siret")
