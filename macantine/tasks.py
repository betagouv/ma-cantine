import logging
import datetime
from django.utils import timezone
from django.conf import settings
from data.models import User, Canteen
from .celery import app
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


def _send_sib_template(template_id, parameters, to_email, to_name):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        params=parameters,
        sender={"email": settings.CONTACT_EMAIL, "name": "ma cantine"},
        reply_to={"email": settings.CONTACT_EMAIL, "name": "ma cantine"},
        template_id=template_id,
    )
    api_instance.send_transac_email(send_smtp_email)


@app.task()
def no_canteen_first_reminder():
    if not settings.TEMPLATE_ID_NO_CANTEEN_FIRST:
        logger.error("Environment variable TEMPLATE_ID_NO_CANTEEN_FIRST not set")
        return
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
            parameters = {"PRENOM": user.first_name}
            _send_sib_template(
                settings.TEMPLATE_ID_NO_CANTEEN_FIRST, parameters, user.email, f"{user.first_name} {user.last_name}"
            )
            logger.info(f"First email sent to {user.get_full_name()} ({user.email})")
            user.email_no_canteen_first_reminder = today
            user.save()
        except ApiException as e:
            logger.error(f"SIB error when sending first no-cantine email to {user.username}")
            logger.exception(e)
        except Exception as e:
            logger.error(f"Unable to send first no-cantine reminder email to {user.username}")
            logger.exception(e)


@app.task()
def no_canteen_second_reminder():
    if not settings.TEMPLATE_ID_NO_CANTEEN_SECOND:
        logger.error("Environment variable TEMPLATE_ID_NO_CANTEEN_SECOND not set")
        return
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
            parameters = {"PRENOM": user.first_name}
            _send_sib_template(
                settings.TEMPLATE_ID_NO_CANTEEN_SECOND, parameters, user.email, f"{user.first_name} {user.last_name}"
            )
            logger.info(f"Second email sent to {user.get_full_name()} ({user.email})")
            user.email_no_canteen_second_reminder = today
            user.save()
        except ApiException as e:
            logger.error(f"SIB error when sending second no-cantine reminder email to {user.username}")
            logger.exception(e)
        except Exception as e:
            logger.error(f"Unable to send second no-cantine reminder email to {user.username}")
            logger.exception(e)


@app.task()
def no_diagnostic_first_reminder():
    if not settings.TEMPLATE_ID_NO_DIAGNOSTIC_FIRST:
        logger.error("Environment variable TEMPLATE_ID_NO_DIAGNOSTIC_FIRST not set")
        return
    today = timezone.now()
    threshold = today - datetime.timedelta(weeks=1)
    canteens = Canteen.objects.filter(
        diagnostic__isnull=True,
        creation_date__lte=threshold,
        email_no_diagnostic_first_reminder__isnull=True,
    ).all()
    if not canteens:
        logger.info("no_diagnostic_first_reminder: No canteens to notify.")
        return

    logger.info(f"no_diagnostic_first_reminder: {len(canteens)} canteens to notify.")

    for canteen in canteens:
        for manager in canteen.managers.all():

            try:
                parameters = {"PRENOM": manager.first_name, "NOM_CANTINE": canteen.name}
                _send_sib_template(
                    settings.TEMPLATE_ID_NO_DIAGNOSTIC_FIRST,
                    parameters,
                    manager.email,
                    f"{manager.get_full_name()}",
                )
                logger.info(
                    f"First no-diagnostic email sent to {manager.get_full_name()} ({manager.email}) for canteen '{canteen.name}'."
                )
                if not canteen.email_no_diagnostic_first_reminder:
                    canteen.email_no_diagnostic_first_reminder = today
                    canteen.save()
            except ApiException as e:
                logger.error(
                    f"SIB error when sending first no-diagnostic email to {manager.username} concerning canteen {canteen.name}"
                )
                logger.exception(e)
            except Exception as e:
                logger.error(
                    f"Unable to send first no-diagnostic reminder email to {manager.username} concerning canteen {canteen.name}"
                )
                logger.exception(e)
