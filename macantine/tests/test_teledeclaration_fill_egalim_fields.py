from django.core.management import call_command
from django.test import TestCase

from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData
from data.models import Diagnostic


class TeledeclarationFillEgalimFieldsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)

    def test_run_on_diagnostic_teledeclared(self):
        diagnostic = self.canteen_site_diagnostic_2022
        self.assertEqual(diagnostic.valeur_totale, 1000)
        self.assertEqual(diagnostic.valeur_bio_agg, 200)
        self.assertEqual(diagnostic.valeur_egalim_agg, 500)
        self.assertEqual(diagnostic.canteen_snapshot["region"], "84")
        # the diagnostic is teledeclared, so egalim fields have been filled
        # clean them before running the command
        for field_name in Diagnostic.TELEDECLARATION_EGALIM_FIELDS:
            setattr(diagnostic, field_name, None)

        call_command("teledeclaration_fill_egalim_fields", "--year", 2022)

        diagnostic.refresh_from_db()
        self.assertIsNotNone(diagnostic.pourcentage_bio)
        self.assertIsNotNone(diagnostic.pourcentage_egalim)
        self.assertIsNotNone(diagnostic.pourcentage_egalim_hors_bio)
        self.assertTrue(diagnostic.objectifs_egalim_atteints)

    def test_ignore_diagnostic_draft(self):
        diagnostic = self.canteen_site_diagnostic_2023
        self.assertEqual(diagnostic.valeur_totale, 1000)
        # self.assertIsNone(diagnostic.valeur_bio_agg)
        # self.assertIsNone(diagnostic.valeur_egalim_agg)
        self.assertIsNone(diagnostic.canteen_snapshot)
        # the diagnostic is not teledeclared, so egalim fields should not be filled
        self.assertIsNone(diagnostic.pourcentage_bio)
        self.assertIsNone(diagnostic.pourcentage_egalim)
        self.assertIsNone(diagnostic.pourcentage_egalim_hors_bio)
        self.assertIsNone(diagnostic.objectifs_egalim_atteints)

        call_command("teledeclaration_fill_egalim_fields", "--year", 2023)

        # should stay unchanged
        diagnostic.refresh_from_db()
        self.assertIsNone(diagnostic.pourcentage_bio)
        self.assertIsNone(diagnostic.pourcentage_egalim)
        self.assertIsNone(diagnostic.pourcentage_egalim_hors_bio)
        self.assertIsNone(diagnostic.objectifs_egalim_atteints)
