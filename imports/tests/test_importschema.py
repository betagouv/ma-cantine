from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase

from data.models import Diagnostic
from imports.models import ImportSchema
from imports.views.diagnostic import (
    DIAGNOSTICS_COMPLETE_SCHEMA,
    DIAGNOSTICS_SIMPLE_ID_SCHEMA,
    DIAGNOSTICS_SIMPLE_SIRET_SCHEMA,
)


class ImportSchemaTest(SimpleTestCase):
    def test_schema_path_url_header(self):
        schema = ImportSchema("bilans_simple_id.json")
        self.assertEqual(schema.path, "data/schemas/imports/bilans_simple_id.json")
        self.assertTrue(schema.url.startswith("https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/"))
        self.assertTrue(schema.url.endswith("/data/schemas/imports/bilans_simple_id.json"))
        self.assertEqual(schema.header[:3], ["cantine_id", "année_bilan", "valeur_totale"])


class DiagnosticsImportSchemasTest(SimpleTestCase):
    def test_schemas_columns_are_diagnostic_fields(self):
        """
        The values are read by column name: the value columns must be Diagnostic fields
        """
        diagnostic_field_names = [field.name for field in Diagnostic._meta.get_fields()]
        for schema, identifier in [
            (DIAGNOSTICS_SIMPLE_SIRET_SCHEMA, "siret"),
            (DIAGNOSTICS_SIMPLE_ID_SCHEMA, "cantine_id"),
            (DIAGNOSTICS_COMPLETE_SCHEMA, "siret"),
            (ImportSchema("bilans_simple_siret_2026.json"), "siret"),
            (ImportSchema("bilans_simple_id_2026.json"), "cantine_id"),
        ]:
            with self.subTest(schema=schema.name):
                self.assertEqual(schema.header[:2], [identifier, "année_bilan"])
                for column in schema.header[2:]:
                    self.assertIn(column, diagnostic_field_names)

    def test_schemas_are_up_to_date(self):
        """
        The schema files must match the output of the generate_import_schema command
        """
        for schema in ["simple_siret", "simple_id", "simple_siret_2026", "simple_id_2026"]:
            with self.subTest(schema=schema):
                out = StringIO()
                call_command("generate_import_schema", model="Diagnostic", schema=schema, dry_run=True, stdout=out)
                self.assertIn("No changes", out.getvalue())
