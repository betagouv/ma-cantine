import logging

import requests

from common.utils import siret

logger = logging.getLogger(__name__)


def get_enseigne_name(etablissement):
    is_active = etablissement["etat_administratif"] == "A"
    has_enseigne = "liste_enseignes" in etablissement.keys() and len(etablissement["liste_enseignes"]) > 0
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
            logger.info(f"API Recherche Entreprises  : No results found for canteen siret : {siret}")
            return
        result = response["results"][0]
        if len(response["results"][0]["matching_etablissements"]) != 1:
            logger.warning(
                f"API Recherche Entreprises : Expecting 1 establishment for siret (choosing the first one) : {siret}"
            )
            return
        return result


def fetch_geo_data_from_siret(canteen_siret, response):
    """
    API rate limit : 400/min
    Pour l'utilsiation de cette méthode dans un script, penser à ne pas dépasser plus que 400 appels/min.
    Les paramètres de l'appel API à Recherche Entreprises:
    * q={siret} : Terme de la recherche pour lequel nous utilions uniquemement le siret
    * etat_administratif=A : Nous renvoyons uniquements les organismes actifs
    * page=1&per_page=1 : Un seul élément est demandé en réponse car la recherche par SIRET doit renvoyer un seul établissement.
    """
    if not siret.is_valid_length_siret(canteen_siret):
        logger.error(f"Api Recherche Entreprises: Le SIRET fourni est invalide : {canteen_siret}")
        return

    response["siret"] = canteen_siret
    try:
        api_response = requests.get(
            f"https://recherche-entreprises.api.gouv.fr/search?etat_administratif=A&page=1&per_page=1&q={canteen_siret}",
        )
        api_response.raise_for_status()
        result = validate_result(canteen_siret, api_response)
        if result:
            try:
                etablissement = result["matching_etablissements"][0]
                response["name"] = get_enseigne_name(etablissement) or result["nom_complet"]
                response["cityInseeCode"] = etablissement["commune"]
                response["postalCode"] = etablissement["code_postal"]
                response["city"] = etablissement["libelle_commune"]
                return response
            except KeyError as e:
                logger.error(
                    f"API Recherche Entreprises : Unexpected siret response format : {api_response}. Unknown key : {e}"
                )
        else:
            logger.warning(
                f"API Recherche Entreprises : Siret lookup failed, code {api_response.status_code} : {api_response}"
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
