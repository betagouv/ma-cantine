from django.test import TestCase

from data.factories import CanteenFactory, PurchaseFactory
from data.models import Purchase


class TestPurchaseQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        canteen = CanteenFactory()
        PurchaseFactory(description="avoine", canteen=canteen, characteristics=[Purchase.Characteristic.BIO])
        PurchaseFactory(
            description="tomates",
            canteen=canteen,
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.PECHE_DURABLE],
        )
        PurchaseFactory.create(
            description="pommes", canteen=canteen, characteristics=[Purchase.Characteristic.PECHE_DURABLE]
        )

    def test_filter_by_characteristics(self):
        self.assertEqual(Purchase.objects.count(), 3)
        self.assertEqual(Purchase.objects.filter_by_characteristics([Purchase.Characteristic.BIO]).count(), 2)
        self.assertEqual(
            Purchase.objects.filter_by_characteristics(
                [Purchase.Characteristic.BIO, Purchase.Characteristic.PECHE_DURABLE]
            ).count(),
            1,
        )
