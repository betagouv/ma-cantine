import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate


class TestInitialDataApi(APITestCase):
    def test_unauthenticated_initial_data(self):
        response = self.client.get(reverse("initial_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertIn("loggedUser", body)

    @authenticate
    def test_authenticated_logged_initial_data(self):
        response = self.client.get(reverse("initial_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertIn("loggedUser", body)
