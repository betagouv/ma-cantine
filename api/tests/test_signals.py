from django.test.utils import override_settings
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from data.factories import DiagnosticFactory
from data.models import AuthenticationMethodHistoricalRecords

from .utils import authenticate, get_oauth2_token


class TestSignals(APITestCase):
    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2021-01-20")
    @authenticate
    def test_authentication_method_created_with_website(self):
        """
        Teledeclarations created via the website should save the corresponding authentication method
        """
        diagnostic = DiagnosticFactory.create(year=2020)
        diagnostic.canteen.managers.add(authenticate.user)
        payload = {"diagnosticId": diagnostic.id}

        self.client.post(reverse("teledeclaration_create"), payload)

        diagnostic.refresh_from_db()
        td = diagnostic.teledeclaration_set.first()
        self.assertEqual(
            td.history.first().authentication_method, AuthenticationMethodHistoricalRecords.AuthMethodChoices.WEBSITE
        )

    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2021-01-20")
    def test_authentication_method_created_with_api(self):
        """
        Teledeclarations created via a third party API should save the corresponding authentication method
        """
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory.create(year=2020)
        diagnostic.canteen.managers.add(user)
        payload = {"diagnosticId": diagnostic.id}

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.client.post(reverse("teledeclaration_create"), payload)

        diagnostic.refresh_from_db()
        td = diagnostic.teledeclaration_set.first()
        self.assertEqual(
            td.history.first().authentication_method, AuthenticationMethodHistoricalRecords.AuthMethodChoices.API
        )
