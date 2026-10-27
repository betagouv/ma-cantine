from django.test import SimpleTestCase

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    TELEDECLARATION_FIELDS,
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)

VOLETS = ["APPROVISIONNEMENT", "GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]


class TeledeclarationFieldsTest(SimpleTestCase):
    def test_every_year_has_all_volets(self):
        for year in TELEDECLARATION_FIELDS:
            with self.subTest(year=year):
                self.assertEqual(list(TELEDECLARATION_FIELDS[year].keys()), VOLETS)

    def test_every_field_exists_on_the_model(self):
        model_fields = {field.name for field in Diagnostic._meta.get_fields()}
        for year in TELEDECLARATION_FIELDS:
            for diagnostic_type in TELEDECLARATION_FIELDS[year]["APPROVISIONNEMENT"]:
                with self.subTest(year=year, diagnostic_type=diagnostic_type):
                    self.assertEqual(
                        set(get_teledeclaration_fields_all(year, "APPROVISIONNEMENT", diagnostic_type)) - model_fields,
                        set(),
                    )
            for volet in VOLETS[1:]:
                with self.subTest(year=year, volet=volet):
                    self.assertEqual(set(get_teledeclaration_fields_all(year, volet)) - model_fields, set())

    def test_non_approvisionnement_volets_ignore_diagnostic_type(self):
        for volet in VOLETS[1:]:
            with self.subTest(volet=volet):
                self.assertEqual(
                    get_teledeclaration_fields_all(2025, volet),
                    get_teledeclaration_fields_all(2025, volet, "COMPLETE"),
                )
                self.assertEqual(get_teledeclaration_fields_required(2025, volet), [])

    def test_current_year_matches_the_model_volet_fields(self):
        latest_year = max(TELEDECLARATION_FIELDS)
        for volet, model_volet_fields in [
            ("GASPILLAGE", Diagnostic.WASTE_FIELDS),
            ("DIVERSIFICATION", Diagnostic.DIVERSIFICATION_FIELDS),
            ("PLASTIQUE", Diagnostic.PLASTIC_FIELDS),
            ("INFORMATION", Diagnostic.INFO_FIELDS),
        ]:
            with self.subTest(volet=volet):
                self.assertEqual(get_teledeclaration_fields_all(latest_year, volet), model_volet_fields)

    def test_service_type_only_from_2024(self):
        self.assertNotIn("service_type", get_teledeclaration_fields_all(2023, "DIVERSIFICATION"))
        self.assertIn("service_type", get_teledeclaration_fields_all(2024, "DIVERSIFICATION"))
        self.assertIn("service_type", get_teledeclaration_fields_all(2026, "DIVERSIFICATION"))

    def test_errors(self):
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2020, "APPROVISIONNEMENT", "SIMPLE")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2025, "UNKNOWN")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2025, "APPROVISIONNEMENT")  # APPROVISIONNEMENT requires a diagnostic_type
