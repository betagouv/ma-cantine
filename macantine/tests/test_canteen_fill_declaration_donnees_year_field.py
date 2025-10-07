from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, Teledeclaration


class CanteenFillDeclarationDonneesYearFieldCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_with_diagnostic_cancelled = CanteenFactory()
        cls.canteen_with_diagnostic_submitted = CanteenFactory(
            siret="75665621899905", production_type=Canteen.ProductionType.CENTRAL, satellite_canteens_count=1
        )
        cls.canteen_satellite_with_central_diagnostic_submitted = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_with_diagnostic_submitted.siret,
        )
        diagnostic_filled = DiagnosticFactory(
            canteen=cls.canteen_with_diagnostic_cancelled,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            value_total_ht=1000,
        )  # filled
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            td_to_cancel = Teledeclaration.create_from_diagnostic(diagnostic_filled, applicant=UserFactory())
            td_to_cancel.cancel()
        diagnostic_filled_and_submitted = DiagnosticFactory(
            canteen=cls.canteen_with_diagnostic_submitted,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            value_total_ht=1000,
        )  # filled & submitted
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            Teledeclaration.create_from_diagnostic(diagnostic_filled_and_submitted, applicant=UserFactory())

    def test_canteen_fill_declaration_donnees_year_field(self):
        self.assertFalse(self.canteen_with_diagnostic_cancelled.declaration_donnees_2024)
        self.assertFalse(self.canteen_with_diagnostic_submitted.declaration_donnees_2024)
        self.assertFalse(self.canteen_satellite_with_central_diagnostic_submitted.declaration_donnees_2024)
        call_command("canteen_fill_declaration_donnees_year_field", year=2024)
        self.canteen_with_diagnostic_cancelled.refresh_from_db()
        self.canteen_with_diagnostic_submitted.refresh_from_db()
        self.canteen_satellite_with_central_diagnostic_submitted.refresh_from_db()
        self.assertFalse(self.canteen_with_diagnostic_cancelled.declaration_donnees_2024)
        self.assertTrue(self.canteen_with_diagnostic_submitted.declaration_donnees_2024)
        self.assertTrue(self.canteen_satellite_with_central_diagnostic_submitted.declaration_donnees_2024)

    def test_test_canteen_fill_declaration_donnees_year_field_for_canteen_with_deletion_date(self):
        self.canteen_with_diagnostic_submitted.delete()
        call_command("canteen_fill_declaration_donnees_year_field", year=2024)
        self.canteen_with_diagnostic_submitted.refresh_from_db()
        self.assertTrue(self.canteen_with_diagnostic_submitted.declaration_donnees_2024)
