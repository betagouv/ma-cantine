from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, PurchaseFactory, UserFactory
from data.models import Purchase
from data.models.creation_source import CreationSource


class PurchaseOldListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user])
        cls.purchase = PurchaseFactory(
            canteen=cls.canteen,
            description="tomates",
            fournisseur="fournisseur",
            date="2022-01-13",
            prix_ht=Decimal(4.5),
            famille_produits=Purchase.Family.FRUITS_ET_LEGUMES,
            caracteristiques=[Purchase.Characteristic.BIO, Purchase.Characteristic.EUROPE],
            creation_user=cls.user,
            creation_source=CreationSource.APP,
        )
        cls.url = reverse("purchase_list_create")

    def test_cannot_list_purchases_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_list_purchases_of_managed_canteens(self):
        # canteen managed by authenticated user
        self.canteen.managers.add(authenticate.user)
        # other user, other canteen, other purchases
        other_user = UserFactory()
        other_user_canteen = CanteenFactory(managers=[other_user])
        PurchaseFactory(canteen=other_user_canteen)
        canteen_not_managed = CanteenFactory()
        PurchaseFactory(canteen=canteen_not_managed)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Purchase.objects.count(), 1 + 1 + 1)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 1)

    def test_cannot_list_purchases_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PurchaseOldListFilterApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        PurchaseFactory(
            canteen=cls.canteen,
            description="avoine",
            famille_produits=Purchase.Family.PRODUITS_DE_LA_MER,
            caracteristiques=[Purchase.Characteristic.BIO],
            date="2020-01-01",
        )
        PurchaseFactory(
            canteen=cls.canteen,
            description="tomates",
            famille_produits=Purchase.Family.PRODUITS_DE_LA_MER,
            caracteristiques=[Purchase.Characteristic.BIO, Purchase.Characteristic.PECHE_DURABLE],
            date="2020-01-02",
        )
        PurchaseFactory(
            canteen=cls.canteen,
            description="pommes",
            famille_produits=Purchase.Family.AUTRES,
            caracteristiques=[Purchase.Characteristic.PECHE_DURABLE],
            date="2020-02-01",
        )
        cls.other_canteen = CanteenFactory()
        PurchaseFactory(
            canteen=cls.other_canteen,
            description="secret",
            famille_produits=None,
            caracteristiques=[],
            date="2020-01-01",
        )
        cls.url = reverse("purchase_list_create")

    @authenticate
    def test_filter_by_search_text(self):
        # user is not (yet) the manager of the canteen
        search_term = "avoine"

        response = self.client.get(f"{self.url}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 0)

        # set the user as manager of the canteen
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("description"), "avoine")

    @authenticate
    def test_filter_by_canteen(self):
        # user is not (yet) the manager of any canteen
        response = self.client.get(f"{self.url}?canteen__id={self.canteen.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 0)

        # set the user as manager of the canteen
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?canteen__id={self.canteen.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 3)

        # try to filter by a canteen the user doesn't manage
        response = self.client.get(f"{self.url}?canteen__id={self.other_canteen.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 0)

    @authenticate
    def test_filter_by_characteristics(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?characteristics={Purchase.Characteristic.BIO}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)

        response = self.client.get(
            f"{self.url}?characteristics={Purchase.Characteristic.BIO}&characteristics={Purchase.Characteristic.PECHE_DURABLE}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 3)

    @authenticate
    def test_filter_by_family(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?family={Purchase.Family.PRODUITS_DE_LA_MER}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)

    @authenticate
    def test_filter_by_date(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(f"{self.url}?date_after=2020-01-02")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)

        response = self.client.get(f"{self.url}?date_before=2020-01-01")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 1)

        response = self.client.get(f"{self.url}?date_after=2020-01-02&date_before=2020-02-01")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)

    @authenticate
    def test_pagination(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 3)
        self.assertIn("next", body)
        self.assertIn("previous", body)
        self.assertEqual(len(body["results"]), 3)
        self.assertEqual(len(body["families"]), 2)
        self.assertEqual(len(body["characteristics"]), 2)
        self.assertEqual(len(body["canteens"]), 1)

        response = self.client.get(f"{self.url}?limit=1&offset=1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 3)
        self.assertIn("next", body)
        self.assertIn("previous", body)
        self.assertEqual(len(body["results"]), 1)
        # the pagination should not change the available filter options
        self.assertEqual(len(body["families"]), 2)
        self.assertEqual(len(body["characteristics"]), 2)
        self.assertEqual(len(body["canteens"]), 1)

    @authenticate
    def test_available_filter_options(self):
        # set the user as manager + add an extra canteen with purchase
        self.canteen.managers.add(authenticate.user)
        canteen_2 = CanteenFactory(managers=[authenticate.user])
        PurchaseFactory(
            canteen=canteen_2, famille_produits=Purchase.Family.AUTRES, caracteristiques=[Purchase.Characteristic.BIO]
        )

        with self.assertNumQueries(7):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 3 + 1)
        self.assertEqual(len(body["families"]), 2)
        self.assertEqual(len(body["characteristics"]), 2)
        self.assertEqual(len(body["canteens"]), 1 + 1)

        response = self.client.get(f"{self.url}?characteristics={Purchase.Characteristic.BIO}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 2 + 1)
        self.assertEqual(len(body["characteristics"]), 2)
        self.assertEqual(len(body["families"]), 1 + 1)
        self.assertEqual(len(body["canteens"]), 1 + 1)

        response = self.client.get(f"{self.url}?family={Purchase.Family.PRODUITS_LAITIERS}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 0)
        self.assertEqual(len(body["characteristics"]), 0)
        self.assertEqual(len(body["families"]), 0)
        self.assertEqual(len(body["canteens"]), 0)


class PurchaseOldDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user])
        cls.purchase = PurchaseFactory(
            canteen=cls.canteen,
            description="tomates",
            fournisseur="fournisseur",
            date="2022-01-13",
            prix_ht=Decimal(4.5),
            famille_produits=Purchase.Family.FRUITS_ET_LEGUMES,
            caracteristiques=[Purchase.Characteristic.BIO, Purchase.Characteristic.EUROPE],
            creation_user=cls.user,
            creation_source=CreationSource.APP,
        )
        cls.url = reverse("purchase_retrieve_update_destroy", kwargs={"pk": cls.purchase.id})

    def test_cannot_get_purchase_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_can_get_purchase(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.purchase.id)

    def test_cannot_get_purchase_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PurchaseOldCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user])
        cls.url = reverse("purchase_list_create")
        cls.PURCHASE_PAYLOAD = {
            "canteen": cls.canteen.id,
            "description": "Saumon",
            "provider": "Test fournisseur",
            "date": "2022-01-13",
            "price_ht": 15.23,
            "family": "PRODUITS_DE_LA_MER",
            "characteristics": ["BIO", "LOCAL"],
            "local_definition": "COMMUNE",
        }

    def test_cannot_create_purchase_if_unauthenticated(self):
        response = self.client.post(self.url, self.PURCHASE_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_purchase_if_canteen_does_not_exist(self):
        payload = {**self.PURCHASE_PAYLOAD, "canteen": 9999}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_purchase_if_not_canteen_manager(self):
        response = self.client.post(self.url, self.PURCHASE_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.post(self.url, self.PURCHASE_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        purchase = Purchase.objects.first()
        self.assertEqual(len(purchase.caracteristiques), 2)
        self.assertEqual(purchase.definition_local, Purchase.Local.COMMUNE)
        self.assertEqual(purchase.definition_local_km, None)

    @authenticate
    def test_create_purchase_creation_user_and_source(self):
        self.canteen.managers.add(authenticate.user)

        # from the APP
        payload = {**self.PURCHASE_PAYLOAD, "creation_source": CreationSource.APP}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertNotIn("creationUser", body)
        self.assertNotIn("creationSource", body)
        self.assertNotIn("creationSourceApiOauth2Application", body)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.creation_user, authenticate.user)
        self.assertEqual(purchase.creation_source, CreationSource.APP)
        self.assertEqual(purchase.creation_source_api_oauth2_application, None)

        # cleanup
        Purchase.objects.all().delete()

        # defaults to API
        response = self.client.post(self.url, self.PURCHASE_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertNotIn("creationUser", body)
        self.assertNotIn("creationSource", body)
        self.assertNotIn("creationSourceApiOauth2Application", body)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.creation_user, authenticate.user)
        self.assertEqual(purchase.creation_source, CreationSource.API)
        self.assertEqual(purchase.creation_source_api_oauth2_application, None)

        # cleanup
        Purchase.objects.all().delete()

        # returns a 404 if the creation_source is not valid
        payload = {**self.PURCHASE_PAYLOAD, "creation_source": "UNKNOWN"}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PurchaseOldUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user])
        cls.purchase = PurchaseFactory(canteen=cls.canteen, creation_user=cls.user, creation_source=CreationSource.APP)
        cls.url = reverse("purchase_retrieve_update_destroy", kwargs={"pk": cls.purchase.id})

    def test_cannot_update_purchase_if_unauthenticated(self):
        payload = {
            "price_ht": 15.23,
        }
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_update_purchase_with_put(self):
        self.purchase.canteen.managers.add(authenticate.user)

        payload = {
            "description": "Saumon",
            "provider": "Test fournisseur",
            "price_ht": 15.23,
        }
        response = self.client.put(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_cannot_update_if_not_canteen_manager(self):
        payload = {
            "description": "Saumon",
            "provider": "Test fournisseur",
            "price_ht": 15.23,
        }
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_to_another_canteen_if_not_canteen_manager(self):
        self.purchase.canteen.managers.add(authenticate.user)
        canteen_not_manager = CanteenFactory()

        payload = {
            "canteen": canteen_not_manager.id,
        }
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_update_purchase(self):
        self.purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "canteen": new_canteen.id,
            "description": "Saumon",
            "provider": "Test fournisseur",
            "price_ht": 15.23,
        }
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.canteen, new_canteen)
        self.assertEqual(self.purchase.description, "Saumon")
        self.assertEqual(self.purchase.fournisseur, "Test fournisseur")
        self.assertEqual(float(self.purchase.prix_ht), 15.23)

    @authenticate
    def test_can_update_purchase_does_not_update_creation_user_and_source(self):
        self.purchase.canteen.managers.add(authenticate.user)
        self.assertEqual(self.purchase.creation_user, self.user)
        self.assertEqual(self.purchase.creation_source, CreationSource.APP)
        self.assertEqual(self.purchase.creation_source_api_oauth2_application, None)

        payload = {
            "description": "Saumon",
            "provider": "Test fournisseur",
            "price_ht": 15.23,
            "creationSource": CreationSource.API,
        }
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("creationUser", body)
        self.assertNotIn("creationSource", body)
        self.assertNotIn("creationSourceApiOauth2Application", body)
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.creation_user, self.user)  # unchanged
        self.assertEqual(self.purchase.creation_source, CreationSource.APP)  # unchanged
        self.assertEqual(self.purchase.creation_source_api_oauth2_application, None)  # unchanged


class PurchaseOldDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user])
        cls.purchase = PurchaseFactory(canteen=cls.canteen, creation_user=cls.user, creation_source=CreationSource.APP)
        cls.url = reverse("purchase_retrieve_update_destroy", kwargs={"pk": cls.purchase.id})

    def test_cannot_delete_if_unauthenticated(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Purchase.objects.count(), 1)

    @authenticate
    def test_cannot_delete_if_not_canteen_manager(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Purchase.objects.count(), 1)

    @authenticate
    def test_can_delete_purchase(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Purchase.all_objects.count(), 1)
