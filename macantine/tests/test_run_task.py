import json
from unittest import mock

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from common.models import CommandLog
from macantine import tasks


class RunTaskCommandTest(TestCase):
    @mock.patch("macantine.tasks.update_user_data", return_value="done")
    def test_runs_task_and_logs_it(self, task_mock):
        task_mock.__module__ = tasks.__name__

        call_command("run_task", "update_user_data")

        task_mock.assert_called_once_with()
        command_log = CommandLog.objects.get()
        self.assertEqual(command_log.command_name, "run_task")
        self.assertEqual(command_log.status, CommandLog.Status.SUCCESS)
        self.assertEqual(command_log.input_data["options"]["task_name"], "update_user_data")

    def test_unknown_task(self):
        with self.assertRaises(CommandError):
            call_command("run_task", "does_not_exist")

    def test_function_imported_in_tasks_module_is_not_a_task(self):
        self.assertTrue(hasattr(tasks, "call_command"))
        with self.assertRaises(CommandError):
            call_command("run_task", "call_command")

    @override_settings(ENVIRONMENT="staging")
    @mock.patch("macantine.tasks.dbt_run")
    def test_prod_only_task_is_skipped_outside_prod(self, task_mock):
        task_mock.__module__ = tasks.__name__

        call_command("run_task", "dbt_run", "--prod-only")

        task_mock.assert_not_called()
        self.assertEqual(CommandLog.objects.get().status, CommandLog.Status.SUCCESS)

    @override_settings(ENVIRONMENT="prod")
    @mock.patch("macantine.tasks.dbt_run", return_value="done")
    def test_prod_only_task_runs_in_prod(self, task_mock):
        task_mock.__module__ = tasks.__name__

        call_command("run_task", "dbt_run", "--prod-only")

        task_mock.assert_called_once_with()

    @mock.patch("macantine.management.commands.run_task.sentry_sdk.capture_exception")
    @mock.patch("macantine.tasks.dbt_run", side_effect=RuntimeError("boom"))
    def test_failing_task_is_sent_to_sentry_and_logged(self, task_mock, capture_exception_mock):
        task_mock.__module__ = tasks.__name__

        with self.assertRaises(RuntimeError):
            call_command("run_task", "dbt_run")

        capture_exception_mock.assert_called_once()
        self.assertEqual(str(capture_exception_mock.call_args.args[0]), "boom")
        self.assertEqual(CommandLog.objects.get().status, CommandLog.Status.FAILURE)


class CronJsonTest(TestCase):
    def test_crons_call_existing_tasks(self):
        with open(settings.BASE_DIR / "clevercloud" / "cron.json") as f:
            crons = json.load(f)

        self.assertTrue(crons)
        for cron in crons:
            # "M H d m Y command task_name [--prod-only]"
            parts = cron.split()
            self.assertEqual(len(parts[:5]), 5, cron)
            self.assertEqual(parts[5], "$ROOT/clevercloud/cron.sh", cron)
            task_name = parts[6]
            task = getattr(tasks, task_name, None)
            self.assertTrue(callable(task) and task.__module__ == tasks.__name__, cron)
            self.assertTrue(set(parts[7:]) <= {"--prod-only"}, cron)
