from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from django.db.models.signals import post_save

from data.models.canteen import Canteen, fill_geo_fields_from_siret
from data.models import Diagnostic
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class TeledeclarationSubmitOutsideOfCampaignScriptTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @authenticate
    def test_submit_single_diagnostic_after_campaign(self):
        canteen = CanteenFactory(name="First name", city_insee_code="38185")

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(
                canteen=canteen,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)
            self.assertEqual(diagnostic.applicant, authenticate.user)

    @authenticate
    def test_submit_multiple_diagnostics_after_campaign(self):
        canteen_1 = CanteenFactory()
        canteen_2 = CanteenFactory()
        canteen_3 = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_1 = DiagnosticFactory(canteen=canteen_1, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic_2 = DiagnosticFactory(canteen=canteen_2, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic_3 = DiagnosticFactory(canteen=canteen_3, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script with multiple diagnostic IDs
            diagnostic_ids = f"{diagnostic_1.id},{diagnostic_2.id},{diagnostic_3.id}"
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=diagnostic_ids,
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script
            diagnostic_1.refresh_from_db()
            diagnostic_2.refresh_from_db()
            diagnostic_3.refresh_from_db()

            self.assertTrue(diagnostic_1.is_teledeclared)
            self.assertTrue(diagnostic_2.is_teledeclared)
            self.assertTrue(diagnostic_3.is_teledeclared)

    @authenticate
    def test_cannot_submit_diagnostic_before_campaign(self):
        canteen = CanteenFactory()

        with freeze_time("2025-01-01"):  # before the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the diagnostic should not be teledeclared
            diagnostic.refresh_from_db()
            self.assertFalse(diagnostic.is_teledeclared)

    @authenticate
    def test_submit_diagnostic_during_campaign(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the diagnostic should be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    def test_submit_diagnostic_during_correction_campaign(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

        with freeze_time("2025-04-17"):  # during the 2024 correction campaign
            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the diagnostic should be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_from_different_year(self):
        canteen = CanteenFactory()
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

        with freeze_time("2026-04-15"):  # during the 2025 campaign
            diagnostic_2025 = DiagnosticFactory(canteen=canteen, year=2025, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)
            self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 0)

        with freeze_time("2026-08-30"):  # after the 2025 campaign
            # Run the script with 2024 year, but pass 2025 diagnostic ID
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic_2025.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, 2025 diagnostic should not be affected
            diagnostic_2025.refresh_from_db()
            self.assertFalse(diagnostic_2025.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_teledeclared(self):
        canteen_1 = CanteenFactory()
        canteen_2 = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic_teledeclared = DiagnosticFactory(
                canteen=canteen_1, year=2024, valeur_totale=10000, valeur_bio=2000
            )
            diagnostic_teledeclared.teledeclare(applicant=authenticate.user)
            diagnostic_not_teledeclared = DiagnosticFactory(
                canteen=canteen_2, year=2024, valeur_totale=10000, valeur_bio=2000
            )

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
            self.assertFalse(diagnostic_not_teledeclared.is_teledeclared)

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script with both diagnostic IDs
            diagnostic_ids = f"{diagnostic_teledeclared.id},{diagnostic_not_teledeclared.id}"
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=diagnostic_ids,
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the teledeclared one should not be affected
            diagnostic_teledeclared.refresh_from_db()
            diagnostic_not_teledeclared.refresh_from_db()

            self.assertTrue(diagnostic_teledeclared.is_teledeclared)
            self.assertTrue(diagnostic_not_teledeclared.is_teledeclared)

    @authenticate
    def test_skip_diagnostic_not_found(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script with a mix of valid and non-existent diagnostic IDs
            fake_id = 99999
            diagnostic_ids = f"{diagnostic.id},{fake_id}"
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=diagnostic_ids,
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the valid diagnostic should be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    def test_submit_diagnostic_even_if_diagnostic_validation_error(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

            # Change the diagnostic to make it invalid
            Diagnostic.objects.filter(id=diagnostic.id).update(valeur_totale=0)
            diagnostic.refresh_from_db()
            self.assertFalse(diagnostic.is_filled)  # property

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the diagnostic should be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    def test_submit_diagnostic_even_if_canteen_validation_error(self):
        canteen = CanteenFactory()

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=canteen, year=2024, valeur_totale=10000, valeur_bio=2000)
            diagnostic.teledeclare(applicant=authenticate.user)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)

            # Change the canteen to make it invalid
            canteen.city_insee_code = None
            canteen.save()
            self.assertFalse(canteen.is_filled)  # model field

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the diagnostic should be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    def test_submit_diagnostic_even_if_satellite_validation_error(self):
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic = DiagnosticFactory(canteen=groupe, year=2024, valeur_totale=10000, valeur_bio=2000)

            # Before running the script
            self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 0)

            # Change the satellite canteen to make it invalid
            satellite.city_insee_code = None
            satellite.save()
            self.assertFalse(satellite.is_filled)  # model field

        with freeze_time("2025-08-30"):  # after the 2024 campaign
            # Run the script
            call_command(
                "teledeclaration_submit_outside_of_campaign",
                year=2024,
                diagnostic_id_list=str(diagnostic.id),
                applicant_id=authenticate.user.id,
                apply=True,
            )

            # After running the script, the diagnostic should be teledeclared
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)
