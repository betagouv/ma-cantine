import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import SectorFactory
from .utils import authenticate


class TestInitialDataApi(APITestCase):
    def test_unauthenticated_initial_data(self):
        """
        The initial data request must contain data that is individually managed
        by other views. If the call isn't authenticated, "loggedUser" should be None
        """
        sector = SectorFactory.create()

        response = self.client.get(reverse("initial_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertIn("loggedUser", body)
        self.assertIsNone(body["loggedUser"])

        self.assertIn("sectors", body)
        self.assertEqual(len(body["sectors"]), 1)
        self.assertEqual(body["sectors"][0]["name"], sector.name)

        self.assertIn("partnerTypes", body)
        self.assertIn("communityEvents", body)
        self.assertIn("videoTutorials", body)

    @authenticate
    def test_authenticated_logged_initial_data(self):
        """
        Same endpoint, this time with data in the "loggedUser" property. Not needed
        to thoroughly test the other keys, just making sure they are present.
        """
        response = self.client.get(reverse("initial_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertIn("loggedUser", body)
        self.assertEqual(body["loggedUser"]["id"], authenticate.user.id)
        self.assertEqual(body["loggedUser"]["email"], authenticate.user.email)
        self.assertEqual(body["loggedUser"]["username"], authenticate.user.username)
        self.assertIn("sectors", body)
        self.assertIn("partnerTypes", body)
        self.assertIn("communityEvents", body)
        self.assertIn("videoTutorials", body)
