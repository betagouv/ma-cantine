import unittest
from unittest.mock import Mock, patch

import requests

from common.api.recherche_entreprises import fetch_geo_data_from_siret


@patch("common.utils.siret.is_valid_length_siret", return_value=True)
class TestRechercheEntrepriseAPI(unittest.TestCase):
    @patch("requests.get")
    def test_fetch_geo_data_from_siret_success(self, mock_get, mock_is_valid_length_siret):
        canteen_siret = "92341284500011"
        test_cases = [
            {
                "name": "Valid without enseigne",
                "data": {
                    "results": [
                        {
                            "siren": "923412845",
                            "nom_complet": "Foo",
                            "etat_administratif": "A",
                            "matching_etablissements": [
                                {
                                    "commune": "12345",
                                    "code_postal": "75001",
                                    "libelle_commune": "PARIS",
                                    "etat_administratif": "A",
                                }
                            ],
                        }
                    ],
                    "total_results": 1,
                },
                "expected_outcome": {
                    "siret": canteen_siret,
                    "name": "Foo",
                    "cityInseeCode": "12345",
                    "postalCode": "75001",
                    "city": "PARIS",
                },
            },
            {
                "name": "Valid with enseigne",
                "data": {
                    "results": [
                        {
                            "siren": "923412845",
                            "nom_complet": "Wrong name",
                            "etat_administratif": "A",
                            "matching_etablissements": [
                                {
                                    "commune": "12345",
                                    "code_postal": "75001",
                                    "libelle_commune": "PARIS",
                                    "date_debut_activite": "2023-01-15",
                                    "etat_administratif": "A",
                                    "liste_enseignes": ["Foo"],
                                }
                            ],
                        }
                    ],
                    "total_results": 1,
                },
                "expected_outcome": {
                    "siret": canteen_siret,
                    "name": "Foo",
                    "cityInseeCode": "12345",
                    "postalCode": "75001",
                    "city": "PARIS",
                },
            },
            {
                "name": "Valid with enseigne",
                "data": {
                    "results": [],
                    "total_results": 0,
                },
                "expected_outcome": None,
            },
        ]
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value

        for tc in test_cases:
            mock_response.json.return_value = tc["data"]
            mock_get.return_value = mock_response
            result = fetch_geo_data_from_siret(canteen_siret)
            self.assertEqual(result, tc["expected_outcome"])

    def test_fetch_geo_data_from_siret_invalid_siret(self, mock_is_valid_length_siret):
        canteen_siret = "invalid_siret"
        result = fetch_geo_data_from_siret(canteen_siret)
        self.assertIsNone(result)

    @patch("requests.get")
    def test_fetch_geo_data_from_siret_no_results(self, mock_get, mock_is_valid_length_siret):
        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {"total_results": 0}
        mock_get.return_value = mock_response

        canteen_siret = "92341284500011"
        result = fetch_geo_data_from_siret(canteen_siret)
        self.assertIsNone(result)

    @patch("requests.get", side_effect=requests.exceptions.HTTPError)
    def test_fetch_geo_data_from_siret_http_error(self, mock_get, mock_is_valid_length_siret):
        canteen_siret = "92341284500011"
        result = fetch_geo_data_from_siret(canteen_siret)
        self.assertEqual(result, {"siret": canteen_siret})

    @patch("requests.get", side_effect=requests.exceptions.ConnectionError)
    def test_fetch_geo_data_from_siret_connection_error(self, mock_get, mock_is_valid_length_siret):
        canteen_siret = "92341284500011"
        result = fetch_geo_data_from_siret(canteen_siret)
        self.assertEqual(result, {"siret": canteen_siret})

    @patch("requests.get", side_effect=requests.exceptions.Timeout)
    def test_fetch_geo_data_from_siret_timeout(self, mock_get, mock_is_valid_length_siret):
        canteen_siret = "92341284500011"
        result = fetch_geo_data_from_siret(canteen_siret)
        self.assertEqual(result, {"siret": canteen_siret})

    @patch("requests.get", side_effect=Exception)
    def test_fetch_geo_data_from_siret_unexpected_exception(self, mock_get, mock_is_valid_length_siret):
        canteen_siret = "92341284500011"
        result = fetch_geo_data_from_siret(canteen_siret)
        self.assertEqual(result, {"siret": canteen_siret})
