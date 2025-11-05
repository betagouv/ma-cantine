from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory


class CanteenTerritoryApiTest(APITestCase):
    @authenticate
    def test_territory_canteens_list(self):
        """
        Elected profiles should get information on canteens in their
        geographical area even if they are not the managers
        """

        # Set an elected profile
        user = authenticate.user
        user.is_elected_official = True
        user.departments = ["01", "02"]
        user.save()

        # Create canteens
        canteen_01 = CanteenFactory.create(department="01")
        canteen_02 = CanteenFactory.create(department="02")
        out_of_place_canteen = CanteenFactory.create(department="03")

        # Make request
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()["results"]

        self.assertEqual(len(body), 2)
        ids = list(map(lambda x: x["id"], body))

        self.assertIn(canteen_01.id, ids)
        self.assertIn(canteen_02.id, ids)
        self.assertNotIn(out_of_place_canteen.id, ids)

    @authenticate
    def test_not_elected_official_territory_canteens_list(self):
        """
        Profiles not enabled as "elected" should not get information on
        canteens via the territory_canteens API endpoint
        """

        # Set an elected profile
        user = authenticate.user
        user.is_elected_official = False
        user.save()

        # Make request
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_territory_canteens_list(self):
        """
        Profiles not authenticated should not be able to use the endpoint
        territory_canteens
        """
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
