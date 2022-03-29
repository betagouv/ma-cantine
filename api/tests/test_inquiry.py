from django.urls import reverse
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.core import mail
from data.factories.canteen import CanteenFactory
from data.factories.user import UserFactory
from .utils import authenticate


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


class TestEmail(APITestCase):
    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="from@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(HOSTNAME="mysite.com")
    @override_settings(SECURE="True")
    def test_send_message(self):
        canteen = CanteenFactory.create(siret="76494221950672", name="Hugo")
        canteen.managers.add(UserFactory.create(email="mgmt1@example.com"))
        canteen.managers.add(UserFactory.create(email="mgmt2@example.com"))

        payload = {
            "email": "test@example.com",
            "name": "My name",
            "message": "Please add me to the team",
            "url": f"/team/{canteen.id}/",
        }
        response = self.client.post(reverse("canteen_team_request", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        # this canteen has min 2 managers (the factory may have added a random amount more)
        self.assertGreaterEqual(len(email.to), 2)
        self.assertIn("mgmt1@example.com", email.to)
        self.assertIn("mgmt2@example.com", email.to)
        self.assertEqual(email.cc[0], "contact@example.com")
        self.assertIn("Please add me to the team", email.body)
        self.assertIn("76494221950672", email.body)
        self.assertIn("Hugo", email.body)
        self.assertIn("https://mysite.com/team/1/", email.body)
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")
        self.assertEqual(email.from_email, "from@example.com")
