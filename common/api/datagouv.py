import logging
import os
from datetime import date

import requests

logger = logging.getLogger(__name__)


# DATAGOUV_DOCUMENTATION: https://www.data.gouv.fr/fr/dataservices/api-catalogue-des-donnees-ouvertes-data-gouv-fr/
DATAGOUV_API_URL = "https://www.data.gouv.fr/api/1"


def get_dataset(dataset_id):
    try:
        response = requests.get(f"{DATAGOUV_API_URL}/datasets/{dataset_id}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"Datagouv dataset get: Error while getting dataset: {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


def get_dataset_resource(dataset_id, resource_id):
    try:
        response = requests.get(f"{DATAGOUV_API_URL}/datasets/{dataset_id}/resources/{resource_id}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(
            f"Datagouv dataset resource get: Error while getting dataset resource: {dataset_id} / {resource_id}"
        )
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


def update_dataset_resources(dataset_id):
    """
    Updating the URL of the different resources displayed on data.gouv.fr in order to force their cache reload and display the correct update dates
    Returns: Number of updated resources
    """
    DATAGOUV_API_KEY = os.getenv("DATAGOUV_API_KEY", "")
    DATAGOUV_API_HEADER = {"X-API-KEY": DATAGOUV_API_KEY}

    if not (dataset_id and DATAGOUV_API_KEY):
        logger.warning("Datagouv resource update: API key or dataset id incorrect values")
        return

    try:
        dataset = get_dataset(dataset_id)
        resources = dataset["resources"]
        count_updated_resources = 0
        for resource in resources:
            if resource["format"] in ["xlsx", "csv"]:
                today = date.today()
                updated_url = resource["url"].split("?v=")[0] + "?v=" + today.strftime("%Y%m%d")
                response = requests.put(
                    f'{DATAGOUV_API_URL}/datasets/{dataset_id}/resources/{resource["id"]}',
                    headers=DATAGOUV_API_HEADER,
                    json={"url": updated_url},
                )
                response.raise_for_status()
                count_updated_resources += 1
        logger.info(f"{count_updated_resources} datagouv's ressources have been updated")
        return count_updated_resources
    except requests.HTTPError as e:
        logger.error(f"Datagouv resource update: Error while updating dataset: {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)
