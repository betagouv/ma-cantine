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
        self.assertEqual(len(mail.outbox[0].to), canteen.managers.all().count())
        self.assertEqual(mail.outbox[0].from_email, "contact@example.com")
        self.assertIn("test@example.com", mail.outbox[0].body)
        self.assertIn("Camille Dupont", mail.outbox[0].body)
        self.assertIn("Test &lt;b&gt;message&lt;/b&gt;", mail.outbox[0].body)

    @override_settings(DEFAULT_FROM_EMAIL="contact@example.com")
    def test_contact_canteen(self):
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
        response = self.client.post(reverse("contact_canteen"), payload)

        self.assertIn("Une personne", mail.outbox[0].body)
