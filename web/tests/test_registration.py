import re
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from data.models import Canteen, Sector
from data.factories import SectorFactory


class TestRegistration(APITestCase):

    def test_user_with_canteen_registration(self):
        """
        Registering a user sends an email to verify their address
        """
        sector = SectorFactory.create()
        email = "test-user@example.com"
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "canteen_name": "Ma Canteen",
            "siret": "TESTING123",
            "management_type": "direct",
            "cgu_approved": True,
            "username": "test-user",
            "department": "69",
            "email": email,
            "city": "Lyon",
            "sectors": [sector.id,],
            "daily_meal_count": 100,
            "postal_code": "123123",
            "city_insee_code": "123123",
            "autocomplete": "Lyon",
        }

        # activation email must be sent after registration
        response = self.client.post(reverse("register"), payload)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Confirmation de votre adresse email - ma cantine"
        )

        # Upon click of the activation link we go directly to the Vue app
        uidb64, token = re.findall(
            r"activation-compte\/(?P<uidb64>.*)\/(?P<token>.*)", mail.outbox[0].body
        )[0]
        activation_response = self.client.get(
            reverse("activate", kwargs={"uidb64": uidb64, "token": token})
        )
        self.assertRedirects(activation_response, reverse("app"), status.HTTP_302_FOUND, fetch_redirect_response=False)


    def test_user_registration_creates_canteen(self):
        """
        Creating a user from the register form should create
        a canteen for them
        """
        sector = SectorFactory.create()
        email = "test-user-2@example.com"
        payload = {
            "first_name": "Test",
            "last_name": "User 2",
            "password1": "testPw1234#!",
            "password2": "testPw1234#!",
            "canteen_name": "Ma Canteen Test",
            "siret": "TESTING123",
            "management_type": "direct",
            "cgu_approved": True,
            "username": "test-user-2",
            "email": email,
            "department": "69",
            "city": "Lyon",
            "sectors": [sector.id,],
            "daily_meal_count": 100,
            "postal_code": "123123",
            "city_insee_code": "123123",
            "autocomplete": "Lyon",
        }

        self.client.post(reverse("register"), payload)

        canteen = Canteen.objects.get(name="Ma Canteen Test")
        user = get_user_model().objects.get(username="test-user-2")

        self.assertIn(user, canteen.managers.all())
        self.assertIn(sector, canteen.sectors.all())

        self.assertEqual(canteen.daily_meal_count, 100)
        self.assertEqual(canteen.city, "Lyon")
        self.assertEqual(canteen.department, "69")

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
            "postal_code": "123123",
            "city_insee_code": "123123",
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
        response = self.client.post(reverse("register_user"), payload)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Confirmation de votre adresse email - ma cantine"
        )

        # Upon click of the activation link we go directly to the Vue app
        uidb64, token = re.findall(
            r"activation-compte\/(?P<uidb64>.*)\/(?P<token>.*)", mail.outbox[0].body
        )[0]
        activation_response = self.client.get(
            reverse("activate", kwargs={"uidb64": uidb64, "token": token})
        )
        self.assertRedirects(activation_response, reverse("app"), status.HTTP_302_FOUND, fetch_redirect_response=False)
