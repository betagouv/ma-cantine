import re

from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from web.forms import RegisterUserForm


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
            "is_dev": False,
        }
        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "username",
            "Vous ne pouvez pas utiliser une adresse email comme nom d'utilisateur.",
            msg_prefix="tester@example.com",
        )

    @override_settings(HOSTNAME="ma-cantine.example.org")
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
            "phone_number": "00-11-22 33 44",
            "cgu_approved": True,
            "username": "test-user",
            "email": email,
            "is_dev": False,
        }

        # activation email must be sent after registration
        self.client.post(reverse("register"), payload)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Confirmation de votre adresse email - ma cantine")

        # Check that the email contains the token
        content = mail.outbox[0].body
        # the link sometimes gets broken in the middle of the token that has a hyphen, avoid this by replacing the line break
        no_line_break = content.replace("-\n", "-")
        matches = re.findall(r"compte\/(?P<uidb64>.*)\/(?P<token>.*)", no_line_break)
        self.assertEqual(len(matches), 1)
        uidb64, token = matches[0]
        activation_response = self.client.get(reverse("activate", kwargs={"uidb64": uidb64, "token": token}))

        redirect_error_message = f"\nEmail body:\n{no_line_break}" + f"\n\nUIDB64: {uidb64}\n\nTOKEN: {token}"
        self.assertRedirects(
            activation_response,
            reverse("app"),
            status.HTTP_302_FOUND,
            fetch_redirect_response=False,
            msg_prefix=redirect_error_message,
        )

    def test_phone_number_validation(self):
        """
        Phone number should be a ten-digit numeric string when ignoring spaces and dashes
        """
        email = "test-phone@example.com"
        payload = {
            "first_name": "Test",
            "last_name": "User Phone",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": True,
            "username": "test-user",
            "phone_number": "123",
            "email": email,
            "is_dev": False,
        }

        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "phone_number",
            "Dix chiffres numériques attendus",
            msg_prefix="test-phone",
        )
