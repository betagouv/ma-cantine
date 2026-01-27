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
from api.views.purchase_import import PURCHASE_SIRET_SCHEMA_FILE_PATH
from data.factories import CanteenFactory
from data.models import ImportFailure, ImportType
from data.models.creation_source import CreationSource
from data.models.purchase import Purchase


class PurchasesSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(PURCHASE_SIRET_SCHEMA_FILE_PATH))

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
        for VALUE_NOT_OK in ["", "TEST"]:
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
class PurchasesImportApiErrorTest(APITestCase):
    def test_unauthenticated(self):
        self.assertEqual(Purchase.objects.count(), 0)

        response = self.client.post(reverse("purchases_import"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Purchase.objects.count(), 0)

    @authenticate
    def test_validata_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # header missing
        file_path = "./api/tests/files/achats/purchases_bad_no_header.csv"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 8)
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

        # wrong header
        file_path = "./api/tests/files/achats/purchases_bad_wrong_header.csv"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 5)
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

        # partial header
        file_path = "./api/tests/files/achats/purchases_bad_partial_header.csv"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["field"],
            "Première ligne du fichier incorrecte",
        )
        self.assertEqual(
            errors[0]["title"],
            "Elle doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_validata_header_error_return_columns_correct_and_incorrect_values(self):
        """
        If a file has a wrong header we should display the incorrect and correct columns names
        """
        CanteenFactory(siret="99775491534896", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad_wrong_header_typo.csv"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 8)
        # siret
        self.assertEqual(errors[0]["field"], "colonne siret")
        self.assertEqual(errors[0]["title"], "Valeur incorrecte vous avez écrit « s_iret » au lieu de « siret »")
        # description
        self.assertEqual(errors[1]["field"], "colonne description")
        self.assertEqual(
            errors[1]["title"], "Valeur incorrecte vous avez écrit « description123 » au lieu de « description »"
        )
        # fournisseur
        self.assertEqual(errors[2]["field"], "colonne fournisseur")
        self.assertEqual(
            errors[2]["title"],
            "Valeur incorrecte vous avez écrit « fournisseur de la cantine » au lieu de « fournisseur »",
        )
        # date
        self.assertEqual(errors[3]["field"], "colonne date")
        self.assertEqual(errors[3]["title"], "Valeur incorrecte vous avez écrit « date! » au lieu de « date »")
        # prix
        self.assertEqual(errors[4]["field"], "colonne prix_ht")
        self.assertEqual(errors[4]["title"], "Valeur incorrecte vous avez écrit « prix ht » au lieu de « prix_ht »")
        # famille de produit
        self.assertEqual(errors[5]["field"], "colonne famille_produits")
        self.assertEqual(
            errors[5]["title"],
            "Valeur incorrecte vous avez écrit « famille de produits » au lieu de « famille_produits »",
        )
        # caractéristiques
        self.assertEqual(errors[6]["field"], "colonne caracteristiques")
        self.assertEqual(
            errors[6]["title"],
            "Valeur incorrecte vous avez écrit « caractéristiques » au lieu de « caracteristiques »",
        )
        # local
        self.assertEqual(errors[7]["field"], "colonne definition_local")
        self.assertEqual(
            errors[7]["title"],
            "Valeur incorrecte vous avez écrit « définition local » au lieu de « definition_local »",
        )

    @authenticate
    def test_validata_header_error_with_extra_columns(self):
        """
        A file should not be valid if it contains more columns
        """
        CanteenFactory(siret="99775491534896", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad_extra_columns.csv"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["field"],
            "4 colonnes supplémentaires",
        )
        self.assertEqual(
            errors[0]["title"],
            "Supprimer les 4 colonnes en excès et toutes les données présentes dans ces dernières. Il se peut qu'un espace ou un symbole invisible soit présent dans votre fichier, en cas de doute faite un copier-coller des données dans un nouveau document.",
        )

    @authenticate
    def test_validata_empty_rows_error(self):
        """
        A file should not be valid if it contains empty rows (Validata)
        """
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad_empty_rows.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("purchases_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 2)
        self.assertTrue(
            errors.pop(0)["field"].startswith("ligne vide"),
        )
        self.assertEqual(Purchase.objects.count(), 0)

    @authenticate
    def test_validata_format_error(self):
        """
        Errors returned by Validata
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="36462492895701")
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
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
        self.assertTrue(
            errors.pop(0)["message"].startswith(
                "La valeur ne doit comporter que des chiffres et le point comme séparateur décimal"
            )
        )
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
    def test_model_validation_error(self):
        """
        Errors returned by model validation
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad_no_local_definition.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'définition de local' : La caractéristique LOCAL est sélectionnée : le champ doit être rempli.",
        )

    @authenticate
    def test_canteen_not_found_with_siret(self):
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 5)
        self.assertEqual(
            errors.pop(0)["message"], "Une cantine avec le siret « 21010034300016 » n'existe pas sur la plateforme."
        )

    @authenticate
    def test_user_not_canteen_manager(self):
        CanteenFactory(siret="21010034300016")
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 5)
        self.assertEqual(errors.pop(0)["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=10)
    def test_file_above_max_size(self):
        """
        Test that the file is not treated if there are too many lines
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="36462492895701")
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )
        self.assertEqual(errors[0]["status"], 400)

    @authenticate
    def test_import_corrupt_purchases_file(self):
        """
        A reasonable error should be thrown
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_bad_corrupt.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(
            errors[0]["field"],
            "Première ligne du fichier incorrecte",
        )
        self.assertEqual(
            errors[0]["title"],
            "Elle doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )


class PurchasesImportApiSuccessTest(APITestCase):
    @authenticate
    def test_import_good_purchases(self):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 5)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 5)
        self.assertEqual(len(errors), 0, errors)
        self.assertIn("seconds", body)

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
        self.assertEqual(purchase.local_definition, None)
        # purchase with characteristics empty
        purchase = Purchase.objects.filter(description="Pommes, vertes 4").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.family, Purchase.Family.AUTRES)
        self.assertEqual(purchase.characteristics, [])
        # Test that the purchase import source contains the complete file digest
        filebytes = Path("./api/tests/files/achats/purchases_good.csv").read_bytes()
        filehash_md5 = hashlib.md5(filebytes).hexdigest()
        self.assertEqual(Purchase.objects.first().import_source, filehash_md5)

    @authenticate
    def test_import_good_purchases_with_empty_columns(self):
        """
        Tests that can import a purchases file with no characteristics or local definition
        """
        CanteenFactory(siret="65449096241683", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good_with_empty_columns.xlsx"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())

    @authenticate
    def test_import_comma_separated_numbers(self):
        """
        Tests that can import a file with comma-separated numbers
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good_separator_comma.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.price_ht, Decimal("90.11"))

    @authenticate
    def test_import_excel_file(self):
        """
        Tests that can import a file with comma-separated numbers
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good.xlsx"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges, local").first()
        self.assertEqual(purchase.price_ht, Decimal("90.11"))

    @authenticate
    def test_import_different_separators(self):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # tab
        file_path = "./api/tests/files/achats/purchases_good_separator_tab.tsv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())

        # semicolon
        file_path = "./api/tests/files/achats/purchases_good_separator_semicolon.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1 + 1)
        self.assertFalse(ImportFailure.objects.exists())

    @authenticate
    @override_settings(CSV_PURCHASE_CHUNK_LINES=1)
    @patch("api.views.PurchasesImportView._process_chunk")
    def test_import_batch_purchases(self, _process_chunk_mock):
        """
        Tests that actually split the file into chunks. The header is considered as a line.
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            _ = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(_process_chunk_mock.call_count, 5)

    @authenticate
    def test_warn_duplicate_file(self):
        """
        Tests that the system will warn of duplicate file upload
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # first upload: success
        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 5)
        self.assertFalse(ImportFailure.objects.exists())

        # second upload: duplicate warning
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 5)  # no additional purchases created
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(errors.pop(0)["message"], "Ce fichier a déjà été utilisé pour un import")
        self.assertEqual(body["count"], 0)
        self.assertTrue(body["duplicateFile"])
        self.assertEqual(len(body["duplicatePurchases"]), 5)
        self.assertEqual(body["duplicatePurchaseCount"], 5)

    @authenticate
    def test_round_cents(self):
        """
        Cents should be rounded to the nearest two digits after the point
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        file_path = "./api/tests/files/achats/purchases_good_floating_number.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("purchases_import"), {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(Purchase.objects.first().price_ht, Decimal("90.11"))
