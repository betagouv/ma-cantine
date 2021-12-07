from django.urls import reverse
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch


@override_settings(TRELLO_LIST_ID_CONTACT="listId")
@patch("common.utils.create_trello_card")
class TestInquiry(APITestCase):
    def test_inquiry(self, mock_create_trello_card):
        """
        Test that an inquiry about functionality hits trello endpoint
        """
        payload = {
            "from": "test@example.com",
            "inquiryType": "functionalityQuestion",
            "message": "I need help with the functionality of the app\nHow do I do something?",
            "name": "Tester",
            "meta": {
                "userId": "123456789",
                "userAgent": "Mozilla",
            },
        }
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card_title = "test@example.com - fonctionnalité"
        card_body = "Nom/Prénom\n---\nTester\nMessage\n---\nI need help with the functionality of the app\nHow do I do something?\nDétails\n---\nAdresse : test@example.com\nuser_id : 123456789\nuser_agent : Mozilla"

        mock_create_trello_card.assert_called_with("listId", card_title, card_body)

    @override_settings(ENVIRONMENT="demo")
    def test_inquiry_environment_prepend(self, mock_create_trello_card):
        """
        Test that the environment is prepended when we are in "demo" or "staging" mode
        """
        payload = {
            "from": "test@example.com",
            "inquiryType": "functionalityQuestion",
            "message": "I need help with the functionality of the app\nHow do I do something?",
            "meta": {
                "userId": "123456789",
                "userAgent": "Mozilla",
            },
        }
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card_title = "(DEMO) test@example.com - fonctionnalité"
        card_body = "Nom/Prénom\n---\nNon renseigné\nMessage\n---\nI need help with the functionality of the app\nHow do I do something?\nDétails\n---\nAdresse : test@example.com\nuser_id : 123456789\nuser_agent : Mozilla"

        mock_create_trello_card.assert_called_with("listId", card_title, card_body)

    def test_missing_fields(self, mock_create_trello_card):
        """
        Test that a 400 error response with details is returned when the requests is missing fields
        """
        payload = {
            "inquiryType": "functionalityQuestion",
            "message": "I need help with the functionality of the app\nHow do I do something?",
            "name": "Tester",
        }
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body.get("from"), "Merci d'indiquer une adresse email")
        mock_create_trello_card.assert_not_called()

        payload = {}
        response = self.client.post(reverse("inquiry"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body.get("from"), "Merci d'indiquer une adresse email")
        self.assertEqual(body.get("message"), "Message manquant dans la requête")
        mock_create_trello_card.assert_not_called()
