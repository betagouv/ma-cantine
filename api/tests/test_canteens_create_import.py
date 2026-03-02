from unittest import skipIf

from django.test.utils import override_settings
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, UserFactory
from data.models import Canteen, ImportFailure, ImportType, Sector
from data.models.creation_source import CreationSource


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensImportApiErrorTest(APITestCase):
    def test_unauthenticated(self):
        self.assertEqual(Canteen.objects.count(), 0)

        response = self.client.post(reverse("canteens_create_import"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Canteen.objects.count(), 0)

    @authenticate
    def test_validata_missing_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Canteen.objects.count(), 0)

        # header missing
        file_path = "./api/tests/files/canteens/canteens_bad_no_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["field"], "Première ligne du fichier incorrecte")
        self.assertEqual(
            errors[0]["title"],
            "Elle doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_validata_wrong_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Canteen.objects.count(), 0)

        # wrong header
        file_path = "./api/tests/files/canteens/canteens_bad_wrong_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 12)
        for error in errors:
            self.assertTrue(error["title"].startswith("Valeur incorrecte vous avez écrit"))

    @authenticate
    def test_validata_extra_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_bad_extra_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
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
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_bad_empty_rows.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(
            errors.pop(0)["field"].startswith("ligne vide"),
        )

    @authenticate
    def test_validata_format_error(self):
        """
        If a canteen succeeds and another one doesn't, no canteen should be saved
        and the array of canteens should return zero
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_bad_nearly_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 3, errors)
        self.assertTrue(
            errors.pop(0)["message"].startswith("La valeur est obligatoire et doit être renseignée"),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith("Les valeurs de cette colonne doivent être uniques"),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith("Secteur inconnu ne respecte pas le motif imposé"),
        )

    @authenticate
    def test_model_validation_error(self):
        """
        If a canteen doesn't pass model validation, no canteen should be saved
        and the array of canteens should return zero
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_bad.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 5, errors)
        self.assertTrue(
            errors.pop(0)["message"].startswith("Champ 'repas par jour' : Le champ doit être au moins égal à 3."),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith(
                "Champ 'repas par an (y compris livrés)' : Le champ doit être au moins égal à 420."
            ),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith(
                "Champ 'siret de la cuisine centrale' : Le champ ne peut être rempli que pour les groupes ou les restaurants satellites."
            ),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith(
                "Champ 'siret de la cuisine centrale' : Restaurant satellite : le champ ne peut pas être égal au SIRET du satellite."
            ),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith(
                "Champ 'Groupe' : Aucun groupe avec le numéro identifiant « 14 » trouvé sur la plateforme."
            ),
        )

    @authenticate
    def test_sectors_error(self):
        """
        - Canteen can't have more than 3 sectors
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteen_bad_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        error_message_min_max = "Champ 'secteurs d'activité' : Le champ doit contenir entre 1 et 3 secteurs."
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1, errors)
        self.assertEqual(errors[0]["message"], error_message_min_max)

    @authenticate
    def test_error_line_ministry(self):
        """
        Line ministry should be empty if canteen is private and sector does not require it
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_bad_line_ministry.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 2)
        self.assertEqual(Canteen.objects.count(), 0)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'Ministère de tutelle' : Le champ doit être vide car le modèle modèle économique n'est pas 'Public'.",
        )
        self.assertEqual(
            errors[1]["message"],
            "Champ 'Ministère de tutelle' : Le champ doit être vide car vous n'avez pas sélectionné de secteur nécessitant un ministère de tutelle.",
        )

    @authenticate
    def test_error_canteen_already_exists(self):
        """
        User cannot create a canteen that already exists
        """
        CanteenFactory(siret="21340172201787")
        self.assertEqual(Canteen.objects.count(), 1)

        file_path = "./api/tests/files/canteens/canteens_bad_canteen_already_exists.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 1)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1, errors)
        self.assertEqual(
            errors[0]["message"],
            "Champ 'siret' : Vous ne pouvez pas créer de cantine avec le numéro SIRET « 21340172201787 » car elle existe déjà sur la plateforme.",
        )

    @authenticate
    def test_when_errors_count_is_0(self):
        file_path = "./api/tests/files/canteens/canteens_bad_one_error.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertTrue(len(body["errors"]) > 0)

    @authenticate
    @override_settings(CSV_IMPORT_MAX_SIZE=1)
    def test_file_above_max_size(self):
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_CREATE, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(
            errors.pop(0)["message"], "Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo"
        )


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteensImportApiSuccessTest(APITestCase):
    @authenticate
    def test_import_only_canteens(self):
        """
        Should be able to import canteens
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 3)
        self.assertEqual(len(body["canteens"]), 3)
        self.assertEqual(len(errors), 0, errors)

    @authenticate
    def test_canteens_import_with_managers(self):
        """
        Should be able to import canteens with managers
        """
        manager = UserFactory(email="manager@example.com")
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good_add_manager.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0, errors)
        self.assertIn(manager, Canteen.objects.first().managers.all())

    @authenticate
    def test_sectors_apostrophes(self):
        """
        Different apostrophes caracters should be accepted but a unique one should be saved
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.filter(sector_list__contains=[Sector.ENTERPRISE_ENTREPRISE]).distinct().count(),
            2,
        )

        body = response.json()
        self.assertEqual(len(errors), 0, errors)

    @authenticate
    def test_sectors_less_or_equal_max(self):
        """
        Canteen can have 3 sectors or less
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good_max_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 3)
        self.assertEqual(len(body["canteens"]), 3)
        self.assertEqual(len(errors), 0, errors)
        self.assertEqual(Canteen.objects.count(), 3)

    @authenticate
    def test_import_excel_file(self):
        """
        User can import excel file
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good.xlsx"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(errors), 0, errors)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertFalse(ImportFailure.objects.exists())
        self.assertEqual(Canteen.objects.count(), 1)

        canteen = Canteen.objects.first()
        self.assertEqual(canteen.creation_source, CreationSource.IMPORT)

    @authenticate
    def test_import_with_choices_slug_value(self):
        """
        Should be able to import canteens
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good_choices_slug_values.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 3)
        self.assertEqual(len(body["canteens"]), 3)
        self.assertEqual(len(errors), 0, errors)

    @authenticate
    def test_import_with_groupe_id(self):
        """
        Should be able to import canteens with groupe id
        """
        canteen_groupe = CanteenFactory(
            name="Canteen groupe", id=9999999999, production_type=Canteen.ProductionType.GROUPE
        )
        self.assertEqual(Canteen.objects.count(), 1)

        file_path = "./api/tests/files/canteens/canteens_good_groupe.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(errors), 0, errors)
        canteen_satellite = Canteen.objects.get(siret="50250039850458")
        self.assertEqual(canteen_satellite.groupe, canteen_groupe)

    @authenticate
    def test_import_with_line_ministry(self):
        """
        Should be able to import canteens with line ministry
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good_line_ministry.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("canteens_create_import"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 2)
        self.assertEqual(len(body["canteens"]), 2)
        self.assertEqual(len(errors), 0, errors)
        self.assertEqual(Canteen.objects.count(), 2)

        canteen1 = Canteen.objects.get(siret="21340172201787")
        self.assertEqual(canteen1.line_ministry, Canteen.Ministries.SANTE)

        canteen2 = Canteen.objects.get(siret="21010034300016")
        self.assertEqual(canteen2.line_ministry, Canteen.Ministries.AGRICULTURE)
