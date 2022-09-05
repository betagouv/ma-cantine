import logging
import datetime
import requests
import csv
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models.functions import Length
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
        opt_out_reminder_emails=False,
    ).all()
    if not users:
        logger.info("no_canteen_first_reminder: No users to notify.")
        return

    logger.info(f"no_canteen_first_reminder: {len(users)} users to notify.")
    for user in users:
        try:
            parameters = {"PRENOM": user.first_name}
            to_name = f"{user.first_name} {user.last_name}".strip() if user.first_name or user.last_name else None
            _send_sib_template(settings.TEMPLATE_ID_NO_CANTEEN_FIRST, parameters, user.email, to_name)
            logger.info(f"First email sent to {user.get_full_name()} ({user.email})")
            user.email_no_canteen_first_reminder = today
            user.save()
        except ApiException as e:
            logger.exception(f"SIB error when sending first no-cantine email to {user.username}:\n{e}")
        except Exception as e:
            logger.exception(f"Unable to send first no-cantine reminder email to {user.username}:\n{e}")


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
        opt_out_reminder_emails=False,
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
            logger.exception(f"SIB error when sending second no-cantine reminder email to {user.username}:\n{e}")
        except Exception as e:
            logger.exception(f"Unable to send second no-cantine reminder email to {user.username}:\n{e}")


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
        for manager in canteen.managers.filter(opt_out_reminder_emails=False):

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
                logger.exception(
                    f"SIB error when sending first no-diagnostic email to {manager.username} concerning canteen {canteen.name}:\n{e}"
                )
            except Exception as e:
                logger.exception(
                    f"Unable to send first no-diagnostic reminder email to {manager.username} concerning canteen {canteen.name}:\n{e}"
                )


def _get_location_csv_string(canteens):
    locations_csv_string = "id,citycode,postcode\n"
    for canteen in canteens:
        if canteen.city_insee_code and len(canteen.city_insee_code) == 5:
            locations_csv_string += f"{canteen.id},{canteen.city_insee_code},\n"
        elif canteen.postal_code and len(canteen.postal_code) == 5:
            locations_csv_string += f"{canteen.id},,{canteen.postal_code}\n"
    return locations_csv_string


def _request_location_api(location_csv_string):
    response = requests.post(
        "https://api-adresse.data.gouv.fr/search/csv/",
        files={
            "data": ("locations.csv", location_csv_string),
        },
        data={
            "postcode": "postcode",
            "citycode": "citycode",
            "result_columns": ["result_citycode", "result_postcode", "result_city", "result_context"],
        },
        timeout=60,
    )
    return response


def _get_candidate_canteens():
    candidate_canteens = (
        Canteen.objects.filter(Q(city=None) | Q(department=None))
        .filter(Q(postal_code__isnull=False) | Q(city_insee_code__isnull=False))
        .filter(geolocation_bot_attempts__lt=10)
        .annotate(postal_code_len=Length("postal_code"))
        .annotate(city_insee_code_len=Length("city_insee_code"))
        .filter(Q(postal_code_len=5) | Q(city_insee_code_len=5))
    )
    return candidate_canteens


def _fill_from_api_response(response, canteens):
    for row in csv.reader(response.text.splitlines()):
        if row[0] == "id":
            continue
        if row[5] != "":  # city found, so rest of data is found
            id = int(row[0])
            canteen = next(filter(lambda x: x.id == id, canteens), None)
            if not canteen:
                continue

            canteen.city_insee_code = row[3]
            canteen.postal_code = row[4]
            canteen.city = row[5]
            canteen.department = row[6].split(",")[0]
            canteen.save()


@app.task()
def fill_missing_geolocation_data():
    candidate_canteens = _get_candidate_canteens()
    candidate_canteens.update(geolocation_bot_attempts=F("geolocation_bot_attempts") + 1)
    paginator = Paginator(candidate_canteens, 70)
    logger.info(f"Geolocation Bot: about to query {candidate_canteens.count()} canteens")

    # Carry out the CSV
    for page_number in paginator:
        canteens = paginator.get_page(page_number).object_list
        if len(canteens) == 0:
            continue
        try:
            location_csv_string = _get_location_csv_string(canteens)
            response = _request_location_api(location_csv_string)
            response.raise_for_status()

            _fill_from_api_response(response, canteens)
        except requests.exceptions.HTTPError as e:
            logger.exception(f"Geolocation Bot error: HTTPError\n{e}")
        except requests.exceptions.ConnectionError as e:
            logger.exception(f"Geolocation Bot error: ConnectionError\n{e}")
        except requests.exceptions.Timeout as e:
            logger.exception(f"Geolocation Bot error: Timeout\n{e}")
        except Exception as e:
            logger.exception(f"Geolocation Bot error: Unexpected exception\n{e}")

    logger.info(f"Geolocation Bot: Ended process for {candidate_canteens.count()} canteens")
