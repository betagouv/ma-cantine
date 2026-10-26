import logging
import time
from itertools import islice

from django.utils import timezone

import macantine.brevo as brevo
from common.utils.commands import MaCantineBaseCommand
from data.models import User

logger = logging.getLogger(__name__)


def batched(iterable, n):
    """
    Batch data into lists of length n. The last batch may be shorter.
    Taken from the itertools recipes: replace with itertools.batched once on Python 3.12
    """
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


class Command(MaCantineBaseCommand):
    """
    Send custom information on Brevo contacts (for the Brevo automations)
    - create the new contacts individually (allowing the update flag to be set)
    - update the existing contacts by batch
    API rate limit is 10 req per second: https://developers.brevo.com/docs/api-limits

    Run user_update_data before (it computes the User.data sent to Brevo)

    Usage:
    - python manage.py user_update_brevo_contacts
    """

    help = "Create & update the Brevo contacts"

    def handle(self, *args, **options):
        logger.info("Start task: user_update_brevo_contacts")
        start = time.time()

        logger.info("Create individually new Brevo users (allowing the update flag to be set)")
        users_to_create_qs = User.objects.brevo_to_create()
        brevo.create_new_brevo_contacts(users_to_create_qs, timezone.now())

        logger.info("Update existing Brevo contacts by batch")
        users_to_update_qs = User.objects.brevo_to_update()
        chunks = batched(users_to_update_qs, brevo.CONTACT_BULK_UPDATE_SIZE)
        brevo.update_existing_brevo_contacts(chunks, timezone.now())

        end = time.time()
        logger.info(
            f"Created {users_to_create_qs.count()} and updated {users_to_update_qs.count()} contacts "
            f"in {end - start:.2f} seconds"
        )
