import logging

import requests

logger = logging.getLogger(__name__)


# DECOUPAGE_ADMINISTRATIF_DOCUMENTATION: https://geo.api.gouv.fr/decoupage-administratif
DECOUPAGE_ADMINISTRATIF_API_URL = "https://geo.api.gouv.fr"


def fetch_communes():
    response = requests.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes", timeout=50)
    response.raise_for_status()
    return response.json()


def fetch_epcis():
    response = requests.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis/?fields=nom", timeout=50)
    response.raise_for_status()
    return response.json()


def fetch_communes_from_epci(epci):
    response = requests.get(f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis/{epci}/communes?fields=code", timeout=5)
    response.raise_for_status()
    return response.json()
