import logging
from collections import Counter

from django.core.management.base import BaseCommand
from simple_history.utils import update_change_reason

from data.models import Canteen

logger = logging.getLogger(__name__)


def canteen_central_to_groupe(canteen_central):
    return {
        "production_type": Canteen.ProductionType.GROUPE,
        "siret": None,
        "siren_unite_legale": canteen_central.siret[:9] if canteen_central.siret else None,
        "economic_model": None,
        "satellite_canteens_count": None,
        "sector_list": [],
    }


def satellite_from_central_dict(canteen_central_dict):
    return {
        "name": canteen_central_dict["name"] + " - Satellite",
        "siret": canteen_central_dict["siret"],
        "siren_unite_legale": canteen_central_dict["siren_unite_legale"],
        "management_type": canteen_central_dict["management_type"],
        "production_type": Canteen.ProductionType.ON_SITE_CENTRAL,
        "economic_model": canteen_central_dict["economic_model"],
        "daily_meal_count": canteen_central_dict["daily_meal_count"],
        "yearly_meal_count": canteen_central_dict["yearly_meal_count"],
        "groupe_id": canteen_central_dict["id"],
        # "central_producer_siret": canteen_central_dict["siret"],  # would make an error because same as 'siret'
        "sector_list": canteen_central_dict["sector_list"],
    }


class Command(BaseCommand):
    """
    Rules:
    - CENTRAL => GROUPE
    - CENTRAL_SERVING => GROUPE + create satellite
    - link between groupe & satellites is done via the 'groupe' FK
    - what if the canteen has validation errors? to avoid errors, we ignore them (skip validations on save)

    Usage:
    - python manage.py canteen_migrate_central_to_groupe
    - python manage.py canteen_migrate_central_to_groupe --apply
    """

    help = "Migrate canteens: from CENTRAL/CENTRAL_SERVING to GROUPE"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        logger.info("Start task: canteen_migrate_central_to_groupe")
        apply = options["apply"]

        if not apply:
            print("Dry run mode, no changes will be applied.")

        # stats before
        canteen_central_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.CENTRAL)
        canteen_central_serving_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        canteen_groupe_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.GROUPE)
        logger.info(f"Found {canteen_central_qs.count()} CENTRAL canteens to migrate to GROUPE")
        logger.info(f"Found {canteen_central_serving_qs.count()} CENTRAL_SERVING canteens to migrate to GROUPE")
        logger.info(f"Found {canteen_groupe_qs.count()} existing GROUPE canteens")

        if apply:
            # Step 1: migrate CENTRAL to GROUPE
            for canteen_central in canteen_central_qs:
                # Before: copy data to allow updating satellites after updating the central to groupe
                canteen_central_dict_copy = canteen_central.__dict__.copy()
                # Step 1.1: update canteen fields
                for field_name, value in canteen_central_to_groupe(canteen_central).items():
                    setattr(canteen_central, field_name, value)
                canteen_central.save(run_validations=False)
                update_change_reason(canteen_central, "Script: canteen_migrate_central_to_groupe")
                # Step 1.2: update canteen satellites
                canteen_central_satellites_qs = Canteen.all_objects.filter(
                    production_type__in=[Canteen.ProductionType.ON_SITE_CENTRAL],
                    central_producer_siret=canteen_central_dict_copy["siret"],
                )
                for satellite in canteen_central_satellites_qs:
                    satellite.groupe = canteen_central
                    satellite.save(run_validations=False)
                    update_change_reason(satellite, "Script: canteen_migrate_central_to_groupe")

            # Step 2: migrate CENTRAL_SERVING to GROUPE
            for canteen_central_serving in canteen_central_serving_qs:
                # Before: copy data to allow creating & updating satellites after updating the central_serving to groupe
                canteen_central_serving_dict_copy = canteen_central_serving.__dict__.copy()
                # Step 2.1: update canteen fields
                for field_name, value in canteen_central_to_groupe(canteen_central_serving).items():
                    setattr(canteen_central_serving, field_name, value)
                canteen_central_serving.save(run_validations=False)
                update_change_reason(canteen_central_serving, "Script: canteen_migrate_central_to_groupe")
                # Step 2.2: create new satellite from central_serving
                satellite_canteen = Canteen(**satellite_from_central_dict(canteen_central_serving_dict_copy))
                satellite_canteen.save(run_validations=False)
                update_change_reason(satellite_canteen, "Script: canteen_migrate_central_to_groupe")
                satellite_canteen.managers.set(canteen_central_serving.managers.all())
                # Step 2.3: update canteen satellites
                canteen_central_serving_satellites_qs = Canteen.all_objects.filter(
                    production_type__in=[Canteen.ProductionType.ON_SITE_CENTRAL],
                    central_producer_siret=canteen_central_serving_dict_copy["siret"],
                )
                for satellite in canteen_central_serving_satellites_qs:
                    satellite.groupe = canteen_central_serving
                    satellite.save(run_validations=False)
                    update_change_reason(satellite, "Script: canteen_migrate_central_to_groupe")

        # stats after
        canteen_central_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.CENTRAL)
        canteen_central_serving_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        canteen_groupe_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.GROUPE)
        logger.info(f"Found {canteen_central_qs.count()} CENTRAL canteens to migrate to GROUPE")
        logger.info(f"Found {canteen_central_serving_qs.count()} CENTRAL_SERVING canteens to migrate to GROUPE")
        logger.info(f"Found {canteen_groupe_qs.count()} existing GROUPE canteens")
        print(Counter(Canteen.all_objects.exclude(groupe=None).values_list("production_type", flat=True)))
