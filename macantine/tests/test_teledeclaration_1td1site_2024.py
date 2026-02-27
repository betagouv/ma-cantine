from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.models import Canteen, Diagnostic
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class Teledeclaration1Td1SiteCanteenNotConcerned(TestCase):
    @authenticate
    def test_for_canteen_site(self):
        """
        Test that the diagnostics of the canteen sites are generated when the command is run.
        """
        site_1 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        site_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_site_1 = DiagnosticFactory(
                canteen=site_1,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            diagnostic_site_2 = DiagnosticFactory(
                canteen=site_2,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            )
            diagnostic_site_1.teledeclare(applicant=authenticate.user)
            diagnostic_site_2.teledeclare(applicant=authenticate.user)

        site_1_snapshot_canteen_before_script = diagnostic_site_1.canteen_snapshot
        site_1_snapshot_satellites_before_script = diagnostic_site_1.satellites_snapshot
        site_2_snapshot_canteen_before_script = diagnostic_site_2.canteen_snapshot
        site_2_snapshot_satellites_before_script = diagnostic_site_2.satellites_snapshot

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(diagnostic_site_1.canteen_snapshot, site_1_snapshot_canteen_before_script)
        self.assertEqual(diagnostic_site_1.satellites_snapshot, site_1_snapshot_satellites_before_script)
        self.assertEqual(diagnostic_site_2.canteen_snapshot, site_2_snapshot_canteen_before_script)
        self.assertEqual(diagnostic_site_2.satellites_snapshot, site_2_snapshot_satellites_before_script)

    @authenticate
    def test_for_satellite_with_central_siret_unknown(self):
        """
        Test that a satellite canteen with a central SIRET that doesn't match any canteen is not modified when the command is run.
        """
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="19622299600015"
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_snapshot_canteen_before_script = satellite_diagnostic.canteen_snapshot
        satellite_snapshot_satellites_before_script = satellite_diagnostic.satellites_snapshot

        # Before the script is run
        self.assertEqual(
            Canteen.objects.filter(siret="19622299600015").count(), 0
        )  # no central canteen exist with the siret used in sat
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(satellite_diagnostic.canteen_snapshot, satellite_snapshot_canteen_before_script)
        self.assertEqual(satellite_diagnostic.satellites_snapshot, satellite_snapshot_satellites_before_script)

    @authenticate
    def test_for_satellite_with_central_siret_empty(self):
        """
        Test that a satellite canteen without a central SIRET that teledeclares is not modified when the command is run.
        """
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="")
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_snapshot_canteen_before_script = satellite_diagnostic.canteen_snapshot
        satellite_snapshot_satellites_before_script = satellite_diagnostic.satellites_snapshot

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(satellite_diagnostic.canteen_snapshot, satellite_snapshot_canteen_before_script)
        self.assertEqual(satellite_diagnostic.satellites_snapshot, satellite_snapshot_satellites_before_script)


class Teledeclaration1Td1SiteCanteenCentralWithSatellitesWithoutDiagnostic(TestCase):
    @authenticate
    def test_central_teledeclare_satellites_diagnostic_are_generated(self):
        """
        Test that the diagnostics for the satellites of a central canteen are generated when the command is run.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)

        # Diagnostics are generated
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).get(canteen=satellite_1).generated_from_groupe_diagnostic, True
        )
        self.assertEqual(
            Diagnostic.objects.in_year(2024).get(canteen=satellite_2).generated_from_groupe_diagnostic, True
        )
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )
