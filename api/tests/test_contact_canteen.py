from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory


class TestCanteenContact(APITestCase):
    @override_settings(DEFAULT_FROM_EMAIL="contact@example.com")
    def test_contact_canteen(self):
        """
        An email should be sent to the managing team when the contact endpoint is called
        """
        canteen = CanteenFactory.create()
        payload = {
            "canteenId": canteen.id,
            "from": "test@example.com",
            "name": "Camille Dupont",
            "message": "Test <b>message</b>",
        }
        response = self.client.post(reverse("contact_canteen"), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        # sent to all managers and our team
        self.assertEqual(len(email.to), canteen.managers.all().count() + 1)
        self.assertEqual(email.from_email, "contact@example.com")
        self.assertIn("Camille Dupont", email.body)
        self.assertIn("Test <b>message</b>", email.body)
        self.assertIn("contact@example.com", email.body)
        self.assertEqual(len(email.reply_to), canteen.managers.all().count() + 2)
        self.assertIn("test@example.com", email.reply_to)

    @override_settings(DEFAULT_FROM_EMAIL="contact@example.com")
    def test_anonymous_contact(self):
        """
        If a name isn't given, gracefully handle email text
        """
        canteen = CanteenFactory.create()
        payload = {
            "canteenId": canteen.id,
            "from": "test@example.com",
            "name": "",
            "message": "Test",
        }
        self.client.post(reverse("contact_canteen"), payload)

        self.assertIn("Une personne", mail.outbox[0].body)
