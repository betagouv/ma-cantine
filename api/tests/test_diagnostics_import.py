import datetime
from decimal import Decimal

import requests_mock
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


@requests_mock.Mocker()
class DiagnosticsImportApiTest(APITestCase):
    def test_unauthenticated_import_call(self, mock):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_diagnostics"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # @authenticate
    # def test_diagnostics_created(self, mock):
    #     """
    #     Given valid data, multiple diagnostics are created for multiple canteens,
    #     the authenticated user is added as the manager,
    #     and a summary of the results is returned
    #     """
    #     self.assertEqual(Canteen.objects.count(), 0)
    #     self.assertEqual(Diagnostic.objects.count(), 0)

    #     with open("./api/tests/files/diagnostics/diagnostics_simple_good_different_canteens.csv") as diag_file:
    #         response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     body = response.json()
    #     self.assertEqual(body["count"], 2)
    #     self.assertEqual(body["canteens"][0]["siret"], "21340172201787")
    #     self.assertEqual(body["canteens"][0]["diagnostics"][0]["year"], 2021)
    #     self.assertEqual(len(body["errors"]), 0)
    #     self.assertEqual(Canteen.objects.count(), 2)
    #     self.assertEqual(Canteen.objects.first().managers.first().id, authenticate.user.id)
    #     self.assertEqual(Diagnostic.objects.count(), 2)
    #     canteen = Canteen.objects.get(siret="21340172201787")
    #     self.assertEqual(canteen.daily_meal_count, 700)
    #     self.assertEqual(canteen.yearly_meal_count, 14000)
    #     self.assertEqual(canteen.production_type, "site")
    #     self.assertEqual(canteen.management_type, "conceded")
    #     self.assertEqual(canteen.economic_model, "public")
    #     self.assertEqual(canteen.creation_source, CreationSource.IMPORT)
    #     diagnostic = Diagnostic.objects.get(canteen_id=canteen.id)
    #     self.assertEqual(diagnostic.year, 2021)
    #     self.assertEqual(diagnostic.valeur_totale, 1000)
    #     self.assertEqual(diagnostic.valeur_bio, 500)
    #     self.assertEqual(diagnostic.valeur_siqo, Decimal("100.1"))
    #     self.assertEqual(diagnostic.valeur_externalites_performance, 10)
    #     self.assertEqual(diagnostic.valeur_egalim_autres, 20)
    #     self.assertEqual(diagnostic.valeur_viandes_volailles, 30)
    #     self.assertEqual(diagnostic.valeur_viandes_volailles_egalim, 1)
    #     self.assertEqual(diagnostic.valeur_viandes_volailles_france, 2)
    #     self.assertEqual(diagnostic.valeur_produits_de_la_mer, 4)
    #     self.assertEqual(diagnostic.valeur_produits_de_la_mer_egalim, 3)
    #     self.assertEqual(diagnostic.diagnostic_type, Diagnostic.DiagnosticType.SIMPLE)
    #     self.assertEqual(diagnostic.creation_source, CreationSource.IMPORT)
    #     self.assertIn("seconds", body)

    # @authenticate
    # def test_error_collection(self, mock):
    #     """
    #     If errors occur, discard the file and return the errors with row and message
    #     """
    #     # creating 2 canteens with same siret here to error when this situation exists IRL
    #     CanteenFactory(siret="42111303053388")
    #     canteen_with_same_siret = CanteenFactory()
    #     Canteen.objects.filter(id=canteen_with_same_siret.id).update(siret="42111303053388")

    #     file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad.csv"
    #     with open(file_path) as diag_file:
    #         response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Diagnostic.objects.count(), 0)
    #     assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
    #     body = response.json()
    #     self.assertEqual(body["count"], 0)
    #     # no new objects should have been saved to the DB since it failed
    #     self.assertEqual(Canteen.objects.count(), 2)
    #     self.assertEqual(Diagnostic.objects.count(), 0)
    #     errors = body["errors"]
    #     self.assertEqual(len(errors), 22, errors)
    #     self.assertEqual(errors[0]["row"], 1)
    #     self.assertEqual(errors[0]["status"], 400)
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'année' : L'année est obligatoire pour créer un diagnostic.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'année' : La valeur « . » doit être un nombre entier.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'repas par jour' : La valeur «\xa0not a number\xa0» doit être un nombre entier.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'repas par jour' : Le champ doit être un nombre entier.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'mode de production' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'secteurs d'activité' : Le champ doit contenir entre 1 et 3 secteurs.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'Valeur totale annuelle HT' : La valeur « invalid total » doit être un nombre décimal.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         f"Champ 'année' : L'année doit être comprise entre 2019 et {NEXT_YEAR}.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'Valeur totale annuelle HT' : La somme des valeurs d'approvisionnement, 300, est plus que le total, 20",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'siret' : Le siret de la cantine ne peut pas être vide",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'Modèle économique' : La valeur «\xa0'blah'\xa0» n’est pas un choix valide.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'code postal' : Ce champ ne peut pas être vide si le code INSEE de la ville est vide.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'repas par jour' : Le champ ne peut pas être vide.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'nom' : Ce champ ne peut pas être vide.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'code postal' : Ce champ ne peut pas être vide si le code INSEE de la ville est vide.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Plusieurs cantines correspondent au SIRET 42111303053388. Veuillez enlever les doublons pour pouvoir créer le diagnostic.",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées EGalim, 100, est plus que la valeur totale (HT) viandes et volailles, 50",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'Valeur totale (HT) viandes et volailles fraiches ou surgelées' : La valeur totale (HT) viandes et volailles fraiches ou surgelées provenance France, 100, est plus que la valeur totale (HT) viandes et volailles, 50",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'Valeur totale (HT) poissons et produits aquatiques' : La valeur totale (HT) poissons et produits aquatiques EGalim, 100, est plus que la valeur totale (HT) poissons et produits aquatiques, 50",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         # TODO: is this the best field to point to as being wrong? hors bio could be confusing
    #         "Champ 'Produits SIQO (hors bio) - Valeur annuelle HT' : La somme des valeurs viandes et poissons EGalim, 300, est plus que la somme des valeurs bio, SIQO, environnementales et autres EGalim, 200",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'siret' : 14 caractères numériques sont attendus",
    #     )
    #     self.assertEqual(
    #         errors.pop(0)["message"],
    #         "Champ 'secteurs d'activité' : Le champ doit contenir entre 1 et 3 secteurs.",
    #     )


    # @authenticate
    # def test_diagnostic_no_header(self, mock):
    #     """
    #     A file should not be valid if doesn't contain a valid header
    #     """
    #     with open("./api/tests/files/diagnostics/diagnostics_simple_bad_no_header.csv") as diag_file:
    #         response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     body = response.json()
    #     self.assertEqual(body["count"], 0)
    #     self.assertEqual(len(body["errors"]), 1)
    #     self.assertEqual(
    #         body["errors"][0]["message"],
    #         "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
    #     )

    # @override_settings(CSV_IMPORT_MAX_SIZE=1)
    # @authenticate
    # def test_max_size(self, mock):
    #     file_path = "./api/tests/files/diagnostics/diagnostics_simple_good_separator_semicolon_decimal_number.csv"
    #     with open(file_path) as diag_file:
    #         response = self.client.post(reverse("import_diagnostics"), {"file": diag_file})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Diagnostic.objects.count(), 0)
    #     assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
    #     body = response.json()
    #     errors = body["errors"]
    #     self.assertEqual(body["count"], 0)
    #     self.assertEqual(
    #         errors.pop(0)["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
    #     )

    # @authenticate
    # def test_import_wrong_header(self, mock):
    #     with open("./api/tests/files/diagnostics/diagnostics_complete_bad_no_header.csv") as diag_file:
    #         response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})
    #     body = response.json()

    #     self.assertEqual(
    #         body["errors"][0]["message"],
    #         "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
    #     )

    #     with open("./api/tests/files/diagnostics/diagnostics_complete_bad_wrong_header.csv") as diag_file:
    #         response = self.client.post(f"{reverse('import_complete_diagnostics')}", {"file": diag_file})
    #     body = response.json()

    #     self.assertEqual(
    #         body["errors"][0]["message"],
    #         "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
    #     )

    # @authenticate
    # def test_optional_appro_values(self, mock):
    #     """
    #     For simplified diagnostics, an empty appro value is considered unknown
    #     """
    #     with open(
    #         "./api/tests/files/diagnostics/diagnostics_simple_good_separator_semicolon_no_appro.csv"
    #     ) as diag_file:
    #         response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})

    #     body = response.json()
    #     self.assertEqual(len(body["errors"]), 0)
    #     self.assertEqual(Diagnostic.objects.count(), 1)
    #     diagnostic = Diagnostic.objects.first()

    #     self.assertEqual(diagnostic.valeur_totale, 1000)
    #     self.assertIsNone(diagnostic.valeur_bio)
    #     self.assertEqual(diagnostic.valeur_siqo, 0)

    # @authenticate
    # def test_mandatory_total_simplified(self, mock):
    #     """
    #     For simplified diagnostics, only the total HT is mandatory in the appro fields
    #     """
    #     file_path = "./api/tests/files/diagnostics/diagnostics_simple_bad_separator_semicolon_no_total.csv"
    #     with open(file_path) as diag_file:
    #         response = self.client.post(f"{reverse('import_diagnostics')}", {"file": diag_file})
    #     self.assertEqual(Diagnostic.objects.count(), 0)
    #     assert_import_failure_created(self, authenticate.user, ImportType.DIAGNOSTIC_SIMPLE, file_path)
    #     body = response.json()
    #     self.assertEqual(len(body["errors"]), 1)
    #     self.assertEqual(
    #         body["errors"][0]["message"], "Champ 'Valeur totale annuelle HT' : Ce champ ne peut pas être vide."
    #     )

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
