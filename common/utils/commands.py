import logging
import io

from django.utils import timezone
from django.core.management.base import BaseCommand

from common.models import CommandLog


DJANGO_DEFAULT_OPTIONS = {"no_color", "settings", "traceback", "verbosity", "pythonpath", "force_color", "skip_checks"}


class MaCantineBaseCommand(BaseCommand):
    """
    Custom base command that automatically logs execution
    - creates a CommandLog entry
    - input_data: captures args (positional) & options (named)
    - output_data: captures INFO-level logs and above
    """

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
            end_date = timezone.now()
            log_contents = log_capture.getvalue()

            CommandLog.objects.create(
                command_name=command_name,
                input_data=input_data,
                status=CommandLog.Status.SUCCESS,
                output_data=log_contents,
                start_date=start_date,
                end_date=end_date,
            )
            return result
        except Exception as e:
            end_date = timezone.now()
            log_contents = log_capture.getvalue() + f"\nERROR: {str(e)}"

            CommandLog.objects.create(
                command_name=command_name,
                input_data=input_data,
                status=CommandLog.Status.FAILURE,
                output_data=log_contents,
                start_date=start_date,
                end_date=end_date,
            )
            raise e
        finally:
            root_logger.removeHandler(handler)
            root_logger.setLevel(original_level)
            log_capture.close()
