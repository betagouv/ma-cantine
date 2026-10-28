from django.test import SimpleTestCase

from imports.schemas import ImportSchema, detect_schema
from imports.views.diagnostic import DIAGNOSTICS_SIMPLE_ID_SCHEMA, DIAGNOSTICS_SIMPLE_SIRET_SCHEMA


class ImportSchemaTest(SimpleTestCase):
    def test_schema_path_url_header(self):
        schema = ImportSchema("bilans_simple_id.json")
        self.assertEqual(schema.path, "data/schemas/imports/bilans_simple_id.json")
        self.assertTrue(schema.url.startswith("https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/"))
        self.assertTrue(schema.url.endswith("/data/schemas/imports/bilans_simple_id.json"))
        self.assertEqual(schema.header[:3], ["cantine_id", "année_bilan", "valeur_totale"])

    def test_detect_schema(self):
        siret_schema, id_schema = DIAGNOSTICS_SIMPLE_SIRET_SCHEMA, DIAGNOSTICS_SIMPLE_ID_SCHEMA
        self.assertEqual(detect_schema(siret_schema.header, [siret_schema, id_schema]), siret_schema)
        self.assertEqual(detect_schema(id_schema.header, [siret_schema, id_schema]), id_schema)
        # exact match only
        self.assertIsNone(detect_schema(id_schema.header[:-1], [siret_schema, id_schema]))
        self.assertIsNone(detect_schema(id_schema.header + ["extra"], [siret_schema, id_schema]))
        self.assertIsNone(detect_schema([column.upper() for column in id_schema.header], [siret_schema, id_schema]))
        self.assertIsNone(detect_schema([], [siret_schema, id_schema]))


class DiagnosticsSimpleImportSchemasTest(SimpleTestCase):
    def test_headers_are_unique(self):
        # the siret & id schemas are accepted by the same import: their headers must differ
        self.assertNotEqual(DIAGNOSTICS_SIMPLE_SIRET_SCHEMA.header, DIAGNOSTICS_SIMPLE_ID_SCHEMA.header)
