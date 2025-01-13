import logging
import time
import zoneinfo
from datetime import datetime

import redis as r
import requests
from django.conf import settings

from data.region_choices import Region

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)

REGIONS_LIB = {i.label.split(" - ")[1]: i.value for i in Region}

CAMPAIGN_DATES = {
    2021: {
        "start_date": datetime(2022, 7, 16, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2022, 12, 5, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2022: {
        "start_date": datetime(2023, 2, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2023, 7, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2023: {
        "start_date": datetime(2024, 1, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2024, 6, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
    2024: {
        "start_date": datetime(2025, 1, 7, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        "end_date": datetime(2025, 3, 31, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
    },
}


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


def fetch_geo_data_from_api_entreprise_by_siret(response):
    try:
        location_response = requests.get(
            f"https://api-adresse.data.gouv.fr/search/?q={response['cityInseeCode']}&citycode={response['cityInseeCode']}&type=municipality&autocomplete=1"
        )
        if location_response.ok:
            location_response = location_response.json()
            results = location_response["features"]
            if results and results[0]:
                try:
                    result = results[0]["properties"]
                    if result:
                        response["city"] = result["label"]
                        response["city_insee_code"] = result["citycode"]
                        response["postal_code"] = result["postcode"]
                        response["department"] = result["context"].split(",")[0]
                        response["department_lib"] = result["context"].split(", ")[1]
                        response["region_lib"] = result["context"].split(", ")[2]
                        response["region"] = int(REGIONS_LIB[response["region_lib"]])
                        return response
                except KeyError as e:
                    logger.warning(f"unexpected location response format : {location_response}. Unknown key : {e}")
            else:
                logger.warning(
                    f"features array for city '{response['city']}' in location response format is non-existant or empty : {location_response}"
                )
        else:
            logger.warning(
                f"location fetching failed, code {location_response.status_code} : {location_response.json()}"
            )
    except Exception as e:
        logger.exception(f"Error completing location data with SIRET for city: {response['city']}")
        logger.exception(e)
    return response
