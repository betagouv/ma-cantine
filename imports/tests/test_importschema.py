import json
from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_verbose_name
from imports.models import ImportSchema
from imports.views.diagnostic import (
    DIAGNOSTICS_COMPLETE_ID_2026_SCHEMA,
    DIAGNOSTICS_COMPLETE_SIRET_SCHEMA,
    DIAGNOSTICS_COMPLETE_SIRET_2026_SCHEMA,
    DIAGNOSTICS_SIMPLE_ID_2026_SCHEMA,
    DIAGNOSTICS_SIMPLE_SIRET_2026_SCHEMA,
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
        (the 2026 format has no année_bilan column: the diagnostics are those of the current campaign year)
        """
        diagnostic_field_names = [field.name for field in Diagnostic._meta.get_fields()]
        for schema, first_columns in [
            (DIAGNOSTICS_SIMPLE_SIRET_SCHEMA, ["siret", "année_bilan"]),
            (DIAGNOSTICS_SIMPLE_ID_SCHEMA, ["cantine_id", "année_bilan"]),
            (DIAGNOSTICS_COMPLETE_SIRET_SCHEMA, ["siret", "année_bilan"]),
            (DIAGNOSTICS_SIMPLE_SIRET_2026_SCHEMA, ["siret"]),
            (DIAGNOSTICS_SIMPLE_ID_2026_SCHEMA, ["cantine_id"]),
            (DIAGNOSTICS_COMPLETE_SIRET_2026_SCHEMA, ["siret"]),
            (DIAGNOSTICS_COMPLETE_ID_2026_SCHEMA, ["cantine_id"]),
        ]:
            with self.subTest(schema=schema.name):
                self.assertEqual(schema.header[: len(first_columns)], first_columns)
                for column in schema.header[len(first_columns) :]:
                    self.assertIn(column, diagnostic_field_names)

    def test_schemas_are_up_to_date(self):
        """
        The schema files must match the output of the generate_import_schema command
        NOTE: detaille_siret (2025) is not tested: its columns are kept optional (unlike in champs.json 2025),
        since this format is also used to import the 2026 diagnostics (where these fields are not required)
        """
        for schema in [
            "simple_siret",
            "simple_id",
            "simple_siret_2026",
            "simple_id_2026",
            "detaille_siret_2026",
            "detaille_id_2026",
        ]:
            with self.subTest(schema=schema):
                out = StringIO()
                call_command("generate_import_schema", model="Diagnostic", schema=schema, dry_run=True, stdout=out)
                self.assertIn("No changes", out.getvalue())

    def test_detaille_siret_schema_titles_are_champs_json_verbose_names(self):
        """
        detaille_siret (2025) is not generated (see above), but its column titles must still be those of champs.json 2025
        """
        schema = json.load(open(DIAGNOSTICS_COMPLETE_SIRET_SCHEMA.path))
        for field in schema["fields"][2:]:  # skip siret & année_bilan
            with self.subTest(field=field["name"]):
                self.assertEqual(
                    field["title"], get_teledeclaration_verbose_name(2025, "APPROVISIONNEMENT", field["name"])
                )
