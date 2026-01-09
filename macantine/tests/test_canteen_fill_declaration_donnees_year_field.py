from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic


class CanteenFillDeclarationDonneesYearFieldCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_with_diagnostic = CanteenFactory()
        cls.canteen_diagnostic_not_teledeclared = DiagnosticFactory(
            canteen=cls.canteen_with_diagnostic,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            valeur_totale=1000,
        )  # filled
        cls.canteen_groupe_with_diagnostic_teledeclared = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_with_groupe_diagnostic_teledeclared = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_with_diagnostic_teledeclared,
        )
        cls.canteen_groupe_diagnostic_teledeclared = DiagnosticFactory(
            canteen=cls.canteen_groupe_with_diagnostic_teledeclared,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            valeur_totale=1000,
        )  # filled
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            cls.canteen_groupe_diagnostic_teledeclared.teledeclare(applicant=UserFactory())

    def test_canteen_fill_declaration_donnees_year_field(self):
        self.assertFalse(self.canteen_with_diagnostic.declaration_donnees_2024)
        self.assertFalse(self.canteen_groupe_with_diagnostic_teledeclared.declaration_donnees_2024)
        self.assertFalse(self.canteen_satellite_with_groupe_diagnostic_teledeclared.declaration_donnees_2024)

        # run management command & refresh from db
        call_command("canteen_fill_declaration_donnees_year_field", year=2024)
        self.canteen_with_diagnostic.refresh_from_db()
        self.canteen_groupe_with_diagnostic_teledeclared.refresh_from_db()
        self.canteen_satellite_with_groupe_diagnostic_teledeclared.refresh_from_db()

        self.assertFalse(self.canteen_with_diagnostic.declaration_donnees_2024)
        self.assertTrue(self.canteen_groupe_with_diagnostic_teledeclared.declaration_donnees_2024)
        self.assertTrue(self.canteen_satellite_with_groupe_diagnostic_teledeclared.declaration_donnees_2024)

    def test_canteen_fill_declaration_donnees_year_field_for_canteen_with_deletion_date(self):
        # delete canteen
        self.canteen_satellite_with_groupe_diagnostic_teledeclared.delete()

        # run management command & refresh from db
        call_command("canteen_fill_declaration_donnees_year_field", year=2024)
        self.canteen_satellite_with_groupe_diagnostic_teledeclared.refresh_from_db()

        self.assertTrue(self.canteen_satellite_with_groupe_diagnostic_teledeclared.declaration_donnees_2024)
