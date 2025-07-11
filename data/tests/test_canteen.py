from django.test import TestCase
from freezegun import freeze_time

from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    PurchaseFactory,
    SectorFactory,
    UserFactory,
)
from data.models import Canteen, Diagnostic, Sector, Teledeclaration


class TestCanteenModel(TestCase):
    def test_create_canteen(self):
        # siret: normalize on save
        canteen = CanteenFactory.create(siret="756 656 218 99905")
        self.assertEqual(canteen.siret, "75665621899905")  # normalized
        # siren_unite_legale: normalize on save
        canteen = CanteenFactory.create(siren_unite_legale="756 656 218")
        self.assertEqual(canteen.siren_unite_legale, "756656218")  # normalized

    def test_create_canteen_siret_validation(self):
        # both siret and siren_unite_legale can be empty or set
        for siret in ["", None, "756 656 218 99905"]:
            for siren_unite_legale in ["", None, "756 656 218"]:
                CanteenFactory.create(siret=siret, siren_unite_legale=siren_unite_legale)

    def test_canteen_properties(self):
        canteen_1 = CanteenFactory(
            sectors=[SectorFactory.create(name="Sector 1")], line_ministry=Canteen.Ministries.CULTURE
        )
        canteen_2 = CanteenFactory()

        # is_spe
        self.assertTrue(canteen_1.is_spe)
        self.assertFalse(canteen_2.is_spe)

    @freeze_time("2024-01-20")
    def test_appro_and_service_diagnostics_in_past_ordered_year_desc(self):
        canteen = CanteenFactory.create()
        DiagnosticFactory(canteen=canteen, year=2024)
        DiagnosticFactory(canteen=canteen, year=2022)
        DiagnosticFactory(canteen=canteen, year=2023)
        canteen.refresh_from_db()

        self.assertEqual(canteen.appro_diagnostics.count(), 2)
        self.assertEqual(canteen.appro_diagnostics.first().year, 2023)
        self.assertEqual(canteen.service_diagnostics.count(), 2)
        self.assertEqual(canteen.service_diagnostics.first().year, 2023)
        self.assertEqual(canteen.latest_published_year, 2023)

    def test_soft_delete_canteen(self):
        """
        The delete method should "soft delete" a canteen and have it hidden by default
        from querysets, unless specifically asked for
        """
        canteen = CanteenFactory.create()
        canteen.delete()
        qs = Canteen.objects.all()
        self.assertEqual(qs.count(), 0, "Soft deleted canteen is not visible in default queryset")
        qs = Canteen.all_objects.all()
        self.assertEqual(qs.count(), 1, "Soft deleted canteens can be accessed in custom queryset")


class TestCanteenVisibleQuerySetAndProperty(TestCase):
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


class TestCanteenSatelliteQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_central_1 = CanteenFactory(
            siret="75665621899905", production_type=Canteen.ProductionType.CENTRAL, satellite_canteens_count=2
        )  # 1 missing
        cls.canteen_central_2 = CanteenFactory(
            siret="75665621899906", production_type=Canteen.ProductionType.CENTRAL, satellite_canteens_count=2
        )
        cls.canteen_on_site_central_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=cls.canteen_central_1.siret
        )
        cls.canteen_on_site_central_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=cls.canteen_central_2.siret
        )
        cls.canteen_on_site_central_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=cls.canteen_central_2.siret
        )

    def test_is_satellite(self):
        self.assertEqual(Canteen.objects.count(), 5)
        self.assertEqual(Canteen.objects.is_satellite().count(), 3)

    def test_annotate_with_central_kitchen_id(self):
        self.assertEqual(Canteen.objects.count(), 5)
        self.assertEqual(
            Canteen.objects.annotate_with_central_kitchen_id()
            .filter(id=self.canteen_on_site_central_1.id)
            .first()
            .central_kitchen_id,
            self.canteen_central_1.id,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_central_kitchen_id()
            .filter(id=self.canteen_on_site_central_2.id)
            .first()
            .central_kitchen_id,
            self.canteen_central_2.id,
        )
        self.assertIsNone(
            Canteen.objects.annotate_with_central_kitchen_id()
            .filter(id=self.canteen_central_1.id)
            .first()
            .central_kitchen_id
        )

    def test_get_satellites(self):
        self.assertEqual(Canteen.objects.count(), 5)
        self.assertEqual(Canteen.objects.get_satellites(self.canteen_central_1.siret).count(), 1)
        self.assertEqual(Canteen.objects.get_satellites(self.canteen_central_2.siret).count(), 2)

    def test_annotate_with_satellites_in_db_count(self):
        self.assertEqual(Canteen.objects.count(), 5)
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .filter(id=self.canteen_central_1.id)
            .first()
            .satellites_in_db_count,
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .filter(id=self.canteen_central_2.id)
            .first()
            .satellites_in_db_count,
            2,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_satellites_in_db_count()
            .filter(id=self.canteen_on_site_central_1.id)
            .first()
            .satellites_in_db_count,
            0,
        )


class TestCanteenPurchaseQuerySet(TestCase):
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


class TestCanteenDiagnosticTeledeclarationQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        CanteenFactory()
        canteen_with_diagnostic_cancelled = CanteenFactory()
        canteen_with_diagnostic_submitted = CanteenFactory()
        diagnostic_filled = DiagnosticFactory(
            canteen=canteen_with_diagnostic_cancelled,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            value_total_ht=1000,
        )  # filled
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            td_to_cancel = Teledeclaration.create_from_diagnostic(diagnostic_filled, applicant=UserFactory())
            td_to_cancel.cancel()
        diagnostic_filled_and_submitted = DiagnosticFactory(
            canteen=canteen_with_diagnostic_submitted,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            value_total_ht=1000,
        )  # filled & submitted
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            Teledeclaration.create_from_diagnostic(diagnostic_filled_and_submitted, applicant=UserFactory())
        DiagnosticFactory(
            canteen=canteen_with_diagnostic_submitted,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2023,
            value_total_ht=None,
        )  # missing data

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

    def test_annotate_with_td_for_year(self):
        self.assertEqual(Canteen.objects.count(), 3)
        # has_td
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2024).filter(has_td=True).count(), 2)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2023).filter(has_td=True).count(), 0)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2022).filter(has_td=True).count(), 0)
        # has_td_submitted
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2024).filter(has_td_submitted=True).count(), 1)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2023).filter(has_td_submitted=True).count(), 0)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2022).filter(has_td_submitted=True).count(), 0)


class TestCanteenSiretOrSirenUniteLegaleQuerySetAndProperty(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_siret_siren = CanteenFactory(siret="75665621899905", siren_unite_legale="756656218")  # OK
        cls.canteen_siret_1 = CanteenFactory(siret="75665621899905", siren_unite_legale="")  # OK
        cls.canteen_siret_2 = CanteenFactory(siret="75665621899905", siren_unite_legale=None)  # OK
        cls.canteen_siren_1 = CanteenFactory(siret="", siren_unite_legale="756656218")  # OK
        cls.canteen_none_1 = CanteenFactory(siret="", siren_unite_legale="")
        cls.canteen_none_2 = CanteenFactory(siret="", siren_unite_legale=None)
        cls.canteen_siren_2 = CanteenFactory(siret=None, siren_unite_legale="756656218")  # OK
        cls.canteen_none_3 = CanteenFactory(siret=None, siren_unite_legale="")
        cls.canteen_none_4 = CanteenFactory(siret=None, siren_unite_legale=None)

    def has_siret_or_siren_unite_legale_queryset(self):
        self.assertEqual(Canteen.objects.count(), 9)
        self.assertEqual(Canteen.objects.has_siret_or_siren_unite_legale().count(), 5)

    def test_siret_or_siren_unite_legale_property(self):
        for canteen in [self.canteen_siret_siren, self.canteen_siret_1, self.canteen_siret_2]:
            self.assertEqual(canteen.siret_or_siren_unite_legale, "75665621899905")
        for canteen in [self.canteen_siren_1, self.canteen_siren_2]:
            self.assertEqual(canteen.siret_or_siren_unite_legale, "756656218")
        for canteen in [self.canteen_none_1, self.canteen_none_2, self.canteen_none_3, self.canteen_none_4]:
            self.assertEqual(canteen.siret_or_siren_unite_legale, "")


class TestCanteenCompleteQuerySetAndProperty(TestCase):
    @classmethod
    def setUpTestData(cls):
        sector = SectorFactory.create(name="Sector", category=Sector.Categories.ADMINISTRATION)
        sector_line_ministry = SectorFactory(
            name="Sector ministry", category=Sector.Categories.AUTRES, has_line_ministry=True
        )
        COMMON = {
            # CanteenFactory generates: name, city_insee_code, sectors
            "yearly_meal_count": 1000,
            "management_type": Canteen.ManagementType.DIRECT,
            "economic_model": Canteen.EconomicModel.PUBLIC,
            "sectors": [sector],
        }
        cls.canteen_central = CanteenFactory(
            **COMMON,
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=1,
        )
        cls.canteen_central_incomplete = CanteenFactory(
            **COMMON,
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=0,  # incomplete
        )
        cls.canteen_central_serving = CanteenFactory(
            **COMMON,
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            daily_meal_count=12,
            satellite_canteens_count=1,
        )
        cls.canteen_central_serving_incomplete = CanteenFactory(
            **COMMON,
            siret=None,  # incomplete
            siren_unite_legale=None,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            daily_meal_count=12,
            satellite_canteens_count=1,
        )
        cls.canteen_on_site = CanteenFactory(
            **COMMON,
            siret=None,
            siren_unite_legale="967669103",  # complete
            production_type=Canteen.ProductionType.ON_SITE,
            daily_meal_count=12,
        )
        cls.canteen_on_site_incomplete_1 = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE,
            daily_meal_count=0,  # incomplete
        )
        cls.canteen_on_site_incomplete_2 = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE,
            daily_meal_count=12,
        )
        cls.canteen_on_site_incomplete_2.sectors.clear()  # incomplete
        cls.canteen_on_site_incomplete_3 = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE,
            daily_meal_count=12,
            line_ministry=None,  # incomplete
        )
        cls.canteen_on_site_incomplete_3.sectors.set([sector_line_ministry])
        cls.canteen_on_site_central = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            daily_meal_count=12,
            central_producer_siret=cls.canteen_central.siret,
        )
        cls.canteen_on_site_central_incomplete = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            daily_meal_count=12,
            central_producer_siret=None,  # incomplete
        )

    def test_is_filled_queryset(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.is_filled().count(), 4)

    def test_is_filled_property(self):
        for canteen in [
            self.canteen_central,
            self.canteen_central_serving,
            self.canteen_on_site,
            self.canteen_on_site_central,
        ]:
            self.assertTrue(canteen.is_filled)
        for canteen in [
            self.canteen_central_incomplete,
            self.canteen_central_serving_incomplete,
            self.canteen_on_site_incomplete_1,
            self.canteen_on_site_incomplete_2,
            self.canteen_on_site_incomplete_3,
            self.canteen_on_site_central_incomplete,
        ]:
            self.assertFalse(canteen.is_filled)

    def test_has_missing_data_queryset(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.objects.has_missing_data().count(), 6)


class TestCanteenAggregateQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        sector = SectorFactory.create(name="Sector", category=Sector.Categories.ADMINISTRATION)
        sector_line_ministry = SectorFactory(
            name="Sector ministry", category=Sector.Categories.AUTRES, has_line_ministry=True
        )
        cls.canteen_central = CanteenFactory(
            siret="75665621899905",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            satellite_canteens_count=1,
            sectors=[sector],
        )
        cls.canteen_central_serving = CanteenFactory(
            siret="75665621899905",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            economic_model=Canteen.EconomicModel.PUBLIC,
            daily_meal_count=12,
            satellite_canteens_count=1,
            sectors=[sector],
        )
        cls.canteen_on_site = CanteenFactory(
            siret=None,
            siren_unite_legale="967669103",
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            daily_meal_count=12,
            sectors=[sector],
        )
        cls.canteen_on_site_central = CanteenFactory(
            siret="96766910375238",
            management_type=Canteen.ManagementType.CONCEDED,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PRIVATE,
            daily_meal_count=12,
            central_producer_siret=cls.canteen_central.siret,
            sectors=[sector_line_ministry],
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
        # group by sectors__category
        result = Canteen.objects.group_and_count_by_field("sectors__category")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["sectors__category"], Sector.Categories.ADMINISTRATION)
        self.assertEqual(result[0]["count"], 3)
        self.assertEqual(result[1]["sectors__category"], Sector.Categories.AUTRES)
        self.assertEqual(result[1]["count"], 1)
