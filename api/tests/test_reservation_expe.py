from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.factories import CanteenFactory, ReservationExpeFactory
from data.models import ReservationExpe


class TestReservationExpeApi(APITestCase):
    @authenticate
    def test_create_reservation_expe(self):
        """
        Test that we can create a new reservation experiment for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "leader_email": "test@example.com",
            "satisfaction": 5,
        }

        response = self.client.post(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        self.assertEqual(body["leaderEmail"], "test@example.com")
        self.assertEqual(body["satisfaction"], 5)

        self.assertEqual(ReservationExpe.objects.get(canteen=canteen).leader_email, "test@example.com")
        self.assertEqual(ReservationExpe.objects.get(canteen=canteen).satisfaction, 5)

    def test_cannot_create_reservation_expe_not_authenticated(self):
        """
        Shouldn't be able to create a reservation expe if not authenticated
        """
        canteen = CanteenFactory.create()

        payload = {
            "satisfaction": 5,
        }

        response = self.client.post(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_reservation_expe_not_manager(self):
        """
        Shouldn't be able to create a reservation expe if not the manager of the canteen
        """
        canteen = CanteenFactory.create()

        payload = {
            "satisfaction": 5,
        }

        response = self.client.post(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_reservation_expe_nonexistent_canteen(self):
        """
        Shouldn't be able to create a reservation expe if not the canteen doesn't exist
        """
        payload = {
            "satisfaction": 5,
        }

        response = self.client.post(reverse("canteen_reservation_expe", kwargs={"canteen_pk": 99}), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_duplicate_reservation_expe(self):
        """
        Shouldn't be able to create more than one reservation expe for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        reservation_expe = ReservationExpeFactory.create(canteen=canteen, satisfaction=5)

        response = self.client.post(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), {"satisfaction": 0}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.satisfaction, 5)
        self.assertEqual(ReservationExpe.objects.count(), 1)

    @authenticate
    def test_get_reservation_expe(self):
        """
        Test that we can get a reservation experiment for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        ReservationExpeFactory.create(canteen=canteen, leader_email="test@example.com")

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["leaderEmail"], "test@example.com")

    def test_cannot_get_reservation_expe_unauthenticated(self):
        """
        Shouldn't be able to get a reservation expe if not authenticated
        """
        canteen = CanteenFactory.create()
        ReservationExpeFactory.create(canteen=canteen)

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_reservation_expe_not_manager(self):
        """
        Shouldn't be able to get a reservation expe if not manager of canteen
        """
        canteen = CanteenFactory.create()
        ReservationExpeFactory.create(canteen=canteen)

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_nonexistant_reservation_expe(self):
        """
        Test attempting to get a reservation expe that doesn't exist
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_update_reservation_expe(self):
        """
        Test that we can update a reservation experiment for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        reservation_expe = ReservationExpeFactory.create(
            canteen=canteen, leader_email="bad@example.com", satisfaction=1
        )
        payload = {"leader_email": "good@example.com", "satisfaction": 3}
        response = self.client.put(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.leader_email, "good@example.com")
        self.assertEqual(reservation_expe.satisfaction, 3)

    def test_cannot_update_reservation_expe_unauthenticated(self):
        """
        Shouldn't be able to update a reservation expe if not authenticated
        """
        canteen = CanteenFactory.create()
        reservation_expe = ReservationExpeFactory.create(canteen=canteen, leader_email="good@example.com")
        payload = {"leader_email": "bad@example.com"}
        response = self.client.put(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.leader_email, "good@example.com")

    @authenticate
    def test_cannot_update_reservation_expe_not_manager(self):
        """
        Shouldn't be able to update a reservation expe if not manager of the canteen
        """
        canteen = CanteenFactory.create()
        reservation_expe = ReservationExpeFactory.create(canteen=canteen, leader_email="good@example.com")
        payload = {"leader_email": "bad@example.com"}
        response = self.client.put(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.leader_email, "good@example.com")

    @authenticate
    def test_cannot_update_nonexistent_reservation_expe(self):
        """
        Shouldn't be able to update a reservation expe if it doesn't exist
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {"leader_email": "bad@example.com"}
        response = self.client.put(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ReservationExpe.objects.count(), 0)

    @authenticate
    def test_cannot_update_canteen_for_reservation_expe(self):
        """
        Check that cannot update canteen on a reservation expe
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        reservation_expe = ReservationExpeFactory.create(canteen=canteen)
        payload = {"canteen": CanteenFactory.create().id}
        response = self.client.put(reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.canteen, canteen)

    @authenticate
    def test_updates_bad_data(self):
        """
        Check that updates with bad data are rejected
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        reservation_expe = ReservationExpeFactory.create(canteen=canteen, satisfaction=3, avg_weight_not_served_t2=70)

        response = self.client.put(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}),
            {"satisfaction": 6},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.satisfaction, 3)

        response = self.client.put(
            reverse("canteen_reservation_expe", kwargs={"canteen_pk": canteen.id}),
            {"avgWeightNotServedT2": -90},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        reservation_expe.refresh_from_db()
        self.assertEqual(reservation_expe.avg_weight_not_served_t2, 70)
