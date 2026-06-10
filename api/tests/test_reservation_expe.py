from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, ReservationExpeFactory
from data.models import ReservationExpe


class ReservationExpeDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.reservation_expe = ReservationExpeFactory(
            canteen=cls.canteen, leader_email="test@example.com", satisfaction=1, avg_weight_not_served_t2=70
        )

    def test_cannot_get_reservation_expe_unauthenticated(self):
        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_reservation_expe_if_canteen_unknown(self):
        self.canteen.managers.add(authenticate.user)
        self.reservation_expe.delete()

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_reservation_expe_if_reservation_expe_unknown(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_cannot_get_reservation_expe_if_not_canteen_manager(self):
        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["leaderEmail"], "test@example.com")


class ReservationExpeCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()

    def test_cannot_create_reservation_expe_if_unauthenticated(self):
        payload = {
            "satisfaction": 5,
        }

        response = self.client.post(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_reservation_expe_if_canteen_unknown(self):
        payload = {
            "satisfaction": 5,
        }

        response = self.client.post(reverse("canteen_reservation_expe", kwargs={"canteen_pk": 9999}), payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_reservation_expe_if_not_canteen_manager(self):
        payload = {
            "satisfaction": 5,
        }

        response = self.client.post(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_duplicate_reservation_expe(self):
        """
        Shouldn't be able to create more than one reservation expe for a canteen
        """
        self.canteen.managers.add(authenticate.user)
        reservation_expe = ReservationExpeFactory(canteen=self.canteen, satisfaction=5)

        response = self.client.post(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), {"satisfaction": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.satisfaction, 5)
        self.assertEqual(ReservationExpe.objects.count(), 1)

    @authenticate
    def test_create_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        payload = {
            "leader_email": "test@example.com",
            "satisfaction": 5,
        }

        response = self.client.post(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["leaderEmail"], "test@example.com")
        self.assertEqual(body["satisfaction"], 5)
        self.assertEqual(ReservationExpe.objects.get(canteen=self.canteen).leader_email, "test@example.com")
        self.assertEqual(ReservationExpe.objects.get(canteen=self.canteen).satisfaction, 5)


class ReservationExpeUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.reservation_expe = ReservationExpeFactory(
            canteen=cls.canteen, leader_email="test@example.com", satisfaction=1, avg_weight_not_served_t2=70
        )

    def test_cannot_update_reservation_expe_if_unauthenticated(self):
        payload = {"leader_email": "bad@example.com"}

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.leader_email, "test@example.com")

    @authenticate
    def test_cannot_update_reservation_expe_if_not_manager(self):
        payload = {"leader_email": "bad@example.com"}

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.leader_email, "test@example.com")

    @authenticate
    def test_cannot_update_reservation_expe_if_reservation_expe_unknown(self):
        self.canteen.managers.add(authenticate.user)
        self.reservation_expe.delete()
        payload = {"leader_email": "bad@example.com"}

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_update_canteen_of_existing_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)
        payload = {"canteen": CanteenFactory().id}

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.canteen, self.canteen)

    @authenticate
    def test_cannot_update_with_bad_data(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}),
            {"satisfaction": 6},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.satisfaction, 3)

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}),
            {"avgWeightNotServedT2": -90},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.avg_weight_not_served_t2, 70)

    @authenticate
    def test_update_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)
        payload = {"leader_email": "good@example.com", "satisfaction": 3}

        response = self.client.patch(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation_expe.refresh_from_db()
        self.assertEqual(self.reservation_expe.leader_email, "good@example.com")
        self.assertEqual(self.reservation_expe.satisfaction, 3)


class ReservationExpeDeleteApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.reservation_expe = ReservationExpeFactory(
            canteen=cls.canteen, leader_email="test@example.com", satisfaction=1, avg_weight_not_served_t2=70
        )

    @authenticate
    def test_cannot_delete_reservation_expe(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.delete(reverse("canteen_reservation_expe", kwargs={"canteen_pk": self.canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
