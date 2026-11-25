import logging
import time
from collections import defaultdict

from common.api.recherche_entreprises import (
    RECHERCHE_ENTREPRISES_DATA_STATUS_NOT_FOUND,
    RECHERCHE_ENTREPRISES_DATA_STATUS_OK,
    fetch_recherche_entreprises_data,
)
from common.utils.commands import MaCantineBaseCommand
from data.models import Canteen

logger = logging.getLogger(__name__)

DEFAULT_SLEEP_SECONDS = 0.25  # API rate limit: 400/min


class Command(MaCantineBaseCommand):
    """
    Fill the canteens' recherche_entreprises_data field (API Recherche Entreprises)
    - canteens with a SIRET: unite_legale & etablissement data
    - canteens without SIRET, but with a SIREN (siren_unite_legale): unite_legale data only
    - loops over all the canteens (including deleted ones)
    - 1 API call per distinct SIRET / SIREN (shared by all its canteens), with a sleep between calls
    - API error: the canteens are left unchanged (run again with --only-missing to retry them)
    - saves with a queryset update: no post_save signal, no history, modification_date is not updated

    Usage:
    - python manage.py canteen_update_recherche_entreprises_data_using_siret_or_siren
    - python manage.py canteen_update_recherche_entreprises_data_using_siret_or_siren --apply
    - python manage.py canteen_update_recherche_entreprises_data_using_siret_or_siren --only-missing --apply
    """

    help = "Fill the canteens' recherche_entreprises_data field using their SIRET (or SIREN)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--only-missing",
            action="store_true",
            help="Only process the canteens never fetched (e.g. after an API error), or whose SIRET / SIREN changed.",
            default=False,
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        logger.info("Start task: canteen_update_recherche_entreprises_data_using_siret_or_siren")
        only_missing = options["only_missing"]
        apply = options["apply"]

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        canteen_ids_by_identifier = self._get_canteen_ids_by_identifier(only_missing)
        logger.info(
            f"Found {sum(len(ids) for ids in canteen_ids_by_identifier.values())} canteens to process "
            f"({len(canteen_ids_by_identifier)} distinct SIRET / SIREN)"
        )

        results = {
            "api_calls": 0,
            RECHERCHE_ENTREPRISES_DATA_STATUS_OK: 0,
            RECHERCHE_ENTREPRISES_DATA_STATUS_NOT_FOUND: 0,
            "api_error": 0,
            "canteen_api_error": 0,
            "canteen_updated": 0,
        }

        for index, ((source, query), canteen_ids) in enumerate(canteen_ids_by_identifier.items(), start=1):
            data = fetch_recherche_entreprises_data(**{source: query})
            results["api_calls"] += 1
            if data is None:
                results["api_error"] += 1
                results["canteen_api_error"] += len(canteen_ids)
            else:
                results[data["status"]] += 1
                if apply:
                    Canteen.all_objects.filter(id__in=canteen_ids).update(recherche_entreprises_data=data)
                results["canteen_updated"] += len(canteen_ids)

            if index % 1000 == 0:
                logger.info(f"Progress: {index}/{len(canteen_ids_by_identifier)}")

            time.sleep(DEFAULT_SLEEP_SECONDS)

        logger.info(f"API calls: {results['api_calls']}")
        logger.info(f"Status ok: {results[RECHERCHE_ENTREPRISES_DATA_STATUS_OK]}")
        logger.info(f"Status not_found: {results[RECHERCHE_ENTREPRISES_DATA_STATUS_NOT_FOUND]}")
        logger.info(f"API errors: {results['api_error']} ({results['canteen_api_error']} canteens unchanged)")
        logger.info(f"Canteens {'updated' if apply else 'to update'}: {results['canteen_updated']}")
        logger.info("End of task: canteen_update_recherche_entreprises_data_using_siret_or_siren")

    @staticmethod
    def _get_canteen_ids_by_identifier(only_missing):
        """
        Group the canteen ids by identifier: (source, query), e.g. ("siret", "21340172201787") or ("siren", "213401722")
        - the SIRET is used if present, otherwise the SIREN
        - only_missing: skip the canteens already fetched with their current identifier
        """
        canteen_ids_by_identifier = defaultdict(list)
        canteen_qs = (
            Canteen.all_objects.has_siret_or_siren_unite_legale()
            .order_by("siret", "siren_unite_legale", "id")
            .values("id", "siret", "siren_unite_legale", "recherche_entreprises_data")
        )
        for canteen in canteen_qs.iterator():
            source, query = (
                ("siret", canteen["siret"]) if canteen["siret"] else ("siren", canteen["siren_unite_legale"])
            )
            if only_missing:
                data = canteen["recherche_entreprises_data"] or {}
                if data.get("source") == source and data.get("query") == query:
                    continue
            canteen_ids_by_identifier[(source, query)].append(canteen["id"])
        return canteen_ids_by_identifier
