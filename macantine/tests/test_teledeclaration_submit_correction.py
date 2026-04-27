from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from django.db.models.signals import post_save

from data.models.canteen import Canteen, fill_geo_fields_from_siret
from data.models import Diagnostic
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class TeledeclarationSubmitCorrectionScriptTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @authenticate
    def test_submit_single_diagnostic_in_correction(self):
        canteen = CanteenFactory(name="First name", city_insee_code="38185")
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(
                canteen=canteen,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            diagnostic.teledeclare(applicant=authenticate.user)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.canteen_snapshot["name"], "First name")
            self.assertEqual(diagnostic.canteen_snapshot["city_insee_code"], "38185")
            original_diagnostic_id = diagnostic.id
            original_teledeclaration_date = diagnostic.teledeclaration_date

            # Make some changes on the canteen
            canteen.name = "New name"
            canteen.city_insee_code = "34172"
            canteen.save()

            # Cancel the teledeclaration
            diagnostic.cancel()

            # Run the script
            call_command("teledeclaration_submit_correction", year=2024)

            # After running the script
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.id, original_diagnostic_id)
            self.assertTrue(diagnostic.is_teledeclared)
            self.assertEqual(diagnostic.applicant, authenticate.user)
            self.assertNotEqual(diagnostic.teledeclaration_date, original_teledeclaration_date)
            self.assertEqual(diagnostic.canteen_snapshot["name"], "New name")
            self.assertEqual(diagnostic.canteen_snapshot["city_insee_code"], "34172")

    @authenticate
    def test_submit_multiple_diagnostics_in_correction(self):
        canteen_1 = CanteenFactory()
        canteen_2 = CanteenFactory()
        canteen_3 = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_1 = DiagnosticFactory(canteen=canteen_1, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic_2 = DiagnosticFactory(canteen=canteen_2, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic_3 = DiagnosticFactory(canteen=canteen_3, year=2024, valeur_totale=10000, valeur_bio=2000)

            diagnostic_1.teledeclare(applicant=authenticate.user)
            diagnostic_2.teledeclare(applicant=authenticate.user)
            diagnostic_3.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 3)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # cancel 2 teledeclarations
            diagnostic_1.cancel()
            diagnostic_2.cancel()

            # Run the script
            call_command("teledeclaration_submit_correction", year=2024)

            # After running the script
            diagnostic_1.refresh_from_db()
            diagnostic_2.refresh_from_db()
            diagnostic_3.refresh_from_db()

            self.assertTrue(diagnostic_1.is_teledeclared)
            self.assertTrue(diagnostic_2.is_teledeclared)
            self.assertTrue(diagnostic_3.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_teledeclared(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_teledeclared = DiagnosticFactory(
                canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000
            )
            diagnostic_teledeclared.teledeclare(applicant=authenticate.user)
            original_teledeclaration_date = diagnostic_teledeclared.teledeclaration_date

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            self.assertTrue(diagnostic_teledeclared.is_teledeclared)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script
            call_command("teledeclaration_submit_correction", year=2024)

            # After running the script, the diagnostic should still be teledeclared (not cancelled and re-teledeclared)
            diagnostic_teledeclared.refresh_from_db()

            self.assertTrue(diagnostic_teledeclared.is_teledeclared)
            self.assertEqual(diagnostic_teledeclared.teledeclaration_date, original_teledeclaration_date)

    @authenticate
    def test_skip_diagnostic_in_draft(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_draft = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            self.assertFalse(diagnostic_draft.is_teledeclared)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script
            call_command("teledeclaration_submit_correction", year=2024)

            # After running the script, the diagnostic should still be in draft (not teledeclared)
            diagnostic_draft.refresh_from_db()

            self.assertFalse(diagnostic_draft.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_if_diagnostic_validation_error(self):
        """
        The script should skip diagnostics that raise a ValidationError during teledeclaration.
        """
        canteen = CanteenFactory()
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)

            # Cancel the teledeclaration
            diagnostic.cancel()

            # Change the diagnostic to make it invalid
            Diagnostic.objects.filter(id=diagnostic.id).update(
                valeur_totale=500, valeur_bio=1000
            )  # valeur_bio > valeur_totale

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script
            call_command("teledeclaration_submit_correction", year=2024)

            # After running the script, the diagnostic should still be in CORRECTION (resubmission failed)
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.CORRECTION)

    @authenticate
    def test_skip_diagnostic_if_canteen_validation_error(self):
        """
        The script should skip diagnostics that raise a ValidationError during teledeclaration.
        """
        canteen = CanteenFactory()
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)

            # Cancel the teledeclaration
            diagnostic.cancel()

            # Change the canteen to make it invalid
            Canteen.objects.filter(id=canteen.id).update(city_insee_code=None)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script
            call_command("teledeclaration_submit_correction", year=2024)

            # After running the script, the diagnostic should still be in CORRECTION (resubmission failed)
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.CORRECTION)
