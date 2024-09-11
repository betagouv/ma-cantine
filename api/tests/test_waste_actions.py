from rest_framework.test import APITestCase
from django.urls import reverse
from data.factories.wasteaction import WasteActionFactory


class TestWasteActionsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        WasteActionFactory.create()

    def test_get_waste_actions(self):
        response = self.client.get(reverse("waste_actions"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
