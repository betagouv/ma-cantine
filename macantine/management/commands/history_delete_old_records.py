import logging

from django.conf import settings
from django.core.management import call_command

from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Delete the history items (django-simple-history) older than MAX_DAYS_HISTORICAL_RECORDS days
    - does nothing if MAX_DAYS_HISTORICAL_RECORDS is not set (the history is kept forever)
    - calls the clean_old_history command of django-simple-history (on all the models with a history)

    Usage:
    - python manage.py history_delete_old_records
    """

    help = "Delete the history items older than MAX_DAYS_HISTORICAL_RECORDS days"

    def handle(self, *args, **options):
        logger.info("Start task: history_delete_old_records")

        if not settings.MAX_DAYS_HISTORICAL_RECORDS:
            logger.info(
                "Environment variable MAX_DAYS_HISTORICAL_RECORDS not set. Old history items will not be removed."
            )
            return

        logger.info(f"History items older than {settings.MAX_DAYS_HISTORICAL_RECORDS} days will be removed.")
        call_command("clean_old_history", days=settings.MAX_DAYS_HISTORICAL_RECORDS, auto=True)
