import json

from django.conf import settings
from django.core.management import get_commands, load_command_class
from django.test import SimpleTestCase

from common.utils.commands import MaCantineBaseCommand

CRON_JSON_PATH = settings.BASE_DIR / "clevercloud" / "cron.json"
CRON_SH = "$ROOT/clevercloud/cron.sh"


def get_cron_commands():
    """
    For each cron of clevercloud/cron.json: (cron line, command name, command options)
    "M H d m Y $ROOT/clevercloud/cron.sh [--prod-only] <command> [<command options>]"
    """
    crons = []
    for cron in json.loads(CRON_JSON_PATH.read_text()):
        parts = cron.split()
        assert parts[5] == CRON_SH, cron
        arguments = parts[6:]
        if arguments[0] == "--prod-only":
            arguments = arguments[1:]
        crons.append((cron, arguments[0], arguments[1:]))
    return crons


class CronTest(SimpleTestCase):
    def test_crons_call_existing_commands_with_valid_options(self):
        commands = get_commands()
        for cron, command_name, command_options in get_cron_commands():
            with self.subTest(cron):
                self.assertIn(command_name, commands)
                command = load_command_class(commands[command_name], command_name)
                # logged in CommandLog & EventLog, and accepts the --trigger option
                self.assertIsInstance(command, MaCantineBaseCommand)
                # the options are valid (cron.sh adds "--trigger cron")
                parser = command.create_parser("manage.py", command_name)
                parser.parse_args(command_options + ["--trigger", "cron"])
