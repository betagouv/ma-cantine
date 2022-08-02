import re
from unittest.mock import MagicMock
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests_mock
import sib_api_v3_sdk


@requests_mock.Mocker()
class TestSubscription(APITestCase):
    def test_beta_tester_existing_user(self, mocker):
        """
        When subscribing for becoming a beta tester the information should be sent
        to Pipedrive. No new user is created if the email is already in Pipedrive
        """
        payload = {
            "name": "Test User",
            "city": "Ma ville",
            "email": "tester@example.com",
            "phone": "099330033",
        }

        # Search person API response
        search_person_matcher = mocker.get(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons/search"),
            json={"success": True, "data": {"items": [{"item": {"id": "1"}}]}},
        )

        # Create person API response
        create_person_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons"),
            json={"success": True, "data": {"id": 1}},
        )

        # Create card API response
        create_card_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/deals"),
            json={"success": True},
        )

        response = self.client.post(reverse("subscribe_beta_tester"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(search_person_matcher.called_once)
        self.assertFalse(create_person_matcher.called)
        self.assertTrue(create_card_matcher.called_once)

    def test_beta_tester_create_person(self, mocker):
        """
        A Pipedrive user is created if it doesn't already exist
        """
        payload = {
            "name": "Test User",
            "city": "Ma ville",
            "email": "tester@example.com",
            "phone": "099330033",
        }

        # Search person API response
        search_person_matcher = mocker.get(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons/search"),
            json={"success": True, "data": {"items": []}},
        )

        # Create person API response
        create_person_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons"),
            json={"success": True, "data": {"id": 1}},
        )

        # Create card API response
        create_card_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/deals"),
            json={"success": True},
        )

        response = self.client.post(reverse("subscribe_beta_tester"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(search_person_matcher.called_once)
        self.assertTrue(create_person_matcher.called_once)
        self.assertTrue(create_card_matcher.called_once)

    def test_beta_tester_create_note(self, mocker):
        """
        A Pipedrive note must be created if a message is specified
        """
        payload = {
            "name": "Test User",
            "city": "Ma ville",
            "email": "tester@example.com",
            "phone": "099330033",
            "message": "Hello !",
        }

        # Search person API response
        search_person_matcher = mocker.get(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons/search"),
            json={"success": True, "data": {"items": []}},
        )

        # Create person API response
        create_person_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons"),
            json={"success": True, "data": {"id": 1}},
        )

        # Create card API response
        create_card_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/deals"),
            json={"success": True, "data": {"id": 1}},
        )

        # Create note matcher
        create_note_matcher = mocker.post(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/notes"),
            json={"success": True, "data": {"id": 1}},
        )

        response = self.client.post(reverse("subscribe_beta_tester"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(search_person_matcher.called_once)
        self.assertTrue(create_person_matcher.called_once)
        self.assertTrue(create_card_matcher.called_once)
        self.assertTrue(create_note_matcher.called_once)

    def test_beta_tester_subscription_missing_email(self, _):
        """
        When subscribing for becoming a beta tester an email
        must be included in the payload.
        """
        payload = {
            "name": "Ma cantine",
            "city": "Ma ville",
            "phone": "099330033",
            "message": "Hello world",
        }
        response = self.client.post(reverse("subscribe_beta_tester"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pipedrive_error(self, mocker):
        """
        A Pipedrive API error returns a 502 response
        """
        payload = {
            "name": "Test User",
            "city": "Ma ville",
            "email": "tester@example.com",
            "phone": "099330033",
        }

        # Search person API response
        search_person_matcher = mocker.get(
            re.compile(r"companydomain\.pipedrive\.com/api/v1/persons/search"),
            json={"success": False},
        )

        response = self.client.post(reverse("subscribe_beta_tester"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertTrue(search_person_matcher.called_once)

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
