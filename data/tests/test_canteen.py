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
        """
        - the field is mandatory
        - the field should be one of the choices
        - some types are not available anymore
        """
        for TUPLE_OK in [(key, key) for key in Canteen.ProductionType.values]:
            with self.subTest(production_type=TUPLE_OK[0]):
                canteen = CanteenFactory(production_type=TUPLE_OK[0])
                self.assertEqual(canteen.production_type, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", "  ", 123, "invalid"]:
            with self.subTest(production_type=VALUE_NOT_OK):
                self.assertRaises(ValidationError, CanteenFactory, production_type=VALUE_NOT_OK)
        # cannot change a Canteen to CENTRAL & CENTRAL_SERVING anymore
        canteen = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        for production_type in [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]:
            canteen.production_type = production_type
            self.assertRaises(ValidationError, canteen.save)

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
        # groupe & central kitchen: must be empty
        for production_type in [Canteen.ProductionType.GROUPE, Canteen.ProductionType.CENTRAL]:
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

    def test_canteen_groupe_fk_validation(self):
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        canteen_groupe_deleted = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        canteen_groupe_deleted.delete()
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)

        # not a satellite: must be empty
        for production_type in [
            Canteen.ProductionType.GROUPE,
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
            Canteen.ProductionType.ON_SITE,
        ]:
            for TUPLE_OK in [(None, None)]:
                with self.subTest(groupe=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, groupe=TUPLE_OK[0])
                    self.assertEqual(canteen.groupe, TUPLE_OK[1])
            for VALUE_NOT_OK in [canteen_groupe.id, canteen_groupe_deleted.id, canteen_site.id, 999, "", "invalid"]:
                with self.subTest(groupe=VALUE_NOT_OK):
                    self.assertRaises(ValueError, CanteenFactory, production_type=production_type, groupe=VALUE_NOT_OK)
        # satellite: can be filled
        for production_type in [Canteen.ProductionType.ON_SITE_CENTRAL]:
            for TUPLE_OK in [(None, None), (canteen_groupe, canteen_groupe)]:
                with self.subTest(groupe=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, groupe=TUPLE_OK[0])
                    self.assertEqual(canteen.groupe, TUPLE_OK[1])
            for TUPLE_OK in [(None, None), (canteen_groupe.id, canteen_groupe)]:
                with self.subTest(groupe_id=TUPLE_OK[0]):
                    canteen = CanteenFactory(production_type=production_type, groupe_id=TUPLE_OK[0])
                    self.assertEqual(canteen.groupe, TUPLE_OK[1])
            for VALUE_NOT_OK in [canteen_site.id, canteen_groupe_deleted.id, 999, "", "invalid"]:
                with self.subTest(groupe=VALUE_NOT_OK):
                    self.assertRaises(ValueError, CanteenFactory, production_type=production_type, groupe=VALUE_NOT_OK)
            for VALUE_NOT_OK in [canteen_site.id, 999]:
                with self.subTest(groupe_id=VALUE_NOT_OK):
                    self.assertRaises(
                        ValidationError, CanteenFactory, production_type=production_type, groupe_id=VALUE_NOT_OK
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

    def test_canteen_reset_geo_fields_when_siret_change_on_save(self):
        canteen = CanteenFactory(siret="21340172201787", city_insee_code="34172", department="34", region="76")
        self.assertEqual(canteen.city_insee_code, "34172")

        canteen.siret = "21380185500015"
        canteen.save()

        self.assertEqual(canteen.city_insee_code, None)
        self.assertEqual(canteen.department, None)
        self.assertEqual(canteen.region, None)
        # geobot will run again

    def test_canteen_skip_validations_on_save(self):
        canteen = CanteenFactory(siret="75665621899905", siren_unite_legale=None)
        canteen.siret = None
        # should not raise
        canteen.save(skip_validations=True)
        self.assertEqual(canteen.siret, None)

    def test_canteen_dirty_fields_on_save(self):
        canteen = CanteenFactory(siret="21340172201787", city_insee_code="34172", department="34", region="76")
        self.assertFalse(canteen.is_dirty())
        self.assertEqual(canteen.get_dirty_fields(), {})

        canteen.siret = "21340172201787"  # same siret
        self.assertFalse(canteen.is_dirty())
        self.assertEqual(canteen.get_dirty_fields(), {})

        canteen.siret = "21380185500015"  # different siret
        self.assertTrue(canteen.is_dirty())
        self.assertEqual(canteen.get_dirty_fields(), {"siret": "21340172201787"})

        canteen.save()
        self.assertEqual(canteen.siret, "21380185500015")
        self.assertFalse(canteen.is_dirty())
        self.assertEqual(canteen.get_dirty_fields(), {})

    def test_update_geo_fields_on_save(self):
        # CanteenFactory skips the post_save signal
        # so we need to call save() to trigger the signal
        canteen = CanteenFactory.build(
            siret="21340172201787", city_insee_code=None, city=None, department=None, region=None
        )
        canteen.save()
        canteen.refresh_from_db()

        self.assertEqual(canteen.city_insee_code, "34172")
        self.assertEqual(canteen.city, "Montpellier")
        self.assertEqual(canteen.department, "34")
        self.assertEqual(canteen.region, "76")


class CanteenModelDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe_1_without_satellites = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_2_with_active_satellites = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_21 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_2_with_active_satellites,
        )
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def test_canteen_soft_delete(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(Canteen.all_objects.count(), 4)

        # ok to delete satellite canteen
        self.canteen_satellite_21.delete()
        # ok to delete site canteen
        self.canteen_site.delete()

        self.assertEqual(Canteen.objects.count(), 4 - 2)
        self.assertEqual(Canteen.all_objects.count(), 4)

    def test_can_soft_delete_if_missing_data_using_skip_validations(self):
        self.canteen_site.daily_meal_count = None
        self.canteen_site.save(skip_validations=True)

        # without skip_validations
        self.assertRaises(ValidationError, self.canteen_site.delete)

        # with skip_validations
        self.canteen_site.delete(skip_validations=True)

    def test_can_soft_delete_groupe_without_satellites(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(Canteen.all_objects.count(), 4)
        self.assertEqual(self.canteen_groupe_1_without_satellites.satellites.count(), 0)

        # ok to delete groupe without satellites
        self.canteen_groupe_1_without_satellites.delete()

        self.assertEqual(Canteen.objects.count(), 4 - 1)
        self.assertEqual(Canteen.all_objects.count(), 4)

    def test_can_soft_delete_groupe_with_only_deleted_satellites(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(Canteen.all_objects.count(), 4)
        self.assertEqual(self.canteen_groupe_2_with_active_satellites.satellites.count(), 1)

        # first delete satellites
        self.canteen_satellite_21.delete()
        self.assertEqual(self.canteen_groupe_2_with_active_satellites.satellites.count(), 0)
        # ok to delete groupe with deleted satellites
        self.canteen_groupe_2_with_active_satellites.delete()

        self.assertEqual(Canteen.objects.count(), 4 - 2)
        self.assertEqual(Canteen.all_objects.count(), 4)

    def test_cannot_soft_delete_groupe_with_active_satellites(self):
        self.assertEqual(self.canteen_groupe_2_with_active_satellites.satellites.count(), 1)
        self.assertRaises(ValidationError, self.canteen_groupe_2_with_active_satellites.delete)
        # even with skip_validations
        self.assertRaises(ValidationError, self.canteen_groupe_2_with_active_satellites.delete, skip_validations=True)

    def test_canteen_hard_delete(self):
        self.assertEqual(Canteen.objects.count(), 4)
        self.assertEqual(Canteen.all_objects.count(), 4)

        self.canteen_site.hard_delete()

        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(Canteen.all_objects.count(), 3)


class CanteenDeleteQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()

    def test_all_objects_queryset(self):
        """
        The delete method should "soft delete" a canteen and have it hidden by default
        from querysets, unless specifically asked for
        """
        self.assertEqual(Canteen.objects.count(), 1)

        self.canteen.delete()

        self.assertEqual(Canteen.objects.all().count(), 0)
        self.assertEqual(Canteen.all_objects.all().count(), 1)

    def test_is_deleted_property(self):
        self.assertFalse(self.canteen.is_deleted)

        self.canteen.delete()

        self.assertTrue(self.canteen.is_deleted)


class CanteenVisibleQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory(line_ministry=None)
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_armee = CanteenFactory(line_ministry=Canteen.Ministries.ARMEE)

    def test_publicly_visible_queryset(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_visible()
        self.assertEqual(qs.count(), 1)
        self.assertTrue(self.canteen in qs)
        self.assertFalse(self.canteen_groupe in qs)
        self.assertFalse(self.canteen_armee in qs)

    def test_publicly_hidden_queryset(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_hidden()
        self.assertEqual(qs.count(), 2)
        self.assertFalse(self.canteen in qs)
        self.assertTrue(self.canteen_groupe in qs)
        self.assertTrue(self.canteen_armee in qs)

    def test_publication_status_display_to_public_property(self):
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(self.canteen.publication_status_display_to_public, "published")
        self.assertEqual(self.canteen_groupe.publication_status_display_to_public, "draft")
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


class CanteenCentralAndSatelliteQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe_with_satellite = CanteenFactory(
            siren_unite_legale="756656218", production_type=Canteen.ProductionType.GROUPE, economic_model=None
        )
        cls.canteen_groupe_without_satellite = CanteenFactory(
            siren_unite_legale="356656218", production_type=Canteen.ProductionType.GROUPE, economic_model=None
        )
        cls.canteen_central_1 = CanteenFactory(
            siret="21340172201787",
            production_type=Canteen.ProductionType.CENTRAL,
            sector_list=[],
        )
        cls.canteen_central_2 = CanteenFactory(siret="21380185500015", production_type=Canteen.ProductionType.CENTRAL)
        cls.canteen_satellite_1 = CanteenFactory(
            siret="92341284500011",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_1.siret,
            groupe=cls.canteen_groupe_with_satellite,
        )
        cls.canteen_satellite_2 = CanteenFactory(
            siret="40419443300078",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_2.siret,
        )
        cls.canteen_satellite_3 = CanteenFactory(
            siret="83014132100034",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_2.siret,
        )
        cls.canteen_satellite_4 = CanteenFactory(
            siret="80631004084476",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )
        cls.canteen_central_serving_1 = CanteenFactory(
            siret="11007001800012",
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
        )
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def test_is_groupe(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.is_groupe().count(), 2)
        self.assertTrue(self.canteen_groupe_with_satellite.is_groupe)

    def test_is_central(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.is_central().count(), 2)
        self.assertTrue(self.canteen_central_1.is_central)

    def test_is_serving(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.is_serving().count(), 6)
        self.assertTrue(self.canteen_satellite_1.is_serving)
        self.assertTrue(self.canteen_central_serving_1.is_serving)
        self.assertTrue(self.canteen_site.is_serving)

    def test_is_satellite(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.is_satellite().count(), 4)
        self.assertTrue(self.canteen_satellite_1.is_satellite)

    def test_satellites_property(self):
        self.assertEqual(self.canteen_groupe_with_satellite.satellites.count(), 1)
        self.assertEqual(self.canteen_central_1.satellites.count(), 1)
        self.assertEqual(self.canteen_central_2.satellites.count(), 2)
        self.assertEqual(self.canteen_satellite_1.satellites.count(), 0)

    def test_satellites_count_property(self):
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_count, 1)
        self.assertEqual(self.canteen_central_1.satellites_count, 1)
        self.assertEqual(self.canteen_central_2.satellites_count, 2)
        self.assertEqual(self.canteen_satellite_1.satellites_count, 0)

    def test_satellites_missing_data_count_property(self):
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_missing_data_count, 0)
        self.assertEqual(self.canteen_groupe_without_satellite.satellites_missing_data_count, 0)
        # add to groupe a satellite with missing data
        self.canteen_satellite_3.groupe = self.canteen_groupe_with_satellite
        self.canteen_satellite_3.siret = None  # missing data
        self.canteen_satellite_3.save(skip_validations=True)
        self.canteen_groupe_with_satellite.refresh_from_db()
        # check again
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_missing_data_count, 1)

    @freeze_time("2026-01-15")  # during the 2025 campaign the year is hardcoded in the query
    def test_satellites_already_teledeclared_count_property(self):
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_already_teledeclared_count, 0)
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_count, 1)
        # create a diagnostic for the autonomous satellite and teledeclare it
        diagnostic_satellite_4 = DiagnosticFactory(canteen=self.canteen_satellite_4, year=2025)
        diagnostic_satellite_4.teledeclare(applicant=UserFactory())
        self.assertEqual(diagnostic_satellite_4.is_teledeclared, True)
        # link satellite to groupe
        self.canteen_satellite_4.groupe = self.canteen_groupe_with_satellite
        self.canteen_satellite_4.save(skip_validations=True)
        self.canteen_groupe_with_satellite.refresh_from_db()
        # check again
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_count, 2)
        self.assertEqual(self.canteen_groupe_with_satellite.satellites_already_teledeclared_count, 1)

    def test_get_satellites_old(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.get_satellites_old(self.canteen_central_1.siret).count(), 1)
        self.assertEqual(Canteen.objects.get_satellites_old(self.canteen_central_2.siret).count(), 2)

    def test_annotate_with_satellites_in_db_count(self):
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .get(id=self.canteen_groupe_with_satellite.id)
            .satellites_in_db_count,
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .get(id=self.canteen_groupe_without_satellite.id)
            .satellites_in_db_count,
            0,
        )

    def test_central_kitchen(self):
        self.assertEqual(self.canteen_groupe_with_satellite.central_kitchen, None)
        self.assertEqual(self.canteen_satellite_1.central_kitchen, self.canteen_groupe_with_satellite)
        self.assertEqual(self.canteen_site.central_kitchen, None)


class CanteenUserManagerQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager = UserFactory()
        cls.canteen_with_manager = CanteenFactory(managers=[cls.manager])
        cls.canteen_without_manager = CanteenFactory(managers=[])

    def test_annotate_with_is_managed_by_user(self):
        self.assertEqual(Canteen.objects.count(), 2)
        qs = Canteen.objects.annotate_with_is_managed_by_user(self.manager)
        self.assertTrue(qs.get(id=self.canteen_with_manager.id).is_managed_by_user)
        self.assertFalse(qs.get(id=self.canteen_without_manager.id).is_managed_by_user)
        qs = Canteen.objects.annotate_with_is_managed_by_user(UserFactory())
        self.assertFalse(qs.get(id=self.canteen_with_manager.id).is_managed_by_user)
        self.assertFalse(qs.get(id=self.canteen_without_manager.id).is_managed_by_user)
        qs = Canteen.objects.annotate_with_is_managed_by_user(None)
        self.assertFalse(qs.get(id=self.canteen_with_manager.id).is_managed_by_user)
        self.assertFalse(qs.get(id=self.canteen_without_manager.id).is_managed_by_user)


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
        cls.canteen_none_1.siret = ""  # missing data
        cls.canteen_none_1.save(skip_validations=True)
        cls.canteen_none_1.refresh_from_db()
        cls.canteen_none_2 = CanteenFactory()
        cls.canteen_none_2.siret = None
        cls.canteen_none_2.siren_unite_legale = ""  # missing
        cls.canteen_none_2.save(skip_validations=True)
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
        cls.canteen_groupe_with_satellite = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_in_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_with_satellite,
            central_producer_siret="21340172201787",
        )
        cls.canteen_groupe_without_satellite = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_on_site = CanteenFactory(
            siret=None,
            siren_unite_legale="967669103",  # complete
            production_type=Canteen.ProductionType.ON_SITE,
        )
        cls.canteen_on_site_missing_data_1 = CanteenFactory(
            siret="21380185500015",
            production_type=Canteen.ProductionType.ON_SITE,
            # daily_meal_count=12,
        )
        cls.canteen_on_site_missing_data_1.daily_meal_count = 0  # missing data
        cls.canteen_on_site_missing_data_1.save(skip_validations=True)
        cls.canteen_on_site_missing_data_1.refresh_from_db()
        cls.canteen_on_site_missing_data_2 = CanteenFactory(
            siret="21670482500019",
            production_type=Canteen.ProductionType.ON_SITE,
            # sector_list=[],  # missing data
        )
        cls.canteen_on_site_missing_data_2.sector_list = []  # missing data
        cls.canteen_on_site_missing_data_2.save(skip_validations=True)
        cls.canteen_on_site_missing_data_2.refresh_from_db()
        cls.canteen_on_site_missing_data_3 = CanteenFactory(
            siret="21640122400011",
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.ADMINISTRATION_PRISON],
            line_ministry=None,  # missing data
        )
        cls.canteen_satellite_not_in_groupe_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="21340172201787"
        )
        cls.canteen_satellite_not_in_groupe_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_satellite_missing_data = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            # economic_model=Canteen.EconomicModel.PRIVATE,  # missing data
        )
        cls.canteen_satellite_missing_data.economic_model = None  # missing data
        cls.canteen_satellite_missing_data.save(skip_validations=True)
        cls.canteen_satellite_missing_data.refresh_from_db()
        cls.canteen_filled_list = [
            cls.canteen_groupe_with_satellite,
            cls.canteen_groupe_without_satellite,
            cls.canteen_satellite_in_groupe,
            cls.canteen_on_site,
            cls.canteen_satellite_not_in_groupe_1,
            cls.canteen_satellite_not_in_groupe_2,
        ]
        cls.canteen_missing_data_list = [
            cls.canteen_on_site_missing_data_1,
            cls.canteen_on_site_missing_data_2,
            cls.canteen_on_site_missing_data_3,
            cls.canteen_satellite_missing_data,
        ]

    def test_is_filled_queryset(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.is_filled().count(), len(self.canteen_filled_list))

    def test_is_filled_field_true(self):
        for index, canteen in enumerate(self.canteen_filled_list):
            with self.subTest(index=index, canteen=canteen):
                self.assertTrue(canteen.is_filled)

    def test_is_filled_property_true(self):
        for index, canteen in enumerate(self.canteen_filled_list):
            with self.subTest(index=index, canteen=canteen):
                self.assertTrue(canteen._is_filled())

    def test_has_missing_data_queryset(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.has_missing_data().count(), len(self.canteen_missing_data_list))

    def test_is_filled_field_false(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.filter(is_filled=False).count(), len(self.canteen_missing_data_list))

    def test_is_filled_property_false(self):
        for index, canteen in enumerate(self.canteen_missing_data_list):
            with self.subTest(index=index, canteen=canteen):
                self.assertFalse(canteen._is_filled())


class CanteenAggregateQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central = CanteenFactory(
            siret="21590350100017",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[],
        )
        cls.canteen_central_serving = CanteenFactory(
            siret="21010034300016",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            economic_model=Canteen.EconomicModel.PUBLIC,
            daily_meal_count=12,
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
        cls.canteen_satellite = CanteenFactory(
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
