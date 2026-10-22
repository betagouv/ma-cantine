from decimal import Decimal

from django.test import SimpleTestCase

from data.utils import compute_percentage, has_any_value_filled


class ComputePercentageTest(SimpleTestCase):
    def test_compute_percentage(self):
        self.assertEqual(compute_percentage(20, 100), Decimal("20.00"))
        self.assertEqual(compute_percentage(1, 3), Decimal("33.33"))
        self.assertEqual(compute_percentage(100, 100), Decimal("100.00"))
        self.assertEqual(compute_percentage(0, 100), Decimal("0.00"))

    def test_compute_percentage_zero_over_zero(self):
        self.assertEqual(compute_percentage(0, 0), Decimal("0.00"))

    def test_compute_percentage_returns_none(self):
        for index, (numerator, denominator) in enumerate(
            [
                (None, 100),  # numerator empty
                (20, None),  # denominator empty
                (None, None),
                (None, 0),
                (20, 0),  # denominator 0 (but numerator not 0)
                (120, 100),  # numerator exceeds denominator
            ]
        ):
            with self.subTest(index=index, numerator=numerator, denominator=denominator):
                self.assertIsNone(compute_percentage(numerator, denominator))


class HasAnyValueFilledTest(SimpleTestCase):
    def test_has_any_value_filled(self):
        self.assertTrue(has_any_value_filled([10, None]))
        self.assertTrue(has_any_value_filled([None, 0]))  # 0 counts as filled
        self.assertTrue(has_any_value_filled([Decimal("0.00")]))
        self.assertTrue(has_any_value_filled(value for value in [None, 0]))  # generator

    def test_has_any_value_filled_returns_false(self):
        self.assertFalse(has_any_value_filled([None, None]))
        self.assertFalse(has_any_value_filled([]))
