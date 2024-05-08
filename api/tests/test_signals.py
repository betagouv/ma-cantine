from django.urls import reverse
from rest_framework.test import APITestCase
from data.factories import DiagnosticFactory
from data.models import AuthenticationMethodHistoricalRecords
from django.test.utils import override_settings
from .utils import authenticate
from freezegun import freeze_time


class TestSignals(APITestCase):
    @override_settings(HOSTNAME="ma-cantine.example.org")
    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2021-01-20")
    @authenticate
    def test_authentication_method_created_with_api(self):
        """
        Teledeclarations created via a third party API should save the corresponding authentication method
        """
        diagnostic = DiagnosticFactory.create(year=2020)
        diagnostic.canteen.managers.add(authenticate.user)
        payload = {"diagnosticId": diagnostic.id}

        self.client.credentials(HTTP_HOST="third-party")
        self.client.post(reverse("teledeclaration_create"), payload)

        diagnostic.refresh_from_db()
        td = diagnostic.teledeclaration_set.first()
        self.assertEqual(
            td.history.first().authentication_method, AuthenticationMethodHistoricalRecords.AuthMethodChoices.API
        )

    @override_settings(HOSTNAME="ma-cantine.example.org")
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

        self.client.credentials(HTTP_HOST="ma-cantine.example.org")
        self.client.post(reverse("teledeclaration_create"), payload)

        diagnostic.refresh_from_db()
        td = diagnostic.teledeclaration_set.first()
        self.assertEqual(
            td.history.first().authentication_method, AuthenticationMethodHistoricalRecords.AuthMethodChoices.WEBSITE
        )
