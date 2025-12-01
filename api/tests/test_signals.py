from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import DiagnosticFactory
from data.models import AuthenticationMethodHistoricalRecords


@freeze_time("2022-08-30")  # during the 2021 campaign
class TestSignals(APITestCase):
    @authenticate
    def test_authentication_method_created_with_website(self):
        """
        Teledeclarations created via the website should save the corresponding authentication method
        """
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        payload = {"diagnosticId": diagnostic.id}

        self.client.post(reverse("teledeclaration_create"), payload)

        diagnostic.refresh_from_db()
        td = diagnostic.teledeclaration_set.first()
        self.assertEqual(
            td.history.first().authentication_method, AuthenticationMethodHistoricalRecords.AuthMethodChoices.WEBSITE
        )

    def test_td_creation_api_blocked_for_third_party(self):
        """
        Teledeclarations cannot be created via a third party API
        """
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(user)

        payload = {"diagnosticId": diagnostic.id}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, 403)

        diagnostic.refresh_from_db()
        td = diagnostic.teledeclaration_set.all()
        self.assertEqual(len(td), 0)
