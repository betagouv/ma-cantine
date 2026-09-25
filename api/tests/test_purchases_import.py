import hashlib
from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import skipIf
from unittest.mock import patch

import requests_mock
from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate, mock_validata_response
from data.factories import CanteenFactory
from data.models import ImportFailure, ImportType
from data.models.creation_source import CreationSource
from data.models.purchase import Purchase


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class PurchasesImportApiErrorTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("purchases_import")

    def test_cannot_import_if_unauthenticated(self):
        self.assertEqual(Purchase.objects.count(), 0)

        response = self.client.post(self.url, {"type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Purchase.objects.count(), 0)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_validata_header_error(self, mock):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # header missing
        mock_validata_response(mock, "purchases_bad_no_header.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_no_header.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 12)
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

        # wrong header
        mock_validata_response(mock, "purchases_bad_wrong_header.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_wrong_header.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

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
        mock_validata_response(mock, "purchases_bad_partial_header.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_partial_header.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

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

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_validata_header_error_return_columns_correct_and_incorrect_values(self, mock):
        """
        If a file has a wrong header we should display the incorrect and correct columns names
        """
        CanteenFactory(siret="99775491534896", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad_wrong_header_typo.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_wrong_header_typo.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 12)
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
        # categories egalim
        self.assertEqual(errors[6]["field"], "colonne categories_egalim")
        self.assertEqual(
            errors[6]["title"],
            "Valeur incorrecte vous avez écrit « catégories egalim » au lieu de « categories_egalim »",
        )
        # origine
        self.assertEqual(errors[7]["field"], "colonne origine")
        self.assertEqual(errors[7]["title"], "Valeur incorrecte vous avez écrit « Origine » au lieu de « origine »")
        # est_circuit_court
        self.assertEqual(errors[8]["field"], "colonne est_circuit_court")
        self.assertEqual(
            errors[8]["title"],
            "Valeur incorrecte vous avez écrit « circuit_court » au lieu de « est_circuit_court »",
        )
        # est_local
        self.assertEqual(errors[9]["field"], "colonne est_local")
        self.assertEqual(errors[9]["title"], "Valeur incorrecte vous avez écrit « local » au lieu de « est_local »")
        # definition_local
        self.assertEqual(errors[10]["field"], "colonne definition_local")
        self.assertEqual(
            errors[10]["title"],
            "Valeur incorrecte vous avez écrit « définition local » au lieu de « definition_local »",
        )
        # definition_local_km
        self.assertEqual(errors[11]["field"], "colonne definition_local_km")
        self.assertEqual(
            errors[11]["title"],
            "Valeur incorrecte vous avez écrit « distance » au lieu de « definition_local_km »",
        )

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_validata_header_error_with_extra_columns(self, mock):
        """
        A file should not be valid if it contains more columns
        """
        CanteenFactory(siret="99775491534896", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad_extra_columns.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_extra_columns.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

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

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_validata_empty_rows_error(self, mock):
        """
        A file should not be valid if it contains empty rows (Validata)
        """
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad_empty_rows.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_empty_rows.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

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

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_validata_format_error(self, mock):
        """
        Errors returned by Validata
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="36462492895701")
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 10)
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # siret
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # description
        self.assertEqual(
            errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée"
        )  # famille_produits
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # date
        self.assertEqual(
            errors.pop(0)["message"],
            "La date doit être écrite sous la forme `aaaa-mm-jj`",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "La date doit être écrite sous la forme `aaaa-mm-jj`",
        )
        self.assertEqual(errors.pop(0)["message"], "La valeur est obligatoire et doit être renseignée")  # prix_ht
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

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_price_not_number_error(self, mock):
        """
        A file should not be valid if the price is not a number
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad_one_error.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_one_error.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors.pop(0)["message"].endswith("doit être un nombre décimal."))

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_canteen_not_found_with_siret(self, mock):
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 8)
        self.assertEqual(
            errors.pop(0)["message"], "Une cantine avec le siret « 21010034300016 » n'existe pas sur la plateforme."
        )

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_user_not_canteen_manager(self, mock):
        CanteenFactory(siret="21010034300016")
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 8)
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
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

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

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_when_errors_count_is_0(self, mock):
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad_one_error.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_one_error.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertTrue(len(body["errors"]) > 0)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_corrupt_purchases_file(self, mock):
        """
        A reasonable error should be thrown
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_bad_corrupt.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_bad_corrupt.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

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


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class PurchasesImportApiSuccessTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("purchases_import")

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_good_purchases(self, mock):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 8)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 8)
        self.assertEqual(len(errors), 0, errors)
        self.assertIn("seconds", body)

        purchase = Purchase.objects.filter(description="Pommes, rouges, local").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.description, "Pommes, rouges, local")
        self.assertEqual(purchase.fournisseur, "Le bon traiteur")
        self.assertEqual(purchase.prix_ht, Decimal("90.11"))
        self.assertEqual(purchase.date, date(2022, 5, 2))
        self.assertEqual(purchase.famille_produits, Purchase.Family.PRODUITS_LAITIERS)
        self.assertEqual(purchase.caracteristiques, [Purchase.Characteristic.BIO, Purchase.Characteristic.LOCAL])
        self.assertEqual(purchase.definition_local, Purchase.Local.DEPARTEMENT)
        self.assertIsNotNone(purchase.import_source)
        self.assertEqual(purchase.creation_user, authenticate.user)
        self.assertEqual(purchase.creation_source, CreationSource.IMPORT)
        # purchase with characteristics empty
        purchase = Purchase.objects.filter(description="Pommes, vertes 1").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.famille_produits, Purchase.Family.AUTRES)
        self.assertEqual(purchase.caracteristiques, [])
        # purchase with characteristics RUP
        purchase = Purchase.objects.filter(description="Pommes, vertes 2").first()
        self.assertEqual(purchase.canteen.siret, "21010034300016")
        self.assertEqual(purchase.famille_produits, Purchase.Family.PRODUITS_LAITIERS)
        self.assertEqual(purchase.caracteristiques, [Purchase.Characteristic.RUP])
        # purchase with definition_local empty
        purchase = Purchase.objects.filter(description="Pommes, vertes 4").first()
        self.assertEqual(purchase.definition_local, "")
        # purchase with definition_local COMMUNE
        purchase = Purchase.objects.filter(description="Pommes, vertes 5").first()
        self.assertEqual(purchase.definition_local, Purchase.Local.COMMUNE)
        # purchase with definition_local KM
        purchase = Purchase.objects.filter(description="Pommes, vertes 6").first()
        self.assertEqual(purchase.definition_local, Purchase.Local.KM)
        self.assertEqual(purchase.definition_local_km, None)
        # purchase with definition_local KM & 200
        purchase = Purchase.objects.filter(description="Pommes, vertes 7").first()
        self.assertEqual(purchase.definition_local, Purchase.Local.KM)
        self.assertEqual(purchase.definition_local_km, 200)
        # Test that the purchase import source contains the complete file digest
        filebytes = Path("./api/tests/files/achats/purchases_good.csv").read_bytes()
        filehash_md5 = hashlib.md5(filebytes).hexdigest()
        self.assertEqual(Purchase.objects.first().import_source, filehash_md5)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_good_purchases_with_empty_columns(self, mock):
        """
        Tests that can import a purchases file with no characteristics or local definition
        """
        CanteenFactory(siret="65449096241683", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_with_empty_columns.xlsx", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_with_empty_columns.xlsx"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_number_decimal_point(self, mock):
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_separator_comma.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_separator_comma.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.prix_ht, Decimal("90.11"))

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_number_decimal_comma(self, mock):
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_decimal_comma.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_decimal_comma.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.prix_ht, Decimal("90.11"))

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_excel_file(self, mock):
        """
        Tests that can import a file with Excel format
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good.xlsx", category="achats")
        file_path = "./api/tests/files/achats/purchases_good.xlsx"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges, local").first()
        self.assertEqual(purchase.prix_ht, Decimal("90.11"))

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_excel_file_number_decimal_comma(self, mock):
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_decimal_comma.xlsx", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_decimal_comma.xlsx"
        with open(file_path, "rb") as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges, local").first()
        self.assertEqual(purchase.prix_ht, Decimal("90.11"))

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_different_separators(self, mock):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # comma
        mock_validata_response(mock, "purchases_good_separator_comma.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_separator_comma.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())

        # tab
        mock_validata_response(mock, "purchases_good_separator_tab.tsv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_separator_tab.tsv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1 + 1)
        self.assertFalse(ImportFailure.objects.exists())

        # semicolon
        mock_validata_response(mock, "purchases_good_separator_semicolon.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_separator_semicolon.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2 + 1)
        self.assertFalse(ImportFailure.objects.exists())

    @requests_mock.Mocker(real_http=True)
    @authenticate
    @override_settings(CSV_PURCHASE_CHUNK_LINES=1)
    @patch("api.views.PurchasesImportView._process_chunk")
    def test_import_batch_purchases(self, mock, _process_chunk_mock):
        """
        Tests that actually split the file into chunks. The header is considered as a line.
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])

        mock_validata_response(mock, "purchases_good.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            _ = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(_process_chunk_mock.call_count, 8)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_warn_duplicate_file(self, mock):
        """
        Tests that the system will warn of duplicate file upload
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        # first upload: success
        mock_validata_response(mock, "purchases_good.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 8)
        self.assertFalse(ImportFailure.objects.exists())

        # second upload: duplicate warning
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 8)  # no additional purchases created
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(errors.pop(0)["message"], "Ce fichier a déjà été utilisé pour un import")
        self.assertEqual(body["count"], 0)
        self.assertTrue(body["duplicateFile"])
        self.assertEqual(len(body["duplicatePurchases"]), 8)
        self.assertEqual(body["duplicatePurchaseCount"], 8)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_round_cents(self, mock):
        """
        Cents should be rounded to the nearest two digits after the point
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_floating_number.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_floating_number.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(Purchase.objects.first().prix_ht, Decimal("90.11"))

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_local_and_circuit_court_independent(self, mock):
        """
        Tests that can import a file can be local or circuit court independently.
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_local_vs_circuit_court.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_local_vs_circuit_court.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())

        only_local = Purchase.objects.filter(description="Only local").first()
        self.assertIn(Purchase.Characteristic.LOCAL, only_local.caracteristiques)
        self.assertNotIn(Purchase.Characteristic.CIRCUIT_COURT, only_local.caracteristiques)
        self.assertEqual(only_local.definition_local, "DEPARTEMENT")

        only_cc = Purchase.objects.filter(description="Only circuit court").first()
        self.assertIn(Purchase.Characteristic.CIRCUIT_COURT, only_cc.caracteristiques)
        self.assertNotIn(Purchase.Characteristic.LOCAL, only_cc.caracteristiques)
        self.assertEqual(only_cc.definition_local, "")

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_siret_separated_caracteristics(self, mock):
        """
        Tests that can import a file with the caracteristics split into:
        - categories_egalim
        - origine
        - est_circuit_court
        - est_local
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_siret_caracteristics.csv", category="achats")
        file_path = "./api/tests/files/achats/purchases_good_siret_caracteristics.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(errors), 0, errors)

        purchase_1 = Purchase.objects.filter(description="Pomme 1").first()
        self.assertEqual(purchase_1.canteen.siret, "21010034300016")
        self.assertEqual(purchase_1.prix_ht, Decimal("100.00"))
        self.assertEqual(purchase_1.famille_produits, Purchase.Family.AUTRES)
        self.assertIn(Purchase.Characteristic.BIO, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.COMMERCE_EQUITABLE, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.LOCAL, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.FRANCE, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.CIRCUIT_COURT, purchase_1.caracteristiques)
        self.assertEqual(purchase_1.definition_local, "REGION")

        purchase_2 = Purchase.objects.filter(description="Pomme 2").first()
        self.assertEqual(purchase_2.canteen.siret, "21010034300016")
        self.assertEqual(purchase_2.prix_ht, Decimal("200.00"))
        self.assertEqual(purchase_2.famille_produits, Purchase.Family.AUTRES)
        self.assertIn(Purchase.Characteristic.BIO, purchase_2.caracteristiques)
        self.assertIn(Purchase.Characteristic.COMMERCE_EQUITABLE, purchase_2.caracteristiques)
        self.assertNotIn(Purchase.Characteristic.CIRCUIT_COURT, purchase_2.caracteristiques)
        self.assertEqual(purchase_2.definition_local, "")


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class PurchasesImportIdApiErrorTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("purchases_import")

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_canteen_not_found_with_id(self, mock):
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_id.csv", category="achats_id")
        file_path = "./api/tests/files/achats/purchases_good_id.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.PURCHASE_ID, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors.pop(0)["message"], "Une cantine avec l'id « 949 » n'existe pas sur la plateforme.")


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class PurchasesImportIdApiSuccessTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("purchases_import")

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_default_type_is_id(self, mock):
        """
        Tests that if no type is provided, the default import type is id
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user], id=949)
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_id.csv", category="achats_id")
        file_path = "./api/tests/files/achats/purchases_good_id.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_with_canteen_id(self, mock):
        """
        Tests that can import a file with id instead of siret
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user], id=949)
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_id.csv", category="achats_id")
        file_path = "./api/tests/files/achats/purchases_good_id.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.prix_ht, Decimal("90.11"))
        self.assertEqual(purchase.canteen.id, 949)

    @requests_mock.Mocker(real_http=True)
    @authenticate
    def test_import_id_separated_caracteristics(self, mock):
        """
        Tests that can import a file with the caracteristics split into:
        - categories_egalim
        - origine
        - est_circuit_court
        - est_local
        """
        CanteenFactory(siret="21010034300016", managers=[authenticate.user], id=949)
        self.assertEqual(Purchase.objects.count(), 0)

        mock_validata_response(mock, "purchases_good_id_caracteristics.csv", category="achats_id")
        file_path = "./api/tests/files/achats/purchases_good_id_caracteristics.csv"
        with open(file_path) as purchase_file:
            response = self.client.post(self.url, {"file": purchase_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(errors), 0, errors)

        purchase_1 = Purchase.objects.filter(description="Pomme 1").first()
        self.assertEqual(purchase_1.prix_ht, Decimal("100.00"))
        self.assertEqual(purchase_1.famille_produits, Purchase.Family.AUTRES)
        self.assertIn(Purchase.Characteristic.BIO, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.COMMERCE_EQUITABLE, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.LOCAL, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.FRANCE, purchase_1.caracteristiques)
        self.assertIn(Purchase.Characteristic.CIRCUIT_COURT, purchase_1.caracteristiques)
        self.assertEqual(purchase_1.definition_local, "REGION")

        purchase_2 = Purchase.objects.filter(description="Pomme 2").first()
        self.assertEqual(purchase_2.prix_ht, Decimal("200.00"))
        self.assertEqual(purchase_2.famille_produits, Purchase.Family.AUTRES)
        self.assertIn(Purchase.Characteristic.BIO, purchase_2.caracteristiques)
        self.assertIn(Purchase.Characteristic.COMMERCE_EQUITABLE, purchase_2.caracteristiques)
        self.assertNotIn(Purchase.Characteristic.CIRCUIT_COURT, purchase_2.caracteristiques)
        self.assertEqual(purchase_2.definition_local, "")
