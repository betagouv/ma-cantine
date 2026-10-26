import logging


from api.views.utils import update_change_reason
from common.api.datagouv import (
    fetch_commune_pat_list,
    map_pat_list_to_communes_insee_code,
)
from common.api.decoupage_administratif import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)
from common.api.recherche_entreprises import fetch_geo_data_from_siret
from data.models.geo import get_lib_department_from_code, get_lib_region_from_code


logger = logging.getLogger(__name__)


#########################################################
# Canteen geo data (called on the Canteen post_save, see data/models/canteen.py)


def update_canteen_geo_fields_from_siret(canteen):
    """
    Input: Canteen with siret but no city_insee_code
    Processing: API Recherche Entreprises + API Découpage Administratif (cached)
    Output: Fill canteen's city_insee_code field + geo fields
    """
    logger.info("Starting update_canteen_geo_fields_from_siret task")

    # clear dirty fields (and avoid possible recursion errors if coming from post_save)
    canteen.refresh_from_db()

    update = False
    # Step 1: fetch city_insee_code from API Recherche Entreprises
    if not canteen.city_insee_code:
        response = fetch_geo_data_from_siret(canteen.siret)
        if response:
            try:
                if "city_insee_code" in response.keys():
                    canteen.city_insee_code = response["city_insee_code"]
                    canteen.siret_etat_administratif = response["etat_administratif"]
                    update = True
            except Exception as e:
                logger.error(e)
        else:
            if not canteen.siret_inconnu:
                canteen.siret_inconnu = True
                update = True
    # Step 2: fetch geo data from API Découpage Administratif & DataGouv
    if canteen.city_insee_code:
        _update_canteen_geo_data_from_insee_code(canteen)
    # Step 3: save & return
    if update:
        canteen._change_reason = "Données de localisation MAJ"
        canteen.save(skip_validations=True)

    return True


def update_canteen_geo_data_from_insee_code(canteen):
    """
    Similar to update_canteen_geo_fields_from_siret, but this time we already have the city_insee_code.
    Processing: API Découpage Administratif (cached)
    Output: Fill canteen's geo fields
    """
    # clear dirty fields (and avoid possible recursion errors if coming from post_save)
    canteen.refresh_from_db()

    if canteen.city_insee_code:
        _update_canteen_geo_data_from_insee_code(canteen)


def _update_canteen_geo_data_from_insee_code(canteen):  # noqa C901
    # fetch geo data from API Découpage Administratif & DataGouv
    communes_details = map_communes_infos()
    epcis_names = map_epcis_code_name()
    pat_mapping = map_pat_list_to_communes_insee_code()

    update = False
    # geo fields
    if canteen.city_insee_code in communes_details:
        if not canteen.postal_code:
            postal_code_list = fetch_commune_detail(canteen.city_insee_code, communes_details, "postal_code_list")
            postal_code = postal_code_list[0] if postal_code_list else None
            if postal_code_list:
                canteen.postal_code = postal_code
                update = True
        if not canteen.city:
            city = fetch_commune_detail(canteen.city_insee_code, communes_details, "city")
            if city:
                canteen.city = city
                update = True
        if not canteen.epci:
            epci = fetch_commune_detail(canteen.city_insee_code, communes_details, "epci")
            if epci:
                canteen.epci = epci
                update = True
        if not canteen.pat_list:
            pat_list = fetch_commune_pat_list(canteen.city_insee_code, pat_mapping, "id")
            if pat_list:
                canteen.pat_list = pat_list
                update = True
        if not canteen.department:
            department = fetch_commune_detail(canteen.city_insee_code, communes_details, "department")
            if department:
                canteen.department = department
                update = True
        if not canteen.region:
            region = fetch_commune_detail(canteen.city_insee_code, communes_details, "region")
            if region:
                canteen.region = region
                update = True
    # geo lib fields
    if canteen.epci and not canteen.epci_lib and canteen.epci in epcis_names:
        canteen.epci_lib = fetch_epci_name(canteen.epci, epcis_names)
        update = True
    if canteen.pat_list and not canteen.pat_lib_list:
        canteen.pat_lib_list = fetch_commune_pat_list(canteen.city_insee_code, pat_mapping, "lib")
        update = True
    if canteen.department and not canteen.department_lib:
        canteen.department_lib = get_lib_department_from_code(canteen.department)
        update = True
    if canteen.region and not canteen.region_lib:
        canteen.region_lib = get_lib_region_from_code(canteen.region)
        update = True
    # save
    if update:
        canteen.save(skip_validations=True)
        update_change_reason(canteen, "Données de localisation MAJ par bot, via code INSEE")
        return True
