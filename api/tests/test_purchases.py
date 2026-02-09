from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, PurchaseFactory, UserFactory
from data.models import Canteen, Diagnostic, Purchase
from data.models.creation_source import CreationSource


class PurchaseListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("purchase_list_create")

    def test_cannot_list_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_list_purchases_of_managed_canteens(self):
        # canteen managed by authenticated user
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(canteen=canteen)
        PurchaseFactory(canteen=canteen)
        # other user, other canteen, other purchases
        other_user = UserFactory()
        other_user_canteen = CanteenFactory(managers=[other_user])
        PurchaseFactory(canteen=other_user_canteen)
        canteen_not_managed = CanteenFactory()
        PurchaseFactory(canteen=canteen_not_managed)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 4)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)


class PurchaseListFilterApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        PurchaseFactory(
            canteen=cls.canteen,
            description="avoine",
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            characteristics=[Purchase.Characteristic.BIO],
            date="2020-01-01",
        )
        PurchaseFactory(
            canteen=cls.canteen,
            description="tomates",
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.PECHE_DURABLE],
            date="2020-01-02",
        )
        PurchaseFactory(
            canteen=cls.canteen,
            description="pommes",
            family=Purchase.Family.AUTRES,
            characteristics=[Purchase.Characteristic.PECHE_DURABLE],
            date="2020-02-01",
        )
        cls.other_canteen = CanteenFactory()
        PurchaseFactory(canteen=cls.other_canteen, description="secret", date="2020-01-01")
        cls.url = reverse("purchase_list_create")

    @authenticate
    def test_filter_by_search_text(self):
        # user is not (yet) the manager of the canteen
        search_term = "avoine"

        response = self.client.get(f"{self.url}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 0)

        # set the user as manager of the canteen
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("description"), "avoine")

    @authenticate
    def test_filter_by_canteen(self):
        # user is not (yet) the manager of any canteen
        response = self.client.get(f"{self.url}?canteen__id={self.canteen.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 0)

        # set the user as manager of the canteen
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?canteen__id={self.canteen.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)

        # try to filter by a canteen the user doesn't manage
        response = self.client.get(f"{self.url}?canteen__id={self.other_canteen.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 0)

    @authenticate
    def test_filter_by_characteristic(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?characteristics={Purchase.Characteristic.BIO}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

        response = self.client.get(
            f"{self.url}?characteristics={Purchase.Characteristic.BIO}&characteristics={Purchase.Characteristic.PECHE_DURABLE}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)

    @authenticate
    def test_filter_by_family(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?family={Purchase.Family.PRODUITS_DE_LA_MER}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

    @authenticate
    def test_filter_by_date(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?date_after=2020-01-02")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

        response = self.client.get(f"{self.url}?date_before=2020-01-01")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)

        response = self.client.get(f"{self.url}?date_after=2020-01-02&date_before=2020-02-01")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)

    @authenticate
    def test_available_filter_options(self):
        """
        Test that filter options with data are included in purchases list response
        """
        self.canteen.managers.add(authenticate.user)

        with self.assertNumQueries(7):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 3)
        self.assertEqual(len(body["families"]), 2)
        self.assertEqual(len(body["characteristics"]), 2)
        self.assertEqual(len(body["canteens"]), 1)

        response = self.client.get(f"{self.url}?characteristics={Purchase.Characteristic.BIO}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 2)
        self.assertEqual(len(body["characteristics"]), 2)
        self.assertEqual(len(body["families"]), 1)

        response = self.client.get(f"{self.url}?family={Purchase.Family.PRODUITS_LAITIERS}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 0)
        self.assertEqual(len(body["characteristics"]), 0)
        self.assertEqual(len(body["families"]), 0)


class PurchaseListExportApiTest(APITestCase):
    def test_excel_export_unauthenticated(self):
        response = self.client.get(reverse("purchase_list_export"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_excel_export(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(description="avoine", canteen=canteen)
        PurchaseFactory(description="tomates", canteen=canteen)
        PurchaseFactory(description="pommes", canteen=canteen)

        response = self.client.get(reverse("purchase_list_export"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    @authenticate
    def test_excel_export_search(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(description="avoine", canteen=canteen)
        PurchaseFactory(description="tomates", canteen=canteen)
        PurchaseFactory(description="pommes", canteen=canteen)

        search_term = "avoine"
        response = self.client.get(f"{reverse('purchase_list_export')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @authenticate
    def test_excel_export_filter(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(family=Purchase.Family.PRODUITS_DE_LA_MER, description="avoine", canteen=canteen)
        PurchaseFactory(family=Purchase.Family.PRODUITS_DE_LA_MER, description="tomates", canteen=canteen)
        PurchaseFactory(family=Purchase.Family.AUTRES, description="pommes", canteen=canteen)

        response = self.client.get(f"{reverse('purchase_list_export')}?family=PRODUITS_DE_LA_MER")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class PurchaseDetailApiTest(APITestCase):
    def test_cannot_get_purchase_unauthenticated(self):
        """
        This endpoint is only available when authenticated
        """
        purchase = PurchaseFactory()
        response = self.client.get(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_someone_elses_purchase(self):
        """
        This endpoint can only return the purchase of canteens the logged user manages
        """
        other_user = UserFactory()
        other_user_canteen = CanteenFactory(managers=[other_user])
        purchase = PurchaseFactory(canteen=other_user_canteen)

        response = self.client.get(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_get_purchase(self):
        """
        The logged user should get the purchase that concern them
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        purchase = PurchaseFactory(canteen=canteen)

        response = self.client.get(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], purchase.id)


class PurchaseCreateApiTest(APITestCase):
    def test_create_purchase_unauthenticated(self):
        """
        The purchase creation is only available when logged in
        """
        payload = {
            "date": "2022-01-13",
            "canteen_id": 1,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase_someone_elses_canteen(self):
        """
        A user can only create a purchase of a canteen they manage
        """
        other_user = UserFactory()
        other_user_canteen = CanteenFactory(managers=[other_user])

        payload = {
            "date": "2022-01-13",
            "canteen": other_user_canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase(self):
        """
        A user can create a purchase
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "date": "2022-01-13",
            "canteen": canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO", "LOCAL"],
            "price_ht": 15.23,
            "local_definition": "AUTOUR_SERVICE",
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.local_definition, Purchase.Local.AUTOUR_SERVICE)
        self.assertEqual(len(purchase.characteristics), 2)

    @authenticate
    def test_create_purchase_creation_source(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "date": "2022-01-13",
            "canteen": canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO", "LOCAL"],
            "price_ht": 15.23,
            "local_definition": "AUTOUR_SERVICE",
        }

        # from the APP
        response = self.client.post(reverse("purchase_list_create"), {**payload, "creation_source": "APP"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_purchase = Purchase.objects.get(pk=body["id"])
        self.assertEqual(created_purchase.creation_source, CreationSource.APP)

        # defaults to API
        response = self.client.post(reverse("purchase_list_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_purchase = Purchase.objects.get(pk=body["id"])
        self.assertEqual(created_purchase.creation_source, CreationSource.API)

        # returns a 404 if the creation_source is not valid
        response = self.client.post(reverse("purchase_list_create"), {**payload, "creation_source": "UNKNOWN"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_purchase_nonexistent_canteen(self):
        """
        A user cannot create a purchase for an nonexistent canteen
        """
        CanteenFactory(managers=[authenticate.user])

        payload = {
            "date": "2022-01-13",
            "canteen": "9999",
            "description": "Saumon",
            "provider": "Test provider",
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PurchaseUpdateApiTest(APITestCase):
    def test_update_purchases_unauthenticated(self):
        """
        The purchase update is only available when logged in
        """
        purchase = PurchaseFactory()
        payload = {
            "id": purchase.id,
            "price_ht": 15.23,
        }
        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_update_purchase_with_put(self):
        """
        A user cannot update the data from a purchase object with PUT
        """
        purchase = PurchaseFactory()
        purchase.canteen.managers.add(authenticate.user)

        payload = {
            "id": purchase.id,
            "description": "Saumon",
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.put(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_update_purchase(self):
        """
        A user can update the data from a purchase object
        """
        purchase = PurchaseFactory()
        purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "id": purchase.id,
            "canteen": new_canteen.id,
            "description": "Saumon",
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        purchase.refresh_from_db()
        self.assertEqual(purchase.canteen, new_canteen)
        self.assertEqual(purchase.description, "Saumon")
        self.assertEqual(purchase.provider, "Test provider")
        self.assertEqual(float(purchase.price_ht), 15.23)

    @authenticate
    def test_update_someone_elses_purchase(self):
        """
        A user should not be able to update someone else's purchase object
        """
        purchase = PurchaseFactory()

        payload = {
            "id": purchase.id,
            "description": "Saumon",
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_update_someone_elses_canteen(self):
        """
        A user should not be able to set someone else's canteen in a purchase update
        """
        purchase = PurchaseFactory()
        purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory()

        payload = {
            "id": purchase.id,
            "canteen": new_canteen.id,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PurchaseDeleteApiTest(APITestCase):
    @authenticate
    def test_delete_purchase(self):
        """
        A user can delete a purchase object
        """
        purchase = PurchaseFactory()
        purchase.canteen.managers.add(authenticate.user)

        response = self.client.delete(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Purchase.objects.filter(pk=purchase.id).count(), 0)

    @authenticate
    def test_delete_unauthorized(self):
        """
        A user cannot delete a purchase object of a canteen they don't manage
        """
        purchase = PurchaseFactory()

        response = self.client.delete(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Purchase.objects.filter(pk=purchase.id).count(), 1)

    def test_delete_unauthenticated(self):
        """
        A user cannot delete a purchase object of a canteen if they're not authenticated
        """
        purchase = PurchaseFactory()

        response = self.client.delete(reverse("purchase_retrieve_update_destroy", kwargs={"pk": purchase.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Purchase.objects.filter(pk=purchase.id).count(), 1)  #

    @authenticate
    def test_delete_multiple_purchases(self):
        """
        Given a list of purchase ids, soft delete those purchases
        """
        purchase_1 = PurchaseFactory(deletion_date=None)
        purchase_1.canteen.managers.add(authenticate.user)
        purchase_2 = PurchaseFactory(deletion_date=None)
        purchase_2.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse("delete_purchases"), {"ids": [purchase_1.id, purchase_2.id]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        purchase_1.refresh_from_db()
        purchase_2.refresh_from_db()
        self.assertIsNotNone(purchase_1.deletion_date)
        self.assertIsNotNone(purchase_2.deletion_date)

    @authenticate
    def test_delete_invalid_purchases(self):
        """
        Ignore ids that are: non-existant; already deleted; not managed by the user
        And delete what can be deleted
        """
        purchase_should_delete = PurchaseFactory(deletion_date=None)
        date = timezone.now()
        purchase_already_deleted = PurchaseFactory(deletion_date=date)
        purchase_should_delete.canteen.managers.add(authenticate.user)
        purchase_already_deleted.canteen.managers.add(authenticate.user)
        invalid_id = "999"
        not_mine = PurchaseFactory(deletion_date=None)
        ids = [purchase_should_delete.id, purchase_already_deleted.id, invalid_id, not_mine.id]

        response = self.client.post(reverse("delete_purchases"), {"ids": ids}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        purchase_should_delete.refresh_from_db()
        self.assertIsNotNone(purchase_should_delete.deletion_date)
        purchase_already_deleted.refresh_from_db()
        self.assertEqual(purchase_already_deleted.deletion_date, date)
        not_mine.refresh_from_db()
        self.assertIsNone(not_mine.deletion_date)


class PurchaseRestoreApiTest(APITestCase):
    @authenticate
    def test_restore_purchases(self):
        """
        This endpoint restores the given IDs of deleted purchases
        """
        date = timezone.now()
        purchase_1 = PurchaseFactory(deletion_date=date)
        purchase_2 = PurchaseFactory(deletion_date=date)
        purchase_not_me = PurchaseFactory(deletion_date=date)
        for purchase in [purchase_1, purchase_2, purchase_not_me]:
            purchase.canteen.managers.add(authenticate.user)
        not_my_purchase = PurchaseFactory(deletion_date=date)

        response = self.client.post(
            reverse("restore_purchases"), {"ids": [purchase_1.id, purchase_2.id, not_my_purchase.id]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 2)
        purchase_1.refresh_from_db()
        purchase_2.refresh_from_db()
        purchase_not_me.refresh_from_db()
        not_my_purchase.refresh_from_db()
        self.assertIsNone(purchase_1.deletion_date)
        self.assertIsNone(purchase_2.deletion_date)
        self.assertEqual(purchase_not_me.deletion_date, date)
        self.assertEqual(not_my_purchase.deletion_date, date)


class PurchaseCanteenSummaryApiTest(APITestCase):
    @authenticate
    def test_purchase_not_authorized(self):
        canteen = CanteenFactory()

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_purchase_nonexistent_canteen(self):
        response = self.client.get(reverse("canteen_purchases_summary", kwargs={"canteen_pk": 999999}), {"year": 2020})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_purchase_total_summary(self):
        """
        Given a year, return spending by category
        Bio category is the sum of all products with either bio or bio en conversion labels
        Every category apart from bio should exlude bio (so bio + label rouge gets counted in bio but not label rouge)
        The categories with multiple labels on them should count items with two or more labels once
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        # For the year 2020
        # bio (+ rouge)
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
            price_ht=50,
        )
        # bio en conversion (+ igp)
        PurchaseFactory(
            canteen=canteen,
            date="2020-08-01",
            characteristics=[Purchase.Characteristic.CONVERSION_BIO, Purchase.Characteristic.IGP],
            price_ht=150,
        )
        # bio + commerce équitable
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.COMMERCE_EQUITABLE],
            price_ht=20,
        )
        # hve x2 = 10
        PurchaseFactory(canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.HVE], price_ht=2)
        PurchaseFactory(canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.HVE], price_ht=8)
        # rouge x2 = 20
        PurchaseFactory(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.LABEL_ROUGE], price_ht=12
        )
        PurchaseFactory(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.LABEL_ROUGE], price_ht=8
        )
        # aoc, igp + igp = 30
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.AOCAOP, Purchase.Characteristic.IGP],
            price_ht=22,
        )
        PurchaseFactory(canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.IGP], price_ht=4)
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.IGP, Purchase.Characteristic.HVE],
            price_ht=4,
        )
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.EXTERNALITES, Purchase.Characteristic.PERFORMANCE],
            price_ht=30,
        )
        PurchaseFactory(
            canteen=canteen, date="2020-01-01", characteristics=[Purchase.Characteristic.PERFORMANCE], price_ht=15
        )
        # some other durable label
        PurchaseFactory(
            canteen=canteen, date="2020-01-08", characteristics=[Purchase.Characteristic.PECHE_DURABLE], price_ht=240
        )
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-15",
            characteristics=[Purchase.Characteristic.COMMERCE_EQUITABLE],
            price_ht=10,
        )
        # no labels
        PurchaseFactory(canteen=canteen, date="2020-01-01", characteristics=[], price_ht=500)

        # Not in the year 2020 - smoke test for year filtering
        PurchaseFactory(
            canteen=canteen, date="2019-01-01", characteristics=[Purchase.Characteristic.BIO], price_ht=666
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["valeurTotale"], 1075.0)
        self.assertEqual(body["valeurBio"], 220.0)
        self.assertEqual(body["valeurBioDontCommerceEquitable"], 20.0)
        self.assertEqual(body["valeurSiqo"], 50.0)
        self.assertEqual(body["valeurEgalimAutres"], 260.0)
        self.assertEqual(body["valeurEgalimAutresDontCommerceEquitable"], 10.0)
        self.assertEqual(body["valeurExternalitesPerformance"], 45.0)

    @authenticate
    def test_complex_purchase_total_summary(self):
        """
        Given a year, return spending by category
        Bio category is the sum of all products with bio label
        Every category apart from bio should exclude bio (so bio + label rouge gets counted in bio but not label rouge)
        Categories should respect the heirarchy (if something is label rouge + AOC only count in rouge; if AOC and fermier count in AOC only)
        The three categories outside of EGalim should get the totals regardless of what other labels they have
        The category of AOC/AOP/IGP/STG should count items with two or more labels once (applicable to extended declaration)
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        d = "2020-03-01"

        # test that bio trumps other labels, but doesn't stop non-EGalim labels
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.FRUITS_ET_LEGUMES,
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.AOCAOP],
            price_ht=120,
        )
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.FRUITS_ET_LEGUMES,
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.COMMERCE_EQUITABLE],
            price_ht=80,
        )

        # check that sums are separate between families
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.VIANDES_VOLAILLES,
            characteristics=[
                Purchase.Characteristic.BIO,
                Purchase.Characteristic.CIRCUIT_COURT,
                Purchase.Characteristic.LOCAL,
            ],
            local_definition=Purchase.Local.AUTRE,
            price_ht=10,
        )

        # check that AOC and STG are regrouped and do not count bio totals and trump some other labels
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.FRUITS_ET_LEGUMES,
            characteristics=[Purchase.Characteristic.AOCAOP],
            price_ht=20,
        )
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.FRUITS_ET_LEGUMES,
            characteristics=[Purchase.Characteristic.STG, Purchase.Characteristic.COMMERCE_EQUITABLE],
            price_ht=60,
        )

        # check that can have a family with only non-EGalim labels
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.AUTRES,
            characteristics=[Purchase.Characteristic.LOCAL],
            local_definition=Purchase.Local.AUTRE,
            price_ht=50,
        )
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.AUTRES,
            characteristics=[Purchase.Characteristic.LOCAL],
            local_definition=Purchase.Local.AUTRE,
            price_ht=50,
        )

        # check that circuit_court meat will include both this and the bio purchase which is also short dist.
        PurchaseFactory(
            canteen=canteen,
            date=d,
            family=Purchase.Family.VIANDES_VOLAILLES,
            characteristics=[Purchase.Characteristic.CIRCUIT_COURT],
            price_ht=90,
        )

        # check that items with no label are included in total
        PurchaseFactory(canteen=canteen, date=d, family=Purchase.Family.AUTRES, characteristics=[], price_ht=110)

        # Not in the year 2020 - smoke test for year filtering
        PurchaseFactory(
            canteen=canteen, date="2019-01-01", characteristics=[Purchase.Characteristic.BIO], price_ht=666
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["valeurTotale"], 590.0)
        self.assertEqual(body["valeurFruitsEtLegumesBio"], 200.0)
        self.assertEqual(body["valeurViandesVolaillesBio"], 10.0)
        self.assertEqual(body["valeurFruitsEtLegumesBioDontCommerceEquitable"], 80.0)
        self.assertEqual(body["valeurViandesVolaillesBioDontCommerceEquitable"], 0)
        self.assertEqual(body["valeurFruitsEtLegumesAocaopIgpStg"], 80.0)
        self.assertEqual(body["valeurFruitsEtLegumesCommerceEquitable"], 0.0)
        self.assertEqual(body["valeurAutresLocal"], 100.0)
        self.assertEqual(body["valeurViandesVolaillesCircuitCourt"], 100.0)
        self.assertEqual(body["valeurViandesVolaillesLocal"], 10.0)
        self.assertEqual(body["valeurAutresNonEgalim"], 210.0)
        self.assertEqual(body["valeurViandesVolaillesNonEgalim"], 90.0)
        self.assertEqual(body["valeurExternalitesPerformance"], 0.0)

    def test_purchase_summary_unauthenticated(self):
        canteen = CanteenFactory()
        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_purchase_meat_totals(self):
        """
        The totals for "viandes et volailles" must be included in the payload
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        # Should be counted both on EGalim and "Provenance France"
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[
                Purchase.Characteristic.BIO,
                Purchase.Characteristic.LABEL_ROUGE,
                Purchase.Characteristic.FRANCE,
            ],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=50,
        )

        # Should be counted on EGalim
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=40,
        )

        # Should be counted on EGalim
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=30,
        )

        # Should not be counted as EGalim, only included in the total
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=20,
        )

        # Should be counted on provenance france
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.FRANCE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=15,
        )

        # Not in the year 2020 - should not be included at all
        PurchaseFactory(
            canteen=canteen,
            date="2019-01-01",
            characteristics=[],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=10,
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["valeurViandesVolailles"], 155.0)
        self.assertEqual(body["valeurViandesVolaillesEgalim"], 120.0)
        self.assertEqual(body["valeurViandesVolaillesFrance"], 65.0)

    @authenticate
    def test_purchase_fish_totals(self):
        """
        The totals for "poissons, produits de la mer et de l'aquaculture" must be included in the payload
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        # Should be counted on EGalim only once
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=55,
        )

        # Should be counted on EGalim
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.BIO],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=40,
        )

        # Should be counted on EGalim
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=30,
        )

        # Should not be counted as EGalim, only included in the total
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=20,
        )

        # Should not be counted as EGalim, only included in the total
        PurchaseFactory(
            canteen=canteen,
            date="2020-01-01",
            characteristics=[Purchase.Characteristic.FRANCE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=15,
        )

        # Not in the year 2020 - should not be included at all
        PurchaseFactory(
            canteen=canteen,
            date="2019-01-01",
            characteristics=[],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=10,
        )

        response = self.client.get(
            reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2020}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["valeurProduitsDeLaMer"], 160.0)
        self.assertEqual(body["valeurProduitsDeLaMerEgalim"], 125.0)

    @authenticate
    def test_get_multi_year_purchase_statistics(self):
        """
        It is possible for a manager to retrieve year-on-year purchase totals for a canteen
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        PurchaseFactory(canteen=canteen, price_ht=100, date="2020-01-01")
        PurchaseFactory(canteen=canteen, price_ht=50, date="2020-12-31")
        PurchaseFactory(canteen=canteen, price_ht=300, date="2021-01-01")
        PurchaseFactory(canteen=canteen, price_ht=150, date="2021-12-31")

        other_canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(canteen=other_canteen, price_ht=999, date="2021-01-01")

        response = self.client.get(reverse("canteen_purchases_summary", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("results", body)
        self.assertEqual(len(body["results"]), 2)
        self.assertEqual(body["results"][0]["year"], 2020)
        self.assertEqual(body["results"][0]["valeurTotale"], 150)
        self.assertIn("valeurBio", body["results"][0])
        self.assertEqual(body["results"][1]["year"], 2021)
        self.assertEqual(body["results"][1]["valeurTotale"], 450)


class PurchaseCanteenOptionsApiTest(APITestCase):
    def test_get_purchase_options_unauthenticated(self):
        response = self.client.get(reverse("purchase_options"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_purchase_options(self):
        """
        A manager should be able to retrieve a list of products and providers that
        they've already entered on their own purchases
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(description="avoine", canteen=canteen, provider="provider1")
        PurchaseFactory(description="pommes", canteen=canteen, provider="provider2")
        PurchaseFactory(description="pommes", canteen=canteen, provider="provider1")
        PurchaseFactory(description=None, canteen=canteen, provider=None)

        PurchaseFactory(description="secret product", provider="secret provider")

        response = self.client.get(f"{reverse('purchase_options')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["products"]), 2)
        self.assertEqual(len(body["providers"]), 2)
        self.assertIn("avoine", body["products"])
        self.assertIn("provider2", body["providers"])
        self.assertNotIn("secret product", body["products"])
        self.assertNotIn("secret provider", body["providers"])


class DiagnosticsFromPurchasesApiTest(APITestCase):
    @freeze_time("2022-02-10")  # during the 2021 campaign
    @authenticate
    def test_create_diagnostics_from_purchases(self):
        """
        Given a list of canteen ids and a year, create diagnostics
        pre-filled with purchase totals for that year
        """
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[authenticate.user])
        central_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[authenticate.user])
        canteens = [canteen_site, central_groupe]
        # purchases to be included in totals
        PurchaseFactory(
            canteen=canteen_site,
            date="2021-01-01",
            price_ht=50,
            family=Purchase.Family.BOISSONS,
            characteristics=[Purchase.Characteristic.AOCAOP],
        )
        # TODO: would be nice to double check the AOCAOP IGP STG aggregation vs other labels
        PurchaseFactory(
            canteen=canteen_site,
            date="2021-12-31",
            price_ht=150,
            family=Purchase.Family.BOULANGERIE,
            characteristics=[],
        )

        PurchaseFactory(canteen=central_groupe, date="2021-01-01", price_ht=5)
        PurchaseFactory(canteen=central_groupe, date="2021-12-31", price_ht=15)

        # purchases to be filtered out from totals
        PurchaseFactory(canteen=canteen_site, date="2022-01-01", price_ht=666)
        PurchaseFactory(canteen=central_groupe, date="2020-12-31", price_ht=666)

        year = 2021
        self.assertEqual(Diagnostic.objects.filter(year=year, canteen__in=canteens).count(), 0)

        response = self.client.post(
            reverse("diagnostics_from_purchases", kwargs={"year": year}),
            {"canteenIds": [canteen_site.id, central_groupe.id]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)
        diag_site = Diagnostic.objects.get(year=year, canteen=canteen_site)
        self.assertIn(diag_site.id, results)
        self.assertEqual(diag_site.valeur_totale, 200)
        # TODO: would be nice to test the aggregation for a simple value (e.g. valeur_siqo)
        self.assertEqual(diag_site.valeur_boissons_aocaop_igp_stg, 50)
        self.assertEqual(diag_site.valeur_boulangerie_non_egalim, 150)
        self.assertEqual(diag_site.valeur_autres_aocaop_igp_stg, 0)
        self.assertEqual(diag_site.central_kitchen_diagnostic_mode, None)
        self.assertEqual(diag_site.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        diag_cc = Diagnostic.objects.get(year=year, canteen=central_groupe)
        self.assertIn(diag_cc.id, results)
        self.assertEqual(diag_cc.valeur_totale, 20)
        self.assertEqual(diag_cc.central_kitchen_diagnostic_mode, "APPRO")

    def test_unauthorised_create_diagnostics_from_purchases(self):
        """
        If not logged in, throw a 403
        """
        response = self.client.post(reverse("diagnostics_from_purchases", kwargs={"year": 2020}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_missing_canteens_create_diagnostics_from_purchases(self):
        """
        If canteen ids are missing, throw a 400
        """
        response = self.client.post(reverse("diagnostics_from_purchases", kwargs={"year": 2021}), {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2024-02-10")  # during the 2023 campaign
    @authenticate
    def test_errors_for_create_diagnostics_from_purchases(self):
        """
        Handle errors in diagnostic creation gracefully, creating what can be created
        """
        canteen_with_diag = CanteenFactory(managers=[authenticate.user])
        canteen_without_purchases = CanteenFactory(managers=[authenticate.user])
        good_canteen = CanteenFactory(managers=[authenticate.user])
        canteens = [canteen_with_diag, canteen_without_purchases, good_canteen]
        not_my_canteen = CanteenFactory()

        year = 2023
        DiagnosticFactory(canteen=canteen_with_diag, year=year)
        PurchaseFactory(canteen=good_canteen, date=f"{year}-01-01", price_ht=100)
        PurchaseFactory(canteen=canteen_with_diag, date=f"{year}-01-01", price_ht=666)
        PurchaseFactory(canteen=not_my_canteen, date=f"{year}-01-01", price_ht=666)

        response = self.client.post(
            reverse("diagnostics_from_purchases", kwargs={"year": year}),
            {"canteenIds": ["666", not_my_canteen.id] + [canteen.id for canteen in canteens]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 1)
        errors = body["errors"]
        self.assertEqual(errors[0], "Cantine inconnue : 666")
        self.assertEqual(errors[1], f"Vous ne gérez pas la cantine : {not_my_canteen.id}")
        self.assertEqual(
            errors[2], f"Il existe déjà un diagnostic pour l'année 2023 pour la cantine : {canteen_with_diag.id}"
        )
        self.assertEqual(errors[3], f"Aucun achat trouvé pour la cantine : {canteen_without_purchases.id}")
        self.assertEqual(len(errors), 4)


class PublicPurchasePublicSummaryApiTest(APITestCase):
    def test_get_public_purchases_summary(self):
        """
        Return percentages from purchase data for the given year and canteen
        """
        canteen = CanteenFactory()
        year = 2024

        # bio percent, ignore lesser labels
        PurchaseFactory(
            canteen=canteen,
            date="2024-01-01",
            characteristics=[Purchase.Characteristic.BIO, Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=10,
        )
        # sustainable percent, meat egalim
        PurchaseFactory(
            canteen=canteen,
            date="2024-01-01",
            characteristics=[Purchase.Characteristic.LABEL_ROUGE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=10,
        )
        # externalities percent, meat egalim, meat france
        PurchaseFactory(
            canteen=canteen,
            date="2024-01-01",
            characteristics=[Purchase.Characteristic.EXTERNALITES, Purchase.Characteristic.FRANCE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=10,
        )
        # egalim others, fish egalim
        PurchaseFactory(
            canteen=canteen,
            date="2024-01-01",
            characteristics=[Purchase.Characteristic.PECHE_DURABLE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=10,
        )
        # meat france (local and circuit_court not included?)
        PurchaseFactory(
            canteen=canteen,
            date="2024-12-31",
            characteristics=[Purchase.Characteristic.FRANCE],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=10,
        )
        # fish non egalim
        PurchaseFactory(
            canteen=canteen,
            date="2024-12-31",
            characteristics=[Purchase.Characteristic.FRANCE],
            family=Purchase.Family.PRODUITS_DE_LA_MER,
            price_ht=10,
        )
        # add misc purchase to have nice round total of 100 HT
        PurchaseFactory(
            canteen=canteen,
            date="2024-12-31",
            characteristics=[],
            family=Purchase.Family.AUTRES,
            price_ht=40,
        )

        # create purchase outside of requested year to check filtering
        PurchaseFactory(
            canteen=canteen,
            date="2023-12-31",
            characteristics=[Purchase.Characteristic.BIO],
            family=Purchase.Family.VIANDES_VOLAILLES,
            price_ht=999999,
        )

        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}), {"year": year}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        # total 2024: 100
        # total 2024 bio: 10
        self.assertEqual(body["percentageValeurBio"], 0.1)
        self.assertEqual(body["percentageValeurSiqo"], 0.1)
        self.assertEqual(body["percentageValeurExternalitesPerformance"], 0.1)
        self.assertEqual(body["percentageValeurEgalimAutres"], 0.1)
        # total 2024 viandes volailles: 40
        # total 2024 viandes volailles egalim: 30
        # total 2024 viandes volailles france: 20
        self.assertEqual(body["percentageValeurViandesVolaillesEgalim"], 0.75)
        self.assertEqual(body["percentageValeurViandesVolaillesFrance"], 0.5)
        # total 2024 produits de la mer: 20
        # total 2024 produits de la mer egalim: 10
        # total 2024 produits de la mer france: 10
        self.assertEqual(body["percentageValeurProduitsDeLaMerEgalim"], 0.5)
        self.assertEqual(body["percentageValeurProduitsDeLaMerFrance"], 0.5)

    def test_cannot_get_redacted_purchases_summary(self):
        """
        If the canteen has redacted the year return a 404
        TODO: do we really want to use redacted_appro_years to control this?
        """
        canteen = CanteenFactory(redacted_appro_years=[2024])
        PurchaseFactory(canteen=canteen, date="2024-01-01")
        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2024}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_purchases_for_public_summary(self):
        """
        If the canteen doesn't have purchases for the year requested return a 404
        """
        canteen = CanteenFactory()
        PurchaseFactory(canteen=canteen, date="2023-12-31")
        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2024}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_get_last_purchase_date_in_public_summary_if_manager(self):
        """
        The purchases summary should return the last purchase date if the user
        is the manager of the canteen
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        PurchaseFactory(canteen=canteen, date="2024-12-01")
        PurchaseFactory(canteen=canteen, date="2024-05-31")
        PurchaseFactory(canteen=canteen, date="2025-01-01")

        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2024}
        )
        body = response.json()
        self.assertEqual(body["lastPurchaseDate"], "2024-12-01")

    @authenticate
    def test_dont_get_last_purchase_date_in_public_summary_if_not_manager(self):
        """
        The purchases summary should not return the last purchase date if the user
        is not the manager of the canteen, even if authenticated
        """
        canteen = CanteenFactory()
        PurchaseFactory(canteen=canteen, date="2024-05-31")

        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}), {"year": 2024}
        )
        body = response.json()
        self.assertNotIn("lastPurchaseDate", body)

    @authenticate
    def test_manager_can_optionally_get_redacted_purchases(self):
        """
        The manager of the canteen has an option to get redacted data
        """
        canteen = CanteenFactory(redacted_appro_years=[2024], managers=[authenticate.user])
        PurchaseFactory(canteen=canteen, date="2024-01-01")
        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}),
            {"year": 2024, "ignoreRedaction": "true"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_manager_can_optionally_not_get_redacted_purchases(self):
        """
        The manager of the canteen has an option to not get redacted data
        """
        canteen = CanteenFactory(redacted_appro_years=[2024], managers=[authenticate.user])
        PurchaseFactory(canteen=canteen, date="2024-01-01")
        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}),
            {"year": 2024, "ignoreRedaction": "false"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_non_manager_cannot_optionally_get_redacted_purchases(self):
        """
        Non-managers cannot get redacted canteen data
        """
        canteen = CanteenFactory(redacted_appro_years=[2024])
        PurchaseFactory(canteen=canteen, date="2024-01-01")
        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}),
            {"year": 2024, "ignoreRedaction": "true"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_cannot_optionally_get_redacted_purchases_summary(self):
        """
        Public cannot get redacted canteen data
        """
        canteen = CanteenFactory(redacted_appro_years=[2024])
        PurchaseFactory(canteen=canteen, date="2024-01-01")
        response = self.client.get(
            reverse("canteen_purchases_percentage_summary", kwargs={"canteen_pk": canteen.id}),
            {"year": 2024, "ignoreRedaction": "true"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
