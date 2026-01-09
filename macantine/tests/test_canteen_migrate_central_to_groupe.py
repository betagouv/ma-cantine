from django.core.management import call_command
from django.test import TestCase

from data.factories import CanteenFactory
from data.models import Canteen


class CanteenMigrateCentralToGroupeCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # canteen_central_1 has 2 satellites (1 deleted)
        cls.canteen_central_1 = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=2,
        )
        cls.canteen_satellite_1_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_1.siret,
        )
        cls.canteen_satellite_1_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_1.siret,
        )
        cls.canteen_satellite_1_2.delete()
        # canteen_central_2 is deleted (0 satellites)
        cls.canteen_central_2_deleted = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=1,
        )
        cls.canteen_central_2_deleted.delete()
        # canteen_central_serving_3 has 1 satellite
        cls.canteen_central_serving_3 = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            satellite_canteens_count=1,
        )
        cls.canteen_satellite_3_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_serving_3.siret,
        )
        # canteen_central_serving_4 has 0 satellites
        cls.canteen_central_serving_4 = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            satellite_canteens_count=1,
        )
        Canteen.objects.filter(id=cls.canteen_central_serving_4.id).update(satellite_canteens_count=0)
        # extra satellites & sites
        cls.canteen_satellite_central_producer_empty = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_serving_4.siret,
        )
        Canteen.objects.filter(id=cls.canteen_satellite_central_producer_empty.id).update(central_producer_siret=None)
        cls.canteen_satellite_central_producer_unknown = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="00000000000000",
        )
        cls.canteen_site = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
        )
        cls.canteen_site_with_central_producer_siret = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
        )
        Canteen.objects.filter(id=cls.canteen_site_with_central_producer_siret.id).update(
            central_producer_siret=cls.canteen_central_1.siret
        )
        # existing GROUPE canteen
        cls.canteen_groupe_1 = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE,
        )

    def test_canteen_migrate_central_to_groupe_dry_run(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.all_objects.count(), 12)
        # Run command (Dry run)
        call_command("canteen_migrate_central_to_groupe")
        # Check that counts were NOT changed
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.all_objects.count(), 12)
        # Refresh from db
        self.canteen_central_1.refresh_from_db()
        self.canteen_central_serving_4.refresh_from_db()
        self.canteen_groupe_1.refresh_from_db()
        # Check that canteens were NOT changed
        self.assertEqual(self.canteen_central_1.production_type, Canteen.ProductionType.CENTRAL)
        self.assertEqual(self.canteen_central_1.satellites.count(), 1)  # 1 is deleted
        self.assertEqual(self.canteen_central_serving_4.production_type, Canteen.ProductionType.CENTRAL_SERVING)
        self.assertEqual(self.canteen_central_serving_4.satellites.count(), 0)

    def test_canteen_migrate_central_to_groupe_apply(self):
        self.assertEqual(Canteen.objects.count(), 10)
        self.assertEqual(Canteen.all_objects.count(), 12)
        # Run command (Apply changes)
        call_command("canteen_migrate_central_to_groupe", apply=True)
        # Check that counts were changed
        self.assertEqual(Canteen.objects.count(), 10 + 2)
        self.assertEqual(Canteen.all_objects.count(), 12 + 2)
        # Refresh from db
        self.canteen_central_1.refresh_from_db()
        self.canteen_central_serving_4.refresh_from_db()
        self.canteen_groupe_1.refresh_from_db()
        # Check that canteens were changed/created
        self.assertEqual(self.canteen_central_1.production_type, Canteen.ProductionType.GROUPE)
        self.assertEqual(self.canteen_central_1.satellites.count(), 1)  # 1 is deleted
        self.assertEqual(Canteen.all_objects.filter(groupe_id=self.canteen_central_1.id).count(), 2)  # 2 satellites
        self.assertEqual(self.canteen_central_serving_4.production_type, Canteen.ProductionType.GROUPE)
        self.assertEqual(self.canteen_central_serving_4.satellites.count(), 1)  # new satellite
