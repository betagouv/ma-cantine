from django.test import SimpleTestCase

from imports.models import ImportSchema


class ImportSchemaTest(SimpleTestCase):
    def test_schema_path_url_header(self):
        schema = ImportSchema("bilans_simple_id.json")
        self.assertEqual(schema.path, "data/schemas/imports/bilans_simple_id.json")
        self.assertTrue(schema.url.startswith("https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/"))
        self.assertTrue(schema.url.endswith("/data/schemas/imports/bilans_simple_id.json"))
        self.assertEqual(schema.header[:3], ["cantine_id", "année_bilan", "valeur_totale"])
