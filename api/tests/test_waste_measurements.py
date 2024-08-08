from django.urls import reverse

# from django.db import transaction
# from django.test.utils import override_settings
# from django.core.exceptions import BadRequest
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory
from data.models import WasteMeasurement
from .utils import authenticate

# import decimal


class TestWasteMeasurementsApi(APITestCase):
    def test_unauthenticated_create_waste_measurement_call(self):
        """
        When calling this API unathenticated we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("waste_measurement_creation", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_waste_measurement_missing_canteen(self):
        """
        When calling this API on an unexistent canteen we expect a 404
        """
        response = self.client.post(reverse("waste_measurement_creation", kwargs={"canteen_pk": 999}), {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_waste_measurement_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("waste_measurement_creation", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_waste_measurement(self):
        """
        When calling this API on a canteen that the user manages
        we expect a waste_measurement to be created
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {}

        response = self.client.post(reverse("waste_measurement_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        waste_measurement = WasteMeasurement.objects.get(canteen__id=canteen.id)

        self.assertIsNotNone(waste_measurement)

    # TODO: edit rules
    # TODO: date rules
    # TODO: fetch rules
