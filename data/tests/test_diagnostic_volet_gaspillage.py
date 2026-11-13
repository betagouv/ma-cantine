from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)
from data.validators import diagnostic_volet_gaspillage as diagnostic_volet_gaspillage_validators


class DiagnosticVoletGaspillageYearValidatorTest(TestCase):
    def test_no_validation_before_2026(self):
        for year in [2021, 2022, 2023, 2024, 2025]:
            with self.subTest(year=year):
                # volet started, canteen with the dons_convention obligation
                diagnostic = DiagnosticFactory(
                    year=year,
                    canteen=CanteenFactory(daily_meal_count=5000, yearly_meal_count=5000 * 200),
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                )
                for field in get_teledeclaration_fields_all(year, "GASPILLAGE"):
                    setattr(diagnostic, field, None)
                diagnostic.diagnostic_gaspillage_realise = True
                self.assertTrue(diagnostic.is_filled_gaspillage)
                errors = diagnostic_volet_gaspillage_validators.validate_gaspillage_fields_required(diagnostic)
                self.assertEqual(errors, {})


class DiagnosticVoletGaspillageDonsConventionValidatorTest(TestCase):
    def _diagnostic(self, daily_meal_count):
        diagnostic = DiagnosticFactory(
            year=2026,
            canteen=CanteenFactory(daily_meal_count=daily_meal_count, yearly_meal_count=daily_meal_count * 200),
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )
        # volet started: all the required fields filled, except dons_convention
        for field in get_teledeclaration_fields_all(2026, "GASPILLAGE"):
            setattr(diagnostic, field, None)
        for field in get_teledeclaration_fields_required(2026, "GASPILLAGE"):
            if field != "dons_convention":
                setattr(diagnostic, field, True)
        return diagnostic

    def test_dons_convention_required_if_canteen_serves_3000_meals_or_more(self):
        for daily_meal_count in [3000, 5000]:
            with self.subTest(daily_meal_count=daily_meal_count):
                diagnostic = self._diagnostic(daily_meal_count=daily_meal_count)
                errors = diagnostic_volet_gaspillage_validators.validate_gaspillage_fields_required(diagnostic)
                self.assertEqual(list(errors.keys()), ["dons_convention"])

                diagnostic.dons_convention = False
                errors = diagnostic_volet_gaspillage_validators.validate_gaspillage_fields_required(diagnostic)
                self.assertEqual(errors, {})

    def test_dons_convention_optional_if_canteen_serves_less_than_3000_meals(self):
        for daily_meal_count in [100, 2999]:
            with self.subTest(daily_meal_count=daily_meal_count):
                diagnostic = self._diagnostic(daily_meal_count=daily_meal_count)
                errors = diagnostic_volet_gaspillage_validators.validate_gaspillage_fields_required(diagnostic)
                self.assertEqual(errors, {})

    def test_other_fields_still_required_if_canteen_serves_less_than_3000_meals(self):
        diagnostic = self._diagnostic(daily_meal_count=100)
        diagnostic.plan_gaspillage_en_place = None
        errors = diagnostic_volet_gaspillage_validators.validate_gaspillage_fields_required(diagnostic)
        self.assertEqual(list(errors.keys()), ["plan_gaspillage_en_place"])


class DiagnosticVoletGaspillageDonsFieldsValidatorTest(TestCase):
    DONS_FIELDS_VALUES = {"dons_frequence": 12, "dons_quantite": 100, "dons_type_denrees": "Fruits et légumes"}

    def _diagnostic(self, year=2026, dons_convention=None, **kwargs):
        diagnostic = DiagnosticFactory(year=year, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        for field in get_teledeclaration_fields_all(year, "GASPILLAGE"):
            setattr(diagnostic, field, None)
        diagnostic.dons_convention = dons_convention
        for field, value in kwargs.items():
            setattr(diagnostic, field, value)
        return diagnostic

    def test_dons_fields_can_be_filled_if_dons_convention(self):
        diagnostic = self._diagnostic(dons_convention=True, **self.DONS_FIELDS_VALUES)
        self.assertEqual(diagnostic_volet_gaspillage_validators.validate_gaspillage_dons_fields(diagnostic), {})

    def test_dons_fields_cannot_be_filled_without_dons_convention(self):
        for dons_convention in [False, None]:
            for field, value in self.DONS_FIELDS_VALUES.items():
                with self.subTest(dons_convention=dons_convention, field=field):
                    diagnostic = self._diagnostic(dons_convention=dons_convention, **{field: value})
                    errors = diagnostic_volet_gaspillage_validators.validate_gaspillage_dons_fields(diagnostic)
                    self.assertEqual(list(errors.keys()), [field])

    def test_dons_fields_empty_without_dons_convention(self):
        for dons_convention in [False, None]:
            with self.subTest(dons_convention=dons_convention):
                diagnostic = self._diagnostic(dons_convention=dons_convention, dons_type_denrees="")
                self.assertEqual(
                    diagnostic_volet_gaspillage_validators.validate_gaspillage_dons_fields(diagnostic), {}
                )

    def test_no_validation_before_2026(self):
        for year in [2021, 2022, 2023, 2024, 2025]:
            with self.subTest(year=year):
                diagnostic = self._diagnostic(year=year, dons_convention=False, **self.DONS_FIELDS_VALUES)
                self.assertEqual(
                    diagnostic_volet_gaspillage_validators.validate_gaspillage_dons_fields(diagnostic), {}
                )

    def test_is_clean_returns_the_error(self):
        diagnostic = self._diagnostic(dons_convention=False, dons_frequence=12)
        _, errors = diagnostic.is_clean()
        self.assertIn("dons_frequence", errors)
        _, errors = diagnostic.is_clean(skip_volets_thematiques=True)
        self.assertNotIn("dons_frequence", errors)
