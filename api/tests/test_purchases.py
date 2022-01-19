from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data.factories import UserFactory, PurchaseFactory, CanteenFactory
from .utils import authenticate


class TestPurchaseApi(APITestCase):
    def test_get_purchases_unauthenticated(self):
        """
        This endpoint is only available when authenticated
        """
        response = self.client.get(reverse("purchase_list_create"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_someone_elses_purchases(self):
        """
        This endpoint can only return the purchases of canteens the logged user manages
        """
        other_user = UserFactory.create()
        other_user_canteen = CanteenFactory.create()
        other_user_canteen.managers.add(other_user)

        PurchaseFactory.create(canteen=other_user_canteen)

        response = self.client.get(reverse("purchase_list_create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results", [])
        self.assertEqual(len(body), 0)

    @authenticate
    def test_get_purchases(self):
        """
        The logged user should get the purchases that concern them
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        PurchaseFactory.create(canteen=canteen)
        PurchaseFactory.create(canteen=canteen)

        response = self.client.get(reverse("purchase_list_create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results", [])
        self.assertEqual(len(body), 2)

    def test_create_purchase_unauthenticated(self):
        """
        The purchase creation is only available when logged in
        """
        payload = {
            "date": "2022-01-13",
            "canteen_id": 1,
            "provider": "Test provider",
            "category": "PECHE",
            "characteristic": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase_someone_elses_canteen(self):
        """
        A user can only create a purchase of a canteen they manage
        """
        other_user = UserFactory.create()
        other_user_canteen = CanteenFactory.create()
        other_user_canteen.managers.add(other_user)

        payload = {
            "date": "2022-01-13",
            "canteen": other_user_canteen.id,
            "provider": "Test provider",
            "category": "PECHE",
            "characteristic": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_purchase(self):
        """
        A user can create a purchase
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {
            "date": "2022-01-13",
            "canteen": canteen.id,
            "provider": "Test provider",
            "category": "PECHE",
            "characteristic": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @authenticate
    def test_create_purchase_nonexistent_canteen(self):
        """
        A user cannot create a purchase for an nonexistent canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {
            "date": "2022-01-13",
            "canteen": "999",
            "provider": "Test provider",
            "category": "PECHE",
            "characteristic": ["BIO"],
            "price_ht": 15.23,
        }
        response = self.client.post(reverse("purchase_list_create"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_purchases_unauthenticated(self):
        """
        The purchase update is only available when logged in
        """
        purchase = PurchaseFactory.create()
        payload = {
            "id": purchase.id,
            "price_ht": 15.23,
        }
        response = self.client.patch(
            reverse("purchase_retrieve_update", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_update_purchase(self):
        """
        A user can update the data from a purchase object
        """
        purchase = PurchaseFactory.create()
        purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory.create()
        new_canteen.managers.add(authenticate.user)

        payload = {
            "id": purchase.id,
            "canteen": new_canteen.id,
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        purchase.refresh_from_db()
        self.assertEqual(purchase.canteen, new_canteen)
        self.assertEqual(purchase.provider, "Test provider")
        self.assertEqual(float(purchase.price_ht), 15.23)

    @authenticate
    def test_update_someone_elses_purchase(self):
        """
        A user should not be able to update someone else's purchase object
        """
        purchase = PurchaseFactory.create()

        payload = {
            "id": purchase.id,
            "provider": "Test provider",
            "price_ht": 15.23,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_update_someone_elses_canteen(self):
        """
        A user should not be able to set someone else's canteen in a purchase update
        """
        purchase = PurchaseFactory.create()
        purchase.canteen.managers.add(authenticate.user)
        new_canteen = CanteenFactory.create()

        payload = {
            "id": purchase.id,
            "canteen": new_canteen.id,
        }

        response = self.client.patch(
            reverse("purchase_retrieve_update", kwargs={"pk": purchase.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
