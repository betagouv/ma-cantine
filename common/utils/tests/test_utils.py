from django.test import TestCase
from django.core.management import CommandError, call_command

from common.utils import utils as utils_utils
from common.models import CommandLog
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
    def test_ma_cantine_base_command_creates_command_log(self):
        # before
        self.assertEqual(CommandLog.objects.count(), 0)

        # call a command that inherits from MaCantineBaseCommand
        call_command("canteen_delete", "--canteen-siret-list", "92341284500011,23456789012345")

        # after
        self.assertEqual(CommandLog.objects.count(), 1)
        command_log = CommandLog.objects.first()
        self.assertEqual(command_log.command_name, "canteen_delete")
        self.assertEqual(command_log.input_data["options"]["canteen_siret_list"], "92341284500011,23456789012345")
        self.assertEqual(command_log.status, CommandLog.Status.SUCCESS)

    def test_ma_cantine_base_command_creates_event_log(self):
        call_command("canteen_delete", "--canteen-siret-list", "92341284500011,23456789012345")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.COMMAND)
        self.assertEqual(event_log.name, "canteen_delete")
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertIsNone(event_log.user)
        self.assertEqual(set(event_log.data.keys()), {"args", "options", "trigger", "seconds", "message"})
        self.assertEqual(event_log.data["trigger"], "manual")  # default
        self.assertEqual(event_log.data["options"]["canteen_siret_list"], "92341284500011,23456789012345")
        self.assertIsNone(event_log.data["message"])

    def test_ma_cantine_base_command_creates_event_log_on_failure(self):
        # unknown combination: the command raises a CommandError
        with self.assertRaises(CommandError):
            call_command("export_dataset", model="Canteen", destination="analysis")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.COMMAND)
        self.assertEqual(event_log.name, "export_dataset")
        self.assertEqual(event_log.status, EventLog.Status.FAILURE)
        self.assertIn("No dataset for Canteen (analysis)", event_log.data["message"])
        self.assertEqual(CommandLog.objects.get().status, CommandLog.Status.FAILURE)

    def test_ma_cantine_base_command_trigger(self):
        call_command("canteen_delete", "--canteen-siret-list", "92341284500011", "--trigger", "cron")

        self.assertEqual(EventLog.objects.get().data["trigger"], "cron")
        self.assertEqual(CommandLog.objects.get().input_data["options"]["trigger"], "cron")

    def test_ma_cantine_base_command_trigger_choices(self):
        with self.assertRaises(CommandError):
            call_command("canteen_delete", "--canteen-siret-list", "92341284500011", "--trigger", "celery")
