from unittest import mock

from django.core.management import CommandError, call_command
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic
from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData

LOGGER_PATH = "macantine.management.commands.diagnostic_fill_computed_fields.logger"


def get_logger_output(mock_logger):
    return "\n".join(call.args[0] for call in mock_logger.info.call_args_list)


class DiagnosticFillComputedFieldsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)
        cls.FIELD_LIST = (
            Diagnostic.APPRO_AGGREGATED_FIELDS + Diagnostic.APPRO_STATS_FIELDS + Diagnostic.OTHER_COMPUTED_FIELDS
        )

    def test_fill_is_clean_field(self):
        diagnostic = DiagnosticFactory(
            year=2024, canteen=CanteenFactory(), diagnostic_type=Diagnostic.DiagnosticType.SIMPLE, valeur_totale=1000
        )
        # simulate existing data (field not computed yet)
        Diagnostic.objects.filter(id=diagnostic.id).update(is_clean=False)

        call_command("diagnostic_fill_computed_fields", "--year", 2024, "--field", "is_clean", "--apply")

        diagnostic.refresh_from_db()
        self.assertTrue(diagnostic.is_clean)

    def test_dry_run(self):
        diagnostic = self.canteen_site_diagnostic_2022
        # simulate an outdated value
        Diagnostic.objects.filter(id=diagnostic.id).update(pourcentage_bio=None)

        with mock.patch(LOGGER_PATH) as mock_logger:
            call_command("diagnostic_fill_computed_fields", "--year", 2022)

        diagnostic.refresh_from_db()
        self.assertIsNone(diagnostic.pourcentage_bio)  # unchanged
        output = get_logger_output(mock_logger)
        self.assertIn("Computed: 1 diagnostics with pourcentage_bio changed", output)
        self.assertIn("Task completed: 1 diagnostics to update", output)

    def test_run_twice_does_not_update_anything(self):
        call_command("diagnostic_fill_computed_fields", "--year", 2022, "--apply")

        with mock.patch(LOGGER_PATH) as mock_logger:
            call_command("diagnostic_fill_computed_fields", "--year", 2022, "--apply")

        self.assertIn("Task completed: 0 diagnostics updated", get_logger_output(mock_logger))

    def test_run_on_diagnostic_teledeclared(self):
        diagnostic = self.canteen_site_diagnostic_2022
        diagnostic_modification_date_before = diagnostic.modification_date
        self.assertEqual(diagnostic.valeur_totale, 1000)
        self.assertEqual(diagnostic.valeur_bio, 200)
        self.assertEqual(diagnostic.valeur_siqo, 0)
        self.assertEqual(diagnostic.valeur_externalites_performance, 0)
        self.assertEqual(diagnostic.valeur_egalim_autres, 300)
        self.assertEqual(diagnostic.canteen_snapshot["yearly_meal_count"], 500)

        # simulate the fact that these fields were empty for non-teledeclared diagnostics
        for field_name in self.FIELD_LIST:
            setattr(diagnostic, field_name, None)

        call_command("diagnostic_fill_computed_fields", "--year", 2022, "--apply")

        diagnostic.refresh_from_db()
        self.assertIsNotNone(diagnostic.valeur_bio_agg)
        self.assertIsNotNone(diagnostic.pourcentage_bio)
        self.assertIsNotNone(diagnostic.pourcentage_egalim)
        self.assertIsNotNone(diagnostic.pourcentage_egalim_hors_bio)
        self.assertTrue(diagnostic.objectifs_egalim_atteints)
        self.assertIsNotNone(diagnostic.cout_repas)
        self.assertEqual(diagnostic.modification_date, diagnostic_modification_date_before)  # unchanged

    def test_run_on_diagnostic_draft(self):
        diagnostic = self.canteen_site_diagnostic_2023
        diagnostic_modification_date_before = diagnostic.modification_date
        self.assertEqual(diagnostic.valeur_totale, 1000)
        self.assertEqual(diagnostic.valeur_bio, 200)
        self.assertEqual(diagnostic.valeur_siqo, 0)
        self.assertEqual(diagnostic.valeur_externalites_performance, 0)
        self.assertEqual(diagnostic.valeur_egalim_autres, 300)
        self.assertIsNone(diagnostic.canteen_snapshot)  # not teledeclared

        # simulate the fact that these fields were empty for non-teledeclared diagnostics
        for field_name in self.FIELD_LIST:
            setattr(diagnostic, field_name, None)

        call_command("diagnostic_fill_computed_fields", "--year", 2023, "--apply")

        # should stay unchanged
        diagnostic.refresh_from_db()
        self.assertIsNotNone(diagnostic.valeur_bio_agg)
        self.assertIsNotNone(diagnostic.pourcentage_bio)
        self.assertIsNotNone(diagnostic.pourcentage_egalim)
        self.assertIsNotNone(diagnostic.pourcentage_egalim_hors_bio)
        self.assertTrue(diagnostic.objectifs_egalim_atteints)
        self.assertIsNotNone(diagnostic.cout_repas)
        self.assertEqual(diagnostic.modification_date, diagnostic_modification_date_before)  # unchanged

    def test_run_does_not_create_historical_records(self):
        history_count_before = Diagnostic.history.count()

        call_command("diagnostic_fill_computed_fields", "--year", 2022, "--apply")

        self.assertEqual(Diagnostic.history.count(), history_count_before)

    def test_run_with_field_only_updates_this_field(self):
        diagnostic = self.canteen_site_diagnostic_2022
        # simulate an empty field, and another field with an outdated value
        Diagnostic.objects.filter(id=diagnostic.id).update(pourcentage_bio=None, pourcentage_siqo=99)

        call_command("diagnostic_fill_computed_fields", "--year", 2022, "--field", "pourcentage_bio", "--apply")

        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.pourcentage_bio, 20)  # filled
        self.assertEqual(diagnostic.pourcentage_siqo, 99)  # unchanged

    def test_run_with_field_is_filled(self):
        diagnostic = self.canteen_site_diagnostic_2022
        self.assertTrue(diagnostic.is_filled)
        # simulate an outdated value (e.g. diagnostic saved before the field was introduced)
        Diagnostic.objects.filter(id=diagnostic.id).update(is_filled=False, pourcentage_bio=None)

        call_command("diagnostic_fill_computed_fields", "--year", 2022, "--field", "is_filled", "--apply")

        diagnostic.refresh_from_db()
        self.assertTrue(diagnostic.is_filled)  # filled
        self.assertIsNone(diagnostic.pourcentage_bio)  # unchanged

    def test_run_with_unknown_field(self):
        with self.assertRaises(CommandError):
            call_command("diagnostic_fill_computed_fields", "--year", 2022, "--field", "valeur_totale", "--apply")


@freeze_time("2026-03-30")  # during the 2025 campaign
class DiagnosticFillComputedFieldsCommandGeneratedFromGroupeTest(TestCase):
    def test_run_on_diagnostic_generated_from_groupe_diagnostic(self):
        user = UserFactory()
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[user])
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe)
        diagnostic_groupe = DiagnosticFactory(
            canteen=canteen_groupe,
            year=2025,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        diagnostic_groupe.teledeclare(applicant=user)
        call_command("diagnostic_fill_invalid_warning_reason_list", year=2025, apply=True)
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        generated_diagnostic_qs = Diagnostic.all_objects.filter(generated_from_groupe_diagnostic=True)
        self.assertEqual(generated_diagnostic_qs.count(), 1)
        generated_diagnostic = generated_diagnostic_qs.first()
        self.assertIsNotNone(generated_diagnostic.pourcentage_bio)

        # simulate the fact that these fields were empty
        generated_diagnostic_qs.update(**{field_name: None for field_name in Diagnostic.APPRO_STATS_FIELDS})

        call_command("diagnostic_fill_computed_fields", "--year", 2025, "--apply")

        generated_diagnostic.refresh_from_db()
        self.assertIsNotNone(generated_diagnostic.pourcentage_bio)
        self.assertIsNotNone(generated_diagnostic.pourcentage_egalim)
        self.assertEqual(generated_diagnostic.pourcentage_bio, diagnostic_groupe.pourcentage_bio)
