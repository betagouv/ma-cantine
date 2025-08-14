from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic

year_data = 2024
date_in_teledeclaration_campaign = "2025-03-30"
date_in_correction_campaign = "2025-04-20"
date_in_last_teledeclaration_campaign = "2024-02-01"


class DiagnosticQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_canteen_1 = CanteenFactory(siret="12345678901234", deletion_date=None, yearly_meal_count=100)
        cls.valid_canteen_2 = CanteenFactory(siren_unite_legale="123456789", deletion_date=None)
        cls.valid_canteen_3 = CanteenFactory(
            siret="12345678901235", siren_unite_legale="123456789", deletion_date=None
        )
        cls.valid_canteen_4 = CanteenFactory(siret="12345678901230", deletion_date=None, yearly_meal_count=0)
        cls.valid_canteen_sat = CanteenFactory(
            siret="12345678901232", deletion_date=None, production_type=Canteen.ProductionType.ON_SITE_CENTRAL
        )
        cls.valid_canteen_5_armee = CanteenFactory(
            siret="12345678901233",
            line_ministry=Canteen.Ministries.ARMEE,
        )
        cls.invalid_canteen = CanteenFactory(siret="", deletion_date=None)  # siret missing
        cls.deleted_canteen = CanteenFactory(
            siret="56789012345678",
            deletion_date=timezone.now() - timezone.timedelta(days=30),
        )

        for index, canteen in enumerate(
            [cls.valid_canteen_1, cls.valid_canteen_2, cls.valid_canteen_3, cls.valid_canteen_5_armee]
        ):
            diagnostic = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
                creation_date=date_in_teledeclaration_campaign,
                canteen=canteen,
                value_total_ht=1000.00,
                value_bio_ht=200.00,
            )
            with freeze_time(date_in_teledeclaration_campaign):
                diagnostic.teledeclare()
            diagnostic_last_year = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data - 1,
                creation_date=date_in_last_teledeclaration_campaign,
                canteen=canteen,
                value_total_ht=1000.00,
                value_bio_ht=200.00,
            )
            with freeze_time(date_in_last_teledeclaration_campaign):
                diagnostic_last_year.teledeclare()
            setattr(cls, f"valid_canteen_diagnostic_{index + 1}", diagnostic)

        cls.invalid_canteen_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.invalid_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.invalid_canteen_diagnostic.teledeclare()
        cls.deleted_canteen_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.deleted_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.deleted_canteen_diagnostic.teledeclare()

    @freeze_time("2025-03-30")
    def test_teledeclared_for_year(self):
        teledeclarations = Diagnostic.objects.teledeclared_for_year(year_data)
        self.assertEqual(teledeclarations.count(), 6)
        self.assertIn(self.valid_canteen_diagnostic_1, teledeclarations)
        self.assertIn(self.invalid_canteen_diagnostic, teledeclarations)
        self.assertIn(self.deleted_canteen_diagnostic, teledeclarations)
        teledeclarations = Diagnostic.objects.teledeclared_for_year(year_data - 1)
        self.assertEqual(teledeclarations.count(), 4)

    def test_publicly_visible(self):
        self.assertEqual(Diagnostic.objects.count(), 10)
        self.assertEqual(Diagnostic.objects.publicly_visible().count(), 8)  # 2 belong to canteen_army


class DiagnosticIsFilledQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_empty = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=None)
        cls.diagnostic_filled = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=1000)

    def test_is_filled_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 2)
        self.assertEqual(Diagnostic.objects.is_filled().count(), 1)

    def test_is_filled_property(self):
        self.assertFalse(self.diagnostic_empty.is_filled)
        self.assertTrue(self.diagnostic_filled.is_filled)


class DiagnosticTeledeclaredQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_empty_draft = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=None)
        cls.diagnostic_filled_draft = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=1000)
        cls.diagnostic_filled_submitted = DiagnosticFactory.create(
            canteen=CanteenFactory(), value_total_ht=1000, status=Diagnostic.DiagnosticStatus.SUBMITTED
        )

    def test_teledeclared_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 3)
        self.assertEqual(Diagnostic.objects.teledeclared().count(), 1)

    def test_is_teledeclared_property(self):
        self.assertFalse(self.diagnostic_empty_draft.is_teledeclared)
        self.assertFalse(self.diagnostic_filled_draft.is_teledeclared)
        self.assertTrue(self.diagnostic_filled_submitted.is_teledeclared)
