import logging
import requests
import time
from data.region_choices import Region
from django.conf import settings
import redis as r

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)

REGIONS_LIB = {i.label.split(" - ")[1]: i.value for i in Region}


def complete_canteen_data(canteen_siret, token):
    canteen = {}
    canteen["siret"] = canteen_siret
    try:
        redis_key = f"{settings.REDIS_PREPEND_KEY}SIRET_API_CALLS_PER_MINUTE"
        redis.incr(redis_key) if redis.exists(redis_key) else redis.set(redis_key, 1, 60)
        if int(redis.get(redis_key)) > 30:
            logger.warning("Siret lookup exceding API rate. Waiting 1 minute")
            time.sleep(60)

        siret_response = requests.get(
            f"https://api.insee.fr/entreprises/sirene/siret/{canteen_siret}",
            headers={"Authorization": f"Bearer {token}"},
        )
        siret_response.raise_for_status()
        if siret_response.ok:
            siret_response = siret_response.json()
            try:
                canteen["name"] = siret_response["etablissement"]["uniteLegale"]["denominationUniteLegale"]
                canteen["cityInseeCode"] = siret_response["etablissement"]["adresseEtablissement"][
                    "codeCommuneEtablissement"
                ]
                canteen["postalCode"] = siret_response["etablissement"]["adresseEtablissement"][
                    "codePostalEtablissement"
                ]
                canteen["city"] = siret_response["etablissement"]["adresseEtablissement"][
                    "libelleCommuneEtablissement"
                ]
                return canteen
            except KeyError as e:
                logger.warning(f"unexpected siret response format : {siret_response}. Unknown key : {e}")
        else:
            logger.warning(f"siret lookup failed, code {siret_response.status_code} : {siret_response}")
    except requests.exceptions.HTTPError as e:
        logger.warning(f"Geolocation Bot: HTTPError\n{e}")
    except requests.exceptions.ConnectionError as e:
        logger.warning(f"Geolocation Bot: ConnectionError\n{e}")
    except requests.exceptions.Timeout as e:
        logger.warning(f"Geolocation Bot: Timeout\n{e}")
    except Exception as e:
        logger.error(f"Geolocation Bot: Unexpected exception\n{e}")
    return canteen


def complete_location_data(response):
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


def get_city_from_siret(siret: str, token: str):
    response = complete_canteen_data(siret, token)
    response = complete_location_data(response)
    return response
