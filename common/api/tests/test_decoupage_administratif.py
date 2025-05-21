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

    def test_map_communes_infos_with_arrondissements(self, mock):
        mock.get(
            f"{DECOUPAGE_ADMINISTRATIF_API_URL}/communes",
            text=json.dumps(
                [
                    {
                        "nom": "Paris",
                        "code": "75056",
                        "codeDepartement": "75",
                        "siren": "217500016",
                        "codeEpci": "200054781",
                        "codeRegion": "11",
                        "codesPostaux": [
                            "75001",
                            "75002",
                            "75003",
                            "75004",
                            "75005",
                            "75006",
                            "75007",
                            "75008",
                            "75009",
                            "75010",
                            "75011",
                            "75012",
                            "75013",
                            "75014",
                            "75015",
                            "75016",
                            "75017",
                            "75018",
                            "75019",
                            "75020",
                            "75116",
                        ],
                        "population": 2113705,
                    },
                    {
                        "nom": "Lyon",
                        "code": "69123",
                        "codeDepartement": "69",
                        "siren": "216901231",
                        "codeEpci": "200046977",
                        "codeRegion": "84",
                        "codesPostaux": [
                            "69001",
                            "69002",
                            "69003",
                            "69004",
                            "69005",
                            "69006",
                            "69007",
                            "69008",
                            "69009",
                        ],
                        "population": 520774,
                    },
                    {
                        "nom": "Marseille",
                        "code": "13055",
                        "codeDepartement": "13",
                        "siren": "211300553",
                        "codeEpci": "200054807",
                        "codeRegion": "93",
                        "codesPostaux": [
                            "13001",
                            "13002",
                            "13003",
                            "13004",
                            "13005",
                            "13006",
                            "13007",
                            "13008",
                            "13009",
                            "13010",
                            "13011",
                            "13012",
                            "13013",
                            "13014",
                            "13015",
                            "13016",
                        ],
                        "population": 877215,
                    },
                ]
            ),
        )

        communes_details = map_communes_infos()
        self.assertEqual(len(communes_details), 3 + 20 + 9 + 16)
        self.assertEqual(communes_details["69123"]["city"], "Lyon")  # initial insee code
        self.assertEqual(communes_details["69301"]["city"], "Lyon")  # enriched insee code
        self.assertEqual(communes_details["69309"]["city"], "Lyon")
        self.assertEqual(communes_details["69309"]["postal_code_list"], ["69009"])

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
