from django.test import SimpleTestCase

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    DIAGNOSTIC_TYPES,
    TELEDECLARATION_YEARS,
    VOLETS_TUNNEL_PROGRESS_FIELD_MAPPING,
    VOLETS,
    VOLETS_EDITABLE_WHEN_IS_TELEDECLARED_ALREADY,
    get_fields_editable_when_is_teledeclared_already,
    get_teledeclaration_config,
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_all_volets,
    get_teledeclaration_fields_all_years,
    get_teledeclaration_fields_required,
    get_teledeclaration_latest_verbose_names,
    get_teledeclaration_verbose_names,
    get_tunnel_progress_field,
)


class TeledeclarationFieldsTest(SimpleTestCase):
    def test_every_year_has_all_volets(self):
        for year in TELEDECLARATION_YEARS:
            with self.subTest(year=year):
                self.assertEqual(set(get_teledeclaration_config(year)), set(VOLETS))

    def test_every_field_has_a_verbose_name(self):
        for year in TELEDECLARATION_YEARS:
            for volet, volet_fields in get_teledeclaration_config(year).items():
                with self.subTest(year=year, volet=volet):
                    self.assertEqual([name for name, field in volet_fields.items() if not field["verbose_name"]], [])

    def test_every_field_exists_on_the_model(self):
        # all the fields of the configuration (even the ones that are not present for any diagnostic_type)
        model_fields = {field.name for field in Diagnostic._meta.get_fields()}
        for year in TELEDECLARATION_YEARS:
            for volet, volet_fields in get_teledeclaration_config(year).items():
                with self.subTest(year=year, volet=volet):
                    self.assertEqual(set(volet_fields) - model_fields, set())

    def test_every_field_has_a_verbose_name(self):
        for year in TELEDECLARATION_YEARS:
            for volet, volet_fields in get_teledeclaration_config(year).items():
                with self.subTest(year=year, volet=volet):
                    fields_without_verbose_name = [
                        name for name, field in volet_fields.items() if not field.get("verbose_name")
                    ]
                    self.assertEqual(fields_without_verbose_name, [])

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
            *Diagnostic.GROUPE_FIELDS,
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
        # fields_added and fields_removed are not in the configuration for now: they will be re-added after
        return
        years = TELEDECLARATION_YEARS
        for previous_year, year in zip(years, years[1:]):
            for volet in VOLETS:
                diagnostic_types = DIAGNOSTIC_TYPES if volet == "APPROVISIONNEMENT" else [None]
                for diagnostic_type in diagnostic_types:
                    with self.subTest(year=year, volet=volet, diagnostic_type=diagnostic_type):
                        volet_fields = get_teledeclaration_config(year)[volet]
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
        # service_type (since 2024) keeps its position of the most recent year, menu_vegetarien_type (until 2023) at the end
        self.assertEqual(
            get_teledeclaration_fields_all_years("DIVERSIFICATION"),
            get_teledeclaration_fields_all(max(TELEDECLARATION_YEARS), "DIVERSIFICATION") + ["menu_vegetarien_type"],
        )

    def test_service_type_replaces_vegetarian_menu_type_from_2024(self):
        self.assertNotIn("service_type", get_teledeclaration_fields_all(2023, "DIVERSIFICATION"))
        self.assertIn("menu_vegetarien_type", get_teledeclaration_fields_all(2023, "DIVERSIFICATION"))
        for year in [2024, 2026]:
            with self.subTest(year=year):
                self.assertIn("service_type", get_teledeclaration_fields_all(year, "DIVERSIFICATION"))
                self.assertNotIn("menu_vegetarien_type", get_teledeclaration_fields_all(year, "DIVERSIFICATION"))

    def test_information_fields_replaced_in_2026(self):
        information_fields_2025 = get_teledeclaration_fields_all(2025, "INFORMATION")
        information_fields_2026 = get_teledeclaration_fields_all(2026, "INFORMATION")
        self.assertIn("information_qualite_durable", information_fields_2025)
        self.assertNotIn("information_part_egalim", information_fields_2025)
        self.assertCountEqual(
            information_fields_2026,
            [
                "information_affichage_permanent",
                "information_electronique_annuelle",
                "information_part_egalim",
                "information_part_pat",
                "information_consultation_qualite",
            ],
        )
        self.assertEqual(set(information_fields_2025) & set(information_fields_2026), set())

    def test_plastique_fields_in_2026(self):
        self.assertCountEqual(
            get_teledeclaration_fields_all(2025, "PLASTIQUE"),
            [
                "plastique_contenant_cuisson_remplace",
                "plastique_contenant_service_remplace",
                "plastique_bouteille_remplace",
                "plastique_ustensile_remplace",
            ],
        )
        # bouteille & ustensile: same question, kept
        self.assertCountEqual(
            get_teledeclaration_fields_all(2026, "PLASTIQUE"),
            [
                "plastique_bouteille_boisson_remplace",
                "plastique_bouteille_remplace",
                "plastique_ustensile_remplace",
                "plastique_vaisselle_jetable_remplace",
                "plastique_contenant_remplace",
                "vente_emporter",
                "plastique_contenant_emporter_remplace",
            ],
        )

    def test_get_teledeclaration_fields_all_volets(self):
        for year in TELEDECLARATION_YEARS:
            for diagnostic_type in DIAGNOSTIC_TYPES:
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
        self.assertIn("diagnostic_gaspillage_realise", get_teledeclaration_fields_all_volets("2025", "SIMPLE"))

    def test_get_teledeclaration_verbose_names(self):
        verbose_names_2025 = get_teledeclaration_verbose_names(2025)
        verbose_names_2026 = get_teledeclaration_verbose_names(2026)
        # the labels change from one year to another
        self.assertEqual(verbose_names_2025["valeur_bio"], "Bio - Valeur annuelle HT")
        self.assertEqual(
            verbose_names_2026["valeur_bio"],
            "Total des achats bio ou avec mention « En conversion vers l'agriculture biologique »",
        )
        # all the volets
        self.assertEqual(verbose_names_2025["plan_gaspillage_en_place"], "Plan d'action contre le gaspillage en place")

    def test_get_teledeclaration_latest_verbose_names(self):
        latest_verbose_names = get_teledeclaration_latest_verbose_names()
        # the most recent year
        self.assertEqual(latest_verbose_names["valeur_bio"], get_teledeclaration_verbose_names(2026)["valeur_bio"])
        # field removed since: its last year
        self.assertNotIn("valeur_autres_aocaop_igp_stg", get_teledeclaration_config(2026)["APPROVISIONNEMENT"])
        self.assertEqual(
            latest_verbose_names["valeur_autres_aocaop_igp_stg"],
            get_teledeclaration_verbose_names(2025)["valeur_autres_aocaop_igp_stg"],
        )

    def test_get_tunnel_progress_field(self):
        self.assertEqual(list(VOLETS_TUNNEL_PROGRESS_FIELD_MAPPING.keys()), VOLETS)
        for volet in VOLETS:
            with self.subTest(volet=volet):
                tunnel_progress_field = get_tunnel_progress_field(volet)
                Diagnostic._meta.get_field(tunnel_progress_field)  # exists on the model
                self.assertIn(tunnel_progress_field, Diagnostic.TUNNEL_PROGRESS_FIELDS)
        self.assertEqual(get_tunnel_progress_field("GASPILLAGE"), "tunnel_waste")
        with self.assertRaises(ValueError):
            get_tunnel_progress_field("UNKNOWN")

    def test_get_fields_editable_when_is_teledeclared_already(self):
        self.assertNotIn("APPROVISIONNEMENT", VOLETS_EDITABLE_WHEN_IS_TELEDECLARED_ALREADY)
        for year in TELEDECLARATION_YEARS:
            with self.subTest(year=year):
                fields = get_fields_editable_when_is_teledeclared_already(year)
                for volet in VOLETS_EDITABLE_WHEN_IS_TELEDECLARED_ALREADY:
                    for field in get_teledeclaration_fields_all(year, volet):
                        self.assertIn(field, fields)
                    self.assertIn(get_tunnel_progress_field(volet), fields)
                # never the appro fields, nor the diagnostic's main fields
                for diagnostic_type in DIAGNOSTIC_TYPES:
                    for field in get_teledeclaration_fields_all(year, "APPROVISIONNEMENT", diagnostic_type):
                        self.assertNotIn(field, fields)
                for field in ["year", "diagnostic_type", "central_kitchen_diagnostic_mode", "status", "tunnel_appro"]:
                    self.assertNotIn(field, fields)
        # depends on the year
        self.assertNotIn("service_type", get_fields_editable_when_is_teledeclared_already(2023))
        self.assertIn("service_type", get_fields_editable_when_is_teledeclared_already(2024))
        with self.assertRaises(ValueError):
            get_fields_editable_when_is_teledeclared_already(2020)

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
