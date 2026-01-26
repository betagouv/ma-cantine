import unittest

import requests_mock

from django.core.cache import cache

from common.api.decoupage_administratif import (
    fetch_commune_detail,
    fetch_epci_name,
    map_communes_infos,
    map_epcis_code_name,
    mock_fetch_communes,
    mock_fetch_epcis,
)


@requests_mock.Mocker()
class TestDecoupageAdministratifAPI(unittest.TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_map_communes_infos(self, mock):
        mock_fetch_communes(mock)

        communes_details = map_communes_infos()

        self.assertEqual(mock.call_count, 1)
        self.assertEqual(len(communes_details), 3)
        self.assertCountEqual(list(communes_details.keys()), ["01002", "38185", "59512"])
        self.assertEqual(communes_details["01002"]["city"], "L'Abergement-de-Varey")
        self.assertEqual(communes_details["01002"]["postal_code_list"], ["01640"])
        self.assertEqual(communes_details["01002"]["department"], "01")
        self.assertEqual(communes_details["01002"]["region"], "84")
        self.assertIsNone(communes_details["01002"]["epci"])  # Not all cities are part of an EPCI
        self.assertEqual(communes_details["38185"]["city"], "Grenoble")

        self.assertEqual(fetch_commune_detail("01002", communes_details, "city"), "L'Abergement-de-Varey")
        self.assertEqual(fetch_commune_detail("01002", communes_details, "epci"), None)
        self.assertEqual(fetch_commune_detail("01002", communes_details, "city"), "L'Abergement-de-Varey")
        self.assertEqual(fetch_commune_detail("01002", communes_details, "epci"), None)
        self.assertEqual(fetch_commune_detail("01003", communes_details, "city"), None)
        self.assertEqual(fetch_commune_detail("01003", communes_details, "epci"), None)

        # Second call to test caching
        communes_details = map_communes_infos()

        self.assertEqual(mock.call_count, 1)  # no additional API call
        self.assertEqual(len(communes_details), 2)

    def test_map_epcis_code_name(self, mock):
        mock_fetch_epcis(mock)

        epci_names = map_epcis_code_name()

        self.assertEqual(mock.call_count, 1)
        self.assertEqual(len(epci_names), 2)
        self.assertEqual(epci_names["200000172"], "CC Faucigny - Glières")
        self.assertEqual(epci_names["200040715"], "Grenoble-Alpes-Métropole")

        self.assertEqual(fetch_epci_name("200000172", epci_names), "CC Faucigny - Glières")
        self.assertEqual(fetch_epci_name("200040715", epci_names), "Grenoble-Alpes-Métropole")
        self.assertEqual(fetch_epci_name("200000439", epci_names), None)
