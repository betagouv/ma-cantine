import logging
import time

from common.utils.commands import MaCantineBaseCommand
from data.models import User

logger = logging.getLogger(__name__)

BATCH_SIZE = 1000


class Command(MaCantineBaseCommand):
    """
    Update the calculated fields in User.data (JSONField): canteen & diagnostic stats
    (used by the Brevo contacts sync, see user_update_brevo_contacts)
    - saved by batches with bulk_update: skips User.save() (validations, avatar optimization...),
      not needed to update a calculated field

    Usage:
    - python manage.py user_update_data
    """

    help = "Update the calculated fields in User.data"

    def handle(self, *args, **options):
        logger.info("Start task: user_update_data")
        start = time.time()

        users_qs = User.objects.with_canteen_stats().with_canteen_diagnostic_stats().only("id", "data")
        users_count = 0
        users_batch = []
        for user in users_qs.iterator(chunk_size=BATCH_SIZE):
            user.update_data(with_save=False)
            users_batch.append(user)
            if len(users_batch) == BATCH_SIZE:
                User.objects.bulk_update(users_batch, ["data"])
                users_count += len(users_batch)
                users_batch = []
        if users_batch:
            User.objects.bulk_update(users_batch, ["data"])
            users_count += len(users_batch)

        end = time.time()
        logger.info(f"Updated {users_count} users in {end - start:.2f} seconds")
