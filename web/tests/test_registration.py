import re
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# TODO : do we want any tests for rest_registration?
# TODO : check registration not broken for users in real site like these test are
# if it is might have to create a URL with name="login"


class TestRegistration(APITestCase):
    def test_register_email_username(self):
        """
        Username cant be an email address
        """
        payload = {
            "first_name": "Tester",
            "last_name": "Tester",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": True,
            "email": "tester@example.com",
            "username": "tester@example.com",
        }
        response = self.client.post(reverse("register"), payload)
        self.assertFormError(
            response,
            "form",
            "username",
            "Vous ne pouvez pas utiliser une adresse email comme nom d'utilisateur.",
            msg_prefix="tester@example.com",
        )

    def test_user_only_registration(self):
        """
        Registering a user sends an email to verify their address
        """
        email = "test-user@example.com"
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": True,
            "username": "test-user",
            "email": email,
        }

        # activation email must be sent after registration
        self.client.post(reverse("register"), payload)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Confirmation de votre adresse email - ma cantine")

        # Upon click of the activation link we go directly to the Vue app
        matches = re.findall(r"compte\/(?P<uidb64>.*)\/(?P<token>.*)", mail.outbox[0].body)
        self.assertEqual(len(matches), 1)
        uidb64, token = matches[0]
        activation_response = self.client.get(reverse("activate", kwargs={"uidb64": uidb64, "token": token}))
        self.assertRedirects(
            activation_response,
            reverse("app"),
            status.HTTP_302_FOUND,
            fetch_redirect_response=False,
        )
