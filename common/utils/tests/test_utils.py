from unittest import mock

from django.test import TestCase
from django.core.management import CommandError, call_command

from common.utils import commands as commands_utils
from common.utils import utils as utils_utils
from data.models import EventLog


class UtilsTest(TestCase):
    def test_normalize_string(self):
        for TUPLE in [
            (" 123 456 789 01234 ", "12345678901234"),
            ("215 903 501 00017", "21590350100017"),
            ("  215 90350100017  ", "21590350100017"),
            ("21590350100017", "21590350100017"),
            ("   ", ""),
            ("", ""),
            (None, None),
        ]:
            with self.subTest(text=TUPLE):
                self.assertEqual(utils_utils.normalize_string(TUPLE[0]), TUPLE[1])

    def test_clean_unicode_string(self):
        for TUPLE in [
            ("Caf<U+00E9>", "Café"),
            ("PAT dAzur", "PAT d'Azur"),
            ("foo\x92bar\x07baz", "foo'barbaz"),
        ]:
            with self.subTest(text=TUPLE):
                self.assertEqual(utils_utils.clean_unicode_string(TUPLE[0]), TUPLE[1])


class CommandsTest(TestCase):
    def test_ma_cantine_base_command_creates_event_log(self):
        call_command("canteen_delete", "--canteen-siret-list", "92341284500011,23456789012345")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.COMMAND)
        self.assertEqual(event_log.name, "canteen_delete")
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertIsNone(event_log.user)
        self.assertEqual(set(event_log.data.keys()), {"args", "options", "trigger", "seconds", "message", "output"})
        self.assertEqual(event_log.data["trigger"], "manual")  # default
        self.assertEqual(event_log.data["options"]["canteen_siret_list"], "92341284500011,23456789012345")
        self.assertIsNone(event_log.data["message"])
        self.assertIsInstance(event_log.data["output"], str)

    def test_ma_cantine_base_command_creates_event_log_on_failure(self):
        # unknown combination: the command raises a CommandError
        with self.assertRaises(CommandError):
            call_command("export_dataset", model="Canteen", destination="analysis")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.COMMAND)
        self.assertEqual(event_log.name, "export_dataset")
        self.assertEqual(event_log.status, EventLog.Status.FAILURE)
        self.assertIn("No dataset for Canteen (analysis)", event_log.data["message"])
        self.assertIn("ERROR: No dataset for Canteen (analysis)", event_log.data["output"])

    def test_ma_cantine_base_command_output_is_truncated(self):
        short_output = "INFO - Start task\n"
        self.assertEqual(commands_utils._truncate_output(short_output), short_output)

        long_output = "INFO - first line\n" + "INFO - line\n" * 2000 + "INFO - last line\n"
        output = commands_utils._truncate_output(long_output)
        self.assertEqual(
            len(output),
            commands_utils.EVENT_LOG_OUTPUT_MAX_LENGTH + len(commands_utils.EVENT_LOG_OUTPUT_TRUNCATION_MARKER),
        )
        self.assertTrue(output.startswith("INFO - first line\n"))
        self.assertIn(commands_utils.EVENT_LOG_OUTPUT_TRUNCATION_MARKER, output)
        self.assertTrue(output.endswith("INFO - last line\n"))

    def test_ma_cantine_base_command_trigger(self):
        call_command("canteen_delete", "--canteen-siret-list", "92341284500011", "--trigger", "cron")

        self.assertEqual(EventLog.objects.get().data["trigger"], "cron")
        self.assertEqual(EventLog.objects.get().data["options"]["trigger"], "cron")

    def test_ma_cantine_base_command_trigger_choices(self):
        with self.assertRaises(CommandError):
            call_command("canteen_delete", "--canteen-siret-list", "92341284500011", "--trigger", "celery")

    @mock.patch("common.utils.commands.sentry_sdk.capture_exception")
    def test_ma_cantine_base_command_failure_is_sent_to_sentry(self, capture_exception_mock):
        with self.assertRaises(CommandError):
            call_command("export_dataset", model="Canteen", destination="analysis")

        capture_exception_mock.assert_called_once()
        self.assertIn("No dataset for Canteen (analysis)", str(capture_exception_mock.call_args.args[0]))

    @mock.patch("common.utils.commands.sentry_sdk.capture_exception")
    def test_ma_cantine_base_command_success_is_not_sent_to_sentry(self, capture_exception_mock):
        call_command("canteen_delete", "--canteen-siret-list", "92341284500011")

        capture_exception_mock.assert_not_called()
