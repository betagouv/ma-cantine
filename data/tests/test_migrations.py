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


class TagsTestCase(TestMigrations):
    migrate_from = "0166_historicalteledeclaration_value_bio_ht_agg_and_more"
    migrate_to = "0167_populate_fields"

    def setUpBeforeMigration(self, apps):
        Teledeclaration = apps.get_model("data", "Teledeclaration")

        # Create a test for a simple Teledeclaration object
        self.td_simple = Teledeclaration.objects.create(
            year=2021,
            declared_data={
                "teledeclaration": {"diagnostic_type": "SIMPLE", "value_total_ht": 100.0, "value_bio_ht": 100.0},
                "canteen": {"yearly_meal_count": 10.0},
            },
        )
        # Create a test for a complete Teledeclaration object
        self.td_complete = Teledeclaration.objects.create(
            year=2020,
            declared_data={
                "teledeclaration": {
                    "diagnostic_type": "COMPLETE",
                    "value_total_ht": 100.0,
                    "value_bio_ht": 10.0,
                    "value_boissons_label_rouge_ht": 10.0,
                    "value_boulangerie_aocaop_igp_stg": 10.0,
                },
                "canteen": {"yearly_meal_count": 10.0},
            },
        )

    def test_migration_0166(self):
        Teledeclaration = apps.get_model("data", "Teledeclaration")
        td_simple = Teledeclaration.objects.get(pk=self.td_simple.id)

        # Assert that the new fields exist and are populated correctly
        self.assertIsNotNone(td_simple.value_bio_ht_agg)
        self.assertIsNotNone(td_simple.value_total_ht)

        td_complete = Teledeclaration.objects.get(pk=self.td_complete.id)
        self.assertEqual(td_complete.value_sustainable_ht_agg, 20)
