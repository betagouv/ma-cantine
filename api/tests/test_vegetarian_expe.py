from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, VegetarianExpeFactory
from data.models import VegetarianExpe


class VegetarianExpeListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.vegetarian_expe = VegetarianExpeFactory(canteen=cls.canteen, satisfaction_guests_t0=5)
        cls.url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_get_vegetarian_expe_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_vegetarian_expe_if_canteen_does_not_exist(self):
        url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # TODO: should be 404

    @authenticate
    def test_cannot_get_vegetarian_expe_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_vegetarian_expe_if_vegetarian_expe_does_not_exist(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # TODO: should be 404

    @authenticate
    def test_can_get_vegetarian_expe(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["satisfactionGuestsT0"], 5)


class VegetarianExpeCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_create_vegetarian_expe_if_unauthenticated(self):
        payload = {
            "satisfaction_guests_t0": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_vegetarian_expe_if_canteen_does_not_exist(self):
        payload = {
            "satisfaction_guests_t0": 5,
        }
        response = self.client.post(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": 9999}), payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_vegetarian_expe_if_not_canteen_manager(self):
        payload = {
            "satisfaction_guests_t0": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_create_vegetarian_expe(self):
        self.canteen.managers.add(authenticate.user)

        payload = {
            "vegetarian_menu_percentage_t0": 0.32,
            "satisfaction_guests_t0": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["vegetarianMenuPercentageT0"], 0.32)
        self.assertEqual(body["satisfactionGuestsT0"], 5)

        self.assertEqual(float(VegetarianExpe.objects.get(canteen=self.canteen).vegetarian_menu_percentage_t0), 0.32)
        self.assertEqual(VegetarianExpe.objects.get(canteen=self.canteen).satisfaction_guests_t0, 5)

    @authenticate
    def test_cannot_create_vegetarian_expe_if_already_exists(self):
        self.canteen.managers.add(authenticate.user)
        vegetarian_expe = VegetarianExpeFactory(canteen=self.canteen, satisfaction_guests_t0=5)

        payload = {
            "satisfaction_guests_t0": 0,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.satisfaction_guests_t0, 5)
        self.assertEqual(VegetarianExpe.objects.count(), 1)


class VegetarianExpeUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.vegetarian_expe = VegetarianExpeFactory(
            canteen=cls.canteen, satisfaction_guests_t0=1, waste_vegetarian_not_served_t0=50
        )
        cls.url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_update_vegetarian_expe_if_unauthenticated(self):
        payload = {"satisfaction_guests_t0": 2}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.vegetarian_expe.refresh_from_db()
        self.assertEqual(self.vegetarian_expe.satisfaction_guests_t0, 1)

    @authenticate
    def test_cannot_update_vegetarian_expe_if_canteen_does_not_exist(self):
        url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": 9999})
        payload = {"satisfaction_guests_t0": 2}
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_vegetarian_expe_if_not_canteen_manager(self):
        payload = {"satisfaction_guests_t0": 2}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.vegetarian_expe.refresh_from_db()
        self.assertEqual(self.vegetarian_expe.satisfaction_guests_t0, 1)

    @authenticate
    def test_cannot_update_vegetarian_expe_if_vegetarian_expe_does_not_exist(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id})
        payload = {"satisfaction_guests_t0": 2}
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(VegetarianExpe.objects.filter(canteen=canteen).count(), 0)

    @authenticate
    def test_cannot_update_vegetarian_expe_with_put(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.put(self.url, data={}, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_can_update_vegetarian_expe(self):
        self.canteen.managers.add(authenticate.user)

        payload = {"satisfaction_guests_t0": 3}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vegetarian_expe.refresh_from_db()
        self.assertEqual(self.vegetarian_expe.satisfaction_guests_t0, 3)

    @authenticate
    def test_cannot_update_vegetarian_expe_canteen(self):
        self.canteen.managers.add(authenticate.user)
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {"canteen": canteen.id}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vegetarian_expe.refresh_from_db()
        self.assertEqual(self.vegetarian_expe.canteen, self.canteen)  # no change

    @authenticate
    def test_cannot_update_vegetarian_expe_with_bad_data(self):
        self.canteen.managers.add(authenticate.user)

        payload = {"satisfaction_guests_t0": 6}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.vegetarian_expe.refresh_from_db()
        self.assertEqual(self.vegetarian_expe.satisfaction_guests_t0, 1)  # no change

        payload = {"waste_vegetarian_not_served_t0": -90}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.vegetarian_expe.refresh_from_db()
        self.assertEqual(self.vegetarian_expe.waste_vegetarian_not_served_t0, 50)  # no change


class VegetarianExpeDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.vegetarian_expe = VegetarianExpeFactory(canteen=cls.canteen)
        cls.url = reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": cls.canteen.id})

    @authenticate
    def test_cannot_delete_vegetarian_expe(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
