from data.factories.provisionalmanager import ProvisionalManagerFactory
from django.urls import reverse
from django.db import transaction
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, UserFactory
from data.models import ProvisionalManager
from .utils import authenticate


class TestLoggedUserApi(APITestCase):
    def test_unauthenticated_get_provisional_managers(self):
        """
        Expect 403 if attempt to get managers for canteen when not logged in
        """
        response = self.client.get(
            reverse("provisional_managers", kwargs={"canteen_pk": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_provisional_managers(self):
        """
        Return provisional managers for canteen if a manager of the canteen
        """
        pm1 = ProvisionalManagerFactory.create()
        pm1.canteen.managers.add(authenticate.user)
        ProvisionalManagerFactory.create()
        response = self.client.get(
            reverse("provisional_managers", kwargs={"canteen_pk": pm1.canteen_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["email"], pm1.email)

    @authenticate
    def test_unauthorised_get_provisional_managers(self):
        """
        Expect 404 if attempt to get managers for canteen not a manager of the canteen
        """
        pm = ProvisionalManagerFactory.create()
        response = self.client.get(
            reverse("provisional_managers", kwargs={"canteen_pk": pm.canteen_id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        with self.assertRaises(ProvisionalManager.DoesNotExist):
            ProvisionalManager.objects.get(canteen__id=999)

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
        with self.assertRaises(ProvisionalManager.DoesNotExist):
            ProvisionalManager.objects.get(canteen__id=canteen.id)

    @authenticate
    def test_authenticated_create_provisional_manager(self):
        """
        When calling this API authenticated we expect to save the
        an unassociated email in the provisional managers table with the canteen id
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {"email": "test@example.com"}
        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pm = ProvisionalManager.objects.get(canteen__id=canteen.id)
        self.assertEqual(pm.email, "test@example.com")
        self.assertEqual(pm.canteen_id, canteen.id)

    @authenticate
    def test_authenticated_create_duplicate_provisional_manager(self):
        """
        If API called twice with the same data, only save once
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {"email": "test@example.com"}
        self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )
        with transaction.atomic():
            response = self.client.post(
                reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pms = ProvisionalManager.objects.filter(canteen__id=canteen.id)
        self.assertEqual(len(pms), 1)

    @authenticate
    def test_authenticated_create_multiple_provisional_manager(self):
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

        pms = ProvisionalManager.objects.all()
        self.assertEqual(len(pms), 4)

    @authenticate
    def test_authenticated_add_manager_existing_user(self):
        """
        If the email matches an existing user, add the user to the canteen managers
        without going through provisional managers table
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        other_user = UserFactory.create()
        payload = {"email": other_user.email}

        response = self.client.post(
            reverse("add_manager", kwargs={"canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(canteen.managers.all().get(id=other_user.id).id, other_user.id)
        with self.assertRaises(ProvisionalManager.DoesNotExist):
            ProvisionalManager.objects.get(email=other_user.email)

    # TODO: test that new user with email matching is linked on creation (maybe not here?)
