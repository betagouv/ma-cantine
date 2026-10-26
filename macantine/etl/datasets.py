"""
The datasets exported by the export_dataset command
"""

import logging
import time

from oauth2_provider.models import get_access_token_model, get_application_model, get_refresh_token_model

from data.models import Canteen, Diagnostic, EventLog, Oauth2ProviderApplicationExtra, Purchase, User, WasteMeasurement

from .analysis import ETL_ANALYSIS_RAW
from .open_data import ETL_OPEN_DATA_CANTEEN, ETL_OPEN_DATA_TELEDECLARATIONS

logger = logging.getLogger(__name__)


def export_datasets(datasets: dict):
    start = time.time()

    for key, etl in datasets.items():
        logger.info(f"Starting {key} dataset extraction")
        etl.extract_dataset()
        etl.transform_dataset()
        etl.load_dataset()

    end = time.time()
    logger.info(f"Exported {len(datasets)} datasets in {end - start:.2f} seconds")


def get_raw_analysis_datasets():
    """
    The raw datasets for analysis (Metabase, dbt sources)
    """
    return {
        "diagnostics_raw_analysis": ETL_ANALYSIS_RAW("diagnostics_raw", Diagnostic.all_objects.all()),
        "canteens_raw_analysis": ETL_ANALYSIS_RAW("canteens_raw", Canteen.all_objects.all()),
        "purchases_raw_analysis": ETL_ANALYSIS_RAW("purchases_raw", Purchase.all_objects.all()),
        "users_raw_analysis": ETL_ANALYSIS_RAW("users_raw", User.objects.all(), exclude_columns=["password"]),
        "canteen_managers_raw_analysis": ETL_ANALYSIS_RAW(
            "canteen_managers_raw", Canteen.managers.through.objects.all()
        ),
        "waste_measurements_raw_analysis": ETL_ANALYSIS_RAW("waste_measurements_raw", WasteMeasurement.objects.all()),
        "event_logs_raw_analysis": ETL_ANALYSIS_RAW("event_logs_raw", EventLog.objects.all()),
        # OAuth2 (API): never export secrets & tokens
        "oauth2_applications_raw_analysis": ETL_ANALYSIS_RAW(
            "oauth2_applications_raw", get_application_model().objects.all(), exclude_columns=["client_secret"]
        ),
        "oauth2_applications_extra_raw_analysis": ETL_ANALYSIS_RAW(
            "oauth2_applications_extra_raw", Oauth2ProviderApplicationExtra.objects.all()
        ),
        "oauth2_access_tokens_raw_analysis": ETL_ANALYSIS_RAW(
            "oauth2_access_tokens_raw",
            get_access_token_model().objects.all(),
            exclude_columns=["token", "token_checksum"],
        ),
        "oauth2_refresh_tokens_raw_analysis": ETL_ANALYSIS_RAW(
            "oauth2_refresh_tokens_raw",
            get_refresh_token_model().objects.all(),
            exclude_columns=["token", "token_checksum"],
        ),
    }


def get_teledeclaration_opendata_datasets():
    """
    The Teledeclaration datasets for opendata (data.gouv.fr) (1 per year)
    These datasets are updated every year by adding a new campaign
    """
    return {
        "teledeclarations_2021_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2021),
        "teledeclarations_2022_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2022),
        "teledeclarations_2023_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2023),
        "teledeclarations_2024_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2024),
        # "teledeclarations_2025_opendata": ETL_OPEN_DATA_TELEDECLARATIONS(2025),  # wait for report to be published
    }


def get_canteen_opendata_datasets():
    """
    The Canteen dataset for opendata (data.gouv.fr)
    """
    return {
        "canteens_opendata": ETL_OPEN_DATA_CANTEEN(),
    }
