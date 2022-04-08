import os
from decimal import Decimal
import unittest
from django.urls import reverse
from django.test.utils import override_settings
from django.core import mail
from rest_framework.test import APITestCase
from rest_framework import status
from data.models import Diagnostic, Canteen, ManagerInvitation
from data.factories import SectorFactory, CanteenFactory, UserFactory
from data.department_choices import Department
from data.region_choices import Region
import requests
import requests_mock
from .utils import authenticate


@requests_mock.Mocker()
class TestImportDiagnosticsAPI(APITestCase):
    def test_unauthenticated_import_call(self, _):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_diagnostics"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_diagnostics_created(self, _):
        """
        Given valid data, multiple diagnostics are created for multiple canteens,
        the authenticated user is added as the manager,
        and a summary of the results is returned
        """
        with open("./api/tests/files/diagnostics_different_canteens.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        self.assertEqual(body["canteens"][0]["siret"], "21340172201787")
        self.assertEqual(body["canteens"][0]["diagnostics"][0]["year"], 2020)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Canteen.objects.first().managers.first().id, authenticate.user.id)
        self.assertEqual(Diagnostic.objects.count(), 2)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.daily_meal_count, 700)
        self.assertEqual(canteen.production_type, "site")
        self.assertEqual(canteen.management_type, "conceded")
        self.assertEqual(canteen.economic_model, "public")
        self.assertEqual(canteen.central_producer_siret, "42126486200010")
        diagnostic = Diagnostic.objects.get(canteen_id=canteen.id)
        self.assertEqual(diagnostic.year, 2020)
        self.assertEqual(diagnostic.value_total_ht, 1000)
        self.assertEqual(diagnostic.value_bio_ht, 500)
        self.assertEqual(diagnostic.value_sustainable_ht, Decimal("100.1"))
        self.assertEqual(diagnostic.value_label_rouge, 10)
        self.assertEqual(diagnostic.value_label_aoc_igp, 20)
        self.assertEqual(diagnostic.value_label_hve, 30)
        self.assertIn("seconds", body)

    @authenticate
    def test_location_found(self, mock):
        """
        Test that location information is filled in from import
        """
        address_api_text = "siret,citycode,postcode,result_citycode,result_postcode,result_city,result_context\n"
        address_api_text += '21340172201787,,11111,00000,11111,Ma ville,"01,Something,Other"\n'
        address_api_text += '73282932000074,00000,,00000,11111,Ma ville,"01,Something,Other"\n'
        address_api_text += '32441387130915,00000,11111,00000,22222,Ma ville,"01,Something,Other"\n'
        mock.post(
            "https://api-adresse.data.gouv.fr/search/csv/",
            text=address_api_text,
        )

        with open("./api/tests/files/diagnostics_locations.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.city_insee_code, "00000")
        self.assertEqual(canteen.city, "Ma ville")
        self.assertEqual(canteen.department, Department.ain)
        self.assertEqual(canteen.region, Region.auvergne_rhone_alpes)
        canteen = Canteen.objects.get(siret="73282932000074")
        self.assertEqual(canteen.postal_code, "11111")
        # Given both a city code and postcode, use citycode only to find location
        canteen = Canteen.objects.get(siret="32441387130915")
        self.assertEqual(canteen.city_insee_code, "00000")
        self.assertEqual(canteen.postal_code, "22222")

    @authenticate
    def test_location_not_found(self, mock):
        """
        If the location isn't found, fail silently
        """
        mock.post(
            "https://api-adresse.data.gouv.fr/search/csv/",
            text="83163531573760,00000,,,,,\n",
        )

        with open("./api/tests/files/diagnostics_bad_location.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="83163531573760")
        self.assertEqual(canteen.postal_code, "")
        self.assertEqual(canteen.city_insee_code, "00000")
        self.assertIsNone(canteen.city)
        self.assertIsNone(canteen.department)

    @authenticate
    def test_address_api_timeout(self, mock):
        """
        If the address API times out, fail silently
        """
        mock.post(
            "https://api-adresse.data.gouv.fr/search/csv/",
            exc=requests.exceptions.ConnectTimeout,
        )

        with open("./api/tests/files/diagnostics_locations.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.postal_code, "54460")
        self.assertEqual(canteen.city_insee_code, "")
        self.assertIsNone(canteen.city)
        self.assertIsNone(canteen.department)

    @authenticate
    def test_canteen_info_not_overridden(self, _):
        """
        If a canteen is present on multiple lines, keep data from first line
        """
        with open("./api/tests/files/diagnostics_same_canteen.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.count(), 2)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.name, "Updated name")

    @authenticate
    def test_location_overridden(self, mock):
        """
        If the canteen already has city/department data, update it on import
        to be consistent with handling of name, meal count, etc
        """
        canteen = CanteenFactory.create(
            siret="32441387130915",
            city_insee_code="55555",
            city="Ma ville",
            postal_code="66666",
            department=Department.ardeche,
        )
        canteen.managers.add(authenticate.user)

        address_api_text = "siret,citycode,postcode,result_citycode,result_postcode,result_city,result_context\n"
        address_api_text += '21340172201787,,11111,00000,11111,Ma ville,"01,Something,Other"\n'
        address_api_text += '73282932000074,00000,,00000,11111,Ma ville,"01,Something,Other"\n'
        address_api_text += '32441387130915,07293,11111,00000,22222,Saint-Romain-de-Lerps,"01,Something,Other"\n'

        mock.post(
            "https://api-adresse.data.gouv.fr/search/csv/",
            text=address_api_text,
        )
        with open("./api/tests/files/diagnostics_locations.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="32441387130915")
        self.assertEqual(canteen.city_insee_code, "00000")
        self.assertEqual(canteen.postal_code, "22222")
        self.assertEqual(canteen.city, "Saint-Romain-de-Lerps")
        self.assertEqual(canteen.department, Department.ain)

    @authenticate
    def test_cannot_modify_existing_canteen_unless_manager(self, _):
        """
        If a canteen exists, then you should have to already be it's manager to add diagnostics.
        No canteens will be created since any error cancels out the entire file
        """
        CanteenFactory.create(siret="21340172201787")
        my_canteen = CanteenFactory.create(siret="73282932000074")
        my_canteen.managers.add(authenticate.user)

        with open("./api/tests/files/diagnostics_different_canteens.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
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
    def test_valid_sectors_parsed(self, _):
        """
        File can specify 0+ sectors to add to the canteen
        """
        SectorFactory.create(name="Social et Médico-social (ESMS)")
        SectorFactory.create(name="Crèche")
        SectorFactory.create(name="Scolaire")
        with open("./api/tests/files/diagnostics_sectors.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.sectors.count(), 3)

    @authenticate
    def test_invalid_sectors_raise_error(self, _):
        """
        If file specifies invalid sector, error is raised for that line
        """
        SectorFactory.create(name="Social et Médico-social (ESMS)")
        with open("./api/tests/files/diagnostics_sectors.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        body = response.json()
        self.assertEqual(body["errors"][0]["status"], 400)
        self.assertEqual(
            body["errors"][0]["message"],
            "Le secteur spécifié ne fait pas partie des options acceptées",
        )

    @authenticate
    def test_error_collection(self, _):
        """
        If errors occur, discard the file and return the errors with row and message
        """
        with open("./api/tests/files/diagnostics_bad_file.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        errors = body["errors"]
        self.assertEqual(errors[0]["row"], 1)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2023.",
        )
        self.assertEqual(
            errors[1]["message"],
            "Champ 'année' : La valeur «\xa0.\xa0» doit être un nombre entier.",
        )
        self.assertEqual(
            errors[2]["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2023.",
        )
        self.assertEqual(
            errors[3]["message"],
            "Champ 'repas par jour' : La valeur «\xa0not a number\xa0» doit être un nombre entier.",
        )
        self.assertEqual(
            errors[4]["message"],
            "Champ 'mode de production' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors[5]["message"],
            "Champ 'Valeur totale annuelle HT' : Ce champ doit être un nombre décimal.",
        )
        self.assertEqual(
            errors[6]["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2023.",
        )
        self.assertEqual(
            errors[7]["message"],
            "Un diagnostic pour cette année et cette cantine existe déjà.",
        )
        self.assertEqual(
            errors[8]["message"],
            "Champ 'Valeur totale annuelle HT' : La somme des valeurs d'approvisionnement, 300, est plus que le total, 20",
        )
        self.assertEqual(
            errors[9]["message"],
            "Champ 'siret' : Le siret de la cantine ne peut pas être vide",
        )
        self.assertEqual(
            errors[10]["message"],
            "Champ 'Secteur économique' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors[11]["message"],
            "Données manquantes : 15 colonnes attendus, 14 trouvés.",
        )
        self.assertEqual(
            errors[12]["message"],
            "Champ 'repas par jour' : Ce champ ne peut pas être vide.",
        )
        self.assertEqual(
            errors[13]["message"],
            "Champ 'nom' : Ce champ ne peut pas être vide.",
        )
        self.assertEqual(
            errors[14]["message"],
            "Champ 'code postal' : Ce champ ne peut pas être vide si le code INSEE de la ville est vide.",
        )

    @authenticate
    def test_diagnostic_header_allowed(self, _):
        """
        Optionally allow a header that starts with SIRET in the file
        """
        with open("./api/tests/files/diagnostics_header.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["errors"]), 0)

    @authenticate
    def test_diagnostic_delimiter_options(self, _):
        """
        Optionally allow using a semicolon or tab as the delimiter
        """
        with open("./api/tests/files/diagnostics_delimiter_semicolon.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["errors"]), 0)

        with open("./api/tests/files/diagnostics_delimiter_tab.tsv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["errors"]), 0)

    @authenticate
    def test_decimal_comma_format(self, _):
        with open("./api/tests/files/diagnostics_decimal_number.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(body["errors"]), 0)

    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    @authenticate
    def test_max_size(self, _):
        with open("./api/tests/files/diagnostics_decimal_number.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        errors = body["errors"]
        self.assertEqual(
            errors[0]["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="test-from@example.com")
    def test_add_managers(self, _):
        """
        This file contains one diagnostic with three emails for managers. The first two
        already have an account with ma cantine, so they should be added. The third one
        has no account, so an invitation should be sent.
        All the managers would recieve an email, either a notification or an invitation.
        """
        gestionnaire_1 = UserFactory(email="gestionnaire1@example.com")
        gestionnaire_2 = UserFactory(email="gestionnaire2@example.com")

        with open("./api/tests/files/diagnostics_managers.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        canteen = Canteen.objects.get(siret="21340172201787")

        self.assertIn(authenticate.user, canteen.managers.all())
        self.assertIn(gestionnaire_1, canteen.managers.all())
        self.assertIn(gestionnaire_2, canteen.managers.all())

        self.assertTrue(ManagerInvitation.objects.count(), 1)
        self.assertEqual(ManagerInvitation.objects.first().email, "gestionnaire3@example.com")

        self.assertEqual(len(mail.outbox), 3)

    @authenticate
    def test_add_managers_invalid_email(self, _):
        with open("./api/tests/files/diagnostics_managers_invalid_email.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["count"], 0)

        errors = body["errors"]
        self.assertEqual(errors[0]["row"], 2)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(errors[0]["message"], "Champ 'email' : Un adresse email des gestionnaires n'est pas valide.")

        self.assertEqual(len(mail.outbox), 0)

    @authenticate
    def test_add_managers_empty_column(self, _):
        with open("./api/tests/files/diagnostics_managers_empty_column.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_cannot_email_file_not_authenticated(self, _):
        """
        If user is not authenticated, cannot send file using this API
        """
        with open("./api/tests/files/diagnostics_bad_file.csv") as diag_file:
            response = self.client.post(reverse("email_diagnostic_file"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(CONTACT_EMAIL="team@example.com")
    @authenticate
    def test_email_diagnostics_file(self, _):
        """
        Check that this endpoint sends an email with the file attached and relevant info
        """
        with open("./api/tests/files/diagnostics_bad_file.csv") as diag_file:
            response = self.client.post(
                reverse("email_diagnostic_file"),
                {"file": diag_file, "message": "Help me", "name": "Camille Dupont", "email": "dupont@example.com"},
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to[0], "team@example.com")
        self.assertEqual("dupont@example.com", email.reply_to[0])
        self.assertEqual(email.attachments[0][0], "diagnostics_bad_file.csv")
        self.assertIn("dupont@example.com", email.body)
        self.assertIn("Camille Dupont", email.body)
        self.assertIn("Help me", email.body)


class TestImportDiagnosticsFromAPIIntegration(APITestCase):
    @unittest.skipUnless(os.environ.get("ENVIRONMENT") == "dev", "Not in dev environment")
    @authenticate
    def test_location_found_integration(self):
        """
        Test that remaining location information is filled in from import when calling the real API
        """
        with open("./api/tests/files/diagnostics_locations.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen.city_insee_code, "54318")
        self.assertEqual(canteen.city, "Liverdun")
        self.assertEqual(canteen.department, Department.meurthe_et_moselle)

        canteen = Canteen.objects.get(siret="73282932000074")
        self.assertEqual(canteen.postal_code, "07130")
        self.assertEqual(canteen.city, "Saint-Romain-de-Lerps")
        self.assertEqual(canteen.department, Department.ardeche)
        # Given both a city code and postcode, use citycode only to find location
        canteen = Canteen.objects.get(siret="32441387130915")
        self.assertEqual(canteen.city_insee_code, "07293")
        self.assertEqual(canteen.postal_code, "07130")
        self.assertEqual(canteen.city, "Saint-Romain-de-Lerps")
        self.assertEqual(canteen.department, Department.ardeche)
