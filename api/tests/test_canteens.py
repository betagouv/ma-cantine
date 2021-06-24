from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory
from data.models import Canteen
from .utils import authenticate


class TestCanteenApi(APITestCase):
    def test_get_published_canteens(self):
        """
        Only published canteens with public data should be
        returned from this call
        """
        published_canteens = [
            CanteenFactory.create(data_is_public=True),
            CanteenFactory.create(data_is_public=True),
        ]
        private_canteens = [
            CanteenFactory.create(data_is_public=False),
        ]
        response = self.client.get(reverse("published_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body), 2)

        for published_canteen in published_canteens:
            self.assertTrue(any(x["id"] == published_canteen.id for x in body))

        for private_canteen in private_canteens:
            self.assertFalse(any(x["id"] == private_canteen.id for x in body))

    def test_get_canteens_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the full representation of the canteens
        """
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_user_canteens(self):
        """
        Users can have access to the full representation of their
        canteens (even if they are not published).
        """
        user_canteens = [
            CanteenFactory.create(),
            CanteenFactory.create(),
        ]
        other_canteens = [
            CanteenFactory.create(),
            CanteenFactory.create(),
        ]
        for canteen in user_canteens:
            canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for user_canteen in user_canteens:
            self.assertTrue(any(x["id"] == user_canteen.id for x in body))

        for other_canteen in other_canteens:
            self.assertFalse(any(x["id"] == other_canteen.id for x in body))

    @authenticate
    def test_modify_canteen_unauthorized(self):
        """
        Users can only modify the canteens they manage
        """
        canteen = CanteenFactory.create(city="Paris")
        payload = {"city": "Lyon"}
        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_modify_canteen(self):
        """
        Users can modify the canteens they manage
        """
        canteen = CanteenFactory.create(city="Paris")
        canteen.managers.add(authenticate.user)
        payload = {"city": "Lyon", "siret": "TESTING123", "management_type": "direct"}
        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(created_canteen.city, "Lyon")
        self.assertEqual(created_canteen.siret, "TESTING123")
        self.assertEqual(created_canteen.management_type, "direct")

    @authenticate
    def test_soft_delete(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        response = self.client.delete(reverse("single_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Model was only soft-deleted but remains in the DB
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
