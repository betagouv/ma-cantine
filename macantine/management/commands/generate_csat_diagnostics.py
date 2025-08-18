import logging

from django.core.management.base import BaseCommand

from data.models import Diagnostic

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate diagnostics of CSAT by splitting diagnostics of central kitchens"

    def handle(self, *args, **options):
        logger.info("Start task: generate diagnostics for satellite kitchens using central kitchen's diagnostics")

        # Step 1: get all valid diagnostics for CC
        diagnostics_cc = Diagnostic.objects.teledeclared_for_year.filter(
            central_kitchen_diagnostic_mode__is_null=False
        )

        # Step 2: Fetch the satellites of the diag's central kitchen
        for diag in diagnostics_cc:
            satellites = diag.canteen.satellites
            nbre_satellites = (
                len(satellites) + 1 if diag.canteen.production_type == "Canteen.ProductionType.CENTRAL_SERVING" else 0
            )

            # Step 3 : Create the satellite diag by duplicating the CC diag
            for satellite in satellites:
                sat_diag = diag.copy()
                sat_diag.pk = None
                sat_diag.canteen = satellite

                # Step 4 : Update the appro fields
                if diag.diagnostic_type == Diagnostic.DiagnosticType.SIMPLE:
                    fields = Diagnostic.SIMPLE_APPRO_FIELDS
                else:
                    fields = Diagnostic.COMPLETE_APPRO_FIELDS
                for field in fields:
                    setattr(sat_diag, field, getattr(diag, field) / nbre_satellites)

                sat_diag.save()
                logger.info(f"Task: Diag for canteen : {satellite.name} has been saved")

        # Done!
        logger.info("Task completed")
