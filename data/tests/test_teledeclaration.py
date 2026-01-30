from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.timezone import now
from freezegun import freeze_time

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, Teledeclaration, Sector

year_data = 2024
date_in_teledeclaration_campaign = "2025-03-30"
date_in_correction_campaign = "2025-04-20"
date_in_last_teledeclaration_campaign = "2024-02-01"


class TeledeclarationQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_canteen_1 = CanteenFactory(siret="92341284500011", production_type=Canteen.ProductionType.CENTRAL)
        cls.valid_canteen_2 = CanteenFactory(siret=None, siren_unite_legale="123456789")
        cls.valid_canteen_3 = CanteenFactory(siret=None, siren_unite_legale="123456789")
        cls.valid_canteen_4 = CanteenFactory(siret="40419443300078")
        cls.valid_canteen_4.yearly_meal_count = 0  # not aberrant
        cls.valid_canteen_4.save(skip_validations=True)
        cls.valid_canteen_4.refresh_from_db()
        cls.valid_canteen_sat = CanteenFactory(
            siret="21380185500015",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.valid_canteen_1.siret,
        )
        cls.valid_canteen_5_armee = CanteenFactory(
            siret="21640122400011",
            line_ministry=Canteen.Ministries.ARMEE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.ADMINISTRATION_ARMEE],
        )
        cls.invalid_canteen = CanteenFactory(deletion_date=None)
        cls.invalid_canteen.siret = ""  # siret missing
        cls.invalid_canteen.save(skip_validations=True)
        cls.invalid_canteen.refresh_from_db()
        cls.deleted_canteen = CanteenFactory(
            siret="21730065600014",
            deletion_date=now().replace(month=3, day=1, year=2025),
        )

        for index, canteen in enumerate(
            [cls.valid_canteen_1, cls.valid_canteen_2, cls.valid_canteen_3, cls.valid_canteen_5_armee]
        ):
            diagnostic = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
                creation_date=date_in_teledeclaration_campaign,
                canteen=canteen,
                valeur_totale=1000.00,
                valeur_bio=200.00,
            )
            diagnostic_last_year = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data - 1,
                creation_date=date_in_last_teledeclaration_campaign,
                canteen=canteen,
                valeur_totale=1000.00,
                valeur_bio=200.00,
            )
            setattr(cls, f"valid_canteen_diagnostic_{index + 1}", diagnostic)
            with freeze_time(date_in_teledeclaration_campaign):
                teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, applicant=UserFactory())
            setattr(cls, f"valid_canteen_td_{index + 1}", teledeclaration)

            with freeze_time(date_in_last_teledeclaration_campaign):
                teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic_last_year, applicant=UserFactory())

        # Corrected TD
        cls.valid_canteen_diagnostic_correction = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=now().replace(month=7, day=1, year=2025),
            canteen=cls.valid_canteen_4,
            valeur_totale=1000.00,
            valeur_bio=200.00,
            valeur_siqo=100.00,
            valeur_externalites_performance=100.00,
            valeur_egalim_autres=100.00,
        )
        user_correction_campaign = UserFactory()
        cls.valid_correction_td = Teledeclaration.create_from_diagnostic(
            cls.valid_canteen_diagnostic_correction, applicant=user_correction_campaign
        )
        cls.valid_correction_td.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        cls.valid_correction_td.save()

        with freeze_time(date_in_correction_campaign):
            cls.valid_correction_td = Teledeclaration.create_from_diagnostic(
                cls.valid_canteen_diagnostic_correction, applicant=user_correction_campaign
            )

        cls.invalid_canteen_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.invalid_canteen,
            valeur_totale=1000.00,
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.invalid_canteen_td = Teledeclaration.create_from_diagnostic(
                cls.invalid_canteen_diagnostic, applicant=UserFactory()
            )

        cls.deleted_canteen_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.deleted_canteen,
            valeur_totale=1000.00,
            valeur_bio=200.00,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.deleted_canteen_td = Teledeclaration.create_from_diagnostic(
                cls.deleted_canteen_diagnostic, applicant=UserFactory()
            )
        cls.canteen_sat_diagnostic = DiagnosticFactory(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
            canteen=cls.valid_canteen_sat,
            valeur_totale=None,
            valeur_bio=None,
        )
        with freeze_time(date_in_teledeclaration_campaign):
            cls.canteen_sat_td = Teledeclaration.create_from_diagnostic(
                cls.canteen_sat_diagnostic, applicant=UserFactory()
            )
        cls.canteen_sat_td.teledeclaration_mode = Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        cls.canteen_sat_diagnostic.save()

    def test_submitted_for_year(self):
        teledeclarations = Teledeclaration.objects.submitted_for_year(year_data)
        self.assertEqual(teledeclarations.count(), 8)
        self.assertIn(self.valid_canteen_td_1, teledeclarations)
        self.assertIn(self.invalid_canteen_td, teledeclarations)
        self.assertIn(self.deleted_canteen_td, teledeclarations)
        teledeclarations = Teledeclaration.objects.submitted_for_year(year_data - 1)
        self.assertEqual(teledeclarations.count(), 4)

    def test_valid_td_by_year(self):
        teledeclarations = Teledeclaration.objects.valid_td_by_year(year_data)
        self.assertEqual(teledeclarations.count(), 5)
        self.assertIn(self.valid_canteen_td_1, teledeclarations)
        self.assertNotIn(self.invalid_canteen_td, teledeclarations)  # canteen without siret
        self.assertNotIn(self.deleted_canteen_td, teledeclarations)  # canteen deleted

    def test_historical_valid_td(self):
        teledeclarations = Teledeclaration.objects.historical_valid_td([year_data])
        self.assertEqual(teledeclarations.count(), 5)
        teledeclarations = Teledeclaration.objects.historical_valid_td([year_data - 1])
        self.assertEqual(teledeclarations.count(), 4)
        teledeclarations = Teledeclaration.objects.historical_valid_td([year_data, year_data - 1])
        self.assertEqual(teledeclarations.count(), 5 + 4)

    def test_meal_price(self):
        canteen_with_meal_price = Canteen.objects.get(siret="92341284500011")
        canteen_without_meal_price = Canteen.objects.get(siret="40419443300078")
        canteen_non_appro = Canteen.objects.get(siret="21380185500015")

        td_with_meal_price = Teledeclaration.objects.get(
            canteen=canteen_with_meal_price.id, status=Teledeclaration.TeledeclarationStatus.SUBMITTED, year=year_data
        )
        td_without_meal_price = Teledeclaration.objects.get(
            canteen=canteen_without_meal_price.id,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            year=year_data,
        )
        td_without_appro = Teledeclaration.objects.get(
            canteen=canteen_non_appro.id, status=Teledeclaration.TeledeclarationStatus.SUBMITTED, year=year_data
        )

        self.assertEqual(
            td_with_meal_price.meal_price,
            td_with_meal_price.value_total_ht / canteen_with_meal_price.yearly_meal_count,
        )
        self.assertIsNone(td_without_meal_price.meal_price)
        self.assertIsNone(td_without_appro.meal_price)

    def test_publicly_visible(self):
        self.assertEqual(Teledeclaration.objects.count(), 13)
        self.assertEqual(Teledeclaration.objects.publicly_visible().count(), 11)  # 2 belong to canteen_army

    def test_with_appro_percent_stats(self):
        teledeclarations = Teledeclaration.objects.with_appro_percent_stats()
        td_1 = teledeclarations.get(id=self.valid_correction_td.id)
        self.assertEqual(td_1.bio_percent, 20)
        self.assertEqual(td_1.egalim_percent, 50)


class TestTeledeclarationModelConstraintsTest(TestCase):
    @authenticate
    def test_diagnostic_deletion(self):
        """
        If the diagnostic used for the teledeclaration is deleted, the teledeclaration
        should be cancelled
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
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
        canteen = CanteenFactory()
        diagnostic = DiagnosticFactory(canteen=canteen)
        applicant = UserFactory()
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
        canteen = CanteenFactory()
        diagnostic = DiagnosticFactory(canteen=canteen)
        applicant = UserFactory()
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
        applicant = UserFactory()
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
