from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from web.views import OIDCAuthorizeView


class MonComptePropGetOrCreateUserTest(APITestCase):
    def test_creates_user_despite_special_chars_in_family_name(self):
        mcp_data = {
            "sub": "12345",
            "email": "test@example.com",
            "given_name": "Jean",
            "family_name": "D'Angelo De La Crüz",
            "phone_number": "0600000000",
            "organizations": [],
        }
        user = OIDCAuthorizeView.get_or_create_user(mcp_data)
        user.full_clean(exclude=["password"])  # should not raise
        self.assertTrue(get_user_model().objects.filter(pk=user.pk).exists())
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.last_name, "D'Angelo De La Crüz")
