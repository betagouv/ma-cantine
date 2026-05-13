import logging
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from common.api.recherche_entreprises import fetch_geo_data_from_siret
from data.models import Canteen
from data.utils import read_csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Script to cleanup the canteen geolocation data (using the SIRET) (API Recherche Entreprises)
    - empty API response: canteen SIRET is probably unknown, reset geolocation data (siret_inconnu will be updated)
    - API response with etat_administratif != "A": canteen SIRET is probably closed, reset geolocation data (siret_etat_administratif will be updated)
    - API response with cityInseeCode different from canteen city_insee_code: reset geolocation data
    - API response with postalCode different from canteen postal_code: reset geolocation data
    - API response with cityInseeCode identical to canteen city_insee_code: update siret_etat_administratif

    Usage:
    - python manage.py canteen_update_geolocation_data_using_siret
    - python manage.py canteen_update_geolocation_data_using_siret --cache-csv stats/recherche_entreprises_cache.csv
    - python manage.py canteen_update_geolocation_data_using_siret --apply
    """

    help = "Update canteen geolocation data if their SIRET doesn't match with API Recherche Entreprises data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cache-csv",
            dest="cache_csv",
            type=str,
            default=None,
            help="Optional cache CSV exported by canteen_export_recherche_entreprises_cache_csv.",
        )
        parser.add_argument(
            "--logging",
            action="store_true",
            help="Enable logging of canteens with SIRET issues (unknown, closed, city_insee_code mismatch, postal_code mismatch).",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        enable_logging = options.get("logging", False)
        apply_changes = options.get("apply", False)
        cache_by_siret = self._load_cache_by_siret(options.get("cache_csv"))

        results = {
            "canteen_siret_unknown": [],
            "canteen_siret_closed": [],
            "canteen_siret_city_insee_code_mismatch": [],
            "canteen_siret_city_insee_code_ok": 0,
            "canteen_siret_postal_code_mismatch": [],
            "canteen_siret_postal_code_ok": 0,
            "canteen_to_update": 0,
            "canteen_updated": 0,
        }
        logger.info("Start task: canteen_update_geolocation_data_using_siret")
        logger.info("Mode: %s", "apply" if apply_changes else "dry-run")
        canteen_qs = Canteen.all_objects.has_siret().order_by("siret")
        logger.info(f"Found {canteen_qs.count()} canteens with SIRET to process")

        for index, canteen in enumerate(canteen_qs):
            pending_changes = {}
            response, source = self._get_geo_data(canteen.siret, cache_by_siret)
            if not response:
                if enable_logging:
                    logger.warning(f"Canteen {canteen.id} - {canteen.siret} - city_insee_code absent")
                if not canteen.siret_inconnu:
                    pending_changes["siret_inconnu"] = True
                    pending_changes["siret_etat_administratif"] = None
                results["canteen_siret_unknown"].append(canteen.id)
            else:
                city_insee_code = response.get("city_insee_code")
                postal_code = response.get("postal_code")
                etat_administratif = response.get("etat_administratif")

                # check if city_insee_code from API matches canteen city_insee_code
                if canteen.city_insee_code and canteen.city_insee_code != city_insee_code:
                    if enable_logging:
                        logger.warning(
                            f"Canteen {canteen.id} - {canteen.siret} - mismatch ({source}: {city_insee_code} / Canteen: {canteen.city_insee_code})"
                        )
                    results["canteen_siret_city_insee_code_mismatch"].append(canteen.id)
                else:  # all good
                    results["canteen_siret_city_insee_code_ok"] += 1
                    # also check if postal code matches (only for canteens with matching city_insee_code, to avoid noise)
                    if canteen.postal_code and canteen.postal_code != postal_code:
                        if enable_logging:
                            logger.warning(
                                f"Canteen {canteen.id} - {canteen.siret} - postal code mismatch ({source}: {postal_code} / Canteen: {canteen.postal_code})"
                            )
                        results["canteen_siret_postal_code_mismatch"].append(canteen.id)
                    else:
                        results["canteen_siret_postal_code_ok"] += 1

                # check if etat_administratif is not "A" (active)
                if etat_administratif != "A":
                    if enable_logging:
                        logger.warning(f"Canteen {canteen.id} - {canteen.siret} - établissement fermé")
                    results["canteen_siret_closed"].append(canteen.id)
                # check if etat_administratif has changed
                if canteen.siret_etat_administratif != etat_administratif:
                    pending_changes["siret_etat_administratif"] = etat_administratif

            should_update = (
                (len(pending_changes) > 0)
                or (canteen.id in results["canteen_siret_city_insee_code_mismatch"])
                or (canteen.id in results["canteen_siret_postal_code_mismatch"])
            )
            if should_update:
                results["canteen_to_update"] += 1
                if apply_changes:
                    if canteen.id in results["canteen_siret_city_insee_code_mismatch"]:
                        canteen.reset_geo_fields(with_city_insee_code=True, with_save=False)
                    elif canteen.id in results["canteen_siret_postal_code_mismatch"]:
                        canteen.reset_geo_fields(with_city_insee_code=False, with_save=False)
                    # after reset_geo_fields, because siret_* have been reset
                    if len(pending_changes) > 0:
                        for field_name, field_value in pending_changes.items():
                            setattr(canteen, field_name, field_value)

                    canteen._change_reason = "Données de localisation MAJ"
                    canteen.save(skip_validations=True)
                    results["canteen_updated"] += 1

            if source == "api" and index > 0 and index % 10 == 0:
                time.sleep(1)  # avoid hitting API rate limits

        logger.info(f"canteen_siret_unknown: {len(results['canteen_siret_unknown'])}")
        logger.info(f"canteen_siret_closed: {len(results['canteen_siret_closed'])}")
        logger.info(f"canteen_siret_city_insee_code_ok: {results['canteen_siret_city_insee_code_ok']}")
        logger.info(
            f"canteen_siret_city_insee_code_mismatch: {len(results['canteen_siret_city_insee_code_mismatch'])}"
        )
        if results["canteen_siret_city_insee_code_mismatch"]:
            logger.info(f"Example (canteen_id): {results['canteen_siret_city_insee_code_mismatch'][0]}")
        logger.info(f"canteen_siret_postal_code_ok: {results['canteen_siret_postal_code_ok']}")
        logger.info(f"canteen_siret_postal_code_mismatch: {len(results['canteen_siret_postal_code_mismatch'])}")
        if results["canteen_siret_postal_code_mismatch"]:
            logger.info(f"Example (canteen_id): {results['canteen_siret_postal_code_mismatch'][0]}")
        logger.info(f"canteen_to_update: {results['canteen_to_update']}")
        logger.info(f"canteen_updated: {results['canteen_updated']}")
        logger.info("End of task: canteen_update_geolocation_data_using_siret")

    @staticmethod
    def _load_cache_by_siret(cache_csv):
        if not cache_csv:
            return {}

        cache_path = Path(cache_csv)
        if not cache_path.exists():
            raise CommandError(f"Cache CSV file not found: {cache_csv}")

        rows = read_csv(cache_path)
        cache_by_siret = {}
        for row in rows:
            siret = row.get("siret")
            if siret:
                cache_by_siret[siret] = row

        logger.info("Loaded %s SIRETs from cache CSV %s", len(cache_by_siret), cache_path)
        return cache_by_siret

    @staticmethod
    def _response_from_cache_row(cache_row):
        status = cache_row.get("status")
        if status == "ok" and cache_row.get("city_insee_code"):
            return {
                "city_insee_code": cache_row.get("city_insee_code"),
                "postal_code": cache_row.get("postal_code"),
                "etat_administratif": cache_row.get("etat_administratif"),
            }
        if status == "not_found":
            return None
        return "fallback_to_api"

    def _get_geo_data(self, siret, cache_by_siret):
        cache_row = cache_by_siret.get(siret)
        if cache_row:
            cache_response = self._response_from_cache_row(cache_row)
            if cache_response != "fallback_to_api":
                return cache_response, "cache"

        return fetch_geo_data_from_siret(siret), "api"
