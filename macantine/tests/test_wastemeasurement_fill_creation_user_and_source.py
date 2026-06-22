from django.core.management import call_command
from rest_framework.test import APITestCase
from django.urls import reverse

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import WasteMeasurementFactory, CanteenFactory
from data.models import WasteMeasurement
from data.models.creation_source import CreationSource


class WastemeasurementFillCreationUserAndSourceTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": cls.canteen.id})
        cls.WM_PAYLOAD = {"period_start_date": "2024-08-01", "period_end_date": "2024-08-10"}

    def test_fill_for_waste_measurement_created_from_api(self):
        user, token = get_oauth2_token("waste_measurements:create")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.post(self.url, self.WM_PAYLOAD)
        wm_id = response.json()["id"]

        self.assertEqual(WasteMeasurement.objects.count(), 1)
        WasteMeasurement.objects.filter(id=wm_id).update(creation_user=None, creation_source=None)
        wm = WasteMeasurement.objects.get(id=wm_id)
        self.assertIsNone(wm.creation_user)
        self.assertIsNone(wm.creation_source)

        # run management command
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_user", apply=True)
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_source", apply=True)

        wm.refresh_from_db()
        self.assertEqual(wm.creation_user, user)
        self.assertEqual(wm.creation_source, CreationSource.API)

    @authenticate
    def test_fill_for_waste_measurement_created_from_app(self):
        self.canteen.managers.add(authenticate.user)
        payload = {**self.WM_PAYLOAD, "creation_source": "APP"}
        response = self.client.post(self.url, payload)
        wm_id = response.json()["id"]

        self.assertEqual(WasteMeasurement.objects.count(), 1)
        WasteMeasurement.objects.filter(id=wm_id).update(creation_user=None, creation_source=None)
        wm = WasteMeasurement.objects.get(id=wm_id)
        self.assertIsNone(wm.creation_user)
        self.assertIsNone(wm.creation_source)

        # run management command
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_user", apply=True)
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_source", apply=True)

        wm.refresh_from_db()
        self.assertEqual(wm.creation_user, authenticate.user)
        self.assertEqual(wm.creation_source, CreationSource.APP)

    def test_fill_for_waste_measurement_created_from_code(self):
        wm = WasteMeasurementFactory(canteen=self.canteen)

        self.assertEqual(WasteMeasurement.objects.count(), 1)
        WasteMeasurement.objects.filter(id=wm.id).update(creation_user=None, creation_source=None)
        wm.refresh_from_db()
        self.assertIsNone(wm.creation_user)
        self.assertIsNone(wm.creation_source)

        # run management command
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_user", apply=True)
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_source", apply=True)

        # check results
        wm.refresh_from_db()
        self.assertIsNone(wm.creation_user)
        self.assertIsNone(wm.creation_source)
