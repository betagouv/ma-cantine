from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CanteenMinistriesApiTest(APITestCase):
    def test_canteen_ministries_list(self):
        """
        The API should return all canteen ministries
        """
        response = self.client.get(reverse("ministries_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 19)
