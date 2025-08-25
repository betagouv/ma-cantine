import logging

from django.core.management.base import BaseCommand

from data.models import Canteen, Diagnostic
from macantine.utils import distribute_appro_values_between_satellites

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate diagnostics of CSAT by splitting diagnostics of central kitchens"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            dest="year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )

    def handle(self, *args, **options):
        year = options["year"] | 2024
        logger.info("Start task: generate diagnostics for satellite canteens using central kitchen's diagnostics")

        # Fetch all valid diagnostics for CC
        diagnostics_cc = Diagnostic.objects.teledeclared_for_year(year=year).filter(
            canteen_snapshot__production_type__in=[
                Canteen.ProductionType.CENTRAL,
                Canteen.ProductionType.CENTRAL_SERVING,
            ]
        )

        # Loop on the diagnostics of the central kitchens
        for diag in diagnostics_cc:
            if diag.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE:
                fields = Diagnostic.SIMPLE_APPRO_FIELDS
            else:
                fields = Diagnostic.COMPLETE_APPRO_FIELDS

            satellites = diag.satellites_snapshot
            updated_appro_fields = {}
            if diag.canteen_snapshot["production_type"] == Canteen.ProductionType.CENTRAL:
                updated_appro_fields = distribute_appro_values_between_satellites(diag, fields, len(satellites))
            elif diag.canteen_snapshot["production_type"] == Canteen.ProductionType.CENTRAL_SERVING:
                updated_appro_fields = distribute_appro_values_between_satellites(diag, fields, len(satellites) + 1)
                cc_asof_date_extraction = Canteen.history.as_of(diag.creation_date).get(pk=diag.canteen_snapshot["id"])
                create_new_diag_from_cc(diag, cc_asof_date_extraction, fields, updated_appro_fields)
            else:
                logger.error(
                    f"Task fail: Shoud only loop over central kitchen diagnostics. Detected a production type : {diag.canteen_snapshot["production_type"]}"
                )
                return

            if not len(satellites) > 0:
                logger.error("Task fail: A central kitchen has 0 satellites. Cannot update the appro fields")
                return

            for satellite in satellites:
                satellite_asof_date_extraction = Canteen.history.as_of(diag.creation_date).get(pk=satellite["id"])
                create_new_diag_from_cc(diag, satellite_asof_date_extraction, fields, updated_appro_fields)
                archive_satellite_diag(satellite_asof_date_extraction, year)

        # Done!
        logger.info("Task completed")


def create_new_diag_from_cc(diag, canteen_asof_date_extraction, fields, updated_appro_fields, central_serving=False):
    new_diag = diag
    new_diag.pk = None

    if not central_serving:
        new_diag.canteen = canteen_asof_date_extraction

    new_diag.creation_source = "Generated from CC diag"
    new_diag.generated_from_central_kitchen_diagnostic = True

    for field in fields:
        setattr(new_diag, field, updated_appro_fields[field])

    new_diag.save()
    logger.info(f"Task: Diag for canteen : {canteen_asof_date_extraction.name} has been saved")


def archive_satellite_diag(satellite_asof_date_extraction, year):
    diag_to_archive = Diagnostic.objects.filter(
        canteen__id=satellite_asof_date_extraction.id, year=year, generated_from_central_kitchen_diagnostic=False
    ).first()
    if diag_to_archive:
        diag_to_archive.status = Diagnostic.DiagnosticStatus.OVERRIDEN_BY_CC
        diag_to_archive.save()
        logger.info(f"Task: A diag of the satellite : {satellite_asof_date_extraction.name} has been archived")
