from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic


class DiagnosticTeledeclaredQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.diagnostic_empty_draft = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=None)
        cls.diagnostic_filled_draft = DiagnosticFactory.create(canteen=CanteenFactory(), value_total_ht=1000)
        cls.diagnostic_filled_submitted = DiagnosticFactory.create(
            canteen=CanteenFactory(), value_total_ht=1000, status=Diagnostic.DiagnosticStatus.SUBMITTED
        )

    def test_teledeclared_queryset(self):
        self.assertEqual(Diagnostic.objects.all().count(), 3)
        self.assertEqual(Diagnostic.objects.teledeclared().count(), 1)

    def test_is_teledeclared_property(self):
        self.assertFalse(self.diagnostic_empty_draft.is_teledeclared)
        self.assertFalse(self.diagnostic_filled_draft.is_teledeclared)
        self.assertTrue(self.diagnostic_filled_submitted.is_teledeclared)


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
