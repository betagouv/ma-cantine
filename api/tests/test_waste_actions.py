from rest_framework.test import APITestCase
from django.urls import reverse
from data.factories.wasteaction import WasteActionFactory


class TestWasteActionsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory.create()

    def test_get_waste_actions_list(self):
        response = self.client.get(reverse("waste_actions_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_waste_action_detail(self):
        response = self.client.get(reverse("waste_action_detail", kwargs={"pk": self.waste_action.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.waste_action.id)
