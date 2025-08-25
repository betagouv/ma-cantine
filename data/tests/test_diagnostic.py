from django.core.exceptions import ValidationError
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
        cls.valid_canteen_1 = CanteenFactory(siret="12345678901234", yearly_meal_count=100)
        cls.valid_canteen_2 = CanteenFactory(siren_unite_legale="123456789", yearly_meal_count=100)
        cls.valid_canteen_3 = CanteenFactory(
            siret="12345678901235", siren_unite_legale="123456789", yearly_meal_count=100
        )
        cls.valid_canteen_4 = CanteenFactory(siret="12345678901230", yearly_meal_count=0)  # not aberrant
        cls.valid_canteen_sat = CanteenFactory(
            siret="12345678901232", production_type=Canteen.ProductionType.ON_SITE_CENTRAL
        )
        cls.valid_canteen_5_armee = CanteenFactory(
            siret="12345678901233", line_ministry=Canteen.Ministries.ARMEE, yearly_meal_count=100
        )
        cls.invalid_canteen = CanteenFactory(siret="", yearly_meal_count=100)  # siret missing
        cls.deleted_canteen = CanteenFactory(
            siret="56789012345678",
            yearly_meal_count=100,
            deletion_date=timezone.now() - timezone.timedelta(days=30),  # soft deleted
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

        cls.valid_canteen_diagnostic_4 = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.valid_canteen_4,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
            value_sustainable_ht=100.00,
            value_externality_performance_ht=100.00,
            value_egalim_others_ht=100.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.valid_canteen_diagnostic_4.teledeclare()

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
            value_total_ht=1000001.00,  # aberrant (and meal_price > 20)
            value_bio_ht=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.deleted_canteen_diagnostic.teledeclare()

    def test_teledeclared_for_year(self):
        self.assertEqual(Diagnostic.objects.count(), 11)
        diagnostics = Diagnostic.objects.teledeclared_for_year(year_data)
        self.assertEqual(diagnostics.count(), 7)
        self.assertIn(self.valid_canteen_diagnostic_1, diagnostics)
        self.assertIn(self.invalid_canteen_diagnostic, diagnostics)
        self.assertIn(self.deleted_canteen_diagnostic, diagnostics)
        diagnostics = Diagnostic.objects.teledeclared_for_year(year_data - 1)
        self.assertEqual(diagnostics.count(), 4)

    def test_valid_td_by_year(self):
        diagnostics = Diagnostic.objects.valid_td_by_year(year_data)
        self.assertEqual(diagnostics.count(), 5)
        self.assertIn(self.valid_canteen_diagnostic_1, diagnostics)
        self.assertNotIn(self.invalid_canteen_diagnostic, diagnostics)  # canteen without siret
        self.assertNotIn(self.deleted_canteen_diagnostic, diagnostics)  # canteen deleted

    def test_historical_valid_td(self):
        diagnostics = Diagnostic.objects.historical_valid_td([year_data])
        self.assertEqual(diagnostics.count(), 5)
        diagnostics = Diagnostic.objects.historical_valid_td([year_data - 1])
        self.assertEqual(diagnostics.count(), 4)
        diagnostics = Diagnostic.objects.historical_valid_td([year_data, year_data - 1])
        self.assertEqual(diagnostics.count(), 5 + 4)

    def test_with_meal_price(self):
        self.assertEqual(Diagnostic.objects.count(), 11)
        diagnostics = Diagnostic.objects.with_meal_price()
        self.assertEqual(diagnostics.count(), 11)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_1.id).canteen_yearly_meal_count, 100)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_1.id).meal_price, 10.0)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_4.id).canteen_yearly_meal_count, 0)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_4.id).meal_price, None)

    def test_exclude_aberrant_values(self):
        self.assertEqual(Diagnostic.objects.count(), 11)
        self.assertEqual(Diagnostic.objects.exclude_aberrant_values().count(), 10)  # 1 aberrant

    def test_publicly_visible(self):
        self.assertEqual(Diagnostic.objects.count(), 11)
        self.assertEqual(Diagnostic.objects.publicly_visible().count(), 9)  # 2 belong to canteen_army

    def test_with_appro_percent_stats(self):
        self.assertEqual(Diagnostic.objects.count(), 11)
        diagnostics = Diagnostic.objects.with_appro_percent_stats()
        self.assertEqual(diagnostics.count(), 11)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_4.id).bio_percent, 20)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_4.id).value_egalim_ht_agg, 500)
        self.assertEqual(diagnostics.get(id=self.valid_canteen_diagnostic_4.id).egalim_percent, 50)


class DiagnosticIsFilledQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_empty = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=None)
        cls.diagnostic_filled = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=1000)

    def test_filled_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 2)
        self.assertEqual(Diagnostic.objects.filled().count(), 1)

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


class DiagnosticModelTeledeclareMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(siret="12345678901234", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_sat = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_central,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            value_total_ht=0,
        )

    @freeze_time(date_in_last_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_outside_of_campaign(self):
        with self.assertRaises(ValidationError):
            self.diagnostic.teledeclare()

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_not_filled(self):
        self.assertEqual(self.diagnostic.value_total_ht, 0)
        with self.assertRaises(ValidationError):
            self.diagnostic.teledeclare()

    @freeze_time(date_in_teledeclaration_campaign)
    def test_teledeclare(self):
        self.assertIsNone(self.diagnostic.canteen_snapshot)
        self.assertIsNone(self.diagnostic.satellites_snapshot)
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.DRAFT)
        self.assertIsNone(self.diagnostic.teledeclaration_date)
        # fill the diagnostic
        self.diagnostic.value_total_ht = 1000
        self.diagnostic.value_bio_ht = 200
        self.diagnostic.value_sustainable_ht = 100
        self.diagnostic.value_externality_performance_ht = 100
        self.diagnostic.value_egalim_others_ht = 100
        self.diagnostic.save()
        # teledeclare
        self.diagnostic.teledeclare()
        self.assertIsNotNone(self.diagnostic.canteen_snapshot)
        self.assertEqual(self.diagnostic.canteen_snapshot["id"], self.canteen_central.id)
        self.assertIsNotNone(self.diagnostic.satellites_snapshot)
        self.assertEqual(len(self.diagnostic.satellites_snapshot), 1)
        self.assertEqual(self.diagnostic.satellites_snapshot[0]["id"], self.canteen_sat.id)
        self.assertEqual(self.diagnostic.value_bio_ht_agg, 200)
        self.assertEqual(self.diagnostic.value_sustainable_ht_agg, 100)
        self.assertEqual(self.diagnostic.value_externality_performance_ht_agg, 100)
        self.assertEqual(self.diagnostic.value_egalim_others_ht_agg, 100)
        self.assertEqual(self.diagnostic.value_egalim_ht_agg, 500)
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.SUBMITTED)
        self.assertIsNotNone(self.diagnostic.teledeclaration_date)
        self.assertEqual(self.diagnostic.teledeclaration_mode, Diagnostic.TeledeclarationMode.CENTRAL_ALL)
        # try to teledeclare again
        with self.assertRaises(ValidationError):
            self.diagnostic.teledeclare()


class DiagnosticModelCancelMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(siret="12345678901234", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_sat = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_central,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            value_total_ht=1000,
        )

    @freeze_time(date_in_last_teledeclaration_campaign)
    def test_cannot_cancel_a_diagnostic_outside_of_campaign(self):
        with self.assertRaises(ValidationError):
            self.diagnostic.cancel()

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_cancel_a_diagnostic_not_teledeclared(self):
        with self.assertRaises(ValidationError):
            self.diagnostic.cancel()

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cancel(self):
        # teledeclare the diagnostic
        self.diagnostic.teledeclare()
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.SUBMITTED)
        self.assertIsNotNone(self.diagnostic.teledeclaration_date)
        self.assertIsNotNone(self.diagnostic.teledeclaration_mode)
        # cancel
        self.diagnostic.cancel()
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.DRAFT)
        self.assertIsNone(self.diagnostic.teledeclaration_date)
        self.assertIsNone(self.diagnostic.teledeclaration_mode)
