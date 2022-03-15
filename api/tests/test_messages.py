from django.urls import reverse
from django.core import mail
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from data.factories import CanteenFactory
from data.models import Message
from .utils import authenticate


@override_settings(CONTACT_EMAIL="contact@example.com")
class TestMessageApi(APITestCase):
    def test_message_creation(self):
        canteen = CanteenFactory.create()
        payload = {
            "destinationCanteen": canteen.id,
            "senderName": "Test tester",
            "senderEmail": "test@example.com",
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }
        response = self.client.post(reverse("message_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = Message.objects.get(destination_canteen=canteen)
        self.assertEqual(message.body, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        self.assertEqual(message.status, Message.Status.PENDING)
        self.assertEqual(message.sender_name, "Test tester")
        self.assertEqual(message.sender_email, "test@example.com")
        self.assertIsNone(message.sent_date)
        self.assertEqual(message.destination_canteen, canteen)

        # email is sent to admins
        email = mail.outbox[0]
        self.assertEqual(email.to[0], "contact@example.com")
        self.assertEqual(email.subject, "📨 Nouveau message en attente de validation")

    @authenticate
    def test_message_creation_authenticated(self):
        canteen = CanteenFactory.create()
        payload = {
            "destinationCanteen": canteen.id,
            "senderEmail": "test@example.com",
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }
        response = self.client.post(reverse("message_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_email(self):
        canteen = CanteenFactory.create()
        payload = {
            "destinationCanteen": canteen.id,
            "senderEmail": "bademail",
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }
        response = self.client.post(reverse("message_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_body(self):
        canteen = CanteenFactory.create()
        payload = {
            "destinationCanteen": canteen.id,
            "senderEmail": "test@example.com",
        }
        response = self.client.post(reverse("message_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_email(self):
        canteen = CanteenFactory.create()
        payload = {
            "destinationCanteen": canteen.id,
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        }
        response = self.client.post(reverse("message_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)
