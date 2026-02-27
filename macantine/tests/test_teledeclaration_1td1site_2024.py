from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.models import Canteen, Diagnostic
from data.models.sector import Sector
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory

# TODO : test tag doublon after rebase


class Teledeclaration1Td1SiteForDiagnosticsAreNotGenerated(TestCase):
    """
    Test the teledeclaration of canteen not concerned by the 1td1site script are not modified when the command is run.
    """

    @authenticate
    def test_for_canteen_site(self):
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

        site_1_snapshot_canteen_before_script = diagnostic_site_1.canteen_snapshot
        site_1_snapshot_satellites_before_script = diagnostic_site_1.satellites_snapshot
        site_2_snapshot_canteen_before_script = diagnostic_site_2.canteen_snapshot
        site_2_snapshot_satellites_before_script = diagnostic_site_2.satellites_snapshot

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 2)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        diagnostic_site_1.refresh_from_db()
        diagnostic_site_2.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(diagnostic_site_1.canteen_snapshot, site_1_snapshot_canteen_before_script)
        self.assertEqual(diagnostic_site_1.satellites_snapshot, site_1_snapshot_satellites_before_script)
        self.assertEqual(diagnostic_site_2.canteen_snapshot, site_2_snapshot_canteen_before_script)
        self.assertEqual(diagnostic_site_2.satellites_snapshot, site_2_snapshot_satellites_before_script)

    @authenticate
    def test_for_satellite_with_central_siret_unknown(self):
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

        satellite_snapshot_canteen_before_script = satellite_diagnostic.canteen_snapshot
        satellite_snapshot_satellites_before_script = satellite_diagnostic.satellites_snapshot

        # Before the script is run
        self.assertEqual(
            Canteen.objects.filter(siret="19622299600015").count(), 0
        )  # no central canteen exist with the siret used in sat
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        satellite_diagnostic.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(satellite_diagnostic.canteen_snapshot, satellite_snapshot_canteen_before_script)
        self.assertEqual(satellite_diagnostic.satellites_snapshot, satellite_snapshot_satellites_before_script)

    @authenticate
    def test_for_satellite_with_central_siret_empty(self):
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
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        satellite_diagnostic.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )
        self.assertEqual(satellite_diagnostic.canteen_snapshot, satellite_snapshot_canteen_before_script)
        self.assertEqual(satellite_diagnostic.satellites_snapshot, satellite_snapshot_satellites_before_script)

    @authenticate
    def test_for_central_with_satellite_deleted(self):
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, siret="19622299600015")
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="19622299600015"
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        satellite.hard_delete()

        # Before the script is run
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        central_diagnostic.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )


class VerifyTeledeclarationGeneratedInformations(TestCase):
    """
    Helper method to verify the generated informations are correct created and the original diagnostic is not modified.
    """

    def verify_teledeclaration_before_script_run(self):
        """
        Test the before script the correct number of diagnostics are presents.
        """
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

    def verify_teledeclaration_generated_after_script_run(self):
        """
        Test the generated diagnostics are correctly created.
        """
        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 1 + len(self.sat_diagnostics_generated))
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(),
            len(self.sat_diagnostics_generated),
        )
        for sat_diagnostic in self.sat_diagnostics_generated:
            with self.subTest(canteen_id=sat_diagnostic.canteen_id):
                self.assertTrue(sat_diagnostic.generated_from_groupe_diagnostic)

    def verify_teledeclaration_central_not_modified_by_script(self):
        """
        The central diagnostic informations should not be modified by the script.
        """
        self.assertEqual(self.central_diagnostic.canteen_snapshot, self.central_snapshot_canteen_before_script)
        self.assertEqual(self.central_diagnostic.satellites_snapshot, self.central_snapshot_satellites_before_script)

    def verify_teledeclaration_metadata_copied_from_central(self):
        """
        The teledeclaration metadata should not be changed for the generated diagnostics.
        """
        for sat_diagnostic in self.sat_diagnostics_generated:
            with self.subTest(canteen_id=sat_diagnostic.canteen_id):
                self.assertEqual(sat_diagnostic.teledeclaration_id, self.central_diagnostic.teledeclaration_id)
                self.assertEqual(sat_diagnostic.teledeclaration_date, self.central_diagnostic.teledeclaration_date)
                self.assertEqual(sat_diagnostic.applicant_snapshot, self.central_diagnostic.applicant_snapshot)

    def verify_satellites_infos_copied_in_canteen_snapshot(self):
        """
        The informations from the satellites are copied in the canteen_snapshot of the generated diagnostics.
        """
        for sat_diagnostic in self.sat_diagnostics_generated:
            with self.subTest(canteen_id=sat_diagnostic.canteen_id):
                satellite = next(
                    filter(lambda x: x["id"] == sat_diagnostic.canteen_id, self.central_diagnostic.satellites_snapshot)
                )
                self.assertEqual(sat_diagnostic.canteen_snapshot["id"], satellite["id"])
                self.assertEqual(sat_diagnostic.canteen_snapshot["name"], satellite["name"])
                self.assertEqual(sat_diagnostic.canteen_snapshot["siret"], satellite["siret"])
                self.assertEqual(
                    sat_diagnostic.canteen_snapshot["siren_unite_legale"], satellite["siren_unite_legale"]
                )
                self.assertEqual(sat_diagnostic.canteen_snapshot["sector_list"], satellite["sector_list"])
                self.assertEqual(sat_diagnostic.canteen_snapshot["line_ministry"], satellite["line_ministry"])
                self.assertEqual(sat_diagnostic.canteen_snapshot["department"], satellite["department"])
                self.assertEqual(sat_diagnostic.canteen_snapshot["region"], satellite["region"])

    def verify_central_meal_counts_divided_in_canteen_snapshots(self):
        """
        The meal counts for the generated diagnostics should be divided equally between the satellites.
        """
        expected_yearly_meal_count = self.central_diagnostic.canteen_snapshot["yearly_meal_count"] / len(
            self.sat_diagnostics_generated
        )
        expected_daily_meal_count = self.central_diagnostic.canteen_snapshot["daily_meal_count"] / len(
            self.sat_diagnostics_generated
        )
        for sat_diagnostic in self.sat_diagnostics_generated:
            with self.subTest(canteen_id=sat_diagnostic.canteen_id):
                self.assertEqual(
                    sat_diagnostic.canteen_snapshot["yearly_meal_count"],
                    expected_yearly_meal_count,
                )
                self.assertEqual(
                    sat_diagnostic.canteen_snapshot["daily_meal_count"],
                    expected_daily_meal_count,
                )

    def verify_central_appro_values_divided_in_diagnostic_generated(self, fields):
        """
        The appro values for the generated diagnostics should be divided equally between the satellites.
        """
        number_of_generated_diagnostics = len(self.sat_diagnostics_generated)
        for sat_diagnostic in self.sat_diagnostics_generated:
            with self.subTest(canteen_id=sat_diagnostic.canteen_id):
                for field in fields:
                    with self.subTest(field=field):
                        central_value = getattr(self.central_diagnostic, field)
                        if central_value is not None:
                            expected_value = central_value / number_of_generated_diagnostics
                            self.assertEqual(
                                getattr(sat_diagnostic, field),
                                expected_value,
                            )

    def verify_satellites_snapshot_empty_for_generated_diagnostics(self):
        """
        The satellites_snapshot should be empty for the generated diagnostics since they have been removed by the script.
        """
        for sat_diagnostic in self.sat_diagnostics_generated:
            with self.subTest(canteen_id=sat_diagnostic.canteen_id):
                self.assertIsNone(sat_diagnostic.satellites_snapshot)


class Teledeclaration1Td1SiteForCentral(VerifyTeledeclarationGeneratedInformations):
    @classmethod
    def setUpTestData(cls):
        cls.central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        # create field previsously allowed for central
        cls.central.line_ministry = Canteen.Ministries.AFFAIRES_ETRANGERES
        cls.central.sector_list = [Sector.SANTE_HOPITAL, Sector.EDUCATION_AUTRE]
        cls.central.yearly_meal_count = 420
        cls.central.daily_meal_count = 3
        cls.central.department = "75"
        cls.central.region = "11"
        cls.central.save(skip_validations=True)
        cls.satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.central.siret,
            department="92",
            region="11",
        )
        cls.satellite_1.yearly_meal_count = None
        cls.satellite_1.daily_meal_count = None
        cls.satellite_1.save(skip_validations=True)
        cls.satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=cls.central.siret,
            department="93",
            region="11",
            siret=None,
            siren_unite_legale="123456789",
            yearly_meal_count=555,
            daily_meal_count=55,
        )

    @authenticate
    def test_central_td_simple_and_mode_all(self):
        """
        Test that when a central canteen teledeclares in mode ALL with SIMPLE type.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.central_snapshot_canteen_before_script = central_diagnostic.canteen_snapshot
        self.central_snapshot_satellites_before_script = central_diagnostic.satellites_snapshot
        self.central_snapshot_before_script = {
            field: getattr(central_diagnostic, field) for field in Diagnostic.SIMPLE_APPRO_FIELDS
        }

        # Before script is run
        self.verify_teledeclaration_before_script_run()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        central_diagnostic.refresh_from_db()
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_2)

        # Save diagnostics informations to test
        self.central_diagnostic = central_diagnostic
        self.sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]

        # After script is run
        self.verify_teledeclaration_generated_after_script_run()
        self.verify_teledeclaration_central_not_modified_by_script()
        self.verify_teledeclaration_metadata_copied_from_central()
        self.verify_satellites_infos_copied_in_canteen_snapshot()
        self.verify_central_meal_counts_divided_in_canteen_snapshots()
        self.verify_central_appro_values_divided_in_diagnostic_generated(Diagnostic.SIMPLE_APPRO_FIELDS)
        self.verify_satellites_snapshot_empty_for_generated_diagnostics()

    @authenticate
    def test_central_td_complete_and_mode_all(self):
        """
        Test that when a central canteen teledeclares in mode ALL with COMPLETE type.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.central_snapshot_canteen_before_script = central_diagnostic.canteen_snapshot
        self.central_snapshot_satellites_before_script = central_diagnostic.satellites_snapshot
        self.central_snapshot_before_script = {
            field: getattr(central_diagnostic, field) for field in Diagnostic.COMPLETE_APPRO_FIELDS
        }

        # Before script is run
        self.verify_teledeclaration_before_script_run()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        central_diagnostic.refresh_from_db()
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_2)

        # Save diagnostics informations to test
        self.central_diagnostic = central_diagnostic
        self.sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]

        # After script is run
        self.verify_teledeclaration_generated_after_script_run()
        self.verify_teledeclaration_central_not_modified_by_script()
        self.verify_teledeclaration_metadata_copied_from_central()
        self.verify_satellites_infos_copied_in_canteen_snapshot()
        self.verify_central_meal_counts_divided_in_canteen_snapshots()
        self.verify_central_appro_values_divided_in_diagnostic_generated(Diagnostic.COMPLETE_APPRO_FIELDS)
        self.verify_satellites_snapshot_empty_for_generated_diagnostics()

    @authenticate
    def test_central_td_simple_and_mode_appro_only(self):
        """
        Test that when a central canteen teledeclares in mode APPRO only with SIMPLE type.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.central_snapshot_canteen_before_script = central_diagnostic.canteen_snapshot
        self.central_snapshot_satellites_before_script = central_diagnostic.satellites_snapshot
        self.central_snapshot_before_script = {
            field: getattr(central_diagnostic, field) for field in Diagnostic.SIMPLE_APPRO_FIELDS
        }

        # Before script is run
        self.verify_teledeclaration_before_script_run()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        central_diagnostic.refresh_from_db()
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_2)

        # Save diagnostics informations to test
        self.central_diagnostic = central_diagnostic
        self.sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]

        # After script is run
        self.verify_teledeclaration_generated_after_script_run()
        self.verify_teledeclaration_central_not_modified_by_script()
        self.verify_teledeclaration_metadata_copied_from_central()
        self.verify_satellites_infos_copied_in_canteen_snapshot()
        self.verify_central_meal_counts_divided_in_canteen_snapshots()
        self.verify_central_appro_values_divided_in_diagnostic_generated(Diagnostic.SIMPLE_APPRO_FIELDS)
        self.verify_satellites_snapshot_empty_for_generated_diagnostics()

    @authenticate
    def test_central_td_complete_and_mode_appro_only(self):
        """
        Test that when a central canteen teledeclares in mode APPRO only with COMPLETE type.
        """
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=self.central,
                year=2024,
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.central_snapshot_canteen_before_script = central_diagnostic.canteen_snapshot
        self.central_snapshot_satellites_before_script = central_diagnostic.satellites_snapshot
        self.central_snapshot_before_script = {
            field: getattr(central_diagnostic, field) for field in Diagnostic.COMPLETE_APPRO_FIELDS
        }

        # Before script is run
        self.verify_teledeclaration_before_script_run()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        central_diagnostic.refresh_from_db()
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).get(canteen=self.satellite_2)

        # Save diagnostics informations to test
        self.central_diagnostic = central_diagnostic
        self.sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]

        # After script is run
        self.verify_teledeclaration_generated_after_script_run()
        self.verify_teledeclaration_central_not_modified_by_script()
        self.verify_teledeclaration_metadata_copied_from_central()
        self.verify_satellites_infos_copied_in_canteen_snapshot()
        self.verify_central_meal_counts_divided_in_canteen_snapshots()
        self.verify_central_appro_values_divided_in_diagnostic_generated(Diagnostic.COMPLETE_APPRO_FIELDS)
        self.verify_satellites_snapshot_empty_for_generated_diagnostics()
