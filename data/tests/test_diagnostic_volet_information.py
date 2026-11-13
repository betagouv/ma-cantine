from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic
from data.models.sector import Sector
from data.models.diagnostic_teledeclaration_fields import (
    get_teledeclaration_fields_all,
    get_teledeclaration_fields_required,
)
from data.validators import diagnostic_volet_information as diagnostic_volet_information_validators


class DiagnosticVoletInformationYearValidatorTest(TestCase):
    def test_no_validation_before_2026(self):
        for year in [2021, 2022, 2023, 2024, 2025]:
            with self.subTest(year=year):
                # volet started (a field of the year filled), canteen in a PAT & in a concerned sector
                diagnostic = DiagnosticFactory(
                    year=year,
                    canteen=CanteenFactory(pat_list=["1415"], sector_list=[Sector.EDUCATION_PRIMAIRE]),
                    diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                )
                for field in get_teledeclaration_fields_all(year, "INFORMATION"):
                    setattr(diagnostic, field, None)
                diagnostic.information_qualite_durable = True
                self.assertTrue(diagnostic.is_filled_information)
                errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
                self.assertEqual(errors, {})


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


class DiagnosticVoletInformationConsultationQualiteValidatorTest(TestCase):
    def _diagnostic(self, sector_list, **canteen_kwargs):
        diagnostic = DiagnosticFactory(
            year=2026,
            canteen=CanteenFactory(sector_list=sector_list, pat_list=["1415"], **canteen_kwargs),
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )
        # volet started: all the required fields filled, except information_consultation_qualite
        for field in get_teledeclaration_fields_all(2026, "INFORMATION"):
            setattr(diagnostic, field, None)
        for field in get_teledeclaration_fields_required(2026, "INFORMATION"):
            if field != "information_consultation_qualite":
                setattr(diagnostic, field, True)
        return diagnostic

    def test_information_consultation_qualite_required_if_canteen_in_a_concerned_sector(self):
        for sector in [
            Sector.EDUCATION_PRIMAIRE,  # établissement scolaire
            Sector.EDUCATION_SUPERIEUR_UNIVERSITAIRE,  # établissement universitaire
            Sector.SOCIAL_CRECHE,  # accueil des enfants de moins de 6 ans
            Sector.SANTE_HOPITAL,  # établissement de santé
            Sector.SOCIAL_EHPAD,  # établissement médico-social
            Sector.ADMINISTRATION_PRISON,  # établissement pénitentiaire
        ]:
            with self.subTest(sector=sector):
                diagnostic = self._diagnostic(sector_list=[sector])
                errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
                self.assertEqual(list(errors.keys()), ["information_consultation_qualite"])

    def test_information_consultation_qualite_required_if_one_of_the_sectors_is_concerned(self):
        diagnostic = self._diagnostic(sector_list=[Sector.ENTERPRISE_ENTREPRISE, Sector.EDUCATION_PRIMAIRE])
        errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
        self.assertEqual(list(errors.keys()), ["information_consultation_qualite"])

    def test_information_consultation_qualite_optional_if_canteen_not_in_a_concerned_sector(self):
        for sector_list in [
            [Sector.ENTERPRISE_ENTREPRISE],
            [Sector.ADMINISTRATION_ADMINISTRATIF],
            [Sector.LOISIR_CENTRE_VACANCES],  # not in the article L.230-5
            [Sector.AUTRES_AUTRE],
        ]:
            with self.subTest(sector_list=sector_list):
                diagnostic = self._diagnostic(sector_list=sector_list)
                errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
                self.assertEqual(errors, {})

    def test_information_consultation_qualite_optional_if_canteen_without_sector(self):
        # groupe: no sector
        diagnostic = self._diagnostic(sector_list=[], production_type=Canteen.ProductionType.GROUPE)
        errors = diagnostic_volet_information_validators.validate_information_fields_required(diagnostic)
        self.assertEqual(errors, {})
