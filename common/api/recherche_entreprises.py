import json
import logging
import requests
from django.utils import timezone

from common.utils import siret as utils_siret
from common.utils import utils as utils_utils

logger = logging.getLogger(__name__)


RECHERCHE_ENTREPRISES_API_URL = "https://recherche-entreprises.api.gouv.fr/search"
DEFAULT_PARAMS = "etat_administratif=A&page=1&per_page=1&mtm_campaign=ma-cantine"

# Canteen.recherche_entreprises_data: subset of the API response (add fields as the need comes)
RECHERCHE_ENTREPRISES_DATA_STATUS_OK = "ok"
RECHERCHE_ENTREPRISES_DATA_STATUS_NOT_FOUND = "not_found"
RECHERCHE_ENTREPRISES_DATA_UNITE_LEGALE_FIELDS = [
    "etat_administratif",  # "A" (active), "C" (cessée)
    "date_fermeture",  # e.g. "2025-05-18" (null if active)
    "nature_juridique",  # INSEE catégorie juridique, e.g. "7210" (commune)
    "activite_principale",  # NAF code, e.g. "84.11Z" (administration publique générale)
]
RECHERCHE_ENTREPRISES_DATA_ETABLISSEMENT_FIELDS = [
    "etat_administratif",  # "A" (active), "F" (fermé)
    "date_fermeture",  # e.g. "2025-05-18" (null if active)
    "activite_principale",  # NAF code, e.g. "56.29B" (autres services de restauration)
    "adresse",  # e.g. "3 RUE DU CHEMIN DE FER 59100 ROUBAIX"
    "latitude",  # string, e.g. "50.693979573878"
    "longitude",  # string, e.g. "3.16664533133567"
    # also in the API response, but not stored:
    # "coordonnees",  # "latitude,longitude": duplicate of latitude & longitude, e.g. "50.693979573878,3.16664533133567"
    # "geo_adresse",  # address normalized with the BAN (mixed case): always empty (null) in the API responses
    # "geo_id",  # BAN address id: always empty (null) in the API responses
]


def get_enseigne_name(etablissement):
    is_active = etablissement["etat_administratif"] == "A"
    has_enseigne = (
        "liste_enseignes" in etablissement.keys()
        and etablissement["liste_enseignes"]
        and len(etablissement["liste_enseignes"]) > 0
    )
    if has_enseigne and is_active:
        return etablissement["liste_enseignes"][0]


def validate_result(siret, response):
    """
    Return a dict with the results of the API if there is valid data to process
    If not, returns None
    """
    if response.ok:
        response = response.json()
        if response["total_results"] == 0:
            logger.info(f"API Recherche Entreprises : No results found for canteen SIRET : {siret}")
            return
        result = response["results"][0]
        if "matching_etablissements" in response["results"][0]:
            if len(response["results"][0]["matching_etablissements"]) > 1:
                logger.warning(
                    f"API Recherche Entreprises : Expecting 1 establishment for SIRET (choosing the first one) : {siret}"
                )
                return
        return result


def fetch_geo_data_from_siren(siren):
    """
    API rate limit : 400/min
    Pour l'utilisation de cette méthode dans un script, penser à ne pas dépasser plus que 400 appels/min.
    Les paramètres de l'appel API à Recherche Entreprises:
    * q={siren} : Terme de la recherche pour lequel nous utilions uniquemement le SIREN
    * etat_administratif=A : Nous renvoyons uniquements les organismes actifs
    * page=1&per_page=1 : Un seul élément est demandé en réponse car la recherche par SIREN doit renvoyer un seul établissement.
    """
    # TODO: replace with utils_siret.validate_siret
    siren = utils_utils.normalize_string(siren)
    if not utils_siret.is_valid_length_siren(siren):
        logger.error(f"Api Recherche Entreprises: Le SIREN fourni est invalide : {siren}")
        return

    response = {}
    response["siren"] = siren
    try:
        api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={siren}"
        api_response = requests.get(api_url)
        api_response.raise_for_status()
        result = validate_result(siren, api_response)
        if result:
            try:
                etablissement = result["siege"]
                response["name"] = get_enseigne_name(etablissement) or result["nom_complet"]
                response["city_insee_code"] = etablissement["commune"]
                response["postal_code"] = etablissement["code_postal"]
                response["city"] = etablissement["libelle_commune"]
                response["epci"] = etablissement["epci"]
                response["department"] = etablissement["departement"]
                response["region"] = etablissement["region"]
                response["etat_administratif"] = etablissement["etat_administratif"]  # "A", "F"
                response["date_fermeture"] = etablissement["date_fermeture"]
                return response
            except KeyError as e:
                logger.error(
                    f"API Recherche Entreprises : Unexpected SIREN response format : {api_response}. Unknown key : {e}"
                )
        else:
            logger.warning(
                f"API Recherche Entreprises : SIREN lookup failed, code {api_response.status_code} : {api_response}"
            )
            return
    except requests.exceptions.HTTPError as e:
        logger.error(f"Api Recherche Entreprises: HTTPError\n{e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Api Recherche Entreprises: ConnectionError\n{e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"Api Recherche Entreprises: Timeout\n{e}")
    except Exception as e:
        logger.error(f"Api Recherche Entreprises: Unexpected exception\n{e}")
    return response


def fetch_geo_data_from_siret(siret):
    """
    API rate limit : 400/min
    Pour l'utilisation de cette méthode dans un script, penser à ne pas dépasser plus que 400 appels/min.
    Les paramètres de l'appel API à Recherche Entreprises:
    * q={siret} : Terme de la recherche pour lequel nous utilions uniquemement le SIRET
    * etat_administratif=A : Nous renvoyons uniquements les organismes actifs
    * page=1&per_page=1 : Un seul élément est demandé en réponse car la recherche par SIRET doit renvoyer un seul établissement.
    """
    # TODO: replace with utils_siret.validate_siret
    siret = utils_utils.normalize_string(siret)
    if not utils_siret.is_valid_length_siret(siret):
        logger.error(f"Api Recherche Entreprises: Le SIRET fourni est invalide : {siret}")
        return

    response = {}
    response["siret"] = siret
    try:
        api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={siret}"
        api_response = requests.get(api_url)
        api_response.raise_for_status()
        result = validate_result(siret, api_response)
        if result:
            try:
                etablissement = result["matching_etablissements"][0]
                response["name"] = get_enseigne_name(etablissement) or result["nom_complet"]
                response["city_insee_code"] = etablissement["commune"]
                response["postal_code"] = etablissement["code_postal"]
                response["city"] = etablissement["libelle_commune"]  # en majuscules
                response["epci"] = etablissement["epci"]
                # response["department"] = etablissement["departement"]  # not in response
                response["region"] = etablissement["region"]
                response["etat_administratif"] = etablissement["etat_administratif"]  # "A", "F"
                response["date_fermeture"] = etablissement["date_fermeture"]
                return response
            except KeyError as e:
                logger.error(
                    f"API Recherche Entreprises : Unexpected SIRET response format : {api_response}. Unknown key : {e}"
                )
        else:
            logger.warning(
                f"API Recherche Entreprises : SIRET lookup failed, code {api_response.status_code} : {api_response}"
            )
            return
    except requests.exceptions.HTTPError as e:
        logger.error(f"Api Recherche Entreprises: HTTPError\n{e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Api Recherche Entreprises: ConnectionError\n{e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"Api Recherche Entreprises: Timeout\n{e}")
    except Exception as e:
        logger.error(f"Api Recherche Entreprises: Unexpected exception\n{e}")
    return response


def _find_matching_result(source, query, results):
    """
    Return the (unite_legale, etablissement) matching the query, or (None, None)
    - SIRET: the unite_legale & its matching etablissement
    - SIREN: the unite_legale only (its siege isn't the canteen)
    """
    for result in results:
        if source == "siren":
            if result["siren"] == query:
                return result, None
        else:
            for etablissement in result.get("matching_etablissements") or []:
                if etablissement["siret"] == query:
                    return result, etablissement
    return None, None


def fetch_recherche_entreprises_data(siret=None, siren=None):
    """
    Fetch the data stored in Canteen.recherche_entreprises_data (using the SIRET, else the SIREN)
    - status "ok": unite_legale (+ etablissement for a SIRET) subsets
    - status "not_found": unknown (or invalid) SIRET / SIREN
    - None if API error (HTTP error, rate limit, timeout, unexpected format): nothing should be stored

    API rate limit : 400/min
    Note: the etat_administratif=A param (DEFAULT_PARAMS) is ignored by the API when searching a SIRET / SIREN
    """
    source, query = ("siret", siret) if siret else ("siren", siren)
    query = utils_utils.normalize_string(query)
    data = {
        "source": source,
        "query": query,
        "status": RECHERCHE_ENTREPRISES_DATA_STATUS_NOT_FOUND,
        "fetch_date": timezone.now().isoformat(),
        "unite_legale": None,
        "etablissement": None,
    }
    is_valid_length = utils_siret.is_valid_length_siret if source == "siret" else utils_siret.is_valid_length_siren
    if not query or not is_valid_length(query):
        logger.warning(f"API Recherche Entreprises : Le {source.upper()} fourni est invalide : {query}")
        return data

    try:
        api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={query}"
        api_response = requests.get(api_url, timeout=30)
        api_response.raise_for_status()
        unite_legale, etablissement = _find_matching_result(source, query, api_response.json()["results"])
        if unite_legale:
            data["status"] = RECHERCHE_ENTREPRISES_DATA_STATUS_OK
            data["unite_legale"] = {
                field: unite_legale[field] for field in RECHERCHE_ENTREPRISES_DATA_UNITE_LEGALE_FIELDS
            }
            if etablissement:
                data["etablissement"] = {
                    field: etablissement[field] for field in RECHERCHE_ENTREPRISES_DATA_ETABLISSEMENT_FIELDS
                }
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"API Recherche Entreprises : {source.upper()} {query} : {e.__class__.__name__}\n{e}")
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"API Recherche Entreprises : {source.upper()} {query} : Unexpected response format\n{e}")
    return None


MOCK_SIREN_000000000_RESULTS = []
MOCK_SIREN_923412845_RESULTS = [
    {
        "siren": "923412845",
        "nom_complet": "LA TURBINE",
        "etat_administratif": "A",
        "date_fermeture": None,
        "nature_juridique": "9220",
        "activite_principale": "94.99Z",
        "siege": {
            "code_postal": "59100",
            "commune": "59512",
            "date_fermeture": None,
            "departement": "59",
            "epci": "200075174",
            "etat_administratif": "A",
            "libelle_commune": "ROUBAIX",
            "liste_enseignes": None,
            "region": "32",
            "siret": "92341284500011",
        },
    }
]
MOCK_SIREN_213401722_RESULTS = [
    {
        "siren": "213401722",
        "nom_complet": "COMMUNE DE MONTPELLIER",
        "etat_administratif": "A",
        "date_fermeture": None,
        "nature_juridique": "7210",
        "activite_principale": "84.11Z",
        "siege": {
            "code_postal": "34070",
            "commune": "34172",
            "date_fermeture": None,
            "departement": "34",
            "epci": "243400017",
            "etat_administratif": "A",
            "libelle_commune": "MONTPELLIER",
            "liste_enseignes": ["MAIRIE"],
            "region": "76",
            "siret": "21340172201787",
        },
    }
]


def mock_fetch_geo_data_from_siren(mock, siren, success=True):
    api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={siren}"
    if success:
        results = eval(f"MOCK_SIREN_{siren}_RESULTS")
        mock.get(
            api_url,
            text=json.dumps(
                {
                    "results": results,
                    "total_results": len(results),
                }
            ),
        )
    else:
        mock.get(api_url, text="", status_code=403)


MOCK_SIRET_00000000000000_RESULTS = []
MOCK_SIRET_92341284500011_RESULTS = [
    {
        "siren": "923412845",
        "nom_complet": "LA TURBINE",
        "etat_administratif": "A",
        "date_fermeture": None,
        "nature_juridique": "9220",
        "activite_principale": "94.99Z",
        "siege": {
            "code_postal": "59100",
            "commune": "59512",
            "date_fermeture": None,
            "departement": "59",
            "epci": "200075174",
            "etat_administratif": "A",
            "libelle_commune": "ROUBAIX",
            "liste_enseignes": None,
            "region": "32",
            "siret": "92341284500011",
        },
        "matching_etablissements": [
            {
                "code_postal": "59100",
                "commune": "59512",
                "date_fermeture": None,
                "epci": "200075174",
                "etat_administratif": "A",
                "libelle_commune": "ROUBAIX",
                "liste_enseignes": None,
                "region": "32",
                "activite_principale": "94.99Z",
                "adresse": "3 RUE DU CHEMIN DE FER 59100 ROUBAIX",
                "latitude": "50.693979573878",
                "longitude": "3.16664533133567",
                "siret": "92341284500011",
            }
        ],
    }
]
MOCK_SIRET_21340172201787_RESULTS = [
    {
        "siren": "213401722",
        "nom_complet": "COMMUNE DE MONTPELLIER",
        "etat_administratif": "A",
        "date_fermeture": None,
        "nature_juridique": "7210",
        "activite_principale": "84.11Z",
        "siege": {
            "code_postal": "34070",
            "commune": "34172",
            "date_fermeture": None,
            "departement": "34",
            "epci": "243400017",
            "etat_administratif": "A",
            "libelle_commune": "MONTPELLIER",
            "liste_enseignes": ["MAIRIE"],
            "region": "76",
            "siret": "21340172201787",
        },
        "matching_etablissements": [
            {
                "code_postal": "34070",
                "commune": "34172",
                "date_fermeture": None,
                "epci": "243400017",
                "etat_administratif": "A",  # active
                "libelle_commune": "MONTPELLIER",
                "liste_enseignes": ["MAIRIE"],
                "region": "76",
                "activite_principale": "84.11Z",
                "adresse": "1 PL GEORGES FRECHE 34070 MONTPELLIER",
                "latitude": "43.599168",
                "longitude": "3.896652",
                "siret": "21340172201787",
            }
        ],
    }
]
MOCK_SIRET_21380185500072_RESULTS = [
    {
        "siren": "213801855",
        "nom_complet": "SCE DES EAUX",
        "etat_administratif": "A",
        "date_fermeture": None,
        "nature_juridique": "7210",
        "activite_principale": "84.11Z",
        "siege": {
            "code_postal": "38000",
            "commune": "38185",
            "date_fermeture": None,
            "departement": "38",
            "epci": "200040715",
            "etat_administratif": "A",
            "libelle_commune": "GRENOBLE",
            "liste_enseignes": ["MAIRIE"],
            "region": "84",
            "siret": "21380185500015",
        },
        "matching_etablissements": [
            {
                "code_postal": "38000",
                "commune": "38185",
                "date_fermeture": "2000-05-01",
                "epci": "200040715",
                "etat_administratif": "F",  # closed
                "libelle_commune": "GRENOBLE",
                "liste_enseignes": ["SCE DES EAUX"],
                "region": "84",
                "activite_principale": "36.00Z",
                "adresse": "11 BD JEAN PAIN 38000 GRENOBLE",
                "latitude": "45.186775",
                "longitude": "5.736387",
                "siret": "21380185500072",
            }
        ],
    }
]


def mock_fetch_geo_data_from_siret(mock, siret, success=True):
    api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={siret}"
    if success:
        results = eval(f"MOCK_SIRET_{siret}_RESULTS")
        mock.get(
            api_url,
            text=json.dumps(
                {
                    "results": results,
                    "total_results": len(results),
                }
            ),
        )
    else:
        mock.get(api_url, text="", status_code=403)
