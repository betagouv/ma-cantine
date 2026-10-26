import datetime
import importlib

from django.apps import apps
from django.test import TestCase
from django.utils import timezone

from common.models import CommandLog
from data.models import EventLog

migration = importlib.import_module("data.migrations.0294_eventlog_from_commandlog")

START_DATE = timezone.make_aware(datetime.datetime(2026, 3, 1, 2, 0))


def create_command_log(**kwargs):
    values = {
        "command_name": "canteen_delete",
        "input_data": {"args": [], "options": {"canteen_siret_list": "92341284500011", "apply": True}},
        "status": CommandLog.Status.SUCCESS,
        "output_data": "INFO - Start task: canteen_delete\n",
        "start_date": START_DATE,
        "end_date": START_DATE + datetime.timedelta(seconds=12.345),
    }
    values.update(kwargs)
    return CommandLog.objects.create(**values)


class EventLogFromCommandLogMigrationTest(TestCase):
    def test_copy_success(self):
        command_log = create_command_log()

        migration.copy_command_logs_to_event_logs(apps, None)

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.COMMAND)
        self.assertEqual(event_log.name, "canteen_delete")
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertIsNone(event_log.user)
        self.assertEqual(event_log.creation_date, START_DATE)
        self.assertEqual(
            event_log.data,
            {
                "args": [],
                "options": {"canteen_siret_list": "92341284500011", "apply": True},
                "trigger": None,
                "seconds": 12.35,
                "message": None,
                "commandlog_id": command_log.id,
            },
        )

    def test_copy_failure_message(self):
        create_command_log(
            status=CommandLog.Status.FAILURE,
            output_data="INFO - Start task: canteen_delete\n\nERROR: Canteen not found",
        )

        migration.copy_command_logs_to_event_logs(apps, None)

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.status, EventLog.Status.FAILURE)
        self.assertEqual(event_log.data["message"], "Canteen not found")

    def test_copy_without_dates_or_input_data(self):
        create_command_log(input_data={}, start_date=None, end_date=None)

        migration.copy_command_logs_to_event_logs(apps, None)

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.data["args"], [])
        self.assertEqual(event_log.data["options"], {})
        self.assertIsNone(event_log.data["seconds"])

    def test_copy_is_idempotent(self):
        create_command_log()
        create_command_log(command_name="dbt_run")

        migration.copy_command_logs_to_event_logs(apps, None)
        migration.copy_command_logs_to_event_logs(apps, None)

        self.assertEqual(EventLog.objects.count(), 2)

    def test_reverse_deletes_only_copied_event_logs(self):
        create_command_log()
        migration.copy_command_logs_to_event_logs(apps, None)
        EventLog.log(EventLog.Category.COMMAND, "dbt_run", EventLog.Status.SUCCESS)

        migration.delete_copied_event_logs(apps, None)

        self.assertEqual(EventLog.objects.count(), 1)
        self.assertEqual(CommandLog.objects.count(), 1)
