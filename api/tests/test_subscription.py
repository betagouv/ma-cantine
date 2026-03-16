from unittest.mock import patch

import requests_mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


@requests_mock.Mocker()
class TestSubscription(APITestCase):
    @patch("api.views.subscription.create_newsletter_contact")
    def test_newsletter_subscription(self, _, create_newsletter_contact):
        """
        When subscribing to the newsletter the email should be sent to Brevo
        """
        self.client.post(
            reverse("subscribe_newsletter"),
            {"email": "test@example.com"},
            format="json",
        )

        create_newsletter_contact.assert_called_once_with("test@example.com")

    @patch("api.views.subscription.create_newsletter_contact")
    def test_newsletter_subscription_email_whitespace(self, _, create_newsletter_contact):
        """
        When subscribing to the newsletter the email should be stripped before being sent to Brevo
        """
        response = self.client.post(
            reverse("subscribe_newsletter"),
            {"email": "  test@example.com      "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        create_newsletter_contact.assert_called_once_with("test@example.com")
