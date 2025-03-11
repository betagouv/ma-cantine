import filecmp
import json
import re

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import SectorFactory, UserFactory
from data.models import Canteen, ImportFailure, ImportType, ManagerInvitation

from .utils import authenticate


class TestCanteenSchema(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open("data/schemas/imports/cantines.json"))

    def get_pattern(self, field_name):
        field_index = next((i for i, f in enumerate(self.schema["fields"]) if f["name"] == field_name), None)
        pattern = self.schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    def test_secteurs_regex(self):
        pattern = self.get_pattern("secteurs")
        for VALUE_OK in [
            "Crèche",
            " Cliniques ",
            "Cliniques+Crèche",
            " Cliniques + Crèche ",
            "EHPAD / maisons de retraite / foyers de personnes âgées",
            "Restaurants administratifs d’Etat (RA)",
            "Restaurants administratifs d'Etat (RA)",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["Secteur qui n'existe pas", "Cliniques,Crèche", " Cliniques + Crèche , Hôpitaux"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_code_insee_commune_regex(self):
        pattern = self.get_pattern("code_insee_commune")
        for VALUE_OK in ["2A215", "54318"]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["AAAAA", "A", " 2A215 ", "543181", "2A215 "]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_code_postal_commune_regex(self):
        pattern = self.get_pattern("code_postal_commune")
        for VALUE_OK in ["75000"]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["75O10", " 75010 ", "", "   ", "750000", "75"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_type_production_regex(self):
        pattern = self.get_pattern("type_production")
        for VALUE_OK in [
            "central",
            "central_serving",
            "site",
            "site_cooked_elsewhere",
            " central_serving",
            " site ",
            "site_cooked_elsewhere ",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["type de production inconnu", "", "CENTRAL", "site-cooked-elsewhere", "     "]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_type_gestion_regex(self):
        pattern = self.get_pattern("type_gestion")
        for VALUE_OK in [
            "conceded",
            " conceded",
            "conceded ",
            " conceded ",
            "direct",
            " direct",
            "direct ",
            " direct ",
        ]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["type de gestion inconnu", "", "CONCEDED", "     "]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_modele_economique_regex(self):
        pattern = self.get_pattern("modèle_économique")
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


class TestCanteenImport(APITestCase):
    def _assertImportFailureCreated(self, user, type, file_path):
        self.assertTrue(ImportFailure.objects.count() >= 1)
        self.assertEqual(ImportFailure.objects.first().user, user)
        self.assertEqual(ImportFailure.objects.first().import_type, type)
        self.assertTrue(filecmp.cmp(file_path, ImportFailure.objects.last().file.path, shallow=False))

    @classmethod
    def setUpTestData(cls):
        SectorFactory.create(name="Cliniques")
        SectorFactory.create(name="Hôpitaux")

    def test_unauthenticated_import_call(self):
        """
        Expect 403 if unauthenticated
        """
        response = self.client.post(reverse("import_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_import_no_header(self):
        """
        A file should not be valid if it doesn't contain a header
        """
        file_path = "./api/tests/files/canteens/canteens_bad_no_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_import_wrong_header(self):
        """
        A file should not be valid if it doesn't contain a valid header
        """
        # wrong header
        file_path = "./api/tests/files/canteens/canteens_bad_wrong_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

        # partial header
        file_path = "./api/tests/files/canteens/canteens_bad_partial_header.csv"
        with open(file_path, "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
        )

    @authenticate
    def test_import_only_canteens(self):
        """
        Should be able to import canteens
        """
        file_path = "./api/tests/files/canteens/canteens_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertFalse(ImportFailure.objects.exists())
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.first().economic_model, None)

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
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(body["errors"]), 0, body["errors"])
        self.assertIn(manager, Canteen.objects.first().managers.all())

    @authenticate
    def test_canteens_empty_when_error(self):
        """
        If a cantine succeeds and another one doesn't, no canteen should be saved
        and the array of cantine should return zero
        """
        # 3 format errors
        file_path = "./api/tests/files/canteens/canteens_bad_nearly_good.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
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

        # not the canteen manager error
        Canteen.objects.create(siret="82399356058716")
        file_path = "./api/tests/files/canteens/canteens_bad_nearly_good_2.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 1 + 0)
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors.pop(0)["message"], "Vous n'êtes pas un gestionnaire de cette cantine.")

    @authenticate
    def test_import_with_empty_rows(self):
        """
        A file should not be valid if it contains empty rows (Validata)
        """
        file_path = "./api/tests/files/canteens/canteens_bad_empty_rows.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 0)
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        errors = body["errors"]
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(errors), 2, errors)
        self.assertTrue(
            errors.pop(0)["field"].startswith("ligne vide"),
        )

    @authenticate
    def test_admin_import(self):
        """
        Admin get to specify extra columns and have fewer requirements on what data is required.
        - new canteen: managers are added without sending emails to them.
        - new canteen: the importer isn't added to the canteen unless specified.
        - updated canteen: admin doesn't have to be a manager.
        """
        Canteen.objects.create(siret="82399356058716", name="Canteen initial")
        user = authenticate.user
        user.is_staff = True
        user.email = "authenticate@example.com"
        user.save()

        file_path = "./api/tests/files/canteens/canteens_admin_good_new_canteen.csv"
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["count"], 3)
        self.assertEqual(len(body["canteens"]), 3)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(ManagerInvitation.objects.count(), 2 + 2 + 2)
        self.assertEqual(len(mail.outbox), 1)

        canteen1 = Canteen.objects.get(siret="21340172201787")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen1, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen1, email="user2@example.com"))
        self.assertEqual(canteen1.managers.count(), 0)
        self.assertEqual(canteen1.line_ministry, Canteen.Ministries.SANTE)
        self.assertEqual(canteen1.import_source, "Automated test")

        canteen2 = Canteen.objects.get(siret="73282932000074")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen2, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen2, email="user2@example.com"))
        self.assertEqual(canteen2.managers.count(), 1)
        self.assertEqual(canteen2.managers.first(), user)
        self.assertEqual(canteen2.line_ministry, None)
        self.assertEqual(canteen2.import_source, "Automated test")

        canteen3 = Canteen.objects.get(siret="82399356058716")
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen3, email="user1@example.com"))
        self.assertIsNotNone(ManagerInvitation.objects.get(canteen=canteen3, email="user2@example.com"))
        self.assertEqual(canteen3.managers.count(), 0)
        self.assertEqual(canteen3.name, "Canteen update")  # updated
        self.assertEqual(canteen3.line_ministry, Canteen.Ministries.SANTE)
        self.assertEqual(canteen3.import_source, "Automated test")

        email = mail.outbox[0]
        self.assertEqual(email.to[0], "user1@example.com")
        self.assertNotIn("Canteen for two", email.body)
        self.assertIn("Staff canteen", email.body)

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
        self._assertImportFailureCreated(authenticate.user, ImportType.CANTEEN_ONLY, file_path)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(body["errors"][0]["status"], 401)
        self.assertTrue(
            body["errors"][0]["message"].startswith(
                "Vous n'êtes pas autorisé à importer des cantines avec des champs administratifs"
            ),
        )

    @authenticate
    def test_sectors_apostrophes(self):
        """
        Different apostrophes caracters should be accepted but a unique one should be saved
        """
        file_path = "./api/tests/files/canteens/canteens_sectors.csv"
        sector = SectorFactory(name="Restaurants administratifs d'Etat (RA)")
        sector.save()
        with open(file_path) as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(
            Canteen.objects.filter(sectors__name__in=["Restaurants administratifs d'Etat (RA)"]).distinct().count(), 2
        )
        self.assertEqual(
            Canteen.objects.filter(sectors__name__in=["Restaurants administratifs d’Etat (RA)"]).distinct().count(), 0
        )

        body = response.json()
        self.assertEqual(body["errors"], 0)
