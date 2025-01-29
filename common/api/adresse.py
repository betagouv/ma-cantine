import logging

import requests

from data.region_choices import Region

logger = logging.getLogger(__name__)

REGIONS_LIB = {i.label.split(" - ")[1]: i.value for i in Region}


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
