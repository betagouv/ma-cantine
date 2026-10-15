from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic
from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData


class DiagnosticFillComputedFieldsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)
        cls.FIELD_LIST = (
            Diagnostic.APPRO_AGGREGATED_FIELDS + Diagnostic.APPRO_STATS_FIELDS + Diagnostic.OTHER_COMPUTED_FIELDS
        )

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

        call_command("diagnostic_fill_computed_fields", "--year", 2022)

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

        call_command("diagnostic_fill_computed_fields", "--year", 2023)

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

        call_command("diagnostic_fill_computed_fields", "--year", 2022)

        self.assertEqual(Diagnostic.history.count(), history_count_before)


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

        call_command("diagnostic_fill_computed_fields", "--year", 2025)

        generated_diagnostic.refresh_from_db()
        self.assertIsNotNone(generated_diagnostic.pourcentage_bio)
        self.assertIsNotNone(generated_diagnostic.pourcentage_egalim)
        self.assertEqual(generated_diagnostic.pourcentage_bio, diagnostic_groupe.pourcentage_bio)
