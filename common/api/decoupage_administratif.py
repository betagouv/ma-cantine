import logging
import json
import requests

from django.core.cache import cache

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# DECOUPAGE ADMINISTRATIF
# API DOCUMENTATION: https://geo.api.gouv.fr/decoupage-administratif

DECOUPAGE_ADMINISTRATIF_API_URL = "https://geo.api.gouv.fr"

CITY_WITH_ARRONDISSEMENTS = [
    {
        "code": "13055",
        "nom": "Marseille",
        "codeArrondissementPrefix": "132",
    },
    {
        "code": "69123",
        "nom": "Lyon",
        "codeArrondissementPrefix": "6938",
    },
    {
        "code": "75056",
        "nom": "Paris",
        "codeArrondissementPrefix": "751",
    },
]


# ------------------------------------------------------------------------------
# Caching

CACHE_KEY_PREFIX = "api_decoupage_administratif"
CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 days


def fetch_communes():
    """
    Fields returned: nom, code, codeDepartement, codeRegion, codesPostaux, population
    - missing: siren, codeEpci
    """
    cache_key = f"{CACHE_KEY_PREFIX}_communes"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes?type=arrondissement-municipal,commune-actuelle"
    response = requests.get(api_url, timeout=50)
    response.raise_for_status()
    response_json = response.json()

    # order by code
    response_json = sorted(response_json, key=lambda x: x["code"])

    # cache mechanism: store the result
    cache.set(cache_key, response_json, timeout=CACHE_TIMEOUT)
    return response_json


def fetch_communes_with_more_fields(with_arrondissements=True):
    """
    Fields returned: nom, code, codeDepartement, siren, codeEpci, codeRegion, codesPostaux, population
    - missing: department, region
    - missing: arrondissements (132**, 6938*, 751**)
    """
    cache_key = f"{CACHE_KEY_PREFIX}_communes_with_more_fields"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes"
    response = requests.get(api_url, timeout=50)
    response.raise_for_status()
    response_json = response.json()

    if with_arrondissements:
        # we do another query to also get the arrondissements
        communes_json = fetch_communes()
        # keep only the arrondissements
        code_arrondisement_prefix_list = [city["codeArrondissementPrefix"] for city in CITY_WITH_ARRONDISSEMENTS]
        communes_json_arrondissements = [
            commune
            for commune in communes_json
            if any(commune["code"].startswith(prefix) for prefix in code_arrondisement_prefix_list)
        ]
        # set the extra fields
        for index, arrondissement in enumerate(communes_json_arrondissements):
            arrondissement_mapping = next(
                (
                    city
                    for city in CITY_WITH_ARRONDISSEMENTS
                    if arrondissement["code"].startswith(city["codeArrondissementPrefix"])
                ),
                None,
            )
            commune = next(
                (commune for commune in response_json if commune["code"] == arrondissement_mapping["code"]), None
            )
            if commune:
                communes_json_arrondissements[index]["siren"] = commune["siren"]
                communes_json_arrondissements[index]["population"] = None
                communes_json_arrondissements[index]["codeEpci"] = commune["codeEpci"]
                # communes_json_arrondissements[index]["codeDepartement"] = commune["codeDepartement"]
                # communes_json_arrondissements[index]["codeRegion"] = commune["codeRegion"]
        # merge the two lists (arrondissements at the top, similar to fetch_communes)
        response_json = communes_json_arrondissements + response_json

    # order by code
    response_json = sorted(response_json, key=lambda x: x["code"])

    # cache mechanism: store the result
    cache.set(cache_key, response_json, timeout=CACHE_TIMEOUT)
    return response_json


def fetch_epcis():
    """
    Fields returned: nom, code (codesDepartements, codesRegions, population)
    """
    cache_key = f"{CACHE_KEY_PREFIX}_epcis"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis?fields=nom,code"
    response = requests.get(api_url, timeout=50)
    response.raise_for_status()

    # cache mechanism: store the result
    cache.set(cache_key, response.json(), timeout=CACHE_TIMEOUT)
    return response.json()


def fetch_communes_from_epci(epci):
    """
    Fields returned: nom, code (codeDepartement, siren, codeEpci, codeRegion, codePostaux, population)
    """
    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis/{epci}/communes?fields=nom,code"
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    return response.json()


def fetch_departements():
    """
    Fields returned: nom, code, codeRegion
    """
    cache_key = f"{CACHE_KEY_PREFIX}_departements"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/departements?zone=metro,drom,com"
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()

    # cache mechanism: store the result
    cache.set(cache_key, response.json(), timeout=CACHE_TIMEOUT)
    return response.json()


def fetch_regions():
    """
    Fields returned: nom, code
    """
    cache_key = f"{CACHE_KEY_PREFIX}_regions"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/regions?zone=metro,drom,com"
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()

    # cache mechanism: store the result
    cache.set(cache_key, response.json(), timeout=CACHE_TIMEOUT)
    return response.json()


def map_communes_infos():
    """
    Create a dict that maps cities with their name/postal_code/department/region/epci
    Input: a list of communes. {"nom":"L'Abergement-Clémenciat","code":"01001","codeDepartement":"01","siren":"210100012","codeEpci":"200069193","codeRegion":"84","codesPostaux":["01400"],"population":859}
    Output: a dict with the commune's insee code as pivot. {"01001": {"city": "L'Abergement-Clémenciat", "postal_code_list": ["01400"], "department": "01", "region": "84", "epci": "200069193"}}
    """
    commune_details = {}
    try:
        communes = fetch_communes_with_more_fields()
        for commune in communes:
            commune_details[commune["code"]] = {}
            commune_details[commune["code"]]["city"] = commune.get("nom", None)
            commune_details[commune["code"]]["postal_code_list"] = commune.get("codesPostaux", [])
            commune_details[commune["code"]]["department"] = commune.get("codeDepartement", None)
            commune_details[commune["code"]]["region"] = commune.get("codeRegion", None)
            commune_details[commune["code"]]["epci"] = commune.get("codeEpci", None)
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


def mock_fetch_communes(mock, success=True):
    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes?type=arrondissement-municipal,commune-actuelle"
    api_url_with_more_fields = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes"
    if success:
        mock.get(api_url, text=json.dumps([]))
        mock.get(
            api_url_with_more_fields,
            text=json.dumps(
                [
                    {
                        "nom": "L'Abergement-de-Varey",
                        "code": "01002",
                        "codeDepartement": "01",
                        "siren": "210100020",
                        "codeEpci": "240100883",
                        "codeRegion": "84",
                        "codesPostaux": ["01640"],
                        "population": "267",
                    },
                    {
                        "nom": "Grenoble",
                        "code": "38185",
                        "codeDepartement": "38",
                        "siren": "213801855",
                        "codeEpci": "200040715",
                        "codeRegion": "84",
                        "codesPostaux": ["38000", "38100"],
                        "population": 156389,
                    },
                    {
                        "nom": "Roubaix",
                        "code": "59512",
                        "codeDepartement": "59",
                        "siren": "215905126",
                        "codeEpci": "200093201",
                        "codeRegion": "32",
                        "codesPostaux": ["59100"],
                        "population": 98286,
                    },
                    {
                        "nom": "Montpellier",
                        "code": "34172",
                        "codeDepartement": "34",
                        "siren": "213401722",
                        "codeEpci": "243400017",
                        "codeRegion": "76",
                        "codesPostaux": ["34000"],
                        "population": 290053,
                    },
                ]
            ),
        )
    else:
        mock.get(api_url, text="", status_code=403)
        mock.get(api_url_with_more_fields, text="", status_code=403)


def mock_fetch_epcis(mock, success=True):
    api_url = f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis?fields=nom,code"
    if success:
        mock.get(
            api_url,
            text=json.dumps(
                [
                    {"nom": "CC Faucigny - Glières", "code": "200000172"},
                    {"nom": "Grenoble-Alpes-Métropole", "code": "200040715"},
                    {"nom": "Métropole Européenne de Lille", "code": "200093201"},
                    {"nom": "Montpellier Méditerranée Métropole", "code": "243400017"},
                ]
            ),
        )
    else:
        mock.get(api_url, text="", status_code=403)
