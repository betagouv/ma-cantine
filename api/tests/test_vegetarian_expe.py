from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from data.factories import CanteenFactory, VegetarianExpeFactory
from data.models import VegetarianExpe


class TestVegetarianExpeApi(APITestCase):
    @authenticate
    def test_create_vegetarian_expe(self):
        """
        Test that we can create a new vegetarian experiment for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "vegetarianMenuPercentageT0": 0.32,
            "satisfactionGuestsT0": 5,
        }

        response = self.client.post(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        self.assertEqual(body["vegetarianMenuPercentageT0"], 0.32)
        self.assertEqual(body["satisfactionGuestsT0"], 5)

        self.assertEqual(float(VegetarianExpe.objects.get(canteen=canteen).vegetarian_menu_percentage_t0), 0.32)
        self.assertEqual(VegetarianExpe.objects.get(canteen=canteen).satisfaction_guests_t0, 5)

    def test_cannot_create_vegetarian_expe_not_authenticated(self):
        """
        Shouldn't be able to create a vegetarian expe if not authenticated
        """
        canteen = CanteenFactory.create()

        payload = {
            "satisfactionGuestsT0": 5,
        }

        response = self.client.post(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_vegetarian_expe_not_manager(self):
        """
        Shouldn't be able to create a vegetarian expe if not the manager of the canteen
        """
        canteen = CanteenFactory.create()

        payload = {
            "satisfactionGuestsT0": 5,
        }

        response = self.client.post(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_vegetarian_expe_nonexistent_canteen(self):
        """
        Shouldn't be able to create a vegetarian expe if not the canteen doesn't exist
        """
        payload = {
            "satisfactionGuestsT0": 5,
        }

        response = self.client.post(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": 99}), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_create_duplicate_vegetarian_expe(self):
        """
        Shouldn't be able to create more than one vegetarian expe for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        vegetarian_expe = VegetarianExpeFactory.create(canteen=canteen, satisfaction_guests_t0=5)

        response = self.client.post(
            reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), {"satisfactionGuestsT0": 0}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.satisfaction_guests_t0, 5)
        self.assertEqual(VegetarianExpe.objects.count(), 1)

    @authenticate
    def test_get_vegetarian_expe(self):
        """
        Test that we can get a vegetarian expe for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        VegetarianExpeFactory.create(canteen=canteen, satisfaction_guests_t0=4)

        response = self.client.get(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["satisfactionGuestsT0"], 4)

    def test_cannot_get_vegetarian_expe_unauthenticated(self):
        """
        Shouldn't be able to get a vegetarian expe if not authenticated
        """
        canteen = CanteenFactory.create()
        VegetarianExpeFactory.create(canteen=canteen)

        response = self.client.get(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_vegetarian_expe_not_manager(self):
        """
        Shouldn't be able to get a vegetarian expe if not manager of canteen
        """
        canteen = CanteenFactory.create()
        VegetarianExpeFactory.create(canteen=canteen)

        response = self.client.get(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_nonexistant_vegetarian_expe(self):
        """
        Test attempting to get a vegetarian expe that doesn't exist
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @authenticate
    def test_update_vegetarian_expe(self):
        """
        Test that we can update a vegetarian experiment for a canteen
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        vegetarian_expe = VegetarianExpeFactory.create(canteen=canteen, satisfaction_guests_t0=1)
        payload = {"satisfactionGuestsT0": 3}
        response = self.client.patch(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.satisfaction_guests_t0, 3)

    def test_cannot_update_vegetarian_expe_unauthenticated(self):
        """
        Shouldn't be able to update a vegetarian expe if not authenticated
        """
        canteen = CanteenFactory.create()
        vegetarian_expe = VegetarianExpeFactory.create(canteen=canteen, satisfaction_guests_t0=1)
        payload = {"satisfactionGuestsT0": 2}
        response = self.client.patch(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.satisfaction_guests_t0, 1)

    @authenticate
    def test_cannot_update_vegetarian_expe_not_manager(self):
        """
        Shouldn't be able to update a vegetarian expe if not manager of the canteen
        """
        canteen = CanteenFactory.create()
        vegetarian_expe = VegetarianExpeFactory.create(canteen=canteen, satisfaction_guests_t0=1)
        payload = {"satisfactionGuestsT0": 2}
        response = self.client.patch(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.satisfaction_guests_t0, 1)

    @authenticate
    def test_cannot_update_nonexistent_vegetarian_expe(self):
        """
        Shouldn't be able to update a vegetarian expe if it doesn't exist
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {"satisfactionGuestsT0": 2}
        response = self.client.patch(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(VegetarianExpe.objects.count(), 0)

    @authenticate
    def test_cannot_update_canteen_for_vegetarian_expe(self):
        """
        Check that cannot update canteen on a reservation expe
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        vegetarian_expe = VegetarianExpeFactory.create(canteen=canteen)
        payload = {"canteen": CanteenFactory.create().id}
        response = self.client.patch(reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.canteen, canteen)

    @authenticate
    def test_updates_bad_data(self):
        """
        Check that updates with bad data are rejected
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        vegetarian_expe = VegetarianExpeFactory.create(
            canteen=canteen, satisfaction_guests_t0=3, waste_vegetarian_not_served_t0=70
        )

        response = self.client.patch(
            reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}),
            {"satisfactionGuestsT0": 6},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.satisfaction_guests_t0, 3)

        response = self.client.patch(
            reverse("canteen_vegetarian_expe", kwargs={"canteen_pk": canteen.id}),
            {"wasteVegetarianNotServedT0": -90},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        vegetarian_expe.refresh_from_db()
        self.assertEqual(vegetarian_expe.waste_vegetarian_not_served_t0, 70)
