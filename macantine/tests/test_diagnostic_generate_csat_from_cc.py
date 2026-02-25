from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.models import Canteen, Diagnostic
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class DiagnosticGenerateCsatFromCC2024CommandTest(TestCase):
    @authenticate
    def test_canteen_sites_diagnostics_teledeclared_are_not_modified(self):
        """
        Test that the diagnostics of the canteen sites are generated when the command is run.
        """
        site_1 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        site_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_site_1 = DiagnosticFactory(
                canteen=site_1,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            diagnostic_site_2 = DiagnosticFactory(
                canteen=site_2,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            )
            diagnostic_site_1.teledeclare(applicant=authenticate.user)
            diagnostic_site_2.teledeclare(applicant=authenticate.user)

        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)

        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

    @authenticate
    def test_sat_without_central_diagnostic_teledeclared_is_not_modified(self):
        """
        Test that the diagnostics of the satellites without central diagnostic are not modified when the command is run.
        """
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="19622299600015"
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(
            Canteen.objects.filter(siret="19622299600015").count(), 0
        )  # no central canteen exist with the siret used in sat
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)

        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

    @authenticate
    def test_central_teledeclare_satellites_diagnostic_are_generated(self):
        """
        Test that the diagnostics for the satellites of a central canteen are generated when the command is run.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)

        # Diagnostics are generated
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).get(canteen=satellite_1).generated_from_groupe_diagnostic, True
        )
        self.assertEqual(
            Diagnostic.objects.in_year(2024).get(canteen=satellite_2).generated_from_groupe_diagnostic, True
        )
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )

        # TODO :  Diagnostic central is ignored

    # TESTS TO DO :
    # def test_central_serving_teledeclare_diagnostic_are_generated(self):
    # def test_command_delete_previous_generated_diagnostics(self):
    # def test_command_split_appro_for_satellites_is_correct(self):
    # def test_other_year_diagnostics_are_not_modified(self):
    # def test_sat_with_diagnostic_not_teledeclared_is_overwritten(self):
    # def test_sat_with_diagnostic_teledeclared_is_overwritten(self):
    # def test_sat_with_two_diagnostics(self):
    # def test_generated_diagnostics_contains_canteen_data(self):
    # renommer le fichier pour préciser 1TD1Site
