import hashlib
import json
import re
from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import skipIf
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory
from data.models import ImportFailure, ImportType
from data.models.creation_source import CreationSource
from data.models.purchase import Purchase


class TestPurchaseSchema(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open("data/schemas/imports/achats.json"))

    def test_prix_ht_decimal(self):
        field_index = next((i for i, f in enumerate(self.schema["fields"]) if f["name"] == "prix_ht"), None)
        pattern = self.schema["fields"][field_index]["constraints"]["pattern"]
        for VALUE_OK in ["1234", "1234.0", "1234.99", "1234.99999", "1234,0", "1234,99", "1234,99999"]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["", " ", "TEST", "1234.99.99", "1234,99,99"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_famille_produits_regex(self):
        field_index = next((i for i, f in enumerate(self.schema["fields"]) if f["name"] == "famille_produits"), None)
        pattern = self.schema["fields"][field_index]["constraints"]["pattern"]
        for VALUE_OK in ["PRODUITS_LAITIERS", "PRODUITS_LAITIERS ", " PRODUITS_LAITIERS "]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["", "TEST", "PRODUITS_LAITIERS,", "PRODUITS_LAITIERS,VIANDES_VOLAILLES"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_caracteristiques_regex(self):
        field_index = next((i for i, f in enumerate(self.schema["fields"]) if f["name"] == "caracteristiques"), None)
        pattern = self.schema["fields"][field_index]["constraints"]["pattern"]
        for VALUE_OK in [
            "BIO",
            "BIO ",
            "BIO,LOCAL",
            "BIO,LOCAL ",
            " BIO,LOCAL ",
            " BIO, LOCAL ",
            " BIO,      LOCAL ",
            "BIO,BIO",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["TEST"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_definition_local_regex(self):
        field_index = next((i for i, f in enumerate(self.schema["fields"]) if f["name"] == "definition_local"), None)
        pattern = self.schema["fields"][field_index]["constraints"]["pattern"]
        for VALUE_OK in ["DEPARTEMENT", "DEPARTEMENT ", " DEPARTEMENT "]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["", "TEST", "DEPARTEMENT,", "DEPARTEMENT,REGION"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class TestPurchaseImport(APITestCase):
    def test_unauthenticated_import_call(self):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_purchases"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_import_good_purchases(self):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 5)
        self.assertFalse(ImportFailure.objects.exists())
        purchase = Purchase.objects.filter(description="Pommes, rouges, local").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.description, "Pommes, rouges, local")
        self.assertEqual(purchase.provider, "Le bon traiteur")
        self.assertEqual(purchase.price_ht, Decimal("90.11"))
        self.assertEqual(purchase.date, date(2022, 5, 2))
        self.assertEqual(purchase.family, Purchase.Family.PRODUITS_LAITIERS)
        self.assertEqual(purchase.characteristics, [Purchase.Characteristic.BIO, Purchase.Characteristic.LOCAL])
        self.assertEqual(purchase.local_definition, Purchase.Local.DEPARTEMENT)
        self.assertIsNotNone(purchase.import_source)
        self.assertEqual(purchase.creation_source, CreationSource.IMPORT)
        # purchase with definition_local empty
        purchase = Purchase.objects.filter(description="Pommes, vertes 1").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.family, Purchase.Family.PRODUITS_LAITIERS)
        self.assertEqual(purchase.characteristics, [Purchase.Characteristic.RUP])
        self.assertEqual(purchase.local_definition, "")
        # purchase with characteristics empty
        purchase = Purchase.objects.filter(description="Pommes, vertes 4").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.family, Purchase.Family.AUTRES)
        self.assertEqual(purchase.characteristics, [""])
        # Test that the purchase import source contains the complete file digest
        filebytes = Path("./api/tests/files/achats/purchases_good.csv").read_bytes()
        filehash_md5 = hashlib.md5(filebytes).hexdigest()
        self.assertEqual(Purchase.objects.first().import_source, filehash_md5)

    @authenticate
    def test_import_comma_separated_numbers(self):
        """
        Tests that can import a file with comma-separated numbers
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_good_separator_comma.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.price_ht, Decimal("90.11"))

    @authenticate
    def test_import_with_local_definition_missing(self):
        """
        If characteristics includes LOCAL, local_definition must be filled
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_bad_no_local_definition.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        errors = response.json()["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"], "La caractéristique LOCAL est sélectionnée : le champ doit être rempli."
        )
        self.assertEqual(errors[0]["status"], 400)

    @authenticate
    def test_import_purchases_different_separators(self):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        # tab
        file_path = "./api/tests/files/achats/purchases_good_separator_tab.tsv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())

        # semicolon
        file_path = "./api/tests/files/achats/purchases_good_separator_semicolon.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1 + 1)
        self.assertFalse(ImportFailure.objects.exists())

    @authenticate
    @override_settings(CSV_PURCHASE_CHUNK_LINES=1)
    @patch("api.views.ImportPurchasesView._process_chunk")
    def test_import_batch_purchases(self, _process_chunk_mock):
        """
        Tests that actually split the file into chunks. The header is considered as a line.
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            _ = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(_process_chunk_mock.call_count, 5)

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=10)
    def test_import_file_too_big(self):
        """
        Test that the file is not treated if there are too many lines
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="36462492895701")

        file_path = "./api/tests/files/achats/purchases_bad.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        errors = response.json()["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )
        self.assertEqual(errors[0]["status"], 400)

    @authenticate
    def test_import_no_header(self):
        """
        A file should not be valid if doesn't contain a header
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad_no_header.csv"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(f"{reverse('import_purchases')}", {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_import_wrong_header(self):
        """
        A file should not be valid if doesn't contain a valid header
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # wrong header
        file_path = "./api/tests/files/achats/purchases_bad_wrong_header.csv"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(f"{reverse('import_purchases')}", {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

        # partial header
        file_path = "./api/tests/files/achats/purchases_bad_partial_header.csv"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(f"{reverse('import_purchases')}", {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_import_bad_purchases(self):
        """
        Test that the right errors are thrown
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="36462492895701")

        file_path = "./api/tests/files/achats/purchases_bad.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        errors = response.json()["errors"]
        self.assertEqual(len(errors), 12)
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # siret
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # description
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # provider
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # family
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # date
        self.assertEqual(
            errors.pop(0)["message"],
            "La date doit être écrite sous la forme `aaaa-mm-jj`",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "La date doit être écrite sous la forme `aaaa-mm-jj`",
        )
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # price
        self.assertTrue(errors.pop(0)["message"].startswith("A price ne respecte pas le motif imposé"))
        self.assertTrue(
            errors.pop(0)["message"].startswith("NOPE ne respecte pas le motif imposé"),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith("BIO,NOPE ne respecte pas le motif imposé"),
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "La ligne n'a pas le même nombre de cellules que l'en-tête",
        )

    @authenticate
    def test_import_corrupt_purchases_file(self):
        """
        A reasonable error should be thrown
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_bad_corrupt.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        errors = response.json()["errors"]
        self.assertEqual(
            errors.pop(0)["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_warn_duplicate_file(self):
        """
        Tests that the system will warn of duplicate file upload
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 5)
        self.assertFalse(ImportFailure.objects.exists())

        # upload again
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 4)  # no additional purchases created
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(errors.pop(0)["message"], "Ce fichier a déjà été utilisé pour un import")
        self.assertEqual(body["count"], 0)
        self.assertTrue(body["duplicateFile"])
        self.assertEqual(len(body["duplicatePurchases"]), 4)
        self.assertEqual(body["duplicatePurchaseCount"], 4)

    @authenticate
    def test_errors_prevent_all_purchase_creation(self):
        """
        Tests that no purchases are created if there are any errors in the file
        even if certain lines are valid
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        # date format error
        file_path = "./api/tests/files/achats/purchases_bad_nearly_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors.pop(0)["message"],
            "La date doit être écrite sous la forme `aaaa-mm-jj`",
        )

        # unknown canteen error
        file_path = "./api/tests/files/achats/purchases_bad_nearly_good_2.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors.pop(0)["message"], "Une cantine avec le siret « 21730065600014 » n'existe pas sur la plateforme."
        )

        # not the canteen manager error
        CanteenFactory(siret="21730065600014")
        file_path = "./api/tests/files/achats/purchases_bad_nearly_good_2.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors.pop(0)["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")

    @authenticate
    def test_round_cents(self):
        """
        Cents should be rounded to the nearest two digits after the point
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_good_floating_number.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(Purchase.objects.first().price_ht, Decimal("90.11"))

    @authenticate
    def test_import_file_many_errors(self):
        """
        Test that all the errors are returned
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="36462492895701")

        file_path = "./api/tests/files/achats/purchases_bad_many_errors.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        self.assertEqual(len(body["errors"]), 12)
        self.assertEqual(body["errorCount"], 12)

    @authenticate
    def test_encoding_autodetect_windows1252(self):
        """
        Attempt to auto-detect file encodings: Windows 1252
        This is a smoke test - purchase import reuses diagnostics import
        More tests are with the diagnostic import tests
        """
        CanteenFactory(siret="96463820453707", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good_encoding_iso-8859-1.csv"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(f"{reverse('import_purchases')}", {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(Purchase.objects.first().description, "deuxième pomme")
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(body["encoding"], "ISO-8859-1")

    @authenticate
    def test_fail_import_bad_format(self):
        file_path = "./api/tests/files/achats/purchases_bad_file_format.ods"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(reverse("import_purchases"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        first_error = errors.pop(0)
        self.assertEqual(first_error["status"], 400)
        self.assertEqual(
            first_error["message"],
            "Ce fichier est au format application/vnd.oasis.opendocument.spreadsheet, merci d'exporter votre fichier au format CSV et réessayer.",
        )

    @authenticate
    def test_fail_import_bad_extension(self):
        file_path = "./api/tests/files/achats/purchases_bad_extension.txt"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        first_error = errors.pop(0)
        self.assertEqual(
            first_error["message"],
            "Ce fichier est au format text/plain, merci d'exporter votre fichier au format CSV et réessayer.",
        )

    @authenticate
    def test_import_with_empty_rows(self):
        """
        A file should not be valid if it contains empty rows (Validata)
        """
        file_path = "./api/tests/files/achats/purchases_bad_empty_rows.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(f"{reverse('import_purchases')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertTrue(
            errors.pop(0)["field"].startswith("ligne vide"),
        )
        self.assertEqual(Purchase.objects.count(), 0)
