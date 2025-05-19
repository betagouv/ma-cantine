import csv
import datetime
import logging
import time

import redis as r
import requests
from django.conf import settings
from django.core.management import call_command
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.models.functions import Length
from django.utils import timezone
from sib_api_v3_sdk.rest import ApiException

import macantine.brevo as brevo
from api.views.utils import update_change_reason
from common.api.adresse import fetch_geo_data_from_code_csv
from common.api.recherche_entreprises import fetch_geo_data_from_siret
from common.utils import siret as utils_siret
from data.models import Canteen, User
from macantine.etl.utils import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)

from .celery import app
from .etl.analysis import ETL_ANALYSIS_CANTEEN, ETL_ANALYSIS_TELEDECLARATIONS
from .etl.open_data import ETL_OPEN_DATA_CANTEEN, ETL_OPEN_DATA_TELEDECLARATIONS

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


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
            brevo.send_sib_template(settings.TEMPLATE_ID_NO_CANTEEN_FIRST, parameters, user.email, to_name)
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
            brevo.send_sib_template(settings.TEMPLATE_ID_NO_CANTEEN_SECOND, parameters, user.email, to_name)
            logger.info(f"Second email sent to {user.get_full_name()} ({user.email})")
            user.email_no_canteen_second_reminder = today
            user.save()
        except ApiException as e:
            logger.exception(f"SIB error when sending second no-cantine reminder email to {user.username}:\n{e}")
        except Exception as e:
            logger.exception(f"Unable to send second no-cantine reminder email to {user.username}:\n{e}")


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

    logger.info("Create individually new Brevo users (allowing the update flag to be set)")
    users_to_create = User.objects.filter(Q(last_brevo_update__isnull=True))
    brevo.create_new_brevo_contacts(users_to_create, today)

    logger.info("Update existing Brevo contacts by batch")
    users_to_update = User.objects.filter(Q(last_brevo_update__lte=threshold))
    bulk_update_size = 100
    chunks = batched(users_to_update, bulk_update_size)
    brevo.update_existing_brevo_contacts(chunks, today)

    end = time.time()
    logger.info(f"update_brevo_contacts task ended. Duration : {end - start} seconds")


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
                brevo.send_sib_template(
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


def _get_candidate_canteens_for_code_geobot():
    return (
        Canteen.objects.has_postal_code_or_city_insee_code()
        .filter(Q(city=None) | Q(department=None) | Q(city_insee_code=None) | Q(postal_code=None))
        .filter(geolocation_bot_attempts__lt=20)
        .annotate(postal_code_len=Length("postal_code"))
        .annotate(city_insee_code_len=Length("city_insee_code"))
        .filter(Q(postal_code_len=5) | Q(city_insee_code_len=5))
        .order_by("creation_date")
    )


def _get_candidate_canteens_for_siret_geobot():
    return Canteen.objects.filter(siret__isnull=False).has_city_insee_code_missing().order_by("-creation_date")


def _get_candidate_canteens_for_epci_geobot():
    return (
        Canteen.objects.has_postal_code_or_city_insee_code()
        .filter(Q(epci=None) | Q(epci=""))
        .order_by("-creation_date")
    )


def _get_candidate_canteens_for_libelle_geobot():
    return Canteen.objects.filter(
        Q(department__isnull=False, department_lib__isnull=True)
        | Q(region__isnull=False, region_lib__isnull=True)
        | Q(epci__isnull=False, epci_lib__isnull=True)
    ).order_by("-creation_date")


def _fill_from_api_response(response, canteens):
    for row in csv.reader(response.splitlines()):
        if row[0] == "id":
            continue
        if row[5] != "":  # city found, so rest of data is found
            id = int(row[0])
            canteen = next(filter(lambda x: x.id == id, canteens), None)
            if not canteen:
                logger.info(f"INSEE Geolocation Bot - response row, ID not found: {id}")
                continue

            canteen.city_insee_code = row[3]
            canteen.postal_code = row[4]
            canteen.city = row[5]
            canteen.department = row[6].split(",")[0]  # e.g. "80, Somme, Hauts-de-France"
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
    """
    Input: Canteens with siret but no city_insee_code
    Processing: API Recherche Entreprises
    Output: Fill canteen's city_insee_code, postal_code & city fields
    """
    candidate_canteens = _get_candidate_canteens_for_siret_geobot()
    logger.info(f"Siret Geolocation Bot: about to fix {candidate_canteens.count()} canteens")
    counter = 0

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return
    for i, canteen in enumerate(candidate_canteens):
        logger.info(f"Traitement de la cantine {canteen.name} {canteen.siret}, appel #{i}")
        if utils_siret.is_valid_length_siret(canteen.siret):
            response = {}
            response = fetch_geo_data_from_siret(canteen.siret, response)
            if response:
                _update_canteen_geo_data(canteen, response)
                counter += 1
        # time.sleeps to avoid API rate limit
        if i > 1 and i % 7 == 0:
            logger.info("7 appels réalisés maximum par seconde...")
            time.sleep(1)
        if i > 1 and i % 200 == 0:
            logger.info("200 appels réalisés maximum par minute...")
            time.sleep(60)

    logger.info(f"Siret Geolocation Bot: Fixed {counter}/{candidate_canteens.count()} canteens")


@app.task()
def fill_missing_geolocation_data_using_insee_code_or_postcode():
    """
    Input: Canteens with postal_code or city_insee_code, but no city or department
    Processing: API Adresse (via csv batch)
    Output: Fill canteen's city & department fields
    """
    candidate_canteens = _get_candidate_canteens_for_code_geobot()
    candidate_canteens.update(geolocation_bot_attempts=F("geolocation_bot_attempts") + 1)
    paginator = Paginator(candidate_canteens, 70)
    logger.info(f"INSEE Geolocation Bot: about to fix {candidate_canteens.count()} canteens")
    counter = 0

    # Carry out the CSV
    for page_number in paginator:
        canteens = paginator.get_page(page_number).object_list
        if len(canteens) == 0:
            continue
        try:
            location_csv_string = _get_location_csv_string(canteens)
            response = fetch_geo_data_from_code_csv(location_csv_string, timeout=60)
            _fill_from_api_response(response, canteens)
            counter += 1
        except requests.exceptions.HTTPError as e:
            logger.info(f"INSEE Geolocation Bot error: HTTPError\n{e}")
        except requests.exceptions.ConnectionError as e:
            logger.info(f"INSEE Geolocation Bot error: ConnectionError\n{e}")
        except requests.exceptions.Timeout as e:
            logger.info(f"INSEE Geolocation Bot error: Timeout\n{e}")
        except Exception as e:
            logger.info(f"INSEE Geolocation Bot error: Unexpected exception\n{e}")

    logger.info(f"INSEE Geolocation Bot: Fixed {counter}/{candidate_canteens.count()} canteens")


@app.task()
def fill_missing_geolocation_epci_data_using_insee_code():
    """
    Input: Canteens with city_insee_code, but no epci
    Processing: API Découpage Administratif
    Output: Fill canteen's epci field (if found)
    """
    candidate_canteens = _get_candidate_canteens_for_epci_geobot()
    logger.info(f"EPCI Geolocation Bot: about to fix {candidate_canteens.count()} canteens")
    counter = 0

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return

    # fetch all the communes and their corrsponding epci via API
    communes_details = map_communes_infos()

    for i, canteen in enumerate(candidate_canteens):
        if not canteen.epci:
            canteen.epci = fetch_commune_detail(canteen.city_insee_code, communes_details, "epci")
            if canteen.epci:
                canteen.save()
                update_change_reason(canteen, "Données de localisation (epci) MAJ par bot, via code INSEE")
                counter += 1

    logger.info(f"EPCI Geolocation Bot: Fixed {counter}/{candidate_canteens.count()} canteens")


@app.task()
def fill_missing_geolocation_libelle_data():
    """
    Input: Canteens with department or region or epci, but no _lib equivalent
    Processing: use our internal geo mappings
    Output: Fill canteen's department_lib, region_lib & epci_lib fields
    """
    candidate_canteens = _get_candidate_canteens_for_libelle_geobot()
    logger.info(f"Libellé Geolocation Bot: about to fix {candidate_canteens.count()} canteens")
    counter = 0

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return

    # fetch all the epci via API
    epcis_names = map_epcis_code_name()

    for i, canteen in enumerate(candidate_canteens):
        update = False
        if canteen.department and not canteen.department_lib:
            canteen.department_lib = canteen.get_department_display()
            if canteen.department_lib:
                update = True
        if canteen.region and not canteen.region_lib:
            canteen.region_lib = canteen.get_region_display()
            if canteen.region_lib:
                update = True
        if canteen.epci and not canteen.epci_lib:
            canteen.epci_lib = fetch_epci_name(canteen.epci, epcis_names)
            if canteen.epci_lib:
                update = True
        if update:
            canteen.save()
            update_change_reason(canteen, "Données de localisation MAJ par bot, via mapping des libellés")
            counter += 1

    logger.info(f"Libellé Geolocation Bot: Fixed {counter}/{candidate_canteens.count()} canteens")


@app.task()
def delete_old_historical_records():
    if not settings.MAX_DAYS_HISTORICAL_RECORDS:
        logger.info("Environment variable MAX_DAYS_HISTORICAL_RECORDS not set. Old history items will not be removed.")
        return
    logger.info(f"History items older than {settings.MAX_DAYS_HISTORICAL_RECORDS} days will be removed.")
    call_command("clean_old_history", days=settings.MAX_DAYS_HISTORICAL_RECORDS, auto=True)


def export_datasets(datasets: dict):
    for key, etl in datasets.items():
        logger.info(f"Starting {key} dataset extraction")
        etl.extract_dataset()
        etl.transform_dataset()
        etl.load_dataset()


def manual_datasets_export():
    """
    Export the Teledeclarations datasets for data.gouv.fr
    This datasets are updated every year by adding a new campaign
    """
    logger.info("Starting manual datasets export")
    datasets = {
        "campagne teledeclaration 2021": ETL_OPEN_DATA_TELEDECLARATIONS(2021),
        "campagne teledeclaration 2022": ETL_OPEN_DATA_TELEDECLARATIONS(2022),
        "campagne teledeclaration 2023": ETL_OPEN_DATA_TELEDECLARATIONS(2023),
    }
    export_datasets(datasets)


@app.task()
def continous_datasets_export():
    """
    Export regulary and automatically datasets that are updated contiously
    """
    logger.info("Starting datasets extractions")
    datasets = {
        "cantines": ETL_OPEN_DATA_CANTEEN(),
        "cantines_analyses": ETL_ANALYSIS_CANTEEN(),
        "td_analyses": ETL_ANALYSIS_TELEDECLARATIONS(),
    }
    export_datasets(datasets)
