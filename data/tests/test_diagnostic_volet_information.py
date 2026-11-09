from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)
from data.validators import diagnostic_volet_information as diagnostic_volet_information_validators


class DiagnosticVoletInformationValidatorTest(TestCase):
    def _diagnostic(self, pat_list):
        diagnostic = DiagnosticFactory(
            year=2026, canteen=CanteenFactory(pat_list=pat_list), diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        # volet started: all the required fields filled, except information_part_pat
        for field in get_teledeclaration_fields_all(2026, "INFORMATION"):
            setattr(diagnostic, field, None)
        for field in get_teledeclaration_fields_required(2026, "INFORMATION"):
            if field != "information_part_pat":
                setattr(diagnostic, field, True)
        return diagnostic

    def test_information_part_pat_required_if_canteen_in_a_pat(self):
        diagnostic = self._diagnostic(pat_list=["1415"])
        errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
        self.assertEqual(list(errors.keys()), ["information_part_pat"])

        diagnostic.information_part_pat = False
        errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
        self.assertEqual(errors, {})

    def test_information_part_pat_optional_if_canteen_not_in_a_pat(self):
        diagnostic = self._diagnostic(pat_list=[])
        errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
        self.assertEqual(errors, {})

    def test_other_fields_still_required_if_canteen_not_in_a_pat(self):
        diagnostic = self._diagnostic(pat_list=[])
        diagnostic.information_part_egalim = None
        errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
        self.assertEqual(list(errors.keys()), ["information_part_egalim"])
