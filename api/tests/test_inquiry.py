from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories.canteen import CanteenFactory
from data.factories.user import UserFactory


class TestInquiry(APITestCase):
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


class TestEmail(APITestCase):
    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(HOSTNAME="mysite.com")
    @override_settings(SECURE="True")
    def test_send_message(self):
        canteen = CanteenFactory.create(
            siret="76494221950672",
            name="Hugo",
            managers=[
                UserFactory.create(email="mgmt1@example.com"),
                UserFactory.create(email="mgmt2@example.com"),
            ],
        )

        payload = {
            "email": "test@example.com",
            "name": "My name",
            "message": "Please add me to the team",
        }
        response = self.client.post(reverse("canteen_team_request", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(len(email.to), 2)
        self.assertIn("mgmt1@example.com", email.to)
        self.assertIn("mgmt2@example.com", email.to)
        self.assertIn("Please add me to the team", email.body)
        self.assertIn("76494221950672", email.body)
        self.assertIn("Hugo", email.body)
        self.assertIn(
            f"https://mysite.com/modifier-ma-cantine/{canteen.id}--\nHugo/gestionnaires?email=test@example.com",
            email.body,
        )
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")
        self.assertEqual(email.from_email, "no-reply@example.com")

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(HOSTNAME="mysite.com")
    @override_settings(SECURE="True")
    def test_send_message_no_managers(self):
        canteen = CanteenFactory.create(siret="76494221950672", name="Hugo")
        canteen.managers.clear()

        payload = {
            "email": "test@example.com",
            "name": "My name",
            "message": "Please add me to the team",
        }
        response = self.client.post(reverse("canteen_team_request", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(len(email.to), 1)
        self.assertIn("contact@example.com", email.to)
        self.assertIn("Please add me to the team", email.body)
        self.assertIn("76494221950672", email.body)
        self.assertIn("Hugo", email.body)
        self.assertIn(
            f"https://mysite.com/modifier-ma-cantine/{canteen.id}--\nHugo/gestionnaires?email=test@example.com",
            email.body,
        )
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")
        self.assertEqual(email.from_email, "no-reply@example.com")
