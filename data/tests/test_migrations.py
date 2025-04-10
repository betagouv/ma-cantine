from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase


class TestMigrations(TestCase):

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert (
            self.migrate_from and self.migrate_to
        ), "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)
        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps


class ApproFieldsTestCase(TestMigrations):
    migrate_from = "0172_historicalteledeclaration_meal_price_and_more"
    migrate_to = "0173_repopulate_fields_agg_meal_price"

    def setUpBeforeMigration(self, apps):
        Teledeclaration = apps.get_model("data", "Teledeclaration")
        Diagnostic = apps.get_model("data", "Diagnostic")
        Canteen = apps.get_model("data", "Canteen")

        # Create a canteen
        canteen = Canteen.objects.create(
            name="Test Canteen",
            siret="12345678912345",
            city="Test City",
            postal_code="75001",
            yearly_meal_count=1000,
        )

        # Create a simple diagnostic
        diag_simple = Diagnostic.objects.create(
            canteen=canteen,
            year=2021,
            diagnostic_type="SIMPLE",
            value_total_ht=100.0,
            value_bio_ht=50.0,
        )

        # Create a teledeclaration for the simple diagnostic
        self.td_simple = Teledeclaration.objects.create(
            year=2021,
            declared_data={
                "teledeclaration": {
                    "diagnostic_type": "SIMPLE",
                    "value_total_ht": 100.0,
                    "value_bio_ht": 50.0,
                    "value_sustainable_ht": None,
                },
                "canteen": {"yearly_meal_count": 1000},
            },
            diagnostic=diag_simple,
        )

        # Create a complete diagnostic
        diag_complete = Diagnostic.objects.create(
            canteen=canteen,
            year=2020,
            diagnostic_type="COMPLETE",
            value_total_ht=200.0,
            value_boissons_label_rouge=10.0,
            value_boulangerie_aocaop_igp_stg=20.0,
            value_boulangerie_externalites=0,
            value_boissons_externalites=None,
        )

        # Create a teledeclaration for the complete diagnostic
        self.td_complete = Teledeclaration.objects.create(
            year=2020,
            declared_data={
                "teledeclaration": {
                    "diagnostic_type": "COMPLETE",
                    "value_total_ht": 200.0,
                    "value_boissons_label_rouge": 10.0,
                    "value_boulangerie_aocaop_igp_stg": 20.0,
                    "value_boulangerie_externalites": 0,
                    "value_boissons_externalites": None,
                },
                "canteen": {"yearly_meal_count": 1000},
            },
            diagnostic=diag_complete,
        )

    def test_migration_0171(self):
        Teledeclaration = apps.get_model("data", "Teledeclaration")
        td_simple = Teledeclaration.objects.get(pk=self.td_simple.id)

        # Assert that the new fields exist and are populated correctly
        self.assertIsNotNone(td_simple.value_bio_ht_agg)
        self.assertIsNotNone(td_simple.value_total_ht)
        self.assertEqual(td_simple.value_total_ht, 100)
        self.assertIsNone(td_simple.value_sustainable_ht_agg)

        td_complete = Teledeclaration.objects.get(pk=self.td_complete.id)
        self.assertEqual(td_complete.value_sustainable_ht_agg, 10 + 20)
        self.assertEqual(td_complete.value_externality_performance_ht_agg, 0)
        self.assertEqual(td_complete.value_bio_ht_agg, None)
        self.assertEqual(td_complete.yearly_meal_count, 1000)
