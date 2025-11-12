from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import SectorM2MFactory


class TestSectorApi(APITestCase):
    def test_get_sectors(self):
        """
        The API should return all sectors
        """
        SectorM2MFactory.create()
        SectorM2MFactory.create()
        SectorM2MFactory.create()

        response = self.client.get(reverse("sectors_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
