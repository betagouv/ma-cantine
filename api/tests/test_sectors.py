from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import SectorFactory


class TestSectorApi(APITestCase):
    def test_get_sectors(self):
        """
        The API should return all sectors
        """
        SectorFactory.create()
        SectorFactory.create()
        SectorFactory.create()

        response = self.client.get(reverse("sectors_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
