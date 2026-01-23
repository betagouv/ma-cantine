import unittest

import requests_mock

from django.core.cache import cache
from common.api.datagouv import (
    map_pat_list_to_communes_insee_code,
    mock_get_pat_csv,
    mock_get_pat_dataset_resource,
)


@requests_mock.Mocker()
class TestDataGouvAPI(unittest.TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_map_pat_list_to_communes_insee_code(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        pat_list_to_communes_insee_code = map_pat_list_to_communes_insee_code()

        self.assertEqual(mock.call_count, 1 + 1)
        self.assertEqual(len(pat_list_to_communes_insee_code), 543)
        self.assertIn("35145", pat_list_to_communes_insee_code)
        self.assertEqual(pat_list_to_communes_insee_code["35145"][0]["pat"], "891")
        self.assertEqual(
            pat_list_to_communes_insee_code["35145"][0]["pat_lib"],
            "Programme Agricole et Alimentaire de Territoire de REDON Agglomération",
        )

        # Second call to test caching
        pat_list_to_communes_insee_code = map_pat_list_to_communes_insee_code()

        self.assertEqual(mock.call_count, 2)  # no additional API call
        self.assertEqual(len(pat_list_to_communes_insee_code), 543)
