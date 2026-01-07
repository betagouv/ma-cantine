from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from api.tests.utils import authenticate
from data.factories import CanteenFactory
from data.models import Canteen


class CanteenGroupeSatellitesListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe_1 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_2 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_0 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_satellite_11 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_1,
        )
        cls.canteen_satellite_12 = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_1,
        )
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def test_canteen_groupe_satellites_list_unauthenticated(self):
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_canteen_groupe_satellites_list_user_not_manager(self):
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        self.client.force_authenticate(user=None)  # Authenticate as a normal user
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_canteen_groupe_satellites_list(self):
        # set user as manager of canteen groups
        self.canteen_groupe_1.managers.add(authenticate.user)
        self.canteen_groupe_2.managers.add(authenticate.user)
        # groupe_1 has 2 satellites
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)

        # groupe_2 has 0 satellites
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_2.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 0)
