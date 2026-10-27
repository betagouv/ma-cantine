from django.test import SimpleTestCase

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    TELEDECLARATION_FIELDS,
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_all_volets,
    get_teledeclaration_fields_all_years,
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

    def test_get_teledeclaration_fields_all_years(self):
        approvisionnement_fields = get_teledeclaration_fields_all_years("APPROVISIONNEMENT")
        self.assertEqual(len(approvisionnement_fields), len(set(approvisionnement_fields)))  # no duplicates
        self.assertIn("valeur_bio", approvisionnement_fields)  # SIMPLE
        self.assertIn("valeur_viandes_volailles_aocaop", approvisionnement_fields)  # COMPLETE, since 2026
        self.assertIn("valeur_viandes_volailles_aocaop_igp_stg", approvisionnement_fields)  # COMPLETE, until 2025
        # most recent year first, then legacy fields
        self.assertLess(
            approvisionnement_fields.index("valeur_viandes_volailles_aocaop"),
            approvisionnement_fields.index("valeur_viandes_volailles_aocaop_igp_stg"),
        )
        # service_type (since 2024) keeps its position of the most recent year
        self.assertEqual(
            get_teledeclaration_fields_all_years("DIVERSIFICATION"),
            get_teledeclaration_fields_all(max(TELEDECLARATION_FIELDS), "DIVERSIFICATION"),
        )

    def test_service_type_only_from_2024(self):
        self.assertNotIn("service_type", get_teledeclaration_fields_all(2023, "DIVERSIFICATION"))
        self.assertIn("service_type", get_teledeclaration_fields_all(2024, "DIVERSIFICATION"))
        self.assertIn("service_type", get_teledeclaration_fields_all(2026, "DIVERSIFICATION"))

    def test_get_teledeclaration_fields_all_volets(self):
        for year in TELEDECLARATION_FIELDS:
            for diagnostic_type in TELEDECLARATION_FIELDS[year]["APPROVISIONNEMENT"]:
                with self.subTest(year=year, diagnostic_type=diagnostic_type):
                    expected_fields = get_teledeclaration_fields_all(year, "APPROVISIONNEMENT", diagnostic_type) + [
                        field for volet in VOLETS[1:] for field in get_teledeclaration_fields_all(year, volet)
                    ]
                    self.assertEqual(get_teledeclaration_fields_all_volets(year, diagnostic_type), expected_fields)
        # depends on the year & diagnostic_type
        self.assertIn("valeur_bio", get_teledeclaration_fields_all_volets(2025, "SIMPLE"))
        self.assertNotIn("valeur_bio", get_teledeclaration_fields_all_volets(2025, "COMPLETE"))
        self.assertNotIn("service_type", get_teledeclaration_fields_all_volets(2023, "SIMPLE"))
        self.assertIn("service_type", get_teledeclaration_fields_all_volets(2024, "SIMPLE"))
        self.assertIn("has_waste_diagnostic", get_teledeclaration_fields_all_volets("2025", "SIMPLE"))

    def test_errors(self):
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2020, "APPROVISIONNEMENT", "SIMPLE")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2025, "UNKNOWN")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all(2025, "APPROVISIONNEMENT")  # APPROVISIONNEMENT requires a diagnostic_type
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all_volets(2020, "SIMPLE")
        with self.assertRaises(ValueError):
            get_teledeclaration_fields_all_volets(2025, None)  # APPROVISIONNEMENT requires a diagnostic_type
