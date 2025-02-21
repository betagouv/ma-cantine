import logging

import requests

from common.utils import siret

logger = logging.getLogger(__name__)


def get_etablishment_or_legal_unit_name(siret_response):
    has_sub_establishment = not siret_response["etablissement"].get("etablissementSiege", True)
    if has_sub_establishment:
        establishment_periods = siret_response["etablissement"]["periodesEtablissement"]
        for period in establishment_periods:
            if not period["dateFin"]:
                return period["enseigne1Etablissement"]
    return siret_response["etablissement"]["uniteLegale"]["denominationUniteLegale"]


def fetch_geo_data_from_siret(canteen_siret, response):
    """
    API rate limit : 400/min
    Pour l'utilsiation de cette méthode dans un script, penser à ne pas dépasser plus que 400 appels/min.
    """
    if not siret.is_valid_siret(canteen_siret):
        logger.error(f"Api Recherche Entreprises: Le SIRET fourni est invalide : {canteen_siret}")
        return

    response["siret"] = canteen_siret
    try:
        siret_response = requests.get(
            f"https://recherche-entreprises.api.gouv.fr/search?q={canteen_siret}",
        )
        siret_response.raise_for_status()
        if siret_response.ok:
            siret_response = siret_response.json()
            try:
                response["name"] = get_etablishment_or_legal_unit_name(siret_response)
                response["cityInseeCode"] = siret_response["etablissement"]["adresseEtablissement"][
                    "codeCommuneEtablissement"
                ]
                response["postalCode"] = siret_response["etablissement"]["adresseEtablissement"][
                    "codePostalEtablissement"
                ]
                response["city"] = siret_response["etablissement"]["adresseEtablissement"][
                    "libelleCommuneEtablissement"
                ]
                return response
            except KeyError as e:
                logger.error(f"unexpected siret response format : {siret_response}. Unknown key : {e}")
        else:
            logger.warning(f"siret lookup failed, code {siret_response.status_code} : {siret_response}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"Api Recherche Entreprises: HTTPError\n{e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Api Recherche Entreprises: ConnectionError\n{e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"Api Recherche Entreprises: Timeout\n{e}")
    except Exception as e:
        logger.error(f"Api Recherche Entreprises: Unexpected exception\n{e}")
    return response
