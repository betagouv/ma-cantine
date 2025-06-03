import logging

from django.core.management.base import BaseCommand

from common.api.decoupage_administratif import fetch_commune_detail, map_communes_infos
from data.models import Teledeclaration
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    TDs from 2021 & 2022 contain only a small subset of canteen data (when serialized in declared_data).
    This one-time command aims to fill the missing canteen geolocation data (department and region) for these TDs.
    """

    def handle(self, *args, **options):
        logger.info("Start task: fill_missing_td_canteen_geolocation_data")

        logger.info("Step 1: Fetch geo data from API Découpage Administratif")
        communes_details = map_communes_infos()

        logger.info("Step 2: Fetch TDs with missing canteen geo data (department or region)")
        td_with_canteen_geo_data_missing = Teledeclaration.objects.filter(
            has_charfield_missing_query("declared_data__canteen__department")
            | has_charfield_missing_query("declared_data__canteen__region")
        ).distinct()
        logger.info(f"Step 2: Found {td_with_canteen_geo_data_missing.count()} TDs with missing canteen geo data")

        logger.info("Step 3: Update TDs with missing canteen geo data")
        for i, td in enumerate(td_with_canteen_geo_data_missing):
            td_declared_data = td.declared_data
            if "canteen" in td_declared_data:
                if "city_insee_code" in td_declared_data["canteen"]:
                    td_canteen_city_insee_code = td_declared_data["canteen"]["city_insee_code"]
                    if td_canteen_city_insee_code in communes_details:
                        td_declared_data["canteen"]["department"] = fetch_commune_detail(
                            td_canteen_city_insee_code, communes_details, "department"
                        )
                        td_declared_data["canteen"]["region"] = fetch_commune_detail(
                            td_canteen_city_insee_code, communes_details, "region"
                        )
                        td.declared_data = td_declared_data
                        td.save()
            if i > 0 and i % 200 == 0:
                logger.info(f"Step 3: Updated {i} TDs with missing canteen geo data")
