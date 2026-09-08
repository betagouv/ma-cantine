from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CanteenMinistriesApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("ministries_list")

    def test_can_list_canteen_ministries(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 19)
