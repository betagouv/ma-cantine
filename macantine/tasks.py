import datetime
import logging
import time

import redis as r
from django.conf import settings
from django.core.management import call_command
from django.db.models import F, Q
from django.db.models.functions import Length
from django.utils import timezone
from sib_api_v3_sdk.rest import ApiException

import macantine.brevo as brevo
from api.views.utils import update_change_reason
from common.api.decoupage_administratif import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)
from common.api.recherche_entreprises import fetch_geo_data_from_siret
from common.utils import siret as utils_siret
from data.department_choices import get_lib_department_from_code
from data.models import Canteen, User
from data.region_choices import get_lib_region_from_code
from data.utils import has_charfield_missing_query

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


def _get_candidate_canteens_for_insee_code_geobot():
    return (
        Canteen.objects.has_city_insee_code()
        .filter(
            has_charfield_missing_query("city")
            | has_charfield_missing_query("postal_code")
            | has_charfield_missing_query("department")
            | has_charfield_missing_query("department_lib")
            | has_charfield_missing_query("region")
            | has_charfield_missing_query("region_lib")
            | has_charfield_missing_query("epci")
            | has_charfield_missing_query("epci_lib")
        )
        .filter(geolocation_bot_attempts__lt=20)
        .annotate(city_insee_code_len=Length("city_insee_code"))
        .filter(city_insee_code_len=5)
        .order_by("creation_date")
    )


def _get_candidate_canteens_for_siret_geobot():
    return Canteen.objects.has_siret().has_city_insee_code_missing().order_by("-creation_date")


def _update_canteen_geo_data_from_siret(canteen, response):
    try:
        if "cityInseeCode" in response.keys():
            canteen.city_insee_code = response["cityInseeCode"]
            # TODO: remove this, leave it to the other geo bot
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
                _update_canteen_geo_data_from_siret(canteen, response)
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
def fill_missing_geolocation_data_using_insee_code():  # noqa C901
    """
    Input: Canteens with city_insee_code, but no postal_code or city or epci or department or region
    Processing: API Découpage Administratif
    Output: Fill canteen's postal_code, city, epci, department & region fields
    """
    candidate_canteens = _get_candidate_canteens_for_insee_code_geobot()
    candidate_canteens.update(geolocation_bot_attempts=F("geolocation_bot_attempts") + 1)
    logger.info(f"INSEE Geolocation Bot: about to fix {candidate_canteens.count()} canteens")
    counter = 0

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return

    # fetch geo data from API Découpage Administratif
    communes_details = map_communes_infos()
    epcis_names = map_epcis_code_name()

    for i, canteen in enumerate(candidate_canteens):
        update = False
        # geo fields
        if canteen.city_insee_code in communes_details:
            if not canteen.postal_code:
                postal_code_list = fetch_commune_detail(canteen.city_insee_code, communes_details, "postal_code_list")
                if postal_code_list:
                    canteen.postal_code = postal_code_list[0]
                    update = True
            if not canteen.city:
                canteen.city = fetch_commune_detail(canteen.city_insee_code, communes_details, "city")
                update = True
            if not canteen.epci:
                canteen.epci = fetch_commune_detail(canteen.city_insee_code, communes_details, "epci")
                update = True
            if not canteen.department:
                canteen.department = fetch_commune_detail(canteen.city_insee_code, communes_details, "department")
                update = True
            if not canteen.region:
                canteen.region = fetch_commune_detail(canteen.city_insee_code, communes_details, "region")
                update = True
        # geo lib fields
        if canteen.epci and not canteen.epci_lib and canteen.epci in epcis_names:
            canteen.epci_lib = fetch_epci_name(canteen.epci, epcis_names)
            update = True
        if canteen.department and not canteen.department_lib:
            canteen.department_lib = get_lib_department_from_code(canteen.department)
            update = True
        if canteen.region and not canteen.region_lib:
            canteen.region_lib = get_lib_region_from_code(canteen.region)
            update = True
        if update:
            canteen.save()
            update_change_reason(canteen, "Données de localisation MAJ par bot, via code INSEE")
            counter += 1

    logger.info(f"INSEE Geolocation Bot: Fixed {counter}/{candidate_canteens.count()} canteens")


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
        # etl.load_dataset()


def datasets_export_analysis_td():
    """
    Export the Teledeclarations datasets for Metabase
    """
    logger.info("Starting manual datasets export")
    datasets = {
        "td_analyses": ETL_ANALYSIS_TELEDECLARATIONS(),
    }
    export_datasets(datasets)


def datasets_export_opendata_td():
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


def datasets_export_opendata_canteens():
    """
    Export regulary and automatically datasets that are updated contiously
    """
    logger.info("Starting datasets extractions")
    datasets = {
        "cantines": ETL_OPEN_DATA_CANTEEN(),
    }
    export_datasets(datasets)


def datasets_export_analysis_canteens():
    """
    Export regulary and automatically datasets that are updated contiously
    """
    logger.info("Starting datasets extractions")
    datasets = {
        "cantines_analyses": ETL_ANALYSIS_CANTEEN(),
    }
    export_datasets(datasets)


@app.task()
def continous_datasets_export():
    """
    Export regulary and automatically datasets that are updated contiously
    """
    datasets_export_analysis_canteens()
    datasets_export_analysis_canteens()
