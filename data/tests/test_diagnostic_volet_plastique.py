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
