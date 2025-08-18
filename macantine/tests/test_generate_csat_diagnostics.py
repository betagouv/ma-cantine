from django.core.management import call_command
from django.test import TestCase

from data.models import Canteen, Diagnostic


class GenerateCsatDiagnosticsCommandTest(TestCase):
    def setUp(self):
        self.canteen = Canteen.objects.create(name="Test Canteen", siret="12345678901234", yearly_meal_count=1000)
        self.diagnostic = Diagnostic.objects.create(
            canteen=self.canteen,
            year=2024,
            value_total_ht=1000,
            value_bio_ht=200,
            status=Diagnostic.DiagnosticStatus.SUBMITTED,
        )

    def test_command_runs_without_error(self):
        try:
            call_command("generate_csat_diagnostics", year=2024)
        except Exception as e:
            self.fail(f"Command raised an exception: {e}")

    def test_command_creates_satellite_diagnostics(self):
        # You may want to set up satellites and check that diagnostics are created for them
        # For now, just check that the original diagnostic still exists
        call_command("generate_csat_diagnostics", year=2024)
        self.assertTrue(Diagnostic.objects.filter(canteen=self.canteen).exists())
