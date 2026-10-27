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

    def test_every_model_field_is_classified(self):
        """
        Every Diagnostic field must be either in the registry (any year & volet),
        or in one of the model's non-TD field lists (meta, computed, teledeclaration, legacy...)
        """
        registry_fields = {field for volet in VOLETS for field in get_teledeclaration_fields_all_years(volet)}
        self.assertEqual(set(Diagnostic.APPRO_FIELDS_LEGACY) & registry_fields, set())
        classified_fields = registry_fields | {
            *Diagnostic.APPRO_FIELDS_LEGACY,
            *Diagnostic.APPRO_AGGREGATED_FIELDS,
            *Diagnostic.APPRO_STATS_FIELDS,
            *Diagnostic.OTHER_COMPUTED_FIELDS,
            *Diagnostic.META_FIELDS,
            *Diagnostic.CREATION_META_FIELDS,
            *Diagnostic.MATOMO_FIELDS,
            *Diagnostic.TUNNEL_PROGRESS_FIELDS,
            *Diagnostic.TELEDECLARATION_FIELDS,
            *Diagnostic.TELEDECLARATION_SNAPSHOT_FIELDS,
            *Diagnostic.TELEDECLARATION_1TD1SITE_FIELDS,
            *Diagnostic.TELEDECLARATION_DATA_QUALITY_FIELDS,
            # not in any list
            "status",
            "applicant",
            "generated_from_purchases",
        }
        unclassified_fields = [
            field.name
            for field in Diagnostic._meta.concrete_fields
            if field.name not in classified_fields and field.attname not in classified_fields
        ]
        self.assertEqual(unclassified_fields, [])

    def test_fields_added_and_removed_match_the_previous_year(self):
        years = sorted(TELEDECLARATION_FIELDS)
        for previous_year, year in zip(years, years[1:]):
            for volet in VOLETS:
                diagnostic_types = (
                    TELEDECLARATION_FIELDS[year][volet].keys() if volet == "APPROVISIONNEMENT" else [None]
                )
                for diagnostic_type in diagnostic_types:
                    with self.subTest(year=year, volet=volet, diagnostic_type=diagnostic_type):
                        volet_fields = TELEDECLARATION_FIELDS[year][volet]
                        if diagnostic_type:
                            volet_fields = volet_fields[diagnostic_type]
                        fields = set(get_teledeclaration_fields_all(year, volet, diagnostic_type))
                        previous_fields = set(get_teledeclaration_fields_all(previous_year, volet, diagnostic_type))
                        self.assertEqual(set(volet_fields.get("fields_added", [])), fields - previous_fields)
                        self.assertEqual(set(volet_fields.get("fields_removed", [])), previous_fields - fields)

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
        # service_type (since 2024) keeps its position of the most recent year, vegetarian_menu_type (until 2023) at the end
        self.assertEqual(
            get_teledeclaration_fields_all_years("DIVERSIFICATION"),
            get_teledeclaration_fields_all(max(TELEDECLARATION_FIELDS), "DIVERSIFICATION") + ["vegetarian_menu_type"],
        )

    def test_service_type_replaces_vegetarian_menu_type_from_2024(self):
        self.assertNotIn("service_type", get_teledeclaration_fields_all(2023, "DIVERSIFICATION"))
        self.assertIn("vegetarian_menu_type", get_teledeclaration_fields_all(2023, "DIVERSIFICATION"))
        for year in [2024, 2026]:
            with self.subTest(year=year):
                self.assertIn("service_type", get_teledeclaration_fields_all(year, "DIVERSIFICATION"))
                self.assertNotIn("vegetarian_menu_type", get_teledeclaration_fields_all(year, "DIVERSIFICATION"))

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
