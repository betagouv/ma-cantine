import base64
import logging
import time

import redis as r
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

redis = r.from_url(settings.REDIS_URL, decode_responses=True)


def get_token_sirene():
    if not settings.SIRET_API_KEY or not settings.SIRET_API_SECRET:
        logger.warning("skipping siret token fetching because key and secret env vars aren't set")
        return
    token_redis_key = f"{settings.REDIS_PREPEND_KEY}SIRET_API_TOKEN"
    if redis.exists(token_redis_key):
        return redis.get(token_redis_key)

    base64Cred = base64.b64encode(bytes(f"{settings.SIRET_API_KEY}:{settings.SIRET_API_SECRET}", "utf-8")).decode(
        "utf-8"
    )
    token_data = {"grant_type": "client_credentials", "validity_period": 604800}
    token_headers = {"Authorization": f"Basic {base64Cred}"}
    token_response = requests.post("https://api.insee.fr/token", data=token_data, headers=token_headers)
    if token_response.ok:
        token_response = token_response.json()
        token = token_response["access_token"]
        expiration_seconds = 60 * 60 * 24
        redis.set(token_redis_key, token, ex=expiration_seconds)
        return token
    else:
        logger.warning(f"token fetching failed, code {token_response.status_code} : {token_response}")


def get_etablishment_or_legal_unit_name(siret_response):
    has_sub_establishment = not siret_response["etablissement"].get("etablissementSiege", True)
    if has_sub_establishment:
        establishment_periods = siret_response["etablissement"]["periodesEtablissement"]
        for period in establishment_periods:
            if not period["dateFin"]:
                return period["enseigne1Etablissement"]
    return siret_response["etablissement"]["uniteLegale"]["denominationUniteLegale"]


def fetch_geo_data_from_api_insee_sirene_by_siret(canteen_siret, response, token):
    response["siret"] = canteen_siret
    try:
        redis_key = f"{settings.REDIS_PREPEND_KEY}SIRET_API_CALLS_PER_MINUTE"
        redis.incr(redis_key) if redis.exists(redis_key) else redis.set(redis_key, 1, 60)
        if int(redis.get(redis_key)) > 30:
            logger.warning("Siret lookup exceding API rate. Waiting 60 seconds.")
            time.sleep(60)

        siret_response = requests.get(
            f"https://api.insee.fr/entreprises/sirene/siret/{canteen_siret}",
            headers={"Authorization": f"Bearer {token}"},
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
        logger.error(f"Api sirene: HTTPError\n{e}")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Api sirene: ConnectionError\n{e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"Api sirene: Timeout\n{e}")
    except Exception as e:
        logger.error(f"Api sirene: Unexpected exception\n{e}")
    return response
