import logging
import json
import requests

from common.utils import siret as utils_siret
from common.utils import utils as utils_utils

logger = logging.getLogger(__name__)


RECHERCHE_ENTREPRISES_API_URL = "https://recherche-entreprises.api.gouv.fr/search"
DEFAULT_PARAMS = "etat_administratif=A&page=1&per_page=1&mtm_campaign=ma-cantine"


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
                response["cityInseeCode"] = etablissement["commune"]
                response["postalCode"] = etablissement["code_postal"]
                response["city"] = etablissement["libelle_commune"]
                response["epci"] = etablissement["epci"]
                response["department"] = etablissement["departement"]
                response["region"] = etablissement["region"]
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
                response["cityInseeCode"] = etablissement["commune"]
                response["postalCode"] = etablissement["code_postal"]
                response["city"] = etablissement["libelle_commune"]  # en majuscules
                response["epci"] = etablissement["epci"]
                # response["department"] = etablissement["departement"]  # not in response
                response["region"] = etablissement["region"]
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


def mock_fetch_geo_data_from_siren(mock, siren, success=True):
    api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={siren}"
    if not success:
        mock.get(api_url, text="", status_code=403)
    mock.get(
        api_url,
        text=json.dumps(
            {
                # siren: 923412845
                "results": [
                    {
                        "siren": "923412845",
                        "nom_complet": "LA TURBINE",
                        "siege": {
                            "commune": "59512",
                            "code_postal": "59100",
                            "libelle_commune": "ROUBAIX",
                            "epci": "200075174",
                            "departement": "59",
                            "region": "32",
                            "liste_enseignes": None,
                            "etat_administratif": "A",
                        },
                        "matching_etablissements": [],
                    }
                ],
                "total_results": 1,
            }
        ),
    )


def mock_fetch_geo_data_from_siret(mock, siret, success=True):
    api_url = f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q={siret}"
    if success:
        mock.get(
            api_url,
            text=json.dumps(
                {
                    # siret: 92341284500011
                    "results": [
                        {
                            "siren": "923412845",
                            "nom_complet": "LA TURBINE",
                            "matching_etablissements": [
                                {
                                    "commune": "59512",
                                    "code_postal": "59100",
                                    "libelle_commune": "ROUBAIX",
                                    "epci": "200075174",
                                    "region": "32",
                                    "liste_enseignes": ["Legal unit name"],
                                    "etat_administratif": "A",
                                }
                            ],
                        }
                    ],
                    "total_results": 1,
                }
            ),
        )
    else:
        mock.get(api_url, text="", status_code=403)
