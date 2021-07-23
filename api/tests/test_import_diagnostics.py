from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.models import Diagnostic, Canteen

# Mock function call which calls API in ../utils/


class TestImportDiagnosticsAPI(APITestCase):
    def test_unauthenticated_import_call(self):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_diagnostics"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_siret_api_called(self):
        """
        When importing a diagnostic, canteen info is fetched from SIRET API
        """
        pass

    @authenticate
    def test_override_possible(self):
        """
        Canteen name can be overridden by provided data
        """
        pass

    @authenticate
    def test_diagnostics_created(self):
        """
        Given valid data, multiple diagnostics are created for multiple canteens,
        the authenticated user is added as the manager,
        and a summary of the results is returned
        """
        with open("./api/tests/files/diagnostics_different_canteens.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["created"]), 2)
        self.assertEqual(body["created"][0]["siret"], "0000001234")
        self.assertEqual(body["created"][0]["year"], "2020")
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.first().managers.first().id, authenticate.user.id
        )
        self.assertEqual(Diagnostic.objects.count(), 2)

    @authenticate
    def test_canteen_info_not_overridden(self):
        """
        If a canteen is present on multiple lines, keep data from first line
        """
        with open("./api/tests/files/diagnostics_same_canteen.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["created"]), 2)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.count(), 2)
        canteen = Canteen.objects.get(siret="0000001234")
        canteen.name = "A cantéen"

    @authenticate
    def test_sectors_parsed(self):
        """
        File can specify 0+ sectors to add to the canteen
        """
        pass

    @authenticate
    def test_invalid_siret(self):
        """
        If siret is invalid, continue data import and return error for line
        """
        pass

    @authenticate
    def test_link_existing_canteen(self):
        """
        If canteen with matching SIRET already exists, use existing canteen for diag
        and don't override data or call SIRET API
        """
        pass

    @authenticate
    def test_error_collection(self):
        """
        If errors occur, skip line, continuing upload, and return errors with row and message
        """
        with open("./api/tests/files/diagnostics_bad_file.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["created"]), 1)
        self.assertEqual(Diagnostic.objects.count(), 1)
        self.assertEqual(body["errors"][0]["row"], 1)
        self.assertEqual(body["errors"][0]["status"], 400)
        self.assertEqual(
            body["errors"][0]["message"], "Field 'year' expected a number but got ''."
        )

    # Test that the function pauses and continues if get a 429 from the API
    # TODO: Limit file upload size
