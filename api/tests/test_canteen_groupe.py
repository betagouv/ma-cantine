from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from freezegun import freeze_time

from api.tests.utils import authenticate, get_oauth2_token
from common.tests.utils import date_in_campaign, date_in_campaign_correction
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen


class CanteenGroupeSatellitesListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe_1 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_2 = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_0 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_satellite_11 = CanteenFactory(
            name="Last",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=cls.canteen_groupe_1,
        )
        cls.canteen_satellite_12 = CanteenFactory(
            name="First",
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

    @authenticate
    def test_cannot_list_if_group_does_not_exist(self):
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": 9999},
        )
        self.client.force_authenticate(user=authenticate.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_list_if_not_group_manager(self):
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        self.client.force_authenticate(user=None)  # Authenticate as a normal user
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_canteen_groupe_satellites_list_for_groupe_with_satellites(self):
        # set user as manager of canteen_groupe_1
        self.canteen_groupe_1.managers.add(authenticate.user)
        # canteen_groupe_1 has 2 satellites
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_1.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], self.canteen_satellite_12.id)  # ordered by name
        self.assertFalse(body[0]["isManagedByUser"])  # user not manager of satellite canteens
        self.assertIn("action", body[0])

        # set user as manager of canteen_satellite_12
        self.canteen_satellite_12.managers.add(authenticate.user)
        # call again
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]["id"], self.canteen_satellite_12.id)  # ordered by name
        self.assertTrue(body[0]["isManagedByUser"])  # user is now manager of satellite canteen
        self.assertIn("action", body[0])

    @authenticate
    def test_canteen_groupe_satellites_list_for_groupe_without_satellites(self):
        # set user as manager of canteen_groupe_2
        self.canteen_groupe_2.managers.add(authenticate.user)
        # canteen_groupe_2 has 0 satellites
        url = reverse(
            "canteen_groupe_satellites_list",
            kwargs={"canteen_pk": self.canteen_groupe_2.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 0)

    def test_canteen_groupe_satellites_list_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen_groupe_1.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

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

    @authenticate
    def test_cannot_link_unlink_satellite_if_group_does_not_exist(self):
        # self.canteen_satellite_0 is not linked yet
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": 9999, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # self.canteen_satellite_11 is linked to groupe_1
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": 9999, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
    def test_satellite_manager_can_unlink_satellite(self):
        # set user as manager of satellite_11 only (not of groupe_1)
        self.canteen_satellite_11.managers.add(authenticate.user)
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen_satellite_11.refresh_from_db()
        self.assertIsNone(self.canteen_satellite_11.groupe_id)

    @authenticate
    def test_satellite_manager_cannot_link_satellite(self):
        # set user as manager of satellite_0 only (not of groupe_1)
        self.canteen_satellite_0.managers.add(authenticate.user)
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.canteen_satellite_0.refresh_from_db()
        self.assertIsNone(self.canteen_satellite_0.groupe_id)

    @authenticate
    def test_satellite_manager_cannot_unlink_another_satellite(self):
        # set user as manager of satellite_12 only
        self.canteen_satellite_12.managers.add(authenticate.user)
        # try to unlink satellite_11 (not managed by the user)
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.canteen_satellite_11.refresh_from_db()
        self.assertEqual(self.canteen_satellite_11.groupe_id, self.canteen_groupe_1.id)

    @authenticate
    def test_cannot_link_non_satellite_or_site(self):
        # set user as manager of group_1
        self.canteen_groupe_1.managers.add(authenticate.user)
        # try to link a groupe canteen
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_groupe_2.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_can_link_site(self):
        # set user as manager of group_1
        self.canteen_groupe_1.managers.add(authenticate.user)
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_site.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen_site.refresh_from_db()
        self.assertEqual(self.canteen_site.groupe_id, self.canteen_groupe_1.id)

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
    @freeze_time(date_in_campaign(2024))
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
    @freeze_time(date_in_campaign(2024))
    def test_satellite_manager_cannot_unlink_during_teledeclaration_if_groupe_has_diagnostic_teledeclared(self):
        # set user as manager of satellite_11 only (not of groupe_1)
        self.canteen_satellite_11.managers.add(authenticate.user)
        # create a diagnostic teledeclared for groupe_1 for year 2024 (by a groupe manager)
        groupe_manager = UserFactory()
        self.canteen_groupe_1.managers.add(groupe_manager)
        DiagnosticFactory(canteen=self.canteen_groupe_1, year=2024, valeur_totale=100).teledeclare(
            applicant=groupe_manager
        )

        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["error"],
            "Vous ne pouvez pas quitter le groupe car sa télédéclaration a été validée et les données de votre cantine ont été prises en compte. Vous pouvez demander à votre groupe d'annuler sa télédéclaration, ou alors vous pourrez renouveler votre demande à la fin de la campagne à partir du 30/04/2025",
        )
        self.canteen_satellite_11.refresh_from_db()
        self.assertEqual(self.canteen_satellite_11.groupe_id, self.canteen_groupe_1.id)

    @authenticate
    def test_can_link_satellite_when_groupe_has_cancelled_diagnostic(self):
        self.canteen_groupe_1.managers.add(authenticate.user)
        with freeze_time(date_in_campaign(2024)):
            diagnostic = DiagnosticFactory(canteen=self.canteen_groupe_1, year=2024, valeur_totale=100)
            diagnostic.teledeclare(applicant=authenticate.user)

        with freeze_time(date_in_campaign_correction(2024)):
            diagnostic.cancel()
            url = reverse(
                "canteen_groupe_satellite_link",
                kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
            )
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.canteen_satellite_11.groupe, self.canteen_groupe_1)

    @authenticate
    def test_can_unlink_satellite_when_groupe_has_cancelled_diagnostic(self):
        self.canteen_groupe_1.managers.add(authenticate.user)
        with freeze_time(date_in_campaign(2024)):
            self.canteen_satellite_11.groupe = self.canteen_groupe_1
            self.canteen_satellite_11.save()
            diagnostic = DiagnosticFactory(canteen=self.canteen_groupe_1, year=2024, valeur_totale=100)
            diagnostic.teledeclare(applicant=authenticate.user)

        with freeze_time(date_in_campaign_correction(2024)):
            diagnostic.cancel()
            url = reverse(
                "canteen_groupe_satellite_unlink",
                kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
            )
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.canteen_satellite_11.refresh_from_db()
            self.assertIsNone(self.canteen_satellite_11.groupe)

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

    @authenticate
    def test_canteen_groupe_satellite_link_unlink_syncs_the_groupe_diagnostic(self):
        self.canteen_groupe_1.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_groupe_1, year=2026)
        self.assertEqual(
            [item["id"] for item in diagnostic.satellites_nombre_repas_an_list],
            [self.canteen_satellite_11.id, self.canteen_satellite_12.id],
        )

        # link
        url = reverse(
            "canteen_groupe_satellite_link",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_0.id},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertIn(
            {"id": self.canteen_satellite_0.id, "nombre_repas_an": self.canteen_satellite_0.yearly_meal_count},
            diagnostic.satellites_nombre_repas_an_list,
        )
        history = diagnostic.history.first()
        self.assertEqual(history.history_user, authenticate.user)
        self.assertEqual(
            history.history_change_reason, f"Groupe satellites sync (canteen {self.canteen_satellite_0.id})"
        )

        # unlink
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertNotIn(
            self.canteen_satellite_11.id, [item["id"] for item in diagnostic.satellites_nombre_repas_an_list]
        )

    @authenticate
    def test_satellite_manager_unlink_syncs_the_groupe_diagnostic(self):
        self.canteen_satellite_11.yearly_meal_count = 1000
        self.canteen_satellite_11.save(skip_validations=True)
        self.canteen_satellite_12.yearly_meal_count = 500
        self.canteen_satellite_12.save(skip_validations=True)
        diagnostic = DiagnosticFactory(canteen=self.canteen_groupe_1, year=2026)
        self.assertEqual(
            diagnostic.satellites_nombre_repas_an_list,
            [
                {"id": self.canteen_satellite_11.id, "nombre_repas_an": 1000},
                {"id": self.canteen_satellite_12.id, "nombre_repas_an": 500},
            ],
        )
        self.assertEqual(diagnostic.satellites_nombre_repas_an_sum, 1500)

        # set user as manager of satellite_11 only (not of groupe_1), then unlink
        self.canteen_satellite_11.managers.add(authenticate.user)
        url = reverse(
            "canteen_groupe_satellite_unlink",
            kwargs={"canteen_pk": self.canteen_groupe_1.id, "satellite_pk": self.canteen_satellite_11.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(
            diagnostic.satellites_nombre_repas_an_list,
            [{"id": self.canteen_satellite_12.id, "nombre_repas_an": 500}],
        )
        self.assertEqual(diagnostic.satellites_nombre_repas_an_sum, 500)

    def test_canteen_groupe_satellite_link_unlink_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen_groupe_1.managers.add(user)
        self.canteen_groupe_2.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

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
