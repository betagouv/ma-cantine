from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from django.db.models.signals import post_save

from data.models.canteen import Canteen, fill_geo_fields_from_siret
from data.models import Diagnostic
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class TeledeclarationResubmitScriptTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @authenticate
    def test_resubmit_single_diagnostic(self):
        """
        The script should resubmit a single teledeclared diagnostic.
        """
        canteen = CanteenFactory(name="First name", city_insee_code="38185")
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(
                canteen=canteen,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            diagnostic.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.canteen_snapshot["name"], "First name")
            self.assertEqual(diagnostic.canteen_snapshot["city_insee_code"], "38185")
            original_diagnostic_id = diagnostic.id
            original_teledeclaration_date = diagnostic.teledeclaration_date

            # we make some changes on the canteen
            canteen.name = "New name"
            canteen.city_insee_code = "34172"
            canteen.save()

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=str(diagnostic.id))

            # After running the script
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.id, original_diagnostic_id)
            self.assertTrue(diagnostic.is_teledeclared)
            self.assertNotEqual(diagnostic.teledeclaration_date, original_teledeclaration_date)
            self.assertEqual(diagnostic.canteen_snapshot["name"], "New name")
            self.assertEqual(diagnostic.canteen_snapshot["city_insee_code"], "34172")

    @authenticate
    def test_resubmit_multiple_diagnostics(self):
        """
        The script should resubmit multiple teledeclared diagnostics.
        """
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
            # Run the script with multiple diagnostic IDs
            diagnostic_ids = f"{diagnostic_1.id},{diagnostic_2.id},{diagnostic_3.id}"
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=diagnostic_ids)

            # After running the script
            diagnostic_1.refresh_from_db()
            diagnostic_2.refresh_from_db()
            diagnostic_3.refresh_from_db()

            self.assertTrue(diagnostic_1.is_teledeclared)
            self.assertTrue(diagnostic_2.is_teledeclared)
            self.assertTrue(diagnostic_3.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_from_different_year(self):
        """
        The script should skip diagnostics that are from a different year than specified.
        """
        canteen = CanteenFactory()
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_2024 = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic_2024.teledeclare(applicant=authenticate.user)

        with freeze_time("2026-04-15"):  # during the 2025 campaign
            diagnostic_2025 = DiagnosticFactory(canteen=canteen, year=2025, valeur_totale=10000, valeur_bio=2000)
            diagnostic_2025.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)

        with freeze_time("2026-04-17"):  # during the 2025 correction campaign
            # Run the script with 2024 year, but pass 2025 diagnostic ID
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=str(diagnostic_2025.id))

            # After running the script, 2025 diagnostic should not be affected
            diagnostic_2025.refresh_from_db()
            self.assertTrue(diagnostic_2025.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_not_teledeclared(self):
        """
        The script should skip diagnostics that are not teledeclared.
        """
        canteen_1 = CanteenFactory()
        canteen_2 = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_teledeclared = DiagnosticFactory(
                canteen=canteen_1, year=2024, valeur_totale=10000, valeur_bio=2000
            )
            diagnostic_teledeclared.teledeclare(applicant=authenticate.user)

            # Create a diagnostic that is not teledeclared
            diagnostic_not_teledeclared = DiagnosticFactory(
                canteen=canteen_2, year=2024, valeur_totale=10000, valeur_bio=2000
            )

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            self.assertFalse(diagnostic_not_teledeclared.is_teledeclared)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script with both diagnostic IDs
            diagnostic_ids = f"{diagnostic_teledeclared.id},{diagnostic_not_teledeclared.id}"
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=diagnostic_ids)

            # After running the script, only the teledeclared one should be affected
            diagnostic_teledeclared.refresh_from_db()
            diagnostic_not_teledeclared.refresh_from_db()

            self.assertTrue(diagnostic_teledeclared.is_teledeclared)
            self.assertFalse(diagnostic_not_teledeclared.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_not_found(self):
        """
        The script should gracefully handle non-existent diagnostic IDs by simply skipping them.
        """
        canteen = CanteenFactory()
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script with a mix of valid and non-existent diagnostic IDs
            fake_id = 99999
            diagnostic_ids = f"{diagnostic.id},{fake_id}"
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=diagnostic_ids)

            # After running the script, the valid diagnostic should still be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

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

            # Change the diagnostic to make it invalid
            Diagnostic.objects.filter(id=diagnostic.id).update(
                valeur_totale=500, valeur_bio=1000
            )  # valeur_bio > valeur_totale

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script with the diagnostic ID
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=str(diagnostic.id))

            # After running the script, the diagnostic should still be teledeclared (resubmission failed)
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

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

            # Change the canteen to make it invalid
            Canteen.objects.filter(id=canteen.id).update(city_insee_code=None)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script with the diagnostic ID
            call_command("teledeclaration_resubmit", year=2024, teledeclaration_id_list=str(diagnostic.id))

            # After running the script, the diagnostic should still be teledeclared (resubmission failed)
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)
