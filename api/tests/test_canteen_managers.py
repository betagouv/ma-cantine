from django.core import mail
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, UserFactory, ManagerInvitationFactory
from data.models import ManagerInvitation


class CanteenManagersListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory(managers=[])
        cls.url = reverse("canteen_managers_list", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_get_canteen_managers_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_canteen_managers_if_canteen_does_not_exist(self):
        url = reverse("canteen_managers_list", kwargs={"canteen_pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_canteen_managers_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_canteen_managers_list(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertNotIn("id", body[0])
        self.assertEqual(body[0]["email"], authenticate.user.email)
        self.assertEqual(body[0]["firstName"], authenticate.user.first_name)
        self.assertEqual(body[0]["lastName"], authenticate.user.last_name)

    def test_canteen_managers_list_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token}")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertNotIn("id", body[0])
        self.assertEqual(body[0]["email"], user.email)
        self.assertEqual(body[0]["firstName"], user.first_name)
        self.assertEqual(body[0]["lastName"], user.last_name)


class CanteenManagersInvitationsListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory(managers=[])
        cls.url = reverse("canteen_managers_invitations_list", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_get_canteen_managers_invitations_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_canteen_managers_invitations_if_canteen_does_not_exist(self):
        url = reverse("canteen_managers_invitations_list", kwargs={"canteen_pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_canteen_managers_invitations_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_canteen_managers_invitations_list(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        # empty
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 0)

        # add an invitation
        ManagerInvitationFactory(canteen=self.canteen, email="new.USER@example.com")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["email"], "new.USER@example.com")

    def test_canteen_managers_invitations_list_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)
        ManagerInvitationFactory(canteen=self.canteen, email="new.USER@example.com")
        self.client.credentials(Authorization=f"Bearer {token}")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["email"], "new.USER@example.com")


class CanteenClaimApiTest(APITestCase):
    @authenticate
    def test_can_claim_canteen(self):
        canteen = CanteenFactory()
        canteen.managers.clear()

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        user = authenticate.user
        self.assertEqual(canteen.managers.first().id, user.id)
        self.assertEqual(canteen.managers.count(), 1)
        canteen.refresh_from_db()
        self.assertEqual(canteen.claimed_by, user)
        self.assertTrue(canteen.has_been_claimed)

    @authenticate
    def test_can_claim_canteen_not_valid(self):
        canteen = CanteenFactory()
        canteen.managers.clear()
        canteen.siret = None
        canteen.save(skip_validations=True)
        self.assertIsNone(canteen.siret)
        self.assertFalse(canteen.is_filled)

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        user = authenticate.user
        self.assertEqual(canteen.managers.first().id, user.id)
        self.assertEqual(canteen.managers.count(), 1)
        canteen.refresh_from_db()
        self.assertEqual(canteen.claimed_by, user)
        self.assertTrue(canteen.has_been_claimed)

    @authenticate
    def test_cannot_claim_canteen_already_claimed(self):
        canteen = CanteenFactory()
        self.assertGreater(canteen.managers.count(), 0)
        user = authenticate.user
        self.assertFalse(canteen.managers.filter(id=user.id).exists())

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(canteen.managers.filter(id=user.id).exists())
        canteen.refresh_from_db()
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_can_undo_claim_canteen(self):
        canteen = CanteenFactory(claimed_by=authenticate.user, has_been_claimed=True, managers=[authenticate.user])

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertIsNone(canteen.claimed_by)
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_can_undo_claim_for_canteen_not_valid(self):
        canteen = CanteenFactory(claimed_by=authenticate.user, has_been_claimed=True, managers=[authenticate.user])
        canteen.siret = None
        canteen.save(skip_validations=True)

        self.assertIsNone(canteen.siret)
        self.assertFalse(canteen.is_filled)

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertIsNone(canteen.claimed_by)
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_cannot_undo_claim_canteen_if_not_original_claimer(self):
        other_user = UserFactory()
        canteen = CanteenFactory(claimed_by=other_user, has_been_claimed=True, managers=[authenticate.user])

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertTrue(canteen.has_been_claimed)
        self.assertEqual(canteen.claimed_by, other_user)


class CanteenManagerInvitationApiTest(APITestCase):
    def test_cannot_add_manager_if_unauthenticated(self):
        response = self.client.post(reverse("add_manager"), {"canteenId": 999})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_remove_manager_if_unauthenticated(self):
        response = self.client.post(reverse("remove_manager"), {"canteenId": 999})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_add_manager_if_canteen_does_not_exist(self):
        payload = {"canteenId": 9999, "email": "test@example.com"}
        response = self.client.post(reverse("add_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen__id=9999)

    @authenticate
    def test_cannot_remove_manager_if_canteen_does_not_exist(self):
        payload = {"canteenId": 9999, "email": "test@example.com"}
        response = self.client.post(reverse("remove_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_add_manager_if_not_canteen_manager(self):
        canteen = CanteenFactory()
        payload = {"canteenId": canteen.id, "email": "test@example.com"}
        response = self.client.post(reverse("add_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen__id=canteen.id)

    @authenticate
    def test_cannot_remove_manager_if_not_canteen_manager(self):
        canteen = CanteenFactory()
        payload = {"canteenId": canteen.id, "email": "test@example.com"}
        response = self.client.post(reverse("remove_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="test-from@example.com")
    def test_authenticated_create_manager_invitation(self):
        """
        When calling this API authenticated we expect to save the
        an unassociated email in the invitations table with the canteen id
        and email an invitation to sign up to the invited manager
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        payload = {"canteenId": canteen.id, "email": "  test@example.com"}
        response = self.client.post(reverse("add_manager"), payload)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pm = ManagerInvitation.objects.get(canteen__id=canteen.id)
        self.assertEqual(pm.email, "test@example.com")
        self.assertEqual(pm.canteen_id, canteen.id)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "test@example.com")
        self.assertEqual(mail.outbox[0].from_email, "test-from@example.com")

        self.assertEqual(body["managers"][0]["email"], authenticate.user.email)
        self.assertEqual(body["managerInvitations"][0]["email"], "test@example.com")

    @authenticate
    def test_authenticated_create_duplicate_manager_invitation(self):
        """
        If API called twice with the same data, only save once,
        and only send one email
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        payload = {"canteenId": canteen.id, "email": "test@example.com"}
        self.client.post(reverse("add_manager"), payload)
        response = self.client.post(reverse("add_manager"), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("managers" in response.json())

        pms = ManagerInvitation.objects.filter(canteen__id=canteen.id)
        self.assertEqual(len(pms), 1)
        self.assertEqual(len(mail.outbox), 1)

    @authenticate
    def test_authenticated_create_multiple_manager_invitation(self):
        """
        One email can be associated to more than one canteen,
        one canteen can be associated to more than one email
        """
        canteen1 = CanteenFactory(managers=[authenticate.user])
        canteen2 = CanteenFactory(managers=[authenticate.user])

        self.client.post(
            reverse("add_manager"),
            {"canteenId": canteen1.id, "email": "test1@example.com"},
        )
        self.client.post(
            reverse("add_manager"),
            {"canteenId": canteen1.id, "email": "test2@example.com"},
        )
        self.client.post(
            reverse("add_manager"),
            {"canteenId": canteen2.id, "email": "test1@example.com"},
        )
        self.client.post(
            reverse("add_manager"),
            {"canteenId": canteen2.id, "email": "test2@example.com"},
        )

        pms = ManagerInvitation.objects.all()
        self.assertEqual(len(pms), 4)

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="test-from@example.com")
    def test_authenticated_add_manager_existing_user(self):
        """
        If the email matches an existing user, add the user to the canteen managers
        without going through invitations table. No email sent for now
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        other_user = UserFactory(email="test@example.com")
        payload = {"canteenId": canteen.id, "email": other_user.email}

        response = self.client.post(reverse("add_manager"), payload)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.all().get(id=other_user.id).id, other_user.id)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(email=other_user.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "test@example.com")
        self.assertEqual(mail.outbox[0].from_email, "test-from@example.com")
        self.assertIn("Accèder à la cantine", mail.outbox[0].body)

        self.assertEqual(len(body["managers"]), canteen.managers.all().count())
        self.assertEqual(len(body["managerInvitations"]), canteen.managerinvitation_set.all().count())

    @authenticate
    def test_authenticated_remove_manager(self):
        """
        It should be possible to remove a given manager from a canteen
        """
        coworker = UserFactory()
        canteen = CanteenFactory(managers=[authenticate.user, coworker])

        payload = {"canteenId": canteen.id, "email": coworker.email}
        response = self.client.post(reverse("remove_manager"), payload)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.filter(id=coworker.id).count(), 0)
        self.assertEqual(canteen.managers.filter(id=authenticate.user.id).count(), 1)
        self.assertEqual(len(body["managers"]), canteen.managers.all().count())

    @authenticate
    def test_authenticated_remove_nonexistent_manager(self):
        """
        When trying to remove a manager that does not manage a canteen, we will
        respond 200 OK.
        """
        coworker = UserFactory()
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {"canteenId": canteen.id, "email": coworker.email}
        response = self.client.post(reverse("remove_manager"), payload)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.filter(id=authenticate.user.id).count(), 1)
        self.assertEqual(len(body["managers"]), canteen.managers.all().count())

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="test-from@example.com")
    def test_authenticated_delete_invitation(self):
        """
        We should be able to remove a pending invitation
        """
        invitedManagerEmail = "invited-manager@example.com"
        canteen = CanteenFactory(managers=[authenticate.user])
        invitation = ManagerInvitationFactory(canteen=canteen, email=invitedManagerEmail)

        payload = {"canteenId": canteen.id, "email": invitedManagerEmail}
        self.client.post(reverse("remove_manager"), payload)

        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(pk=invitation.id)

        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen=canteen, email=invitedManagerEmail)

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="test-from@example.com")
    def test_authenticated_add_manager_email_insensitive(self):
        """
        If the email does not match an existing user, we try with a case insensitive query
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        other_user = UserFactory(email="TEst@example.com")

        payload = {"canteenId": canteen.id, "email": "test@example.com"}
        response = self.client.post(reverse("add_manager"), payload)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.all().get(id=other_user.id).id, other_user.id)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(email=other_user.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "test@example.com")
        self.assertEqual(mail.outbox[0].from_email, "test-from@example.com")
        self.assertIn("Accèder à la cantine", mail.outbox[0].body)

        self.assertEqual(len(body["managers"]), canteen.managers.all().count())
        self.assertEqual(len(body["managerInvitations"]), canteen.managerinvitation_set.all().count())

    def test_create_user_with_pending_invitations(self):
        """
        If invitations match a newly created user's email address (case insensitive),
        add that user to the canteen's managers
        """
        canteen = CanteenFactory()
        self.assertFalse(canteen.managers.filter(email="new.user@example.com").exists())

        ManagerInvitationFactory(canteen=canteen, email="new.USER@example.com")
        UserFactory(email="new.user@example.com")

        self.assertTrue(canteen.managers.filter(email="new.user@example.com").exists())


class CanteenTeamRequestEmailTest(APITestCase):
    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(HOSTNAME="mysite.com")
    @override_settings(SECURE="True")
    def test_send_message(self):
        canteen = CanteenFactory(
            siret="76494221950672",
            name="Hugo",
            managers=[
                UserFactory(email="mgmt1@example.com"),
                UserFactory(email="mgmt2@example.com"),
            ],
        )

        payload = {
            "email": "test@example.com",
            "name": "My name",
            "message": "Please add me to the team",
        }
        response = self.client.post(reverse("canteen_team_request", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(len(email.to), 2)
        self.assertIn("mgmt1@example.com", email.to)
        self.assertIn("mgmt2@example.com", email.to)
        self.assertIn("Please add me to the team", email.body)
        self.assertIn("76494221950672", email.body)
        self.assertIn("Hugo", email.body)
        self.assertIn(
            f"https://mysite.com/modifier-ma-cantine/{canteen.id}--\nHugo/gestionnaires?email=test@example.com",
            email.body,
        )
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")
        self.assertEqual(email.from_email, "no-reply@example.com")

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="no-reply@example.com")
    @override_settings(CONTACT_EMAIL="contact@example.com")
    @override_settings(HOSTNAME="mysite.com")
    @override_settings(SECURE="True")
    def test_send_message_no_managers(self):
        canteen = CanteenFactory(siret="76494221950672", name="Hugo")
        canteen.managers.clear()

        payload = {
            "email": "test@example.com",
            "name": "My name",
            "message": "Please add me to the team",
        }
        response = self.client.post(reverse("canteen_team_request", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(len(email.to), 1)
        self.assertIn("contact@example.com", email.to)
        self.assertIn("Please add me to the team", email.body)
        self.assertIn("76494221950672", email.body)
        self.assertIn("Hugo", email.body)
        self.assertIn(
            f"https://mysite.com/modifier-ma-cantine/{canteen.id}--\nHugo/gestionnaires?email=test@example.com",
            email.body,
        )
        self.assertEqual(len(email.reply_to), 1)
        self.assertEqual(email.reply_to[0], "test@example.com")
        self.assertEqual(email.from_email, "no-reply@example.com")
