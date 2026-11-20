import json
import unittest
from unittest.mock import Mock, patch

import requests
import requests_mock

from common.api.recherche_entreprises import (
    DEFAULT_PARAMS,
    MOCK_SIRET_92341284500011_RESULTS,
    RECHERCHE_ENTREPRISES_API_URL,
    fetch_geo_data_from_siret,
    fetch_recherche_entreprises_data,
    mock_fetch_geo_data_from_siren,
    mock_fetch_geo_data_from_siret,
)


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
                    "city_insee_code": "12345",
                    "postal_code": "75001",
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
                    "city_insee_code": "12345",
                    "postal_code": "75001",
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


@requests_mock.Mocker()
class TestFetchRechercheEntreprisesData(unittest.TestCase):
    def test_siret_found(self, mock):
        mock_fetch_geo_data_from_siret(mock, siret="21380185500072", success=True)
        data = fetch_recherche_entreprises_data(siret="21380185500072")
        self.assertEqual(data["source"], "siret")
        self.assertEqual(data["query"], "21380185500072")
        self.assertEqual(data["status"], "ok")
        self.assertIn("fetch_date", data)
        self.assertEqual(
            data["unite_legale"],
            {
                "etat_administratif": "A",
                "date_fermeture": None,
                "nature_juridique": "7210",
                "activite_principale": "84.11Z",
            },
        )
        self.assertEqual(
            data["etablissement"],
            {"etat_administratif": "F", "date_fermeture": "2000-05-01", "activite_principale": "36.00Z"},
        )

    def test_siret_not_found(self, mock):
        mock_fetch_geo_data_from_siret(mock, siret="00000000000000", success=True)
        data = fetch_recherche_entreprises_data(siret="00000000000000")
        self.assertEqual(data["status"], "not_found")
        self.assertIsNone(data["unite_legale"])
        self.assertIsNone(data["etablissement"])

    def test_siret_result_not_matching(self, mock):
        # the API returns another unite_legale (fuzzy search): not found
        mock.get(
            f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q=92341284500029",
            text=json.dumps({"results": MOCK_SIRET_92341284500011_RESULTS, "total_results": 1}),
        )
        data = fetch_recherche_entreprises_data(siret="92341284500029")
        self.assertEqual(data["status"], "not_found")

    def test_siret_invalid(self, mock):
        data = fetch_recherche_entreprises_data(siret="123")
        self.assertEqual(data["status"], "not_found")
        self.assertFalse(mock.called)

    def test_siren_found(self, mock):
        mock_fetch_geo_data_from_siren(mock, siren="213401722", success=True)
        data = fetch_recherche_entreprises_data(siren="213401722")
        self.assertEqual(data["source"], "siren")
        self.assertEqual(data["query"], "213401722")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["unite_legale"]["nature_juridique"], "7210")
        self.assertIsNone(data["etablissement"])  # the siege isn't the canteen

    def test_siren_not_found(self, mock):
        mock_fetch_geo_data_from_siren(mock, siren="000000000", success=True)
        data = fetch_recherche_entreprises_data(siren="000000000")
        self.assertEqual(data["status"], "not_found")

    def test_api_error(self, mock):
        mock_fetch_geo_data_from_siret(mock, siret="92341284500011", success=False)  # 403
        self.assertIsNone(fetch_recherche_entreprises_data(siret="92341284500011"))
        mock.get(f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q=92341284500011", status_code=429)
        self.assertIsNone(fetch_recherche_entreprises_data(siret="92341284500011"))
        mock.get(f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q=92341284500011", exc=requests.exceptions.Timeout)
        self.assertIsNone(fetch_recherche_entreprises_data(siret="92341284500011"))

    def test_unexpected_format(self, mock):
        mock.get(f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q=92341284500011", text="not json")
        self.assertIsNone(fetch_recherche_entreprises_data(siret="92341284500011"))
        mock.get(
            f"{RECHERCHE_ENTREPRISES_API_URL}?{DEFAULT_PARAMS}&q=92341284500011",
            text=json.dumps(
                {"results": [{"siren": "923412845", "matching_etablissements": [{"siret": "92341284500011"}]}]}
            ),
        )
        self.assertIsNone(fetch_recherche_entreprises_data(siret="92341284500011"))  # missing fields
