from django.test import TestCase
from django.test.utils import override_settings
from freezegun import freeze_time

from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    PurchaseFactory,
    TeledeclarationFactory,
)
from data.models import Canteen, Diagnostic, Teledeclaration


class TestCanteenModel(TestCase):
    def test_create_canteen(self):
        # siret: normalize on save
        canteen = CanteenFactory.create(siret="756 656 218 99905")
        self.assertEqual(canteen.siret, "75665621899905")  # normalized
        # siren_unite_legale: normalize on save
        canteen = CanteenFactory.create(siren_unite_legale="756 656 218")
        self.assertEqual(canteen.siren_unite_legale, "756656218")  # normalized
        # region: get from department on save
        canteen = CanteenFactory.create(department="38", region=None)
        self.assertEqual(canteen.region, "84")  # Auvergne-Rhône-Alpes

    def test_create_canteen_siret_validation(self):
        # both siret and siren_unite_legale can be empty or set
        for siret in ["", None, "756 656 218 99905"]:
            for siren_unite_legale in ["", None, "756 656 218"]:
                CanteenFactory.create(siret=siret, siren_unite_legale=siren_unite_legale)

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


class TestCanteenVisibleQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        CanteenFactory(line_ministry=None, publication_status=Canteen.PublicationStatus.PUBLISHED)
        cls.canteen_published_armee = CanteenFactory(
            line_ministry=Canteen.Ministries.ARMEE, publication_status=Canteen.PublicationStatus.PUBLISHED
        )
        cls.canteen_draft = CanteenFactory(line_ministry=None, publication_status=Canteen.PublicationStatus.DRAFT)

    @override_settings(PUBLISH_BY_DEFAULT=False)
    def test_publicly_visible(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_visible()
        self.assertEqual(qs.count(), 2)
        self.assertTrue(self.canteen_draft not in qs)

    @override_settings(PUBLISH_BY_DEFAULT=False)
    def test_publicly_hidden(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_hidden()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.canteen_draft)

    @override_settings(PUBLISH_BY_DEFAULT=True)
    def test_publicly_visible_publish_by_default(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_visible()
        self.assertEqual(qs.count(), 2)
        self.assertTrue(self.canteen_published_armee not in qs)

    @override_settings(PUBLISH_BY_DEFAULT=True)
    def test_publicly_hidden_publish_by_default(self):
        self.assertEqual(Canteen.objects.count(), 3)
        qs = Canteen.objects.publicly_hidden()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.canteen_published_armee)


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
        canteen_with_diagnostics = CanteenFactory()
        CanteenFactory()
        diagnostic_complete = DiagnosticFactory(
            canteen=canteen_with_diagnostics,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2024,
            value_total_ht=1000,
        )  # complete
        DiagnosticFactory(
            canteen=canteen_with_diagnostics,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2023,
            value_total_ht=None,
        )
        TeledeclarationFactory(
            canteen=canteen_with_diagnostics,
            diagnostic=diagnostic_complete,
            year=2024,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
        )

    def test_annotate_with_diagnostic_for_year(self):
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2024).filter(diagnostic_for_year__isnull=False).count(),
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2023).filter(diagnostic_for_year__isnull=False).count(),
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2022).filter(diagnostic_for_year__isnull=False).count(),
            0,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2024)
            .filter(has_diagnostic_filled_for_year=True)
            .count(),
            1,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2023)
            .filter(has_diagnostic_filled_for_year=True)
            .count(),
            0,
        )
        self.assertEqual(
            Canteen.objects.annotate_with_diagnostic_for_year(2022)
            .filter(has_diagnostic_filled_for_year=True)
            .count(),
            0,
        )
        # TODO: diagnostic_for_year_cc_mode

    def test_annotate_with_td_for_year(self):
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2024).filter(has_td=True).count(), 1)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2023).filter(has_td=True).count(), 0)
        self.assertEqual(Canteen.objects.annotate_with_td_for_year(2022).filter(has_td=True).count(), 0)


class TestCanteenSiretOrSirenUniteLegaleQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        CanteenFactory(siret="75665621899905", siren_unite_legale="756656218")  # OK
        CanteenFactory(siret="75665621899905", siren_unite_legale="")  # OK
        CanteenFactory(siret="75665621899905", siren_unite_legale=None)  # OK
        CanteenFactory(siret="", siren_unite_legale="756656218")  # OK
        CanteenFactory(siret="", siren_unite_legale="")
        CanteenFactory(siret="", siren_unite_legale=None)
        CanteenFactory(siret=None, siren_unite_legale="756656218")  # OK
        CanteenFactory(siret=None, siren_unite_legale="")
        CanteenFactory(siret=None, siren_unite_legale=None)

    def has_siret_or_siren_unite_legale(self):
        self.assertEqual(Canteen.objects.count(), 9)
        self.assertEqual(Canteen.objects.has_siret_or_siren_unite_legale().count(), 5)


class TestCanteenCompletePropertyAndQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        COMMON = {
            # CanteenFactory generates: name, city_insee_code, sectors
            "yearly_meal_count": 1000,
            "publication_status": Canteen.PublicationStatus.PUBLISHED,
            "management_type": Canteen.ManagementType.DIRECT,
            "economic_model": Canteen.EconomicModel.PUBLIC,
        }
        cls.canteen_central = CanteenFactory(
            **COMMON,
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=1
        )
        cls.canteen_central_incomplete = CanteenFactory(
            **COMMON,
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=0  # incomplete
        )
        cls.canteen_central_serving = CanteenFactory(
            **COMMON,
            siret="75665621899905",
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            daily_meal_count=12,
            satellite_canteens_count=1
        )
        cls.canteen_central_serving_incomplete = CanteenFactory(
            **COMMON,
            siret=None,  # incomplete
            siren_unite_legale=None,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            daily_meal_count=12,
            satellite_canteens_count=1
        )
        cls.canteen_on_site = CanteenFactory(
            **COMMON,
            siret=None,
            siren_unite_legale="967669103",  # complete
            production_type=Canteen.ProductionType.ON_SITE,
            daily_meal_count=12
        )
        cls.canteen_on_site_incomplete = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE,
            daily_meal_count=0  # incomplete
        )
        cls.canteen_on_site_central = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            daily_meal_count=12,
            central_producer_siret="75665621899905"
        )
        cls.canteen_on_site_central_incomplete = CanteenFactory(
            **COMMON,
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            daily_meal_count=12,
            central_producer_siret=None  # incomplete
        )

    def test_is_filled_queryset(self):
        self.assertEqual(Canteen.objects.count(), 8)
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
            self.canteen_on_site_incomplete,
            self.canteen_on_site_central_incomplete,
        ]:
            self.assertFalse(canteen.is_filled)

    def test_has_missing_data_queryset(self):
        self.assertEqual(Canteen.objects.count(), 8)
        self.assertEqual(Canteen.objects.has_missing_data().count(), 4)
