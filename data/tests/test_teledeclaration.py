from unittest.mock import patch

from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.timezone import now
from freezegun import freeze_time

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Diagnostic, Teledeclaration

year_data = now().year - 1
mocked_campaign_dates = {
    year_data: {
        "teledeclaration_start_date": now().replace(month=1, day=1, hour=0, minute=0, second=0),
        "teledeclaration_end_date": now().replace(month=4, day=30, hour=23, minute=59, second=59),
        "correction_start_date": now().replace(month=6, day=1, hour=0, minute=0, second=0),
        "correction_end_date": now().replace(month=8, day=31, hour=23, minute=59, second=59),
    }
}


class TeledeclarationQuerySetTest(TestCase):
    def setUp(self):
        """
        Set up mock data for testing.
        The date is frozen to an old date to allow creating teledeclarations with correct dates
        (using fake time directly corrupts the QuerySet Date Range filter).
        """
        self._create_canteens()
        self._create_diagnostics_and_teledeclarations()

    def _create_canteens(self):
        """Create canteens for testing."""
        self.valid_canteen_1 = CanteenFactory(siret="12345678901234", deletion_date=None)
        self.valid_canteen_2 = CanteenFactory(siren_unite_legale="123456789", deletion_date=None)
        self.valid_canteen_3 = CanteenFactory(
            siret="12345678901235", siren_unite_legale="123456789", deletion_date=None
        )
        self.valid_canteen_4 = CanteenFactory(siret="12345678901230", deletion_date=None)
        self.invalid_canteen = CanteenFactory(siret="", deletion_date=None)  # siret missing
        self.deleted_canteen = CanteenFactory(
            siret="56789012345678",
            deletion_date=now().replace(month=3, day=1),
        )

    def _create_diagnostics_and_teledeclarations(self):
        """Create diagnostics and teledeclarations for testing."""
        for index, canteen in enumerate([self.valid_canteen_1, self.valid_canteen_2, self.valid_canteen_3]):
            diagnostic = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
                creation_date=now().replace(month=3, day=1),
                canteen=canteen,
                value_total_ht=1000.00,
                value_bio_ht=200.00,
            )
            setattr(self, f"valid_canteen_diagnostic_{index + 1}", diagnostic)
            teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, applicant=UserFactory.create())
            setattr(self, f"valid_canteen_td_{index + 1}", teledeclaration)

        # Corrected TD
        self.valid_canteen_diagnostic_correction = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=now().replace(month=7, day=1),
            canteen=self.valid_canteen_4,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        user_correction_campaign = UserFactory.create()
        self.valid_correction_td = Teledeclaration.create_from_diagnostic(
            self.valid_canteen_diagnostic_correction, applicant=user_correction_campaign
        )
        self.valid_correction_td.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        self.valid_correction_td.save()

        with freeze_time(now().replace(month=7, day=1, hour=0, minute=0, second=0)):
            self.valid_correction_td = Teledeclaration.create_from_diagnostic(
                self.valid_canteen_diagnostic_correction, applicant=user_correction_campaign
            )

        self.invalid_canteen_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.invalid_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        self.invalid_canteen_td = Teledeclaration.create_from_diagnostic(
            self.invalid_canteen_diagnostic, applicant=UserFactory.create()
        )

        self.deleted_canteen_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.deleted_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        self.deleted_canteen_td = Teledeclaration.create_from_diagnostic(
            self.deleted_canteen_diagnostic, applicant=UserFactory.create()
        )

    def test_submitted_for_year(self):
        with patch("data.models.teledeclaration.CAMPAIGN_DATES", mocked_campaign_dates):
            teledeclarations = Teledeclaration.objects.submitted_for_year(year_data)
        self.assertEqual(teledeclarations.count(), 6)
        self.assertIn(self.valid_canteen_td_1, teledeclarations)
        self.assertIn(self.invalid_canteen_td, teledeclarations)
        self.assertIn(self.deleted_canteen_td, teledeclarations)

    def test_for_stat(self):
        with patch("data.models.teledeclaration.CAMPAIGN_DATES", mocked_campaign_dates):
            teledeclarations = Teledeclaration.objects.for_stat(year_data)
        self.assertEqual(teledeclarations.count(), 4)
        self.assertIn(self.valid_canteen_td_1, teledeclarations)
        self.assertNotIn(self.invalid_canteen_td, teledeclarations)  # canteen without siret
        self.assertNotIn(self.deleted_canteen_td, teledeclarations)  # canteen deleted


class TestTeledeclarationModelConstraintsTest(TestCase):
    @authenticate
    def test_diagnostic_deletion(self):
        """
        If the diagnostic used for the teledeclaration is deleted, the teledeclaration
        should be cancelled
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        diagnostic.delete()
        teledeclaration.refresh_from_db()
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED)
        self.assertIsNone(teledeclaration.diagnostic)

    def test_one_submitted_td_constraint(self):
        """
        Only one TD per canteen and per year can be submitted
        """
        # Doesn't use the TeledeclarationFactory to escape the `clean` function validation
        # bulk_create does not pass through the `save` method, so it allows us to test the
        # actual constraint.
        canteen = CanteenFactory.create()
        diagnostic = DiagnosticFactory.create(canteen=canteen)
        applicant = UserFactory.create()
        teledeclaration_1 = Teledeclaration(
            canteen=canteen,
            year=year_data,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        teledeclaration_2 = Teledeclaration(
            canteen=canteen,
            year=year_data,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        with self.assertRaises(IntegrityError):
            Teledeclaration.objects.bulk_create([teledeclaration_1, teledeclaration_2])

    def test_several_cancelled_td_constraint(self):
        """
        Cancelled TDs should not influence the constraint
        """
        # Doesn't use the TeledeclarationFactory to escape the `clean` function validation
        # bulk_create does not pass through the `save` method, so it allows us to test the
        # actual constraint.
        canteen = CanteenFactory.create()
        diagnostic = DiagnosticFactory.create(canteen=canteen)
        applicant = UserFactory.create()
        teledeclaration_1 = Teledeclaration(
            canteen=canteen,
            year=year_data,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
            declared_data={"foo": 1},
        )
        teledeclaration_2 = Teledeclaration(
            canteen=canteen,
            year=year_data,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        try:
            Teledeclaration.objects.bulk_create([teledeclaration_1, teledeclaration_2])
        except IntegrityError:
            self.fail("Should be able to create a submitted TD if a cancelled one exists already")

    def test_bypass_constraint_if_no_canteen(self):
        """
        A TD that does not have a canteen attached to it (e.g., for deleted canteens) should not be
        considered in the constraint.
        """
        # Doesn't use the TeledeclarationFactory to escape the `clean` function validation
        # bulk_create does not pass through the `save` method, so it allows us to test the
        # actual constraint.
        applicant = UserFactory.create()
        teledeclaration_1 = Teledeclaration(
            canteen=None,
            year=year_data,
            diagnostic=None,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        teledeclaration_2 = Teledeclaration(
            canteen=None,
            year=year_data,
            diagnostic=None,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        try:
            Teledeclaration.objects.bulk_create([teledeclaration_1, teledeclaration_2])
        except IntegrityError:
            self.fail("Should be able to have several submitted TDs for deleted canteens")
