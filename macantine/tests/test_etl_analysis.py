from django.db import connection
from django.test import TestCase
from django.utils import timezone

from data.factories import (
    AccessTokenFactory,
    ApplicationFactory,
    CanteenFactory,
    EventLogFactory,
    RefreshTokenFactory,
    UserFactory,
)
from data.models import Canteen, EventLog, Sector, User
from macantine.etl.analysis import ETL_ANALYSIS_RAW
from macantine.etl.data_ware_house import copy_into_table, get_column_types
from macantine.tasks import get_raw_analysis_datasets


def copy_into_test_db(file, table, column_types):
    """Use the test database as the Data Warehouse"""
    with connection.cursor() as cursor:
        copy_into_table(cursor, table, column_types, file)


def fetch_all(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


class RawETLAnalysisTest(TestCase):
    def run_etl(self, etl):
        etl.warehouse.copy_file = copy_into_test_db
        etl.extract_dataset()
        etl.transform_dataset()
        etl.load_dataset()

    def test_copy_canteens(self):
        canteen = CanteenFactory(sector_list=[Sector.SANTE_HOPITAL])
        CanteenFactory(deletion_date=timezone.now())

        self.run_etl(ETL_ANALYSIS_RAW("test_canteens_raw", Canteen.all_objects.all()))

        self.assertEqual(fetch_all('SELECT count(*) FROM "test_canteens_raw"'), [(2,)])
        self.assertEqual(
            fetch_all(f'SELECT name, sector_list FROM "test_canteens_raw" WHERE id = {canteen.id}'),
            [(canteen.name, f'["{Sector.SANTE_HOPITAL}"]')],  # jsonb (not parsed by Django)
        )
        with connection.cursor() as cursor:
            column_types = get_column_types(cursor, "test_canteens_raw")
        self.assertEqual(column_types["sector_list"], "jsonb")  # array converted
        self.assertEqual(column_types["creation_date"], "timestamp with time zone")

    def test_exclude_columns(self):
        UserFactory()

        etl = ETL_ANALYSIS_RAW("test_users_raw", User.objects.all(), exclude_columns=["password"])
        self.run_etl(etl)

        self.assertNotIn("password", etl.column_types)
        with connection.cursor() as cursor:
            self.assertNotIn("password", get_column_types(cursor, "test_users_raw"))
        self.assertEqual(fetch_all('SELECT count(*) FROM "test_users_raw"'), [(1,)])

    def test_exclude_unknown_column(self):
        etl = ETL_ANALYSIS_RAW("test_users_raw", User.objects.all(), exclude_columns=["passwrd"])

        with self.assertRaises(ValueError):
            etl.extract_dataset()

    def test_reload_keeps_table_and_adds_new_columns(self):
        user = UserFactory()
        CanteenFactory(managers=[user])
        with connection.cursor() as cursor:
            cursor.execute('CREATE TABLE "test_canteen_managers_raw" (canteen_id bigint, user_id bigint)')
            cursor.execute('INSERT INTO "test_canteen_managers_raw" VALUES (0, 0), (0, 1)')
            cursor.execute('CREATE VIEW "test_stg_canteen_managers" AS SELECT * FROM "test_canteen_managers_raw"')

        self.run_etl(ETL_ANALYSIS_RAW("test_canteen_managers_raw", Canteen.managers.through.objects.all()))

        self.assertEqual(fetch_all('SELECT user_id FROM "test_canteen_managers_raw"'), [(user.id,)])
        self.assertEqual(fetch_all('SELECT user_id FROM "test_stg_canteen_managers"'), [(user.id,)])  # view kept
        with connection.cursor() as cursor:
            self.assertIn("id", get_column_types(cursor, "test_canteen_managers_raw"))  # column added

    def test_reload_recreates_table_if_column_type_changed(self):
        CanteenFactory()
        with connection.cursor() as cursor:
            cursor.execute('CREATE TABLE "test_canteens_raw" (id integer, sector_list text)')
            cursor.execute('CREATE VIEW "test_stg_canteens" AS SELECT * FROM "test_canteens_raw"')

        self.run_etl(ETL_ANALYSIS_RAW("test_canteens_raw", Canteen.all_objects.all()))

        self.assertEqual(fetch_all('SELECT count(*) FROM "test_canteens_raw"'), [(1,)])
        with connection.cursor() as cursor:
            self.assertEqual(get_column_types(cursor, "test_canteens_raw")["sector_list"], "jsonb")
            self.assertEqual(get_column_types(cursor, "test_stg_canteens"), {})  # dependent view dropped

    def test_copy_event_logs(self):
        canteen = CanteenFactory()
        EventLogFactory(canteen=canteen, data={"message": None, "count": 3, "seconds": 1.2})

        etl = get_raw_analysis_datasets()["event_logs_raw_analysis"]
        etl.dataset_name = "test_event_logs_raw"
        self.run_etl(etl)

        self.assertEqual(
            fetch_all('SELECT category, name, status, canteen_id, data FROM "test_event_logs_raw"'),
            [
                (
                    EventLog.Category.IMPORT,
                    "PURCHASE_SIRET",
                    EventLog.Status.SUCCESS,
                    canteen.id,
                    '{"count": 3, "message": null, "seconds": 1.2}',  # jsonb (not parsed by Django)
                )
            ],
        )
        with connection.cursor() as cursor:
            self.assertEqual(get_column_types(cursor, "test_event_logs_raw")["data"], "jsonb")


class OAuth2RawETLAnalysisTest(TestCase):
    def test_secrets_are_not_exported(self):
        user = UserFactory()
        application = ApplicationFactory(user=user, client_secret="client-secret-value")
        access_token = AccessTokenFactory(
            user=user, application=application, token="access-token-value", scope="user:read"
        )
        RefreshTokenFactory(user=user, application=application, token="refresh-token-value", access_token=access_token)
        application.refresh_from_db()
        access_token.refresh_from_db()
        secrets = [
            "client-secret-value",
            application.client_secret,  # hashed
            "access-token-value",
            access_token.token_checksum,
            "refresh-token-value",
        ]

        datasets = get_raw_analysis_datasets()
        for key in [
            "oauth2_applications_raw_analysis",
            "oauth2_applications_extra_raw_analysis",
            "oauth2_access_tokens_raw_analysis",
            "oauth2_refresh_tokens_raw_analysis",
        ]:
            with self.subTest(key):
                etl = datasets[key]
                etl.warehouse.copy_file = copy_into_test_db
                etl.extract_dataset()
                etl.file.seek(0)
                content = etl.file.read().decode()
                etl.load_dataset()

                self.assertEqual(len(content.splitlines()), 1)
                for secret in secrets:
                    self.assertNotIn(secret, content)
                with connection.cursor() as cursor:
                    exported_columns = get_column_types(cursor, etl.dataset_name)
                for column in ["client_secret", "token", "token_checksum"]:
                    self.assertNotIn(column, exported_columns)
