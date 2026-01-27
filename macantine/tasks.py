import logging
import time

import redis as r
from django.conf import settings
from django.core.management import call_command
from django.db.models import F
from django.utils import timezone

import macantine.brevo as brevo
from api.views.utils import update_change_reason
from common.api.datagouv import (
    fetch_commune_pat_list,
    map_pat_list_to_communes_insee_code,
)
from common.api.decoupage_administratif import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)
from common.api.recherche_entreprises import fetch_geo_data_from_siret
from data.models.geo import get_lib_department_from_code, get_lib_region_from_code
from data.models import Canteen, User

from .celery import app
from .etl.analysis import ETL_ANALYSIS_CANTEEN, ETL_ANALYSIS_TELEDECLARATIONS
from .etl.open_data import ETL_OPEN_DATA_CANTEEN, ETL_OPEN_DATA_TELEDECLARATIONS

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


##########################################################################
# User data


@app.task()
def update_user_data():
    """
    Update calculated fields in User.data JSONField
    """
    logger.info("update_user_data task starting")
    start = time.time()
    users = User.objects.with_canteen_stats().with_canteen_diagnostic_stats()
    for user in users:
        user.update_data()
    end = time.time()
    logger.info(f"update_user_data task ended. Duration : {end - start} seconds")


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

    logger.info("Create individually new Brevo users (allowing the update flag to be set)")
    users_to_create = User.objects.brevo_to_create()
    brevo.create_new_brevo_contacts(users_to_create, timezone.now())

    logger.info("Update existing Brevo contacts by batch")
    users_to_update = User.objects.brevo_to_update()
    chunks = batched(users_to_update, brevo.CONTACT_BULK_UPDATE_SIZE)
    brevo.update_existing_brevo_contacts(chunks, timezone.now())

    end = time.time()
    logger.info(f"update_brevo_contacts task ended. Duration : {end - start} seconds")


@app.task()
def update_canteen_geo_fields_from_siret(canteen):
    """
    Input: Canteen with siret
    Processing: API Recherche Entreprises + API Découpage Administratif (cached)
    Output: Fill canteen's city_insee_code field + geo fields
    """
    # Step 1: fetch city_insee_code from API Recherche Entreprises
    if not canteen.city_insee_code:
        response = fetch_geo_data_from_siret(canteen.siret)
        if response:
            try:
                if "cityInseeCode" in response.keys():
                    canteen.city_insee_code = response["cityInseeCode"]
                    canteen.siret_etat_administratif = response["etat_administratif"]
                    update = True
            except Exception as e:
                logger.error(e)
        else:
            if not canteen.siret_inconnu:
                canteen.siret_inconnu = True
                update = True
    # Step 2: fetch geo data from API Découpage Administratif & DataGouv
    if canteen.city_insee_code:
        _update_canteen_geo_data_from_insee_code(canteen)
    # Step 3: save & return
    if update:
        canteen._change_reason = "Données de localisation MAJ"
        canteen.save(skip_validations=True)
    return True


@app.task()
def fill_missing_insee_code_using_siret():
    """
    Input: Canteens with siret but no city_insee_code
    Processing: API Recherche Entreprises
    Output: Fill canteen's city_insee_code field
    """
    candidate_canteens = Canteen.objects.candidates_for_siret_to_city_insee_code_bot()
    logger.info(f"Siret to insee_code Bot: found {candidate_canteens.count()} canteens")
    counter = 0

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return

    for i, canteen in enumerate(candidate_canteens):
        logger.info(f"Traitement de la cantine {canteen.name} {canteen.siret}, appel #{i}")
        updated = update_canteen_geo_fields_from_siret(canteen)
        if updated:
            counter += 1
        # time.sleeps to avoid API rate limit
        if i > 1 and i % 7 == 0:
            logger.info("7 appels réalisés maximum par seconde...")
            time.sleep(1)
        if i > 1 and i % 200 == 0:
            logger.info("200 appels réalisés maximum par minute...")
            time.sleep(60)

    result = f"Updated {counter}/{candidate_canteens.count()} canteens"
    logger.info(f"Siret to insee_code Bot: {result}")
    return result


def _update_canteen_geo_data_from_insee_code(canteen):  # noqa C901
    # fetch geo data from API Découpage Administratif & DataGouv
    communes_details = map_communes_infos()
    epcis_names = map_epcis_code_name()
    pat_mapping = map_pat_list_to_communes_insee_code()

    update = False
    # geo fields
    if canteen.city_insee_code in communes_details:
        if not canteen.postal_code:
            postal_code_list = fetch_commune_detail(canteen.city_insee_code, communes_details, "postal_code_list")
            postal_code = postal_code_list[0] if postal_code_list else None
            if postal_code_list:
                canteen.postal_code = postal_code
                update = True
        if not canteen.city:
            city = fetch_commune_detail(canteen.city_insee_code, communes_details, "city")
            if city:
                canteen.city = city
                update = True
        if not canteen.epci:
            epci = fetch_commune_detail(canteen.city_insee_code, communes_details, "epci")
            if epci:
                canteen.epci = epci
                update = True
        if not canteen.pat_list:
            pat_list = fetch_commune_pat_list(canteen.city_insee_code, pat_mapping, "id")
            if pat_list:
                canteen.pat_list = pat_list
                update = True
        if not canteen.department:
            department = fetch_commune_detail(canteen.city_insee_code, communes_details, "department")
            if department:
                canteen.department = department
                update = True
        if not canteen.region:
            region = fetch_commune_detail(canteen.city_insee_code, communes_details, "region")
            if region:
                canteen.region = region
                update = True
    # geo lib fields
    if canteen.epci and not canteen.epci_lib and canteen.epci in epcis_names:
        canteen.epci_lib = fetch_epci_name(canteen.epci, epcis_names)
        update = True
    if canteen.pat_list and not canteen.pat_lib_list:
        canteen.pat_lib_list = fetch_commune_pat_list(canteen.city_insee_code, pat_mapping, "lib")
        update = True
    if canteen.department and not canteen.department_lib:
        canteen.department_lib = get_lib_department_from_code(canteen.department)
        update = True
    if canteen.region and not canteen.region_lib:
        canteen.region_lib = get_lib_region_from_code(canteen.region)
        update = True

    return update


@app.task()
def fill_missing_geolocation_data_using_insee_code():
    """
    Input: Canteens with city_insee_code, but no postal_code or city or epci or department or region
    Processing: API Découpage Administratif
    Output: Fill canteen's postal_code, city, epci, department & region fields
    """
    candidate_canteens = Canteen.objects.candidates_for_city_insee_code_to_geo_data_bot()
    candidate_canteens.update(geolocation_bot_attempts=F("geolocation_bot_attempts") + 1)
    logger.info(f"INSEE Geolocation Bot: found {candidate_canteens.count()} canteens")
    counter = 0

    if len(candidate_canteens) == 0:
        logger.info("No candidate canteens have been found. Nothing to do here...")
        return

    for i, canteen in enumerate(candidate_canteens):
        update = _update_canteen_geo_data_from_insee_code(canteen)
        if update:
            # save
            canteen.save(skip_validations=True)
            update_change_reason(canteen, "Données de localisation MAJ par bot, via code INSEE")
            counter += 1

    result = f"Updated {counter}/{candidate_canteens.count()} canteens"
    logger.info(f"INSEE Geolocation Bot: {result}")
    return result


@app.task()
def delete_old_historical_records():
    if not settings.MAX_DAYS_HISTORICAL_RECORDS:
        logger.info("Environment variable MAX_DAYS_HISTORICAL_RECORDS not set. Old history items will not be removed.")
        return
    logger.info(f"History items older than {settings.MAX_DAYS_HISTORICAL_RECORDS} days will be removed.")
    call_command("clean_old_history", days=settings.MAX_DAYS_HISTORICAL_RECORDS, auto=True)


@app.task()
def canteen_fill_declaration_donnees_year_field():
    call_command("canteen_fill_declaration_donnees_year_field", year=2025)


def export_datasets(datasets: dict):
    for key, etl in datasets.items():
        logger.info(f"Starting {key} dataset extraction")
        etl.extract_dataset()
        etl.transform_dataset()
        etl.load_dataset()


@app.task()
def export_dataset_td_analysis():
    """
    Export the Teledeclaration datasets for analysis (Metabase)
    """
    logger.info("Starting manual datasets export")
    datasets = {
        "td_analyses": ETL_ANALYSIS_TELEDECLARATIONS(),
    }
    export_datasets(datasets)


@app.task()
def export_dataset_td_opendata():
    """
    Export the Teledeclaration datasets for opendata (data.gouv.fr) (1 per year)
    This datasets are updated every year by adding a new campaign
    """
    logger.info("Starting manual datasets export")
    datasets = {
        "campagne teledeclaration 2021": ETL_OPEN_DATA_TELEDECLARATIONS(2021),
        "campagne teledeclaration 2022": ETL_OPEN_DATA_TELEDECLARATIONS(2022),
        "campagne teledeclaration 2023": ETL_OPEN_DATA_TELEDECLARATIONS(2023),
        "campagne teledeclaration 2024": ETL_OPEN_DATA_TELEDECLARATIONS(2024),
        # "campagne teledeclaration 2025": ETL_OPEN_DATA_TELEDECLARATIONS(2025),  # wait for report to be published
    }
    export_datasets(datasets)


@app.task()
def export_dataset_canteen_analysis():
    """
    Export the Canteen datasets for analysis (Metabase)
    """
    logger.info("Starting datasets extractions")
    datasets = {
        "cantines_analyses": ETL_ANALYSIS_CANTEEN(),
    }
    export_datasets(datasets)


@app.task()
def export_dataset_canteen_opendata():
    """
    Export the Canteen datasets for opendata (data.gouv.fr)
    """
    logger.info("Starting datasets extractions")
    datasets = {
        "cantines": ETL_OPEN_DATA_CANTEEN(),
    }
    export_datasets(datasets)
