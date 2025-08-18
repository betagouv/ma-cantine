import logging

from django.core.management.base import BaseCommand

from data.models import Diagnostic

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
        logger.info("Start task: generate diagnostics for satellite kitchens using central kitchen's diagnostics")

        # Step 1: get all valid diagnostics for CC
        diagnostics_cc = Diagnostic.objects.teledeclared_for_year(year=year).filter(
            central_kitchen_diagnostic_mode__isnull=False
        )

        # Step 2: Fetch the satellites of the diag's central kitchen
        for diag in diagnostics_cc:
            satellites = diag.canteen.satellites
            nbre_satellites = (
                len(satellites) + 1
                if diag.canteen.production_type == "Canteen.ProductionType.CENTRAL_SERVING"
                else len(satellites)
            )
            if not nbre_satellites > 0:
                logger.error("Task fail: A central kitchen has 0 satellites. Cannot update the appro fields")
                return

            # Step 3 : Compute the updated appro fields
            if diag.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE:
                fields = Diagnostic.SIMPLE_APPRO_FIELDS
            else:
                fields = Diagnostic.COMPLETE_APPRO_FIELDS
            updated_appro_fields = {}
            for field in fields:
                try:
                    updated_appro_fields[field] = getattr(diag, field) / nbre_satellites
                except TypeError:
                    updated_appro_fields[field] = None

            # Step 4: Create the satellite diag by duplicating the CC diag
            for satellite in satellites:
                sat_diag = diag
                sat_diag.pk = None
                sat_diag.canteen = satellite

                # Step 5: Update the appro values
                for field in fields:
                    setattr(sat_diag, field, updated_appro_fields[field])

                sat_diag.save()
                logger.info(f"Task: Diag for canteen : {satellite.name} has been saved")

        # Done!
        logger.info("Task completed")
