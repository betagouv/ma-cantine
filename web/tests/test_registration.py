import re

from django.contrib.auth import tokens
from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import UserFactory
from web.forms import RegisterUserForm


class RegistrationTest(APITestCase):
    def test_cannot_register_with_email_yopmail(self):
        payload = {
            "first_name": "Tester",
            "last_name": "Tester",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": True,
            "email": "test@yopmail.com",
            "is_dev": False,
        }
        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "email",
            "Ce nom de domaine email n'est pas autorisé.",
            msg_prefix="test@yopmail.com",
        )

    def test_cannot_register_with_invalid_phone_number(self):
        payload = {
            "first_name": "Test",
            "last_name": "User Phone",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": True,
            "phone_number": "123",  # should be 10 digits
            "email": "test-phone@example.com",
            "is_dev": False,
        }

        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "phone_number",
            "Dix chiffres numériques attendus",
            msg_prefix="test-phone",
        )

    def test_cannot_register_with_duplicate_email(self):
        UserFactory(email="existing@example.com")
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": True,
            "email": "existing@example.com",
            "is_dev": False,
        }
        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "email",
            "Un objet Utilisateur avec ce champ Adresse électronique existe déjà.",
            msg_prefix="existing@example.com",
        )

    def test_cannot_register_with_weak_password(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password1": "short1",
            "password2": "short1",
            "cgu_approved": True,
            "email": "weak-password@example.com",
            "is_dev": False,
        }
        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "password2",
            [
                "Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.",
                "Ce mot de passe est trop courant.",
            ],
            msg_prefix="short1",
        )

    def test_cannot_register_without_accepting_cgu(self):
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "cgu_approved": False,
            "email": "test-cgu@example.com",
            "is_dev": False,
        }
        form = RegisterUserForm(data=payload)
        self.assertFormError(
            form,
            "cgu_approved",
            "Champ requis.",
            msg_prefix="test-cgu@example.com",
        )

    @override_settings(HOSTNAME="ma-cantine.example.org")
    def test_can_register(self):
        """
        Registering a user sends an email to verify their address
        """
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "phone_number": "00-11-22 33 44",
            "cgu_approved": True,
            "email": "test-user@example.com",
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


class AccountActivationViewTest(APITestCase):
    def test_activating_already_confirmed_account_redirects_to_login(self):
        user = UserFactory(email="already-confirmed@example.com", email_confirmed=True)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        response = self.client.get(reverse("activate", kwargs={"uidb64": uidb64, "token": "irrelevant-token"}))

        self.assertRedirects(response, reverse("login"), status.HTTP_302_FOUND, fetch_redirect_response=False)
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    def test_activating_with_invalid_token_redirects_to_invalid_token_page(self):
        user = UserFactory(email="not-yet-confirmed@example.com", email_confirmed=False)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        response = self.client.get(reverse("activate", kwargs={"uidb64": uidb64, "token": "not-a-valid-token"}))

        self.assertRedirects(response, reverse("invalid_token"), status.HTTP_302_FOUND, fetch_redirect_response=False)
        self.assertIsNone(self.client.session.get("_auth_user_id"))
        user.refresh_from_db()
        self.assertFalse(user.email_confirmed)

    def test_activating_with_valid_token_confirms_and_logs_in(self):
        user = UserFactory(email="to-confirm@example.com", email_confirmed=False)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = tokens.default_token_generator.make_token(user)

        response = self.client.get(reverse("activate", kwargs={"uidb64": uidb64, "token": token}))

        self.assertRedirects(response, reverse("app"), status.HTTP_302_FOUND, fetch_redirect_response=False)
        self.assertEqual(self.client.session.get("_auth_user_id"), str(user.id))
        user.refresh_from_db()
        self.assertTrue(user.email_confirmed)


class ActivationTokenViewTest(APITestCase):
    def test_get_resend_activation_email_page(self):
        response = self.client.get(reverse("registration_email"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "auth/register_resend_email.html")

    def test_resending_activation_email_does_not_log_in_as_target_user(self):
        """
        Regression test: posting someone else's email to the "resend activation email"
        endpoint must not authenticate the requester as that user (account takeover).
        """
        victim = UserFactory(email="victim@example.com", email_confirmed=False)

        response = self.client.post(reverse("registration_email"), {"email": victim.email})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsNone(self.client.session.get("_auth_user_id"))

        # the activation email was still sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [victim.email])
