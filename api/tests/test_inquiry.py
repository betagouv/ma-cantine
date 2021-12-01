from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch


class TestInquiry(APITestCase):
    @patch("common.utils.create_trello_card")
    def test_inquiry(self, mock_create_trello_card):
        """
        Test that an inquiry about functionality hits trello endpoint
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
        card_title = "test@example.com - fonctionnalité"
        card_body = "Message\n---\nI need help with the functionality of the app\nHow do I do something?\nDétailles\n---\nAdresse : test@example.com\nuser_id : 123456789\nuser_agent : Mozilla"

        mock_create_trello_card.assert_called_with(card_title, card_body)
        # TODO: do we want to give the user a reciept? For peace of mind.
