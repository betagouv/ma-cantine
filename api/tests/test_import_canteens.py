import json
import re

from django.test import TestCase


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
