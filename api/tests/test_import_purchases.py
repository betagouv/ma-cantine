import hashlib
from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory
from data.models.purchase import Purchase

from .utils import authenticate


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
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/good_purchase_import.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.canteen.siret, "82399356058716")
        self.assertEqual(purchase.description, "Pommes, rouges")
        self.assertEqual(purchase.provider, "Le bon traiteur")
        self.assertEqual(purchase.price_ht, Decimal("90.11"))
        self.assertEqual(purchase.date, date(2022, 5, 2))
        self.assertEqual(purchase.family, Purchase.Family.PRODUITS_LAITIERS)
        self.assertEqual(purchase.characteristics, [Purchase.Characteristic.BIO, Purchase.Characteristic.LOCAL])
        self.assertEqual(purchase.local_definition, Purchase.Local.DEPARTMENT)

        # Test that the purchase import source contains the complete file digest
        self.assertIsNotNone(purchase.import_source)
        filebytes = Path("./api/tests/files/good_purchase_import.csv").read_bytes()
        filehash_md5 = hashlib.md5(filebytes).hexdigest()
        self.assertEqual(Purchase.objects.first().import_source, filehash_md5)

    @authenticate
    def test_import_comma_separated_numbers(self):
        """
        Tests that can import a file with comma-separated numbers
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/comma_separated_purchase_import.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.price_ht, Decimal("90.11"))

    @authenticate
    def test_import_with_no_local_definition(self):
        """
        Tests that can import a file without local definition
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/good_purchase_import_no_local_def.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)
        purchase = Purchase.objects.filter(description="Pommes, rouges").first()
        self.assertEqual(purchase.canteen.siret, "82399356058716")
        self.assertEqual(purchase.description, "Pommes, rouges")
        self.assertEqual(purchase.provider, "Le bon traiteur")
        self.assertEqual(purchase.price_ht, Decimal("90.11"))
        self.assertEqual(purchase.date, date(2022, 5, 2))
        self.assertEqual(purchase.family, Purchase.Family.PRODUITS_LAITIERS)
        self.assertEqual(purchase.characteristics, [Purchase.Characteristic.BIO])
        self.assertEqual(purchase.local_definition, None)

    @authenticate
    def test_import_purchases_different_separators(self):
        """
        Tests that can import a well formatted purchases file
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/purchase_import_delimiter_tab.tsv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)

        with open("./api/tests/files/purchase_import_delimiter_semicolon.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)

    @authenticate
    @override_settings(CSV_PURCHASE_CHUNK_LINES=1)
    @patch("api.views.ImportPurchasesView._process_chunk")
    def test_import_batch_purchases(self, _process_chunk_mock):
        """
        Tests that actually split the file into chunks. The header is considered as a line.
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])

        with open("./api/tests/files/good_purchase_import.csv") as purchase_file:
            _ = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(_process_chunk_mock.call_count, 3)

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=10)
    def test_import_file_too_big(self):
        """
        Test that the file is not treated if there are too many lines
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        CanteenFactory.create(siret="36462492895701")
        with open("./api/tests/files/bad_purchase_import.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        errors = response.json()["errors"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )
        self.assertEqual(errors[0]["status"], 400)

    @authenticate
    def test_import_bad_purchases(self):
        """
        Test that the right errors are thrown
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        CanteenFactory.create(siret="36462492895701")
        with open("./api/tests/files/bad_purchase_import.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        errors = response.json()["errors"]
        self.assertEqual(errors.pop(0)["message"], "Champ 'siret' : Le siret de la cantine ne peut pas être vide")
        self.assertEqual(
            errors.pop(0)["message"], "Une cantine avec le siret « 86180597100897 » n'existe pas sur la plateforme."
        )
        self.assertEqual(errors.pop(0)["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")
        self.assertEqual(
            errors.pop(0)["message"], "Champ 'description du produit' : La description ne peut pas être vide"
        )
        self.assertEqual(errors.pop(0)["message"], "Champ 'fournisseur' : Le fournisseur ne peut pas être vide")
        self.assertEqual(errors.pop(0)["message"], "Champ 'date' : La date ne peut pas être vide")
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'date' : Le format de date de la valeur «\xa02022-02-31\xa0» est correct (AAAA-MM-JJ), mais la date n’est pas valide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'date' : Le format de date de la valeur «\xa02022/03/01\xa0» n’est pas valide. Le format correct est AAAA-MM-JJ.",
        )
        self.assertEqual(errors.pop(0)["message"], "Champ 'prix HT' : Le prix ne peut pas être vide")
        self.assertEqual(
            errors.pop(0)["message"], "Champ 'prix HT' : La valeur «\xa0A price\xa0» doit être un nombre décimal."
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'famille de produits' : La valeur «\xa0'NOPE'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'caractéristiques' : L'élément n°2 du tableau n’est pas valide\xa0: La valeur «\xa0'NOPE'\xa0» n’est pas un choix valide.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'définition de local' : La définition de local est obligatoire pour les produits locaux",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Format fichier : 7-8 colonnes attendues, 6 trouvées.",
        )

    @authenticate
    def test_import_corrupt_purchases_file(self):
        """
        A reasonable error should be thrown
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/corrupt_purchase_import.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        errors = response.json()["errors"]
        self.assertEqual(errors.pop(0)["message"], "Format fichier : 7-8 colonnes attendues, 1 trouvées.")

    @authenticate
    def test_warn_duplicate_file(self):
        """
        Tests that the system will warn of duplicate file upload
        """
        file_path = "./api/tests/files/good_purchase_import.csv"

        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 2)

        with open(file_path) as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(errors.pop(0)["message"], "Ce fichier a déjà été utilisé pour un import")
        self.assertEqual(body["count"], 0)
        self.assertTrue(body["duplicateFile"])
        self.assertEqual(len(body["duplicatePurchases"]), 2)
        self.assertEqual(body["duplicatePurchaseCount"], 2)

        # no additional purchases created
        self.assertEqual(Purchase.objects.count(), 2)

    @authenticate
    def test_errors_prevent_all_purchase_creation(self):
        """
        Tests that no purchases are created if there are any errors in the file
        even if certain lines are valid
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/nearly_good_purchase_import.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        body = response.json()
        self.assertEqual(len(body["errors"]), 1)

    @authenticate
    def test_round_cents(self):
        """
        Cents should be rounded to the nearest two digits after the point
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        with open("./api/tests/files/purchases_floating_number.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Purchase.objects.first().price_ht, Decimal("90.11"))

    @authenticate
    def test_import_file_many_errors(self):
        """
        Test that only the first errors are returned, but that the error count is correct
        """
        CanteenFactory.create(siret="82399356058716", managers=[authenticate.user])
        CanteenFactory.create(siret="36462492895701")
        with open("./api/tests/files/purchase_many_errors.csv") as purchase_file:
            response = self.client.post(reverse("import_purchases"), {"file": purchase_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 0)
        body = response.json()
        self.assertEqual(len(body["errors"]), 30)
        self.assertEqual(body["errorCount"], 56)

    @authenticate
    def test_encoding_autodetect_cp1252(self):
        """
        Attempt to auto-detect file encodings: Windows 1252
        This is a smoke test - purchase import reuses diagnostics import
        More tests are with the diagnostic import tests
        """
        canteen = CanteenFactory.create(siret="82399356058716")
        canteen.managers.add(authenticate.user)
        self.assertEqual(Purchase.objects.count(), 0)

        with open("./api/tests/files/purchase_encoding_iso-8859-1.csv", "rb") as diag_file:
            response = self.client.post(f"{reverse('import_purchases')}", {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Purchase.objects.first().description, "deuxième pomme")
        self.assertEqual(body["encoding"], "ISO-8859-1")
