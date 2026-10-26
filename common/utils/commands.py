import logging
import io

from django.utils import timezone
from django.core.management.base import BaseCommand

from common.models import CommandLog
from data.models import EventLog


DJANGO_DEFAULT_OPTIONS = {"no_color", "settings", "traceback", "verbosity", "pythonpath", "force_color", "skip_checks"}
EVENT_LOG_MESSAGE_MAX_LENGTH = 1000
TRIGGER_CRON = "cron"
TRIGGER_MANUAL = "manual"


class MaCantineBaseCommand(BaseCommand):
    """
    Custom base command that automatically logs execution
    - creates a CommandLog entry
        - input_data: captures args (positional) & options (named)
        - output_data: captures INFO-level logs and above
    - creates an EventLog entry (category COMMAND)
        - data: args, options, trigger, seconds & message (the error, if the command failed)

    Every command gets a --trigger option: "cron" for the scheduled runs (clevercloud/cron.json), "manual" by default
    """

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super().create_parser(prog_name, subcommand, **kwargs)
        parser.add_argument(
            "--trigger",
            type=str,
            choices=[TRIGGER_CRON, TRIGGER_MANUAL],
            default=TRIGGER_MANUAL,
            help="How the command was started: cron (scheduled run) or manual (default).",
        )
        return parser

    def execute(self, *args, **options):
        # init
        command_name = self.__class__.__module__.split(".")[-1]
        input_data = {"args": args, "options": {k: v for k, v in options.items() if k not in DJANGO_DEFAULT_OPTIONS}}
        start_date = timezone.now()

        # logging
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        original_level = root_logger.level
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(handler)

        try:
            result = super().execute(*args, **options)
            self._log_run(command_name, input_data, start_date, log_capture.getvalue())
            return result
        except Exception as e:
            log_contents = log_capture.getvalue() + f"\nERROR: {str(e)}"
            self._log_run(command_name, input_data, start_date, log_contents, error=e)
            raise e
        finally:
            root_logger.removeHandler(handler)
            root_logger.setLevel(original_level)
            log_capture.close()

    @staticmethod
    def _log_run(command_name, input_data, start_date, log_contents, error=None):
        end_date = timezone.now()
        status = CommandLog.Status.FAILURE if error else CommandLog.Status.SUCCESS

        CommandLog.objects.create(
            command_name=command_name,
            input_data=input_data,
            status=status,
            output_data=log_contents,
            start_date=start_date,
            end_date=end_date,
        )
        # never raises (logging must not break the command)
        EventLog.log(
            category=EventLog.Category.COMMAND,
            name=command_name,
            status=EventLog.Status.FAILURE if error else EventLog.Status.SUCCESS,
            data={
                **input_data,
                "trigger": input_data["options"].get("trigger"),
                "seconds": round((end_date - start_date).total_seconds(), 2),
                "message": str(error)[:EVENT_LOG_MESSAGE_MAX_LENGTH] if error else None,
            },
        )
