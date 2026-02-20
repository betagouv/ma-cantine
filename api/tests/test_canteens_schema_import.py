import json
import re
from django.test import TestCase
from api.views.canteen_create_import import CANTEEN_SCHEMA_FILE_PATH
from api.views.canteen_update_import import CANTEEN_UPDATE_SCHEMA_FILE_PATH


class CanteensSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema_create = json.load(open(CANTEEN_SCHEMA_FILE_PATH))
        cls.schema_update = json.load(open(CANTEEN_UPDATE_SCHEMA_FILE_PATH))
        cls.schemas = [cls.schema_create, cls.schema_update]

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    def test_secteurs_regex(self):
        for schema in self.schemas:
            pattern = self.get_pattern(schema, "secteurs")
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
        for schema in self.schemas:
            pattern = self.get_pattern(schema, "type_production")
            for VALUE_OK in [
                "Restaurant avec cuisine sur place",
                " Restaurant avec cuisine sur place",
                "Restaurant avec cuisine sur place ",
                " Restaurant avec cuisine sur place ",
                "Restaurant satellite",
                " Restaurant satellite",
                "Restaurant satellite ",
                " Restaurant satellite ",
                "site_cooked_elsewhere",
                "site",
                " site_cooked_elsewhere",
                " site",
                "site_cooked_elsewhere ",
                "site ",
                " site_cooked_elsewhere ",
                " site ",
            ]:
                with self.subTest(VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in [
                "Cuisine centrale",
                " Cuisine centrale",
                "Cuisine centrale ",
                " Cuisine centrale ",
                "central",
                " central",
                "central ",
                " central ",
                "type de production inconnu",
                "",
                "     ",
                "Cuisine centrale et site",
                "central_serving",
            ]:
                with self.subTest(VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_type_gestion_regex(self):
        for schema in self.schemas:
            pattern = self.get_pattern(schema, "type_gestion")
            for VALUE_OK in [
                "Concédée",
                " Concédée",
                "Concédée ",
                " Concédée ",
                "Directe",
                " Directe",
                "Directe ",
                " Directe ",
                "conceded",
                "direct",
                " conceded",
                " direct",
                "conceded ",
                "direct ",
                " conceded ",
                " direct ",
            ]:
                with self.subTest(VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["type de gestion inconnu", "", "     "]:
                with self.subTest(VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_modele_economique_regex(self):
        for schema in self.schemas:
            pattern = self.get_pattern(schema, "modèle_économique")
            for VALUE_OK in [
                "Public",
                " Public",
                "Public ",
                " Public ",
                "Privé",
                " Privé",
                "Privé ",
                " Privé ",
                "public",
                "private",
                " public",
                " private",
                "public ",
                "private ",
                " public ",
                " private ",
            ]:
                with self.subTest(VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["modèle économique inconnu", "", "     "]:
                with self.subTest(VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_administration_tutelle_regex(self):
        for schema in self.schemas:
            pattern = self.get_pattern(schema, "administration_tutelle")
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
