from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django_otp.oath import totp
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from django_otp.plugins.otp_totp.models import TOTPDevice

from data.factories import UserFactory

User = get_user_model()


class MaCantineAdminSiteLoginTest(TestCase):
    def setUp(self):
        self.staff_not_superuser_no_otp = UserFactory(
            email="staff@example.com",
            first_name="Staff",
            last_name="User",
            is_staff=True,
            is_superuser=False,
        )
        self.superuser_no_otp = UserFactory(
            email="superuser@example.com",
            first_name="Super",
            last_name="User",
            is_staff=True,
            is_superuser=True,
        )
        self.user_no_staff_not_superuser = UserFactory(
            email="nonstaff@example.com",
            first_name="Non",
            last_name="Staff",
            is_staff=False,
            is_superuser=False,
        )

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_non_staff_user_cannot_access_admin(self):
        self.client.force_login(self.user_no_staff_not_superuser)
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_staff_non_superuser_without_otp_can_access_admin(self):
        self.client.force_login(self.staff_not_superuser_no_otp)
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)

    def test_superuser_without_otp_redirected_to_login(self):
        self.client.force_login(self.superuser_no_otp)
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    def test_staff_non_superuser_can_login_without_otp(self):
        self.staff_not_superuser_no_otp.set_password("testPw1234#!")
        self.staff_not_superuser_no_otp.save(update_fields=["password"])

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": self.staff_not_superuser_no_otp.username,
                "password": "testPw1234#!",
                "next": reverse("admin:index"),
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/", response.url)

        final_response = self.client.get(response.url)
        self.assertEqual(final_response.status_code, 200)

    def test_staff_user_with_otp_can_access_admin(self):
        # Set user password & device
        self.staff_not_superuser_no_otp.set_password("testPw1234#!")
        self.staff_not_superuser_no_otp.save(update_fields=["password"])
        device = TOTPDevice.objects.create(
            user=self.staff_not_superuser_no_otp,
            name="test",
            confirmed=True,
        )
        totp_code = totp(device.bin_key, device.step, device.t0)

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": self.staff_not_superuser_no_otp.username,
                "password": "testPw1234#!",
                "otp_token": totp_code,
                "next": reverse("admin:index"),
            },
        )

        # Should redirect to admin index
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/", response.url)

        # Follow redirect and check admin loads
        final_response = self.client.get(response.url)
        self.assertEqual(final_response.status_code, 200)

    def test_superuser_with_otp_can_access_admin(self):
        # Set user password & device
        self.superuser_no_otp.set_password("testPw1234#!")
        self.superuser_no_otp.save(update_fields=["password"])
        device = TOTPDevice.objects.create(
            user=self.superuser_no_otp,
            name="test",
            confirmed=True,
        )
        totp_code = totp(device.bin_key, device.step, device.t0)

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": self.superuser_no_otp.username,
                "password": "testPw1234#!",
                "otp_token": totp_code,
                "next": reverse("admin:index"),
            },
        )

        # Should redirect to admin index
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/", response.url)

        # Follow redirect and check admin loads
        final_response = self.client.get(response.url)
        self.assertEqual(final_response.status_code, 200)

    def test_staff_user_with_static_token_can_access_admin(self):
        # Set user password & backup device
        self.staff_not_superuser_no_otp.set_password("testPw1234#!")
        self.staff_not_superuser_no_otp.save(update_fields=["password"])
        device = StaticDevice.objects.create(user=self.staff_not_superuser_no_otp, name="backup", confirmed=True)
        static_token = StaticToken.objects.create(device=device, token="123456")

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": self.staff_not_superuser_no_otp.username,
                "password": "testPw1234#!",
                "otp_token": static_token.token,
                "next": reverse("admin:index"),
            },
        )

        # Should redirect to admin index
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/", response.url)

        # Follow redirect and check admin loads
        final_response = self.client.get(response.url)
        self.assertEqual(final_response.status_code, 200)

    def test_superuser_with_static_token_can_access_admin(self):
        # Set user password & backup device
        self.superuser_no_otp.set_password("testPw1234#!")
        self.superuser_no_otp.save(update_fields=["password"])
        device = StaticDevice.objects.create(user=self.superuser_no_otp, name="backup", confirmed=True)
        static_token = StaticToken.objects.create(device=device, token="123456")

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": self.superuser_no_otp.username,
                "password": "testPw1234#!",
                "otp_token": static_token.token,
                "next": reverse("admin:index"),
            },
        )

        # Should redirect to admin index
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/", response.url)

        # Follow redirect and check admin loads
        final_response = self.client.get(response.url)
        self.assertEqual(final_response.status_code, 200)

    @override_settings(LOGIN_URL="/s-identifier")
    def test_login_url_not_affected_by_global_setting(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        # Should redirect to admin login, not the global LOGIN_URL
        self.assertIn("/admin/login/", response.url)
        self.assertNotIn("/s-identifier", response.url)


class MaCantineAdminSiteCustomUrlsTest(TestCase):
    def setUp(self):
        self.staff_not_superuser_no_otp = UserFactory(
            email="staff@example.com",
            first_name="Staff",
            last_name="User",
            is_staff=True,
            is_superuser=True,
        )
        device = TOTPDevice.objects.create(user=self.staff_not_superuser_no_otp, name="test", confirmed=True)
        self.client.force_login(self.staff_not_superuser_no_otp)
        # Mark the OTP device as verified for this session, as django_otp.login() would
        session = self.client.session
        session["otp_device_id"] = device.persistent_id
        session.save()

    def test_custom_urls_registered_sector(self):
        response = self.client.get("/admin/data/sector-textchoices/")
        self.assertEqual(response.status_code, 200)

    def test_custom_urls_registered_canteen(self):
        response = self.client.get("/admin/data/canteen-canteen-economic-model-textchoices/")
        self.assertEqual(response.status_code, 200)

    def test_synthetic_data_models_in_app_list(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        # Check that synthetic models are present in the response
        self.assertContains(response, "Secteurs ")
        self.assertContains(response, "(TextChoices)")
