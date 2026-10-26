from django.test import SimpleTestCase

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    TELEDECLARATION_FIELDS,
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)

VOLETS = ["APPRO", "GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]


class TeledeclarationFieldsTest(SimpleTestCase):
    def test_every_year_has_all_volets(self):
        for year in TELEDECLARATION_FIELDS:
            with self.subTest(year=year):
                self.assertEqual(list(TELEDECLARATION_FIELDS[year].keys()), VOLETS)

    def test_every_field_exists_on_the_model(self):
        model_fields = {field.name for field in Diagnostic._meta.get_fields()}
        for year in TELEDECLARATION_FIELDS:
            for diagnostic_type in TELEDECLARATION_FIELDS[year]["APPRO"]:
                with self.subTest(year=year, diagnostic_type=diagnostic_type):
                    self.assertEqual(set(get_teledeclaration_fields_all(year, diagnostic_type)) - model_fields, set())
            for volet in VOLETS[1:]:
                with self.subTest(year=year, volet=volet):
                    self.assertEqual(set(get_teledeclaration_fields_all(year, volet=volet)) - model_fields, set())

    def test_appro_is_the_default_volet(self):
        self.assertEqual(
            get_teledeclaration_fields_all(2025, "SIMPLE"),
            get_teledeclaration_fields_all(2025, "SIMPLE", volet="APPRO"),
        )
        self.assertEqual(
            get_teledeclaration_fields_required(2025, "COMPLETE"),
            get_teledeclaration_fields_required(2025, "COMPLETE", volet="APPRO"),
        )

    def test_non_appro_volets_ignore_diagnostic_type(self):
        for volet in VOLETS[1:]:
            with self.subTest(volet=volet):
                self.assertEqual(
                    get_teledeclaration_fields_all(2025, volet=volet),
                    get_teledeclaration_fields_all(2025, "COMPLETE", volet=volet),
                )
                self.assertEqual(get_teledeclaration_fields_required(2025, volet=volet), [])

    def test_current_year_matches_the_model_volet_fields(self):
        latest_year = max(TELEDECLARATION_FIELDS)
        for volet, model_volet_fields in [
            ("GASPILLAGE", Diagnostic.WASTE_FIELDS),
            ("DIVERSIFICATION", Diagnostic.DIVERSIFICATION_FIELDS),
            ("PLASTIQUE", Diagnostic.PLASTIC_FIELDS),
            ("INFORMATION", Diagnostic.INFO_FIELDS),
        ]:
            with self.subTest(volet=volet):
                self.assertEqual(get_teledeclaration_fields_all(latest_year, volet=volet), model_volet_fields)

    def test_service_type_only_from_2024(self):
        self.assertNotIn("service_type", get_teledeclaration_fields_all(2023, volet="DIVERSIFICATION"))
        self.assertIn("service_type", get_teledeclaration_fields_all(2024, volet="DIVERSIFICATION"))
        self.assertIn("service_type", get_teledeclaration_fields_all(2026, volet="DIVERSIFICATION"))

    def test_errors(self):
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2020, "SIMPLE")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2025, volet="UNKNOWN")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2025)  # APPRO requires a diagnostic_type
