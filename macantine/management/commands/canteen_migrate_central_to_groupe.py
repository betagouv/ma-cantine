import logging
from collections import Counter

from django.core.management.base import BaseCommand
from simple_history.utils import update_change_reason

from data.models import Canteen
from api.serializers import SatelliteTeledeclarationSerializer

logger = logging.getLogger(__name__)


def canteen_central_to_groupe(canteen_central):
    return {
        "production_type": Canteen.ProductionType.GROUPE,
        "siret": None,
        "siren_unite_legale": canteen_central.siret[:9] if canteen_central.siret else None,
        "city": None,
        "city_insee_code": None,
        "postal_code": None,
        "epci": None,
        "epci_lib": None,
        "pat_list": [],
        "pat_lib_list": [],
        "department": None,
        "department_lib": None,
        "region": None,
        "region_lib": None,
        "economic_model": None,
        "satellite_canteens_count": None,
        "sector_list": [],
        "line_ministry": None,
    }


def satellite_from_central_dict(canteen_central_dict):
    return {
        "name": canteen_central_dict["name"] + " - Satellite",
        "siret": canteen_central_dict["siret"],
        "siren_unite_legale": canteen_central_dict["siren_unite_legale"],
        "city": canteen_central_dict["city"],
        "city_insee_code": canteen_central_dict["city_insee_code"],
        "postal_code": canteen_central_dict["postal_code"],
        "epci": canteen_central_dict["epci"],
        "epci_lib": canteen_central_dict["epci_lib"],
        "pat_list": canteen_central_dict["pat_list"],
        "pat_lib_list": canteen_central_dict["pat_lib_list"],
        "department": canteen_central_dict["department"],
        "department_lib": canteen_central_dict["department_lib"],
        "region": canteen_central_dict["region"],
        "region_lib": canteen_central_dict["region_lib"],
        "management_type": canteen_central_dict["management_type"],
        "production_type": Canteen.ProductionType.ON_SITE_CENTRAL,
        "economic_model": canteen_central_dict["economic_model"],
        "daily_meal_count": canteen_central_dict["daily_meal_count"],
        "yearly_meal_count": canteen_central_dict["yearly_meal_count"],
        "groupe_id": canteen_central_dict["id"],
        # "central_producer_siret": canteen_central_dict["siret"],  # would make an error because same as 'siret'
        "sector_list": canteen_central_dict["sector_list"],
        "line_ministry": canteen_central_dict["line_ministry"],
        "deletion_date": canteen_central_dict["deletion_date"] if canteen_central_dict["deletion_date"] else None,
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
        canteen_central_all_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.CENTRAL)
        canteen_central_serving_all_qs = Canteen.all_objects.filter(
            production_type=Canteen.ProductionType.CENTRAL_SERVING
        )
        canteen_groupe_all_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.GROUPE)
        logger.info(f"Found {canteen_central_all_qs.count()} CENTRAL canteens to migrate to GROUPE")
        logger.info(f"Found {canteen_central_serving_all_qs.count()} CENTRAL_SERVING canteens to migrate to GROUPE")
        logger.info(f"Found {canteen_groupe_all_qs.count()} existing GROUPE canteens")

        if apply:
            # Step 1: migrate CENTRAL to GROUPE
            for canteen_central in canteen_central_all_qs:
                # Before: copy data to allow updating satellites after updating the central to groupe
                canteen_central_dict_copy = canteen_central.__dict__.copy()
                # Step 1.1: update canteen fields
                for field_name, value in canteen_central_to_groupe(canteen_central).items():
                    setattr(canteen_central, field_name, value)
                canteen_central.save(skip_validations=True)
                update_change_reason(canteen_central, "Script: canteen_migrate_central_to_groupe")
                # Step 1.2: link canteen satellites (only if central not deleted)
                if not canteen_central.is_deleted:
                    canteen_central_satellites_all_qs = Canteen.all_objects.filter(
                        production_type__in=[Canteen.ProductionType.ON_SITE_CENTRAL],
                        central_producer_siret=canteen_central_dict_copy["siret"],
                    )
                    for satellite in canteen_central_satellites_all_qs:
                        satellite.groupe = canteen_central
                        satellite.save(skip_validations=True)
                        update_change_reason(satellite, "Script: canteen_migrate_central_to_groupe")

            # Step 2: migrate CENTRAL_SERVING to GROUPE
            for canteen_central_serving in canteen_central_serving_all_qs:
                # Before: copy data to allow creating & updating satellites after updating the central_serving to groupe
                canteen_central_serving_dict_copy = canteen_central_serving.__dict__.copy()
                # Step 2.1: update canteen fields
                for field_name, value in canteen_central_to_groupe(canteen_central_serving).items():
                    setattr(canteen_central_serving, field_name, value)
                canteen_central_serving.save(skip_validations=True)
                update_change_reason(canteen_central_serving, "Script: canteen_migrate_central_to_groupe")
                # Step 2.2: create (and link) new satellite from central_serving
                new_satellite = Canteen(**satellite_from_central_dict(canteen_central_serving_dict_copy))
                new_satellite.save(skip_validations=True)
                update_change_reason(new_satellite, "Script: canteen_migrate_central_to_groupe")
                new_satellite.managers.set(canteen_central_serving.managers.all())
                # Step 2.3: if central_serving has diagnostics teledeclared, update the satellites_snapshot with the new_satellite
                for diagnostic_teledeclared in canteen_central_serving.diagnostics.teledeclared():
                    diagnostic_teledeclared_satellites_snapshot = diagnostic_teledeclared.satellites_snapshot or []
                    diagnostic_teledeclared_satellites_snapshot.append(
                        SatelliteTeledeclarationSerializer(new_satellite).data
                    )
                    diagnostic_teledeclared.satellites_snapshot = diagnostic_teledeclared_satellites_snapshot
                    diagnostic_teledeclared.save()
                    update_change_reason(
                        diagnostic_teledeclared,
                        "Script: canteen_migrate_central_to_groupe - added new satellite to satellites_snapshot",
                    )
                # Step 2.4: link canteen satellites (if central_serving not deleted)
                if not canteen_central_serving.is_deleted:
                    canteen_central_serving_satellites_all_qs = Canteen.all_objects.filter(
                        production_type__in=[Canteen.ProductionType.ON_SITE_CENTRAL],
                        central_producer_siret=canteen_central_serving_dict_copy["siret"],
                    )
                    for satellite in canteen_central_serving_satellites_all_qs:
                        satellite.groupe = canteen_central_serving
                        satellite.save(skip_validations=True)
                        update_change_reason(satellite, "Script: canteen_migrate_central_to_groupe")

            # stats after
            canteen_central_all_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.CENTRAL)
            canteen_central_serving_all_qs = Canteen.all_objects.filter(
                production_type=Canteen.ProductionType.CENTRAL_SERVING
            )
            canteen_groupe_all_qs = Canteen.all_objects.filter(production_type=Canteen.ProductionType.GROUPE)
            logger.info(f"Found {canteen_central_all_qs.count()} CENTRAL canteens to migrate to GROUPE")
            logger.info(
                f"Found {canteen_central_serving_all_qs.count()} CENTRAL_SERVING canteens to migrate to GROUPE"
            )
            logger.info(f"Found {canteen_groupe_all_qs.count()} existing GROUPE canteens")
            print(Counter(Canteen.all_objects.exclude(groupe=None).values_list("production_type", flat=True)))
