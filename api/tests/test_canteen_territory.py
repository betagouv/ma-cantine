from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory


class CanteenTerritoryApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("territory_canteens")

    @authenticate
    def test_can_get_territory_canteens_if_elected_official(self):
        # Set an elected profile
        user = authenticate.user
        user.is_elected_official = True
        user.departments = ["01", "02"]
        user.save()

        # Create canteens (not manager)
        canteen_01 = CanteenFactory(department="01")
        canteen_02 = CanteenFactory(department="02")
        out_of_place_canteen = CanteenFactory(department="03")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 2)
        ids = list(map(lambda x: x["id"], results))

        self.assertIn(canteen_01.id, ids)
        self.assertIn(canteen_02.id, ids)
        self.assertNotIn(out_of_place_canteen.id, ids)

    @authenticate
    def test_cannot_get_territory_canteens_if_not_elected_official(self):
        # Set a non-elected profile
        user = authenticate.user
        user.is_elected_official = False
        user.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_get_territory_canteens_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
