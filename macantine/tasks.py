import logging
import time

import redis as r
from django.conf import settings
from django.core.management import call_command
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
from data.models import User
from data.models.geo import get_lib_department_from_code, get_lib_region_from_code

from .celery import app
from .etl.analysis import (
    ETL_ANALYSIS_CANTEEN,
    ETL_ANALYSIS_CANTEEN_RAW,
    ETL_ANALYSIS_CANTEEN_MANAGER_RAW,
    ETL_ANALYSIS_TELEDECLARATIONS,
    ETL_ANALYSIS_DIAGNOSTIC_RAW,
    ETL_ANALYSIS_USER_RAW,
    ETL_ANALYSIS_WASTE_MEASUREMENT_RAW,
)
from .etl.open_data import (
    ETL_OPEN_DATA_CANTEEN,
    ETL_OPEN_DATA_TELEDECLARATIONS,
)

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


##########################################################################
# User data


@app.task()
def update_user_data():
    """
    Update calculated fields in User.data JSONField
    """
    logger.info("Starting update_user_data task task")
    start = time.time()

    users_qs = User.objects.with_canteen_stats().with_canteen_diagnostic_stats()
    for user in users_qs:
        user.update_data()

    end = time.time()
    result = f"Updated {users_qs.count()} users in {end - start:.2f} seconds"
    logger.info(result)
    return result


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
    logger.info("Starting update_brevo_contacts task")
    start = time.time()

    logger.info("Create individually new Brevo users (allowing the update flag to be set)")
    users_to_create_qs = User.objects.brevo_to_create()
    brevo.create_new_brevo_contacts(users_to_create_qs, timezone.now())

    logger.info("Update existing Brevo contacts by batch")
    users_to_update_qs = User.objects.brevo_to_update()
    chunks = batched(users_to_update_qs, brevo.CONTACT_BULK_UPDATE_SIZE)
    brevo.update_existing_brevo_contacts(chunks, timezone.now())

    end = time.time()
    result = f"Created {users_to_create_qs.count()} and updated {users_to_update_qs.count()} contacts in {end - start:.2f} seconds"
    logger.info(result)
    return result


@app.task()
def update_canteen_geo_fields_from_siret(canteen):
    """
    Input: Canteen with siret but no city_insee_code
    Processing: API Recherche Entreprises + API Découpage Administratif (cached)
    Output: Fill canteen's city_insee_code field + geo fields
    """
    logger.info("Starting update_canteen_geo_fields_from_siret task")

    # clear dirty fields (and avoid possible recursion errors if coming from post_save)
    canteen.refresh_from_db()

    update = False
    # Step 1: fetch city_insee_code from API Recherche Entreprises
    if not canteen.city_insee_code:
        response = fetch_geo_data_from_siret(canteen.siret)
        if response:
            try:
                if "city_insee_code" in response.keys():
                    canteen.city_insee_code = response["city_insee_code"]
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
def update_canteen_geo_data_from_insee_code(canteen):
    """
    Similar to update_canteen_geo_fields_from_siret, but this time we already have the city_insee_code.
    Processing: API Découpage Administratif (cached)
    Output: Fill canteen's geo fields
    """
    # clear dirty fields (and avoid possible recursion errors if coming from post_save)
    canteen.refresh_from_db()

    if canteen.city_insee_code:
        _update_canteen_geo_data_from_insee_code(canteen)


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
    # save
    if update:
        canteen.save(skip_validations=True)
        update_change_reason(canteen, "Données de localisation MAJ par bot, via code INSEE")
        return True


@app.task()
def delete_old_historical_records():
    logger.info("Starting delete_old_historical_records task")

    if not settings.MAX_DAYS_HISTORICAL_RECORDS:
        logger.info("Environment variable MAX_DAYS_HISTORICAL_RECORDS not set. Old history items will not be removed.")
        return

    logger.info(f"History items older than {settings.MAX_DAYS_HISTORICAL_RECORDS} days will be removed.")
    call_command("clean_old_history", days=settings.MAX_DAYS_HISTORICAL_RECORDS, auto=True)


@app.task()
def canteen_fill_declaration_donnees_year_field():
    logger.info("Starting canteen_fill_declaration_donnees_year_field task")

    result = call_command("canteen_fill_declaration_donnees_year_field", year=2025)

    return result


def export_datasets(datasets: dict):
    start = time.time()

    for key, etl in datasets.items():
        logger.info(f"Starting {key} dataset extraction")
        etl.extract_dataset()
        etl.transform_dataset()
        etl.load_dataset(datagouv=True)

    end = time.time()
    result = f"Exported {len(datasets)} datasets in {end - start:.2f} seconds"
    logger.info(result)
    return result


@app.task()
def export_dataset_raw_analysis():
    """
    Export the raw datasets for analysis (Metabase)
    """
    logger.info("Starting export_dataset_raw_analysis task")

    datasets = {
        "diagnostics_raw_analysis": ETL_ANALYSIS_DIAGNOSTIC_RAW(),
        "canteens_raw_analysis": ETL_ANALYSIS_CANTEEN_RAW(),
        # "purchases_raw_analysis": ETL_ANALYSIS_PURCHASE_RAW(),
        "users_raw_analysis": ETL_ANALYSIS_USER_RAW(),
        "canteen_managers_raw_analysis": ETL_ANALYSIS_CANTEEN_MANAGER_RAW(),
        "waste_measurements_raw_analysis": ETL_ANALYSIS_WASTE_MEASUREMENT_RAW(),
    }
    result = export_datasets(datasets)

    return result


@app.task()
def export_dataset_td_analysis():
    """
    Export the Teledeclaration datasets for analysis (Metabase)
    """
    logger.info("Starting export_dataset_td_analysis task")

    datasets = {
        "teledeclarations_analysis": ETL_ANALYSIS_TELEDECLARATIONS(),
    }
    result = export_datasets(datasets)

    return result


@app.task()
def export_dataset_td_opendata():
    """
    Export the Teledeclaration datasets for opendata (data.gouv.fr) (1 per year)
    This datasets are updated every year by adding a new campaign
    """
    logger.info("Starting export_dataset_td_opendata task")

    datasets = {
        "teledeclarations_2021_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2021),
        "teledeclarations_2022_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2022),
        "teledeclarations_2023_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2023),
        "teledeclarations_2024_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2024),
        # "teledeclarations_2025_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2025),  # wait for report to be published
    }
    result = export_datasets(datasets)

    return result


@app.task()
def export_dataset_canteen_analysis():
    """
    Export the Canteen datasets for analysis (Metabase)
    """
    logger.info("Starting export_dataset_canteen_analysis task")

    datasets = {
        "canteens_analysis": ETL_ANALYSIS_CANTEEN(),
    }
    result = export_datasets(datasets)

    return result


@app.task()
def export_dataset_canteen_opendata():
    """
    Export the Canteen datasets for opendata (data.gouv.fr)
    """
    logger.info("Starting export_dataset_canteen_opendata task")

    datasets = {
        "canteens_opendata": ETL_OPEN_DATA_CANTEEN(),
    }
    result = export_datasets(datasets)

    return result
