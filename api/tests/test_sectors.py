from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SectorApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("sectors_list")

    def test_sector_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 26)
