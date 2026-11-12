from django.core.management import CommandError, call_command
from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic


class DiagnosticFillSatellitesNombreRepasAnCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_1 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=cls.canteen_groupe
        )
        cls.canteen_satellite_2 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=cls.canteen_groupe
        )
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def setUp(self):
        self.diagnostic_groupe = DiagnosticFactory(canteen=self.canteen_groupe, year=2026)
        self.diagnostic_site = DiagnosticFactory(canteen=self.canteen_site, year=2026)
        # simulate diagnostics created before the field existed
        Diagnostic.objects.update(satellites_nombre_repas_an=None, satellites_nombre_repas_an_total=None)

    def test_year_before_2026(self):
        with self.assertRaises(CommandError):
            call_command("diagnostic_fill_satellites_nombre_repas_an", "--year", 2025)

    def test_dry_run(self):
        call_command("diagnostic_fill_satellites_nombre_repas_an", "--year", 2026)
        self.diagnostic_groupe.refresh_from_db()
        self.assertIsNone(self.diagnostic_groupe.satellites_nombre_repas_an)

    def test_apply(self):
        call_command("diagnostic_fill_satellites_nombre_repas_an", "--year", 2026, "--apply")
        self.diagnostic_groupe.refresh_from_db()
        self.assertEqual(
            self.diagnostic_groupe.satellites_nombre_repas_an,
            {str(self.canteen_satellite_1.id): None, str(self.canteen_satellite_2.id): None},
        )
        self.assertIsNone(self.diagnostic_groupe.satellites_nombre_repas_an_total)
        # not a groupe: untouched
        self.diagnostic_site.refresh_from_db()
        self.assertIsNone(self.diagnostic_site.satellites_nombre_repas_an)

    def test_apply_keeps_the_existing_values(self):
        Diagnostic.objects.filter(id=self.diagnostic_groupe.id).update(
            satellites_nombre_repas_an={str(self.canteen_satellite_1.id): 1000}
        )
        call_command("diagnostic_fill_satellites_nombre_repas_an", "--year", 2026, "--apply")
        self.diagnostic_groupe.refresh_from_db()
        self.assertEqual(
            self.diagnostic_groupe.satellites_nombre_repas_an,
            {str(self.canteen_satellite_1.id): 1000, str(self.canteen_satellite_2.id): None},
        )
        self.assertEqual(self.diagnostic_groupe.satellites_nombre_repas_an_total, 1000)

    def test_apply_ignores_teledeclared_diagnostics(self):
        Diagnostic.objects.filter(id=self.diagnostic_groupe.id).update(status=Diagnostic.DiagnosticStatus.SUBMITTED)
        call_command("diagnostic_fill_satellites_nombre_repas_an", "--year", 2026, "--apply")
        self.diagnostic_groupe.refresh_from_db()
        self.assertIsNone(self.diagnostic_groupe.satellites_nombre_repas_an)
