import json
import re

from django.test import TestCase
from imports.views.diagnostic import (
    DIAGNOSTICS_SIMPLE_2026_ID_SCHEMA,
    DIAGNOSTICS_SIMPLE_2026_SIRET_SCHEMA,
    DIAGNOSTICS_SIMPLE_ID_SCHEMA,
)


class DiagnosticsSimpleSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_SIMPLE_ID_SCHEMA.path))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test


class DiagnosticsSimple2026SchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schemas = {
            "siret": json.load(open(DIAGNOSTICS_SIMPLE_2026_SIRET_SCHEMA.path)),
            "id": json.load(open(DIAGNOSTICS_SIMPLE_2026_ID_SCHEMA.path)),
        }

    @staticmethod
    def _pattern_for(schema, field_name):
        field = next(f for f in schema["fields"] if f["name"] == field_name)
        return field["constraints"]["pattern"]

    def test_definition_local_regex(self):
        for schema_name, schema in self.schemas.items():
            pattern = self._pattern_for(schema, "definition_local")
            for VALUE_OK in ["PAT", "COMMUNE", "DEPARTEMENT", "REGION", "KM"]:
                with self.subTest(schema=schema_name, VALUE=VALUE_OK):
                    self.assertTrue(re.match(pattern, VALUE_OK))
            for VALUE_NOT_OK in ["", "TEST", "pat", "PAT,KM", " PAT", "AUTOUR_SERVICE"]:
                with self.subTest(schema=schema_name, VALUE=VALUE_NOT_OK):
                    self.assertFalse(re.match(pattern, VALUE_NOT_OK))
