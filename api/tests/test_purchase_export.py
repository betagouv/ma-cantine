from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.utils import authenticate

from data.factories import PurchaseFactory, CanteenFactory
from data.models import Purchase


class PurchaseListExportApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        PurchaseFactory(
            canteen=cls.canteen,
            description="avoine",
            famille_produits=Purchase.Family.PRODUITS_DE_LA_MER,
            caracteristiques=[],
            prix_ht=Decimal("12.34"),
        )
        PurchaseFactory(
            canteen=cls.canteen,
            description="tomates",
            famille_produits=Purchase.Family.PRODUITS_DE_LA_MER,
            caracteristiques=[],
        )
        PurchaseFactory(
            canteen=cls.canteen, description="pommes", famille_produits=Purchase.Family.AUTRES, caracteristiques=[]
        )
        cls.url = reverse("purchase_list_export")

    def test_excel_export_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_excel_export(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        purchase_avoine = next((p for p in response.data if p["description"] == "avoine"), None)
        self.assertEqual(purchase_avoine["canteen"], self.canteen.name)
        self.assertEqual(purchase_avoine["description"], "avoine")
        self.assertEqual(purchase_avoine["famille_produits_display"], Purchase.Family.PRODUITS_DE_LA_MER.label)
        self.assertEqual(purchase_avoine["caracteristiques_display"], "")
        self.assertEqual(purchase_avoine["prix_ht"], Decimal("12.34"))

    @authenticate
    def test_excel_export_search(self):
        self.canteen.managers.add(authenticate.user)
        search_term = "avoine"

        response = self.client.get(f"{self.url}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @authenticate
    def test_excel_export_filter(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?family={Purchase.Family.PRODUITS_DE_LA_MER}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
