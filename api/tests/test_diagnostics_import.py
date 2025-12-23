import datetime
from decimal import Decimal

from django.test.utils import override_settings
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic, ImportType
from data.models.creation_source import CreationSource

NEXT_YEAR = datetime.date.today().year + 1


class DiagnosticsSimpleImportApiTest(APITestCase):
    def test_unauthenticated_import_call(self):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_diagnostics_simple"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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

        with open("./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics_simple"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        self.assertEqual(body["errorCount"], 0)
        self.assertEqual(Diagnostic.objects.count(), 2)

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
        self.assertIn("seconds", body)

    # @authenticate
    # def test_validata_errors(self ):
    #   siret
    #   année
    #   autre champs obligatoire
    #   champs avec un text au lieu d'un nombre attendu

    @authenticate
    def test_error_collection(self):
        """
        If errors occur, discard the file and return the errors with row and message
        """
        # creating 2 canteens with same siret here to error when this situation exists IRL
        CanteenFactory(siret="42111303053388")
        canteen_with_same_siret = CanteenFactory()
        Canteen.objects.filter(id=canteen_with_same_siret.id).update(siret="42111303053388")

        file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("import_diagnostics_simple"), {"file": diag_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)

        body = response.json()
        # no new objects should have been saved to the DB since it failed
        self.assertEqual(body["count"], 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        errors = body["errors"]
        self.assertEqual(len(errors), 7, errors)
        self.assertEqual(errors[0]["row"], 1)
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
            "Plusieurs cantines correspondent au SIRET 42111303053388. Veuillez enlever les doublons pour pouvoir créer le diagnostic.",
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
    def test_diagnostic_no_header(self):
        """
        A file should not be valid if doesn't contain a valid header
        """
        with open("./api/tests/files/diagnostics/diagnostics_simple_bad_no_header.csv") as diag_file:
            response = self.client.post(reverse("import_diagnostics_simple"), {"file": diag_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    @authenticate
    def test_max_size(self):
        file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv"
        with open(file_path) as diag_file:
            response = self.client.post(reverse("import_diagnostics_simple"), {"file": diag_file})
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
    def test_import_wrong_header(self):

        with open("./api/tests/files/diagnostics/diagnostics_simple_bad_wrong_header.csv") as diag_file:
            response = self.client.post(f"{reverse('import_diagnostics_simple')}", {"file": diag_file})
        body = response.json()

        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    # @authenticate
    # def test_update_existing_diagnostic(self, mock):
    #     """
    #     If a diagnostic already exists for the canteen, update the diag and canteen
    #     with data in import file
    #     """
    #     canteen = CanteenFactory(siret="21340172201787", name="Old name", managers=[authenticate.user])
    #     diagnostic = DiagnosticFactory(canteen=canteen, year=2021, valeur_totale=1, valeur_bio=0.2)

    #     with open("./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv") as diag_file:
    #         response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     body = response.json()
    #     self.assertEqual(len(body["errors"]), 0)
    #     canteen.refresh_from_db()
    #     self.assertEqual(canteen.name, "A canteen")
    #     diagnostic.refresh_from_db()
    #     self.assertEqual(diagnostic.valeur_totale, 1000)

    # @authenticate
    # def test_update_diagnostic_conditional_on_teledeclaration_status(self, mock):
    #     """
    #     If a diagnostic with a valid TD already exists for the canteen, throw an error
    #     If the TD is cancelled, allow update
    #     """
    #     date_in_2022_teledeclaration_campaign = "2022-08-30"
    #     canteen = CanteenFactory(siret="21340172201787", name="Old name", managers=[authenticate.user])
    #     diagnostic = DiagnosticFactory(canteen=canteen, year=2021, valeur_totale=1, valeur_bio=0.2)

    #     with freeze_time(date_in_2022_teledeclaration_campaign):
    #         diagnostic.teledeclare(applicant=authenticate.user)

    #         with open("./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv") as diag_file:
    #             response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         body = response.json()
    #         self.assertEqual(len(body["errors"]), 1)
    #         self.assertEqual(
    #             body["errors"][0]["message"],
    #             "Ce n'est pas possible de modifier un diagnostic télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration.",
    #         )
    #         canteen.refresh_from_db()
    #         self.assertEqual(canteen.name, "Old name")
    #         diagnostic.refresh_from_db()
    #         self.assertEqual(diagnostic.valeur_totale, 1)

    #         # now test cancelled TD
    #         diagnostic.cancel()
    #         with open("./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv") as diag_file:
    #             response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         body = response.json()
    #         self.assertEqual(len(body["errors"]), 0)
    #         canteen.refresh_from_db()
    #         self.assertEqual(canteen.name, "A canteen")
    #         diagnostic.refresh_from_db()
    #         self.assertEqual(diagnostic.valeur_totale, 1000)

    # @authenticate
    # def test_fail_import_bad_format(self, mock):
    #     with open("./api/tests/files/diagnostics/diagnostics_bad_file_format.ods", "rb") as diag_file:
    #         response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     body = response.json()
    #     errors = body["errors"]
    #     first_error = errors.pop(0)
    #     self.assertEqual(first_error["status"], 400)
    #     self.assertEqual(
    #         first_error["message"],
    #         "Ce fichier est au format application/vnd.oasis.opendocument.spreadsheet, merci d'exporter votre fichier au format CSV et réessayer.",
    #     )
