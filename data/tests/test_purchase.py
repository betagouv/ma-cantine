from decimal import Decimal
from datetime import date

from django.test import TransactionTestCase, TestCase
from django.core.exceptions import ValidationError

from data.factories import PurchaseFactory, CanteenFactory, UserFactory
from data.models import Purchase


class PurchaseModelSaveTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    # def test_purchase_canteen_validation(self):

    def test_purchase_date_validation(self):
        """
        - field is mandatory
        - cannot be in the future
        """
        for TUPLE_OK in [("2024-01-01", "2024-01-01"), (str(date.today()), str(date.today()))]:
            with self.subTest(date=TUPLE_OK[0]):
                purchase = PurchaseFactory(date=TUPLE_OK[0])
                self.assertEqual(str(purchase.date), TUPLE_OK[1])
        for VALUE_NOT_OK in [None, "", "  ", "invalid", "123", "3000-01-01"]:
            with self.subTest(date=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, date=VALUE_NOT_OK)

    # def test_purchase_category_validation(self):  # not used anymore

    def test_purchase_famille_produits_validation(self):
        """
        - field is optional
        - must be one of the choices if provided
        """
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Purchase.Family.values)]:
            with self.subTest(famille_produits=TUPLE_OK[0]):
                purchase = PurchaseFactory(famille_produits=TUPLE_OK[0])
                self.assertEqual(purchase.famille_produits, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123"]:
            with self.subTest(famille_produits=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, famille_produits=VALUE_NOT_OK)

    def test_purchase_caracteristiques_validation(self):
        """
        - field is optional
        - must be a list of choices if provided
        - EUROPE & FRANCE cannot be selected at the same time
        """
        for TUPLE_OK in (
            [(None, None), ([], []), ([""], [""])]
            + [([key], [key]) for key in Purchase.Characteristic.values]
            + [
                (
                    [Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
                    [Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
                    [Purchase.Characteristic.BIO, Purchase.Characteristic.FRANCE],
                )
            ]
        ):
            with self.subTest(caracteristiques=TUPLE_OK[0]):
                definition_local = (
                    Purchase.Local.KM if TUPLE_OK[0] and Purchase.Characteristic.LOCAL in TUPLE_OK[0] else None
                )
                purchase = PurchaseFactory(caracteristiques=TUPLE_OK[0], definition_local=definition_local)
                self.assertEqual(purchase.caracteristiques, TUPLE_OK[1])
        for VALUE_NOT_OK in [
            ["  "],
            [123],
            ["invalid"],
            ["123"],
            [Purchase.Characteristic.EUROPE, Purchase.Characteristic.FRANCE],
        ]:
            with self.subTest(caracteristiques=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, caracteristiques=VALUE_NOT_OK)

    def test_purchase_definition_local_validation(self):
        """
        - field is optional
        - if caracteristiques includes "LOCAL"
            - definition_local can be filled
            - if definition_local is "KM", then definition_local_km can be filled
            - if definition_local is not "KM", then definition_local_km must be empty
        - if caracteristiques does not include "LOCAL", definition_local must be empty
        """
        # caracteristiques includes "LOCAL"
        for TUPLE_OK in [(None, None), ("", ""), *((key, key) for key in Purchase.Local.values)]:
            with self.subTest(caracteristiques=[Purchase.Characteristic.LOCAL], definition_local=TUPLE_OK[0]):
                purchase = PurchaseFactory(
                    caracteristiques=[Purchase.Characteristic.LOCAL], definition_local=TUPLE_OK[0]
                )
                self.assertEqual(purchase.definition_local, TUPLE_OK[1])
        for VALUE_NOT_OK in ["  ", 123, "invalid", "123"]:
            with self.subTest(caracteristiques=[Purchase.Characteristic.LOCAL], definition_local=VALUE_NOT_OK):
                self.assertRaises(
                    ValidationError,
                    PurchaseFactory,
                    caracteristiques=[Purchase.Characteristic.LOCAL],
                    definition_local=VALUE_NOT_OK,
                )
        # caracteristiques does not include "LOCAL"
        for TUPLE_OK in [(None, None), ("", "")]:
            with self.subTest(caracteristiques=[], definition_local=TUPLE_OK[0]):
                purchase = PurchaseFactory(definition_local=TUPLE_OK[0], caracteristiques=[])
                self.assertEqual(purchase.definition_local, TUPLE_OK[1])
            with self.subTest(caracteristiques=[Purchase.Characteristic.BIO], definition_local=TUPLE_OK[0]):
                purchase = PurchaseFactory(
                    caracteristiques=[Purchase.Characteristic.BIO], definition_local=TUPLE_OK[0]
                )
                self.assertEqual(purchase.definition_local, TUPLE_OK[1])
        for VALUE_NOT_OK in [key for key in Purchase.Local.values]:
            with self.subTest(caracteristiques=[], definition_local=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, caracteristiques=[], definition_local=VALUE_NOT_OK)
            with self.subTest(caracteristiques=[Purchase.Characteristic.BIO], definition_local=VALUE_NOT_OK):
                self.assertRaises(
                    ValidationError,
                    PurchaseFactory,
                    caracteristiques=[Purchase.Characteristic.BIO],
                    definition_local=VALUE_NOT_OK,
                )

    def test_purchase_definition_local_km_validation(self):
        # caracteristiques includes "LOCAL" and definition_local is "KM"
        for TUPLE_OK in [(None, None), (0, 0), (1, 1), (100, 100), ("200", 200), (Decimal("123.45"), 123)]:
            with self.subTest(
                caracteristiques=[Purchase.Characteristic.LOCAL],
                definition_local=Purchase.Local.KM,
                definition_local_km=TUPLE_OK[0],
            ):
                purchase = PurchaseFactory(
                    caracteristiques=[Purchase.Characteristic.LOCAL],
                    definition_local=Purchase.Local.KM,
                    definition_local_km=TUPLE_OK[0],
                )
                self.assertEqual(purchase.definition_local_km, TUPLE_OK[1])
        for VALUE_NOT_OK in ["", "  ", -1, -100, "invalid", "123.45"]:
            with self.subTest(
                caracteristiques=[Purchase.Characteristic.LOCAL],
                definition_local=Purchase.Local.KM,
                definition_local_km=VALUE_NOT_OK,
            ):
                self.assertRaises(
                    (ValueError, ValidationError),
                    PurchaseFactory,
                    caracteristiques=[Purchase.Characteristic.LOCAL],
                    definition_local=Purchase.Local.KM,
                    definition_local_km=VALUE_NOT_OK,
                )
        # caracteristiques includes "LOCAL" and definition_local is not "KM"
        for VALUE_NOT_OK in [0, 1, 100, "200", Decimal("123.45")]:
            with self.subTest(
                caracteristiques=[Purchase.Characteristic.LOCAL],
                definition_local=Purchase.Local.PAT,
                definition_local_km=VALUE_NOT_OK,
            ):
                self.assertRaises(
                    ValidationError,
                    PurchaseFactory,
                    caracteristiques=[Purchase.Characteristic.LOCAL],
                    definition_local=Purchase.Local.PAT,
                    definition_local_km=VALUE_NOT_OK,
                )
        # caracteristiques does not include "LOCAL"
        for VALUE_NOT_OK in [0, 1, 100, "200", Decimal("123.45")]:
            with self.subTest(
                caracteristiques=[],
                definition_local=None,
                definition_local_km=VALUE_NOT_OK,
            ):
                self.assertRaises(
                    ValidationError,
                    PurchaseFactory,
                    caracteristiques=[],
                    definition_local=None,
                    definition_local_km=VALUE_NOT_OK,
                )
            with self.subTest(
                caracteristiques=[Purchase.Characteristic.BIO],
                definition_local=None,
                definition_local_km=VALUE_NOT_OK,
            ):
                self.assertRaises(
                    ValidationError,
                    PurchaseFactory,
                    caracteristiques=[Purchase.Characteristic.BIO],
                    definition_local=None,
                    definition_local_km=VALUE_NOT_OK,
                )

    def test_purchase_prix_ht_validation(self):
        """
        - field is required
        - must be >= 0
        """
        for TUPLE_OK in [(0, 0), (1000, 1000), ("2000", 2000), (Decimal("1234.56"), Decimal("1234.56"))]:
            with self.subTest(prix_ht=TUPLE_OK[0]):
                purchase = PurchaseFactory(prix_ht=TUPLE_OK[0])
                self.assertEqual(purchase.prix_ht, TUPLE_OK[1])
        for VALUE_NOT_OK in [None, -100, "", "invalid"]:
            with self.subTest(prix_ht=VALUE_NOT_OK):
                self.assertRaises(ValidationError, PurchaseFactory, prix_ht=VALUE_NOT_OK)


class PurchaseModelDeleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.purchase = PurchaseFactory()

    def test_purchase_soft_delete(self):
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Purchase.all_objects.count(), 1)

        self.purchase.delete()

        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Purchase.all_objects.count(), 1)

    def test_purchase_hard_delete(self):
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Purchase.all_objects.count(), 1)

        self.purchase.hard_delete()

        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Purchase.all_objects.count(), 0)


class PurchaseQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory()
        cls.purchase_2023_canteen = PurchaseFactory(canteen=cls.canteen, date="2023-01-01")
        cls.purchase_2024 = PurchaseFactory(date="2024-01-01")

    def test_for_user_queryset(self):
        self.assertEqual(Purchase.objects.for_user(self.user).count(), 0)

        self.canteen.managers.add(self.user)
        self.canteen.save()

        self.assertEqual(Purchase.objects.for_user(self.user).count(), 1)

    def test_for_year_queryset(self):
        self.assertEqual(Purchase.objects.for_year(2022).count(), 0)
        self.assertEqual(Purchase.objects.for_year(2023).count(), 1)
        self.assertEqual(Purchase.objects.for_year(2024).count(), 1)


class PurchaseDeleteQuerySetAndPropertyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.purchase = PurchaseFactory()

    def test_all_objects_queryset(self):
        """
        The delete method should "soft delete" a purchase and have it hidden by default
        from querysets, unless specifically asked for
        """
        self.assertEqual(Purchase.objects.count(), 1)

        self.purchase.delete()

        self.assertEqual(Purchase.objects.all().count(), 0)
        self.assertEqual(Purchase.all_objects.all().count(), 1)

    def test_is_deleted_property(self):
        self.assertFalse(self.purchase.is_deleted)

        self.purchase.delete()

        self.assertTrue(self.purchase.is_deleted)


class PurchaseModelPropertiesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.purchase_empty = PurchaseFactory(
            canteen=cls.canteen, date="2026-01-01", caracteristiques=[], famille_produits=None, prix_ht=15
        )
        cls.purchase = PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[
                Purchase.Characteristic.BIO,
                Purchase.Characteristic.FRANCE,
                Purchase.Characteristic.CIRCUIT_COURT,
                Purchase.Characteristic.LOCAL,
            ],
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=15,
        )

    def test_purchase_categories_egalim_property(self):
        self.assertEqual(self.purchase_empty.categories_egalim, [])
        self.assertEqual(self.purchase.categories_egalim, [Purchase.Characteristic.BIO])

    def test_purchase_origine_property(self):
        self.assertEqual(self.purchase_empty.origine, None)
        self.assertEqual(self.purchase.origine, Purchase.Characteristic.FRANCE)

    def test_purchase_est_local_property(self):
        self.assertFalse(self.purchase_empty.est_local)
        self.assertTrue(self.purchase.est_local)

    def test_purchase_est_circuit_court_property(self):
        self.assertFalse(self.purchase_empty.est_circuit_court)
        self.assertTrue(self.purchase.est_circuit_court)

    def test_purchase_famille_produits_display_property(self):
        self.assertEqual(self.purchase_empty.famille_produits_display, "")
        self.assertEqual(self.purchase.famille_produits_display, "Boulangerie/Pâtisserie fraîches et surgelées")

    def test_purchase_caracteristiques_display_property(self):
        self.assertEqual(self.purchase_empty.caracteristiques_display, "")
        self.assertEqual(
            self.purchase.caracteristiques_display,
            "Bio, Origine France, Circuit-court, Produit local",
        )


class PurchaseSummaryFranceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[Purchase.Characteristic.FRANCE],
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=10,
        )
        PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[Purchase.Characteristic.CIRCUIT_COURT],
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=50,
        )
        PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[Purchase.Characteristic.EUROPE, Purchase.Characteristic.LOCAL],  # e.g. border
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=15,
        )
        PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[
                Purchase.Characteristic.FRANCE,
                Purchase.Characteristic.CIRCUIT_COURT,
                Purchase.Characteristic.LOCAL,
            ],
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=15,
        )
        PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[Purchase.Characteristic.EUROPE],
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=5,
        )
        PurchaseFactory(
            canteen=cls.canteen,
            date="2026-01-01",
            caracteristiques=[],
            famille_produits=Purchase.Family.BOULANGERIE,
            prix_ht=5,
        )

    def test_canteen_summary_for_year_france_2024(self):
        # before 2025, circuit court and local were seperated from France (like 2026)
        Purchase.objects.filter(canteen=self.canteen).update(date="2024-01-01")

        result = Purchase.canteen_summary_for_year(self.canteen, 2024)

        self.assertNotIn("valeur_boulangerie_europe", result)
        self.assertEqual(result["valeur_boulangerie_france"], 10 + 15)
        self.assertEqual(result["valeur_boulangerie_circuit_court"], 50 + 15)
        self.assertEqual(result["valeur_boulangerie_local"], 15 + 15)

    def test_canteen_summary_for_year_france_2025(self):
        # in 2025, circuit court and local were counted as France
        Purchase.objects.filter(canteen=self.canteen).update(date="2025-01-01")

        result = Purchase.canteen_summary_for_year(self.canteen, 2025)

        self.assertNotIn("valeur_boulangerie_europe", result)
        self.assertEqual(result["valeur_boulangerie_france"], 10 + 50 + 15 + 15)
        self.assertEqual(result["valeur_boulangerie_circuit_court"], 50 + 15)
        self.assertEqual(result["valeur_boulangerie_local"], 15 + 15)

    def test_canteen_summary_for_year_france_2026(self):
        # in 2026, Europe was added
        result = Purchase.canteen_summary_for_year(self.canteen, 2026)

        self.assertEqual(result["valeur_boulangerie_europe"], 15 + 5)
        self.assertEqual(result["valeur_boulangerie_france"], 10 + 15)
        self.assertEqual(result["valeur_boulangerie_circuit_court"], 50 + 15)
        self.assertEqual(result["valeur_boulangerie_local"], 15 + 15)
