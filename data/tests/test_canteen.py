from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, PurchaseFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector, SectorCategory, Teledeclaration
from data.models.creation_source import CreationSource
from data.models.geo import Department, Region


class CanteenModelSaveTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_canteen_name_validation(self):
        for TUPLE_OK in [
            ("  ", "  "),
            (" canteen ", " canteen "),
            ("Cantéen", "Cantéen"),
            ("Canteen 123", "Canteen 123"),
            ("Canteen - A !@#$%^&*()", "Canteen - A !@#$%^&*()"),
        ]:
            with self.subTest(name=TUPLE_OK[0]):
                canteen = CanteenFactory(name=TUPLE_OK[0])
                self.assertEqual(canteen.name, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, ""]:
            with self.subTest(name=VALUE_NOT_OK):
                self.assertRaises(ValidationError, Canteen.objects.create, name=VALUE_NOT_OK)

    def test_canteen_siret_validation(self):
        for TUPLE_OK in [
            ("756 656 218 99905", "75665621899905"),
            ("75665621899905", "75665621899905"),
            (75665621899905, "75665621899905"),
        ]:
            with self.subTest(
                siret=TUPLE_OK[0],
            ):
                canteen = CanteenFactory(siret=TUPLE_OK[0], siren_unite_legale=None)
                self.assertEqual(canteen.siret, TUPLE_OK[1])
                canteen.delete()  # to avoid unique siret constraint
        for VALUE_NOT_OK in [None, "", "  ", "123", "923412845000115", "1234567890123A"]:
            with self.subTest(siret=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, siret=VALUE_NOT_OK, siren_unite_legale=None)

    def test_canteen_siren_unite_legale_validation(self):
        for TUPLE_OK in [
            ("756 656 218", "756656218"),
            ("756656218", "756656218"),
            (756656218, "756656218"),
        ]:
            with self.subTest(siren_unite_legale=TUPLE_OK):
                canteen = CanteenFactory(siret=None, siren_unite_legale=TUPLE_OK[0])
                self.assertEqual(canteen.siren_unite_legale, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", "  ", "123", "9234128450", "92341284A"]:
            with self.subTest(siren_unite_legale=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, siret=None, siren_unite_legale=VALUE_NOT_OK)

    def test_canteen_siret_or_siren_unite_legale_validation(self):
        for TUPLE_OK in [
            ("75665621899905", None),
            ("75665621899905", ""),
            (None, "756656218"),
            ("", "756656218"),
        ]:
            with self.subTest(siret=TUPLE_OK[0], siren_unite_legale=TUPLE_OK[1]):
                canteen = CanteenFactory(siret=TUPLE_OK[0], siren_unite_legale=TUPLE_OK[1])
                canteen.delete()  # to avoid unique siret constraint
                self.assertEqual(canteen.siret, TUPLE_OK[0])
                self.assertEqual(canteen.siren_unite_legale, TUPLE_OK[1])
        for TUPLE_NOT_OK in [
            ("75665621899905", "756656218"),
            ("75665621899905", "756 656 218"),
            ("", ""),
            (None, None),
            ("", None),
            (None, ""),
        ]:
            with self.subTest(siret=TUPLE_NOT_OK[0], siren_unite_legale=TUPLE_NOT_OK[1]):
                self.assertRaises(
                    ValidationError,
                    CanteenFactory,
                    siret=TUPLE_NOT_OK[0],
                    siren_unite_legale=TUPLE_NOT_OK[1],
                )

    def test_canteen_siret_required_if_central_validation(self):
        for production_type in [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]:
            for TUPLE_NOT_OK in [
                ("", "756656218"),
                (None, "756656218"),
            ]:
                with self.subTest(
                    production_type=production_type,
                    siret=TUPLE_NOT_OK[0],
                    siren_unite_legale=TUPLE_NOT_OK[1],
                ):
                    self.assertRaises(
                        ValidationError,
                        CanteenFactory,
                        production_type=production_type,
                        siret=TUPLE_NOT_OK[0],
                        siren_unite_legale=TUPLE_NOT_OK[1],
                    )

    def test_canteen_siret_unique_validation(self):
        central_kitchen = CanteenFactory(siret="21590350100017", production_type=Canteen.ProductionType.CENTRAL)
        canteen_existing = CanteenFactory(siret="75665621899905", siren_unite_legale=None)
        # on create
        for VALUE_NOT_OK in ["75665621899905", "756 656 218 99905", 75665621899905]:
            with self.subTest(siret=VALUE_NOT_OK):
                self.assertRaises(
                    ValidationError,
                    CanteenFactory,
                    siret=VALUE_NOT_OK,
                    siren_unite_legale=None,
                )
        # on update
        central_kitchen.siret = canteen_existing.siret
        self.assertRaises(ValidationError, central_kitchen.save)

    def test_canteen_epci_validation(self):
        for TUPLE_OK in [(None, None), ("", ""), ("  ", ""), ("756 656 218", "756656218"), ("756656218", "756656218")]:
            with self.subTest(epci=TUPLE_OK[0]):
                canteen = CanteenFactory(epci=TUPLE_OK[0])
                self.assertEqual(canteen.epci, TUPLE_OK[1])
        for VALUE_NOT_OK in ["123", "9234128450", "92341284A"]:
            with self.subTest(epci=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, epci=VALUE_NOT_OK)

    def test_canteen_department_validation(self):
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Department.values)]:
            with self.subTest(department=TUPLE_OK[0]):
                canteen = CanteenFactory(department=TUPLE_OK[0])
                self.assertEqual(canteen.department, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123", "999", "2a", "2C"]:
            with self.subTest(department=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, department=VALUE_NOT_OK)

    def test_canteen_region_validation(self):
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Region.values)]:
            with self.subTest(region=TUPLE_OK[0]):
                canteen = CanteenFactory(region=TUPLE_OK[0])
                self.assertEqual(canteen.region, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123", "999"]:
            with self.subTest(region=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, region=VALUE_NOT_OK)

    def test_canteen_daily_meal_count_validation(self):
        for TUPLE_OK in [(3, 3), (50, 50), ("123", 123), (10.5, 10)]:
            with self.subTest(daily_meal_count=TUPLE_OK[0]):
                canteen = CanteenFactory(daily_meal_count=TUPLE_OK[0], yearly_meal_count=1000)
                self.assertEqual(canteen.daily_meal_count, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", 0, -1, -100, 2, "10.5", "10,5", "invalid"]:
            with self.subTest(daily_meal_count=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, daily_meal_count=VALUE_NOT_OK)

    def test_canteen_yearly_meal_count_validation(self):
        for TUPLE_OK in [(420, 420), ("1234", 1234), (1234.5, 1234)]:
            with self.subTest(yearly_meal_count=TUPLE_OK[0]):
                canteen = CanteenFactory(daily_meal_count=10, yearly_meal_count=TUPLE_OK[0])
                self.assertEqual(canteen.yearly_meal_count, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", 0, -1, -100, 419, "1234.5", "1234,5", "invalid"]:
            with self.subTest(yearly_meal_count=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, yearly_meal_count=VALUE_NOT_OK)

    def test_canteen_daily_less_than_yearly_meal_count_validation(self):
        for TUPLE_OK in [(3, 420)]:
            with self.subTest(daily_meal_count=TUPLE_OK[0], yearly_meal_count=TUPLE_OK[1]):
                canteen = CanteenFactory(daily_meal_count=TUPLE_OK[0], yearly_meal_count=TUPLE_OK[1])
                self.assertEqual(canteen.daily_meal_count, TUPLE_OK[0])
                self.assertEqual(canteen.yearly_meal_count, TUPLE_OK[1])
        for TUPLE_NOT_OK in [(1000, 1000), (1001, 1000)]:
            with self.subTest(daily_meal_count=TUPLE_NOT_OK[0], yearly_meal_count=TUPLE_NOT_OK[1]):
                self.assertRaises(
                    ValidationError,
                    CanteenFactory,
                    daily_meal_count=TUPLE_NOT_OK[0],
                    yearly_meal_count=TUPLE_NOT_OK[1],
                )

    def test_canteen_management_type_validation(self):
        for TUPLE_OK in [(key, key) for key in Canteen.ManagementType.values]:
            with self.subTest(management_type=TUPLE_OK[0]):
                canteen = CanteenFactory(management_type=TUPLE_OK[0])
                self.assertEqual(canteen.management_type, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", "  ", 123, "invalid"]:
            with self.subTest(management_type=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, management_type=VALUE_NOT_OK)

    def test_canteen_production_type_validation(self):
        for TUPLE_OK in [(key, key) for key in Canteen.ProductionType.values]:
            with self.subTest(production_type=TUPLE_OK[0]):
                canteen = CanteenFactory(production_type=TUPLE_OK[0])
                self.assertEqual(canteen.production_type, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", "  ", 123, "invalid"]:
            with self.subTest(production_type=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, production_type=VALUE_NOT_OK)

    def test_canteen_economic_model_validation(self):
        # groupe: must be empty
        for production_type in [Canteen.ProductionType.GROUPE]:
            for TUPLE_OK in [(None, None), ("", "")]:
                with self.subTest(
                    siren_unite_legale="756656218", production_type=production_type, economic_model=TUPLE_OK[0]
                ):
                    canteen = CanteenFactory(production_type=production_type, economic_model=TUPLE_OK[0])
                    self.assertEqual(canteen.economic_model, TUPLE_OK[1])
            for VALUE_NOT_OK in [key for key, _ in Canteen.EconomicModel.choices]:
                with self.subTest(production_type=production_type, economic_model=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError,
                        CanteenFactory,
                        production_type=production_type,
                        economic_model=VALUE_NOT_OK,
                    )
        for production_type in [
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
            Canteen.ProductionType.ON_SITE_CENTRAL,
        ]:
            for TUPLE_OK in [(key, key) for key in Canteen.EconomicModel.values]:
                with self.subTest(economic_model=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, economic_model=TUPLE_OK[0])
                    self.assertEqual(canteen.economic_model, TUPLE_OK[1])
            for VALUE_NOT_OK in [None, "", "  ", 123, "invalid"]:
                with self.subTest(economic_model=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError, CanteenFactory, production_type=production_type, economic_model=VALUE_NOT_OK
                    )

    def test_canteen_sector_list_validation(self):
        # central kitchen: must be empty
        for production_type in [Canteen.ProductionType.CENTRAL]:
            for TUPLE_OK in [([], [])]:
                with self.subTest(production_type=production_type, sector_list=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, sector_list=TUPLE_OK[0])
                    self.assertEqual(canteen.sector_list, TUPLE_OK[1])
            for VALUE_NOT_OK in [None]:
                with self.subTest(production_type=production_type, sector_list=VALUE_NOT_OK):
                    self.assertRaises(
                        IntegrityError, CanteenFactory, production_type=production_type, sector_list=VALUE_NOT_OK
                    )
            for VALUE_NOT_OK in [[Sector.EDUCATION_PRIMAIRE], [999], ["invalid"], [Sector.EDUCATION_PRIMAIRE, 999]]:
                with self.subTest(production_type=production_type, sector_list=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError, CanteenFactory, production_type=production_type, sector_list=VALUE_NOT_OK
                    )
        # other types: must be filled, between 1 & 3
        for production_type in [
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
            Canteen.ProductionType.ON_SITE_CENTRAL,
        ]:
            for TUPLE_OK in [
                ([Sector.EDUCATION_PRIMAIRE], [Sector.EDUCATION_PRIMAIRE]),
                (
                    [Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL],
                    [Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL],
                ),
                (
                    [Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL, Sector.ENTERPRISE_ENTREPRISE],
                    [Sector.EDUCATION_PRIMAIRE, Sector.SANTE_HOPITAL, Sector.ENTERPRISE_ENTREPRISE],
                ),
            ]:
                with self.subTest(production_type=production_type, sector_list=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, sector_list=TUPLE_OK[0])
                    self.assertEqual(canteen.sector_list, TUPLE_OK[1])
            for VALUE_NOT_OK in [None]:
                with self.subTest(production_type=production_type, sector_list=VALUE_NOT_OK):
                    self.assertRaises(
                        IntegrityError, CanteenFactory, production_type=production_type, sector_list=VALUE_NOT_OK
                    )
            for VALUE_NOT_OK in [
                [],
                [
                    Sector.EDUCATION_PRIMAIRE,
                    Sector.SANTE_HOPITAL,
                    Sector.ENTERPRISE_ENTREPRISE,
                    Sector.ADMINISTRATION_ADMINISTRATIF,
                ],
                [999],
                ["invalid"],
                [Sector.EDUCATION_PRIMAIRE, 999],
            ]:
                with self.subTest(production_type=production_type, sector_list=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError, CanteenFactory, production_type=production_type, sector_list=VALUE_NOT_OK
                    )

    def test_canteen_line_ministry_validation(self):
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Canteen.Ministries.values)]:
            with self.subTest(line_ministry=TUPLE_OK[0]):
                canteen = CanteenFactory(line_ministry=TUPLE_OK[0])
                self.assertEqual(canteen.line_ministry, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid"]:
            with self.subTest(line_ministry=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, line_ministry=VALUE_NOT_OK)

    def test_canteen_satellite_canteens_count_validation(self):
        # central kitchen: must be filled
        for production_type in [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]:
            for TUPLE_OK in [(1, 1), (1000, 1000), ("123", 123), (10.5, 10)]:
                with self.subTest(production_type=production_type, satellite_canteens_count=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, satellite_canteens_count=TUPLE_OK[0])
                    self.assertEqual(canteen.satellite_canteens_count, TUPLE_OK[1])
            for VALUE_NOT_OK in [None, "", 0, -1, -100, "10.5", "10,5", "invalid"]:
                with self.subTest(production_type=production_type, satellite_canteens_count=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError,
                        CanteenFactory,
                        production_type=production_type,
                        satellite_canteens_count=VALUE_NOT_OK,
                    )
        for production_type in [Canteen.ProductionType.ON_SITE, Canteen.ProductionType.ON_SITE_CENTRAL]:
            for TUPLE_OK in [(None, None)]:
                with self.subTest(production_type=production_type, satellite_canteens_count=TUPLE_OK[0]):
                    canteen = CanteenFactory(
                        production_type=production_type,
                        satellite_canteens_count=TUPLE_OK[0],
                    )
                    self.assertEqual(canteen.satellite_canteens_count, TUPLE_OK[1])
            for VALUE_NOT_OK in [0, -1, -100, "10.5", "10,5", "invalid", 5, "5"]:
                with self.subTest(production_type=production_type, satellite_canteens_count=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError,
                        CanteenFactory,
                        production_type=production_type,
                        satellite_canteens_count=VALUE_NOT_OK,
                    )

    def test_canteen_central_producer_siret_validation(self):
        central_kitchen = CanteenFactory(siret="21590350100017", production_type=Canteen.ProductionType.CENTRAL)
        canteen_site = CanteenFactory(siret="83014132100034", production_type=Canteen.ProductionType.ON_SITE)

        for production_type in [Canteen.ProductionType.GROUPE, Canteen.ProductionType.ON_SITE_CENTRAL]:
            for TUPLE_OK in [
                ("215 903 501 00017", central_kitchen.siret),
                (central_kitchen.siret, central_kitchen.siret),
                (int(central_kitchen.siret), central_kitchen.siret),
                ("75665621899905", "75665621899905"),
            ]:
                with self.subTest(
                    production_type=production_type,
                    central_producer_siret=TUPLE_OK[0],
                ):
                    canteen = CanteenFactory(production_type=production_type, central_producer_siret=TUPLE_OK[0])
                    self.assertEqual(canteen.central_producer_siret, TUPLE_OK[1])
            # the canteen's central_producer_siret cannot be the canteen's own siret
            self.assertRaises(
                ValidationError,
                CanteenFactory,
                siret="21380185500015",
                production_type=production_type,
                central_producer_siret="21380185500015",
            )
        for production_type in Canteen.ProductionType.values:
            for TUPLE_OK in [(None, None), ("", "")]:
                with self.subTest(
                    production_type=production_type,
                    central_producer_siret=TUPLE_OK[0],
                ):
                    canteen = CanteenFactory(production_type=production_type, central_producer_siret=TUPLE_OK[0])
                    self.assertEqual(canteen.central_producer_siret, TUPLE_OK[1])
        for production_type in [
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
        ]:
            for VALUE_NOT_OK in [
                "215 903 501 00017",
                central_kitchen.siret,
                int(central_kitchen.siret),
                canteen_site.siret,
                "75665621899905",
            ]:
                with self.subTest(
                    production_type=production_type,
                    siret=VALUE_NOT_OK,
                ):
                    self.assertRaises(
                        ValidationError,
                        CanteenFactory,
                        production_type=production_type,
                        central_producer_siret=VALUE_NOT_OK,
                    )

    def test_canteen_creation_source_validation(self):
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in CreationSource.values)]:
            with self.subTest(creation_source=TUPLE_OK[0]):
                canteen = CanteenFactory(creation_source=TUPLE_OK[0])
                self.assertEqual(canteen.creation_source, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid"]:
            with self.subTest(creation_source=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, creation_source=VALUE_NOT_OK)


class CanteenQuerySetTest(TestCase):
    def test_soft_delete_canteen(self):
        """
        The delete method should "soft delete" a canteen and have it hidden by default
        from querysets, unless specifically asked for
        """
        canteen = CanteenFactory()
        canteen.delete()
        qs = Canteen.objects.all()
        self.assertEqual(qs.count(), 0, "Soft deleted canteen is not visible in default queryset")
        qs = Canteen.all_objects.all()
        self.assertEqual(qs.count(), 1, "Soft deleted canteens can be accessed in custom queryset")


class CanteenVisibleQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory(line_ministry=None)
        cls.canteen_armee = CanteenFactory(line_ministry=Canteen.Ministries.ARMEE)

    def test_publicly_visible_queryset(self):
        self.assertEqual(Canteen.objects.count(), 2)
        qs = Canteen.objects.publicly_visible()
        self.assertEqual(qs.count(), 1)
        self.assertTrue(self.canteen_armee not in qs)

    def test_publicly_hidden_queryset(self):
        self.assertEqual(Canteen.objects.count(), 2)
        qs = Canteen.objects.publicly_hidden()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.canteen_armee)

    def test_publication_status_display_to_public_property(self):
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(self.canteen.publication_status_display_to_public, "published")
        self.assertEqual(self.canteen_armee.publication_status_display_to_public, "draft")


class CanteenCreatedBeforeQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        with freeze_time("2025-01-01"):  # before the 2024 campaign
            CanteenFactory()
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            CanteenFactory()
        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            CanteenFactory()
        with freeze_time("2025-06-30"):  # after the 2024 campaign
            CanteenFactory()

    def test_created_before_year_campaign_end_date(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(Canteen.objects.created_before_year_campaign_end_date(1990).count(), 0)
        self.assertEqual(Canteen.objects.created_before_year_campaign_end_date(2023).count(), 0)
        self.assertEqual(Canteen.objects.created_before_year_campaign_end_date(2024).count(), 2)
        self.assertEqual(Canteen.objects.created_before_year_campaign_end_date(2025).count(), 4)


class CanteenCentralAndSatelliteQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(
            siren_unite_legale="756656218", production_type=Canteen.ProductionType.GROUPE, economic_model=None
        )
        cls.canteen_central_1 = CanteenFactory(
            siret="21340172201787",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=2,
            sector_list=[],
        )  # 1 missing
        cls.canteen_central_2 = CanteenFactory(
            siret="21380185500015", production_type=Canteen.ProductionType.CENTRAL, satellite_canteens_count=2
        )
        cls.canteen_on_site_central_1 = CanteenFactory(
            siret="92341284500011",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_1.siret,
        )
        cls.canteen_on_site_central_2 = CanteenFactory(
            siret="40419443300078",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_2.siret,
        )
        cls.canteen_on_site_central_3 = CanteenFactory(
            siret="83014132100034",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_2.siret,
        )
        cls.canteen_central_serving_1 = CanteenFactory(
            siret="11007001800012",
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
        )

    def test_is_groupe(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(Canteen.objects.is_groupe().count(), 1)
        self.assertTrue(self.canteen_groupe.is_groupe)

    def test_is_central(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(Canteen.objects.is_central().count(), 2)
        self.assertTrue(self.canteen_central_1.is_central)

    def test_is_satellite(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(Canteen.objects.is_satellite().count(), 3)
        self.assertTrue(self.canteen_on_site_central_1.is_satellite)

    def test_annotate_with_central_kitchen_id(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(
            Canteen.objects.annotate_with_central_kitchen_id()
            .get(id=self.canteen_on_site_central_1.id)
            .central_kitchen_id,
            self.canteen_central_1.id,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_central_kitchen_id()
            .get(id=self.canteen_on_site_central_2.id)
            .central_kitchen_id,
            self.canteen_central_2.id,
        )
        self.assertIsNone(
            Canteen.objects.annotate_with_central_kitchen_id().get(id=self.canteen_central_1.id).central_kitchen_id
        )

    def test_get_satellites(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(Canteen.objects.get_satellites(self.canteen_central_1.siret).count(), 1)
        self.assertEqual(Canteen.objects.get_satellites(self.canteen_central_2.siret).count(), 2)

    def test_annotate_with_satellites_in_db_count(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .get(id=self.canteen_central_1.id)
            .satellites_in_db_count,
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .get(id=self.canteen_central_2.id)
            .satellites_in_db_count,
            2,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .get(id=self.canteen_on_site_central_1.id)
            .satellites_in_db_count,
            0,
        )


class CanteenPurchaseQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        canteen_with_purchases = CanteenFactory()
        CanteenFactory()
        PurchaseFactory(canteen=canteen_with_purchases, date="2024-01-01")
        PurchaseFactory(canteen=canteen_with_purchases, date="2023-01-01")

    def test_annotate_with_purchases_for_year(self):
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.annotate_with_purchases_for_year(2024).filter(has_purchases_for_year=True).count(), 1
        )
        self.assertEqual(
            Canteen.objects.annotate_with_purchases_for_year(2023).filter(has_purchases_for_year=True).count(), 1
        )
        self.assertEqual(
            Canteen.objects.annotate_with_purchases_for_year(2022).filter(has_purchases_for_year=True).count(), 0
        )


class CanteenDiagnosticTeledeclarationQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CanteenFactory()
        canteen_with_diagnostic_teledeclared = CanteenFactory()
        canteen_with_diagnostic_cancelled = CanteenFactory()
        cls.diagnostic_filled_teledeclared = DiagnosticFactory(
            canteen=canteen_with_diagnostic_teledeclared,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            valeur_totale=1000,
        )
        cls.diagnostic_filled_cancelled = DiagnosticFactory(
            canteen=canteen_with_diagnostic_cancelled,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            valeur_totale=1000,
        )
        cls.diagnostic_not_filled = DiagnosticFactory(
            canteen=canteen_with_diagnostic_teledeclared,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2023,
            valeur_totale=None,
        )  # missing data
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            cls.diagnostic_filled_teledeclared.teledeclare(applicant=UserFactory())
            cls.diagnostic_filled_cancelled.teledeclare(applicant=UserFactory())
            cls.diagnostic_filled_cancelled.cancel()

    def test_annotate_with_diagnostic_for_year(self):
        self.assertEqual(Canteen.objects.count(), 3)
        # diagnostic_for_year
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2024).filter(diagnostic_for_year__isnull=False).count(),
            2,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2023).filter(diagnostic_for_year__isnull=False).count(),
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2022).filter(diagnostic_for_year__isnull=False).count(),
            0,
        )
        # has_diagnostic_filled_for_year
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2024)
            .filter(has_diagnostic_filled_for_year=True)
            .count(),
            2,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2023)
            .filter(has_diagnostic_filled_for_year=True)
            .count(),
            0,  # missing data
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2022)
            .filter(has_diagnostic_filled_for_year=True)
            .count(),
            0,
        )
        # TODO: diagnostic_for_year_cc_mode
        # has_diagnostic_teledeclared_for_year
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2024)
            .filter(has_diagnostic_teledeclared_for_year=True)
            .count(),
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2023)
            .filter(has_diagnostic_teledeclared_for_year=True)
            .count(),
            0,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2022)
            .filter(has_diagnostic_teledeclared_for_year=True)
            .count(),
            0,
        )


class CanteenSiretOrSirenUniteLegaleQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_siret_1 = CanteenFactory(siret="21590350100017", siren_unite_legale="")  # OK
        cls.canteen_siret_2 = CanteenFactory(siret="21010034300016", siren_unite_legale=None)  # OK
        cls.canteen_siren_1 = CanteenFactory(siret="", siren_unite_legale="756656218")  # OK
        cls.canteen_siren_2 = CanteenFactory(siret=None, siren_unite_legale="756656218")  # OK
        cls.canteen_none_1 = CanteenFactory()
        cls.canteen_none_2 = CanteenFactory()
        Canteen.objects.filter(id=cls.canteen_none_1.id).update(siret="")
        cls.canteen_none_1.refresh_from_db()
        Canteen.objects.filter(id=cls.canteen_none_2.id).update(siret=None, siren_unite_legale="")
        cls.canteen_none_2.refresh_from_db()

    def has_siret_or_siren_unite_legale_queryset(self):
        self.assertEqual(Canteen.objects.count(), 7)
        self.assertEqual(Canteen.objects.has_siret_or_siren_unite_legale().count(), 4)

    def test_siret_or_siren_unite_legale_property(self):
        self.assertEqual(self.canteen_siret_1.siret_or_siren_unite_legale, "21590350100017")
        self.assertEqual(self.canteen_siret_2.siret_or_siren_unite_legale, "21010034300016")
        for canteen in [self.canteen_siren_1, self.canteen_siren_2]:
            self.assertEqual(canteen.siret_or_siren_unite_legale, "756656218")
        for canteen in [self.canteen_none_1, self.canteen_none_2]:
            self.assertEqual(canteen.siret_or_siren_unite_legale, "")


class CanteenLineMinistryAndSectorAndSPEQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(
            siret="21340172201787",
            production_type=Canteen.ProductionType.CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            satellite_canteens_count=2,
            sector_list=[],
        )
        cls.canteen_central_serving = CanteenFactory(
            siret="11007001800012",
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[
                Sector.EDUCATION_SECONDAIRE_COLLEGE,
                Sector.EDUCATION_SECONDAIRE_LYCEE,
                Sector.ENTERPRISE_ENTREPRISE,
            ],
        )
        cls.canteen_satellite_spe = CanteenFactory(
            siret="92341284500011",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            central_producer_siret=cls.canteen_central.siret,
            sector_list=[Sector.ADMINISTRATION_ETABLISSEMENT_PUBLIC],
            line_ministry=Canteen.Ministries.CULTURE,
        )
        cls.canteen_private = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PRIVATE,
            central_producer_siret=cls.canteen_central.siret,
            sector_list=[Sector.ADMINISTRATION_ETABLISSEMENT_PUBLIC],
            line_ministry=None,
        )

    def test_is_public_queryset(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(Canteen.objects.is_public().count(), 3)
        self.assertFalse(self.canteen_private in Canteen.objects.is_public())

    def test_is_public_property(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertTrue(self.canteen_central.is_public)
        self.assertTrue(self.canteen_central_serving.is_public)
        self.assertTrue(self.canteen_satellite_spe.is_public)
        self.assertFalse(self.canteen_private.is_public)

    def test_annotate_with_requires_line_ministry_queryset(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertFalse(
            Canteen.objects.annotate_with_requires_line_ministry()
            .get(id=self.canteen_central.id)
            .requires_line_ministry
        )
        self.assertFalse(
            Canteen.objects.annotate_with_requires_line_ministry()
            .get(id=self.canteen_central_serving.id)
            .requires_line_ministry
        )
        self.assertTrue(
            Canteen.objects.annotate_with_requires_line_ministry()
            .get(id=self.canteen_satellite_spe.id)
            .requires_line_ministry
        )
        self.assertFalse(
            Canteen.objects.annotate_with_requires_line_ministry()
            .get(id=self.canteen_private.id)
            .requires_line_ministry
        )
        # change economic_model to public
        self.canteen_private.economic_model = Canteen.EconomicModel.PUBLIC
        self.canteen_private.save()
        self.assertTrue(
            Canteen.objects.annotate_with_requires_line_ministry()
            .get(id=self.canteen_private.id)
            .requires_line_ministry
        )

    def test_annotate_with_sector_list_count_queryset(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(
            Canteen.objects.annotate_with_sector_list_count().get(id=self.canteen_central.id).sector_list_count,
            0,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_sector_list_count()
            .get(id=self.canteen_central_serving.id)
            .sector_list_count,
            3,
        )

    def test_annotate_with_sector_category_list_queryset(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(
            Canteen.objects.annotate_with_sector_category_list().get(id=self.canteen_central.id).sector_category_list,
            [],
        )
        self.assertEqual(
            len(
                Canteen.objects.annotate_with_sector_category_list()
                .get(id=self.canteen_central_serving.id)
                .sector_category_list
            ),
            2,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_sector_category_list()
            .get(id=self.canteen_satellite_spe.id)
            .sector_category_list,
            [SectorCategory.ADMINISTRATION.value],
        )

    def test_category_list_from_sector_list_property(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(self.canteen_central.category_list_from_sector_list, [])
        self.assertEqual(len(self.canteen_central_serving.category_list_from_sector_list), 2)
        self.assertEqual(self.canteen_satellite_spe.category_list_from_sector_list, [SectorCategory.ADMINISTRATION])
        self.assertEqual(self.canteen_private.category_list_from_sector_list, [SectorCategory.ADMINISTRATION])

    def test_is_spe_property(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertFalse(self.canteen_central.is_spe)
        self.assertFalse(self.canteen_central_serving.is_spe)
        self.assertTrue(self.canteen_satellite_spe.is_spe)
        self.assertFalse(self.canteen_private.is_spe)


class CanteenCompleteQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(
            siret="21590350100017",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=1,
        )
        cls.canteen_central_incomplete = CanteenFactory(
            siret="21010034300016",
            production_type=Canteen.ProductionType.CENTRAL,
            # satellite_canteens_count=0,  # incomplete
        )
        Canteen.objects.filter(id=cls.canteen_central_incomplete.id).update(satellite_canteens_count=0)  # incomplete
        cls.canteen_central_incomplete.refresh_from_db()
        cls.canteen_central_serving = CanteenFactory(
            siret="21340172201787",
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            satellite_canteens_count=1,
        )
        cls.canteen_central_serving_incomplete = CanteenFactory(
            # siret=None,  # incomplete
            siren_unite_legale=None,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            satellite_canteens_count=1,
        )
        Canteen.objects.filter(id=cls.canteen_central_serving_incomplete.id).update(siret=None)  # incomplete
        cls.canteen_central_serving_incomplete.refresh_from_db()
        cls.canteen_on_site = CanteenFactory(
            siret=None,
            siren_unite_legale="967669103",  # complete
            production_type=Canteen.ProductionType.ON_SITE,
        )
        cls.canteen_on_site_incomplete_1 = CanteenFactory(
            siret="21380185500015",
            production_type=Canteen.ProductionType.ON_SITE,
            # daily_meal_count=12,
        )
        Canteen.objects.filter(id=cls.canteen_on_site_incomplete_1.id).update(daily_meal_count=0)  # incomplete
        cls.canteen_on_site_incomplete_1.refresh_from_db()
        cls.canteen_on_site_incomplete_2 = CanteenFactory(
            siret="21670482500019",
            production_type=Canteen.ProductionType.ON_SITE,
            # sector_list=[],  # incomplete
        )
        Canteen.objects.filter(id=cls.canteen_on_site_incomplete_2.id).update(sector_list=[])  # incomplete
        cls.canteen_on_site_incomplete_2.refresh_from_db()
        cls.canteen_on_site_incomplete_3 = CanteenFactory(
            siret="21640122400011",
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.ADMINISTRATION_PRISON],
            line_ministry=None,  # incomplete
        )
        cls.canteen_on_site_central_1 = CanteenFactory(
            siret="21630113500010",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.canteen_on_site_central_2 = CanteenFactory(
            siret="21130055300016",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_serving.siret,
        )
        cls.canteen_on_site_central_incomplete = CanteenFactory(
            siret="21730065600014",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            daily_meal_count=12,
            central_producer_siret=cls.canteen_central_serving.siret,
        )
        Canteen.objects.filter(id=cls.canteen_on_site_central_incomplete.id).update(
            central_producer_siret=None
        )  # incomplete
        cls.canteen_on_site_central_incomplete.refresh_from_db()
        cls.canteen_filled_list = [
            cls.canteen_central,
            cls.canteen_central_serving,
            cls.canteen_on_site,
            cls.canteen_on_site_central_1,
            cls.canteen_on_site_central_2,
        ]
        cls.canteen_missing_data_list = [
            cls.canteen_central_incomplete,
            cls.canteen_central_serving_incomplete,
            cls.canteen_on_site_incomplete_1,
            cls.canteen_on_site_incomplete_2,
            cls.canteen_on_site_incomplete_3,
            cls.canteen_on_site_central_incomplete,
        ]

    def test_filled_queryset(self):
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.objects.filled().count(), len(self.canteen_filled_list))

    def test_is_filled_property(self):
        for index, canteen in enumerate(self.canteen_filled_list):
            with self.subTest(index=index, canteen=canteen):
                self.assertTrue(canteen.is_filled)
        for index, canteen in enumerate(self.canteen_missing_data_list):
            with self.subTest(index=index, canteen=canteen):
                self.assertFalse(canteen.is_filled)

    def test_has_missing_data_queryset(self):
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.objects.has_missing_data().count(), len(self.canteen_missing_data_list))


class CanteenAggregateQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(
            siret="21590350100017",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            satellite_canteens_count=1,
            sector_list=[],
        )
        cls.canteen_central_serving = CanteenFactory(
            siret="21010034300016",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            economic_model=Canteen.EconomicModel.PUBLIC,
            daily_meal_count=12,
            satellite_canteens_count=1,
            sector_list=[Sector.EDUCATION_SECONDAIRE_LYCEE, Sector.ENTERPRISE_ENTREPRISE],
        )
        cls.canteen_on_site = CanteenFactory(
            siret=None,
            siren_unite_legale="967669103",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            daily_meal_count=12,
            sector_list=[Sector.EDUCATION_SECONDAIRE_LYCEE, Sector.AUTRES_AUTRE],
        )
        cls.canteen_on_site_central = CanteenFactory(
            siret="96766910375238",
            management_type=Canteen.ManagementType.CONCEDED,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PRIVATE,
            daily_meal_count=12,
            central_producer_siret=cls.canteen_central.siret,
            sector_list=[Sector.ADMINISTRATION_PRISON],
            line_ministry=Canteen.Ministries.ARMEE,
        )

    def test_group_and_count_by_field(self):
        self.assertEqual(Canteen.objects.count(), 4)
        # group by production_type
        result = Canteen.objects.group_and_count_by_field("management_type")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["management_type"], Canteen.ManagementType.DIRECT)
        self.assertEqual(result[0]["count"], 3)
        self.assertEqual(result[1]["management_type"], Canteen.ManagementType.CONCEDED)
        self.assertEqual(result[1]["count"], 1)
        # group by production_type
        result = Canteen.objects.group_and_count_by_field("production_type")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["production_type"], Canteen.ProductionType.CENTRAL)
        self.assertEqual(result[0]["count"], 1)
        # group by economic_model
        result = Canteen.objects.group_and_count_by_field("economic_model")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["economic_model"], Canteen.EconomicModel.PUBLIC)
        self.assertEqual(result[0]["count"], 3)
        self.assertEqual(result[1]["economic_model"], Canteen.EconomicModel.PRIVATE)
        self.assertEqual(result[1]["count"], 1)
        # group by sector_category
        result = Canteen.objects.group_and_count_by_field("sector_category")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["sector_category"], SectorCategory.EDUCATION)
        self.assertEqual(result[0]["count"], 2)


class CanteenModelPropertiesTest(TestCase):
    def test_canteen_get_declaration_donnees_year_display(self):
        canteen_with_diagnostic_cancelled = CanteenFactory(declaration_donnees_2024=False)
        canteen_with_diagnostic_submitted = CanteenFactory(
            siret="21590350100017",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=1,
            declaration_donnees_2024=True,
        )
        canteen_satellite_with_central_diagnostic_submitted = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=canteen_with_diagnostic_submitted.siret,
            declaration_donnees_2024=True,
        )
        diagnostic_filled = DiagnosticFactory(
            canteen=canteen_with_diagnostic_cancelled,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            valeur_totale=1000,
        )  # filled
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            td_to_cancel = Teledeclaration.create_from_diagnostic(diagnostic_filled, applicant=UserFactory())
            td_to_cancel.cancel()
        diagnostic_filled_and_submitted = DiagnosticFactory(
            canteen=canteen_with_diagnostic_submitted,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            valeur_totale=1000,
        )  # filled & submitted
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            Teledeclaration.create_from_diagnostic(diagnostic_filled_and_submitted, applicant=UserFactory())

        self.assertEqual(canteen_with_diagnostic_cancelled.get_declaration_donnees_year_display(2023), "")
        self.assertEqual(canteen_with_diagnostic_cancelled.get_declaration_donnees_year_display(2024), "")
        self.assertEqual(canteen_with_diagnostic_submitted.get_declaration_donnees_year_display(2023), "")
        self.assertEqual(
            canteen_with_diagnostic_submitted.get_declaration_donnees_year_display(2024), "📩 Télédéclarée"
        )
        self.assertEqual(
            canteen_satellite_with_central_diagnostic_submitted.get_declaration_donnees_year_display(2023), ""
        )
        self.assertEqual(
            canteen_satellite_with_central_diagnostic_submitted.get_declaration_donnees_year_display(2024),
            "📩 Télédéclarée (par CC)",
        )

    @freeze_time("2024-01-20")
    def test_appro_and_service_diagnostics_in_past_ordered_year_desc(self):
        canteen = CanteenFactory()
        DiagnosticFactory(canteen=canteen, year=2024)
        DiagnosticFactory(canteen=canteen, year=2022)
        DiagnosticFactory(canteen=canteen, year=2023)
        canteen.refresh_from_db()

        self.assertEqual(canteen.appro_diagnostics.count(), 2)
        self.assertEqual(canteen.appro_diagnostics.first().year, 2023)
        self.assertEqual(canteen.service_diagnostics.count(), 2)
        self.assertEqual(canteen.service_diagnostics.first().year, 2023)
        self.assertEqual(canteen.latest_published_year, 2023)
