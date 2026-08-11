from unittest.mock import patch

import requests_mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


@requests_mock.Mocker()
class SubscriptionApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("subscribe_newsletter")

    @patch("api.views.subscription.create_newsletter_contact")
    def test_can_subscribe_newsletter(self, _, create_newsletter_contact):
        payload = {"email": "test@example.com"}
        self.client.post(self.url, payload, format="json")

        create_newsletter_contact.assert_called_once_with("test@example.com")

    @patch("api.views.subscription.create_newsletter_contact")
    def test_can_subscribe_newsletter_with_email_whitespace(self, _, create_newsletter_contact):
        payload = {"email": "  test@example.com      "}
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_newsletter_contact.assert_called_once_with("test@example.com")  # stripped
