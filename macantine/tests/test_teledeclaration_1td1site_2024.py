from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.models import Canteen, Diagnostic
from data.models.sector import Sector
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory

# TODO : on devrait stocker l'id du diagnostic à partir duquel on a fait la génération non ?
# TODO : SAT avec les doublons after rebase avec le tag "DOUBLON_1TD1SITE"


class Teledeclaration1Td1SiteNoTeledeclarationGenerated(TestCase):
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
    def test_central_with_satellite_deleted(self):
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
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        central_diagnostic.refresh_from_db()

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 0
        )

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


class Teledeclaration1Td1SiteDiagnosticsAreGenerated(TestCase):
    @authenticate
    def test_correct_number_of_diagnostics_generated_for_central(self):
        """
        For a central with satellites, the script should generate a new diagnostic for each satellite.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
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
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)  # Central + 2 satellites
        diagnostics_generated = (
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True)
        )
        self.assertEqual(diagnostics_generated.count(), 2)

    @authenticate
    def test_correct_number_of_diagnostics_generated_for_central_serving(self):
        """
        For a central serving with satellites, the script should generate a new diagnostic for each satellite and one for the central.
        """
        central_serving = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_serving.siret
        )
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_serving.siret
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central_serving,
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
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().count(), 4
        )  # Central + 2 satellites + 1 for the central serving
        diagnostics_generated = (
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True)
        )
        self.assertEqual(diagnostics_generated.count(), 3)

    @authenticate
    def test_canteen_informations_copied_canteen_exact_datetime_teledeclaration(self):
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL,
            yearly_meal_count=420,
            daily_meal_count=3,
        )
        satellite_siret = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            department="92",
            region="11",
        )
        satellite_siret.yearly_meal_count = None
        satellite_siret.daily_meal_count = None
        satellite_siret.save(skip_validations=True)
        satellite_siren = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            department="93",
            region="11",
            siret=None,
            siren_unite_legale="123456789",
            sector_list=[Sector.SANTE_HOPITAL, Sector.EDUCATION_AUTRE],
            line_ministry=Canteen.Ministries.AFFAIRES_ETRANGERES,
            yearly_meal_count=555,
            daily_meal_count=55,
            economic_model=Canteen.EconomicModel.PUBLIC,
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Change satellite informations
        satellite_siren.yearly_meal_count = 2000
        satellite_siren.daily_meal_count = 20
        satellite_siren.sector_list = [Sector.EDUCATION_ENSEIGNEMENT_AGRICOLE]
        satellite_siren.line_ministry = None
        satellite_siren.department = "93"
        satellite_siren.economic_model = Canteen.EconomicModel.PRIVATE
        satellite_siren.management_type = Canteen.ManagementType.CONCEDED
        satellite_siren.production_type = Canteen.ProductionType.ON_SITE
        satellite_siren.save(skip_validations=True)
        satellite_siren.refresh_from_db()

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        field_to_be_copied = [
            "name",
            "siret",
            "siren_unite_legale",
            "yearly_meal_count",
            "daily_meal_count",
            "sector_list",
            "line_ministry",
            "economic_model",
            "management_type",
            "production_type",
            "central_producer_siret",
            "department",
            "region",
            "city_insee_code",
        ]

        diagnostic_generated_satellite_siret = Diagnostic.objects.in_year(2024).get(
            canteen=satellite_siret, generated_from_groupe_diagnostic=True
        )
        diagnostic_generated_siren = Diagnostic.objects.in_year(2024).get(
            canteen=satellite_siren, generated_from_groupe_diagnostic=True
        )

        for field in field_to_be_copied:
            with self.subTest(field=field):
                self.assertEqual(
                    diagnostic_generated_satellite_siret.canteen_snapshot[field], getattr(satellite_siret, field)
                )
                self.assertEqual(diagnostic_generated_siren.canteen_snapshot[field], getattr(satellite_siren, field))

    @authenticate
    def test_central_serving_informations_copied_in_canteen_snapshot(self):
        """
        The informations from the central serving are copied in the canteen_snapshot of the generated diagnostics.
        """
        central_serving = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL_SERVING)
        CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_serving.siret
        )

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central_serving,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        diagnostic_generated = Diagnostic.objects.in_year(2024).get(
            canteen=central_serving, generated_from_groupe_diagnostic=True
        )

        # Fields to be copied
        field_to_be_copied = [
            "name",
            "siret",
            "siren_unite_legale",
            "sector_list",
            "line_ministry",
            "economic_model",
            "management_type",
            "department",
            "region",
            "city_insee_code",
        ]

        for field in field_to_be_copied:
            with self.subTest(field=field):
                self.assertEqual(diagnostic_generated.canteen_snapshot[field], getattr(central_serving, field))

        # Fields to be updated
        number_of_satellites = 2
        self.assertEqual(
            diagnostic_generated.canteen_snapshot["production_type"], Canteen.ProductionType.CENTRAL_SERVING
        )
        self.assertEqual(
            diagnostic_generated.canteen_snapshot["yearly_meal_count"],
            central_serving.yearly_meal_count / number_of_satellites,
        )  # Correct ?
        self.assertEqual(
            diagnostic_generated.canteen_snapshot["daily_meal_count"],
            central_serving.daily_meal_count / number_of_satellites,
        )  # Correct ?
        self.assertEqual(diagnostic_generated.canteen_snapshot["central_producer_siret"], central_serving.siret)

    @authenticate
    def test_satellite_without_meal_count_has_central_divided_values(self):
        """
        If a satellite has no meal count, it should have the values of the central divided by the number of satellites.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=10000, daily_meal_count=100
        )
        satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret
        )
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central.siret)
        satellite.yearly_meal_count = None
        satellite.daily_meal_count = None
        satellite.save(skip_validations=True)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            central_diagnostic = DiagnosticFactory(
                canteen=central,
                year=2024,
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        diagnostic_generated = Diagnostic.objects.in_year(2024).get(
            canteen=satellite, generated_from_groupe_diagnostic=True
        )
        self.assertEqual(
            diagnostic_generated.canteen_snapshot["yearly_meal_count"], int(central.yearly_meal_count / 3)
        )
        self.assertEqual(diagnostic_generated.canteen_snapshot["daily_meal_count"], int(central.daily_meal_count / 3))

    @authenticate
    def test_generated_diagnostics_metadata_copied_from_central_diagnostic(self):
        """
        The metadata from the central diagnostic is copied in the generated diagnostics.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
        satelitte = CanteenFactory(
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
        diagnostic_generated = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=satelitte)
        diagnostic_central = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=central)
        self.assertEqual(diagnostic_generated.teledeclaration_id, diagnostic_central.teledeclaration_id)
        self.assertEqual(diagnostic_generated.teledeclaration_date, diagnostic_central.teledeclaration_date)
        self.assertEqual(diagnostic_generated.applicant_snapshot, diagnostic_central.applicant_snapshot)

    @authenticate
    def test_generated_diagnostics_have_empty_satellites_snapshot(self):
        """
        The satellites_snapshot should be empty for the generated diagnostics since they have been removed by the script.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL_SERVING, yearly_meal_count=420, daily_meal_count=3
        )
        satelitte = CanteenFactory(
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
        diagnostic_generated = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=satelitte)
        diagnostic_central_generated = (
            Diagnostic.objects.in_year(2024).teledeclared().get(canteen=central, generated_from_groupe_diagnostic=True)
        )
        self.assertIsNone(diagnostic_generated.satellites_snapshot)
        self.assertIsNone(diagnostic_central_generated.satellites_snapshot)

    @authenticate
    def test_satellite_with_teledeclaration_reteledeclare_by_central_are_archived(self):
        """
        Test that when a satellite canteen has a teledeclaration, then it's also teledeclare with the central teledeclaration, the script flags it.
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
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        self.assertEqual(Diagnostic.objects.in_year(2024).count(), 2)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 3)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().filter(canteen=satellite).count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(canteen=satellite, generated_from_groupe_diagnostic=True)
            .count(),
            1,
        )
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .filter(canteen=satellite, generated_from_groupe_diagnostic=False)
            .count(),
            1,
        )
        self.assertEqual(
            Diagnostic.objects.in_year(2024)
            .filter(status=Diagnostic.DiagnosticStatus.SUBMITTED_BUT_OVERRIDDEN_BY_GROUPE)
            .count(),
            1,
        )
        diagnostic_generated = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=satellite, generated_from_groupe_diagnostic=True)
        )
        self.assertEqual(diagnostic_generated.status, Diagnostic.DiagnosticStatus.SUBMITTED_BUT_OVERRIDDEN_BY_GROUPE)


class Teledeclaration1Td1SiteDiagnosticsFieldsValuesAreGenerated(TestCase):
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

    def verify_appro_fields_divided(self, fields, divisor, central_diagnostic, sat_diagnostics_generated):
        for sat_diagnostic in sat_diagnostics_generated:
            with self.subTest(sat_diagnostic=sat_diagnostic):
                for field in fields:
                    with self.subTest(field=field):
                        central_value = getattr(central_diagnostic, field)
                        if central_value is not None:
                            expected_value = central_value / divisor
                            expected_value_rounded = round(expected_value, 2)  # The value saved has 2 decimal
                            self.assertEqual(
                                float(getattr(sat_diagnostic, field)),
                                expected_value_rounded,
                            )

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
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.SIMPLE_APPRO_FIELDS,
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
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_3_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=self.central, generated_from_groupe_diagnostic=True)
        )
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic, sat_3_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.SIMPLE_APPRO_FIELDS,
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
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.COMPLETE_APPRO_FIELDS,
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
                valeur_totale=10000,
                valeur_bio=2000,
            )
            central_diagnostic.teledeclare(applicant=authenticate.user)

        # Run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)

        # After the script is run
        sat_1_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_1)
        sat_2_diagnostic = Diagnostic.objects.in_year(2024).teledeclared().get(canteen=self.satellite_2)
        sat_3_diagnostic = (
            Diagnostic.objects.in_year(2024)
            .teledeclared()
            .get(canteen=self.central, generated_from_groupe_diagnostic=True)
        )
        sat_diagnostics_generated = [sat_1_diagnostic, sat_2_diagnostic, sat_3_diagnostic]
        number_of_generated_diagnostics = len(sat_diagnostics_generated)

        # Appro fields are divided and copied in the generated diagnostics
        self.verify_appro_fields_divided(
            Diagnostic.COMPLETE_APPRO_FIELDS,
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
            central_diagnostic.teledeclare(applicant=authenticate.user)

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


class Teledeclaration1Td1SiteScript(TestCase):
    @authenticate
    def test_script_run_again_does_not_generate_new_diagnostics(self):
        """
        Test that when the script is run again, it does not generate new diagnostics.
        """
        central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, yearly_meal_count=420, daily_meal_count=3
        )
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

        # Before the script is run
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 1)

        # Run the script first time
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 1
        )

        # Re-run the script
        call_command("teledeclaration_generate_1td1site", year=2024, apply=True)
        self.assertEqual(Diagnostic.objects.in_year(2024).teledeclared().count(), 2)
        self.assertEqual(
            Diagnostic.objects.in_year(2024).teledeclared().filter(generated_from_groupe_diagnostic=True).count(), 1
        )
