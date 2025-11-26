from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SectorApiTest(APITestCase):
    def test_sector_list(self):
        """
        The API should return all sectors
        """
        response = self.client.get(reverse("sectors_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 26)
