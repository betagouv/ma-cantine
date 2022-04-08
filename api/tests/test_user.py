import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate


class TestLoggedUserApi(APITestCase):
    def test_unauthenticated_logged_user_call(self):
        """
        When calling this API unathenticated we expect a 204
        """
        response = self.client.get(reverse("logged_user"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_authenticated_logged_user_call(self):
        """
        When calling this API athenticated we expect to get a
        JSON representation of the authenticated user
        """
        response = self.client.get(reverse("logged_user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertEqual(body.get("username"), authenticate.user.username)
        self.assertEqual(body.get("email"), authenticate.user.email)
        self.assertEqual(body.get("firstName"), authenticate.user.first_name)
        self.assertEqual(body.get("lastName"), authenticate.user.last_name)
        self.assertIn("id", body)
