from unittest import mock

from django.core.management import CommandError, call_command
from django.test import TestCase

from data.models import EventLog


@mock.patch("macantine.management.commands.export_dataset.export_datasets")
class ExportDatasetCommandTest(TestCase):
    def test_raw_analysis(self, export_datasets_mock):
        call_command("export_dataset", model="Raw", destination="analysis")

        datasets = export_datasets_mock.call_args.args[0]
        self.assertIn("canteens_raw_analysis", datasets)
        self.assertIn("event_logs_raw_analysis", datasets)
        self.assertEqual(
            EventLog.objects.get(category=EventLog.Category.COMMAND, name="export_dataset").status,
            EventLog.Status.SUCCESS,
        )

    def test_canteen_opendata(self, export_datasets_mock):
        call_command("export_dataset", model="Canteen", destination="opendata")

        self.assertEqual(list(export_datasets_mock.call_args.args[0]), ["canteens_opendata"])

    def test_teledeclaration_opendata(self, export_datasets_mock):
        call_command("export_dataset", model="Teledeclaration", destination="opendata")

        self.assertIn("teledeclarations_2024_opendata", export_datasets_mock.call_args.args[0])

    def test_unknown_combination_fails(self, export_datasets_mock):
        with self.assertRaises(CommandError):
            call_command("export_dataset", model="Canteen", destination="analysis")

        export_datasets_mock.assert_not_called()
        self.assertEqual(
            EventLog.objects.get(category=EventLog.Category.COMMAND, name="export_dataset").status,
            EventLog.Status.FAILURE,
        )
