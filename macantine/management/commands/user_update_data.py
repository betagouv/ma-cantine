import logging
import time

from common.utils.commands import MaCantineBaseCommand
from data.models import User

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Update the calculated fields in User.data (JSONField): canteen & diagnostic stats
    (used by the Brevo contacts sync, see user_update_brevo_contacts)

    Usage:
    - python manage.py user_update_data
    """

    help = "Update the calculated fields in User.data"

    def handle(self, *args, **options):
        logger.info("Start task: user_update_data")
        start = time.time()

        users_qs = User.objects.with_canteen_stats().with_canteen_diagnostic_stats()
        for user in users_qs:
            user.update_data()

        end = time.time()
        logger.info(f"Updated {users_qs.count()} users in {end - start:.2f} seconds")
