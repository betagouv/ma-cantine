import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import UserFactory
from .utils import authenticate, get_oauth2_token


class TestLoggedUserApi(APITestCase):
    def test_unauthenticated_logged_user_call(self):
        """
        When calling this API unathenticated we expect a 204
        """
        response = self.client.get(reverse("logged_user"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wrong_scope_user_info_call(self):
        _, token = get_oauth2_token("canteen:read")
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_info"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_scope_logged_user_call(self):
        _, token = get_oauth2_token("user:read")
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_info"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_authenticated_logged_user_call(self):
        """
        When calling this API athenticated we expect to get a
        JSON representation of the authenticated user
        """
        response = self.client.get(reverse("logged_user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertEqual(body.get("username"), authenticate.user.username)
        self.assertEqual(body.get("email"), authenticate.user.email)
        self.assertEqual(body.get("firstName"), authenticate.user.first_name)
        self.assertEqual(body.get("lastName"), authenticate.user.last_name)
        self.assertIn("id", body)

    @authenticate
    def test_authenticated_user_info_call(self):
        response = self.client.get(reverse("user_info"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertEqual(body.get("username"), authenticate.user.username)
        self.assertEqual(body.get("firstName"), authenticate.user.first_name)
        self.assertEqual(body.get("lastName"), authenticate.user.last_name)

    def test_username_generation(self):
        response = self.client.post(reverse("username_suggestion"), {"first_name": "Anne", "last_name": "Iversaire"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn("suggestion", body)
        self.assertEqual(body["suggestion"], "anne_iversaire")

    def test_username_generation_with_spaces(self):
        response = self.client.post(
            reverse("username_suggestion"), {"first_name": " Omar Khe ", "last_name": "   Ting"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn("suggestion", body)
        self.assertEqual(body["suggestion"], "omar-khe_ting")

    def test_username_generation_with_accents(self):
        response = self.client.post(reverse("username_suggestion"), {"first_name": "Oscar", "last_name": "Abé"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn("suggestion", body)
        self.assertEqual(body["suggestion"], "oscar_abe")

    def test_with_email(self):
        response = self.client.post(reverse("username_suggestion"), {"email": "tester_12@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn("suggestion", body)
        self.assertEqual(body["suggestion"], "tester_12")

    def test_random_number(self):
        UserFactory.create(username="anne_iversaire")
        response = self.client.post(reverse("username_suggestion"), {"first_name": "Anne", "last_name": "Iversaire"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = json.loads(response.content.decode())
        self.assertIn("suggestion", body)
        self.assertTrue(body["suggestion"].startswith("anne_iversaire_"))

    @authenticate
    def test_user_job_update(self):
        """
        User can update their job details if logged in
        """
        user = authenticate.user
        self.assertNotEqual(user.job, "OTHER")
        self.assertNotEqual(user.other_job_description, "Magician")
        payload = {
            "job": "OTHER",
            "otherJobDescription": "Magician",
        }
        response = self.client.patch(reverse("update_user", kwargs={"pk": user.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["job"], "OTHER")
        self.assertEqual(body["otherJobDescription"], "Magician")

    @authenticate
    def test_user_source_update(self):
        """
        User can update how they heard of us if logged in
        """
        user = authenticate.user
        self.assertNotEqual(user.source, "OTHER")
        self.assertNotEqual(user.other_source_description, "Narnia")
        payload = {
            "source": "OTHER",
            "otherSourceDescription": "Narnia",
        }
        response = self.client.patch(reverse("update_user", kwargs={"pk": user.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["source"], "OTHER")
        self.assertEqual(body["otherSourceDescription"], "Narnia")

    def test_user_update_wrong_token(self):
        user, token = get_oauth2_token("user:read")
        self.client.credentials(Authorization=f"Bearer {token}")
        payload = {
            "source": "OTHER",
            "otherSourceDescription": "Narnia",
        }
        response = self.client.patch(reverse("update_user", kwargs={"pk": user.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
