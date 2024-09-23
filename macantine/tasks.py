import csv
import datetime
import logging
import time

import redis as r
import requests
import sib_api_v3_sdk
from django.conf import settings
from django.core.management import call_command
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.models.functions import Length
from django.utils import timezone
from sib_api_v3_sdk.rest import ApiException

from api.views.utils import update_change_reason
from common.utils import get_token_sirene
from data.models import Canteen, User

from .celery import app
from .etl.analysis import ETL_ANALYSIS
from .etl.open_data import ETL_CANTEEN, ETL_TD
from .utils import fetch_geo_data_from_api_insee_sirene_by_siret

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
api_client = sib_api_v3_sdk.ApiClient(configuration)
email_api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
contacts_api_instance = sib_api_v3_sdk.ContactsApi(api_client)


def _send_sib_template(template_id, parameters, to_email, to_name):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}],
        params=parameters,
        sender={"email": settings.CONTACT_EMAIL, "name": "ma cantine"},
        reply_to={"email": settings.CONTACT_EMAIL, "name": "ma cantine"},
        template_id=template_id,
    )
    email_api_instance.send_transac_email(send_smtp_email)


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


def user_to_brevo_payload(user, bulk=True):
    has_canteens = user.canteens.exists()
    date_joined = user.date_joined

    def missing_diag_for_year(year, user):
        return user.canteens.exists() and any(not x.has_diagnostic_for_year(year) for x in user.canteens.all())

    def missing_td_for_year(year, user):
        return user.canteens.exists() and any(not x.has_teledeclaration_for_year(year) for x in user.canteens.all())

    missing_publications = (
        has_canteens and user.canteens.filter(publication_status=Canteen.PublicationStatus.DRAFT).exists()
    )

    dict_attributes = {
        "MA_CANTINE_DATE_INSCRIPTION": date_joined.strftime("%Y-%m-%d"),
        "MA_CANTINE_COMPTE_DEV": user.is_dev,
        "MA_CANTINE_COMPTE_ELU_E": user.is_elected_official,
        "MA_CANTINE_GERE_UN_ETABLISSEMENT": has_canteens,
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2023": missing_diag_for_year(2023, user),
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2022": missing_diag_for_year(2022, user),
        "MA_CANTINE_MANQUE_BILAN_DONNEES_2021": missing_diag_for_year(2021, user),
        "MA_CANTINE_MANQUE_TD_DONNEES_2023": missing_td_for_year(2023, user),
        "MA_CANTINE_MANQUE_TD_DONNEES_2022": missing_td_for_year(2022, user),
        "MA_CANTINE_MANQUE_TD_DONNEES_2021": missing_td_for_year(2021, user),
        "MA_CANTINE_MANQUE_PUBLICATION": missing_publications,
    }
    if bulk:
        return sib_api_v3_sdk.UpdateBatchContactsContacts(email=user.email, attributes=dict_attributes)
    return sib_api_v3_sdk.CreateContact(email=user.email, attributes=dict_attributes, update_enabled=True)


##########################################################################
# Taken from itertools recipes. Will be able to remove once we pass to
# Python 3.12 since they added it as itertools.batched. Server is currently
# on Python 3.11
from itertools import islice  # noqa: E402


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


##########################################################################


@app.task()
def update_brevo_contacts():
    """
    Send custom information on Brevo contacts for automatisation
    API rate limit is 10 req per second : https://developers.brevo.com/docs/api-limits
    """
    logger.info("update_brevo_contacts task starting")
    start = time.time()
    # This call concerns the users that have not been updated in the last day
    today = timezone.now()
    threshold = today - datetime.timedelta(days=1)

    # Attempt a bulk update first to save API calls
    users_to_update = User.objects.filter(Q(last_brevo_update__lte=threshold) | Q(last_brevo_update__isnull=True))
    bulk_update_size = 100
    chunks = batched(users_to_update, bulk_update_size)

    logger.info("update_brevo_contacts batch updating started")

    for chunk in chunks:
        contacts = [user_to_brevo_payload(user) for user in chunk]
        update_object = sib_api_v3_sdk.UpdateBatchContacts(contacts)
        try:
            contacts_api_instance.update_batch_contacts(update_object)
            for user in chunk:
                user.last_brevo_update = today
                user.save()
        except Exception as e:
            logger.exception(f"Error bulk updating Brevo users {e}", stack_info=True)
        time.sleep(0.1)  # API rate limit is 10 req per second

    # Try creating those who didn't make it (allowing the update flag to be set)
    users_to_update = User.objects.filter(Q(last_brevo_update__lte=threshold) | Q(last_brevo_update__isnull=True))
    logger.info("update_brevo_contacts individual creating/updating started")

    for user in users_to_update:
        try:
            contact = user_to_brevo_payload(user, bulk=False)
            contacts_api_instance.create_contact(contact)
            user.last_brevo_update = today
            user.save()
        except Exception as e:
            logger.exception(f"Error creating/updating an individual Brevo user {e}", stack_info=True)
        time.sleep(0.1)  # API rate limit is 10 req per second

    end = time.time()
    logger.info(f"update_brevo_contacts task ended. Duration : { end - start } seconds")


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


def _request_location_api_in_bulk(location_csv_string):
    response = requests.post(
        "https://api-adresse.data.gouv.fr/search/csv/",
        files={
            "data": ("locations.csv", location_csv_string),
        },
        data={
            "postcode": "postcode",
            "citycode": "citycode",
            "result_columns": [
                "result_citycode",
                "result_postcode",
                "result_city",
                "result_context",
            ],
        },
        timeout=60,
    )
    return response


def _get_candidate_canteens_for_code_geobot():
    candidate_canteens = (
        Canteen.objects.filter(Q(city=None) | Q(department=None) | Q(city_insee_code=None) | Q(postal_code=None))
        .filter(Q(postal_code__isnull=False) | Q(city_insee_code__isnull=False))
        .filter(geolocation_bot_attempts__lt=10)
        .annotate(postal_code_len=Length("postal_code"))
        .annotate(city_insee_code_len=Length("city_insee_code"))
        .filter(Q(postal_code_len=5) | Q(city_insee_code_len=5))
        .order_by("creation_date")
    )
    return candidate_canteens


def _get_candidate_canteens_for_siret_geobot():
    return Canteen.objects.filter(city_insee_code__isnull=True, siret__isnull=False).order_by("creation_date")


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
            update_change_reason(canteen, "Données de localisation MAJ par bot, via code INSEE ou code postale")


def _update_canteen_geo_data(canteen, response):
    try:
        if "cityInseeCode" in response.keys():
            canteen.city_insee_code = response["cityInseeCode"]
            canteen.postal_code = response["postalCode"]
            canteen.city = response["city"]
            canteen.save()
            update_change_reason(canteen, "Données de localisation MAJ par bot, via SIRET")
            logger.info(f"Canteen info has been updated. Canteen name : {canteen.name}")
    except Exception as e:
        logger.error(f"Unable to update canteen info for canteen : {canteen.name}")
        logger.error(e)


@app.task()
def fill_missing_geolocation_data_using_siret():
    candidate_canteens = _get_candidate_canteens_for_siret_geobot()
    token = get_token_sirene()

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return
    for canteen in candidate_canteens:
        if len(canteen.siret) == 14:
            response = {}
            response = fetch_geo_data_from_api_insee_sirene_by_siret(canteen.siret, response, token)
            if response:
                _update_canteen_geo_data(canteen, response)

    logger.info(f"Siret Geolocation Bot: Ended process for {candidate_canteens.count()} canteens")


@app.task()
def fill_missing_geolocation_data_using_insee_code_or_postcode():
    candidate_canteens = _get_candidate_canteens_for_code_geobot()
    candidate_canteens.update(geolocation_bot_attempts=F("geolocation_bot_attempts") + 1)
    paginator = Paginator(candidate_canteens, 70)
    logger.info(f"INSEE Geolocation Bot: about to query {candidate_canteens.count()} canteens")

    # Carry out the CSV
    for page_number in paginator:
        canteens = paginator.get_page(page_number).object_list
        if len(canteens) == 0:
            continue
        try:
            location_csv_string = _get_location_csv_string(canteens)
            response = _request_location_api_in_bulk(location_csv_string)
            response.raise_for_status()

            _fill_from_api_response(response, canteens)
        except requests.exceptions.HTTPError as e:
            logger.info(f"INSEE Geolocation Bot error: HTTPError\n{e}")
        except requests.exceptions.ConnectionError as e:
            logger.info(f"INSEE Geolocation Bot error: ConnectionError\n{e}")
        except requests.exceptions.Timeout as e:
            logger.info(f"INSEE Geolocation Bot error: Timeout\n{e}")
        except Exception as e:
            logger.info(f"INSEE Geolocation Bot error: Unexpected exception\n{e}")

    logger.info(f"INSEE Geolocation Bot: Ended process for {candidate_canteens.count()} canteens")


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
        "campagne teledeclaration 2021": ETL_TD(2021),
        "campagne teledeclaration 2022": ETL_TD(2022),
        "cantines": ETL_CANTEEN(),
        "td_analyses": ETL_ANALYSIS(),
    }
    for key, etl in datasets.items():
        logger.info(f"Starting {key} dataset extraction")
        etl.extract_dataset()
        etl.transform_dataset()
        etl.load_dataset()
