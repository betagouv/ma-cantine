from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from freezegun import freeze_time

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory
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

    def test_cannot_list_if_unauthenticated(self):
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_list_if_wrong_token(self):
        _, token = get_oauth2_token("user:read")
        self.client.credentials(Authorization=f"Bearer {token}")

        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_list_if_group_does_not_exist(self):
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": 9999},
        )
        self.client.force_authenticate(user=authenticate.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # should be 404

    @authenticate
    def test_cannot_list_if_user_not_group_manager(self):
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

    def test_canteen_groupe_satellites_list_correct_token(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen_groupe_1.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)


class CanteenGroupeSatelliteLinkUnlinkApiTest(APITestCase):
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

    def test_cannot_link_unlink_satellite_if_unauthenticated(self):
        # self.canteen_satellite_0 is not linked yet
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # self.canteen_satellite_11 is linked to groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_link_unlink_satellite_if_wrong_token(self):
        _, token = get_oauth2_token("user:read")
        self.client.credentials(Authorization=f"Bearer {token}")

        # self.canteen_satellite_0 is not linked yet
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # self.canteen_satellite_11 is linked to groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_link_unlink_satellite_if_group_does_not_exist(self):
        # self.canteen_satellite_0 is not linked yet
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": 9999, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # should be 404

        # self.canteen_satellite_11 is linked to groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": 9999, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # should be 404

    @authenticate
    def test_cannot_link_unlink_satellite_if_user_not_group_manager(self):
        # self.canteen_satellite_0 is not linked yet
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # self.canteen_satellite_11 is linked to groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_link_non_satellite(self):
        # set user as manager of group_1
        self.canteen_groupe_1.managers.add(authenticate.user)
        # try to link a non-satellite canteen
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_site.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_link_already_linked_satellite(self):
        # set user as manager of group_2
        self.canteen_groupe_2.managers.add(authenticate.user)
        # try to link a satellite already linked to groupe_1
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_2.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_unlink_satellite_not_in_group(self):
        # set user as manager of group_2
        self.canteen_groupe_2.managers.add(authenticate.user)
        # try to unlink a satellite linked to groupe_1 from groupe_2
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_2.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    @freeze_time("2025-01-20")  # during the 2024 campaign
    def test_cannot_link_unlink_during_teledeclaration_if_groupe_has_diagnostic_teledeclared(self):
        # set user as manager of group_1
        self.canteen_groupe_1.managers.add(authenticate.user)
        # create a diagnostic teledeclared for groupe_1 for year 2024
        DiagnosticFactory(canteen=self.canteen_groupe_1, year=2024, valeur_totale=100).teledeclare(
            applicant=authenticate.user
        )

        # try to link a satellite to groupe_1
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # try to unlink a satellite from groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_canteen_groupe_satellite_link_unlink(self):
        # set user as manager of group_1 and group_2
        self.canteen_groupe_1.managers.add(authenticate.user)
        self.canteen_groupe_2.managers.add(authenticate.user)

        # Link self.canteen_satellite_0 to groupe_1
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen_groupe_1.id)
        self.canteen_satellite_0.refresh_from_db()
        self.assertEqual(self.canteen_satellite_0.groupe_id, self.canteen_groupe_1.id)

        # Unlink self.canteen_satellite_11 from groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen_groupe_1.id)
        self.canteen_satellite_11.refresh_from_db()
        self.assertIsNone(self.canteen_satellite_11.groupe_id)

    def test_canteen_groupe_satellite_link_unlink_correct_token(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen_groupe_1.managers.add(user)
        self.canteen_groupe_2.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        # Link self.canteen_satellite_0 to groupe_1
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen_groupe_1.id)
        self.canteen_satellite_0.refresh_from_db()
        self.assertEqual(self.canteen_satellite_0.groupe_id, self.canteen_groupe_1.id)

        # Unlink self.canteen_satellite_11 from groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen_groupe_1.id)
        self.canteen_satellite_11.refresh_from_db()
        self.assertIsNone(self.canteen_satellite_11.groupe_id)
