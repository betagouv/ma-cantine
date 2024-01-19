import logging
import datetime
import requests
import csv
import os
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models.functions import Length
from django.core.management import call_command
from data.models import User, Canteen

from .celery import app
from .extract_open_data import ETL_TD, ETL_CANTEEN

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


def _user_name(user):
    return user.get_full_name() or user.username


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
        is_dev=False,
    ).all()
    if not users:
        logger.info("no_canteen_first_reminder: No users to notify.")
        return

    logger.info(f"no_canteen_first_reminder: {len(users)} users to notify.")
    for user in users:
        try:
            parameters = {"PRENOM": user.first_name}
            to_name = _user_name(user)
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
        is_dev=False,
    ).all()
    if not users:
        logger.info("no_canteen_second_reminder: No users to notify.")
        return

    logger.info(f"no_canteen_second_reminder: {len(users)} users to notify.")
    for user in users:
        try:
            parameters = {"PRENOM": user.first_name}
            to_name = _user_name(user)
            _send_sib_template(settings.TEMPLATE_ID_NO_CANTEEN_SECOND, parameters, user.email, to_name)
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
        if _covered_by_central_kitchen(canteen):
            continue

        for manager in canteen.managers.filter(opt_out_reminder_emails=False, is_dev=False):
            try:
                parameters = {"PRENOM": manager.first_name, "NOM_CANTINE": canteen.name}
                to_name = _user_name(manager)
                _send_sib_template(
                    settings.TEMPLATE_ID_NO_DIAGNOSTIC_FIRST,
                    parameters,
                    manager.email,
                    f"{to_name}",
                )
                logger.info(
                    f"First no-diagnostic email sent to {to_name} ({manager.email}) for canteen '{canteen.name}'."
                )
                if not canteen.email_no_diagnostic_first_reminder:
                    canteen.email_no_diagnostic_first_reminder = today
                    canteen.save()
            except ApiException as e:
                logger.exception(
                    f"SIB error when sending first no-diagnostic email to {to_name} concerning canteen {canteen.name}:\n{e}"
                )
            except Exception as e:
                logger.exception(
                    f"Unable to send first no-diagnostic reminder email to {to_name} concerning canteen {canteen.name}:\n{e}"
                )


def _covered_by_central_kitchen(canteen):
    if canteen.production_type == Canteen.ProductionType.ON_SITE_CENTRAL and canteen.central_producer_siret:
        try:
            central_kitchen = Canteen.objects.get(siret=canteen.central_producer_siret)
            covered_by_central_kitchen = central_kitchen.diagnostic_set.exists()
            return covered_by_central_kitchen
        except Canteen.DoesNotExist:
            pass
        except Canteen.MultipleObjectsReturned as e:
            logger.exception(f"Multiple central canteens detected on email task: {e}")
    return False


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
        .order_by("creation_date")
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
                logger.info(f"Geolocation Bot - response row, ID not found: {id}")
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
            logger.info(f"Geolocation Bot error: HTTPError\n{e}")
        except requests.exceptions.ConnectionError as e:
            logger.info(f"Geolocation Bot error: ConnectionError\n{e}")
        except requests.exceptions.Timeout as e:
            logger.info(f"Geolocation Bot error: Timeout\n{e}")
        except Exception as e:
            logger.info(f"Geolocation Bot error: Unexpected exception\n{e}")

    logger.info(f"Geolocation Bot: Ended process for {candidate_canteens.count()} canteens")


@app.task()
def delete_old_historical_records():
    if not settings.MAX_DAYS_HISTORICAL_RECORDS:
        logger.info("Environment variable MAX_DAYS_HISTORICAL_RECORDS not set. Old history items will not be removed.")
        return
    logger.info(f"History items older than {settings.MAX_DAYS_HISTORICAL_RECORDS} days will be removed.")
    call_command("clean_old_history", days=settings.MAX_DAYS_HISTORICAL_RECORDS, auto=True)


@app.task()
def export_datasets():
    logger.info("Starting datasets extractions")
    datasets = {
        'campagne teledeclaration 2021': ETL_TD(2021),
        'cantines': ETL_CANTEEN()
    }
    for key, etl in datasets.items():
        logger.info(f"Starting {key} dataset extraction")
        etl.extract_dataset()
        etl.export_dataset(stage='to_validate')
        logger.info(f"Validating {key} dataset. Dataset size : {etl.len_dataset()} lines")
        if os.environ['DEFAULT_FILE_STORAGE'] == 'storages.backends.s3boto3.S3Boto3Storage':
            if etl.is_valid():
                logger.info(f"Exporting {key} dataset to s3")
                etl.export_dataset(stage='validated')
            else:
                logger.error(f"The dataset {key} is invalid and therefore will not be exported to s3")
        elif os.environ['DEFAULT_FILE_STORAGE'] == 'django.core.files.storage.FileSystemStorage':
            logger.info(f"Saving {key} dataset locally")
            etl.export_dataset(stage='validated')
        else:
            logger.info("Exporting the dataset is not possible with the file system configured")

