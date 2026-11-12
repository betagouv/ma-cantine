import logging
from collections import Counter

from common.api.datagouv import map_pat_list_to_communes_insee_code
from common.api.decoupage_administratif import map_communes_infos, map_epcis_code_name
from common.utils.commands import MaCantineBaseCommand
from data.models import Canteen
from macantine.tasks import fill_missing_canteen_geo_fields_from_insee_code

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Fill the missing (empty) geo fields of canteens that have a city_insee_code
    (API Découpage Administratif & DataGouv PAT dataset, cached: no API call per canteen)
    - same logic as the post_save signal (fill_missing_canteen_geo_fields_from_insee_code): existing values are never overwritten
    - loops over all the canteens with a city_insee_code (including deleted ones), and only saves the updated ones
    - saves with update_fields (only the updated geo fields): modification_date is not updated

    Use case: backfill canteens created without their geo fields (e.g. SIRET canteens created with a city_insee_code
    between the geobots removal (#6691) and #7603)

    Possible v2 (e.g. when adding new geo fields, such as PNR or SCOT):
    - --fields: only process some fields (e.g. --fields pnr scot), and only load the needed data sources
    - --overwrite: update the fields to match the current dataset (replace or clear the existing values, instead of
      only filling the empty ones), only for the fields that fully come from a dataset (epci, pat, department,
      region, *_lib...), never for city & postal_code (can be filled by the user, and a commune can have multiple
      postal codes)
    - it would then replace canteen_update_pat_data_using_city_insee_code (--fields pat_list pat_lib_list --overwrite)
      (port its tests, and update docs/geo.md)

    Usage:
    - python manage.py canteen_fill_missing_geo_data_using_city_insee_code
    - python manage.py canteen_fill_missing_geo_data_using_city_insee_code --apply
    """

    help = "Fill the missing geo fields of canteens using their city_insee_code"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        logger.info("Start task: canteen_fill_missing_geo_data_using_city_insee_code")
        apply = options["apply"]

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        communes_details = map_communes_infos()
        epcis_names = map_epcis_code_name()
        pat_mapping = map_pat_list_to_communes_insee_code()

        canteen_qs = Canteen.all_objects.has_city_insee_code().order_by("id")
        logger.info(f"Found {canteen_qs.count()} canteens with a city_insee_code")

        canteen_updated_count = 0
        field_updated_counter = Counter()

        for canteen in canteen_qs.iterator():
            updated_fields = fill_missing_canteen_geo_fields_from_insee_code(
                canteen, communes_details, epcis_names, pat_mapping
            )
            if updated_fields:
                canteen_updated_count += 1
                field_updated_counter.update(updated_fields)
                if apply:
                    canteen._change_reason = (
                        "Données de localisation complétées (canteen_fill_missing_geo_data_using_city_insee_code)"
                    )
                    canteen.save(skip_validations=True, update_fields=updated_fields)

        logger.info(f"Canteens {'updated' if apply else 'to update'}: {canteen_updated_count}")
        for field_name, count in sorted(field_updated_counter.items()):
            logger.info(f"- {field_name}: {count}")
