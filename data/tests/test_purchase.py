from decimal import Decimal

from django.test import TransactionTestCase
from django.core.exceptions import ValidationError

from data.factories import PurchaseFactory
from data.models import Purchase


class CanteenModelSaveTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    # def test_purchase_canteen_validation(self):
    # def test_purchase_date_validation(self):

    def test_purchase_category_validation(self):
        """
        - field is optional
        - must be one of the choices if provided
        """
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Purchase.PurchaseCategory.values)]:
            with self.subTest(category=TUPLE_OK[0]):
                purchase = PurchaseFactory(category=TUPLE_OK[0])
                self.assertEqual(purchase.category, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123"]:
            with self.subTest(category=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, category=VALUE_NOT_OK)

    def test_purchase_family_validation(self):
        """
        - field is optional
        - must be one of the choices if provided
        """
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Purchase.Family.values)]:
            with self.subTest(family=TUPLE_OK[0]):
                purchase = PurchaseFactory(family=TUPLE_OK[0])
                self.assertEqual(purchase.family, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123"]:
            with self.subTest(family=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, family=VALUE_NOT_OK)

    def test_purchase_characteristics_validation(self):
        """
        - field is optional
        - must be a list of choices if provided
        """
        for TUPLE_OK in (
            [(None, None), ([], []), ([""], [""])]
            + [([key], [key]) for key in Purchase.Characteristic.values]
            + [
                (
                    [Purchase.Characteristic.BIO, Purchase.Characteristic.LOCAL],
                    [Purchase.Characteristic.BIO, Purchase.Characteristic.LOCAL],
                )
            ]
        ):
            with self.subTest(characteristics=TUPLE_OK[0]):
                purchase = PurchaseFactory(characteristics=TUPLE_OK[0])
                self.assertEqual(purchase.characteristics, TUPLE_OK[1])
        for VALUE_NOT_OK in [["  "], [123], ["invalid"], ["123"]]:
            with self.subTest(characteristics=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, characteristics=VALUE_NOT_OK)

    def test_purchase_local_definition_validation(self):
        """
        - field is optional
        - must be one of the choices if provided
        """
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Purchase.Local.values)]:
            with self.subTest(local_definition=TUPLE_OK[0]):
                purchase = PurchaseFactory(local_definition=TUPLE_OK[0])
                self.assertEqual(purchase.local_definition, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123"]:
            with self.subTest(local_definition=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, local_definition=VALUE_NOT_OK)

    def test_purchase_price_ht_validation(self):
        """
        - field is required
        - must be >= 0
        """
        for TUPLE_OK in [(0, 0), (1000, 1000), ("2000", 2000), (Decimal("1234.56"), Decimal("1234.56"))]:
            with self.subTest(price_ht=TUPLE_OK[0]):
                purchase = PurchaseFactory(price_ht=TUPLE_OK[0])
                self.assertEqual(purchase.price_ht, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, -100, "", "invalid"]:
            with self.subTest(price_ht=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, price_ht=VALUE_NOT_OK)
