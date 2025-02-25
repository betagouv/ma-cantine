import unittest
from unittest.mock import Mock, patch

import requests

from common.api.recherche_entreprises import fetch_geo_data_from_siret


@patch("common.utils.siret.is_valid_siret", return_value=True)
class TestFetchGeoDataFromSiret(unittest.TestCase):

    @patch("requests.get")
    def test_fetch_geo_data_from_siret_success(self, mock_get, mock_is_valid_siret):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "results": [
                {
                    "siren": "923412845",
                    "nom_complet": "LA TURBINE",
                    "nom_raison_sociale": "LA TURBINE",
                    "nombre_etablissements_ouverts": 1,
                    "siege": {
                        "commune": "59512",
                    },
                    "etat_administratif": "A",
                    "matching_etablissements": [
                        {
                            "commune": "12345",
                            "code_postal": "75001",
                            "libelle_commune": "PARIS",
                            "date_debut_activite": "2023-01-15",
                            "est_siege": "true",
                            "etat_administratif": "A",
                            "siret": "92341284500011",
                        }
                    ],
                }
            ],
            "total_results": 1,
            "page": 1,
            "per_page": 10,
            "total_pages": 1,
        }

        mock_get.return_value = mock_response

        response = {}
        canteen_siret = "12345678901234"
        expected_response = {
            "siret": canteen_siret,
            "name": "Foo",
            "cityInseeCode": "12345",
            "postalCode": "75001",
            "city": "Paris",
        }

        with patch("common.api.recherche_entreprises.get_etablishment_or_legal_unit_name", return_value="Foo"):
            result = fetch_geo_data_from_siret(canteen_siret, response)
            self.assertEqual(result, expected_response)

    def test_fetch_geo_data_from_siret_invalid_siret(self, mock_is_valid_siret):
        response = {}
        canteen_siret = "invalid_siret"
        result = fetch_geo_data_from_siret(canteen_siret, response)
        self.assertIsNone(result)

    @patch("requests.get")
    def test_fetch_geo_data_from_siret_no_results(self, mock_get, mock_is_valid_siret):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"total_results": 0}
        mock_get.return_value = mock_response

        response = {}
        canteen_siret = "12345678901234"
        result = fetch_geo_data_from_siret(canteen_siret, response)
        self.assertIsNone(result)

    @patch("requests.get", side_effect=requests.exceptions.HTTPError)
    def test_fetch_geo_data_from_siret_http_error(self, mock_get, mock_is_valid_siret):
        response = {}
        canteen_siret = "12345678901234"
        result = fetch_geo_data_from_siret(canteen_siret, response)
        self.assertEqual(result, {"siret": canteen_siret})

    @patch("requests.get", side_effect=requests.exceptions.ConnectionError)
    def test_fetch_geo_data_from_siret_connection_error(self, mock_get, mock_is_valid_siret):
        response = {}
        canteen_siret = "12345678901234"
        result = fetch_geo_data_from_siret(canteen_siret, response)
        self.assertEqual(result, {"siret": canteen_siret})

    @patch("requests.get", side_effect=requests.exceptions.Timeout)
    def test_fetch_geo_data_from_siret_timeout(self, mock_get, mock_is_valid_siret):
        response = {}
        canteen_siret = "12345678901234"
        result = fetch_geo_data_from_siret(canteen_siret, response)
        self.assertEqual(result, {"siret": canteen_siret})

    @patch("requests.get", side_effect=Exception)
    def test_fetch_geo_data_from_siret_unexpected_exception(self, mock_get, mock_is_valid_siret):
        response = {}
        canteen_siret = "12345678901234"
        result = fetch_geo_data_from_siret(canteen_siret, response)
        self.assertEqual(result, {"siret": canteen_siret})
