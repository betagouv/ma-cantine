import json
import re
from unittest import skipIf

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import assert_import_failure_created, authenticate
from data.factories import CanteenFactory, UserFactory
from data.models import Canteen, ImportFailure, ImportType, ManagerInvitation, Sector
from data.models.creation_source import CreationSource


class CanteenSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open("data/schemas/imports/cantines.json"))
        cls.schema_admin = json.load(open("data/schemas/imports/cantines_admin.json"))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    def test_secteurs_regex(self):
        pattern = self.get_pattern(self.schema, "secteurs")
        for VALUE_OK in [
            "",
            " ",
            "Crèche",
            " Cliniques ",
            "Cliniques,Crèche",
            " Cliniques , Crèche ",
            "EHPAD / maisons de retraite / foyers de personnes âgées",
            "Restaurants administratifs d’Etat (RA)",
            "Restaurants administratifs d'Etat (RA)",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["Secteur qui n'existe pas", "Cliniques+Crèche", " Cliniques + Crèche , Hôpitaux"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_type_production_regex(self):
        pattern = self.get_pattern(self.schema, "type_production")
        for VALUE_OK in [
            "Cuisine centrale",
            "Cuisine centrale et site",
            "Restaurant avec cuisine sur place",
            "Restaurant satellite",
            " Cuisine centrale et site",
            " Restaurant avec cuisine sur place ",
            "Restaurant satellite ",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in [
            "type de production inconnu",
            "",
            "central",
            "central_serving",
            "site_cooked_elsewhere",
            "site",
            "     ",
        ]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_type_gestion_regex(self):
        pattern = self.get_pattern(self.schema, "type_gestion")
        for VALUE_OK in [
            "Concédée",
            " Concédée",
            "Concédée ",
            " Concédée ",
            "Directe",
            " Directe",
            "Directe ",
            " Directe ",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["type de gestion inconnu", "", "conceded", "direct", "     "]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_modele_economique_regex(self):
        pattern = self.get_pattern(self.schema, "modèle_économique")
        for VALUE_OK in [
            "public",
            " public",
            "public ",
            " public ",
            "private",
            " private",
            "private ",
            " private ",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["modèle économique inconnu", "", "PUBLIC", "     "]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_admin_ministere_tutelle_regex(self):
        pattern = self.get_pattern(self.schema_admin, "admin_ministère_tutelle")
        for VALUE_OK in [
            "Agriculture, Alimentation et Forêts",
            " Santé et Solidarités",
            "Préfecture - Administration Territoriale de l'État (ATE) ",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["agriculture", "     "]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteenImportErrorTest(APITestCase):
    def test_unauthenticated(self):
        response = self.client.post(reverse("import_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_header_error(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        # header missing
        file_path = "./api/tests/files/canteens/canteens_bad_no_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors.pop(0)["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

        # wrong header
        file_path = "./api/tests/files/canteens/canteens_bad_wrong_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors.pop(0)["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

        # partial header
        file_path = "./api/tests/files/canteens/canteens_bad_partial_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors.pop(0)["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_validata_empty_rows_error(self):
        """
        A file should not be valid if it contains empty rows
        """
        file_path = "./api/tests/files/canteens/canteens_bad_empty_rows.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
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
        file_path = "./api/tests/files/canteens/canteens_bad_nearly_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
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
    def test_not_canteen_manager_error(self):
        """
        Cannot update an existing canteen if the user is not a manager of this canteen
        """
        CanteenFactory(siret="21010034300016")
        file_path = "./api/tests/files/canteens/canteens_bad_nearly_good_2.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 1 + 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors.pop(0)["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")

    @authenticate
    def test_staff_import_non_admin_header(self):
        """
        Staff users must import file with additionnal columns
        """
        user = authenticate.user
        user.is_staff = True
        user.save()

        file_path = "./api/tests/files/canteens/canteens_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors.pop(0)["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_staff_import_non_staff(self):
        """
        Non-staff users shouldn't have staff import capabilities
        """
        file_path = "./api/tests/files/canteens/canteens_admin_good_new_canteen.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["status"], 400)
        self.assertEqual(
            errors.pop(0)["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_sectors_error(self):
        """
        - Sectors are required if canteen production_type is site, site_cooked_elsewhere, central_serving
        - Canteen can't have more than 3 sectors
        """
        file_path = "./api/tests/files/canteens/canteen_bad_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        error_message_central = "Champ 'secteurs d'activité' : Cuisine centrale : le champ doit être vide."
        error_message_min_max = "Champ 'secteurs d'activité' : Le champ doit contenir entre 1 et 3 secteurs."
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 4, errors)
        self.assertEqual(errors.pop(0)["message"], error_message_central)
        self.assertEqual(errors.pop(0)["message"], error_message_min_max)
        self.assertEqual(errors.pop(0)["message"], error_message_min_max)
        self.assertEqual(errors.pop(0)["message"], error_message_min_max)

    @authenticate
    def test_model_validation_error(self):
        """
        If a canteen doesn't pass model validation, no canteen should be saved
        and the array of canteens should return zero
        """
        file_path = "./api/tests/files/canteens/canteens_bad.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        assert_import_failure_created(self, authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 4, errors)
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
                "Champ 'secteurs d'activité' : Cuisine centrale : le champ doit être vide."
            ),
        )
        self.assertTrue(
            errors.pop(0)["message"].startswith(
                "Champ 'siret de la cuisine centrale' : Restaurant satellite : le champ ne peut pas être égal au SIRET du satellite."
            ),
        )


@skipIf(settings.SKIP_TESTS_THAT_REQUIRE_INTERNET, "Skipping tests that require internet access")
class CanteenImportSuccessTest(APITestCase):
    @authenticate
    def test_import_only_canteens(self):
        """
        Should be able to import canteens
        """
        self.assertEqual(Canteen.objects.count(), 0)

        file_path = "./api/tests/files/canteens/canteens_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 5)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 5)
        self.assertEqual(len(body["canteens"]), 5)
        self.assertEqual(len(errors), 0, errors)

    @authenticate
    def test_import_canteens_with_managers(self):
        """
        Should be able to import canteens with managers
        """
        manager = UserFactory(email="manager@example.com")

        file_path = "./api/tests/files/canteens/canteens_good_add_manager.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
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
    def test_empty_sectors_central_canteen(self):
        """
        Sectors are not required if canteen production_type is central
        """
        file_path = "./api/tests/files/canteens/canteen_good_empty_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 1)
        canteen = Canteen.objects.get(siret="16463707389922")
        self.assertEqual(canteen.production_type, "central")
        self.assertEqual(len(canteen.sector_list), 0)

    @authenticate
    def test_sectors_apostrophes(self):
        """
        Different apostrophes caracters should be accepted but a unique one should be saved
        """
        file_path = "./api/tests/files/canteens/canteens_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.filter(sector_list__contains=[Sector.ADMINISTRATION_ADMINISTRATIF]).distinct().count(),
            2,
        )

        body = response.json()
        self.assertEqual(len(errors), 0, errors)

    @authenticate
    def test_sectors_less_or_equal_max(self):
        """
        Canteen can have 3 sectors or less
        """
        file_path = "./api/tests/files/canteens/canteens_good_max_sectors.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
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
        file_path = "./api/tests/files/canteens/canteens_good.xlsx"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
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
    def test_admin_import(self):
        """
        Admin get to specify extra columns and have fewer requirements on what data is required.
        - new canteen: managers are added without sending emails to them.
        - new canteen: the importer isn't added to the canteen unless specified.
        - updated canteen: admin doesn't have to be a manager.
        """
        canteen = CanteenFactory(name="Canteen initial", siret="21010034300016")
        canteen.managers.clear()
        user = authenticate.user
        user.is_staff = True
        user.email = "authenticate@example.com"
        user.save()

        file_path = "./api/tests/files/canteens/canteens_admin_good_new_canteen.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        errors = body["errors"]

        self.assertEqual(body["count"], 3)
        self.assertEqual(len(body["canteens"]), 3)
        self.assertEqual(len(errors), 0, errors)
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(ManagerInvitation.objects.count(), 2 + 2 + 2)
        self.assertEqual(len(mail.outbox), 1)

        canteen1 = Canteen.objects.get(siret="21340172201787")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen1, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen1, email="user2@example.com"))
        self.assertEqual(canteen1.managers.count(), 0)
        self.assertEqual(canteen1.line_ministry, Canteen.Ministries.SANTE)
        self.assertEqual(canteen1.import_source, "Automated test")

        canteen2 = Canteen.objects.get(siret="21380185500015")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen2, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen2, email="user2@example.com"))
        self.assertEqual(canteen2.managers.count(), 1)
        self.assertEqual(canteen2.managers.first(), user)
        self.assertEqual(canteen2.line_ministry, None)
        self.assertEqual(canteen2.import_source, "Automated test")

        canteen3 = Canteen.objects.get(siret="21010034300016")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen3, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen3, email="user2@example.com"))
        self.assertEqual(canteen3.managers.count(), 0)
        self.assertEqual(canteen3.name, "Canteen update")  # updated
        self.assertEqual(canteen3.line_ministry, Canteen.Ministries.AGRICULTURE)
        self.assertEqual(canteen3.import_source, "Automated test")

        email = mail.outbox[0]
        self.assertEqual(email.to[0], "user1@example.com")
        self.assertNotIn("Canteen for two", email.body)
        self.assertIn("Staff canteen", email.body)
