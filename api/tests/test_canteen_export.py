from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.utils import authenticate

from data.factories import CanteenFactory


class CanteenListExportApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user_canteen_list_export")

    def test_excel_export_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_excel_export(self):
        CanteenFactory(managers=[authenticate.user])
        CanteenFactory(managers=[authenticate.user])
        CanteenFactory()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
