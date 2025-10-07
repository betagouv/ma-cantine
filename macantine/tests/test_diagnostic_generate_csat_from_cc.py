from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.factories import UserFactory
from data.models import Canteen, Diagnostic


class DiagnosticGenerateCsatFromCCCommandTest(TestCase):
    def setUp(self):
        # Create a central kitchen
        self.central_kitchen = Canteen.objects.create(
            id=1,
            name="Central Kitchen",
            siret="11111111111111",
            yearly_meal_count=1000,
            production_type=Canteen.ProductionType.CENTRAL,
        )
        # Create a central serving kitchen
        self.central_serving_kitchen = Canteen.objects.create(
            id=2,
            name="Central Serving Kitchen",
            siret="11111111111110",
            yearly_meal_count=100,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
        )
        # Create two satellites
        self.satellite_1 = Canteen.objects.create(
            id=11,
            name="Satellite 1",
            siret="22222222222222",
            yearly_meal_count=500,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=self.central_kitchen.siret,
        )
        self.satellite_2 = Canteen.objects.create(
            id=12,
            name="Satellite 2",
            siret="33333333333333",
            yearly_meal_count=500,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=self.central_kitchen.siret,
        )
        # Create 2 regular kitchens to check they remain intact
        self.kitchen_1 = Canteen.objects.create(
            name="Kitchen",
            siret="444444444444444",
            yearly_meal_count=1000,
            production_type=Canteen.ProductionType.ON_SITE,
        )
        self.kitchen_2 = Canteen.objects.create(
            name="Kitchen 2",
            siret="444444444444445",
            yearly_meal_count=1000,
            production_type=Canteen.ProductionType.ON_SITE,
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            # Create a diagnostic for the central kitchen
            self.diagnostic_central_kitchen = Diagnostic.objects.create(
                canteen=self.central_kitchen,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=2024,
                value_total_ht=1000,
                value_bio_ht=200,
            )
            self.diagnostic_central_kitchen.teledeclare(applicant=UserFactory())
            # Create a diagnostic for the central serving kitchen
            self.diagnostic_central_serving_kitchen = Diagnostic.objects.create(
                canteen=self.central_serving_kitchen,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=2024,
                value_total_ht=1000,
                value_bio_ht=200,
            )
            self.diagnostic_central_serving_kitchen.teledeclare(applicant=UserFactory())
            # Create a diagnostic for the satellite_1
            self.diagnostic_satellite_1 = Diagnostic.objects.create(
                canteen=self.satellite_1,
                year=2024,
                value_total_ht=100,
                value_bio_ht=20,
            )
            self.diagnostic_satellite_1.teledeclare(applicant=UserFactory())
            # Create a diagnostic for the on site canteen
            self.diagnostic_on_site_kitchen_1 = Diagnostic.objects.create(
                canteen=self.kitchen_1,
                year=2024,
                value_total_ht=100,
                value_bio_ht=20,
            )
            self.diagnostic_on_site_kitchen_1.teledeclare(applicant=UserFactory())
            # Create a diagnostic for the on site canteen 2 (don't teledeclare it)
            self.diagnostic_on_site_kitchen_2 = Diagnostic.objects.create(
                canteen=self.kitchen_2,
                year=2024,
                value_total_ht=100,
                value_bio_ht=20,
            )

    def test_command_generates_diagnostics_for_satellites(self):
        self.assertEqual(Canteen.objects.count(), 6)
        self.assertEqual(Diagnostic.objects.count(), 5)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 5)
        self.assertEqual(Diagnostic.objects.in_year(2024).filter(status=Diagnostic.DiagnosticStatus.DRAFT).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 4)
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(generated_from_central_kitchen_diagnostic=False)
            .count(),
            4,
        )

        # Run the command
        call_command("diagnostic_generate_csat_from_cc", year=2024, apply=True)
        # There should be 3 new diagnostics: 2 for the satellites, 1 for the central serving kitchen
        self.assertEqual(Diagnostic.objects.in_year(2024).filter(status=Diagnostic.DiagnosticStatus.DRAFT).count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).filter(status=Diagnostic.DiagnosticStatus.OVERRIDEN_BY_CC).count(), 1
        )
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 4 - 1 + 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(generated_from_central_kitchen_diagnostic=True)
            .count(),
            3,
        )

    def test_command_creates_satellite_diagnostics_with_split_appro(self):
        call_command("diagnostic_generate_csat_from_cc", year=2024, apply=True)
        # There should be a new diagnostic for each satellite
        diag_sat1 = Diagnostic.objects.teledeclared().get(
            canteen=self.satellite_1, year=2024, generated_from_central_kitchen_diagnostic=True
        )
        diag_sat2 = Diagnostic.objects.teledeclared().get(
            canteen=self.satellite_2, year=2024, generated_from_central_kitchen_diagnostic=True
        )
        # The satellite canteen data should be set
        # The appro values should be split equally (1000/2, 200/2)
        self.assertEqual(diag_sat1.canteen.name, "Satellite 1")
        self.assertEqual(diag_sat1.value_total_ht, 500)
        self.assertEqual(diag_sat1.value_bio_ht, 100)
        self.assertEqual(diag_sat2.canteen.name, "Satellite 2")
        self.assertEqual(diag_sat2.value_total_ht, 500)
        self.assertEqual(diag_sat2.value_bio_ht, 100)

    def test_command_does_not_remove_original_cc_diag(self):
        call_command("diagnostic_generate_csat_from_cc", year=2024, apply=True)
        self.assertTrue(Diagnostic.objects.filter(canteen=self.central_kitchen, year=2024).exists())

    def test_command_does_not_edit_on_site_kitchen_diag(self):
        call_command("diagnostic_generate_csat_from_cc", year=2024, apply=True)
        self.assertTrue(Diagnostic.objects.filter(canteen=self.kitchen_1, year=2024).exists())

    def test_command_create_a_central_serving_diag(self):
        call_command("diagnostic_generate_csat_from_cc", year=2024, apply=True)
        self.assertTrue(
            Diagnostic.objects.filter(
                canteen=self.central_serving_kitchen, year=2024, generated_from_central_kitchen_diagnostic=True
            ).exists()
        )
        self.assertTrue(
            Diagnostic.objects.filter(
                canteen=self.central_serving_kitchen, year=2024, generated_from_central_kitchen_diagnostic=False
            ).exists()
        )
