from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, InvitationFactory, UserFactory
from data.models import Canteen, Invitation


class UserInvitationsListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_other = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_satellite_2 = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_satellite_other = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        # sent by canteen_groupe
        cls.invitation_sent = InvitationFactory(
            creation_canteen=cls.canteen_groupe, invited_canteen=cls.canteen_satellite_2
        )
        cls.invitation_sent_declined = InvitationFactory(
            creation_canteen=cls.canteen_groupe,
            invited_canteen=cls.canteen_satellite_other,
            status=Invitation.Status.DECLINED,
            answer_date=timezone.now(),
        )
        # received by canteen_satellite
        cls.invitation_received = InvitationFactory(
            creation_canteen=cls.canteen_groupe_other, invited_canteen=cls.canteen_satellite
        )
        # not related to the user
        cls.invitation_other = InvitationFactory(
            creation_canteen=cls.canteen_groupe_other, invited_canteen=cls.canteen_satellite_other
        )
        cls.url = reverse("user_invitations")

    def test_cannot_list_if_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_list_empty_if_no_canteen(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    @authenticate
    def test_list_sent(self):
        self.canteen_groupe.managers.add(authenticate.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {invitation["id"] for invitation in response.json()},
            {self.invitation_sent.id, self.invitation_sent_declined.id},
        )

    @authenticate
    def test_list_received(self):
        self.canteen_satellite.managers.add(authenticate.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({invitation["id"] for invitation in response.json()}, {self.invitation_received.id})

    @authenticate
    def test_list_sent_and_received(self):
        self.canteen_groupe.managers.add(authenticate.user)
        self.canteen_satellite.managers.add(authenticate.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(
            {invitation["id"] for invitation in body},
            {self.invitation_sent.id, self.invitation_sent_declined.id, self.invitation_received.id},
        )
        invitation_received = next(
            invitation for invitation in body if invitation["id"] == self.invitation_received.id
        )
        self.assertEqual(invitation_received["category"], Invitation.Category.ADD_SATELLITE)
        self.assertEqual(invitation_received["status"], Invitation.Status.SENT)
        self.assertEqual(invitation_received["creationCanteen"]["id"], self.canteen_groupe_other.id)
        self.assertEqual(invitation_received["invitedCanteen"]["id"], self.canteen_satellite.id)
        self.assertEqual(invitation_received["direction"], Invitation.Direction.RECEIVED)
        invitation_sent = next(invitation for invitation in body if invitation["id"] == self.invitation_sent.id)
        self.assertEqual(invitation_sent["direction"], Invitation.Direction.SENT)
        self.assertIn("creationDate", invitation_received)
        self.assertIsNone(invitation_received["answerDate"])
        self.assertNotIn("creationUser", invitation_received)
        self.assertNotIn("answerUser", invitation_received)

    @authenticate
    def test_list_filters(self):
        self.canteen_groupe.managers.add(authenticate.user)
        self.canteen_satellite.managers.add(authenticate.user)

        for query_params, expected_ids in [
            (
                {"creation_canteen": self.canteen_groupe.id},
                {self.invitation_sent.id, self.invitation_sent_declined.id},
            ),
            ({"invited_canteen": self.canteen_satellite.id}, {self.invitation_received.id}),
            ({"status": Invitation.Status.SENT}, {self.invitation_sent.id, self.invitation_received.id}),
            (
                {"creation_canteen": self.canteen_groupe.id, "status": Invitation.Status.SENT},
                {self.invitation_sent.id},
            ),
            (
                {"direction": Invitation.Direction.SENT},
                {self.invitation_sent.id, self.invitation_sent_declined.id},
            ),
            ({"direction": Invitation.Direction.RECEIVED}, {self.invitation_received.id}),
            (
                {"direction": Invitation.Direction.SENT, "status": Invitation.Status.SENT},
                {self.invitation_sent.id},
            ),
            # filtering on a canteen not managed by the user does not leak its invitations
            ({"creation_canteen": self.canteen_groupe_other.id}, {self.invitation_received.id}),
        ]:
            with self.subTest(query_params=query_params):
                response = self.client.get(self.url, query_params)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual({invitation["id"] for invitation in response.json()}, expected_ids)

    def test_cannot_list_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen_satellite.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserInvitationCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_groupe_other = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        cls.url = reverse("user_invitations")
        cls.payload = {
            "category": Invitation.Category.ADD_SATELLITE,
            "creationCanteen": cls.canteen_groupe.id,
            "invitedCanteen": cls.canteen_satellite.id,
        }

    def test_cannot_create_if_unauthenticated(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen_groupe.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_if_not_creation_canteen_manager(self):
        # even if manager of the invited canteen
        self.canteen_satellite.managers.add(authenticate.user)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Invitation.objects.count(), 0)

    @authenticate
    def test_create(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["category"], Invitation.Category.ADD_SATELLITE)
        self.assertEqual(body["status"], Invitation.Status.SENT)
        self.assertEqual(body["creationCanteen"]["id"], self.canteen_groupe.id)
        self.assertEqual(body["invitedCanteen"]["id"], self.canteen_satellite.id)
        self.assertEqual(body["direction"], Invitation.Direction.SENT)
        invitation = Invitation.objects.get(id=body["id"])
        self.assertEqual(invitation.creation_user, authenticate.user)
        self.assertIsNone(invitation.answer_user)
        self.assertIsNone(invitation.answer_date)

    @authenticate
    def test_create_ignores_read_only_fields(self):
        self.canteen_groupe.managers.add(authenticate.user)
        other_user = UserFactory()
        payload = {**self.payload, "status": Invitation.Status.ACCEPTED, "creationUser": other_user.id}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invitation = Invitation.objects.get(id=response.json()["id"])
        self.assertEqual(invitation.status, Invitation.Status.SENT)
        self.assertEqual(invitation.creation_user, authenticate.user)

    @authenticate
    def test_cannot_create_with_missing_or_unknown_fields(self):
        self.canteen_groupe.managers.add(authenticate.user)
        for field_name, value in [("category", "UNKNOWN"), ("creationCanteen", 9999), ("invitedCanteen", 9999)]:
            with self.subTest(field_name=field_name):
                response = self.client.post(self.url, {**self.payload, field_name: value}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field_name, response.json())
        self.assertEqual(Invitation.objects.count(), 0)

    @authenticate
    def test_cannot_create_if_validation_errors(self):
        self.canteen_groupe.managers.add(authenticate.user)
        self.canteen_satellite_in_groupe = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=self.canteen_groupe_other
        )
        for invited_canteen, error in [
            (None, "Le champ ne peut pas être vide."),
            (
                self.canteen_groupe_other,
                "Le champ doit être un restaurant satellite ou un restaurant avec cuisine sur place.",
            ),
            (self.canteen_satellite_in_groupe, "Cette cantine est déjà rattachée à un groupe."),
        ]:
            with self.subTest(invited_canteen=invited_canteen):
                payload = {**self.payload, "invitedCanteen": invited_canteen.id if invited_canteen else None}
                response = self.client.post(self.url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(error, response.json()["invitedCanteen"])
        self.assertEqual(Invitation.objects.count(), 0)

    @authenticate
    def test_cannot_create_if_pending_invitation(self):
        self.canteen_groupe.managers.add(authenticate.user)
        InvitationFactory(creation_canteen=self.canteen_groupe_other, invited_canteen=self.canteen_satellite)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Cette cantine a déjà une invitation en attente d'un autre groupe.", response.json()["invitedCanteen"]
        )

    @authenticate
    def test_cannot_create_from_a_canteen_that_is_not_a_groupe(self):
        self.canteen_site.managers.add(authenticate.user)
        payload = {**self.payload, "creationCanteen": self.canteen_site.id}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Le champ doit être une cantine de type 'Groupe'.", response.json()["creationCanteen"])
