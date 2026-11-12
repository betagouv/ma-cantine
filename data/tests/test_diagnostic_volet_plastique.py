from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)
from data.models.sector import Sector
from data.validators import diagnostic_volet_plastique as diagnostic_volet_plastique_validators


def get_plastique_diagnostic(year=2026, field_empty=None, **canteen_kwargs):
    """
    A diagnostic with the volet plastique started: all the fields filled, except field_empty
    """
    diagnostic = DiagnosticFactory(
        year=year, canteen=CanteenFactory(**canteen_kwargs), diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
    )
    for field in get_teledeclaration_fields_all(year, "PLASTIQUE"):
        setattr(diagnostic, field, None if field == field_empty else True)
    return diagnostic


class DiagnosticVoletPlastiqueVenteEmporterValidatorTest(TestCase):
    FIELD = "vente_emporter"

    def test_vente_emporter_required(self):
        self.assertIn(self.FIELD, get_teledeclaration_fields_required(2026, "PLASTIQUE"))
        diagnostic = get_plastique_diagnostic(field_empty=self.FIELD, sector_list=[Sector.EDUCATION_PRIMAIRE])
        errors = diagnostic_volet_plastique_validators.validate_plastique_fields_required(diagnostic)
        self.assertIn(self.FIELD, errors)


class DiagnosticVoletPlastiqueContenantEmporterValidatorTest(TestCase):
    FIELD = "plastique_contenant_emporter_remplace"

    def test_plastique_contenant_emporter_remplace_optional(self):
        """
        Only asked (in the tunnel) if vente_emporter is True, like the dons_* fields with dons_convention
        """
        self.assertNotIn(self.FIELD, get_teledeclaration_fields_required(2026, "PLASTIQUE"))


class DiagnosticVoletPlastiqueContenantEmporterFieldsValidatorTest(TestCase):
    FIELD = "plastique_contenant_emporter_remplace"

    def test_plastique_contenant_emporter_remplace_required_if_vente_emporter(self):
        diagnostic = get_plastique_diagnostic(field_empty=self.FIELD)
        self.assertTrue(diagnostic.vente_emporter)
        errors = diagnostic_volet_plastique_validators.validate_plastique_contenant_emporter_fields(diagnostic)
        self.assertEqual(list(errors.keys()), [self.FIELD])
        # answered (even False): no error
        for value in [True, False]:
            with self.subTest(value=value):
                setattr(diagnostic, self.FIELD, value)
                errors = diagnostic_volet_plastique_validators.validate_plastique_contenant_emporter_fields(diagnostic)
                self.assertEqual(errors, {})

    def test_plastique_contenant_emporter_remplace_optional_if_no_vente_emporter(self):
        for vente_emporter in [False, None]:
            with self.subTest(vente_emporter=vente_emporter):
                diagnostic = get_plastique_diagnostic(field_empty=self.FIELD)
                diagnostic.vente_emporter = vente_emporter
                errors = diagnostic_volet_plastique_validators.validate_plastique_contenant_emporter_fields(diagnostic)
                self.assertEqual(errors, {})

    def test_plastique_contenant_emporter_remplace_must_be_empty_if_no_vente_emporter(self):
        for vente_emporter in [False, None]:
            for value in [True, False]:
                with self.subTest(vente_emporter=vente_emporter, value=value):
                    diagnostic = get_plastique_diagnostic()
                    diagnostic.vente_emporter = vente_emporter
                    setattr(diagnostic, self.FIELD, value)
                    errors = diagnostic_volet_plastique_validators.validate_plastique_contenant_emporter_fields(
                        diagnostic
                    )
                    self.assertEqual(list(errors.keys()), [self.FIELD])

    def test_no_validation_before_2026(self):
        diagnostic = get_plastique_diagnostic(year=2025)
        diagnostic.vente_emporter = True
        diagnostic.plastique_contenant_emporter_remplace = None
        errors = diagnostic_volet_plastique_validators.validate_plastique_contenant_emporter_fields(diagnostic)
        self.assertEqual(errors, {})
        diagnostic.vente_emporter = False
        diagnostic.plastique_contenant_emporter_remplace = True
        errors = diagnostic_volet_plastique_validators.validate_plastique_contenant_emporter_fields(diagnostic)
        self.assertEqual(errors, {})

    def test_is_clean_returns_the_error(self):
        diagnostic = get_plastique_diagnostic(field_empty=self.FIELD)
        _, errors = diagnostic.is_clean()
        self.assertIn(self.FIELD, errors)
        _, errors = diagnostic.is_clean(skip_volets_thematiques=True)
        self.assertNotIn(self.FIELD, errors)
