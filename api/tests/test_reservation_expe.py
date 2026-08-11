from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, ReservationExpeFactory
from data.models import ReservationExpe


class ReservationExpeListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.reservation_expe = ReservationExpeFactory(canteen=cls.canteen, leader_email="test@example.com")
        cls.url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_get_reservation_expe_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_reservation_expe_if_canteen_does_not_exist(self):
        url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # TODO: should be 404

    @authenticate
    def test_cannot_get_reservation_expe_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_reservation_expe_if_reservation_expe_does_not_exist(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # TODO: should be 404

    @authenticate
    def test_can_list_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["leaderEmail"], "test@example.com")


class ReservationExpeCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_create_reservation_expe_if_unauthenticated(self):
        payload = {
            "satisfaction": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_reservation_expe_if_canteen_does_not_exist(self):
        payload = {
            "satisfaction": 5,
        }
        url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": 9999})
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_reservation_expe_if_not_canteen_manager(self):
        payload = {
            "satisfaction": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_create_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        payload = {
            "leader_email": "test@example.com",
            "satisfaction": 5,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["leaderEmail"], "test@example.com")
        self.assertEqual(body["satisfaction"], 5)
        self.assertEqual(ReservationExpe.objects.get(canteen=self.canteen).leader_email, "test@example.com")
        self.assertEqual(ReservationExpe.objects.get(canteen=self.canteen).satisfaction, 5)

    @authenticate
    def test_cannot_create_duplicate_reservation_expe(self):
        """
        Shouldn't be able to create more than one reservation expe for a canteen
        """
        self.canteen.managers.add(authenticate.user)
        reservation_expe = ReservationExpeFactory(canteen=self.canteen, satisfaction=5)

        payload = {
            "satisfaction": 0,
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.satisfaction, 5)
        self.assertEqual(ReservationExpe.objects.count(), 1)


class ReservationExpeUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.reservation_expe = ReservationExpeFactory(
            canteen=cls.canteen, leader_email="good@example.com", satisfaction=1, avg_weight_not_served_t2=70
        )
        cls.url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_update_reservation_expe_if_unauthenticated(self):
        payload = {"leader_email": "bad@example.com"}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.leader_email, "good@example.com")

    @authenticate
    def test_cannot_update_reservation_expe_if_canteen_does_not_exist(self):
        url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": 9999})
        payload = {"leader_email": "bad@example.com"}
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_reservation_expe_if_not_canteen_manager(self):
        payload = {"leader_email": "bad@example.com"}
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.leader_email, "good@example.com")

    @authenticate
    def test_cannot_update_reservation_expe_if_reservation_expe_does_not_exist(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id})
        payload = {"leader_email": "bad@example.com"}
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ReservationExpe.objects.filter(canteen=canteen).count(), 0)

    @authenticate
    def test_cannot_update_reservation_expe_with_put(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.put(self.url, data={}, format="json")

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_can_update_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        payload = {"leader_email": "other@example.com", "satisfaction": 3}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.leader_email, "other@example.com")
        self.assertEqual(self.reservation_expe.satisfaction, 3)

    @authenticate
    def test_cannot_update_reservation_expe_canteen(self):
        self.canteen.managers.add(authenticate.user)
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {"canteen": canteen.id}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.canteen, self.canteen)  # no change

    @authenticate
    def test_cannot_update_reservation_expe_with_bad_data(self):
        self.canteen.managers.add(authenticate.user)

        payload = {"satisfaction": 6}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.satisfaction, 1)

        payload = {"avg_weight_not_served_t2": -90}
        response = self.client.patch(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.avg_weight_not_served_t2, 70)


class ReservationExpeDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.reservation_expe = ReservationExpeFactory(canteen=cls.canteen)
        cls.url = reverse("canteen_reservation_expe", kwargs={"canteen_pk": cls.canteen.id})

    @authenticate
    def test_cannot_delete_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
