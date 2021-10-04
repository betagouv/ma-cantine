from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TestCanteenNotFoundMessage(APITestCase):
    """
    Message sent by the user if they don't find a canteen they are
    looking for in the /nos-cantines page. The form is located at
    the bottom of the page.
    """

    @override_settings(DEFAULT_FROM_EMAIL="from@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    def test_send_message(self):
        payload = {
            "from": "test@example.com",
            "message": "I did not find a canteen I'm looking for",
            "name": "Tester",
        }
        response = self.client.post(reverse("canteen_not_found"), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(len(email.to), 1)
        self.assertEqual(email.to[0], "contact@example.com")
        self.assertIn("I did not find a canteen I'm looking for", email.body)
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")
        self.assertEqual(email.from_email, "from@example.com")

    @override_settings(DEFAULT_FROM_EMAIL="from@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    def test_bad_email(self):
        payload = {
            "from": "Bad email",
            "message": "I did not find a canteen I'm looking for",
            "name": "Tester",
        }
        response = self.client.post(reverse("canteen_not_found"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)
