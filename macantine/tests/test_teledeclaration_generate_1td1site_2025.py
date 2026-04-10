from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time
from django.utils import timezone
from django.db.models.signals import post_save

from data.models.canteen import Canteen, fill_geo_fields_from_siret
from data.models import Diagnostic
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
    def test_correct_number_of_diagnostics_generated_for_groupe(self):
        """
        The script should generate one diagnostic for each satellite saved in snapshot.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 3)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            0,
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            2,
        )

    @authenticate
    def test_when_script_run_again_delete_previous_generated_diagnostics(self):
        """
        Test that when the script is run again, it deletes the previous generated diagnostics and create one.
        """
        groupe_1 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        groupe_2 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite_1 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe_1)
        satellite_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe_2)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_1_diagnostic = DiagnosticFactory(
                canteen=groupe_1,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_2_diagnostic = DiagnosticFactory(
                canteen=groupe_2,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_1_diagnostic.teledeclare(applicant=authenticate.user)
            groupe_2_diagnostic.teledeclare(applicant=authenticate.user)

        # Before the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 2)

        # Run the script first time
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 4)
        first_time_generated_diagnostic_satellite_1 = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        first_time_generated_diagnostic_satellite_2 = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite_2, generated_from_groupe_diagnostic=True)
        )

        # Re-run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 4)
        second_time_generated_diagnostic_satellite_1 = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        second_time_generated_diagnostic_satellite_2 = (
            Diagnostic.all_objects.in_year(2025)
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
    def test_tag_satellites_with_teledeclaration_and_teledeclare_by_groupe_mode_all(self):
        """
        Test when a satellite canteen has a teledeclaration, and it's also teledeclared by the groupe the script tags it as doublon.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=None)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            satellite.groupe = groupe
            satellite.save(skip_validations=True)
            self.assertEqual(satellite.groupe, groupe)
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 2)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_diagnostic.refresh_from_db()
        self.assertFalse(satellite_diagnostic.generated_from_groupe_diagnostic)
        self.assertIn(Diagnostic.InvalidReason.DOUBLON_1TD1SITE, satellite_diagnostic.invalid_reason_list)

    @authenticate
    def test_tag_satellites_with_teledeclaration_and_teledeclare_by_groupe_mode_appro(self):
        """
        Test when a satellite canteen has a teledeclaration, and it's also teledeclared by the groupe with mode "appro only" the script does not tag it as doublon.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=None)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            satellite.groupe = groupe
            satellite.save(skip_validations=True)
            self.assertEqual(satellite.groupe, groupe)
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 2)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_diagnostic.refresh_from_db()
        self.assertFalse(satellite_diagnostic.generated_from_groupe_diagnostic)
        self.assertIn(Diagnostic.InvalidReason.DOUBLON_1TD1SITE, satellite_diagnostic.invalid_reason_list)

    @authenticate
    def test_when_script_run_again_remove_tag_doublon(self):
        """
        If a satellite has the tag "DOUBLON_1TD1SITE" when the script is re-run, it should be removed.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=None)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            satellite_diagnostic = DiagnosticFactory(
                canteen=satellite,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            satellite_diagnostic.teledeclare(applicant=authenticate.user)
            satellite.groupe = groupe
            satellite.save(skip_validations=True)
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .filter(invalid_reason_list__contains=[Diagnostic.InvalidReason.DOUBLON_1TD1SITE])
            .count(),
            1,
        )

        # Update de SAT
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic.cancel()
            satellite.groupe = None
            satellite.save(skip_validations=True)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .filter(invalid_reason_list__contains=[Diagnostic.InvalidReason.DOUBLON_1TD1SITE])
            .count(),
            1,
        )

        # Commented because a groupe without satellite cannot teledeclare
        # # Teledeclare the groupe again but without the satellite
        # with freeze_time("2026-03-30"):  # during the 2025 campaign
        #     groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Re-run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .filter(invalid_reason_list__contains=[Diagnostic.InvalidReason.DOUBLON_1TD1SITE])
            .count(),
            0,
        )

    @authenticate
    def test_when_groupe_is_deleted_has_satellite_teledeclarations(self):
        """
        Test when a groupe is deleted after the teledeclaration, the script still generates diagnostics for its satellites.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # groupe.delete()
        Canteen.objects.filter(id=groupe.id).update(deletion_date=timezone.now())

        # Before the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            0,
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            2,
        )

    @authenticate
    def test_when_satellite_is_deleted_has_teledeclaration(self):
        """
        Test when a satellite is deleted after the teledeclaration, it still has a generated diagnostic.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite_1 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_1.delete()

        # Before the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            0,
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            2,
        )

    @authenticate
    def test_when_satellite_is_hard_deleted_has_teledeclaration(self):
        """
        Test when a satellite is hard deleted after the teledeclaration, it still has a generated diagnostic.
        Note: hard delete is not possible anymore
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite_1 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        satellite_1.hard_delete()

        # Before the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            0,
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 3)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            2,
        )


class Teledeclaration1Td1SiteTeledeclarationFieldsTest(TestCase):
    @authenticate
    def test_empty_satellites_snapshot(self):
        """
        The satellites_snapshot should be empty for the generated diagnostics.
        """
        groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, yearly_meal_count=1011, daily_meal_count=3
        )
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=satellite)
        self.assertIsNone(diagnostic_generated.satellites_snapshot)

    @authenticate
    def test_update_teledeclaration_mode(self):
        """
        Test the teledeclaration_mode value is updated in the generated diagnostics.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_generated = (
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True)
        )
        for diagnostic in diagnostic_generated:
            self.assertEqual(diagnostic.teledeclaration_mode, Diagnostic.TeledeclarationMode.SITE)

    @authenticate
    def test_copy_teledeclaration_metadata(self):
        """
        The metadata from the groupe diagnostic are copied in the generated diagnostics.
        """
        groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, yearly_meal_count=1011, daily_meal_count=3
        )
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=satellite)
        diagnostic_groupe = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=groupe)
        self.assertEqual(diagnostic_generated.teledeclaration_id, diagnostic_groupe.teledeclaration_id)
        self.assertEqual(diagnostic_generated.teledeclaration_date, diagnostic_groupe.teledeclaration_date)
        self.assertEqual(diagnostic_generated.teledeclaration_version, diagnostic_groupe.teledeclaration_version)

    @authenticate
    def test_copy_applicant_informations(self):
        """
        The applicant informations from the groupe diagnostic are copied in the generated diagnostics.
        """
        groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, yearly_meal_count=1011, daily_meal_count=3
        )
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=satellite)
        diagnostic_groupe = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=groupe)
        self.assertEqual(diagnostic_generated.applicant_snapshot, diagnostic_groupe.applicant_snapshot)
        self.assertEqual(diagnostic_generated.applicant, diagnostic_groupe.applicant)

    @authenticate
    def test_copy_invalid_reason_list(self):
        """
        The invalid reason list from the groupe diagnostic are copied in the generated diagnostics.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2,
                invalid_reason_list=[
                    Diagnostic.InvalidReason.VALEURS_INCOHERENTES
                ],  # Fake invalid reason list is added
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_generated = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite, generated_from_groupe_diagnostic=True)
        )
        self.assertEqual(diagnostic_generated.invalid_reason_list, groupe_diagnostic.invalid_reason_list)


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
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            # factory build + save: to circumvent the factory and create a history entry
            groupe = CanteenFactory.build(production_type=Canteen.ProductionType.GROUPE)
            groupe.save()
            satellite_siret = CanteenFactory.build(
                name="Mon premier nom SIRET",
                siret="33533639200154",
                groupe=groupe,
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                economic_model=Canteen.EconomicModel.PUBLIC,
                management_type=Canteen.ManagementType.CONCEDED,
            )
            satellite_siret.save()
            satellite_siren = CanteenFactory.build(
                name="Mon premier nom SIREN",
                siret=None,
                siren_unite_legale="123456789",
                groupe=groupe,
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                economic_model=Canteen.EconomicModel.PUBLIC,
                management_type=Canteen.ManagementType.CONCEDED,
            )
            satellite_siren.save()
        with freeze_time("2026-03-31"):  # during the 2025 campaign (1 day later)
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

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
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_satellite_siret = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite_siret, generated_from_groupe_diagnostic=True)
        )
        diagnostic_satellite_siren = (
            Diagnostic.all_objects.in_year(2025)
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
    def test_dont_copy_groupe_fields(self):
        """
        Before, some informations from the groupe were copied in the canteen_snapshot of the generated diagnostics: geodata, sector and line ministry.
        We don't do this anymore.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PRIVATE,  # Private economic model for the satellite
            groupe=groupe,
            # sector_list=[],  # can't set to None, the groupe would not be able to teledeclare
            line_ministry=None,
            city_insee_code="38185",
            epci=None,
            pat_list=[],
            department=None,
            region=None,
        )

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.all_objects.in_year(2025).get(
            canteen=satellite, generated_from_groupe_diagnostic=True
        )

        # Fields that used to be copied
        field_not_copied = [
            "city_insee_code",
            "epci",
            "pat_list",
            "department",
            "region",
            "sector_list",
            "line_ministry",
        ]

        for field in field_not_copied:
            with self.subTest(field=field):
                self.assertEqual(diagnostic_generated.canteen_snapshot[field], getattr(satellite, field))

    @authenticate
    def test_dont_divide_yearly_meal_count_by_number_of_satellites(self):
        """
        Before, the yearly meal count is divided by the number of satellites (and converted to integer)
        We don't do this anymore.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, yearly_meal_count=1011)
        satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=groupe,
            yearly_meal_count=450,
        )
        satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=groupe,
            yearly_meal_count=550,  # can't set to None, the groupe would not be able to teledeclare
        )

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_1_diagnostic = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite_1, generated_from_groupe_diagnostic=True)
        )
        satellite_2_diagnostic = (
            Diagnostic.all_objects.in_year(2025)
            .teledeclared()
            .get(canteen=satellite_2, generated_from_groupe_diagnostic=True)
        )

        self.assertEqual(
            int(satellite_1_diagnostic.canteen_snapshot["yearly_meal_count"]), satellite_1.yearly_meal_count
        )
        self.assertEqual(
            int(satellite_2_diagnostic.canteen_snapshot["yearly_meal_count"]), satellite_2.yearly_meal_count
        )


class Teledeclaration1Td1SiteTunnelFieldsValuesTest(TestCase):
    def setUp(self):
        post_save.disconnect(fill_geo_fields_from_siret, sender=Canteen)
        return super().setUp()

    def tearDown(self):
        post_save.connect(fill_geo_fields_from_siret, sender=Canteen)
        return super().tearDown()

    @classmethod
    def setUpTestData(cls):
        cls.groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, yearly_meal_count=1011, daily_meal_count=3
        )
        cls.satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=cls.groupe, yearly_meal_count=450
        )
        cls.satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.groupe,
            siret=None,
            siren_unite_legale="123456789",
            yearly_meal_count=550,
        )
        cls.groupe_satellites_yearly_meal_count_sum = (
            cls.satellite_1.yearly_meal_count + cls.satellite_2.yearly_meal_count
        )

        cls.appro_fields = {}
        for field in Diagnostic.SIMPLE_APPRO_FIELDS:
            cls.appro_fields[field] = 10000.50
        for field in Diagnostic.COMPLETE_APPRO_FIELDS:
            cls.appro_fields[field] = 500.75

    def verify_field_are_equals(self, value, expected_value):
        # self.assertAlmostEqual(float(value), float(expected_value), places=2)
        self.assertEqual(int(value), int(expected_value))  # avoid rounding errors

    def verify_appro_fields_divided(self, fields, satellite_diagnostic, groupe_diagnostic, divisor):
        for field in fields:
            with self.subTest(field=field):
                groupe_value = getattr(groupe_diagnostic, field)
                diagnostic_value = getattr(satellite_diagnostic, field)
                expected_value = groupe_value / divisor
                self.verify_field_are_equals(diagnostic_value, expected_value)

    @authenticate
    def test_total_value_divided_by_satellite_yearly_meal_count(self):
        """
        Before, we divided the total value by the number of satellites.
        Now, we divide the total value by the yearly_meal_count (ratio) of the satellite.
        """
        total_value = 15000.50
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=self.groupe,
                year=2025,
                valeur_totale=total_value,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_1_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_1)
        satellite_2_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_2)
        self.verify_field_are_equals(
            satellite_1_diagnostic.valeur_totale,
            total_value / (self.groupe_satellites_yearly_meal_count_sum / self.satellite_1.yearly_meal_count),
        )
        self.verify_field_are_equals(
            satellite_2_diagnostic.valeur_totale,
            total_value / (self.groupe_satellites_yearly_meal_count_sum / self.satellite_2.yearly_meal_count),
        )

    @authenticate
    def test_groupe_type_simple(self):
        """
        Test that when a groupe canteen teledeclares with mode ALL.
        """
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=self.groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_1_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_1)
        satellite_2_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_2)
        satellite_diagnostics_generated = [satellite_1_diagnostic, satellite_2_diagnostic]

        # Appro fields are divided and copied in the generated diagnostics
        for index, satellite_diagnostic in enumerate(satellite_diagnostics_generated):
            with self.subTest(satellite_diagnostic_index=index):
                self.verify_appro_fields_divided(
                    Diagnostic.APPRO_1TD1SITE_FIELDS,
                    satellite_diagnostic,
                    groupe_diagnostic,
                    self.groupe_satellites_yearly_meal_count_sum
                    / satellite_diagnostic.canteen_snapshot["yearly_meal_count"],
                )

    @authenticate
    def test_groupe_type_complete(self):
        """
        Test that when a groupe canteen teledeclares in mode ALL with COMPLETE type.
        """
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=self.groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_1_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_1)
        satellite_2_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_2)
        satellite_diagnostics_generated = [satellite_1_diagnostic, satellite_2_diagnostic]

        # Appro fields are divided and copied in the generated diagnostics
        for index, satellite_diagnostic in enumerate(satellite_diagnostics_generated):
            with self.subTest(satellite_diagnostic_index=index):
                self.verify_appro_fields_divided(
                    Diagnostic.APPRO_1TD1SITE_FIELDS,
                    satellite_diagnostic,
                    groupe_diagnostic,
                    self.groupe_satellites_yearly_meal_count_sum
                    / satellite_diagnostic.canteen_snapshot["yearly_meal_count"],
                )

    @authenticate
    def test_groupe_no_type(self):
        """
        Test that when a groupe canteen teledeclares without mode.
        """
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=self.groupe,
                year=2025,
                diagnostic_type=None,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                **self.appro_fields,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_1_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_1)
        satellite_2_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_2)
        satellite_diagnostics_generated = [satellite_1_diagnostic, satellite_2_diagnostic]

        # Appro fields are divided and copied in the generated diagnostics
        for index, satellite_diagnostic in enumerate(satellite_diagnostics_generated):
            with self.subTest(satellite_diagnostic_index=index):
                self.verify_appro_fields_divided(
                    Diagnostic.APPRO_1TD1SITE_FIELDS,
                    satellite_diagnostic,
                    groupe_diagnostic,
                    self.groupe_satellites_yearly_meal_count_sum
                    / satellite_diagnostic.canteen_snapshot["yearly_meal_count"],
                )

    @authenticate
    def test_mode_all_non_appro_fields_are_copied(self):
        """
        Test that when a groupe canteen teledeclares in mode ALL with non appro fields, the values are copied in the generated diagnostics.
        """
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=self.groupe,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user, skip_validations=True)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        satellite_1_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_1)
        satellite_2_diagnostic = Diagnostic.all_objects.in_year(2025).teledeclared().get(canteen=self.satellite_2)
        satellite_diagnostics_generated = [satellite_1_diagnostic, satellite_2_diagnostic]

        for sat_diagnostic in satellite_diagnostics_generated:
            with self.subTest(sat_diagnostic=sat_diagnostic):
                for field in Diagnostic.NON_APPRO_FIELDS:
                    with self.subTest(field=field):
                        self.assertEqual(getattr(sat_diagnostic, field), getattr(groupe_diagnostic, field))


class Teledeclaration1Td1SiteNotConcernedByScriptTest(TestCase):
    """
    Test the teledeclaration of canteen or diagnostic not concerned by the 1td1site script are not modified when the command is run.
    """

    @authenticate
    def test_canteen_site(self):
        site_1 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        site_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            diagnostic_site_1 = DiagnosticFactory(
                canteen=site_1,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            )
            diagnostic_site_2 = DiagnosticFactory(
                canteen=site_2,
                year=2025,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            )
            diagnostic_site_1.teledeclare(applicant=authenticate.user)
            diagnostic_site_2.teledeclare(applicant=authenticate.user)

        diagnostic_site_1_before_script = diagnostic_site_1
        diagnostic_site_2_before_script = diagnostic_site_2

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            0,
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)
        diagnostic_site_1.refresh_from_db()
        diagnostic_site_2.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.all_objects.in_year(2025).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            0,
        )
        self.assertEqual(diagnostic_site_1, diagnostic_site_1_before_script)
        self.assertEqual(diagnostic_site_2, diagnostic_site_2_before_script)

    @authenticate
    def test_teledeclaration_other_year_are_not_generated(self):
        groupe = CanteenFactory(
            production_type=Canteen.ProductionType.GROUPE, yearly_meal_count=1011, daily_meal_count=3
        )
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)

        with freeze_time("2024-03-30"):  # during the 2023 campaign
            groupe_diagnostic_2023 = DiagnosticFactory(
                canteen=groupe,
                year=2023,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic_2023.teledeclare(applicant=authenticate.user)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            groupe_diagnostic_2024 = DiagnosticFactory(
                canteen=groupe,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic_2024.teledeclare(applicant=authenticate.user)

        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic_2025 = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic_2025.teledeclare(applicant=authenticate.user)

        # Before the script is run
        self.assertEqual(Diagnostic.all_objects.count(), 3)
        self.assertEqual(Diagnostic.all_objects.in_year(2023).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 1)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.count(), 5)
        self.assertEqual(Diagnostic.all_objects.in_year(2023).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.all_objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 3)

    @authenticate
    def test_groupe_with_diagnostic_not_teledeclared(self):
        """
        Test that when a diagnostic is draft, it is not modified when the script is run.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
            )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).count(), 1)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 0)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).filter(generated_from_groupe_diagnostic=True).count(), 0)

    @authenticate
    def test_cancelled_groupe_diagnostics(self):
        """
        If a teledeclaration is cancelled, no diagnostics should be generated.
        """
        groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=groupe)
        with freeze_time("2026-03-30"):  # during the 2025 campaign
            groupe_diagnostic = DiagnosticFactory(
                canteen=groupe,
                year=2025,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            groupe_diagnostic.teledeclare(applicant=authenticate.user)
            groupe_diagnostic.cancel()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.all_objects.in_year(2025).count(), 1)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).teledeclared().count(), 0)
        self.assertEqual(Diagnostic.all_objects.in_year(2025).filter(generated_from_groupe_diagnostic=True).count(), 0)
