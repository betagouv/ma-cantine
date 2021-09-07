from unittest.mock import MagicMock
from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import sib_api_v3_sdk


class TestSubscription(APITestCase):
    @override_settings(CONTACT_EMAIL="contact-test@example.com")
    @override_settings(DEFAULT_FROM_EMAIL="contact-test@example.com")
    def test_beta_tester_subscription(self):
        """
        When subscribing for becoming a beta tester an email
        should be sent to the contact address with the tester's
        data.
        """
        payload = {
            "school": "Ma cantine",
            "city": "Ma ville",
            "email": "tester@exaple.com",
            "phone": "099330033",
            "message": "Hello world",
        }

        response = self.client.post(
            reverse("subscribe_beta_tester"), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "contact-test@example.com")
        self.assertEqual(mail.outbox[0].from_email, "contact-test@example.com")

    def test_beta_tester_subscription_missing_email(self):
        """
        When subscribing for becoming a beta tester an email
        must be included in the payload.
        """
        payload = {
            "measures": {},
            "school": "Ma cantine",
            "city": "Ma ville",
            "phone": "099330033",
            "message": "Hello world",
        }
        response = self.client.post(
            reverse("subscribe_beta_tester"), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_beta_tester_diagnostic_data(self):
        """
        When subscribing for becoming a beta tester an email
        the diagnostic data must be in the email
        """
        payload = {
            "measures": {
                "valueBioHt": 1000,
                "vegetarianMenuType": "UNIQUE",
            },
            "email": "me@example.com",
            "school": "Ma cantine",
            "city": "Ma ville",
            "phone": "099330033",
            "message": "Hello world",
        }
        response = self.client.post(
            reverse("subscribe_beta_tester"), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertIn("Bio - Valeur annuelle HT : 1000 €", email.body)
        self.assertIn(
            "Menu végétarien proposé : Un menu végétarien en plat unique", email.body
        )

    @override_settings(NEWSLETTER_SENDINBLUE_LIST_ID="1")
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_newsletter_subscription(self):
        """
        When subscribing to the newsletter, the SIB library should
        be called with the adequate parameters
        """

        class FakeSIBConfiguration:
            api_key = {}

        class FakeContactCreate:
            list_ids = None
            update_enabled = None

        class FakeSIBInstanceAPI:
            create_contact = MagicMock()

        fake_sib_configuration = FakeSIBConfiguration()
        fake_contact_create = FakeContactCreate()
        fake_sib_api_instance = FakeSIBInstanceAPI()

        sib_api_v3_sdk.Configuration = MagicMock(return_value=fake_sib_configuration)
        sib_api_v3_sdk.ApiClient = MagicMock()
        sib_api_v3_sdk.ContactsApi = MagicMock(return_value=fake_sib_api_instance)
        sib_api_v3_sdk.CreateContact = MagicMock(return_value=fake_contact_create)

        self.client.post(
            reverse("subscribe_newsletter"),
            {"email": "test@example.com"},
            format="json",
        )

        # SIB API was configured correctly
        sib_api_v3_sdk.Configuration.assert_called()
        self.assertEqual(fake_sib_configuration.api_key["api-key"], "fake-api-key")

        # SIB API client was instantiated
        sib_api_v3_sdk.ApiClient.assert_called_with(fake_sib_configuration)

        # SIB create_contact was setup correctly
        sib_api_v3_sdk.CreateContact.assert_called_with(email="test@example.com")
        self.assertEqual(fake_contact_create.list_ids, [1])
        self.assertEqual(fake_contact_create.update_enabled, True)

        # SIB API was called correctly
        sib_api_v3_sdk.ContactsApi.assert_called_once()
        fake_sib_api_instance.create_contact.assert_called_with(fake_contact_create)
