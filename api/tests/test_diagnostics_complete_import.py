import json
from unittest import skipIf

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.conf import settings
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from api.views.diagnostic_import import DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic, ImportFailure, ImportType
from data.models.creation_source import CreationSource


class DiagnosticsCompleteSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class DiagnosticsCompleteImportApiErrorTest(APITestCase):
    def test_unauthenticated(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        response = self.client.post(reverse("diagnostics_complete_import"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Diagnostic.objects.count(), 0)

    @authenticate
    def test_validata_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Diagnostic.objects.count(), 0)

        # header missing
        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_bad_no_header.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_COMPLETE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 125)  # len(schema["fields"])
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

    @authenticate
    def test_validata_header_extra_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Diagnostic.objects.count(), 0)

        # wrong header
        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_bad_wrong_header.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_COMPLETE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "3 colonnes supplémentaires")
        self.assertEqual(
            errors[0]["title"],
            "Supprimer les 3 colonnes en excès et toutes les données présentes dans ces dernières. Il se peut qu'un espace ou un symbole invisible soit présent dans votre fichier, en cas de doute faite un copier-coller des données dans un nouveau document.",
        )

    @authenticate
    def test_validata_empty_rows_error(self):
        """
        A file should not be valid if it contains empty rows (Validata)
        """
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_bad_empty_rows.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_COMPLETE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(
            errors[0]["field"].startswith("ligne vide"),
        )

    @authenticate
    def test_validata_format_error(self):
        """
        Errors returned by Validata
        """
        # creating canteens
        CanteenFactory(siret="82821513700013", managers=[authenticate.user])
        CanteenFactory(siret="82217035300012", managers=[authenticate.user])
        CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        CanteenFactory(siret="90930179110860", managers=[authenticate.user])
        CanteenFactory(siret="73282932000074", managers=[authenticate.user])
        CanteenFactory(siret="82938781909454", managers=[authenticate.user])
        CanteenFactory(siret="15952607273997", managers=[authenticate.user])
        CanteenFactory(siret="42111303053388", managers=[authenticate.user])
        self.assertEqual(Canteen.objects.count(), 8)
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_bad_format.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_COMPLETE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 10)
        # Missing required values
        self.assertEqual(errors[0]["field"], "année_bilan")
        self.assertEqual(errors[0]["message"], "La valeur est obligatoire et doit être renseignée")
        self.assertEqual(errors[1]["field"], "valeur_totale")
        self.assertEqual(errors[1]["message"], "La valeur est obligatoire et doit être renseignée")
        self.assertEqual(errors[2]["field"], "valeur_viandes_volailles")
        self.assertEqual(errors[2]["message"], "La valeur est obligatoire et doit être renseignée")
        self.assertEqual(errors[3]["field"], "valeur_viandes_volailles_bio")
        self.assertEqual(errors[3]["message"], "La valeur est obligatoire et doit être renseignée")
        self.assertEqual(errors[4]["field"], "valeur_produits_de_la_mer_bio")
        self.assertEqual(errors[4]["message"], "La valeur est obligatoire et doit être renseignée")
        self.assertEqual(errors[5]["field"], "valeur_fruits_et_legumes_bio")
        self.assertEqual(errors[5]["message"], "La valeur est obligatoire et doit être renseignée")
        self.assertEqual(errors[6]["field"], "siret")
        self.assertEqual(errors[6]["message"], "La valeur est obligatoire et doit être renseignée")
        # Invalid number
        self.assertEqual(errors[7]["field"], "valeur_totale")
        self.assertEqual(
            errors[7]["message"], "La valeur ne doit comporter que des chiffres et le point comme séparateur décimal"
        )
        self.assertEqual(errors[8]["field"], "valeur_totale")
        self.assertTrue(errors[8]["message"].startswith("Le séparateur décimal à utiliser est le point"))
        # Unique SIRET
        self.assertEqual(errors[9]["field"], "siret")
        self.assertEqual(errors[9]["message"], "Les valeurs de cette colonne doivent être uniques")

    @freeze_time("2025-02-15")  # during the 2024 campaign
    @authenticate
    def test_model_validation_error(self):
        # TODO: update diagnostics_complete_bad.csv and add tests
        pass

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    def test_file_above_max_size(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_good_different_canteens.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_COMPLETE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(
            errors[0]["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )

    @authenticate
    def test_file_bad_format(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_bad_file_format.ods"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

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

            file_path = (
                "./api/tests/files/diagnostics_complete/diagnostics_complete_good_one_canteen_seperator_semicolon.csv"
            )
            with open(file_path) as diag_file:
                response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            body = response.json()
            errors = body["errors"]
            self.assertEqual(body["count"], 0)
            self.assertEqual(
                errors[0]["message"],
                "Ce n'est pas possible de modifier un bilan télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration.",
            )
            self.assertEqual(diagnostic.valeur_totale, 1)

            # now test cancelled TD
            diagnostic.cancel()
            with open(file_path) as diag_file:
                response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            body = response.json()
            errors = body["errors"]
            self.assertEqual(body["count"], 1)
            self.assertEqual(len(errors), 0, errors)

            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.valeur_totale, 2000)

    @authenticate
    def test_canteen_not_found_with_siret(self):
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = (
            "./api/tests/files/diagnostics_complete/diagnostics_complete_good_one_canteen_seperator_semicolon.csv"
        )
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

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

        file_path = (
            "./api/tests/files/diagnostics_complete/diagnostics_complete_good_one_canteen_seperator_semicolon.csv"
        )
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(errors[0]["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")

    @authenticate
    def test_when_errors_count_is_0(self):
        CanteenFactory(siret="21340172201787", managers=[authenticate.user])

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_bad_one_error.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file, "type": "siret"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertTrue(len(body["errors"]) > 0)


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class DiagnosticsCompleteImportApiSuccessTest(APITestCase):
    @freeze_time("2025-02-10")  # during the 2024 campaign
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

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_good_different_canteens.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

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
        self.assertEqual(diagnostic_1.valeur_totale, 2000)
        # TODO: add more assertions with Decimal
        self.assertEqual(diagnostic_1.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(diagnostic_1.creation_source, CreationSource.IMPORT)

        diagnostic_2 = Diagnostic.objects.get(canteen_id=canteen_2.id)
        self.assertEqual(diagnostic_2.year, 2024)
        self.assertEqual(diagnostic_2.valeur_totale, 200)
        # TODO: add more assertions with Decimal & None
        self.assertEqual(diagnostic_2.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(diagnostic_2.creation_source, CreationSource.IMPORT)

    @freeze_time("2025-02-10")  # during the 2024 campaign
    @authenticate
    def test_diagnostics_created_excel_file(self):
        canteen = CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.count(), 0)

        file_path = "./api/tests/files/diagnostics_complete/diagnostics_complete_good.xlsx"
        with open(file_path, "rb") as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        diagnostic_1 = Diagnostic.objects.get(canteen_id=canteen.id)
        self.assertEqual(diagnostic_1.year, 2024)
        self.assertEqual(diagnostic_1.valeur_totale, 2000)
        # TODO: add more assertions with Decimal
        self.assertEqual(diagnostic_1.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(diagnostic_1.creation_source, CreationSource.IMPORT)

    @freeze_time("2025-02-10")  # during the 2024 campaign
    @authenticate
    def test_update_existing_diagnostic(self):
        """
        If a diagnostic already exists for the canteen,
        update the diag with data from import file
        """
        canteen = CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=1000, valeur_bio=200)

        file_path = (
            "./api/tests/files/diagnostics_complete/diagnostics_complete_good_one_canteen_seperator_semicolon.csv"
        )
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)

        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.valeur_totale, 2000)
        self.assertEqual(diagnostic.valeur_bio, 400)

    @authenticate
    def test_update_diagnostic_cancelled_during_correction_campaign(self):
        """
        If a canteen has a cancelled diagnostic,
        it can import a new diagnostic during the correction campaign
        """
        canteen = CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=1000, valeur_bio=200)

        with freeze_time("2025-01-20"):  # during the 2024 campaign
            diagnostic.teledeclare(applicant=authenticate.user)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            diagnostic.cancel()

            file_path = (
                "./api/tests/files/diagnostics_complete/diagnostics_complete_good_one_canteen_seperator_semicolon.csv"
            )
            with open(file_path) as diag_file:
                response = self.client.post(reverse("diagnostics_complete_import"), {"file": diag_file})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.valeur_totale, 2000)
            self.assertEqual(diagnostic.valeur_bio, 400)
