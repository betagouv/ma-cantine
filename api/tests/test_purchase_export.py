from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.utils import authenticate

from data.factories import PurchaseFactory, CanteenFactory
from data.models import Purchase


class PurchaseListExportApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("purchase_list_export")

    def test_excel_export_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_excel_export(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(description="avoine", canteen=canteen)
        PurchaseFactory(description="tomates", canteen=canteen)
        PurchaseFactory(description="pommes", canteen=canteen)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    @authenticate
    def test_excel_export_search(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(description="avoine", canteen=canteen)
        PurchaseFactory(description="tomates", canteen=canteen)
        PurchaseFactory(description="pommes", canteen=canteen)

        search_term = "avoine"
        response = self.client.get(f"{self.url}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @authenticate
    def test_excel_export_filter(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(family=Purchase.Family.PRODUITS_DE_LA_MER, description="avoine", canteen=canteen)
        PurchaseFactory(family=Purchase.Family.PRODUITS_DE_LA_MER, description="tomates", canteen=canteen)
        PurchaseFactory(family=Purchase.Family.AUTRES, description="pommes", canteen=canteen)

        response = self.client.get(f"{self.url}?family=PRODUITS_DE_LA_MER")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
