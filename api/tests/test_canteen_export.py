from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.utils import authenticate

from data.factories import CanteenFactory


class CanteenListExportApiTest(APITestCase):
    def test_excel_export_unauthenticated(self):
        response = self.client.get(reverse("user_canteen_list_export"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_excel_export(self):
        CanteenFactory(managers=[authenticate.user])
        CanteenFactory(managers=[authenticate.user])
        CanteenFactory()

        response = self.client.get(reverse("user_canteen_list_export"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @authenticate
    def test_excel_export_only_canteens_with_siret(self):
        CanteenFactory(managers=[authenticate.user], siret=None, siren_unite_legale="123456789")
        CanteenFactory(managers=[authenticate.user])

        response = self.client.get(reverse("user_canteen_list_export"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
