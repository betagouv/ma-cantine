from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector

year_data = 2024
date_in_teledeclaration_campaign = "2025-03-30"
date_in_correction_campaign = "2025-04-20"
date_in_last_teledeclaration_campaign = "2024-02-01"

VALID_DIAGNOSTIC_SIMPLE_2024 = {
    "year": 2024,
    "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
    "valeur_totale": 1000,
    "valeur_bio": None,
    "valeur_siqo": None,
    "valeur_externalites_performance": None,
    "valeur_egalim_autres": None,
    "valeur_viandes_volailles": None,
    "valeur_viandes_volailles_egalim": None,
    "valeur_viandes_volailles_france": None,
    "valeur_produits_de_la_mer": None,
    "valeur_produits_de_la_mer_egalim": None,
}

VALID_DIAGNOSTIC_SIMPLE_2025 = {
    "year": 2025,
    "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
    "valeur_totale": 1000,
    "valeur_bio": 200,
    "valeur_siqo": 100,
    "valeur_externalites_performance": 100,
    "valeur_egalim_autres": 100,
    "valeur_viandes_volailles": 100,
    "valeur_viandes_volailles_egalim": 50,
    "valeur_viandes_volailles_france": 20,
    "valeur_produits_de_la_mer": 80,
    "valeur_produits_de_la_mer_egalim": 40,
}


class DiagnosticModelSaveTest(TransactionTestCase):
    def test_year_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_YEAR = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_YEAR.pop("year")
        # on save
        for VALUE_OK_ON_SAVE in [None, -2000, 0, 1991, 2024, "2023"]:
            with self.subTest(year=VALUE_OK_ON_SAVE):
                diagnostic = DiagnosticFactory(year=VALUE_OK_ON_SAVE, **VALID_DIAGNOSTIC_WITHOUT_YEAR)
                self.assertEqual(diagnostic.year, VALUE_OK_ON_SAVE)
        for VALUE_NOT_OK_ON_SAVE in ["", "  ", "invalid"]:
            with self.subTest(year=VALUE_NOT_OK_ON_SAVE):
                self.assertRaises(
                    ValueError, Diagnostic.objects.create, year=VALUE_NOT_OK_ON_SAVE, **VALID_DIAGNOSTIC_WITHOUT_YEAR
                )
        # on full_clean
        for TUPLE_OK_ON_FULL_CLEAN in [(2024, 2024), ("2023", 2023)]:
            with self.subTest(year=TUPLE_OK_ON_FULL_CLEAN[0]):
                diagnostic = DiagnosticFactory(year=TUPLE_OK_ON_FULL_CLEAN[0], **VALID_DIAGNOSTIC_WITHOUT_YEAR)
                diagnostic.full_clean()
                self.assertEqual(diagnostic.year, TUPLE_OK_ON_FULL_CLEAN[1])
        for VALUE_NOT_OK_ON_FULL_CLEAN in [None, 1991]:
            with self.subTest(year=VALUE_NOT_OK_ON_FULL_CLEAN):
                diagnostic = DiagnosticFactory(year=VALUE_NOT_OK_ON_FULL_CLEAN, **VALID_DIAGNOSTIC_WITHOUT_YEAR)
                self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_type_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_TYPE = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_TYPE.pop("diagnostic_type")
        # on save
        for VALUE_OK_ON_SAVE in [None, "", "  ", "invalid", 123, *Diagnostic.DiagnosticType.values]:
            with self.subTest(diagnostic_type=VALUE_OK_ON_SAVE):
                diagnostic = DiagnosticFactory(diagnostic_type=VALUE_OK_ON_SAVE, **VALID_DIAGNOSTIC_WITHOUT_TYPE)
                self.assertEqual(diagnostic.diagnostic_type, VALUE_OK_ON_SAVE)
        for VALUE_NOT_OK_ON_SAVE in []:
            with self.subTest(diagnostic_type=VALUE_NOT_OK_ON_SAVE):
                self.assertRaises(
                    (ValueError, ValidationError),
                    DiagnosticFactory,
                    diagnostic_type=VALUE_NOT_OK_ON_SAVE,
                    **VALID_DIAGNOSTIC_WITHOUT_TYPE,
                )
        # on full_clean
        for VALUE_OK_ON_FULL_CLEAN in [*Diagnostic.DiagnosticType.values]:
            with self.subTest(diagnostic_type=VALUE_OK_ON_FULL_CLEAN):
                diagnostic = DiagnosticFactory(diagnostic_type=VALUE_OK_ON_FULL_CLEAN, **VALID_DIAGNOSTIC_WITHOUT_TYPE)
                diagnostic.full_clean()
                self.assertEqual(diagnostic.diagnostic_type, VALUE_OK_ON_FULL_CLEAN)
        for VALUE_NOT_OK_ON_FULL_CLEAN in [None, "", 123, "invalid"]:
            with self.subTest(diagnostic_type=VALUE_NOT_OK_ON_FULL_CLEAN):
                diagnostic = DiagnosticFactory(
                    diagnostic_type=VALUE_NOT_OK_ON_FULL_CLEAN, **VALID_DIAGNOSTIC_WITHOUT_TYPE
                )
                self.assertRaises(ValidationError, diagnostic.full_clean)

    @freeze_time("2024-02-10")  # during the 2024 campaign
    def test_diagnostic_appro_fields_required_before_2024_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_SIMPLE_2024.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on full_clean
        diagnostic = DiagnosticFactory(valeur_totale=None, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
        diagnostic.full_clean()

    def test_diagnostic_simple_appro_fields_required_after_2025_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on full_clean (simple & valeur_totale)
        diagnostic = DiagnosticFactory(valeur_totale=None, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025)
        diagnostic.full_clean()

    def test_diagnostic_complete_appro_fields_required_after_2025_validation(self):
        VALID_DIAGNOSTIC_COMPLETE_2025 = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_COMPLETE_2025["diagnostic_type"] = Diagnostic.DiagnosticType.COMPLETE
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_COMPLETE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on full_clean (complete & valeur_totale)
        diagnostic = DiagnosticFactory(valeur_totale=None, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_COMPLETE_2025)
        diagnostic.full_clean()

    def test_diagnostic_valeur_totale_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on save
        for VALEUR_TOTALE_VALUE_OK_ON_SAVE in [None, -1000, 0, 1000, Decimal("1234.56")]:
            with self.subTest(valeur_totale=VALEUR_TOTALE_VALUE_OK_ON_SAVE):
                diagnostic = DiagnosticFactory(
                    valeur_totale=VALEUR_TOTALE_VALUE_OK_ON_SAVE, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE
                )
                self.assertEqual(diagnostic.valeur_totale, VALEUR_TOTALE_VALUE_OK_ON_SAVE)
        for VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE in ["", "  ", "invalid"]:
            with self.subTest(valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE):
                self.assertRaises(
                    (ValueError, ValidationError),
                    DiagnosticFactory,
                    valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE,
                    **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE,
                )
        # on full_clean
        for VALEUR_TOTALE_VALUE_OK_ON_FULL_CLEAN in [1000, Decimal("1234.56")]:
            diagnostic = DiagnosticFactory(
                valeur_totale=VALEUR_TOTALE_VALUE_OK_ON_FULL_CLEAN, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE
            )
            diagnostic.full_clean()
        for VALEUR_TOTALE_VALUE_NOT_OK_ON_FULL_CLEAN in [None, -1000, 0]:
            with self.subTest(valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_FULL_CLEAN):
                diagnostic = DiagnosticFactory(
                    valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_FULL_CLEAN, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE
                )
                self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_valeur_totale_extra_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTAL_HT = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTAL_HT.pop("valeur_totale")
        # should be > the sum of other fields
        self.assertEqual(
            sum(
                VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTAL_HT[k]
                for k in [
                    "valeur_bio",
                    "valeur_siqo",
                    "valeur_externalites_performance",
                    "valeur_egalim_autres",
                ]
            ),
            500,
        )
        for VALUE_NOT_OK in [-100, 0, 100]:
            with self.subTest(valeur_totale=VALUE_NOT_OK):
                diagnostic = DiagnosticFactory(valeur_totale=VALUE_NOT_OK, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTAL_HT)
                self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_valeur_viandes_volailles_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_VIANDES_VOLAILLES = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_VIANDES_VOLAILLES.pop("valeur_viandes_volailles")
        # should be >= valeur_viandes_volailles_egalim
        self.assertEqual(VALID_DIAGNOSTIC_WITHOUT_VALEUR_VIANDES_VOLAILLES["valeur_viandes_volailles_egalim"], 50)
        for VALUE_NOT_OK in [-100, 0, 49]:
            with self.subTest(valeur_viandes_volailles=VALUE_NOT_OK):
                diagnostic = DiagnosticFactory(
                    valeur_viandes_volailles=VALUE_NOT_OK, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_VIANDES_VOLAILLES
                )
                self.assertRaises(ValidationError, diagnostic.full_clean)
        # should be >= valeur_viandes_volailles_france
        self.assertEqual(VALID_DIAGNOSTIC_WITHOUT_VALEUR_VIANDES_VOLAILLES["valeur_viandes_volailles_france"], 20)
        for VALUE_NOT_OK in [-100, 0, 19]:
            with self.subTest(valeur_viandes_volailles=VALUE_NOT_OK):
                diagnostic = DiagnosticFactory(
                    valeur_viandes_volailles=VALUE_NOT_OK, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_VIANDES_VOLAILLES
                )
                self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_valeur_produits_de_la_mer_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_PRODUITS_DE_LA_MER = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_PRODUITS_DE_LA_MER.pop("valeur_produits_de_la_mer")
        # should be >= valeur_produits_de_la_mer_egalim
        self.assertEqual(VALID_DIAGNOSTIC_WITHOUT_VALEUR_PRODUITS_DE_LA_MER["valeur_produits_de_la_mer_egalim"], 40)
        for VALUE_NOT_OK in [-100, 0, 39]:
            with self.subTest(valeur_produits_de_la_mer=VALUE_NOT_OK):
                diagnostic = DiagnosticFactory(
                    valeur_produits_de_la_mer=VALUE_NOT_OK, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_PRODUITS_DE_LA_MER
                )
                self.assertRaises(ValidationError, diagnostic.full_clean)


class Diagnostic2024ModelSaveTest(TransactionTestCase):
    @freeze_time("2024-02-10")  # during the 2024 campaign
    def test_diagnostic_simple_2024(self):
        # valid
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
        diagnostic.full_clean()
        # valid (valeur_bio is optional)
        VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_BIO = {**VALID_DIAGNOSTIC_SIMPLE_2024, "valeur_bio": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_BIO)
        diagnostic.full_clean()
        # not valid (valeur_totale is required)
        VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_TOTALE = {**VALID_DIAGNOSTIC_SIMPLE_2024, "valeur_totale": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)

    @freeze_time("2024-02-10")  # during the 2024 campaign
    def test_diagnostic_complete_2024(self):
        # valid
        VALID_DIAGNOSTIC_SIMPLE_2024_COMPLETE = {
            **VALID_DIAGNOSTIC_SIMPLE_2024,
            "diagnostic_type": Diagnostic.DiagnosticType.COMPLETE,
        }
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024_COMPLETE)
        diagnostic.full_clean()


class Diagnostic2025ModelSaveTest(TransactionTestCase):
    def test_diagnostic_simple_2025(self):
        # valid
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025)
        diagnostic.full_clean()
        # not valid (valeur_bio is required)
        VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_BIO = {**VALID_DIAGNOSTIC_SIMPLE_2025, "valeur_bio": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_BIO)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        # not valid (valeur_totale is required)
        VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_TOTALE = {**VALID_DIAGNOSTIC_SIMPLE_2025, "valeur_totale": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_complete_2025(self):
        # valid (because DiagnosticFactory sets default values)
        VALID_DIAGNOSTIC_SIMPLE_2025_COMPLETE = {
            **VALID_DIAGNOSTIC_SIMPLE_2025,
            "diagnostic_type": Diagnostic.DiagnosticType.COMPLETE,
        }
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025_COMPLETE)
        diagnostic.full_clean()
        # not valid (valeur_produits_de_la_mer is required)
        diagnostic = DiagnosticFactory(
            **VALID_DIAGNOSTIC_SIMPLE_2025_COMPLETE
        )  # sets a value for valeur_produits_de_la_mer
        diagnostic.valeur_produits_de_la_mer = None
        diagnostic.save()
        self.assertRaises(ValidationError, diagnostic.full_clean)


class DiagnosticQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_valid_1 = CanteenFactory(siret="92341284500011", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_valid_2 = CanteenFactory(siret=None, siren_unite_legale="123456789")
        cls.canteen_valid_3 = CanteenFactory(siret=None, siren_unite_legale="123456789")
        cls.canteen_valid_4 = CanteenFactory(siret="40419443300078")
        Canteen.objects.filter(id=cls.canteen_valid_4.id).update(yearly_meal_count=0)  # not aberrant
        cls.canteen_valid_4.refresh_from_db()
        cls.canteen_valid_5 = CanteenFactory(siret="21340172201787")
        Canteen.objects.filter(id=cls.canteen_valid_5.id).update(yearly_meal_count=None)  # not aberrant
        cls.canteen_valid_5.refresh_from_db()
        cls.canteen_valid_sat = CanteenFactory(
            siret="21380185500015",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_valid_1.siret,
        )
        cls.canteen_valid_6_armee = CanteenFactory(siret="21640122400011", line_ministry=Canteen.Ministries.ARMEE)
        cls.canteen_missing_siret = CanteenFactory()
        Canteen.objects.filter(id=cls.canteen_missing_siret.id).update(siret="")  # siret missing
        cls.canteen_missing_siret.refresh_from_db()
        cls.canteen_meal_price_aberrant = CanteenFactory(siret="21670482500019", yearly_meal_count=1000)
        cls.canteen_valeur_totale_aberrant = CanteenFactory(siret="21630113500010", yearly_meal_count=100000)
        cls.canteen_aberrant = CanteenFactory(siret="21130055300016", yearly_meal_count=1000)
        cls.canteen_deleted = CanteenFactory(
            siret="21730065600014",
            deletion_date=timezone.make_aware(
                datetime.strptime(date_in_teledeclaration_campaign, "%Y-%m-%d")
            ),  # soft deleted
        )

        for index, canteen in enumerate(
            [
                cls.canteen_valid_1,
                cls.canteen_valid_2,
                cls.canteen_valid_3,
                cls.canteen_valid_4,
                cls.canteen_valid_5,
                cls.canteen_valid_6_armee,
            ]
        ):
            diagnostic = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
                creation_date=date_in_teledeclaration_campaign,
                canteen=canteen,
                valeur_totale=1000.00,
                valeur_bio=200.00,
                valeur_siqo=100.00,
                valeur_externalites_performance=100.00,
                valeur_egalim_autres=100.00,
            )
            with freeze_time(date_in_teledeclaration_campaign):
                diagnostic.teledeclare(applicant=UserFactory())
            diagnostic_last_year = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data - 1,
                creation_date=date_in_last_teledeclaration_campaign,
                canteen=canteen,
                valeur_totale=1000.00,
                valeur_bio=200.00,
            )
            with freeze_time(date_in_last_teledeclaration_campaign):
                diagnostic_last_year.teledeclare(applicant=UserFactory())
            setattr(cls, f"diagnostic_canteen_valid_{index + 1}", diagnostic)

        cls.diagnostic_canteen_missing_siret = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_missing_siret,
            valeur_totale=1000.00,
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_missing_siret.teledeclare(applicant=UserFactory())

        cls.diagnostic_canteen_meal_price_aberrant = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_meal_price_aberrant,
            valeur_totale=1000000.00,  # meal_price > 20
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_meal_price_aberrant.teledeclare(applicant=UserFactory())

        cls.diagnostic_canteen_valeur_totale_aberrant = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_valeur_totale_aberrant,
            valeur_totale=1000001.00,  # aberrant but meal_price < 20
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_valeur_totale_aberrant.teledeclare(applicant=UserFactory())

        cls.diagnostic_canteen_aberrant = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_aberrant,
            valeur_totale=1000001.00,  # aberrant AND meal_price > 20
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_aberrant.teledeclare(applicant=UserFactory())

        cls.diagnostic_canteen_deleted = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_deleted,
            valeur_totale=1000.00,
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_deleted.teledeclare(applicant=UserFactory())

    def test_canteen_not_deleted_during_campaign(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.canteen_not_deleted_during_campaign(year_data)
        self.assertEqual(diagnostics.count(), 16)
        self.assertNotIn(self.diagnostic_canteen_deleted, diagnostics)

    def test_canteen_has_siret_or_siren_unite_legale(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.canteen_has_siret_or_siren_unite_legale()
        self.assertEqual(diagnostics.count(), 16)
        self.assertNotIn(self.diagnostic_canteen_missing_siret, diagnostics)

    def test_canteen_for_stat(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.canteen_for_stat(year_data)
        self.assertEqual(diagnostics.count(), 15)
        self.assertNotIn(self.diagnostic_canteen_missing_siret, diagnostics)  # canteen without siret/siren
        self.assertNotIn(self.diagnostic_canteen_deleted, diagnostics)  # canteen deleted during campaign

    def test_teledeclared_for_year(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.teledeclared_for_year(year_data)
        self.assertEqual(diagnostics.count(), 11)
        self.assertIn(self.diagnostic_canteen_valid_1, diagnostics)
        self.assertIn(self.diagnostic_canteen_missing_siret, diagnostics)
        self.assertIn(self.diagnostic_canteen_deleted, diagnostics)
        diagnostics = Diagnostic.objects.teledeclared_for_year(year_data - 1)
        self.assertEqual(diagnostics.count(), 6)

    def test_valid_td_by_year(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.valid_td_by_year(year_data)
        self.assertEqual(diagnostics.count(), 8)
        self.assertIn(self.diagnostic_canteen_valid_1, diagnostics)
        self.assertNotIn(self.diagnostic_canteen_missing_siret, diagnostics)  # canteen without siret/siren
        self.assertNotIn(self.diagnostic_canteen_deleted, diagnostics)  # canteen deleted during campaign

    def test_historical_valid_td(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.historical_valid_td([year_data])
        self.assertEqual(diagnostics.count(), 8)
        diagnostics = Diagnostic.objects.historical_valid_td([year_data - 1])
        self.assertEqual(diagnostics.count(), 6)
        diagnostics = Diagnostic.objects.historical_valid_td([year_data, year_data - 1])
        self.assertEqual(diagnostics.count(), 8 + 6)

    def test_with_meal_price(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.with_meal_price()
        self.assertEqual(diagnostics.count(), 17)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_1.id).canteen_yearly_meal_count, 1000)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_1.id).meal_price, 1.0)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_4.id).canteen_yearly_meal_count, 0)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_4.id).meal_price, None)

    def test_exclude_aberrant_values(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.exclude_aberrant_values()
        self.assertEqual(diagnostics.count(), 16)
        self.assertNotIn(self.diagnostic_canteen_aberrant, diagnostics)

    def test_publicly_visible(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        self.assertEqual(Diagnostic.objects.publicly_visible().count(), 15)  # 2 belong to canteen_army

    def test_with_appro_percent_stats(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.with_appro_percent_stats()
        self.assertEqual(diagnostics.count(), 17)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_4.id).bio_percent, 20)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_4.id).egalim_percent, 50)


class DiagnosticIsFilledQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_2024_simple_not_filled = DiagnosticFactory(
            year=2024, canteen=CanteenFactory(), diagnostic_type=Diagnostic.DiagnosticType.SIMPLE, valeur_totale=None
        )
        cls.diagnostic_2024_simple_filled = DiagnosticFactory(
            year=2024, canteen=CanteenFactory(), diagnostic_type=Diagnostic.DiagnosticType.SIMPLE, valeur_totale=1000
        )
        cls.diagnostic_2024_complete_not_filled = DiagnosticFactory(
            year=2024, canteen=CanteenFactory(), diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, valeur_totale=None
        )
        cls.diagnostic_2024_complete_filled = DiagnosticFactory(
            year=2024, canteen=CanteenFactory(), diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, valeur_totale=1000
        )
        cls.diagnostic_2025_simple_not_filled = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            valeur_totale=None,
            valeur_bio=None,
        )
        cls.diagnostic_2025_simple_filled = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            valeur_totale=1000,
            valeur_bio=200,
            valeur_siqo=100,
            valeur_egalim_autres=100,
            valeur_viandes_volailles=100,
            valeur_viandes_volailles_egalim=0,
        )
        cls.diagnostic_2025_complete_not_filled = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_totale=1000,
            valeur_bio=200,
            valeur_siqo=100,
            valeur_egalim_autres=100,
            valeur_viandes_volailles=100,
            valeur_viandes_volailles_egalim=0,
        )
        cls.diagnostic_2025_complete_not_filled.valeur_produits_de_la_mer = None
        cls.diagnostic_2025_complete_not_filled.save()
        cls.diagnostic_2025_complete_filled = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_totale=1000,
            valeur_bio=200,
            valeur_siqo=100,
            valeur_egalim_autres=100,
            valeur_viandes_volailles=100,
            valeur_viandes_volailles_egalim=0,
            # rest will be filled by DiagnosticFactory defaults
        )

    def test_filled_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 8)
        self.assertEqual(Diagnostic.objects.filled().count(), 4)

    def test_is_filled_property(self):
        # filled
        for diagnostic in [
            self.diagnostic_2024_simple_filled,
            self.diagnostic_2024_complete_filled,
            self.diagnostic_2025_simple_filled,
            self.diagnostic_2025_complete_filled,
        ]:
            with self.subTest(diagnostic=diagnostic):
                self.assertTrue(diagnostic.is_filled)
        # not filled
        for diagnostic in [
            self.diagnostic_2024_simple_not_filled,
            self.diagnostic_2024_complete_not_filled,
            self.diagnostic_2025_simple_not_filled,
            self.diagnostic_2025_complete_not_filled,
        ]:
            with self.subTest(diagnostic=diagnostic):
                self.assertFalse(diagnostic.is_filled)


class DiagnosticTeledeclaredQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_not_filled_draft = DiagnosticFactory(canteen=CanteenFactory(), valeur_totale=None)
        cls.diagnostic_filled_draft = DiagnosticFactory(canteen=CanteenFactory(), valeur_totale=1000)
        cls.diagnostic_filled_submitted = DiagnosticFactory(
            canteen=CanteenFactory(), valeur_totale=1000, status=Diagnostic.DiagnosticStatus.SUBMITTED
        )

    def test_teledeclared_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 3)
        self.assertEqual(Diagnostic.objects.teledeclared().count(), 1)

    def test_is_teledeclared_property(self):
        self.assertFalse(self.diagnostic_not_filled_draft.is_teledeclared)
        self.assertFalse(self.diagnostic_filled_draft.is_teledeclared)
        self.assertTrue(self.diagnostic_filled_submitted.is_teledeclared)


class DiagnosticModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen_central = CanteenFactory(siret="92341284500011", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_sat = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_central,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
            valeur_bio=200,
        )

    def test_delete_canteen(self):
        self.assertIsNotNone(self.diagnostic.canteen)
        # soft delete
        self.canteen_central.delete()
        self.diagnostic.refresh_from_db()
        self.assertIsNotNone(self.diagnostic.canteen)
        # hard delete
        self.canteen_central.hard_delete()
        self.diagnostic.refresh_from_db()
        self.assertIsNone(self.diagnostic.canteen)

    def test_delete_applicant(self):
        with freeze_time(date_in_teledeclaration_campaign):
            self.diagnostic.teledeclare(applicant=self.user)
        self.assertIsNotNone(self.diagnostic.applicant)
        # delete
        self.user.delete()
        self.diagnostic.refresh_from_db()
        self.assertIsNone(self.diagnostic.applicant)


class DiagnosticModelTeledeclareMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen_central = CanteenFactory(siret="92341284500011", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_sat = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
            sector_list=[Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL],
        )
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_central,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=0,
        )

    @freeze_time(date_in_last_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_outside_of_campaign(self):
        with self.assertRaises(ValidationError):
            self.diagnostic.teledeclare(applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_cannot_teledeclare_a_diagnostic_not_filled(self):
        self.assertEqual(self.diagnostic.valeur_totale, 0)
        with self.assertRaises(ValidationError):
            self.diagnostic.teledeclare(applicant=self.user)

    @freeze_time(date_in_teledeclaration_campaign)
    def test_teledeclare(self):
        self.assertIsNone(self.diagnostic.applicant)
        self.assertIsNone(self.diagnostic.canteen_snapshot)
        self.assertIsNone(self.diagnostic.satellites_snapshot)
        self.assertIsNone(self.diagnostic.applicant_snapshot)
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.DRAFT)
        self.assertIsNone(self.diagnostic.teledeclaration_date)
        self.assertIsNone(self.diagnostic.teledeclaration_mode)
        self.assertIsNone(self.diagnostic.teledeclaration_version)
        self.assertIsNone(self.diagnostic.teledeclaration_id)
        # fill the diagnostic
        self.diagnostic.valeur_totale = 1000
        self.diagnostic.valeur_bio = 200
        self.diagnostic.valeur_siqo = 100
        self.diagnostic.valeur_externalites_performance = 100
        self.diagnostic.valeur_egalim_autres = 100
        self.diagnostic.save()
        # teledeclare
        self.diagnostic.teledeclare(applicant=self.user)
        self.assertEqual(self.diagnostic.applicant, self.user)
        self.assertIsNotNone(self.diagnostic.canteen_snapshot)
        self.assertEqual(self.diagnostic.valeur_bio_agg, 200)
        self.assertEqual(self.diagnostic.valeur_siqo_agg, 100)
        self.assertEqual(self.diagnostic.valeur_externalites_performance_agg, 100)
        self.assertEqual(self.diagnostic.valeur_egalim_autres_agg, 100)
        self.assertEqual(self.diagnostic.valeur_egalim_hors_bio_agg, 300)
        self.assertEqual(self.diagnostic.valeur_egalim_agg, 500)
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.SUBMITTED)
        self.assertIsNotNone(self.diagnostic.teledeclaration_date)
        self.assertEqual(self.diagnostic.teledeclaration_mode, Diagnostic.TeledeclarationMode.CENTRAL_ALL)
        self.assertEqual(self.diagnostic.teledeclaration_version, 16)
        self.assertIsNone(self.diagnostic.teledeclaration_id)
        # for snapshots, see tests below
        # try to teledeclare again
        with self.assertRaises(ValidationError):
            self.diagnostic.teledeclare(applicant=UserFactory())


class DiagnosticModelCancelMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(siret="92341284500011", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_sat = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_central,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
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
        self.diagnostic.teledeclare(applicant=UserFactory())
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.SUBMITTED)
        self.assertIsNotNone(self.diagnostic.applicant)
        self.assertIsNotNone(self.diagnostic.teledeclaration_date)
        self.assertIsNotNone(self.diagnostic.teledeclaration_mode)
        self.assertIsNotNone(self.diagnostic.teledeclaration_version)
        self.assertIsNone(self.diagnostic.teledeclaration_id)
        # cancel
        self.diagnostic.cancel()
        self.assertEqual(self.diagnostic.status, Diagnostic.DiagnosticStatus.DRAFT)
        self.assertIsNone(self.diagnostic.applicant)
        self.assertIsNone(self.diagnostic.teledeclaration_date)
        self.assertIsNone(self.diagnostic.teledeclaration_mode)
        self.assertIsNone(self.diagnostic.teledeclaration_version)
        self.assertIsNone(self.diagnostic.teledeclaration_id)


class DiagnosticTeledeclaredSnapshotsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        # central + sat
        cls.canteen_central = CanteenFactory(siret="92341284500011", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_sat = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.diagnostic_central = DiagnosticFactory(
            canteen=cls.canteen_central,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
        )
        # site
        cls.canteen_site = CanteenFactory(
            siret="21640122400011",
            production_type=Canteen.ProductionType.ON_SITE,
            sector_list=[Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL],
        )
        cls.diagnostic_site = DiagnosticFactory(
            canteen=cls.canteen_site,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
            valeur_bio=200,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_central.teledeclare(applicant=cls.user)
            cls.diagnostic_site.teledeclare(applicant=cls.user)

    def test_diagnostic_canteen_snapshot(self):
        # central
        self.assertIsNotNone(self.diagnostic_central.canteen_snapshot)
        self.assertEqual(self.diagnostic_central.canteen_snapshot["id"], self.canteen_central.id)
        self.assertEqual(self.diagnostic_central.canteen_snapshot["production_type"], Canteen.ProductionType.CENTRAL)
        self.assertEqual(self.diagnostic_central.canteen_snapshot["sector_list"], [])
        self.assertEqual(self.diagnostic_central.canteen_snapshot_sector_list_display, None)
        # site
        self.assertIsNotNone(self.diagnostic_site.canteen_snapshot)
        self.assertEqual(self.diagnostic_site.canteen_snapshot["id"], self.canteen_site.id)
        self.assertEqual(self.diagnostic_site.canteen_snapshot["production_type"], Canteen.ProductionType.ON_SITE)
        self.assertEqual(len(self.diagnostic_site.canteen_snapshot["sector_list"]), 2)
        self.assertEqual(self.diagnostic_site.canteen_snapshot["sector_list"][0], "education_primaire")
        self.assertEqual(
            self.diagnostic_site.canteen_snapshot_sector_list_display,
            "Ecole primaire (maternelle et élémentaire), Hôpitaux",
        )

    def test_diagnostic_satellites_snapshot(self):
        # central
        self.assertIsNotNone(self.diagnostic_central.satellites_snapshot)
        self.assertEqual(len(self.diagnostic_central.satellites_snapshot), 1)
        self.assertEqual(self.diagnostic_central.satellites_snapshot[0]["id"], self.canteen_sat.id)
        # site
        self.assertIsNone(self.diagnostic_site.satellites_snapshot)

    def test_diagnostic_applicant_snapshot(self):
        # central
        self.assertIsNotNone(self.diagnostic_central.applicant_snapshot)
        self.assertEqual(self.diagnostic_central.applicant_snapshot["id"], self.user.id)
        self.assertEqual(self.diagnostic_central.applicant_snapshot["email"], self.user.email)
        # site
        self.assertIsNotNone(self.diagnostic_site.applicant_snapshot)
        self.assertEqual(self.diagnostic_site.applicant_snapshot["id"], self.user.id)
        self.assertEqual(self.diagnostic_site.applicant_snapshot["email"], self.user.email)
