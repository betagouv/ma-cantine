from django.urls import reverse
from django.core import mail
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, ManagerInvitationFactory
from data.models import Canteen
from .utils import authenticate


class TestCanteenApi(APITestCase):
    def test_get_published_canteens(self):
        """
        Only published canteens with public data should be
        returned from this call
        """
        published_canteens = [
            CanteenFactory.create(data_is_public=True),
            CanteenFactory.create(data_is_public=True),
        ]
        private_canteens = [
            CanteenFactory.create(data_is_public=False),
        ]
        response = self.client.get(reverse("published_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("count"), 2)

        results = body.get("results", [])

        for published_canteen in published_canteens:
            self.assertTrue(any(x["id"] == published_canteen.id for x in results))

        for private_canteen in private_canteens:
            self.assertFalse(any(x["id"] == private_canteen.id for x in results))

        for recieved_canteen in results:
            self.assertFalse("managers" in recieved_canteen)
            self.assertFalse("managerInvitations" in recieved_canteen)

    def test_get_single_published_canteen(self):
        """
        We are able to get a single published canteen.
        """
        published_canteen = CanteenFactory.create(data_is_public=True)
        response = self.client.get(
            reverse("single_published_canteen", kwargs={"pk": published_canteen.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("id"), published_canteen.id)

    def test_get_single_unpublished_canteen(self):
        """
        A 404 is raised if we try to get a sinlge published canteen
        that has not been published by the manager.
        """
        private_canteen = CanteenFactory.create(data_is_public=False)
        response = self.client.get(
            reverse("single_published_canteen", kwargs={"pk": private_canteen.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_canteens_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the full representation of the canteens
        """
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_user_canteens(self):
        """
        Users can have access to the full representation of their
        canteens (even if they are not published).
        """
        user_canteens = [
            ManagerInvitationFactory.create().canteen,
            ManagerInvitationFactory.create().canteen,
        ]
        other_canteens = [
            CanteenFactory.create(),
            CanteenFactory.create(),
        ]
        user = authenticate.user
        for canteen in user_canteens:
            canteen.managers.add(user)

        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for user_canteen in user_canteens:
            self.assertTrue(any(x["id"] == user_canteen.id for x in body))

        for recieved_canteen in body:
            self.assertEqual(recieved_canteen["managers"][0]["email"], user.email)
            self.assertTrue("email" in recieved_canteen["managerInvitations"][0])

        for other_canteen in other_canteens:
            self.assertFalse(any(x["id"] == other_canteen.id for x in body))

    @authenticate
    def test_modify_canteen_unauthorized(self):
        """
        Users can only modify the canteens they manage
        """
        canteen = CanteenFactory.create(city="Paris")
        payload = {"city": "Lyon"}
        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_modify_canteen(self):
        """
        Users can modify the canteens they manage
        """
        canteen = CanteenFactory.create(city="Paris")
        canteen.managers.add(authenticate.user)
        payload = {"city": "Lyon", "siret": "TESTING123", "management_type": "direct"}
        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(created_canteen.city, "Lyon")
        self.assertEqual(created_canteen.siret, "TESTING123")
        self.assertEqual(created_canteen.management_type, "direct")

    @override_settings(CONTACT_EMAIL="contact-test@example.com")
    @authenticate
    def test_publish_email(self):
        """
        An email should be sent to the team when a cantine is published
        """
        canteen = CanteenFactory.create(data_is_public=False)
        canteen.managers.add(authenticate.user)
        payload = {"data_is_public": True}
        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "contact-test@example.com")
        self.assertIn(
            "La cantine « %s » vient d'être publiée" % canteen.name, mail.outbox[0].body
        )

    @authenticate
    def test_soft_delete(self):
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        response = self.client.delete(
            reverse("single_canteen", kwargs={"pk": canteen.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Model was only soft-deleted but remains in the DB
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
