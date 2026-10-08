import logging
import time

import sentry_sdk
from django.conf import settings
from django.core.management.base import CommandError

from common.utils.commands import MaCantineBaseCommand
from macantine import tasks

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Run a task (function) of macantine/tasks.py
    Called by the crons defined in clevercloud/cron.json (see docs/cron.md)

    - every run is logged in CommandLog (visible in the admin)
    - if the task fails, the exception is sent to Sentry

    Usage:
    - python manage.py run_task update_user_data
    - python manage.py run_task dbt_run --prod-only  # does nothing outside of prod
    """

    help = "Run a task of macantine/tasks.py"

    def add_arguments(self, parser):
        parser.add_argument("task_name", type=str, help="Name of the function in macantine/tasks.py")
        parser.add_argument(
            "--prod-only",
            action="store_true",
            help="Only run the task if ENVIRONMENT is 'prod'",
        )

    def handle(self, *args, **options):
        task_name = options["task_name"]

        task = getattr(tasks, task_name, None)
        # only the functions defined in macantine/tasks.py (not the imported ones)
        if not callable(task) or task_name.startswith("_") or task.__module__ != tasks.__name__:
            raise CommandError(f"Unknown task: {task_name}")

        if options["prod_only"] and settings.ENVIRONMENT != "prod":
            logger.info(f"Skip task: {task_name} (prod only, ENVIRONMENT is {settings.ENVIRONMENT})")
            return

        logger.info(f"Start task: {task_name}")
        start = time.time()
        try:
            result = task()
        except Exception as e:
            with sentry_sdk.new_scope() as scope:
                scope.set_tag("task", task_name)
                sentry_sdk.capture_exception(e)
            # the process exits right after: make sure the event is sent
            sentry_sdk.flush()
            raise
        end = time.time()
        logger.info(f"End task: {task_name} in {end - start:.2f} seconds. Result: {result}")
