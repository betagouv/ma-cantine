from unittest import mock

import requests
import requests_mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory


class CanteenStatusApiTest(APITestCase):
    @authenticate
    def test_check_siret_managed(self):
        """
        If checking a siret of a canteen that exists and I manage, give me canteen info
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertTrue(body["isManagedByUser"])
        self.assertFalse(body["canBeClaimed"])

    @authenticate
    def test_check_siret_unmanaged(self):
        """
        If checking a siret of a canteen that exists but no one manages,
        give me minimal canteen info and an indication that the canteen can be claimed
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.clear()

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertFalse(body["isManagedByUser"])
        self.assertTrue(body["canBeClaimed"])

    @authenticate
    def test_check_siret_managed_by_someone_else(self):
        """
        If checking a siret of a canteen that exists but is managed by someone else,
        give me minimal canteen info and an indication that the canteen can't be claimed
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertFalse(body["isManagedByUser"])
        self.assertFalse(body["canBeClaimed"])  # CanteenFactory creates canteens with managers

    @requests_mock.Mocker()
    @authenticate
    def test_check_siret_new_canteen(self, mock):
        siret = "34974603058674"
        city = "Paris 15e Arrondissement"
        postcode = "75015"
        insee_code = "75115"
        sirene_api_url = f"https://recherche-entreprises.api.gouv.fr/search?etat_administratif=A&page=1&per_page=1&mtm_campaign=ma-cantine&q={siret}"
        sirene_mocked_response = {
            "results": [
                {
                    "siren": "923412845",
                    "nom_complet": "Wrong name",
                    "matching_etablissements": [
                        {
                            "commune": insee_code,
                            "code_postal": postcode,
                            "libelle_commune": city,
                            "liste_enseignes": ["Legal unit name"],
                            "etat_administratif": "A",
                        }
                    ],
                }
            ],
            "total_results": 1,
        }
        mock.get(sirene_api_url, json=sirene_mocked_response)
        geo_api_url = f"https://api-adresse.data.gouv.fr/search/?q={insee_code}&citycode={insee_code}&type=municipality&autocomplete=1"
        geo_mocked_response = {
            "features": [
                {
                    "properties": {
                        "label": city,
                        "citycode": insee_code,
                        "postcode": postcode,
                        "context": "38, Isère, Auvergne-Rhône-Alpes",
                    }
                }
            ],
        }
        mock.get(geo_api_url, json=geo_mocked_response)

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertEqual(body["name"], "Legal unit name")
        self.assertEqual(body["siret"], siret)
        self.assertEqual(body["postalCode"], postcode)
        self.assertEqual(body["city"], city)
        self.assertEqual(body["cityInseeCode"], insee_code)
        self.assertEqual(body["department"], "38")

        # Check the given name if the canteen is an etablissement (sub of an unite legale)
        sirene_mocked_response = {
            "results": [
                {
                    "siren": "923412845",
                    "nom_complet": "A name",
                    "matching_etablissements": [
                        {
                            "commune": insee_code,
                            "code_postal": postcode,
                            "libelle_commune": city,
                            "liste_enseignes": ["ECOLE PRIMAIRE PUBLIQUE"],
                            "etat_administratif": "A",
                        }
                    ],
                }
            ],
            "total_results": 1,
        }
        mock.get(sirene_api_url, json=sirene_mocked_response)
        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        body = response.json()
        self.assertEqual(body["name"], "ECOLE PRIMAIRE PUBLIQUE")

    @mock.patch("requests.get", side_effect=requests.exceptions.ConnectTimeout)
    @mock.patch("requests.post", side_effect=requests.exceptions.ConnectTimeout)
    @authenticate
    def test_external_api_down(self, mock_get, mock_post):
        siret = "34974603058674"

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertNotIn("name", body)
        self.assertEqual(body["siret"], "34974603058674")
        self.assertNotIn("postalCode", body)
        self.assertNotIn("city", body)
        self.assertNotIn("cityInseeCode", body)
        self.assertNotIn("department", body)
