from django.core.management import call_command
from django.test import TestCase

from data.models import Canteen, Diagnostic


class GenerateCsatDiagnosticsCommandTest(TestCase):
    def setUp(self):
        # Create a central kitchen
        self.central_kitchen = Canteen.objects.create(
            id=1,
            name="Central Kitchen",
            siret="11111111111111",
            yearly_meal_count=1000,
            production_type=Canteen.ProductionType.CENTRAL,
        )
        # Create two satellites
        self.satellite1 = Canteen.objects.create(
            id=2,
            name="Satellite 1",
            siret="22222222222222",
            yearly_meal_count=500,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=self.central_kitchen.siret,
        )
        self.satellite2 = Canteen.objects.create(
            id=3,
            name="Satellite 2",
            siret="33333333333333",
            yearly_meal_count=500,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=self.central_kitchen.siret,
        )
        # Create a regular kitchen to check it remains intact
        self.kitchen = Canteen.objects.create(
            name="Kitchen",
            siret="444444444444444",
            yearly_meal_count=1000,
            production_type=Canteen.ProductionType.ON_SITE,
        )
        # Create a diagnostic for the central kitchen
        self.cc_diag = Diagnostic.objects.create(
            canteen=self.central_kitchen,
            canteen_snapshot={"production_type": Canteen.ProductionType.CENTRAL},
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            value_total_ht=1000,
            value_bio_ht=200,
            status=Diagnostic.DiagnosticStatus.SUBMITTED,
            teledeclaration_date="2025-01-15",
            generated_from_central_kitchen_diagnostic=False,
            satellites_snapshot=[{"id": 2, "name": "Satellite 1"}, {"id": 3, "name": "Satellite 2"}],
        )
        # Create a diagnostic for the sat 1
        self.cc_diag = Diagnostic.objects.create(
            canteen=self.satellite1,
            canteen_snapshot={"production_type": Canteen.ProductionType.ON_SITE_CENTRAL},
            year=2024,
            value_total_ht=100,
            value_bio_ht=20,
            status=Diagnostic.DiagnosticStatus.SUBMITTED,
            teledeclaration_date="2025-01-15",
            creation_source="Sat",
            generated_from_central_kitchen_diagnostic=False,
        )
        # Create a diagnostic for the kitchen
        self.cc_diag = Diagnostic.objects.create(
            canteen=self.kitchen,
            canteen_snapshot={"production_type": Canteen.ProductionType.ON_SITE_CENTRAL},
            year=2024,
            value_total_ht=100,
            value_bio_ht=20,
            status=Diagnostic.DiagnosticStatus.SUBMITTED,
            teledeclaration_date="2025-01-15",
            generated_from_central_kitchen_diagnostic=False,
        )

    def test_command_creates_satellite_diagnostics_with_split_appro(self):
        call_command("generate_csat_diagnostics", year=2024)
        # There should be a diagnostic for each satellite
        sat1_diag = Diagnostic.objects.filter(
            canteen=self.satellite1, year=2024, status=Diagnostic.DiagnosticStatus.SUBMITTED
        ).first()
        sat2_diag = Diagnostic.objects.filter(
            canteen=self.satellite2, year=2024, status=Diagnostic.DiagnosticStatus.SUBMITTED
        ).first()
        self.assertIsNotNone(sat1_diag)
        self.assertIsNotNone(sat2_diag)
        # The appro values should be split equally (1000/2, 200/2)
        self.assertEqual(sat1_diag.value_total_ht, 500)
        self.assertEqual(sat2_diag.value_total_ht, 500)
        self.assertEqual(sat1_diag.value_bio_ht, 100)
        self.assertEqual(sat2_diag.value_bio_ht, 100)
        # The satellite canteen data should be set
        self.assertEqual(sat1_diag.canteen.name, "Satellite 1")
        self.assertEqual(sat2_diag.canteen.name, "Satellite 2")

    def test_command_runs_without_error(self):
        try:
            call_command("generate_csat_diagnostics", year=2024)
        except Exception as e:
            self.fail(f"Command raised an exception: {e}")

    def test_command_does_not_remove_original_cc_diag(self):
        call_command("generate_csat_diagnostics", year=2024)
        self.assertTrue(Diagnostic.objects.filter(canteen=self.central_kitchen, year=2024).exists())

    def test_command_does_not_edit_on_site_kitchen(self):
        call_command("generate_csat_diagnostics", year=2024)
        self.assertTrue(Diagnostic.objects.filter(canteen=self.kitchen, year=2024).exists())
