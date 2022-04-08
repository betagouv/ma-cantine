import logging
import datetime
from django.utils import timezone
from data.models import User
from .celery import app

logger = logging.getLogger(__name__)


@app.task()
def no_canteen_first_reminder():
    today = timezone.now()
    threshold = today - datetime.timedelta(weeks=1)
    users = User.objects.filter(
        canteens=None,
        date_joined__lte=threshold,
        email_no_canteen_first_reminder__isnull=True,
    ).all()
    if not users:
        logger.info("no_canteen_first_reminder: No users to notify.")
        return

    logger.info(f"no_canteen_first_reminder: {len(users)} users to notify.")
    for user in users:
        try:
            print(f"First email sent to {user.get_full_name()}")  # Send SIB template
            user.email_no_canteen_first_reminder = today
            user.save()
        except Exception as e:
            logger.error(f"Unable to send first no-cantine reminder email to {user.username}")
            logger.exception(e)


@app.task()
def no_canteen_second_reminder():
    today = timezone.now()
    threshold = today - datetime.timedelta(weeks=2)
    first_reminder_threshold = today - datetime.timedelta(weeks=1)
    users = User.objects.filter(
        canteens=None,
        date_joined__lte=threshold,
        email_no_canteen_first_reminder__lte=first_reminder_threshold,
        email_no_canteen_second_reminder__isnull=True,
    ).all()
    if not users:
        logger.info("no_canteen_second_reminder: No users to notify.")
        return

    logger.info(f"no_canteen_second_reminder: {len(users)} users to notify.")
    for user in users:
        try:
            print(f"Second email sent to {user.get_full_name()}")  # Send SIB template
            user.email_no_canteen_second_reminder = today
            user.save()
        except Exception as e:
            logger.error(f"Unable to send second no-cantine reminder email to {user.username}")
            logger.exception(e)
