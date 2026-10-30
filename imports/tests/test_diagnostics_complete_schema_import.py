import json
import re

from django.test import TestCase
from imports.views.diagnostic import DIAGNOSTICS_COMPLETE_2026_SCHEMA, DIAGNOSTICS_COMPLETE_SCHEMA


class DiagnosticsCompleteSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_COMPLETE_SCHEMA.path))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test


class DiagnosticsComplete2026SchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_COMPLETE_2026_SCHEMA.path))

    @staticmethod
    def _pattern_for(schema, field_name):
        field = next(f for f in schema["fields"] if f["name"] == field_name)
        return field["constraints"]["pattern"]

    def test_definition_local_regex(self):
        pattern = self._pattern_for(self.schema, "definition_local")
        for VALUE_OK in ["PAT", "COMMUNE", "DEPARTEMENT", "REGION", "KM"]:
            with self.subTest(VALUE=VALUE_OK):
                self.assertTrue(re.match(pattern, VALUE_OK))
        for VALUE_NOT_OK in ["", "TEST", "pat", "PAT,KM", " PAT", "AUTOUR_SERVICE"]:
            with self.subTest(VALUE=VALUE_NOT_OK):
                self.assertFalse(re.match(pattern, VALUE_NOT_OK))
