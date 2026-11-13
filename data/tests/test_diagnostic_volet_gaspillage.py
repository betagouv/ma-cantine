from django.test import TestCase

from data.factories import DiagnosticFactory
from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all
from data.validators import diagnostic_volet_gaspillage as diagnostic_volet_gaspillage_validators


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
