from unittest.mock import MagicMock
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import requests_mock
import sib_api_v3_sdk


@requests_mock.Mocker()
class TestSubscription(APITestCase):
    @override_settings(NEWSLETTER_SENDINBLUE_LIST_ID="1")
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_newsletter_subscription(self, _):
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

    @override_settings(NEWSLETTER_SENDINBLUE_LIST_ID="1")
    @override_settings(ANYMAIL={"SENDINBLUE_API_KEY": "fake-api-key"})
    def test_email_whitespace(self, _):
        """
        When subscribing to the newsletter the email should be stripped
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

        response = self.client.post(
            reverse("subscribe_newsletter"),
            {"email": "  test@example.com      "},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
