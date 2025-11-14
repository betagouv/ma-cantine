from django.core.management import call_command
from django.test import TestCase

from data.models import Canteen, Diagnostic, SectorM2M, User


class FixturesTest(TestCase):
    def test_load_fixtures(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Canteen.objects.count(), 0)
        self.assertEqual(Diagnostic.objects.count(), 0)
        self.assertEqual(SectorM2M.objects.count(), 0)
        call_command("loaddata", "initial_data.json")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Canteen.objects.count(), 1)
        self.assertEqual(Diagnostic.objects.count(), 1)
        self.assertEqual(SectorM2M.objects.count(), 1)
