from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CanteenTeamRequestInquiryTest(APITestCase):
    @override_settings(CONTACT_EMAIL="contact@example.com")
    def test_inquiry(self):
        """
        Test that an inquiry about functionality sends an email to admins
        """
        payload = {
            "from": "test@example.com",
            "inquiryType": "fonctionnalité",
            "message": "I need help with the functionality of the app.",
            "name": "Tester",
            "username": None,
            "siret_or_siren": "12345",
            "meta": {
                "userId": "123456789",
                "userAgent": "Mozilla",
            },
        }
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title = "Demande de support de test@example.com - fonctionnalité"

        # email is sent to admins
        email = mail.outbox[0]
        self.assertEqual(email.to[0], "contact@example.com")
        self.assertEqual(email.subject, title)
        self.assertIn("test@example.com", email.reply_to)
        self.assertIn(payload["name"], email.body)
        self.assertIn(payload["siret_or_siren"], email.body)
        self.assertIn(payload["message"], email.body)
        self.assertIn(payload["meta"]["userId"], email.body)
        self.assertIn(payload["meta"]["userAgent"], email.body)
        self.assertIn("Non renseigné", email.body)

    @override_settings(ENVIRONMENT="demo")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    def test_inquiry_environment_prepend(self):
        """
        Test that the environment is prepended when we are in "demo" or "staging" mode
        """
        payload = {
            "from": "test@example.com",
            "inquiryType": "fonctionnalité",
            "message": "I need help with the functionality of the app\nHow do I do something?",
            "meta": {
                "userId": "123456789",
                "userAgent": "Mozilla",
            },
        }
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        title = "(DEMO) Demande de support de test@example.com - fonctionnalité"

        # email is sent to admins
        email = mail.outbox[0]
        self.assertEqual(email.to[0], "contact@example.com")
        self.assertEqual(email.subject, title)

    def test_inquiry_missing_fields(self):
        """
        Test that a 400 error response with details is returned when the requests is missing fields
        """
        payload = {
            "inquiryType": "fonctionnalité",
            "message": "I need help with the functionality of the app\nHow do I do something?",
            "name": "Tester",
        }
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body.get("from"), "Merci d'indiquer une adresse email")
        self.assertEqual(len(mail.outbox), 0)

        payload = {}
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body.get("from"), "Merci d'indiquer une adresse email")
        self.assertEqual(body.get("message"), "Message manquant dans la requête")
        self.assertEqual(len(mail.outbox), 0)
