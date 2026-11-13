from django.test import TestCase

from data.factories import DiagnosticFactory
from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all
from data.validators import diagnostic_volet_diversification as diagnostic_volet_diversification_validators


class DiagnosticVoletDiversificationPlanFieldsValidatorTest(TestCase):
    def _diagnostic(self, year=2026, plan_diversification_en_place=None, plan_diversification_actions=None):
        diagnostic = DiagnosticFactory(year=year, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        for field in get_teledeclaration_fields_all(year, "DIVERSIFICATION"):
            setattr(diagnostic, field, None)
        diagnostic.plan_diversification_en_place = plan_diversification_en_place
        diagnostic.plan_diversification_actions = plan_diversification_actions
        return diagnostic

    def test_plan_diversification_actions_can_be_filled_if_plan_diversification_en_place(self):
        diagnostic = self._diagnostic(
            plan_diversification_en_place=True,
            plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
        )
        errors = diagnostic_volet_diversification_validators.validate_diversification_plan_fields(diagnostic)
        self.assertEqual(errors, {})

    def test_plan_diversification_actions_cannot_be_filled_without_plan_diversification_en_place(self):
        for plan_diversification_en_place in [False, None]:
            with self.subTest(plan_diversification_en_place=plan_diversification_en_place):
                diagnostic = self._diagnostic(
                    plan_diversification_en_place=plan_diversification_en_place,
                    plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_plan_fields(diagnostic)
                self.assertEqual(list(errors.keys()), ["plan_diversification_actions"])

    def test_plan_diversification_actions_empty_without_plan_diversification_en_place(self):
        for plan_diversification_actions in [None, []]:
            with self.subTest(plan_diversification_actions=plan_diversification_actions):
                diagnostic = self._diagnostic(
                    plan_diversification_en_place=False, plan_diversification_actions=plan_diversification_actions
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_plan_fields(diagnostic)
                self.assertEqual(errors, {})

    def test_no_validation_before_2026(self):
        for year in [2021, 2022, 2023, 2024, 2025]:
            with self.subTest(year=year):
                diagnostic = self._diagnostic(
                    year=year,
                    plan_diversification_en_place=False,
                    plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_plan_fields(diagnostic)
                self.assertEqual(errors, {})

    def test_is_clean_returns_the_error(self):
        diagnostic = self._diagnostic(
            plan_diversification_en_place=False,
            plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
        )
        _, errors = diagnostic.is_clean()
        self.assertIn("plan_diversification_actions", errors)
        _, errors = diagnostic.is_clean(skip_volets_thematiques=True)
        self.assertNotIn("plan_diversification_actions", errors)


class DiagnosticVoletDiversificationMenuVegetarienFieldsValidatorTest(TestCase):
    def _diagnostic(self, year=2026, menu_vegetarien_frequence=None, menu_vegetarien_bases=None):
        diagnostic = DiagnosticFactory(year=year, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        for field in get_teledeclaration_fields_all(year, "DIVERSIFICATION"):
            setattr(diagnostic, field, None)
        diagnostic.menu_vegetarien_frequence = menu_vegetarien_frequence
        diagnostic.menu_vegetarien_bases = menu_vegetarien_bases
        return diagnostic

    def test_menu_vegetarien_bases_can_be_filled_if_menu_vegetarien_proposed(self):
        for menu_vegetarien_frequence in [
            Diagnostic.MenuVegetarienFrequence.MOINS_HEBDO,
            Diagnostic.MenuVegetarienFrequence.HEBDO,
            Diagnostic.MenuVegetarienFrequence.PLUS_HEBDO,
            Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
        ]:
            with self.subTest(menu_vegetarien_frequence=menu_vegetarien_frequence):
                diagnostic = self._diagnostic(
                    menu_vegetarien_frequence=menu_vegetarien_frequence,
                    menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_menu_vegetarien_fields(
                    diagnostic
                )
                self.assertEqual(errors, {})

    def test_menu_vegetarien_bases_cannot_be_filled_without_menu_vegetarien(self):
        for menu_vegetarien_frequence in [Diagnostic.MenuVegetarienFrequence.JAMAIS, None]:
            with self.subTest(menu_vegetarien_frequence=menu_vegetarien_frequence):
                diagnostic = self._diagnostic(
                    menu_vegetarien_frequence=menu_vegetarien_frequence,
                    menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_menu_vegetarien_fields(
                    diagnostic
                )
                self.assertEqual(list(errors.keys()), ["menu_vegetarien_bases"])

    def test_menu_vegetarien_bases_empty_without_menu_vegetarien(self):
        for menu_vegetarien_bases in [None, []]:
            with self.subTest(menu_vegetarien_bases=menu_vegetarien_bases):
                diagnostic = self._diagnostic(
                    menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.JAMAIS,
                    menu_vegetarien_bases=menu_vegetarien_bases,
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_menu_vegetarien_fields(
                    diagnostic
                )
                self.assertEqual(errors, {})

    def test_no_validation_before_2026(self):
        for year in [2021, 2022, 2023, 2024, 2025]:
            with self.subTest(year=year):
                diagnostic = self._diagnostic(
                    year=year,
                    menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.JAMAIS,
                    menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
                )
                errors = diagnostic_volet_diversification_validators.validate_diversification_menu_vegetarien_fields(
                    diagnostic
                )
                self.assertEqual(errors, {})

    def test_is_clean_returns_the_error(self):
        diagnostic = self._diagnostic(
            menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.JAMAIS,
            menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
        )
        _, errors = diagnostic.is_clean()
        self.assertIn("menu_vegetarien_bases", errors)
        _, errors = diagnostic.is_clean(skip_volets_thematiques=True)
        self.assertNotIn("menu_vegetarien_bases", errors)
