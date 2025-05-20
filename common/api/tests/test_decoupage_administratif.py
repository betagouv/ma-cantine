import json
import unittest

import requests_mock

from common.api.decoupage_administratif import (
    DECOUPAGE_ADMINISTRATIF_API_URL,
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
)


@requests_mock.Mocker()
class TestDecoupageAdministratifAPI(unittest.TestCase):
    def test_map_communes_infos(self, mock):
        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes",
            text=json.dumps(
                [
                    {
                        "nom": "L'Abergement-Clémenciat",
                        "code": "01001",
                        "codeDepartement": "01",
                        "siren": "210100012",
                        "codeEpci": "200069193",
                        "codeRegion": "84",
                        "codesPostaux": ["01400"],
                        "population": "832",
                    },
                    {
                        "nom": "L'Abergement-de-Varey",
                        "code": "01002",
                        "codeDepartement": "01",
                        "siren": "210100020",
                        "codeRegion": "84",
                        "codesPostaux": ["01640"],
                        "population": "267",
                    },
                ]
            ),
        )

        communes_details = map_communes_infos()
        self.assertEqual(len(communes_details), 2)
        self.assertCountEqual(list(communes_details.keys()), ["01001", "01002"])
        self.assertEqual(communes_details["01001"]["city"], "L'Abergement-Clémenciat")
        self.assertEqual(communes_details["01001"]["postal_code_list"], ["01400"])
        self.assertEqual(communes_details["01001"]["department"], "01")
        self.assertEqual(communes_details["01001"]["region"], "84")
        self.assertEqual(communes_details["01001"]["epci"], "200069193")
        self.assertEqual(communes_details["01002"]["city"], "L'Abergement-de-Varey")
        self.assertIsNone(communes_details["01002"]["epci"])  # Not all cities are part of an EPCI

        self.assertEqual(fetch_commune_detail("01001", communes_details, "city"), "L'Abergement-Clémenciat")
        self.assertEqual(fetch_commune_detail("01001", communes_details, "epci"), "200069193")
        self.assertEqual(fetch_commune_detail("01002", communes_details, "city"), "L'Abergement-de-Varey")
        self.assertEqual(fetch_commune_detail("01002", communes_details, "epci"), None)
        self.assertEqual(fetch_commune_detail("01003", communes_details, "city"), None)
        self.assertEqual(fetch_commune_detail("01003", communes_details, "epci"), None)

    def test_map_epcis_code_name(self, mock):
        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/epcis?fields=nom",
            text=json.dumps(
                [
                    {"nom": "CC Faucigny - Glières", "code": "200000172"},
                    {"nom": "CC du Pays de Pontchâteau St-Gildas-des-Bois", "code": "200000438"},
                ]
            ),
        )
        epci_names = map_epcis_code_name()
        self.assertEqual(len(epci_names), 2)
        self.assertEqual(epci_names["200000172"], "CC Faucigny - Glières")
        self.assertEqual(epci_names["200000438"], "CC du Pays de Pontchâteau St-Gildas-des-Bois")

        self.assertEqual(fetch_epci_name("200000172", epci_names), "CC Faucigny - Glières")
        self.assertEqual(fetch_epci_name("200000438", epci_names), "CC du Pays de Pontchâteau St-Gildas-des-Bois")
        self.assertEqual(fetch_epci_name("200000439", epci_names), None)
