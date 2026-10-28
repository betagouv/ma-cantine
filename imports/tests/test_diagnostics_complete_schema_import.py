import json

from django.test import TestCase
from imports.views.diagnostic import DIAGNOSTICS_COMPLETE_SCHEMA


class DiagnosticsCompleteSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_COMPLETE_SCHEMA.path))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test
