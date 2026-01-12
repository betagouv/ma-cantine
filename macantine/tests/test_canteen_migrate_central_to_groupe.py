from freezegun import freeze_time

from django.core.management import call_command
from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
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
        # canteen_central_2 is deleted (1 satellite)
        cls.canteen_central_2_deleted = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=2,
        )
        cls.canteen_central_2_deleted.delete()
        cls.canteen_satellite_2_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_2_deleted.siret,
        )
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
        cls.canteen_central_serving_4.satellite_canteens_count = 0
        cls.canteen_central_serving_4.save(skip_validations=True)
        # extra satellites & sites
        cls.canteen_satellite_central_producer_empty = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.canteen_central_serving_4.siret,
        )
        cls.canteen_satellite_central_producer_empty.central_producer_siret = None
        cls.canteen_satellite_central_producer_empty.save(skip_validations=True)
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
        cls.canteen_site_with_central_producer_siret.central_producer_siret = cls.canteen_central_1.siret
        cls.canteen_site_with_central_producer_siret.save(skip_validations=True)
        # existing GROUPE canteen
        cls.canteen_groupe_1 = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE,
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            # create a diagnostic teledeclared for canteen_central_1
            cls.diagnostic_canteen_central_1 = DiagnosticFactory(
                canteen=cls.canteen_central_1,
                year=2024,
            )
            cls.diagnostic_canteen_central_1.teledeclare(applicant=UserFactory())
            # create a diagnostic teledeclared for canteen_central_serving_3
            cls.diagnostic_canteen_central_serving_3 = DiagnosticFactory(
                canteen=cls.canteen_central_serving_3,
                year=2024,
            )
            cls.diagnostic_canteen_central_serving_3.teledeclare(applicant=UserFactory())

    def test_canteen_migrate_central_to_groupe_dry_run(self):
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.all_objects.count(), 13)  # 11 + 2 deleted
        # Run command (Dry run)
        call_command("canteen_migrate_central_to_groupe")
        # Check that counts were NOT changed
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.all_objects.count(), 13)  # 11 + 2 deleted
        # Refresh from db
        self.canteen_central_1.refresh_from_db()
        self.canteen_central_2_deleted.refresh_from_db()
        self.canteen_groupe_1.refresh_from_db()
        # Check that canteens were NOT changed
        self.assertEqual(self.canteen_central_1.production_type, Canteen.ProductionType.CENTRAL)
        self.assertEqual(self.canteen_central_1.satellites.count(), 1)  # 1 is deleted
        self.assertEqual(self.canteen_central_2_deleted.production_type, Canteen.ProductionType.CENTRAL)
        self.assertEqual(self.canteen_central_2_deleted.satellites.count(), 1)

    def test_canteen_migrate_central_serving_to_groupe_dry_run(self):
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.all_objects.count(), 13)  # 11 + 2 deleted
        # Run command (Dry run)
        call_command("canteen_migrate_central_to_groupe")
        # Check that counts were NOT changed
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.all_objects.count(), 13)  # 11 + 2 deleted
        # Refresh from db
        self.canteen_central_serving_3.refresh_from_db()
        self.canteen_central_serving_4.refresh_from_db()
        # Check that canteens were NOT changed
        self.assertEqual(self.canteen_central_serving_3.production_type, Canteen.ProductionType.CENTRAL_SERVING)
        self.assertEqual(self.canteen_central_serving_3.satellites.count(), 1)
        self.assertEqual(self.canteen_central_serving_4.production_type, Canteen.ProductionType.CENTRAL_SERVING)
        self.assertEqual(self.canteen_central_serving_4.satellites.count(), 0)

    def test_canteen_migrate_central_to_groupe_apply(self):
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.all_objects.count(), 13)  # 11 + 2 deleted
        self.assertEqual(self.canteen_central_1.satellites.count(), 1)
        self.assertEqual(self.canteen_central_2_deleted.satellites.count(), 1)
        self.assertEqual(self.canteen_groupe_1.satellites.count(), 0)
        # Run command (Apply changes)
        call_command("canteen_migrate_central_to_groupe", apply=True)
        # Check that counts were changed
        self.assertEqual(Canteen.objects.count(), 11 + 2)  # 11 + 2 new satellites
        self.assertEqual(Canteen.all_objects.count(), 13 + 2)  # 11 + 2 deleted + 2 new satellites
        # Refresh from db
        self.canteen_central_1.refresh_from_db()
        self.diagnostic_canteen_central_1.refresh_from_db()
        self.canteen_central_2_deleted.refresh_from_db()
        self.canteen_groupe_1.refresh_from_db()
        # Check that canteens were changed/created
        self.assertEqual(self.canteen_central_1.production_type, Canteen.ProductionType.GROUPE)
        self.assertEqual(
            self.canteen_central_1.satellites.count(), 1
        )  # 1 is deleted and non-satellites were not linked
        self.assertEqual(Canteen.all_objects.filter(groupe_id=self.canteen_central_1.id).count(), 2)
        self.assertEqual(len(self.diagnostic_canteen_central_1.satellites_snapshot), 1)
        self.assertEqual(
            self.canteen_central_2_deleted.production_type, Canteen.ProductionType.GROUPE
        )  # changed even if deleted
        self.assertEqual(
            self.canteen_central_2_deleted.satellites.count(), 0
        )  # non-deleted satellites were not linked
        self.assertEqual(Canteen.all_objects.filter(groupe_id=self.canteen_central_2_deleted.id).count(), 0)
        self.assertEqual(self.canteen_groupe_1.satellites.count(), 0)

    def test_canteen_migrate_central_serving_to_groupe_apply(self):
        self.assertEqual(Canteen.objects.count(), 11)
        self.assertEqual(Canteen.all_objects.count(), 13)  # 11 + 2 deleted
        self.assertEqual(self.canteen_central_serving_3.satellites.count(), 1)
        self.assertEqual(len(self.diagnostic_canteen_central_serving_3.satellites_snapshot), 1)
        self.assertEqual(self.canteen_central_serving_4.satellites.count(), 0)
        # Run command (Apply changes)
        call_command("canteen_migrate_central_to_groupe", apply=True)
        # Check that counts were changed
        self.assertEqual(Canteen.objects.count(), 11 + 2)  # 11 + 2 new satellites
        self.assertEqual(Canteen.all_objects.count(), 13 + 2)  # 11 + 2 deleted + 2 new satellites
        # Refresh from db
        self.canteen_central_serving_3.refresh_from_db()
        self.diagnostic_canteen_central_serving_3.refresh_from_db()
        self.canteen_central_serving_4.refresh_from_db()
        # Check that canteens were changed/created
        self.assertEqual(self.canteen_central_serving_3.production_type, Canteen.ProductionType.GROUPE)
        self.assertEqual(self.canteen_central_serving_3.satellites.count(), 1 + 1)  # 1 new satellite created
        self.assertEqual(Canteen.all_objects.filter(groupe_id=self.canteen_central_serving_3.id).count(), 2)
        self.assertEqual(len(self.diagnostic_canteen_central_serving_3.satellites_snapshot), 1 + 1)
        self.assertEqual(self.canteen_central_serving_4.production_type, Canteen.ProductionType.GROUPE)
        self.assertEqual(self.canteen_central_serving_4.satellites.count(), 0 + 1)  # 1 new satellite created
        self.assertEqual(Canteen.all_objects.filter(groupe_id=self.canteen_central_serving_4.id).count(), 1)
