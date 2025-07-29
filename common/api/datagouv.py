import csv
import json
import logging
import os
from datetime import date

import requests

logger = logging.getLogger(__name__)


# DATAGOUV_DOCUMENTATION: https://www.data.gouv.fr/fr/dataservices/api-catalogue-des-donnees-ouvertes-data-gouv-fr/
DATAGOUV_API_URL = "https://www.data.gouv.fr/api/1"

# PAT (Projets Alimentaires Territoriaux): https://france-pat.fr/presentation-de-l-observatoire/
# Note: data updated twice a year
# Note: communes can belong to multiple PATs
PAT_DATAGOUV_DATASET_ID = "pat-projets-alimentaires-territoriaux-description"
# PAT_DATAGOUV_RESOURCE_ID = "4f2a6bed-e9e3-48eb-aecc-85b08cb984f3"  # 20250224
PAT_DATAGOUV_RESOURCE_ID = "96606cae-0b3b-4910-9d8b-65e3dd7f1bda"  # 20250224 (ISO-8859-1)
PAT_DATAGOUV_CSV_URL = "https://static.data.gouv.fr/resources/pat-projets-alimentaires-territoriaux-description/20250224-103639/pats-20250224-win1252.csv"


def get_dataset(dataset_id):
    try:
        response = requests.get(f"{DATAGOUV_API_URL}/datasets/{dataset_id}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(f"Datagouv dataset get: Error while getting dataset: {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


def get_dataset_resource(dataset_id, resource_id):
    try:
        response = requests.get(f"{DATAGOUV_API_URL}/datasets/{dataset_id}/resources/{resource_id}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        logger.error(
            f"Datagouv dataset resource get: Error while getting dataset resource: {dataset_id} / {resource_id}"
        )
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


def update_dataset_resources(dataset_id):
    """
    Updating the URL of the different resources displayed on data.gouv.fr in order to force their cache reload and display the correct update dates
    Returns: Number of updated resources
    """
    DATAGOUV_API_KEY = os.getenv("DATAGOUV_API_KEY", "")
    DATAGOUV_API_HEADER = {"X-API-KEY": DATAGOUV_API_KEY}

    if not (dataset_id and DATAGOUV_API_KEY):
        logger.warning("Datagouv resource update: API key or dataset id incorrect values")
        return

    try:
        dataset = get_dataset(dataset_id)
        resources = dataset["resources"]
        count_updated_resources = 0
        for resource in resources:
            if resource["format"] in ["xlsx", "csv"]:
                today = date.today()
                updated_url = resource["url"].split("?v=")[0] + "?v=" + today.strftime("%Y%m%d")
                response = requests.put(
                    f'{DATAGOUV_API_URL}/datasets/{dataset_id}/resources/{resource["id"]}',
                    headers=DATAGOUV_API_HEADER,
                    json={"url": updated_url},
                )
                response.raise_for_status()
                count_updated_resources += 1
        logger.info(f"{count_updated_resources} datagouv's ressources have been updated")
        return count_updated_resources
    except requests.HTTPError as e:
        logger.error(f"Datagouv resource update: Error while updating dataset: {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)


def get_pat_list():
    """
    Fetch PAT list from data.gouv.fr
    Returns: a list of PATs
    """
    pat_list = []
    try:
        pat_dataset_resource = get_dataset_resource(PAT_DATAGOUV_DATASET_ID, PAT_DATAGOUV_RESOURCE_ID)
        response = requests.get(pat_dataset_resource["url"])
        response.raise_for_status()
        reader = csv.DictReader(response.iter_lines(decode_unicode=True), delimiter=";")
        pat_list = list(reader)
    except requests.HTTPError as e:
        logger.info(e)
    return pat_list


def map_pat_list_to_communes_insee_code():
    """
    Create a dict that maps Insee codes with their PAT
    Input: a list of PAT. 891;https://france-pat.fr/pat/redon-agglomeration/;"Programme Agricole et Alimentaire de Territoire de REDON Agglomération";;"Pays de la Loire, Bretagne";"Ille-et-Vilaine, Loire-Atlantique, Morbihan";;35145,56232,44185,56011,56216,56250,44067,35045,35268,35285,35064,35151,35219,56221,35236,56154,56239,35013,35237,56001,56223,44123,35328,44057,44092,56194,35294,44044,44128,56060,44007;...
    Output: a dict with the commune's insee code as pivot. {"35145": [{"pat": "891", "pat_lib": "Programme Agricole et Alimentaire de Territoire de REDON Agglomération"}]}
    """
    pat_mapping = {}
    try:
        pat_list = get_pat_list()
        for pat in pat_list:
            pat_city_insee_code_list = [
                insee_code for insee_code in pat["communes_code_insee"].split(",") if insee_code
            ]
            for city_insee_code in pat_city_insee_code_list:
                if city_insee_code not in pat_mapping.keys():
                    pat_mapping[city_insee_code] = []
                pat_mapping[city_insee_code].append(
                    {
                        "pat": pat["id"],
                        "pat_lib": pat["nom_administratif"],
                    }
                )
    except requests.HTTPError as e:
        logger.info(e)
    return pat_mapping


def fetch_commune_pat_list(code_insee_commune, pat_mapping, geo_detail_type):
    """
    Provide List of PAT city, given the insee code of the city
    """
    if code_insee_commune and code_insee_commune in pat_mapping.keys():
        if geo_detail_type == "id":
            return [pat["pat"] for pat in pat_mapping[code_insee_commune]]
        elif geo_detail_type == "lib":
            return [pat["pat_lib"] for pat in pat_mapping[code_insee_commune]]


def mock_get_pat_dataset_resource(mock, success=True):
    if not success:
        mock.get(
            f"{DATAGOUV_API_URL}/datasets/{PAT_DATAGOUV_DATASET_ID}/resources/{PAT_DATAGOUV_RESOURCE_ID}",
            text=json.dumps({}),
            status_code=403,
        )
    mock.get(
        f"{DATAGOUV_API_URL}/datasets/{PAT_DATAGOUV_DATASET_ID}/resources/{PAT_DATAGOUV_RESOURCE_ID}",
        text=json.dumps(
            {
                "id": "96606cae-0b3b-4910-9d8b-65e3dd7f1bda",
                "title": "pats-20250224-win1252.csv",
                "url": f"{PAT_DATAGOUV_CSV_URL}",
            }
        ),
        status_code=200,
    )


def mock_get_pat_csv(mock, success=True):
    if not success:
        mock.get(
            f"{PAT_DATAGOUV_CSV_URL}",
            text="",
            status_code=403,
        )
    pat_csv_text = (
        "id;lien_vers_la_fiche_pat;nom_administratif;nom_usuel;regions;departement;epci;communes_code_insee\n"
    )
    pat_csv_text += '891;https://france-pat.fr/pat/redon-agglomeration/;"Programme Agricole et Alimentaire de Territoire de REDON Agglomération";;"Pays de la Loire, Bretagne";"Ille-et-Vilaine, Loire-Atlantique, Morbihan";;35145,56232,44185,56011,56216,56250,44067,35045,35268,35285,35064,35151,35219,56221,35236,56154,56239,35013,35237,56001,56223,44123,35328,44057,44092,56194,35294,44044,44128,56060,44007\n'
    pat_csv_text += '1294;https://france-pat.fr/pat/pat-de-lisere/;"PAT du Département de l\'Isère";"PAT de l\'Isère";Auvergne-Rhône-Alpes;Isère;;38019,38039,38055,38071,38089,38106,38127,38146,38162,38182,38199,38217,38237,38254,38271,38288,38308,38325,38342,38358,38376,38393,38409,38426,38444,38462,38479,38498,38517,38533,38551,38567,38001,38020,38040,38056,38072,38090,38107,38128,38147,38163,38183,38200,38218,38238,38255,38272,38289,38309,38326,38343,38359,38377,38394,38410,38427,38445,38463,38480,38499,38518,38535,38552,38002,38022,38041,38057,38073,38091,38108,38129,38148,38166,38184,38203,38219,38239,38256,38273,38290,38310,38328,38344,38360,38378,38395,38412,38428,38446,38464,38481,38500,38519,38536,38553,38003,38023,38042,38058,38074,38092,38109,38130,38149,38167,38185,38204,38221,38240,38257,38275,38291,38311,38329,38345,38361,38379,38396,38413,38429,38448,38465,38483,38501,38520,38537,38554,38004,38026,38043,38059,38075,38093,38110,38131,38150,38169,38186,38205,38222,38241,38258,38276,38292,38313,38330,38346,38362,38380,38397,38414,38430,38449,38466,38484,38503,38521,38538,38555,38005,38027,38044,38060,38076,38094,38111,38132,38151,38170,38187,38206,38223,38242,38259,38277,38294,38314,38331,38347,38363,38381,38398,38415,38431,38450,38467,38485,38504,38522,38539,38556,38006,38029,38045,38061,38077,38095,38112,38133,38152,38171,38188,38207,38224,38243,38260,38278,38295,38315,38332,38348,38364,38382,38399,38416,38432,38451,38468,38486,38505,38523,38540,38557,38008,38030,38046,38062,38078,38097,38113,38134,38153,38172,38189,38208,38225,38244,38261,38279,38296,38316,38333,38349,38365,38383,38400,38417,38433,38452,38469,38487,38507,38524,38542,38558,38009,38031,38047,38063,38080,38098,38114,38135,38154,38173,38190,38209,38226,38245,38263,38280,38297,38317,38334,38350,38366,38384,38401,38418,38434,38453,38470,38488,38508,38525,38543,38559,38010,38032,38048,38064,38081,38099,38115,38136,38155,38174,38191,38210,38228,38246,38264,38281,38298,38318,38335,38351,38368,38386,38402,38419,38436,38454,38471,38489,38509,38526,38544,38560,38011,38033,38049,38065,38082,38100,38116,38137,38156,38175,38192,38211,38229,38247,38265,38282,38299,38319,38336,38352,38369,38387,38403,38420,38437,38455,38472,38490,38511,38527,38545,38561,38012,38034,38050,38066,38083,38101,38117,38138,38157,38176,38193,38212,38230,38248,38266,38283,38300,38320,38337,38353,38370,38388,38404,38421,38438,38456,38473,38492,38512,38528,38546,38562,38013,38035,38051,38067,38084,38102,38118,38139,38158,38177,38194,38213,38231,38249,38267,38284,38301,38321,38338,38354,38372,38389,38405,38422,38439,38457,38474,38494,38513,38529,38547,38563,38015,38036,38052,38068,38085,38103,38120,38140,38159,38179,38195,38214,38232,38250,38268,38285,38303,38322,38339,38355,38373,38390,38406,38423,38440,38458,38475,38495,38514,38530,38548,38564,38017,38037,38053,38069,38086,38104,38124,38141,38160,38180,38197,38215,38235,38252,38269,38286,38304,38323,38340,38356,38374,38391,38407,38424,38442,38459,38476,38496,38515,38531,38549,38565,38018,38038,38054,38070,38087,38105,38126,38144,38161,38181,38198,38216,38236,38253,38270,38287,38307,38324,38341,38357,38375,38392,38408,38425,38443,38460,38478,38497,38516,38532,38550,38566\n'
    mock.get(
        f"{PAT_DATAGOUV_CSV_URL}",
        text=pat_csv_text,
        status_code=200,
    )
