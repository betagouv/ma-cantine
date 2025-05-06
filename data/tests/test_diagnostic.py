from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic


class DiagnosticIsFilledQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_empty = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=None)
        cls.diagnostic_filled = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=1000)

    def test_is_filled_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 2)
        self.assertEqual(Diagnostic.objects.is_filled().count(), 1)

    def test_is_filled_property(self):
        self.assertFalse(self.diagnostic_empty.is_filled)
        self.assertTrue(self.diagnostic_filled.is_filled)
