from django.core.management import call_command
from django.test import TestCase

from data.models import Diagnostic
from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData


class TeledeclarationFillEgalimFieldsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)
        cls.FIELD_LIST = (
            Diagnostic.AGGREGATED_APPRO_FIELDS + Diagnostic.COMPUTED_EGALIM_FIELDS + Diagnostic.OTHER_COMPUTED_FIELDS
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
