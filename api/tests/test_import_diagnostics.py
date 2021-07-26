from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.models import Diagnostic, Canteen
from data.factories import SectorFactory


class TestImportDiagnosticsAPI(APITestCase):
    def test_unauthenticated_import_call(self):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_diagnostics"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        canteen = Canteen.objects.get(siret="0000001234")
        self.assertEqual(canteen.postal_code, "17000")
        self.assertEqual(canteen.daily_meal_count, 700)
        self.assertEqual(canteen.production_type, "site")
        self.assertEqual(canteen.management_type, "conceded")
        diagnostic = Diagnostic.objects.get(canteen_id=canteen.id)
        self.assertEqual(diagnostic.year, 2020)
        self.assertEqual(diagnostic.value_total_ht, 1000)
        self.assertEqual(diagnostic.value_bio_ht, 500)
        self.assertEqual(diagnostic.value_sustainable_ht, Decimal("100.1"))
        self.assertEqual(diagnostic.value_fair_trade_ht, Decimal("200.2"))

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
    def test_valid_sectors_parsed(self):
        """
        File can specify 0+ sectors to add to the canteen
        """
        SectorFactory.create(name="Social et Médico-social (ESMS)")
        SectorFactory.create(name="Crèche")
        SectorFactory.create(name="Scolaire")
        with open("./api/tests/files/diagnostics_sectors.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="0000001234")
        self.assertEqual(canteen.sectors.count(), 3)

    @authenticate
    def test_invalid_sectors_raise_error(self):
        """
        If file specifies invalid sector, error is raised for that line
        """
        SectorFactory.create(name="Social et Médico-social (ESMS)")
        with open("./api/tests/files/diagnostics_sectors.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        body = response.json()
        self.assertEqual(body["errors"][0]["status"], 400)
        self.assertEqual(
            body["errors"][0]["message"], "Sector matching query does not exist."
        )

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

    # TODO: Limit file upload size
