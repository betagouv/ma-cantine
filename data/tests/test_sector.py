from django.test import TestCase

from data.factories import SectorFactory
from data.models import Sector


class TeledeclarationQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector = SectorFactory(id=1)
        cls.sector_spe = SectorFactory(id=2)

    def test_is_spe(self):
        self.assertEqual(Sector.objects.count(), 2)
        self.assertEqual(Sector.objects.is_spe().count(), 1)
