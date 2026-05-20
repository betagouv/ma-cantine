import logging

from django.core.management.base import BaseCommand

from common.api.datagouv import fetch_commune_pat_list, map_pat_list_to_communes_insee_code, PAT_DATAGOUV_DATE
from data.models import Canteen
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py canteen_update_pat_data_using_city_insee_code
    - python manage.py canteen_update_pat_data_using_city_insee_code --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        logger.info("Start task: canteen_update_pat_data_using_city_insee_code")
        apply = options["apply"]

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        pat_mapping = map_pat_list_to_communes_insee_code()
        logger.info(
            f"Fetched PAT mapping for {len(pat_mapping)} communes from data.gouv.fr dataset (PAT_DATAGOUV_DATE={PAT_DATAGOUV_DATE})"
        )

        results = {"canteen_updated": 0, "pat_list_updated": 0, "pat_lib_list_updated": 0}

        canteen_qs = Canteen.all_objects.exclude(has_charfield_missing_query("city_insee_code"))
        logger.info(f"Found {canteen_qs.count()} canteens with a city_insee_code")

        for index, canteen in enumerate(canteen_qs):
            expected_pat_list = fetch_commune_pat_list(canteen.city_insee_code, pat_mapping, "id") or []
            expected_pat_lib_list = fetch_commune_pat_list(canteen.city_insee_code, pat_mapping, "lib") or []
            if (canteen.pat_list != expected_pat_list) or (canteen.pat_lib_list != expected_pat_lib_list):
                if canteen.pat_list != expected_pat_list:
                    canteen.pat_list = expected_pat_list
                    results["pat_list_updated"] += 1
                if canteen.pat_lib_list != expected_pat_lib_list:
                    canteen.pat_lib_list = expected_pat_lib_list
                    results["pat_lib_list_updated"] += 1
                results["canteen_updated"] += 1
                if apply:
                    canteen._change_reason = (
                        f"Données PAT MAJ ({PAT_DATAGOUV_DATE}) (canteen_update_pat_data_using_city_insee_code)"
                    )
                    canteen.save(skip_validations=True, update_fields=Canteen.GEO_PAT_FIELDS)

        logger.info(f"Finished processing {canteen_qs.count()} canteens")
        logger.info(f"Canteens updated: {results['canteen_updated']}")
        logger.info(f"Updated pat_list: {results['pat_list_updated']}")
        logger.info(f"Updated pat_lib_list: {results['pat_lib_list_updated']}")
