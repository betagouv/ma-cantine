from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from django.db.models.signals import post_save

from data.models.canteen import Canteen, fill_geo_fields_from_siret
from data.models import Diagnostic
from data.models.sector import Sector
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory


class Teledeclaration1Td1SiteScriptGenerationTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @authenticate
    def test_correct_number_of_diagnostics_generated_for_central(self):
        """
        The script should generate one diagnostic for each satellite saved in snapshot.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )

    @authenticate
    def test_correct_number_of_diagnostics_generated_for_central_serving(self):
        """
        The script should generate one diagnostic for each satellite saved in snapshot (the central serving is already in the snapshot)
        """
        central_serving = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_serving.siret
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_serving_diagnostic = DiagnosticFactory(
                canteen=central_serving,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_serving_diagnostic.teledeclare(applicant=authenticate.user)
            # Need to add satellites to the snapshot with groupe migration
            call_command("canteen_migrate_central_to_groupe", apply=True)

        # Before the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )

    @authenticate
    def test_when_script_run_again_delete_previous_generated_diagnostics(self):
        """
        Test that when the script is run again, it deletes the previous generated diagnostics and create one.
        """
        central_1 = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        central_2 = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_1.siret
        )
        satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_2.siret
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_1_diagnostic = DiagnosticFactory(
                canteen=central_1,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_2_diagnostic = DiagnosticFactory(
                canteen=central_2,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_1_diagnostic.teledeclare(applicant=authenticate.user)
            central_2_diagnostic.teledeclare(applicant=authenticate.user)

        # Before the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)

        # Run the script first time
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 4)
        first_time_generated_diagnostic_satellite_1 = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        first_time_generated_diagnostic_satellite_2 = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_2, generated_from_groupe_diagnostic=True)
        )

        # Re-run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 4)
        second_time_generated_diagnostic_satellite_1 = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        second_time_generated_diagnostic_satellite_2 = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_2, generated_from_groupe_diagnostic=True)
        )

        # The generated diagnostics are incremented
        self.assertNotEqual(
            first_time_generated_diagnostic_satellite_1.id, second_time_generated_diagnostic_satellite_1.id
        )
        self.assertNotEqual(
            first_time_generated_diagnostic_satellite_2.id, second_time_generated_diagnostic_satellite_2.id
        )

    @authenticate
    def test_tag_satellites_with_teledeclaration_and_teledeclare_by_central_mode_all(self):
        """
        Test when a satellite canteen has a teledeclaration, and it's also teledeclared by the central the script tags it as doublon.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=None)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite.central_producer_siret = central.siret
            satellite.save(skip_validations=True)
            self.assertEqual(satellite.central_producer_siret, central.siret)
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        satellite_diagnostic.refresh_from_db()
        self.assertFalse(satellite_diagnostic.generated_from_groupe_diagnostic)
        self.assertIn(Diagnostic.InvalidReason.DOUBLON_1TD1SITE, satellite_diagnostic.invalid_reason_list)

    @authenticate
    def test_tag_satellites_with_teledeclaration_and_teledeclare_by_central_mode_appro(self):
        """
        Test when a satellite canteen has a teledeclaration, and it's also teledeclared by the central with mode "appro only" the script does not tag it as doublon.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=None)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite.central_producer_siret = central.siret
            satellite.save(skip_validations=True)
            self.assertEqual(satellite.central_producer_siret, central.siret)
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        satellite_diagnostic.refresh_from_db()
        self.assertFalse(satellite_diagnostic.generated_from_groupe_diagnostic)
        self.assertIn(Diagnostic.InvalidReason.DOUBLON_1TD1SITE, satellite_diagnostic.invalid_reason_list)

    @authenticate
    def test_when_script_run_again_remove_tag_doublon(self):
        """
        If a satellite has the tag "DOUBLON_1TD1SITE" when the script is re-run, it should be removed.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=None)
        with freeze_time("2025-03-29"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)
            satellite.central_producer_siret = central.siret
            satellite.save(skip_validations=True)
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(invalid_reason_list__contains=[Diagnostic.InvalidReason.DOUBLON_1TD1SITE])
            .count(),
            1,
        )

        # Update de SAT
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic.cancel()
            satellite.central_producer_siret = None
            satellite.save(skip_validations=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(invalid_reason_list__contains=[Diagnostic.InvalidReason.DOUBLON_1TD1SITE])
            .count(),
            1,
        )

        # Teledeclare the central again but without the satellite
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Re-run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(invalid_reason_list__contains=[Diagnostic.InvalidReason.DOUBLON_1TD1SITE])
            .count(),
            0,
        )

    @authenticate
    def test_when_central_is_deleted_has_satellite_teledeclarations(self):
        """
        Test when a central is deleted after the teledeclaration, the script still generates diagnostics for its satellites.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, siret="19622299600015")
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        central.delete()

        # Before the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )

    @authenticate
    def test_when_satellite_is_deleted_has_teledeclaration(self):
        """
        Test when a satellite is deleted after the teledeclaration, it still has a generated diagnostic.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, siret="19622299600015")
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_1.delete()

        # Before the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )

    @authenticate
    def test_when_satellite_is_hard_deleted_has_teledeclaration(self):
        """
        Test when a satellite is hard deleted after the teledeclaration, it still has a generated diagnostic.
        Note: hard delete is not possible anymore
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, siret="19622299600015")
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_1.hard_delete()

        # Before the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 2
        )


class Teledeclaration1Td1SiteTeledeclarationFieldsTest(TestCase):
    @authenticate
    def test_empty_satellites_snapshot(self):
        """
        The satellites_snapshot should be empty for the generated diagnostics.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=satellite)
        self.assertIsNone(diagnostic_generated.satellites_snapshot)

    @authenticate
    def test_update_teledeclaration_mode(self):
        """
        Test the teledeclaration_mode value is updated in the generated diagnostics.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = (
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True)
        )
        for diagnostic in diagnostic_generated:
            self.assertEqual(diagnostic.teledeclaration_mode, Diagnostic.TeledeclarationMode.SITE)

    @authenticate
    def test_copy_teledeclaration_metadata(self):
        """
        The metadata from the central diagnostic are copied in the generated diagnostics.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=satellite)
        diagnostic_central = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=central)
        self.assertEqual(diagnostic_generated.teledeclaration_id, diagnostic_central.teledeclaration_id)
        self.assertEqual(diagnostic_generated.teledeclaration_date, diagnostic_central.teledeclaration_date)
        self.assertEqual(diagnostic_generated.teledeclaration_version, diagnostic_central.teledeclaration_version)

    @authenticate
    def test_copy_applicant_informations(self):
        """
        The applicant informations from the central diagnostic are copied in the generated diagnostics.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=satellite)
        diagnostic_central = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=central)
        self.assertEqual(diagnostic_generated.applicant_snapshot, diagnostic_central.applicant_snapshot)
        self.assertEqual(diagnostic_generated.applicant, diagnostic_central.applicant)

    @authenticate
    def test_copy_invalid_reason_list(self):
        """
        The invalid reason list from the central diagnostic are copied in the generated diagnostics.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2,
                invalid_reason_list=[
                    Diagnostic.InvalidReason.VALEURS_INCOHERENTES
                ],  # Fake invalid reason list is added
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite, generated_from_groupe_diagnostic=True)
        )
        self.assertEqual(diagnostic_generated.invalid_reason_list, central_diagnostic.invalid_reason_list)


class Teledeclaration1Td1SiteCanteenFieldsTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @authenticate
    def test_keep_history_canteen_fields(self):
        """
        The historical values of the canteen when the teledeclaration is done are kept in the generated diagnostics (don't use the current values).
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            # factory build + save: to circumvent the factory and create a history entry
            central = CanteenFactory.build(
                production_type=Canteen.ProductionType.CENTRAL, siret="21340172201787", city_insee_code="34172"
            )
            central.save()
            satellite_siret = CanteenFactory.build(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                central_producer_siret=central.siret,
                name="Mon premier nom SIRET",
                siret="33533639200154",
                economic_model=Canteen.EconomicModel.PUBLIC,
                management_type=Canteen.ManagementType.CONCEDED,
            )
            satellite_siret.save()
            satellite_siren = CanteenFactory.build(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                central_producer_siret=central.siret,
                name="Mon premier nom SIREN",
                siret=None,
                siren_unite_legale="123456789",
                economic_model=Canteen.EconomicModel.PUBLIC,
                management_type=Canteen.ManagementType.CONCEDED,
            )
            satellite_siren.save()
        with freeze_time("2025-03-31"):  # during the 2024 campaign (1 day later)
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Change satellite informations
        satellite_siret.name = "Mon nouveau nom SIRET"
        satellite_siret.siret = "12345678900002"
        satellite_siret.economic_model = Canteen.EconomicModel.PRIVATE
        satellite_siret.management_type = Canteen.ManagementType.DIRECT
        satellite_siret.production_type = Canteen.ProductionType.ON_SITE  # Make it autonomous
        satellite_siret.save(skip_validations=True)
        satellite_siren.siren_unite_legale = "1234567890"
        satellite_siren.save(skip_validations=True)
        satellite_siren.refresh_from_db()
        satellite_siret.refresh_from_db()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_satellite_siret = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_siret, generated_from_groupe_diagnostic=True)
        )
        diagnostic_satellite_siren = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_siren, generated_from_groupe_diagnostic=True)
        )

        # Old values are present in the generated fields for SIRET SAT
        siret_canteen_snapshot = diagnostic_satellite_siret.canteen_snapshot
        self.assertEqual(siret_canteen_snapshot["siret"], "33533639200154")
        self.assertEqual(siret_canteen_snapshot["name"], "Mon premier nom SIRET")
        self.assertEqual(siret_canteen_snapshot["production_type"], Canteen.ProductionType.ON_SITE_CENTRAL)
        self.assertEqual(siret_canteen_snapshot["economic_model"], Canteen.EconomicModel.PUBLIC)
        self.assertEqual(siret_canteen_snapshot["management_type"], Canteen.ManagementType.CONCEDED)
        # Old values are present in the generated fields for SIREN SAT
        siren_canteen_snapshot = diagnostic_satellite_siren.canteen_snapshot
        self.assertEqual(siren_canteen_snapshot["siren_unite_legale"], "123456789")

    @authenticate
    def test_copy_central_fields(self):
        """
        Some informations from the central are copied in the canteen_snapshot of the generated diagnostics: geodata, sector and line ministry.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
            city_insee_code="75056",
            department="75",
            region="11",
        )
        central.sector_list = [Sector.EDUCATION_AUTRE]
        central.line_ministry = Canteen.Ministries.AFFAIRES_ETRANGERES
        central.save(skip_validations=True)

        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            line_ministry=None,  # No line ministry for the satellite
            city_insee_code=None,  # No city insee code for the satellite
            department=None,  # No department for the satellite
            region=None,  # No region for the satellite
            economic_model=Canteen.EconomicModel.PRIVATE,  # Private economic model for the satellite
        )
        satellite.sector_list = []
        satellite.save(skip_validations=True)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.objects.in_year(2024).get(
            canteen=satellite, generated_from_groupe_diagnostic=True
        )

        # Fields to be copied
        field_to_be_copied = [
            "city_insee_code",
            "department",
            "region",
            "sector_list",
            "line_ministry",
        ]

        for field in field_to_be_copied:
            with self.subTest(field=field):
                self.assertEqual(diagnostic_generated.canteen_snapshot[field], getattr(central, field))

    @authenticate
    def test_divide_meal_count_by_number_of_satellites(self):
        """
        The yearly meal count is divided by the number of satellites, value not rounded keep decimal.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=1011)
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            yearly_meal_count=420,
        )
        satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
        )
        satellite_2.yearly_meal_count = None
        satellite_2.save(skip_validations=True)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        number_of_satellites = 2
        satellite_1_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        satellite_2_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_2, generated_from_groupe_diagnostic=True)
        )

        expected_yearly_meal_count = int(
            central_diagnostic.canteen_snapshot["yearly_meal_count"] / number_of_satellites
        )
        self.assertIsNotNone(satellite_2_diagnostic.canteen_snapshot["yearly_meal_count"])
        self.assertEqual(int(satellite_1_diagnostic.canteen_snapshot["yearly_meal_count"]), expected_yearly_meal_count)
        self.assertEqual(int(satellite_2_diagnostic.canteen_snapshot["yearly_meal_count"]), expected_yearly_meal_count)

    @authenticate
    def test_keep_history_meal_count(self):
        """
        If the central changes its yearly meal count after the teledeclaraiont, the script uses the old value.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=1000, daily_meal_count=100
        )
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            yearly_meal_count=420,
        )
        satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            yearly_meal_count=420,
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Change the meal count of the central
        central.yearly_meal_count = 9999
        central.save(skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        number_of_satellites = 2
        satellite_1_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        satellite_2_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite_2, generated_from_groupe_diagnostic=True)
        )

        expected_yearly_meal_count = central_diagnostic.canteen_snapshot["yearly_meal_count"] / number_of_satellites

        self.assertEqual(satellite_1_diagnostic.canteen_snapshot["yearly_meal_count"], expected_yearly_meal_count)
        self.assertEqual(satellite_2_diagnostic.canteen_snapshot["yearly_meal_count"], expected_yearly_meal_count)

    @authenticate
    def test_meal_count_is_none(self):
        """
        Test that when the central has a None yearly meal count, the script generates a diagnostic with a None value.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        central.yearly_meal_count = None
        central.save(skip_validations=True)
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            yearly_meal_count=420,
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(canteen=central, year=2024, valeur_totale=10000, valeur_bio=2000)
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        satellite_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite, generated_from_groupe_diagnostic=True)
        )
        self.assertIsNone(satellite_diagnostic.canteen_snapshot["yearly_meal_count"])


class Teledeclaration1Td1SiteTunnelFieldsValuesTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @classmethod
    def setUpTestData(cls):
        cls.central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        cls.satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.central.siret,
        )
        cls.satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.central.siret,
            siret=None,
            siren_unite_legale="123456789",
        )

        cls.appro_fields = {}
        for field in Diagnostic.SIMPLE_APPRO_FIELDS:
            cls.appro_fields[field] = 10000.50
        for field in Diagnostic.COMPLETE_APPRO_FIELDS:
            cls.appro_fields[field] = 500.75

    def verify_field_are_equals(self, value, expected_value):
        value_cleaned = float(value)
        expected_value_cleaned = round(expected_value, 2)
        self.assertEqual(value_cleaned, expected_value_cleaned)

    def verify_appro_fields_divided(self, fields, divisor, central_diagnostic, sat_diagnostics_generated):
        for index, sat_diagnostic in enumerate(sat_diagnostics_generated):
            with self.subTest(sat_diagnostic_index=index):
                for field in fields:
                    with self.subTest(field=field):
                        central_value = getattr(central_diagnostic, field)
                        diagnostic_value = getattr(sat_diagnostic, field)
                        self.assertIsNotNone(central_value)
                        self.assertIsNotNone(diagnostic_value)
                        self.verify_field_are_equals(diagnostic_value, central_value / divisor)

    @authenticate
    def test_total_value_divided_by_number_of_satellites(self):
        """
        Test that the total value is divided by the number of satellites.
        """
        total_value = 15000.50
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                valeur_totale=total_value,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        self.verify_field_are_equals(sat_1_diagnostic.valeur_totale, total_value / 2)
        self.verify_field_are_equals(sat_2_diagnostic.valeur_totale, total_value / 2)

    @authenticate
    def test_central_type_simple(self):
        """
        Test that when a central canteen teledeclares with mode ALL.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.APPRO_1TD1SITE_FIELDS,
            number_of_generated_diagnostics,
            central_diagnostic,
            sat_diagnostics_generated,
        )

    @authenticate
    def test_central_serving_type_simple(self):
        """
        Test that when a central serving canteen teledeclares with mode ALL.
        """
        # Change the production type of the central to central serving
        self.central.production_type = Canteen.ProductionType.CENTRAL_SERVING
        self.central.save(skip_validations=True)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)
            # Need to add satellites to the snapshot with groupe migration
            call_command("canteen_migrate_central_to_groupe", apply=True)
            # Save satellite canteen created
            new_canteen_id = central_diagnostic.satellites_snapshot[len(central_diagnostic.satellites_snapshot) - 1][
                "id"
            ]
            sat_created = Canteen.objects.get(id=new_canteen_id)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_3_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=sat_created)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic, sat_3_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.APPRO_1TD1SITE_FIELDS,
            number_of_generated_diagnostics,
            central_diagnostic,
            sat_diagnostics_generated,
        )

    @authenticate
    def test_central_type_complete(self):
        """
        Test that when a central canteen teledeclares in mode ALL with COMPLETE type.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.APPRO_1TD1SITE_FIELDS,
            number_of_generated_diagnostics,
            central_diagnostic,
            sat_diagnostics_generated,
        )

    @authenticate
    def test_central_serving_type_complete(self):
        """
        Test that when a central serving canteen teledeclares with mode ALL.
        """
        # Change the production type of the central to central serving
        self.central.production_type = Canteen.ProductionType.CENTRAL_SERVING
        self.central.save(skip_validations=True)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)
            # Need to add satellites to the snapshot with groupe migration
            call_command("canteen_migrate_central_to_groupe", apply=True)
            # Save satellite canteen created
            new_canteen_id = central_diagnostic.satellites_snapshot[len(central_diagnostic.satellites_snapshot) - 1][
                "id"
            ]
            sat_created = Canteen.objects.get(id=new_canteen_id)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_3_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=sat_created)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic, sat_3_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.APPRO_1TD1SITE_FIELDS,
            number_of_generated_diagnostics,
            central_diagnostic,
            sat_diagnostics_generated,
        )

    @authenticate
    def test_central_no_type(self):
        """
        Test that when a central canteen teledeclares without mode.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=None,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.APPRO_1TD1SITE_FIELDS,
            number_of_generated_diagnostics,
            central_diagnostic,
            sat_diagnostics_generated,
        )

    @authenticate
    def test_central_serving_no_type(self):
        """
        Test that when a central serving canteen teledeclares with no type.
        """
        # Change the production type of the central to central serving
        self.central.production_type = Canteen.ProductionType.CENTRAL_SERVING
        self.central.save(skip_validations=True)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=None,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)
            # Need to add satellites to the snapshot with groupe migration
            call_command("canteen_migrate_central_to_groupe", apply=True)
            # Save satellite canteen created
            new_canteen_id = central_diagnostic.satellites_snapshot[len(central_diagnostic.satellites_snapshot) - 1][
                "id"
            ]
            sat_created = Canteen.objects.get(id=new_canteen_id)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_3_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=sat_created)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic, sat_3_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.APPRO_1TD1SITE_FIELDS,
            number_of_generated_diagnostics,
            central_diagnostic,
            sat_diagnostics_generated,
        )

    @authenticate
    def test_mode_all_non_appro_fields_are_copied(self):
        """
        Test that when a central canteen teledeclares in mode ALL with non appro fields, the values are copied in the generated diagnostics.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]

        for sat_diagnostic in sat_diagnostics_generated:
            with self.subTest(sat_diagnostic=sat_diagnostic):
                for field in Diagnostic.NON_APPRO_FIELDS:
                    with self.subTest(field=field):
                        self.assertEqual(getattr(sat_diagnostic, field), getattr(central_diagnostic, field))


class Teledeclaration1Td1SiteNotConcernedByScriptTest(TestCase):
    """
    Test the teledeclaration of canteen or diagnostic not concerned by the 1td1site script are not modified when the command is run.
    """

    @authenticate
    def test_canteen_site(self):
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

        diagnostic_site_1_before_script = diagnostic_site_1
        diagnostic_site_2_before_script = diagnostic_site_2

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        diagnostic_site_1.refresh_from_db()
        diagnostic_site_2.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(diagnostic_site_1, diagnostic_site_1_before_script)
        self.assertEqual(diagnostic_site_2, diagnostic_site_2_before_script)

    @authenticate
    def test_satellite_with_central_siret_unknown(self):
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

        satellite_diagnostic_before_script = satellite_diagnostic

        # Before the script is run
        self.assertEqual(
            Canteen.objects.filter(siret="19622299600015").count(), 0
        )  # no central canteen exist with the siret used in sat
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        satellite_diagnostic.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(satellite_diagnostic, satellite_diagnostic_before_script)

    @authenticate
    def test_satellite_with_central_siret_empty(self):
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="")
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_snapshot_canteen_before_script = satellite_diagnostic.canteen_snapshot
        satellite_snapshot_satellites_before_script = satellite_diagnostic.satellites_snapshot

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        satellite_diagnostic.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(satellite_diagnostic.canteen_snapshot, satellite_snapshot_canteen_before_script)
        self.assertEqual(satellite_diagnostic.satellites_snapshot, satellite_snapshot_satellites_before_script)

    @authenticate
    def test_teledeclaration_other_year_are_not_generated(self):
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)

        with freeze_time("2024-03-30"):  # during the 2023 campaign
            central_diagnostic_2023 = DiagnosticFactory(
                canteen=central,
                year=2023,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic_2023.teledeclare(applicant=authenticate.user)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic_2024 = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic_2024.teledeclare(applicant=authenticate.user)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            central_diagnostic_2025 = DiagnosticFactory(
                canteen=central,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic_2025.teledeclare(applicant=authenticate.user)

        # Before the script is run
        self.assertEqual(Diagnostic.objects.count(), 3)
        self.assertEqual(Diagnostic.objects.in_year(2023).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2025).teledeclared().count(), 1)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.count(), 5)
        self.assertEqual(Diagnostic.objects.in_year(2023).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(Diagnostic.objects.in_year(2025).teledeclared().count(), 1)

    @authenticate
    def test_central_without_satellites(self):
        """
        Test that when a central canteen has no satellites, the script does not generate any diagnostic.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)

    @authenticate
    def test_central_with_diagnostic_not_teledeclared(self):
        """
        Test that when a diagnostic is draft, it is not modified when the script is run.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
            )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 0)
        self.assertEqual(Diagnostic.objects.in_year(2024).filter(generated_from_groupe_diagnostic=True).count(), 0)

    @authenticate
    def test_cancelled_central_diagnostics(self):
        """
        If a teledeclaration is cancelled, no diagnostics should be generated.
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)
            central_diagnostic.cancel()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 0)
        self.assertEqual(Diagnostic.objects.in_year(2024).filter(generated_from_groupe_diagnostic=True).count(), 0)
