from datetime import datetime

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Diagnostic


year_data = 2024
date_in_teledeclaration_campaign = "2025-03-30"
date_in_correction_campaign = "2025-04-20"
date_in_last_teledeclaration_campaign = "2024-02-01"


class DiagnosticFillInvalidWarningReasonListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_deleted = CanteenFactory(
            siret="21730065600014",
            deletion_date=timezone.make_aware(
                datetime.strptime(date_in_teledeclaration_campaign, "%Y-%m-%d")
            ),  # soft deleted
        )
        cls.diagnostic_canteen_deleted = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_deleted,
            valeur_totale=1000.00,
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):  # during the 2024 campaign
            cls.diagnostic_canteen_deleted.teledeclare(applicant=UserFactory())

    def test_command_should_not_add_if_other_year(self):
        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIsNone(self.diagnostic_canteen_deleted.invalid_reason_list)

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2025, apply=True)

        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIsNone(self.diagnostic_canteen_deleted.invalid_reason_list)

    def test_command_should_not_remove_if_other_year(self):
        Diagnostic.objects.filter(id=self.diagnostic_canteen_deleted.id).update(
            invalid_reason_list=[Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE]
        )
        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIn(
            Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE,
            self.diagnostic_canteen_deleted.invalid_reason_list,
        )

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2025, apply=True)

        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIn(
            Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE,
            self.diagnostic_canteen_deleted.invalid_reason_list,
        )

    def test_command_should_not_add_if_dry_run(self):
        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIsNone(self.diagnostic_canteen_deleted.invalid_reason_list)

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2024)

        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIsNone(self.diagnostic_canteen_deleted.invalid_reason_list)

    def test_command_should_add_for_given_year(self):
        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIsNone(self.diagnostic_canteen_deleted.invalid_reason_list)

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2024, apply=True)

        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIn(
            Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE,
            self.diagnostic_canteen_deleted.invalid_reason_list,
        )

        # even if there was a past/wrong reason_item
        Diagnostic.objects.filter(id=self.diagnostic_canteen_deleted.id).update(
            invalid_reason_list=[Diagnostic.InvalidReason.CANTINE_SUPPRIMEE]
        )
        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIn(Diagnostic.InvalidReason.CANTINE_SUPPRIMEE, self.diagnostic_canteen_deleted.invalid_reason_list)
        self.assertNotIn(
            Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE,
            self.diagnostic_canteen_deleted.invalid_reason_list,
        )

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2024, apply=True)

        self.diagnostic_canteen_deleted.refresh_from_db()
        self.assertIn(
            Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE,
            self.diagnostic_canteen_deleted.invalid_reason_list,
        )
        self.assertNotIn(
            Diagnostic.InvalidReason.CANTINE_SUPPRIMEE, self.diagnostic_canteen_deleted.invalid_reason_list
        )
