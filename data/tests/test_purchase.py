from django.test import TestCase

from data.factories import CanteenFactory, PurchaseFactory
from data.models import Purchase


class TestPurchaseQuerySet(TestCase):
    def test_for_canteen_and_year(self):
        canteen_1 = CanteenFactory()
        canteen_2 = CanteenFactory()
        PurchaseFactory(canteen=canteen_1, date="2024-01-01")
        PurchaseFactory(canteen=canteen_1, date="2024-01-02")
        PurchaseFactory(canteen=canteen_1, date="2024-01-03")
        PurchaseFactory(canteen=canteen_2, date="2024-01-01")
        PurchaseFactory(canteen=canteen_2, date="2024-01-02")
        PurchaseFactory(canteen=canteen_2, date="2024-01-03")
        self.assertEqual(Purchase.objects.count(), 6)
        self.assertEqual(Purchase.objects.for_canteen_and_year(canteen_1, 2024).count(), 3)
        self.assertEqual(Purchase.objects.for_canteen_and_year(canteen_1.id, 2024).count(), 3)  # can also filter by id
        self.assertEqual(Purchase.objects.for_canteen_and_year(canteen_2, 2024).count(), 3)
        self.assertEqual(Purchase.objects.for_canteen_and_year(canteen_1, 2023).count(), 0)
        self.assertEqual(Purchase.objects.for_canteen_and_year(canteen_2, 2023).count(), 0)
