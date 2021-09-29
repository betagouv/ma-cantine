from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.models import Diagnostic, Canteen
from data.factories import SectorFactory, CanteenFactory


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
        self.assertEqual(body["count"], 2)
        self.assertEqual(body["canteens"][0]["siret"], "21340172201787")
        self.assertEqual(body["canteens"][0]["diagnostics"][0]["year"], 2020)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.first().managers.first().id, authenticate.user.id
        )
        self.assertEqual(Diagnostic.objects.count(), 2)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.postal_code, "17000")
        self.assertEqual(canteen.daily_meal_count, 700)
        self.assertEqual(canteen.production_type, "site")
        self.assertEqual(canteen.management_type, "conceded")
        self.assertEqual(canteen.central_producer_siret, "42126486200010")
        diagnostic = Diagnostic.objects.get(canteen_id=canteen.id)
        self.assertEqual(diagnostic.year, 2020)
        self.assertEqual(diagnostic.value_total_ht, 1000)
        self.assertEqual(diagnostic.value_bio_ht, 500)
        self.assertEqual(diagnostic.value_sustainable_ht, Decimal("100.1"))
        self.assertEqual(diagnostic.value_fair_trade_ht, Decimal("200.2"))
        self.assertIn("seconds", body)

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
        self.assertEqual(body["count"], 2)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.count(), 2)
        canteen = Canteen.objects.get(siret="21340172201787")
        canteen.name = "A cantéen"

    @authenticate
    def test_cannot_modify_existing_canteen_unless_manager(self):
        """
        If a canteen exists, then you should have to already be it's manager to add diagnostics.
        No canteens will be created since any error cancels out the entire file
        """
        CanteenFactory.create(siret="21340172201787")
        my_canteen = CanteenFactory.create(siret="73282932000074")
        my_canteen.managers.add(authenticate.user)

        with open("./api/tests/files/diagnostics_different_canteens.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        error = body["errors"][0]
        self.assertEqual(error["row"], 1)
        self.assertEqual(error["status"], 401)
        self.assertEqual(
            error["message"],
            "Vous n'êtes pas un gestionnaire de cette cantine.",
        )

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
        canteen = Canteen.objects.get(siret="21340172201787")
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
            body["errors"][0]["message"],
            "Le secteur spécifié ne fait pas partie des options acceptées",
        )

    @authenticate
    def test_error_collection(self):
        """
        If errors occur, discard the file and return the errors with row and message
        """
        with open("./api/tests/files/diagnostics_bad_file.csv") as diag_file:
            response = self.client.post(
                reverse("import_diagnostics"), {"file": diag_file}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        errors = body["errors"]
        self.assertEqual(errors[0]["row"], 1)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2022.",
        )
        self.assertEqual(
            errors[1]["message"],
            "Champ 'année' : La valeur «\xa0.\xa0» doit être un nombre entier.",
        )
        self.assertEqual(
            errors[2]["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2022.",
        )
        self.assertEqual(
            errors[3]["message"],
            "La valeur 'not a number' n'est pas valide pour le champ 'repas par jour'.",
        )
        self.assertEqual(
            errors[4]["message"],
            "Champ 'mode de production' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors[5]["message"],
            "Champ 'Valeur totale annuelle HT' : La valeur «\xa0invalid total\xa0» doit être un nombre décimal.",
        )
        self.assertEqual(
            errors[6]["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2022.",
        )
        self.assertEqual(
            errors[7]["message"],
            "Un diagnostic pour cette année et cette cantine existe déjà.",
        )
        self.assertEqual(
            errors[8]["message"],
            "Champ 'Valeur totale annuelle HT' : La somme des valeurs d'approvisionnement, 600, est plus que le total, 20",
        )
        self.assertEqual(
            errors[9]["message"],
            "Champ 'siret' : Le siret de la cantine ne peut pas être vide",
        )
