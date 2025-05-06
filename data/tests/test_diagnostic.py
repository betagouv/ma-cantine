from django.test import TestCase
from django.utils.timezone import now

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Diagnostic, Teledeclaration

year_data = now().year - 1
mocked_campaign_dates = {
    year_data: {
        "teledeclaration_start_date": now().replace(month=1, day=1, hour=0, minute=0, second=0),
        "teledeclaration_end_date": now().replace(month=12, day=31, hour=23, minute=59, second=59),
    }
}


class DiagnosticQuerySetTest(TestCase):
    def setUp(self):
        """
        Set up mock data for testing.
        The date is freezed to an old date in order to have freedom to create teledeclaration with correct date
        (using fake time direclty corrupts the QuerySet Date Range filter)
        """

        # Create canteens and diagnostics
        self.valid_canteen_1 = CanteenFactory(siret="12345678901234", deletion_date=None)
        self.valid_canteen_2 = CanteenFactory(siren_unite_legale="123456789", deletion_date=None)
        self.valid_canteen_3 = CanteenFactory(
            siret="12345678901235", siren_unite_legale="123456789", deletion_date=None
        )
        self.invalid_canteen = CanteenFactory(siret="", deletion_date=None)  # siret missing
        self.deleted_canteen = CanteenFactory(
            siret="56789012345678",
            deletion_date=now().replace(month=6, day=1),
        )

        for index, canteen in enumerate([self.valid_canteen_1, self.valid_canteen_2, self.valid_canteen_3]):
            setattr(
                self,
                f"valid_canteen_diagnostic_{index + 1}",
                DiagnosticFactory(
                    year=year_data,
                    creation_date=now().replace(month=3, day=1),
                    canteen=canteen,
                    value_total_ht=1000.00,
                    value_bio_ht=200.00,
                ),
            )
            Teledeclaration.create_from_diagnostic(
                getattr(self, f"valid_canteen_diagnostic_{index + 1}"), applicant=UserFactory.create()
            )

        self.invalid_canteen_diagnostic = DiagnosticFactory(
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.invalid_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        Teledeclaration.create_from_diagnostic(self.invalid_canteen_diagnostic, applicant=UserFactory.create())

        self.deleted_canteen_diagnostic = DiagnosticFactory(
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.deleted_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        Teledeclaration.create_from_diagnostic(self.deleted_canteen_diagnostic, applicant=UserFactory.create())

    def test_is_filled(self):
        valid_canteen_empty_diagnostic = Diagnostic.objects.create(
            year=year_data - 1, canteen=self.valid_canteen_1, value_total_ht=None
        )
        self.assertEqual(Diagnostic.objects.count(), 5 + 1)
        diagnostics = Diagnostic.objects.is_filled()
        self.assertEqual(diagnostics.count(), 5)
        self.assertIn(self.valid_canteen_diagnostic_1, diagnostics)
        self.assertNotIn(valid_canteen_empty_diagnostic, diagnostics)


class DiagnosticQuerySetAndPropertyTest(TestCase):

    def setUp(self):
        self.empty_total_diagnostic = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=None)
        self.filled_total_diagnostic = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=1000)

    def test_is_filled_queryset(self):
        all_diagnostics = Diagnostic.objects.all()
        diagnostics_filled = Diagnostic.objects.is_filled()
        self.assertEqual(all_diagnostics.count(), 2)
        self.assertEqual(diagnostics_filled.count(), 1)

    def test_is_filled_property(self):
        self.assertFalse(self.empty_total_diagnostic.is_filled)
        self.assertTrue(self.filled_total_diagnostic.is_filled)
