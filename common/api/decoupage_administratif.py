import logging

import requests

logger = logging.getLogger(__name__)


# DECOUPAGE_ADMINISTRATIF_DOCUMENTATION: https://geo.api.gouv.fr/decoupage-administratif
DECOUPAGE_ADMINISTRATIF_API_URL = "https://geo.api.gouv.fr"


# https://fr.wikipedia.org/wiki/Arrondissements_de_Paris
PARIS_INSEE_CODE_FROM_API = "75056"
PARIS_INSEE_CODE_PREFIX = "750"
PARIS_ARRONDISSEMENT_COUNT = 20
# https://fr.wikipedia.org/wiki/Arrondissements_de_Lyon
LYON_INSEE_CODE_FROM_API = "69123"
LYON_INSEE_CODE_PREFIX = "693"
LYON_ARRONDISSEMENT_COUNT = 9
# https://fr.wikipedia.org/wiki/Secteurs_et_arrondissements_de_Marseille
MARSEILLE_INSEE_CODE_FROM_API = "13055"
MARSEILLE_INSEE_CODE_PREFIX = "132"
MARSEILLE_ARRONDISSEMENT_COUNT = 16


def fetch_communes():
    response = requests.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes", timeout=50)
    response.raise_for_status()
    return response.json()


def fetch_epcis():
    response = requests.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis?fields=nom", timeout=50)
    response.raise_for_status()
    return response.json()


def fetch_communes_from_epci(epci):
    response = requests.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis/{epci}/communes?fields=code", timeout=5)
    response.raise_for_status()
    return response.json()


def map_communes_infos():
    """
    Create a dict that maps cities with their name/postal_code/department/region/epci
    Input: a list of communes. {"nom":"L'Abergement-Clémenciat","code":"01001","codeDepartement":"01","siren":"210100012","codeEpci":"200069193","codeRegion":"84","codesPostaux":["01400"],"population":859}
    Output: a dict with the commune's insee code as pivot. {"01001": {"city": "L'Abergement-Clémenciat", "postal_code_list": ["01400"], "department": "01", "region": "84", "epci": "200069193"}}
    """
    commune_details = {}
    try:
        communes = fetch_communes()
        for commune in communes:
            commune_details[commune["code"]] = {}
            commune_details[commune["code"]]["city"] = commune.get("nom", None)
            commune_details[commune["code"]]["postal_code_list"] = commune.get("codesPostaux", [])
            commune_details[commune["code"]]["department"] = commune.get("codeDepartement", None)
            commune_details[commune["code"]]["region"] = commune.get("codeRegion", None)
            commune_details[commune["code"]]["epci"] = commune.get("codeEpci", None)
        # add missing arrondissements of Paris, Lyon and Marseille
        for city in ["PARIS", "LYON", "MARSEILLE"]:
            city_details_from_api = commune_details.get(eval(f"{city}_INSEE_CODE_FROM_API"))
            if city_details_from_api:
                for i in range(1, eval(f"{city}_ARRONDISSEMENT_COUNT") + 1):
                    city_arrondissement_insee_code = f"{eval(f'{city}_INSEE_CODE_PREFIX')}{i:02}"
                    city_arrondissement_postal_code = city_details_from_api["postal_code_list"][0][:-2] + f"{i:02}"
                    commune_details[city_arrondissement_insee_code] = {
                        **city_details_from_api,
                        "postal_code_list": [city_arrondissement_postal_code],
                    }
    except requests.exceptions.HTTPError as e:
        logger.info(e)
    return commune_details


def map_epcis_code_name():
    """
    Create a dict that maps epci with their name
    Input: a list of epcis. {"nom":"CC Faucigny - Glières","code":"200000172","codesDepartements":["74"],"codesRegions":["84"],"population":28363}
    Output: a dict with the epci's code as pivot. {"200000172": "CC Faucigny - Glières"}
    """
    epcis_names = {}
    try:
        epcis = fetch_epcis()
        for epci in epcis:
            epcis_names[epci["code"]] = epci["nom"]
    except requests.exceptions.HTTPError as e:
        logger.info(e)
    return epcis_names


def fetch_commune_detail(code_insee_commune, commune_details, geo_detail_type):
    """
    Provide EPCI code/ Department code/ Region code for a city, given the insee code of the city
    """
    if (
        code_insee_commune
        and code_insee_commune in commune_details.keys()
        and geo_detail_type in commune_details[code_insee_commune].keys()
    ):
        return commune_details[code_insee_commune][geo_detail_type]


def fetch_epci_name(code_insee_epci, epcis_names):
    """
    Provide EPCI code for an epci, given its insee code
    """
    if code_insee_epci and code_insee_epci in epcis_names.keys():
        return epcis_names[code_insee_epci]
