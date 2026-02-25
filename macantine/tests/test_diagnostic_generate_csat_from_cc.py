from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.models import Canteen, Diagnostic
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class DiagnosticGenerateCsatFromCC2024CommandTest(TestCase):

    # TESTS TO DO :
    # def test_canteen_sites_diagnostics_teledeclared_are_not_modified(self):
    # def test_sat_without_central_diagnostic_teledeclared_is_not_modified(self):
    # def test_central_teledeclare_diagnostic_are_generated(self):
    # def test_central_serving_teledeclare_diagnostic_are_generated(self):
    # def test_command_delete_previous_generated_diagnostics(self):
    # def test_command_split_appro_for_satellites_is_correct(self):
    # def test_other_year_diagnostics_are_not_modified(self):
    # def test_sat_with_diagnostic_not_teledeclared_is_overwritten(self):
    # def test_sat_with_diagnostic_teledeclared_is_overwritten(self):
    # def test_sat_with_two_diagnostics(self):
    # def test_generated_diagnostics_contains_canteen_data(self):