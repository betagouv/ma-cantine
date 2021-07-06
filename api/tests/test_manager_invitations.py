from data.factories.managerinvitation import ManagerInvitationFactory
from django.core import mail
from django.urls import reverse
from django.db import transaction
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, UserFactory
from data.models import ManagerInvitation
from .utils import authenticate


class TestManagerInvitationApi(APITestCase):
    def test_unauthenticated_manager_call(self):
        """
        When calling this API unauthenticated we expect a 403
        """
        response = self.client.post(reverse("add_manager", kwargs={"canteen_pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_manager_missing_canteen(self):
        """
        When calling this API on a nonexistent canteen we expect a 404
        """
        payload = {"email": "test@example.com"}
        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": 999}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen__id=999)

    @authenticate
    def test_manager_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 404
        """
        canteen = CanteenFactory.create()
        payload = {"email": "test@example.com"}
        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(canteen__id=canteen.id)

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
        payload = {"email": "test@example.com"}
        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )
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
        payload = {"email": "test@example.com"}
        self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )
        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )

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
        payload1 = {"email": "test1@example.com"}
        payload2 = {"email": "test2@example.com"}

        self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen1.id}), payload1
        )
        self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen1.id}), payload2
        )
        self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen2.id}), payload1
        )
        self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen2.id}), payload2
        )

        pms = ManagerInvitation.objects.all()
        self.assertEqual(len(pms), 4)

    @authenticate
    def test_authenticated_add_manager_existing_user(self):
        """
        If the email matches an existing user, add the user to the canteen managers
        without going through invitations table
        no email sent for now (TODO: decide email to send)
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        other_user = UserFactory.create()
        payload = {"email": other_user.email}

        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.all().get(id=other_user.id).id, other_user.id)
        with self.assertRaises(ManagerInvitation.DoesNotExist):
            ManagerInvitation.objects.get(email=other_user.email)
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(len(body["managers"]), canteen.managers.all().count())
        self.assertEqual(len(body["managerInvitations"]), canteen.managerinvitation_set.all().count())

