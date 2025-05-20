import json
import unittest

import requests_mock

from common.api.decoupage_administratif import (
    DECOUPAGE_ADMINISTRATIF_API_URL,
    map_communes_infos,
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
