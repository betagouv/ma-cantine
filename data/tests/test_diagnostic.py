from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Sector
from data.models.diagnostic import (
    Diagnostic,
    canteen_has_siret_or_siren_unite_legale_query,
    canteen_soft_deleted_during_campaign_query,
    circuit_court_sup_france_query,
    commerce_equitable_sup_bio_query,
    local_sup_france_query,
)

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
    @freeze_time("2026-01-30")  # during the 2025 campaign
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
        this_year = datetime.now().date().year
        last_year = datetime.now().date().year - 1
        next_year = datetime.now().date().year + 1
        last_two_years = datetime.now().date().year - 2
        next_two_years = datetime.now().date().year + 2
        for TUPLE_OK_ON_FULL_CLEAN in [
            (this_year, this_year),
            (f"{this_year}", this_year),
            (last_year, last_year),
            (f"{last_year}", last_year),
            (next_year, next_year),
            (f"{next_year}", next_year),
        ]:
            with self.subTest(year=TUPLE_OK_ON_FULL_CLEAN[0]):
                diagnostic = DiagnosticFactory(year=TUPLE_OK_ON_FULL_CLEAN[0], **VALID_DIAGNOSTIC_WITHOUT_YEAR)
                diagnostic.full_clean()
                self.assertEqual(diagnostic.year, TUPLE_OK_ON_FULL_CLEAN[1])
        for VALUE_NOT_OK_ON_FULL_CLEAN in [None, 1991, last_two_years, next_two_years, 2222]:
            with self.subTest(year=VALUE_NOT_OK_ON_FULL_CLEAN):
                diagnostic = DiagnosticFactory(year=VALUE_NOT_OK_ON_FULL_CLEAN, **VALID_DIAGNOSTIC_WITHOUT_YEAR)
                self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_can_edit_status_draft_validation(self):
        # DRAFT diagnostic cannot be edited during the campaign but not after
        with freeze_time("2025-01-20"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.DRAFT)
            diagnostic.full_clean()  # should not raise
        with freeze_time("2025-04-18"):  # during the 2024 correction campaign
            self.assertRaises(ValidationError, diagnostic.full_clean)
        with freeze_time("2025-08-30"):  # after the 2024 correction campaign
            self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_can_edit_status_correction_validation(self):
        # CORRECTION diagnostic can be edited during the campaign & correction but not after correction
        with freeze_time("2025-01-20"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
            diagnostic.teledeclare(applicant=UserFactory(), skip_validations=True)
        with freeze_time("2025-04-18"):  # during the 2024 correction campaign
            diagnostic.cancel()
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.CORRECTION)
            diagnostic.full_clean()  # should not raise
        with freeze_time("2025-08-30"):  # after the 2024 correction campaign
            self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_can_edit_status_submitted_validation(self):
        # SUBMITTED diagnostic can be edited during the campaign & correction but not after campaign
        with freeze_time("2025-01-20"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
            diagnostic.teledeclare(applicant=UserFactory(), skip_validations=True)
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.SUBMITTED)
            diagnostic.full_clean()  # should not raise
        with freeze_time("2025-04-18"):  # during the 2024 correction campaign
            diagnostic.full_clean()  # should not raise
        with freeze_time("2025-08-30"):  # after the 2024 correction campaign
            self.assertRaises(ValidationError, diagnostic.full_clean)

    @freeze_time("2026-01-30")  # during the 2025 campaign
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

    @freeze_time("2024-02-10")  # during the 2023 campaign
    def test_diagnostic_appro_fields_required_before_2024_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_SIMPLE_2024.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on full_clean
        diagnostic = DiagnosticFactory(valeur_totale=None, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
        diagnostic.full_clean()

    @freeze_time("2026-01-30")  # during the 2025 campaign
    def test_diagnostic_simple_appro_fields_required_after_2025_validation(self):
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on full_clean (simple & valeur_totale)
        diagnostic = DiagnosticFactory(valeur_totale=None, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025)
        diagnostic.full_clean()

    @freeze_time("2026-01-30")  # during the 2025 campaign
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

    @freeze_time("2026-01-30")  # during the 2025 campaign
    def test_diagnostic_valeur_totale_validation(self):
        # TODO: add tests against each simple field / sum of each label / sum of egalim fields
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE = VALID_DIAGNOSTIC_SIMPLE_2025.copy()
        VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE.pop("valeur_totale")
        # on save
        for VALEUR_TOTALE_VALUE_OK_ON_SAVE in [None, -1000, 0, 1000, Decimal("1234.56")]:
            with self.subTest(valeur_totale=VALEUR_TOTALE_VALUE_OK_ON_SAVE):
                diagnostic = DiagnosticFactory(
                    valeur_totale=VALEUR_TOTALE_VALUE_OK_ON_SAVE, **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE
                )
                self.assertEqual(diagnostic.valeur_totale, VALEUR_TOTALE_VALUE_OK_ON_SAVE)
        for VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE_VALUEERROR in [""]:
            with self.subTest(valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE_VALUEERROR):
                self.assertRaises(
                    (ValueError, ValidationError),
                    DiagnosticFactory,
                    valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE_VALUEERROR,
                    **VALID_DIAGNOSTIC_WITHOUT_VALEUR_TOTALE,
                )
        for VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE_TYPEERROR in ["  ", "invalid"]:
            with self.subTest(valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE_TYPEERROR):
                self.assertRaises(
                    (TypeError, ValidationError),
                    DiagnosticFactory,
                    valeur_totale=VALEUR_TOTALE_VALUE_NOT_OK_ON_SAVE_TYPEERROR,
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

    @freeze_time("2026-01-30")  # during the 2025 campaign
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

    @freeze_time("2026-01-30")  # during the 2025 campaign
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

    @freeze_time("2026-01-30")  # during the 2025 campaign
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


@freeze_time("2024-02-10")  # during the 2023 campaign
class Diagnostic2024ModelSaveTest(TransactionTestCase):
    def test_diagnostic_simple_2024_valid(self):
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024)
        diagnostic.full_clean()

    def test_diagnostic_simple_2024_valid_without_valeur_bio(self):
        # valeur_bio is optional
        VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_BIO = {**VALID_DIAGNOSTIC_SIMPLE_2024, "valeur_bio": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_BIO)
        diagnostic.full_clean()

    def test_diagnostic_simple_2024_not_valid_without_valeur_totale(self):
        # valeur_totale is required
        VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_TOTALE = {**VALID_DIAGNOSTIC_SIMPLE_2024, "valeur_totale": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2024_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_complete_2024_valid(self):
        VALID_DIAGNOSTIC_COMPLETE_2024 = {
            **VALID_DIAGNOSTIC_SIMPLE_2024,
            "diagnostic_type": Diagnostic.DiagnosticType.COMPLETE,
        }
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_COMPLETE_2024)
        diagnostic.full_clean()


@freeze_time("2026-01-30")  # during the 2025 campaign
class Diagnostic2025ModelSaveTest(TransactionTestCase):
    def test_diagnostic_simple_2025_valid(self):
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025)
        diagnostic.full_clean()

    def test_diagnostic_simple_2025_not_valid_without_appro_fields(self):
        # valeur_bio is required
        VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_BIO = {**VALID_DIAGNOSTIC_SIMPLE_2025, "valeur_bio": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_BIO)
        self.assertRaises(ValidationError, diagnostic.full_clean)
        # valeur_totale is required
        VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_TOTALE = {**VALID_DIAGNOSTIC_SIMPLE_2025, "valeur_totale": None}
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_SIMPLE_2025_WITHOUT_VALEUR_TOTALE)
        self.assertRaises(ValidationError, diagnostic.full_clean)

    def test_diagnostic_complete_2025_valid(self):
        # valid because DiagnosticFactory sets default values
        VALID_DIAGNOSTIC_COMPLETE_2025 = {
            **VALID_DIAGNOSTIC_SIMPLE_2025,
            "diagnostic_type": Diagnostic.DiagnosticType.COMPLETE,
        }
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_COMPLETE_2025)
        diagnostic.full_clean()

    def test_diagnostic_complete_2025_not_valid_without_appro_fields(self):
        # valeur_produits_de_la_mer is required
        VALID_DIAGNOSTIC_COMPLETE_2025_WITHOUT_VALEUR_PRODUITS_DE_LA_MER = {
            **VALID_DIAGNOSTIC_SIMPLE_2025,
            "diagnostic_type": Diagnostic.DiagnosticType.COMPLETE,
            "valeur_produits_de_la_mer": None,  # will be overridden by DiagnosticFactory
        }
        diagnostic = DiagnosticFactory(**VALID_DIAGNOSTIC_COMPLETE_2025_WITHOUT_VALEUR_PRODUITS_DE_LA_MER)
        diagnostic.valeur_produits_de_la_mer = None
        diagnostic.save()
        self.assertRaises(ValidationError, diagnostic.full_clean)


class DiagnosticQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_valid_1 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_valid_2 = CanteenFactory(siret=None, siren_unite_legale="123456789")
        cls.canteen_valid_3 = CanteenFactory(siret=None, siren_unite_legale="123456789")
        cls.canteen_valid_4 = CanteenFactory(siret="40419443300078")
        cls.canteen_valid_4.yearly_meal_count = 0  # not aberrant
        cls.canteen_valid_4.save(skip_validations=True)
        cls.canteen_valid_4.refresh_from_db()
        cls.canteen_valid_5 = CanteenFactory(siret="21340172201787")
        cls.canteen_valid_5.yearly_meal_count = None  # not aberrant
        cls.canteen_valid_5.save(skip_validations=True)
        cls.canteen_valid_5.refresh_from_db()
        cls.canteen_valid_sat = CanteenFactory(
            siret="21380185500015",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_valid_1,
        )
        cls.canteen_valid_6_armee = CanteenFactory(
            siret="21640122400011",
            line_ministry=Canteen.Ministries.ARMEE,
            sector_list=[Sector.ADMINISTRATION_ARMEE],
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        cls.canteen_missing_siret = CanteenFactory()
        cls.canteen_missing_siret.siret = ""  # missing data
        cls.canteen_missing_siret.save(skip_validations=True)
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
                diagnostic.teledeclare(applicant=UserFactory(), skip_validations=True)
            diagnostic_last_year = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data - 1,
                creation_date=date_in_last_teledeclaration_campaign,
                canteen=canteen,
                valeur_totale=1000.00,
                valeur_bio=200.00,
            )
            with freeze_time(date_in_last_teledeclaration_campaign):
                diagnostic_last_year.teledeclare(applicant=UserFactory(), skip_validations=True)
            setattr(cls, f"diagnostic_canteen_valid_{index + 1}", diagnostic)
            setattr(cls, f"diagnostic_last_year_canteen_valid_{index + 1}", diagnostic_last_year)

        cls.diagnostic_canteen_missing_siret = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_missing_siret,
            valeur_totale=1000.00,
            valeur_bio=200.00,
            invalid_reason_list=[Diagnostic.InvalidReason.CANTINE_SANS_SIRET_OU_SIREN],
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_missing_siret.teledeclare(applicant=UserFactory(), skip_validations=True)

        cls.diagnostic_canteen_meal_price_aberrant = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.canteen_meal_price_aberrant,
            valeur_totale=1000000.00,  # meal_price > 20
            valeur_bio=200.00,
            invalid_reason_list=[Diagnostic.InvalidReason.VALEURS_ABERRANTES],
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
            invalid_reason_list=[],
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
            invalid_reason_list=[Diagnostic.InvalidReason.VALEURS_ABERRANTES],
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
            invalid_reason_list=[Diagnostic.InvalidReason.CANTINE_SOFT_SUPPRIMEE_PENDANT_CAMPAGNE],
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.diagnostic_canteen_deleted.teledeclare(applicant=UserFactory())

    def test_canteen_soft_deleted_during_campaign_query(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.filter(canteen_soft_deleted_during_campaign_query(year_data))
        self.assertEqual(diagnostics.count(), 1)
        self.assertIn(self.diagnostic_canteen_deleted, diagnostics)

    def test_canteen_has_siret_or_siren_unite_legale_query(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.filter(canteen_has_siret_or_siren_unite_legale_query())
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
        diagnostics = Diagnostic.objects.valid_td_by_year(year_data - 1)
        self.assertEqual(diagnostics.count(), 6)
        self.assertIn(self.diagnostic_last_year_canteen_valid_1, diagnostics)  # groupe (but 2023)
        diagnostics = Diagnostic.objects.valid_td_by_year(year_data)
        self.assertEqual(diagnostics.count(), 8)
        self.assertIn(self.diagnostic_canteen_valid_1, diagnostics)  # groupe (and 2024)
        self.assertNotIn(self.diagnostic_canteen_missing_siret, diagnostics)  # canteen without siret/siren
        self.assertNotIn(self.diagnostic_canteen_deleted, diagnostics)  # canteen deleted during campaign

    def test_valid_td_site_by_year(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        self.assertEqual(Diagnostic.all_objects.count(), 17)  # we didn't generate 1TD1Site for now
        diagnostics = Diagnostic.all_objects.valid_td_site_by_year(year_data - 1)
        self.assertEqual(diagnostics.count(), 6)
        self.assertIn(self.diagnostic_last_year_canteen_valid_1, diagnostics)  # groupe (but 2023)
        diagnostics = Diagnostic.all_objects.valid_td_site_by_year(year_data)
        self.assertEqual(diagnostics.count(), 6)
        self.assertNotIn(self.diagnostic_canteen_valid_1, diagnostics)  # groupe (and 2024)  # difference
        self.assertNotIn(self.diagnostic_canteen_missing_siret, diagnostics)  # canteen without siret/siren
        self.assertNotIn(self.diagnostic_canteen_deleted, diagnostics)  # canteen deleted during campaign

    def test_valid_td_all_years(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.valid_td_all_years([year_data])
        self.assertEqual(diagnostics.count(), 8)
        diagnostics = Diagnostic.objects.valid_td_all_years([year_data - 1])
        self.assertEqual(diagnostics.count(), 6)
        diagnostics = Diagnostic.objects.valid_td_all_years([year_data, year_data - 1])
        self.assertEqual(diagnostics.count(), 8 + 6)

    def test_valid_td_site_all_years(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        self.assertEqual(Diagnostic.all_objects.count(), 17)  # we didn't generate 1TD1Site for now
        diagnostics = Diagnostic.all_objects.valid_td_site_all_years([year_data])
        self.assertEqual(diagnostics.count(), 6)  # difference
        diagnostics = Diagnostic.all_objects.valid_td_site_all_years([year_data - 1])
        self.assertEqual(diagnostics.count(), 6)
        diagnostics = Diagnostic.all_objects.valid_td_site_all_years([year_data, year_data - 1])
        self.assertEqual(diagnostics.count(), 6 + 6)

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
        self.assertEqual(Diagnostic.objects.publicly_visible().count(), 15)  # army excluded

    def test_with_appro_percent_stats(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        diagnostics = Diagnostic.objects.with_appro_percent_stats()
        self.assertEqual(diagnostics.count(), 17)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_4.id).pourcentage_bio, 20)
        self.assertEqual(diagnostics.get(id=self.diagnostic_canteen_valid_4.id).pourcentage_egalim, 50)

    def test_exclude_generated(self):
        self.assertEqual(Diagnostic.objects.count(), 17)
        DiagnosticFactory(generated_from_groupe_diagnostic=True)
        self.assertEqual(Diagnostic.objects.count(), 17)
        self.assertEqual(Diagnostic.all_objects.count(), 18)


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


class DiagnosticLabelFamilySumQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_simple = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            valeur_totale=1000,
            valeur_bio=200,
            valeur_bio_dont_commerce_equitable=50,
            valeur_viandes_volailles=100,
            valeur_viandes_volailles_egalim=50,
            valeur_viandes_volailles_france=20,
            valeur_autres_france=30,
        )
        cls.diagnostic_complete_1 = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_viandes_volailles_bio=10,
            valeur_viandes_volailles_bio_dont_commerce_equitable=5,
            valeur_viandes_volailles_label_rouge=7,
            valeur_viandes_volailles_france=20,
            valeur_produits_de_la_mer_bio=15,
            valeur_produits_de_la_mer_bio_dont_commerce_equitable=None,
            valeur_produits_de_la_mer_label_rouge=8,
            valeur_produits_de_la_mer_france=25,
        )
        cls.diagnostic_complete_2 = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_viandes_volailles_bio=10,
            valeur_viandes_volailles_bio_dont_commerce_equitable=None,
            valeur_viandes_volailles_label_rouge=7,
            valeur_viandes_volailles_france=20,
            valeur_produits_de_la_mer_bio=15,
            valeur_produits_de_la_mer_bio_dont_commerce_equitable=10,
            valeur_produits_de_la_mer_label_rouge=8,
            valeur_produits_de_la_mer_france=25,
        )

    def test_with_label_sum_queryset(self):
        diagnostic_qs = (
            Diagnostic.objects.with_label_sum("bio")
            .with_label_sum("bio_dont_commerce_equitable")
            .with_label_sum("label_rouge")
            .with_label_sum("france")
        )
        diagnostic_simple = diagnostic_qs.get(id=self.diagnostic_simple.id)
        self.assertEqual(diagnostic_simple.bio_sum, 0)
        self.assertEqual(diagnostic_simple.bio_dont_commerce_equitable_sum, 0)
        self.assertEqual(diagnostic_simple.label_rouge_sum, 0)
        self.assertEqual(diagnostic_simple.france_sum, 20 + 30)
        diagnostic_complete_1 = diagnostic_qs.get(id=self.diagnostic_complete_1.id)
        self.assertEqual(diagnostic_complete_1.bio_sum, 10 + 15)
        self.assertEqual(diagnostic_complete_1.bio_dont_commerce_equitable_sum, 5 + 0)
        self.assertEqual(diagnostic_complete_1.label_rouge_sum, 7 + 8)
        self.assertEqual(diagnostic_complete_1.france_sum, 20 + 25)
        diagnostic_complete_2 = diagnostic_qs.get(id=self.diagnostic_complete_2.id)
        self.assertEqual(diagnostic_complete_2.bio_sum, 10 + 15)
        self.assertEqual(diagnostic_complete_2.bio_dont_commerce_equitable_sum, 0 + 10)
        self.assertEqual(diagnostic_complete_2.label_rouge_sum, 7 + 8)
        self.assertEqual(diagnostic_complete_2.france_sum, 20 + 25)

    def test_label_sum_property(self):
        self.assertEqual(self.diagnostic_simple.label_sum("bio"), None)
        self.assertEqual(self.diagnostic_simple.label_sum("bio_dont_commerce_equitable"), None)
        self.assertEqual(self.diagnostic_simple.label_sum("label_rouge"), None)
        self.assertEqual(self.diagnostic_simple.label_sum("france"), 20 + 30)
        self.assertEqual(self.diagnostic_complete_1.label_sum("bio"), 10 + 15)
        self.assertEqual(self.diagnostic_complete_1.label_sum("bio_dont_commerce_equitable"), 5 + 0)
        self.assertEqual(self.diagnostic_complete_1.label_sum("label_rouge"), 7 + 8)
        self.assertEqual(self.diagnostic_complete_1.label_sum("france"), 20 + 25)
        self.assertEqual(self.diagnostic_complete_2.label_sum("bio"), 10 + 15)
        self.assertEqual(self.diagnostic_complete_2.label_sum("bio_dont_commerce_equitable"), 0 + 10)
        self.assertEqual(self.diagnostic_complete_2.label_sum("label_rouge"), 7 + 8)
        self.assertEqual(self.diagnostic_complete_2.label_sum("france"), 20 + 25)

    def test_with_family_sum_queryset(self):
        diagnostic_qs = Diagnostic.objects.with_family_sum("viandes_volailles").with_family_sum("produits_de_la_mer")
        diagnostic_simple = diagnostic_qs.get(id=self.diagnostic_simple.id)
        self.assertEqual(diagnostic_simple.viandes_volailles_sum, 0)
        self.assertEqual(diagnostic_simple.produits_de_la_mer_sum, 0)
        diagnostic_complete_1 = diagnostic_qs.get(id=self.diagnostic_complete_1.id)
        self.assertEqual(
            diagnostic_complete_1.viandes_volailles_sum, 10 + 7
        )  # bio_dont_commerce_equitable & france are not included
        self.assertEqual(diagnostic_complete_1.produits_de_la_mer_sum, 15 + 8)
        diagnostic_complete_2 = diagnostic_qs.get(id=self.diagnostic_complete_2.id)
        self.assertEqual(diagnostic_complete_2.viandes_volailles_sum, 10 + 7)
        self.assertEqual(diagnostic_complete_2.produits_de_la_mer_sum, 15 + 8)

    def test_family_sum_property(self):
        self.assertEqual(self.diagnostic_simple.family_sum("viandes_volailles"), 0)
        self.assertEqual(self.diagnostic_simple.family_sum("produits_de_la_mer"), 0)
        self.assertEqual(self.diagnostic_complete_1.family_sum("viandes_volailles"), 10 + 7)
        self.assertEqual(self.diagnostic_complete_1.family_sum("produits_de_la_mer"), 15 + 8)
        self.assertEqual(self.diagnostic_complete_2.family_sum("viandes_volailles"), 10 + 7)
        self.assertEqual(self.diagnostic_complete_2.family_sum("produits_de_la_mer"), 15 + 8)


class DiagnosticEgalimQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.TEST_CASES = [
            # (valeur_totale, valeur_*, pourcentage_*)
            (1000, 1000, 100),
            (1000, 200, 20),
            (1000, 0, 0),
            (0, 200, None),
            (0, 0, None),
            # TODO: with None input the behavior is sometimes different..
            # (1000, None, None),
            # (None, 200, None),
            # (None, None, None)
        ]

    def test_compute_pourcentage_bio_method(self):
        for valeur_totale, valeur_bio, pourcentage_bio in self.TEST_CASES:
            with self.subTest(valeur_totale=valeur_totale, valeur_bio=valeur_bio):
                diagnostic = DiagnosticFactory(
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                    valeur_totale=valeur_totale,
                    valeur_bio=valeur_bio,
                )
                self.assertEqual(diagnostic.valeur_bio_agg, valeur_bio)
                self.assertEqual(diagnostic.compute_pourcentage_bio(), pourcentage_bio)
                self.assertEqual(diagnostic.pourcentage_bio, pourcentage_bio)

    def test_compute_pourcentage_egalim_method(self):
        for valeur_totale, valeur_siqo, pourcentage_egalim in self.TEST_CASES:
            with self.subTest(valeur_totale=valeur_totale, valeur_siqo=valeur_siqo):
                diagnostic = DiagnosticFactory(
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                    valeur_totale=valeur_totale,
                    valeur_bio=0,
                    valeur_siqo=valeur_siqo,
                    valeur_externalites_performance=0,
                    valeur_egalim_autres=0,
                )
                self.assertEqual(diagnostic.valeur_egalim_agg, valeur_siqo)
                self.assertEqual(diagnostic.compute_pourcentage_egalim(), pourcentage_egalim)
                self.assertEqual(diagnostic.pourcentage_egalim, pourcentage_egalim)

    def test_compute_pourcentage_egalim_hors_bio_method(self):
        for valeur_totale, valeur_externalites_performance, pourcentage_egalim_hors_bio in self.TEST_CASES:
            with self.subTest(
                valeur_totale=valeur_totale, valeur_externalites_performance=valeur_externalites_performance
            ):
                diagnostic = DiagnosticFactory(
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                    valeur_totale=valeur_totale,
                    valeur_bio=1000,
                    valeur_siqo=0,
                    valeur_externalites_performance=valeur_externalites_performance,
                    valeur_egalim_autres=0,
                )
                self.assertEqual(diagnostic.valeur_egalim_hors_bio_agg, valeur_externalites_performance)
                self.assertEqual(diagnostic.compute_pourcentage_egalim_hors_bio(), pourcentage_egalim_hors_bio)
                self.assertEqual(diagnostic.pourcentage_egalim_hors_bio, pourcentage_egalim_hors_bio)

    def test_compute_objectifs_egalim_atteints_method(self):
        # see more tests in tests/test_utils.py::TestEgalimObjectives
        diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            valeur_totale=1000,
            valeur_bio=200,
            valeur_siqo=100,
            valeur_externalites_performance=100,
            valeur_egalim_autres=100,
        )
        self.assertEqual(diagnostic.pourcentage_bio, 20)
        self.assertEqual(diagnostic.pourcentage_egalim_hors_bio, 30)
        self.assertEqual(diagnostic.pourcentage_egalim, 20 + 30)
        self.assertTrue(diagnostic.compute_objectifs_egalim_atteints())
        self.assertTrue(diagnostic.objectifs_egalim_atteints)


class DiagnosticInvalidWarningQueriesTest(TestCase):
    def test_circuit_court_sup_france_query(self):
        diagnostic_complete = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_viandes_volailles_france=20,
            valeur_viandes_volailles_circuit_court=25,
        )

        diagnostic_qs = (
            Diagnostic.objects.with_label_sum("france")
            .with_label_sum("circuit_court")
            .filter(circuit_court_sup_france_query())
        )

        self.assertEqual(diagnostic_qs.count(), 1)
        self.assertIn(diagnostic_complete, diagnostic_qs)

    def test_local_sup_france_query(self):
        diagnostic_complete = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_produits_de_la_mer_france=25,
            valeur_produits_de_la_mer_local=30,
        )

        diagnostic_qs = (
            Diagnostic.objects.with_label_sum("france").with_label_sum("local").filter(local_sup_france_query())
        )

        self.assertEqual(diagnostic_qs.count(), 1)
        self.assertIn(diagnostic_complete, diagnostic_qs)

    def test_commerce_equitable_sup_bio_query(self):
        diagnostic_simple = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            valeur_bio=10,
            valeur_bio_dont_commerce_equitable=15,
        )
        diagnostic_complete = DiagnosticFactory(
            year=2025,
            canteen=CanteenFactory(),
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            valeur_viandes_volailles_bio=10,
            valeur_viandes_volailles_bio_dont_commerce_equitable=15,
        )

        diagnostic_qs = (
            Diagnostic.objects.with_label_sum("bio")
            .with_label_sum("bio_dont_commerce_equitable")
            .filter(commerce_equitable_sup_bio_query())
        )

        self.assertEqual(diagnostic_qs.count(), 2)
        self.assertIn(diagnostic_simple, diagnostic_qs)
        self.assertIn(diagnostic_complete, diagnostic_qs)


class DiagnosticModelDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen_site,
            year=year_data,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            valeur_totale=1000,
            valeur_bio=200,
        )

    def test_delete_canteen(self):
        self.assertIsNotNone(self.diagnostic.canteen)
        # soft delete
        self.canteen_site.delete()
        self.diagnostic.refresh_from_db()
        self.assertIsNotNone(self.diagnostic.canteen)
        # hard delete
        self.canteen_site.hard_delete()
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
