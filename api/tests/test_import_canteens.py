import json
import re

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import SectorFactory, UserFactory
from data.models import Canteen

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
        for VALUE_OK in ["Crèche", " Cliniques ", "Cliniques+Crèche", " Cliniques + Crèche "]:
            self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["Secteur qui n'existe pas", "Crèche,Cliniques", " Crèche + Cliniques , Hôpitaux"]:
            self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_code_insee_commune_regex(self):
        pattern = self.get_pattern("code_insee_commune")
        for VALUE_OK in ["2A215", "54318"]:
            self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["AAAAA", "A", " 2A215 ", "543181", "2A215 "]:
            self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_code_postal_commune_regex(self):
        pattern = self.get_pattern("code_postal_commune")
        for VALUE_OK in ["75000"]:
            self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["75O10", " 75010 ", "", "   ", "750000", "75"]:
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
            self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["type de production inconnu", "", "CENTRAL", "site-cooked-elsewhere", "     "]:
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
            self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["type de gestion inconnu", "", "CONCEDED", "     "]:
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
            self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["modèle économique inconnu", "", "PUBLIC", "     "]:
            self.assertFalse(re.match(pattern, VALUE_NOT_OK))


class TestCanteenImport(APITestCase):
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
        with open("./api/tests/files/canteens/canteens_bad_no_header.csv", "rb") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["errors"]), 1)
        self.assertEqual(
            body["errors"][0]["message"],
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre",
        )

    @authenticate
    def test_import_only_canteens(self):
        """
        Should be able to import canteens from a file that doesn't have commas for the optional fields
        """
        with open("./api/tests/files/canteens/canteens_good.csv") as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(body["errors"]), 0)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Canteen.objects.first().economic_model, None)

    @authenticate
    def test_import_canteens_with_managers(self):
        """
        Should be able to import canteens
        """
        manager = UserFactory(email="manager@example.com")
        with open("./api/tests/files/canteens/canteens_good_add_manager.csv") as canteen_file:
            response = self.client.post(reverse("import_canteens"), {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(len(body["canteens"]), 1)
        self.assertEqual(len(body["errors"]), 0, body["errors"])
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertIn(manager, Canteen.objects.first().managers.all())

    @authenticate
    def test_canteens_empty_when_error(self):
        """
        If a cantine succeeds and another one doesn't, no canteen should be saved
        and the array of cantine should return zero
        """
        SectorFactory.create(name="Crèche")
        with open("./api/tests/files/canteens/canteens_bad.csv") as canteen_file:
            response = self.client.post(f"{reverse('import_canteens')}", {"file": canteen_file})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["count"], 0)
        self.assertEqual(len(body["canteens"]), 0)
        self.assertEqual(len(body["errors"]), 1, body["errors"])
        self.assertEqual(Canteen.objects.count(), 0)
