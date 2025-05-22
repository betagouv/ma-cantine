import csv
import logging
import os
from datetime import date

import requests

logger = logging.getLogger(__name__)


# DATAGOUV_DOCUMENTATION: https://www.data.gouv.fr/fr/dataservices/api-catalogue-des-donnees-ouvertes-data-gouv-fr/
DATAGOUV_API_URL = "https://www.data.gouv.fr/api/1"

# PAT (Projets Alimentaires Territoriaux): https://france-pat.fr/presentation-de-l-observatoire/
PAT_DATAGOUV_DATASET_ID = "pat-projets-alimentaires-territoriaux-description"
# PAT_DATAGOUV_RESOURCE_ID = "4f2a6bed-e9e3-48eb-aecc-85b08cb984f3"  # 20250224  # TODO: update twice a year
PAT_DATAGOUV_RESOURCE_ID = "96606cae-0b3b-4910-9d8b-65e3dd7f1bda"  # 20250224 (ISO-8859-1)  # TODO: update twice a year


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


def map_pat_list_to_communes_insee_code():
    """
    Create a dict that maps insee codes with their pat
    Input: a list of pat. 891;https://france-pat.fr/pat/redon-agglomeration/;"Programme Agricole et Alimentaire de Territoire de REDON Agglomération";;"Pays de la Loire, Bretagne";"Ille-et-Vilaine, Loire-Atlantique, Morbihan";;35145,56232,44185,56011,56216,56250,44067,35045,35268,35285,35064,35151,35219,56221,35236,56154,56239,35013,35237,56001,56223,44123,35328,44057,44092,56194,35294,44044,44128,56060,44007;...
    Output: a dict with the commune's insee code as pivot. {"35145": {"pat": "891", "pat_lib": "Programme Agricole et Alimentaire de Territoire de REDON Agglomération"}}
    """
    pat_mapping = {}
    try:
        pat_list = []
        pat_dataset_resource = get_dataset_resource(PAT_DATAGOUV_DATASET_ID, PAT_DATAGOUV_RESOURCE_ID)
        response = requests.get(pat_dataset_resource["url"])
        response.raise_for_status()
        print(response.encoding)
        reader = csv.DictReader(response.iter_lines(decode_unicode=True), delimiter=";")
        pat_list = list(reader)
        # with open(pat_dataset_resource["url"], "r", encoding="utf-8") as pat_csv_file:
        #     pat_list = pat_csv_file.read().splitlines()
        for pat in pat_list:
            city_insee_code_list = [insee_code for insee_code in pat["communes_code_insee"].split(",") if insee_code]
            for city_insee_code in city_insee_code_list:
                if city_insee_code not in pat_mapping.keys():
                    pat_mapping[city_insee_code] = []
                pat_mapping[city_insee_code].append(
                    {
                        "pat": pat["id"],
                        "pat_lib": pat["nom_administratif"],
                    }
                )
            if len(city_insee_code_list) == 0:
                logger.warning(f"PAT with no insee code : {pat['id']} : {pat['nom_administratif']}")
        print(len(pat_list))
        print(len(pat_mapping.keys()))
        from collections import Counter

        # Stats
        print(Counter([len(pat_mapping[insee_code]) for insee_code in pat_mapping.keys()]))
        # for city_insee_code in pat_mapping.keys():
        #     # PAT with comma
        #     if "," in pat_mapping[city_insee_code][0]["pat_lib"]:
        #         print(f"Pat with comma : {city_insee_code} : {pat_mapping[city_insee_code]}")
        #     # PAT with more than 2 communes
        #     if len(pat_mapping[city_insee_code]) > 2:
        #         print(f"Pat with more than 2 : {city_insee_code} : {pat_mapping[city_insee_code]}")

    except requests.HTTPError as e:
        logger.info(e)
    # return pat_mapping
