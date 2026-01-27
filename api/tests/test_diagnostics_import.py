import json
from decimal import Decimal

from django.test.utils import override_settings
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase

from api.views.diagnostic_import import DIAGNOSTICS_SIMPLE_SCHEMA_FILE_PATH
from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic, ImportType, ImportFailure
from data.models.creation_source import CreationSource


class DiagnosticsSimpleSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_SIMPLE_SCHEMA_FILE_PATH))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test


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
        self.assertEqual(len(errors), 21)
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

    @authenticate
    def test_validata_header_extra_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Diagnostic.objects.count(), 0)

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

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_format.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("diagnostics_simple_import"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Diagnostic.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 10)
        # Missing required values
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[0]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[1]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[2]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[3]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[4]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[5]["message"])
        self.assertEqual("La valeur est obligatoire et doit être renseignée", errors[6]["message"])
        # Invalid number
        self.assertEqual(
            "La valeur ne doit comporter que des chiffres et le point comme séparateur décimal", errors[7]["message"]
        )
        self.assertTrue(errors[8]["message"].startswith("Le séparateur décimal à utiliser est le point"))
        # Unique SIRET
        self.assertEqual("Les valeurs de cette colonne doivent être uniques", errors[9]["message"])

    @freeze_time("2025-02-15")  # during the 2024 campaign
    @authenticate
    def test_model_validation_error(self):
        """
        Errors returned by model validation
        """
        # creating canteens
        CanteenFactory(siret="21340172201787", managers=[authenticate.user])
        CanteenFactory(siret="21380185500015", managers=[authenticate.user])
        CanteenFactory(siret="21670482500019", managers=[authenticate.user])
        CanteenFactory(siret="21640122400011", managers=[authenticate.user])
        CanteenFactory(siret="21630113500010", managers=[authenticate.user])
        CanteenFactory(siret="21130055300016", managers=[authenticate.user])
        CanteenFactory(siret="21730065600014", managers=[authenticate.user])
        CanteenFactory(siret="21590350100017", managers=[authenticate.user])
        CanteenFactory(siret="21010034300016", managers=[authenticate.user])
        CanteenFactory(siret="92341284500011", managers=[authenticate.user])
        CanteenFactory(siret="40419443300078", managers=[authenticate.user])
        CanteenFactory(siret="83014132100034", managers=[authenticate.user])
        CanteenFactory(siret="11007001800012", managers=[authenticate.user])
        CanteenFactory(siret="21070017500016", managers=[authenticate.user])
        # creating 2 canteens with same siret here to error when this situation exists IRL
        canteen_with_same_siret = CanteenFactory()
        canteen_with_same_siret.siret = "21340172201787"
        canteen_with_same_siret.save(skip_validations=True)
        self.assertEqual(Canteen.objects.count(), 15)
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
        self.assertEqual(len(errors), 17)
        self.assertEqual(errors[0]["row"], 2)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors.pop(0)["message"],
            # Note: if the line has other errors, they will not be raised...
            "Plusieurs cantines correspondent au SIRET 21340172201787. Veuillez enlever les doublons pour pouvoir créer le bilan.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'année' : L'année doit être comprise entre 2024 et 2026.",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : La valeur totale (HT), 1000, est moins que la valeur (HT) valeur_bio, 1500",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : La valeur totale (HT), 1000, est moins que la somme des valeurs d'approvisionnement, 1500",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : La valeur totale (HT), 1000, est moins que la somme des valeurs d'approvisionnement, 2000",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale annuelle HT' : La valeur totale (HT), 1000, est moins que la somme des valeurs d'approvisionnement pour le label france, 1600",
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
            "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques provenance France, 100, est plus que la valeur totale (HT) poissons et produits aquatiques, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            # TODO: is this the best field to point to as being wrong? hors bio could be confusing
            "Champ 'Produits SIQO (hors bio) - Valeur annuelle HT' : La somme des valeurs viandes et poissons EGalim, 300, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, 200",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Bio - Valeur annuelle HT' : La valeur (HT) bio dont commerce équitable, 150, est plus que la valeur totale (HT) bio, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) des autres achats EGalim' : La valeur (HT) achats commerce équitable (hors bio), 150, est plus que la valeur totale (HT) des autres achats EGalim, 50",
        )
        # Both totals meat are greater than the total return 2 errors
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, 60, est plus que la valeur totale (HT) viandes et volailles, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, 60, est plus que la valeur totale (HT) viandes et volailles, 50",
        )
        # Both totals meat are greater than the total return 2 errors
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques EGalim, 60, est plus que la valeur totale (HT) poissons et produits aquatiques, 50",
        )
        self.assertEqual(
            errors.pop(0)["message"],
            "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques provenance France, 60, est plus que la valeur totale (HT) poissons et produits aquatiques, 50",
        )
        self.assertEqual(len(errors), 0)

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

    @freeze_time("2025-02-10")  # during the 2024 campaign
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

    @freeze_time("2025-02-10")  # during the 2024 campaign
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
