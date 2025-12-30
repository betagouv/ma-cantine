import datetime
from decimal import Decimal

from django.test.utils import override_settings
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic, ImportType, ImportFailure
from data.models.creation_source import CreationSource

NEXT_YEAR = datetime.date.today().year + 1


class DiagnosticsSimpleImportApiErrorTest(APITestCase):
    def test_unauthenticated(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        response = self.client.post(reverse("diagnostics_simple_import"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Diagnostic.objects.count(), 0)

    @authenticate
    def test_validata_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Diagnostic.objects.count(), 0)

        # header missing
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_no_header.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

        # wrong header
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_wrong_header.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

        # partial header
        # TODO

    @authenticate
    def test_validata_empty_rows_error(self):
        """
        A file should not be valid if it contains empty rows (Validata)
        """
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_empty_rows.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(
            errors.pop(0)["field"].startswith("ligne vide"),
        )

    @authenticate
    def test_validata_format_error(self):
        """
        Errors returned by Validata
        """
        # creating canteens
        CanteenFactory(siret="50044221500025", managers=[authenticate.user])
        CanteenFactory(siret="82821513700013", managers=[authenticate.user])
        CanteenFactory(siret="82217035300012", managers=[authenticate.user])
        CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        CanteenFactory(siret="90930179110860", managers=[authenticate.user])
        CanteenFactory(siret="73282932000074", managers=[authenticate.user])
        CanteenFactory(siret="82938781909454", managers=[authenticate.user])
        CanteenFactory(siret="15952607273997", managers=[authenticate.user])
        CanteenFactory(siret="42111303053388", managers=[authenticate.user])
        self.assertEqual(Canteen.objects.count(), 9)
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_format.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 11)
        # Invalid year
        self.assertEqual(errors[0]["field"], "année_bilan")
        self.assertTrue(errors[0]["message"].startswith("L'année doit être composée de 4 chiffres"))
        # Missing required values
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[1]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[2]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[3]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[4]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[5]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[6]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[7]["message"])
        # Invalid number
        self.assertEqual(
            "La valeur ne doit comporter que des chiffres et le point comme séparateur décimal", errors[8]["message"]
        )
        self.assertTrue(errors[9]["message"].startswith("Le séparateur décimal à utiliser est le point"))
        # Unique SIRET
        self.assertEqual("Les valeurs de cette colonne doivent être uniques", errors[10]["message"])

    @authenticate
    def test_model_validation_error(self):
        """
        Errors returned by model validation
        """
        # creating canteens
        CanteenFactory(siret="50044221500025", managers=[authenticate.user])
        CanteenFactory(siret="82821513700013", managers=[authenticate.user])
        CanteenFactory(siret="82217035300012", managers=[authenticate.user])
        CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        CanteenFactory(siret="90930179110860", managers=[authenticate.user])
        CanteenFactory(siret="73282932000074", managers=[authenticate.user])
        # creating 2 canteens with same siret here to error when this situation exists IRL
        CanteenFactory(siret="42111303053388", managers=[authenticate.user])
        canteen_with_same_siret = CanteenFactory()
        Canteen.objects.filter(id=canteen_with_same_siret.id).update(siret="42111303053388")

        self.assertEqual(Canteen.objects.count(), 8)
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 7)
        self.assertEqual(errors[0]["row"], 2)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors.pop(0)["message"],
            f"Champ 'année' : L'année doit être comprise entre 2019 et {NEXT_YEAR}.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : La somme des valeurs d'approvisionnement, 300, est plus que le total, 20",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Plusieurs cantines correspondent au SIRET 42111303053388. Veuillez enlever les doublons pour pouvoir créer le bilan.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, 100, est plus que la valeur totale (HT) viandes et volailles, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, 100, est plus que la valeur totale (HT) viandes et volailles, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques EGalim, 100, est plus que la valeur totale (HT) poissons et produits aquatiques, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            # TODO: is this the best field to point to as being wrong? hors bio could be confusing
            "Champ 'Produits SIQO (hors bio) - Valeur annuelle HT' : La somme des valeurs viandes et poissons EGalim, 300, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, 200",
        )

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    def test_file_above_max_size(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(
            errors.pop(0)["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )

    @authenticate
    def test_file_bad_format(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_file_format.ods"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertIn("Une erreur inconnue", errors[0]["message"])

    @authenticate
    def test_update_diagnostic_teledeclared(self):
        """
        If a diagnostic with a valid TD already exists for the canteen, throw an error
        If the TD is cancelled, allow update
        """
        date_in_2024_teledeclaration_campaign = "2025-01-30"
        canteen = CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=1, valeur_bio=0.2)

        with freeze_time(date_in_2024_teledeclaration_campaign):
            diagnostic.teledeclare(applicant=authenticate.user)

            file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_one_canteen.csv"
            with open(file_path) as diag_file:
                response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            body = response.json()
            errors = body["errors"]
            self.assertEqual(body["count"], 0)
            self.assertEqual(
                errors[0]["message"],
                "Ce n'est pas possible de modifier un diagnostic télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration.",
            )
            self.assertEqual(diagnostic.valeur_totale, 1)

            # now test cancelled TD
            diagnostic.cancel()
            with open(file_path) as diag_file:
                response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            body = response.json()
            errors = body["errors"]
            self.assertEqual(body["count"], 1)
            self.assertEqual(len(errors), 0, errors)

            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.valeur_totale, 1000)

    @authenticate
    def test_canteen_not_found_with_siret(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_one_canteen.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(
            errors[0]["message"],
            "Une cantine avec le siret « 21340172201787 » n'existe pas sur la plateforme.",
        )

    @authenticate
    def test_user_not_canteen_manager(self):
        CanteenFactory(siret="21340172201787", managers=[])
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_one_canteen.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(errors[0]["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")


class DiagnosticsSimpleImportApiSuccessTest(APITestCase):
    @authenticate
    def test_diagnostics_created(self):
        """
        Given valid data, multiple diagnostics are created for multiple canteens,
        the authenticated user is added as the manager
        """
        siret_canteen_1 = "21340172201787"
        siret_canteen_2 = "73282932000074"
        canteen_1 = CanteenFactory(siret=siret_canteen_1, managers=[authenticate.user])
        canteen_2 = CanteenFactory(siret=siret_canteen_2, managers=[authenticate.user])
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(errors), 0, errors)
        self.assertIn("seconds", body)

        diagnostic_1 = Diagnostic.objects.get(canteen_id=canteen_1.id)
        self.assertEqual(diagnostic_1.year, 2024)
        self.assertEqual(diagnostic_1.valeur_totale, 1000)
        self.assertEqual(diagnostic_1.valeur_bio, 500)
        self.assertEqual(diagnostic_1.valeur_bio_dont_commerce_equitable, 250)
        self.assertEqual(diagnostic_1.valeur_siqo, Decimal("100.1"))
        self.assertEqual(diagnostic_1.valeur_externalites_performance, 10)
        self.assertEqual(diagnostic_1.valeur_egalim_autres, 20)
        self.assertEqual(diagnostic_1.valeur_egalim_autres_dont_commerce_equitable, 15)
        self.assertEqual(diagnostic_1.valeur_viandes_volailles, 2)
        self.assertEqual(diagnostic_1.valeur_viandes_volailles_egalim, 1)
        self.assertEqual(diagnostic_1.valeur_viandes_volailles_france, 1)
        self.assertEqual(diagnostic_1.valeur_produits_de_la_mer, 3)
        self.assertEqual(diagnostic_1.valeur_produits_de_la_mer_egalim, 1)
        self.assertEqual(diagnostic_1.valeur_produits_de_la_mer_france, 1)
        self.assertEqual(diagnostic_1.valeur_fruits_et_legumes_france, Decimal("1.1"))
        self.assertEqual(diagnostic_1.valeur_charcuterie_france, Decimal("1.2"))
        self.assertEqual(diagnostic_1.valeur_produits_laitiers_france, Decimal("1.3"))
        self.assertEqual(diagnostic_1.valeur_boulangerie_france, Decimal("1.4"))
        self.assertEqual(diagnostic_1.valeur_boissons_france, Decimal("1.5"))
        self.assertEqual(diagnostic_1.valeur_autres_france, Decimal("1.6"))
        self.assertEqual(diagnostic_1.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
        self.assertEqual(diagnostic_1.creation_source, CreationSource.IMPORT)

        diagnostic_2 = Diagnostic.objects.get(canteen_id=canteen_2.id)
        self.assertEqual(diagnostic_2.year, 2024)
        self.assertEqual(diagnostic_2.valeur_totale, 200)
        self.assertEqual(diagnostic_2.valeur_bio, 0)
        self.assertEqual(diagnostic_2.valeur_bio_dont_commerce_equitable, 0)
        self.assertEqual(diagnostic_2.valeur_siqo, 0)
        self.assertEqual(diagnostic_2.valeur_externalites_performance, 0)
        self.assertEqual(diagnostic_2.valeur_egalim_autres, 0)
        self.assertEqual(diagnostic_2.valeur_egalim_autres_dont_commerce_equitable, 0)
        self.assertEqual(diagnostic_2.valeur_viandes_volailles, 0)
        self.assertEqual(diagnostic_2.valeur_viandes_volailles_egalim, 0)
        self.assertEqual(diagnostic_2.valeur_viandes_volailles_france, None)
        self.assertEqual(diagnostic_2.valeur_produits_de_la_mer, 0)
        self.assertEqual(diagnostic_2.valeur_produits_de_la_mer_egalim, 0)
        self.assertEqual(diagnostic_2.valeur_produits_de_la_mer_france, None)
        self.assertEqual(diagnostic_2.valeur_fruits_et_legumes_france, None)
        self.assertEqual(diagnostic_2.valeur_charcuterie_france, None)
        self.assertEqual(diagnostic_2.valeur_produits_laitiers_france, None)
        self.assertEqual(diagnostic_2.valeur_boulangerie_france, None)
        self.assertEqual(diagnostic_2.valeur_boissons_france, None)
        self.assertEqual(diagnostic_2.valeur_autres_france, None)
        self.assertEqual(diagnostic_2.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
        self.assertEqual(diagnostic_2.creation_source, CreationSource.IMPORT)

    @authenticate
    def test_diagnostics_created_excel_file(self):
        canteen = CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good.xlsx"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        diagnostic_1 = Diagnostic.objects.get(canteen_id=canteen.id)
        self.assertEqual(diagnostic_1.year, 2024)
        self.assertEqual(diagnostic_1.valeur_totale, 1000)
        self.assertEqual(diagnostic_1.valeur_bio, 500)
        self.assertEqual(diagnostic_1.valeur_bio_dont_commerce_equitable, 250)
        self.assertEqual(diagnostic_1.valeur_siqo, Decimal("100.1"))
        self.assertEqual(diagnostic_1.valeur_externalites_performance, 10)
        self.assertEqual(diagnostic_1.valeur_egalim_autres, 20)
        self.assertEqual(diagnostic_1.valeur_egalim_autres_dont_commerce_equitable, 15)
        self.assertEqual(diagnostic_1.valeur_viandes_volailles, 2)
        self.assertEqual(diagnostic_1.valeur_viandes_volailles_egalim, 1)
        self.assertEqual(diagnostic_1.valeur_viandes_volailles_france, 1)
        self.assertEqual(diagnostic_1.valeur_produits_de_la_mer, 3)
        self.assertEqual(diagnostic_1.valeur_produits_de_la_mer_egalim, 1)
        self.assertEqual(diagnostic_1.valeur_produits_de_la_mer_france, 1)
        self.assertEqual(diagnostic_1.valeur_fruits_et_legumes_france, Decimal("1.1"))
        self.assertEqual(diagnostic_1.valeur_charcuterie_france, Decimal("1.2"))
        self.assertEqual(diagnostic_1.valeur_produits_laitiers_france, Decimal("1.3"))
        self.assertEqual(diagnostic_1.valeur_boulangerie_france, Decimal("1.4"))
        self.assertEqual(diagnostic_1.valeur_boissons_france, Decimal("1.5"))
        self.assertEqual(diagnostic_1.valeur_autres_france, Decimal("1.6"))
        self.assertEqual(diagnostic_1.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
        self.assertEqual(diagnostic_1.creation_source, CreationSource.IMPORT)

    @authenticate
    def test_update_existing_diagnostic(self):
        """
        If a diagnostic already exists for the canteen,
        update the diag with data from import file
        """
        canteen = CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=1, valeur_bio=0.2)

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_one_canteen.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.valeur_totale, 1000)
        self.assertEqual(diagnostic.valeur_bio, 500)
