import logging
import json
import requests

from data.models.geo import Region

logger = logging.getLogger(__name__)

REGIONS_LIB = {i.label.split(" - ")[1]: i.value for i in Region}
# ADRESSE_API_DOCUMENTATION: https://adresse.data.gouv.fr/outils/api-doc/adresse
ADRESSE_API_URL = "https://api-adresse.data.gouv.fr/search"
ADRESSE_CSV_API_URL = "https://api-adresse.data.gouv.fr/search/csv"


def fetch_geo_data_from_code(response):
    try:
        location_response = requests.get(
            f"{ADRESSE_API_URL}/?q={response['cityInseeCode']}&citycode={response['cityInseeCode']}&type=municipality&autocomplete=1"
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


def fetch_geo_data_from_code_csv(csv_str, timeout=4):
    # NB: max size of a csv file is 50 MB
    response = requests.post(
        ADRESSE_CSV_API_URL,
        files={
            "data": ("locations.csv", csv_str),
        },
        data={
            "postcode": "postcode",
            "citycode": "citycode",
            "result_columns": ["result_citycode", "result_postcode", "result_city", "result_context"],
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.text


def mock_fetch_geo_data_from_code(mock, city_insee_code):
    api_url = f"https://api-adresse.data.gouv.fr/search/?q={city_insee_code}&citycode={city_insee_code}&type=municipality&autocomplete=1"
    mock.get(
        api_url,
        text=json.dumps(
            {
                # city_insee_code: 59512
                "features": [
                    {
                        "properties": {
                            "label": "ROUBAIX",
                            "citycode": "59512",
                            "postcode": "59100",
                            "context": "38, Isère, Auvergne-Rhône-Alpes",
                        }
                    }
                ],
            }
        ),
    )
