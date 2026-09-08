import json
import re

from django.test import TestCase

from api.views.purchase_import import PURCHASE_ID_SCHEMA_FILE_PATH, PURCHASE_SIRET_SCHEMA_FILE_PATH


class PurchasesImportSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schemas = {
            "siret": json.load(open(PURCHASE_SIRET_SCHEMA_FILE_PATH)),
            "id": json.load(open(PURCHASE_ID_SCHEMA_FILE_PATH)),
        }

    @staticmethod
    def _pattern_for(schema, field_name):
        field = next(f for f in schema["fields"] if f["name"] == field_name)
        return field["constraints"]["pattern"]

    def test_famille_produits_regex(self):
        for schema_name, schema in self.schemas.items():
            pattern = self._pattern_for(schema, "famille_produits")
            for VALUE_OK in ["PRODUITS_LAITIERS", "PRODUITS_LAITIERS ", " PRODUITS_LAITIERS "]:
                with self.subTest(schema=schema_name, VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["", "TEST", "PRODUITS_LAITIERS,", "PRODUITS_LAITIERS,VIANDES_VOLAILLES"]:
                with self.subTest(schema=schema_name, VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_categories_egalim_regex(self):
        for schema_name, schema in self.schemas.items():
            pattern = self._pattern_for(schema, "categories_egalim")
            for VALUE_OK in [
                "BIO",
                "BIO ",
                "BIO,COMMERCE_EQUITABLE",
                "BIO,COMMERCE_EQUITABLE ",
                " BIO,COMMERCE_EQUITABLE ",
                " BIO, COMMERCE_EQUITABLE ",
                " BIO,      COMMERCE_EQUITABLE ",
                "BIO,BIO",
            ]:
                with self.subTest(schema=schema_name, VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["", "TEST"]:
                with self.subTest(schema=schema_name, VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_origine_regex(self):
        for schema_name, schema in self.schemas.items():
            pattern = self._pattern_for(schema, "origine")
            for VALUE_OK in [
                "EUROPE",
                "FRANCE",
                "FRANCE ",
                " FRANCE ",
            ]:
                with self.subTest(schema=schema_name, VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["", "TEST", "FRANCE,", "FRANCE,EUROPE"]:
                with self.subTest(schema=schema_name, VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))

    def test_definition_local_regex(self):
        for schema_name, schema in self.schemas.items():
            pattern = self._pattern_for(schema, "definition_local")
            for VALUE_OK in [
                "PAT",
                " PAT ",
                "COMMUNE",
                "DEPARTEMENT",
                "DEPARTEMENT ",
                " DEPARTEMENT ",
                "REGION",
                "KM",
            ]:
                with self.subTest(schema=schema_name, VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["", "TEST", "DEPARTEMENT,", "DEPARTEMENT,REGION"]:
                with self.subTest(schema=schema_name, VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))
