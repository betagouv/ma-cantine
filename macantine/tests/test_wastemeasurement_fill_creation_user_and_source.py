from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import (
    AccessTokenFactory,
    ApplicationFactory,
    CanteenFactory,
    RefreshTokenFactory,
    UserFactory,
    WasteMeasurementFactory,
)
from data.models import WasteMeasurement
from data.models.creation_source import CreationSource


class WastemeasurementFillCreationUserAndSourceTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("canteen_waste_measurements_list", kwargs={"canteen_pk": cls.canteen.id})
        cls.WM_PAYLOAD = {"period_start_date": "2024-08-01", "period_end_date": "2024-08-10"}

    def test_fill_for_waste_measurement_created_from_api(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")
        response = self.client.post(self.url, self.WM_PAYLOAD)
        wm_id = response.json()["id"]

        self.assertEqual(WasteMeasurement.objects.count(), 1)
        WasteMeasurement.objects.filter(id=wm_id).update(
            creation_user=None, creation_source=None, creation_source_api_oauth2_application=None
        )
        wm = WasteMeasurement.objects.get(id=wm_id)
        self.assertIsNone(wm.creation_user)
        self.assertIsNone(wm.creation_source)
        self.assertIsNone(wm.creation_source_api_oauth2_application)

        # run management command
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_user", apply=True)
        call_command("wastemeasurement_fill_creation_user_and_source", field="creation_source", apply=True)
        call_command(
            "wastemeasurement_fill_creation_user_and_source",
            field="creation_source_api_oauth2_application",
            apply=True,
        )

        wm.refresh_from_db()
        self.assertEqual(wm.creation_user, user)
        self.assertEqual(wm.creation_source, CreationSource.API)
        self.assertEqual(wm.creation_source_api_oauth2_application, token.application)

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


class WastemeasurementFillCreationSourceApiOauth2ApplicationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application_1 = ApplicationFactory()
        cls.application_2 = ApplicationFactory()

    def setUp(self):
        self.user = UserFactory()
        self.wm = WasteMeasurementFactory(creation_user=self.user, creation_source=CreationSource.API)
        self.creation_date = self.wm.creation_date

    def run_command(self, apply=True):
        call_command(
            "wastemeasurement_fill_creation_user_and_source",
            field="creation_source_api_oauth2_application",
            apply=apply,
        )
        self.wm.refresh_from_db()

    def test_fill_from_token_valid_at_creation_date(self):
        # application_1: token valid at creation date, application_2: token valid later
        RefreshTokenFactory(
            user=self.user,
            application=self.application_1,
            created=self.creation_date - timedelta(days=1),
            revoked=self.creation_date + timedelta(hours=1),
        )
        AccessTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            expires=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.wm.creation_source_api_oauth2_application, self.application_1)

    def test_fill_from_only_application_used(self):
        # no token valid at creation date, but the user only ever used application_2
        RefreshTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            revoked=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.wm.creation_source_api_oauth2_application, self.application_2)

    def test_not_filled_if_ambiguous(self):
        for application in [self.application_1, self.application_2]:
            RefreshTokenFactory(
                user=self.user, application=application, created=self.creation_date - timedelta(days=1)
            )

        self.run_command()

        self.assertIsNone(self.wm.creation_source_api_oauth2_application)

    def test_dry_run_does_not_change_anything(self):
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command(apply=False)

        self.assertIsNone(self.wm.creation_source_api_oauth2_application)
