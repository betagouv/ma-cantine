import json

from django.test import TestCase
from imports.views.diagnostic import DIAGNOSTICS_SIMPLE_ID_SCHEMA


class DiagnosticsSimpleSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_SIMPLE_ID_SCHEMA.path))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test
