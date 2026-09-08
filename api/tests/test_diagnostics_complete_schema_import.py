import json

from django.test import TestCase
from api.views.diagnostic_import import DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH


class DiagnosticsCompleteSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = json.load(open(DIAGNOSTICS_COMPLETE_SCHEMA_FILE_PATH))

    def get_pattern(self, schema, field_name):
        field_index = next((i for i, f in enumerate(schema["fields"]) if f["name"] == field_name), None)
        pattern = schema["fields"][field_index]["constraints"]["pattern"]
        return pattern

    # no regex patterns to test
