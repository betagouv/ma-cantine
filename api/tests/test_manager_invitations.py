from data.factories.managerinvitation import ManagerInvitationFactory
from django.core import mail
from django.urls import reverse
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, UserFactory
from data.models import ManagerInvitation
from .utils import authenticate


class TestManagerInvitationApi(APITestCase):
    def test_unauthenticated_add_manager_call(self):
        """
        When calling this API unauthenticated we expect a 403
        """
        response = self.client.post(reverse("add_manager"), {"canteenId": 999})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_remove_manager_call(self):
        """
        When calling this API unauthenticated we expect a 403
        """
        response = self.client.post(reverse("remove_manager"), {"canteenId": 999})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_add_manager_missing_canteen(self):
        """
        When calling this API on a nonexistent canteen we expect a 404
        """
        payload = {"canteenId": 999, "email": "test@example.com"}
        response = self.client.post(reverse("add_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen__id=999)

    @authenticate
    def test_remove_manager_missing_canteen(self):
        """
        When calling this API on a nonexistent canteen we expect a 404
        """
        payload = {"canteenId": 999, "email": "test@example.com"}
        response = self.client.post(reverse("remove_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_add_manager_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 404
        """
        canteen = CanteenFactory.create()
        payload = {"canteenId": canteen.id, "email": "test@example.com"}
        response = self.client.post(reverse("add_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen__id=canteen.id)

    @authenticate
    def test_remove_manager_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 404
        """
        canteen = CanteenFactory.create()
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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
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
        canteen1 = CanteenFactory.create()
        canteen2 = CanteenFactory.create()
        canteen1.managers.add(authenticate.user)
        canteen2.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        other_user = UserFactory.create(email="test@example.com")
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
        coworker = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        canteen.managers.add(coworker)

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
        coworker = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        invitation = ManagerInvitationFactory.create(canteen=canteen, email=invitedManagerEmail)

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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        other_user = UserFactory.create(email="TEst@example.com")
        payload = {"canteenId": canteen.id, "email": "test@example.com"}

        response = self.client.post(reverse("add_manager"), payload)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.all().get(id=other_user.id).id, other_user.id)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(email=other_user.email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "TEst@example.com")
        self.assertEqual(mail.outbox[0].from_email, "test-from@example.com")
        self.assertIn("Accèder à la cantine", mail.outbox[0].body)

        self.assertEqual(len(body["managers"]), canteen.managers.all().count())
        self.assertEqual(len(body["managerInvitations"]), canteen.managerinvitation_set.all().count())

    @authenticate
    @override_settings(DEFAULT_FROM_EMAIL="test-from@example.com")
    def test_authenticated_add_manager_multiple_case_insensitive(self):
        """
        If the email does not match an existing user, we try with a case insensitive query. If several
        users have a similar email with different cases, we don't proceed.
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        UserFactory.create(email="TEst@example.com")
        UserFactory.create(email="TEST@example.com")
        UserFactory.create(email="TesT@example.com")

        payload = {"canteenId": canteen.id, "email": "test@example.com"}

        response = self.client.post(reverse("add_manager"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        manager_emails = list(map(lambda x: x.email, canteen.managers.all()))
        self.assertNotIn("TEst@example.com", manager_emails)
        self.assertNotIn("TEST@example.com", manager_emails)
        self.assertNotIn("TesT@example.com", manager_emails)
        self.assertEqual(len(mail.outbox), 1)
