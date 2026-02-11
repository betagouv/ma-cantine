from unittest import mock

import requests
import requests_mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory
from common.api.recherche_entreprises import mock_fetch_geo_data_from_siret, mock_fetch_geo_data_from_siren
from common.api.adresse import mock_fetch_geo_data_from_code


class CanteenStatusBySiretApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.siret = "92341284500011"
        cls.insee_code = "59512"
        cls.postcode = "59100"
        cls.url = reverse("canteen_status_by_siret", kwargs={"siret": cls.siret})

    @authenticate
    def test_check_siret_managed(self):
        """
        If checking a siret of a canteen that exists and I manage, give me canteen info
        """
        canteen = CanteenFactory(siret=self.siret, managers=[authenticate.user])

        response = self.client.get(self.url)

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
        canteen = CanteenFactory(siret=self.siret)
        canteen.managers.clear()

        response = self.client.get(self.url)

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
        canteen = CanteenFactory(siret=self.siret)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertFalse(body["isManagedByUser"])
        self.assertFalse(body["canBeClaimed"])  # CanteenFactory creates canteens with managers

    @requests_mock.Mocker()
    @authenticate
    def test_check_siret_new_canteen(self, mock):
        mock_fetch_geo_data_from_siret(mock, self.siret)
        mock_fetch_geo_data_from_code(mock, self.insee_code)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertEqual(body["name"], "LA TURBINE")
        self.assertEqual(body["siret"], self.siret)
        self.assertEqual(body["postalCode"], "59100")
        self.assertEqual(body["city"], "ROUBAIX")
        self.assertEqual(body["cityInseeCode"], "59512")
        self.assertEqual(body["department"], "38")

    @requests_mock.Mocker()
    @authenticate
    def test_check_siret_existing_canteen(self, mock):
        canteen = CanteenFactory(siret=self.siret)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)

    @mock.patch("requests.get", side_effect=requests.exceptions.ConnectTimeout)
    @mock.patch("requests.post", side_effect=requests.exceptions.ConnectTimeout)
    @authenticate
    def test_external_api_down(self, mock_get, mock_post):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertNotIn("name", body)
        self.assertEqual(body["siret"], self.siret)
        self.assertNotIn("postalCode", body)
        self.assertNotIn("city", body)
        self.assertNotIn("cityInseeCode", body)
        self.assertNotIn("department", body)


class CanteenStatusBySirenApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.siren = "923412845"
        cls.url = reverse("canteen_status_by_siren", kwargs={"siren": cls.siren})

    @requests_mock.Mocker()
    @authenticate
    def test_check_siren_new_canteen(self, mock):
        mock_fetch_geo_data_from_siren(mock, self.siren)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertEqual(body["name"], "LA TURBINE")
        self.assertEqual(body["siren"], self.siren)
        self.assertEqual(body["postalCode"], "59100")
        self.assertEqual(body["city"], "ROUBAIX")
        self.assertEqual(body["cityInseeCode"], "59512")
        self.assertEqual(body["department"], "59")

    @requests_mock.Mocker()
    @authenticate
    def test_check_siren_existing_canteen(self, mock):
        canteen = CanteenFactory(siret=None, siren_unite_legale=self.siren)
        mock_fetch_geo_data_from_siren(mock, self.siren)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertEqual(body["name"], "LA TURBINE")
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(body["canteens"][0]["id"], canteen.id)

    @mock.patch("requests.get", side_effect=requests.exceptions.ConnectTimeout)
    @mock.patch("requests.post", side_effect=requests.exceptions.ConnectTimeout)
    @authenticate
    def test_external_api_down(self, mock_get, mock_post):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertNotIn("name", body)
        self.assertEqual(body["siren"], self.siren)
        self.assertNotIn("postalCode", body)
        self.assertNotIn("city", body)
        self.assertNotIn("cityInseeCode", body)
        self.assertNotIn("department", body)
