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
from data.models.teledeclaration import Teledeclaration
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
        self.assertEqual(canteen.yearly_meal_count, 14000)
        self.assertEqual(canteen.production_type, "site")
        self.assertEqual(canteen.management_type, "conceded")
        self.assertEqual(canteen.economic_model, "public")
        self.assertEqual(canteen.central_producer_siret, "42126486200010")
        self.assertEqual(canteen.publication_status, Canteen.PublicationStatus.DRAFT)
        diagnostic = Diagnostic.objects.get(canteen_id=canteen.id)
        self.assertEqual(diagnostic.year, 2020)
        self.assertEqual(diagnostic.value_total_ht, 1000)
        self.assertEqual(diagnostic.value_bio_ht, 500)
        self.assertEqual(diagnostic.value_sustainable_ht, Decimal("100.1"))
        self.assertEqual(diagnostic.value_externality_performance_ht, 10)
        self.assertEqual(diagnostic.value_egalim_others_ht, 20)
        self.assertEqual(diagnostic.value_meat_poultry_ht, 30)
        self.assertEqual(diagnostic.value_meat_poultry_egalim_ht, 1)
        self.assertEqual(diagnostic.value_meat_poultry_france_ht, 2)
        self.assertEqual(diagnostic.value_fish_ht, 4)
        self.assertEqual(diagnostic.value_fish_egalim_ht, 3)
        self.assertEqual(diagnostic.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
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
        self.assertEqual(Diagnostic.objects.count(), 0)
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
    def test_import_some_without_diagnostic(self, _):
        """
        Should be able to import canteens without creating diagnostics if only canteen columns
        are present
        """
        with open("./api/tests/files/mix_diag_canteen_import.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.count(), 1)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["errors"]), 0)
        diagnostic = Diagnostic.objects.first()
        self.assertEqual(diagnostic.canteen.siret, "73282932000074")
        self.assertEqual(Diagnostic.objects.filter(canteen=Canteen.objects.get(siret="21340172201787")).count(), 0)

    @authenticate
    def test_import_only_canteens(self, _):
        """
        Should be able to import canteens from a file that doesn't have commas for the optional fields
        """
        with open("./api/tests/files/canteen_import.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Canteen.objects.first().economic_model, None)

    @authenticate
    def test_staff_import(self, _):
        """
        Staff get to specify extra columns and have fewer requirements on what data is required.
        Test that a mixed import of canteens/diagnostics works.
        Test that can add some managers without sending emails to them.
        Check that the importer isn't added to the canteen unless specified.
        """
        user = authenticate.user
        user.is_staff = True
        user.email = "authenticate@example.com"
        user.save()

        with open("./api/tests/files/mix_diag_canteen_staff_import.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["count"], 1)  # 1 bc only diagnostics returned not canteens
        self.assertEqual(len(body["canteens"]), 2)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.count(), 1)
        self.assertEqual(ManagerInvitation.objects.count(), 4)
        self.assertEqual(len(mail.outbox), 1)

        canteen1 = Canteen.objects.get(siret="21340172201787")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen1, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen1, email="user2@example.com"))
        self.assertEqual(canteen1.managers.count(), 0)
        self.assertEqual(canteen1.import_source, "Automated test")
        self.assertEqual(canteen1.publication_status, Canteen.PublicationStatus.PUBLISHED)

        canteen2 = Canteen.objects.get(siret="73282932000074")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen2, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen2, email="user2@example.com"))
        self.assertIsNotNone(Diagnostic.objects.get(canteen=canteen2))
        self.assertEqual(canteen2.managers.count(), 1)
        self.assertEqual(canteen2.managers.first(), user)
        self.assertEqual(canteen2.import_source, "Automated test")
        self.assertEqual(canteen2.publication_status, Canteen.PublicationStatus.DRAFT)

        email = mail.outbox[0]
        self.assertEqual(email.to[0], "user1@example.com")
        self.assertNotIn("Canteen for two", email.body)
        self.assertIn("Staff canteen", email.body)

    @authenticate
    def test_staff_import_non_staff(self, _):
        """
        Non-staff users shouldn't have staff import capabilities
        """
        with open("./api/tests/files/mix_diag_canteen_staff_import.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(body["errors"]), 2)
        self.assertEqual(body["errors"][0]["message"], "Format fichier : 23 ou 12 colonnes attendues, 26 trouvées.")
        self.assertEqual(body["errors"][0]["status"], 401)

    @authenticate
    def test_error_collection(self, _):
        """
        If errors occur, discard the file and return the errors with row and message
        """
        # creating 2 canteens with same siret here to error when this situation exists IRL
        CanteenFactory.create(siret="42111303053388")
        CanteenFactory.create(siret="42111303053388")
        with open("./api/tests/files/diagnostics_bad_file.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        # no new objects should have been saved to the DB since it failed
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.count(), 0)
        errors = body["errors"]
        first_error = errors.pop(0)
        self.assertEqual(first_error["row"], 1)
        self.assertEqual(first_error["status"], 400)
        self.assertEqual(
            first_error["message"],
            "Champ 'année' : L'année est obligatoire pour créer un diagnostic.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'année' : La valeur «\xa0.\xa0» doit être un nombre entier.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2024.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'repas par jour' : La valeur « not a number » doit être un nombre entier.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'mode de production' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : Ce champ doit être un nombre décimal.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'année' : L'année doit être comprise entre 2019 et 2024.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Un diagnostic pour cette année et cette cantine existe déjà.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : La somme des valeurs d'approvisionnement, 300, est plus que le total, 20",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'siret' : Le siret de la cantine ne peut pas être vide",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Secteur économique' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'repas par an (y compris livrés)' : Ce champ ne peut pas être vide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'repas par jour' : Ce champ ne peut pas être vide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'nom' : Ce champ ne peut pas être vide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'code postal' : Ce champ ne peut pas être vide si le code INSEE de la ville est vide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Plusieurs cantines correspondent au SIRET 42111303053388. Veuillez enlever les doublons pour pouvoir créer le diagnostic.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées EGAlim, 100, est plus que la valeur totale (HT) viandes et volailles, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, 100, est plus que la valeur totale (HT) viandes et volailles, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques EGAlim, 100, est plus que la valeur totale (HT) poissons et produits aquatiques, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            # TODO: is this the best field to point to as being wrong? hors bio could be confusing
            "Champ 'Produits SIQO (hors bio) - Valeur annuelle HT' : La somme des valeurs viandes et poissons EGAlim, 300, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGAlim, 200",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'siret' : Le SIRET doit être composé des chiffres",
        )

    @authenticate
    def test_staff_error_collection(self, _):
        """
        If errors occur, discard the file and return the errors with row and message
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        with open("./api/tests/files/diagnostics_bad_staff_file.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(Canteen.objects.count(), 0)
        errors = body["errors"]
        first_error = errors.pop(0)
        self.assertEqual(first_error["status"], 400)
        self.assertEqual(
            first_error["message"],
            "Champ 'état de publication' : La valeur «\xa0'publish'\xa0» n’est pas un choix valide.",
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

    @authenticate
    def test_success_complete_diagnostic_import(self, _):
        """
        Users should be able to import a complete diagnostic
        """
        with open("./api/tests/files/complete_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        finished_diag = Diagnostic.objects.get(canteen__siret="29969025300230", year=2021)
        self.assertEqual(finished_diag.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(finished_diag.value_total_ht, 10500)
        self.assertEqual(finished_diag.value_meat_poultry_ht, 800)
        self.assertEqual(finished_diag.value_fish_ht, 900)
        self.assertEqual(finished_diag.total_label_bio, 80)
        self.assertEqual(finished_diag.total_label_label_rouge, 90)
        self.assertEqual(finished_diag.total_label_aocaop_igp_stg, 100)
        self.assertEqual(finished_diag.total_label_hve, 110)
        self.assertEqual(finished_diag.total_label_peche_durable, 120)
        self.assertEqual(finished_diag.total_label_rup, 130)
        self.assertEqual(finished_diag.total_label_commerce_equitable, 140)
        self.assertEqual(finished_diag.total_label_fermier, 150)
        self.assertEqual(finished_diag.total_label_externalites, 160)
        self.assertEqual(finished_diag.total_label_performance, 170)
        self.assertEqual(finished_diag.total_label_non_egalim, 180)
        self.assertEqual(finished_diag.total_label_france, 190)
        self.assertEqual(finished_diag.total_label_short_distribution, 200)
        self.assertEqual(finished_diag.total_label_local, 210)
        self.assertEqual(finished_diag.total_family_viandes_volailles, 110)
        self.assertEqual(finished_diag.total_family_produits_de_la_mer, 110)
        self.assertEqual(finished_diag.total_family_fruits_et_legumes, 110)
        self.assertEqual(finished_diag.total_family_charcuterie, 110)
        self.assertEqual(finished_diag.total_family_produits_laitiers, 110)
        self.assertEqual(finished_diag.total_family_boulangerie, 110)
        self.assertEqual(finished_diag.total_family_boissons, 110)
        self.assertEqual(finished_diag.total_family_autres, 660)
        # auto-calculated simplified fields
        self.assertEqual(finished_diag.value_bio_ht, 80)
        self.assertEqual(finished_diag.value_sustainable_ht, 190)
        self.assertEqual(finished_diag.value_externality_performance_ht, 330)
        self.assertEqual(finished_diag.value_egalim_others_ht, 650)
        self.assertEqual(finished_diag.value_meat_poultry_egalim_ht, 100)
        self.assertEqual(finished_diag.value_meat_poultry_france_ht, 30)
        self.assertEqual(finished_diag.value_fish_egalim_ht, 100)

        unfinished_diag = Diagnostic.objects.get(canteen__siret="29969025300230", year=2022)
        self.assertEqual(unfinished_diag.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(unfinished_diag.value_total_ht, 30300)  # picked a field at random to smoke test
        self.assertEqual(unfinished_diag.value_meat_poultry_ht, None)
        self.assertEqual(unfinished_diag.value_fish_ht, 10)
        self.assertEqual(unfinished_diag.value_autres_label_rouge, None)  # picked a field at random to smoke test

    @authenticate
    def test_complete_diagnostic_error_collection(self, _):
        """
        Test that the expected errors are returned for a badly formatted file for complete diagnostic
        """
        with open("./api/tests/files/bad_complete_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        body = response.json()
        self.assertEqual(body["count"], 0)
        errors = body["errors"]
        self.assertGreater(len(errors), 0)
        first_error = errors.pop(0)
        self.assertEqual(
            first_error["message"],
            "Champ 'année' : Ce champ doit être un nombre entier. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer.",
        )
        # two of the same error, generated in slightly different ways
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'année' : Ce champ doit être un nombre entier. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Données manquantes : au moins 13 colonnes attendues, 12 trouvées. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : Ce champ doit être un nombre décimal.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Produits aquatiques frais et surgelés, Bio' : Ce champ doit être vide ou un nombre décimal.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées EGAlim, 100, est plus que la valeur totale (HT) viandes et volailles, 10",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, 920, est plus que la valeur totale (HT) viandes et volailles, 100",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques EGAlim, 100, est plus que la valeur totale (HT) poissons et produits aquatiques, 10",
        )

        with open("./api/tests/files/bad_header_complete_diagnostics_0.csv") as diag_file:
            response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})
        body = response.json()

        self.assertEqual(
            body["errors"][0]["message"],
            "Deux lignes en-tête attendues, 0 trouvée. Veuillez vérifier que vous voulez importer les diagnostics complets, et assurez-vous que le format de l'en-tête suit les exemples donnés.",
        )

        with open("./api/tests/files/bad_header_complete_diagnostics_1.csv") as diag_file:
            response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})
        body = response.json()

        self.assertEqual(
            body["errors"][0]["message"],
            "Deux lignes en-tête attendues, 1 trouvée. Veuillez vérifier que vous voulez importer les diagnostics complets, et assurez-vous que le format de l'en-tête suit les exemples donnés.",
        )

    @authenticate
    def test_tmp_no_staff_complete_diag(self, _):
        """
        Test error is thrown if staff attempts to add metadata
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        with open("./api/tests/files/staff_complete_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        body = response.json()
        self.assertEqual(body["count"], 0)
        errors = body["errors"]
        self.assertGreater(len(errors), 0)
        self.assertEqual(errors.pop(0)["message"], "Format fichier : 128 colonnes attendues, 131 trouvées.")
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'année' : Ce champ doit être un nombre entier. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer.",
        )

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

    @authenticate
    def test_canteens_empty_when_error(self, _):
        """
        If a cantine succeeds and another one doesn't, no canteen should be saved
        and the array of cantine should return zero
        """
        SectorFactory.create(name="Crèche")
        with open("./api/tests/files/mixed_cantine_creation.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)

    @authenticate
    def test_teledeclare_diagnostics_on_import(self, _):
        """
        Staff have the option to teledeclare imported diagnostics directly from import
        NB: since total is required for diag import all teledeclarations should work
        """
        user = authenticate.user
        user.is_staff = True
        user.email = "authenticate@example.com"
        user.save()
        self.assertEqual(Teledeclaration.objects.count(), 0)
        with open("./api/tests/files/teledeclaration_simple.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["teledeclarations"], 1)
        self.assertEqual(Teledeclaration.objects.count(), 1)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_error_teledeclare_diagnostics_on_import(self, _):
        """
        Provide line-by-line errors if the import isn't successful
        """
        user = authenticate.user
        user.is_staff = True
        user.email = "authenticate@example.com"
        user.save()
        with open("./api/tests/files/teledeclaration_error.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        body = response.json()
        self.assertEqual(len(body["errors"]), 2)
        self.assertEqual(
            body["errors"][0]["message"],
            "Champ 'teledeclaration' : 'lol' n'est pas un statut de télédéclaration valid",
        )
        self.assertEqual(
            body["errors"][1]["message"],
            "C'est que possible de télédéclarer pour l'année 2022. Ce diagnostic est pour 2021.",
        )
        self.assertEqual(Diagnostic.objects.count(), 0)
        self.assertEqual(Teledeclaration.objects.count(), 0)

    @override_settings(ENABLE_TELEDECLARATION=False)
    @authenticate
    def test_error_teledeclare_diagnostics_on_import_not_campaign(self, _):
        """
        Prevent importing TDs if outside of campagne
        """
        user = authenticate.user
        user.is_staff = True
        user.save()
        with open("./api/tests/files/teledeclaration_simple.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        body = response.json()
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "Champ 'teledeclaration' : c'est pas possible de télédéclarer des diagnostics hors de campagne",
        )

    @authenticate
    def test_optional_appro_values(self, _):
        """
        For simplified diagnostics, an empty appro value is considered unknown
        """
        with open("./api/tests/files/diagnostic_simplified_optional_appro.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        body = response.json()
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Diagnostic.objects.count(), 1)
        diagnostic = Diagnostic.objects.first()

        self.assertEqual(diagnostic.value_total_ht, 1000)
        self.assertIsNone(diagnostic.value_bio_ht)
        self.assertEqual(diagnostic.value_sustainable_ht, 0)

    @authenticate
    def test_mandatory_total_ht_simplified(self, _):
        """
        For simplified diagnostics, only the total HT is mandatory in the appro fields
        """
        with open("./api/tests/files/diagnostic_simplified_missing_total_ht.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        body = response.json()
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(Diagnostic.objects.count(), 0)

        self.assertEqual(
            body["errors"][0]["message"], "Champ 'Valeur totale annuelle HT' : Ce champ doit être un nombre décimal."
        )

    @authenticate
    def test_siret_cc(self, _):
        """
        A validation error should appear if the SIRET for the CC is the same as the SIRET
        for the canteen.
        """
        with open("./api/tests/files/diagnostic_same_siret_cc.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

        body = response.json()
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(Diagnostic.objects.count(), 0)

        self.assertEqual(
            body["errors"][0]["message"],
            "Champ 'siret de la cuisine centrale' : Le SIRET de la cuisine centrale doit être différent de celui de la cantine",
        )

    @authenticate
    def test_success_cuisine_centrale_complete_import(self, _):
        """
        Users should be able to import a file with central cuisines and their satellites, with only
        appro data at the level of the cuisine centrale.
        """
        with open("./api/tests/files/cc_complete_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_cc_complete_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)  # Only two diagnostics created
        self.assertEqual(len(body["canteens"]), 7)  # Seven canteens involved

        # Verify the correct links between CC and satellites are created

        cuisine_centrale_1 = Canteen.objects.get(siret="29969025300230")
        satellite_1_1 = Canteen.objects.get(siret="38589540005962")
        satellite_1_2 = Canteen.objects.get(siret="30218342886548")
        satellite_1_3 = Canteen.objects.get(siret="27309825823572")

        cuisine_centrale_2 = Canteen.objects.get(siret="96463820453707")
        satellite_2_1 = Canteen.objects.get(siret="65436828882140")
        satellite_2_2 = Canteen.objects.get(siret="21231178258956")

        for satellite in (satellite_1_1, satellite_1_2, satellite_1_3):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_1.siret)

        for satellite in (satellite_2_1, satellite_2_2):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_2.siret)

        # Ensure no diagnostics were created in the satellites

        for satellite in (satellite_1_1, satellite_1_2, satellite_1_3, satellite_2_1, satellite_2_2):
            self.assertFalse(Diagnostic.objects.filter(canteen=satellite).exists())

        # Verify the content of diagnostics for the CCs

        finished_diag = Diagnostic.objects.get(canteen__siret="29969025300230", year=2021)
        finished_diag.central_kitchen_diagnostic_mode = Diagnostic.CentralKitchenDiagnosticMode.APPRO

        self.assertEqual(finished_diag.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(finished_diag.value_total_ht, 10500)
        self.assertEqual(finished_diag.value_meat_poultry_ht, 800)
        self.assertEqual(finished_diag.value_fish_ht, 900)
        self.assertEqual(finished_diag.total_label_bio, 80)
        self.assertEqual(finished_diag.total_label_label_rouge, 90)
        self.assertEqual(finished_diag.total_label_aocaop_igp_stg, 100)
        self.assertEqual(finished_diag.total_label_hve, 110)
        self.assertEqual(finished_diag.total_label_peche_durable, 120)
        self.assertEqual(finished_diag.total_label_rup, 130)
        self.assertEqual(finished_diag.total_label_commerce_equitable, 140)
        self.assertEqual(finished_diag.total_label_fermier, 150)
        self.assertEqual(finished_diag.total_label_externalites, 160)
        self.assertEqual(finished_diag.total_label_performance, 170)
        self.assertEqual(finished_diag.total_label_non_egalim, 180)
        self.assertEqual(finished_diag.total_label_france, 190)
        self.assertEqual(finished_diag.total_label_short_distribution, 200)
        self.assertEqual(finished_diag.total_label_local, 210)
        self.assertEqual(finished_diag.total_family_viandes_volailles, 110)
        self.assertEqual(finished_diag.total_family_produits_de_la_mer, 110)
        self.assertEqual(finished_diag.total_family_fruits_et_legumes, 110)
        self.assertEqual(finished_diag.total_family_charcuterie, 110)
        self.assertEqual(finished_diag.total_family_produits_laitiers, 110)
        self.assertEqual(finished_diag.total_family_boulangerie, 110)
        self.assertEqual(finished_diag.total_family_boissons, 110)
        self.assertEqual(finished_diag.total_family_autres, 660)
        # auto-calculated simplified fields
        self.assertEqual(finished_diag.value_bio_ht, 80)
        self.assertEqual(finished_diag.value_sustainable_ht, 190)
        self.assertEqual(finished_diag.value_externality_performance_ht, 330)
        self.assertEqual(finished_diag.value_egalim_others_ht, 650)
        self.assertEqual(finished_diag.value_meat_poultry_egalim_ht, 100)
        self.assertEqual(finished_diag.value_meat_poultry_france_ht, 30)
        self.assertEqual(finished_diag.value_fish_egalim_ht, 100)

        unfinished_diag = Diagnostic.objects.get(canteen__siret="96463820453707", year=2022)
        unfinished_diag.central_kitchen_diagnostic_mode = Diagnostic.CentralKitchenDiagnosticMode.APPRO

        self.assertEqual(unfinished_diag.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(unfinished_diag.value_total_ht, 30300)
        self.assertEqual(unfinished_diag.value_meat_poultry_ht, None)
        self.assertEqual(unfinished_diag.value_fish_ht, 10)
        self.assertEqual(unfinished_diag.value_autres_label_rouge, None)

    @authenticate
    def test_success_cuisine_centrale_complete_update_satellites(self, _):
        """
        Users should be able to import a file with central cuisines and their satellites. The existing satellites
        should be updated.
        """
        # In the file, cuisine_centrale_1 has three satellites. We will create two of them and verify that a
        # third one is added after the import
        cuisine_centrale_1 = CanteenFactory.create(
            siret="29969025300230", production_type=Canteen.ProductionType.CENTRAL
        )
        satellite_1_1 = CanteenFactory.create(
            siret="38589540005962",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="29969025300230",
        )
        satellite_1_3 = CanteenFactory.create(
            siret="27309825823572",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="29969025300230",
        )

        # In the file, cuisine_centrale_2 has two satellites. We will create a different one of them and verify that a
        # it is removed from the list of satellites after the import
        cuisine_centrale_2 = CanteenFactory.create(
            siret="96463820453707", production_type=Canteen.ProductionType.CENTRAL
        )
        satellite_to_remove = CanteenFactory.create(
            siret="44331934540185",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="96463820453707",
        )

        for canteen in (cuisine_centrale_1, satellite_1_1, satellite_1_3, cuisine_centrale_2, satellite_to_remove):
            canteen.managers.add(authenticate.user)

        with open("./api/tests/files/cc_complete_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_cc_complete_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)  # Only two diagnostics created
        self.assertEqual(len(body["canteens"]), 7)  # Seven canteens involved

        for canteen in (cuisine_centrale_1, satellite_1_1, satellite_1_3, cuisine_centrale_2, satellite_to_remove):
            canteen.refresh_from_db()

        satellite_1_2 = Canteen.objects.get(siret="30218342886548")
        satellite_2_1 = Canteen.objects.get(siret="65436828882140")
        satellite_2_2 = Canteen.objects.get(siret="21231178258956")

        self.assertIsNone(satellite_to_remove.central_producer_siret)
        self.assertEqual(cuisine_centrale_1.satellite_canteens_count, 3)
        self.assertEqual(cuisine_centrale_2.satellite_canteens_count, 2)

        for satellite in (satellite_1_1, satellite_1_2, satellite_1_3):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_1.siret)

        for satellite in (satellite_2_1, satellite_2_2):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_2.siret)

    @authenticate
    def test_success_cuisine_centrale_simple_import(self, _):
        """
        Users should be able to import a file with central cuisines and their satellites, with only
        simplified appro data at the level of the cuisine centrale.
        """
        with open("./api/tests/files/cc_simple_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_cc_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)  # Only two diagnostics created
        self.assertEqual(len(body["canteens"]), 7)  # Seven canteens involved

        # Verify the correct links between CC and satellites are created

        cuisine_centrale_1 = Canteen.objects.get(siret="29969025300230")
        satellite_1_1 = Canteen.objects.get(siret="38589540005962")
        satellite_1_2 = Canteen.objects.get(siret="30218342886548")
        satellite_1_3 = Canteen.objects.get(siret="27309825823572")

        cuisine_centrale_2 = Canteen.objects.get(siret="96463820453707")
        satellite_2_1 = Canteen.objects.get(siret="65436828882140")
        satellite_2_2 = Canteen.objects.get(siret="21231178258956")

        for satellite in (satellite_1_1, satellite_1_2, satellite_1_3):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_1.siret)

        for satellite in (satellite_2_1, satellite_2_2):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_2.siret)

        # Ensure no diagnostics were created in the satellites

        for satellite in (satellite_1_1, satellite_1_2, satellite_1_3, satellite_2_1, satellite_2_2):
            self.assertFalse(Diagnostic.objects.filter(canteen=satellite).exists())

        # Verify the content of diagnostics for the CCs

        cc1_diag = Diagnostic.objects.get(canteen__siret="29969025300230", year=2021)
        cc1_diag.central_kitchen_diagnostic_mode = Diagnostic.CentralKitchenDiagnosticMode.APPRO

        self.assertEqual(cc1_diag.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
        self.assertEqual(cc1_diag.value_total_ht, 10500)
        self.assertEqual(cc1_diag.value_bio_ht, 500)
        self.assertEqual(cc1_diag.value_sustainable_ht, Decimal("100.10"))
        self.assertEqual(cc1_diag.value_meat_poultry_ht, 0)
        self.assertEqual(cc1_diag.value_fish_ht, 0)

        cc2_diag = Diagnostic.objects.get(canteen__siret="96463820453707", year=2022)
        cc2_diag.central_kitchen_diagnostic_mode = Diagnostic.CentralKitchenDiagnosticMode.APPRO

        self.assertEqual(cc2_diag.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
        self.assertEqual(cc2_diag.value_total_ht, 30300)
        self.assertEqual(cc2_diag.value_meat_poultry_ht, 6000)
        self.assertEqual(cc2_diag.value_fish_ht, 3000)

    @authenticate
    def test_success_cuisine_centrale_simple_update_satellites(self, _):
        """
        Users should be able to import a file with central cuisines and their satellites. The existing satellites
        should be updated. This should be the case even if the user does not manage the satellites.
        """
        # In the file, cuisine_centrale_1 has three satellites. We will create two of them and verify that a
        # third one is added after the import
        cuisine_centrale_1 = CanteenFactory.create(
            siret="29969025300230", production_type=Canteen.ProductionType.CENTRAL
        )
        satellite_1_1 = CanteenFactory.create(
            siret="38589540005962",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="29969025300230",
        )
        satellite_1_3 = CanteenFactory.create(
            siret="27309825823572",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="29969025300230",
        )

        # In the file, cuisine_centrale_2 has two satellites. We will create a different one of them and verify that a
        # it is removed from the list of satellites after the import
        cuisine_centrale_2 = CanteenFactory.create(
            siret="96463820453707", production_type=Canteen.ProductionType.CENTRAL
        )
        satellite_to_remove = CanteenFactory.create(
            siret="44331934540185",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="96463820453707",
        )

        for canteen in (cuisine_centrale_1, satellite_1_1, satellite_1_3, cuisine_centrale_2, satellite_to_remove):
            canteen.managers.add(authenticate.user)

        with open("./api/tests/files/cc_simple_diagnostics.csv") as diag_file:
            response = self.client.post(f"{reverse('import_cc_diagnostics')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)  # Only two diagnostics created
        self.assertEqual(len(body["canteens"]), 7)  # Seven canteens involved

        for canteen in (cuisine_centrale_1, satellite_1_1, satellite_1_3, cuisine_centrale_2, satellite_to_remove):
            canteen.refresh_from_db()

        satellite_1_2 = Canteen.objects.get(siret="30218342886548")
        satellite_2_1 = Canteen.objects.get(siret="65436828882140")
        satellite_2_2 = Canteen.objects.get(siret="21231178258956")

        self.assertIsNone(satellite_to_remove.central_producer_siret)
        self.assertEqual(cuisine_centrale_1.satellite_canteens_count, 3)
        self.assertEqual(cuisine_centrale_2.satellite_canteens_count, 2)

        for satellite in (satellite_1_1, satellite_1_2, satellite_1_3):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_1.siret)

        for satellite in (satellite_2_1, satellite_2_2):
            self.assertEqual(satellite.central_producer_siret, cuisine_centrale_2.siret)


class TestImportDiagnosticsFromAPIIntegration(APITestCase):
    @unittest.skipUnless(os.environ.get("ENVIRONMENT") == "dev", "Not in dev environment")
    @authenticate
    def test_location_found_integration(self):
        """
        Test that remaining location information is filled in from import when calling the real API
        """
        with open("./api/tests/files/diagnostics_locations.csv") as diag_file:
            with requests_mock.Mocker() as m:
                m.register_uri("POST", "https://api-adresse.data.gouv.fr/search/csv/", real_http=True)
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
