from data.models.canteen import Canteen
from data.factories.canteen import CanteenFactory
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate


class TestPublishCanteen(APITestCase):
    @authenticate
    def test_modify_canteen_unauthorized(self):
        """
        Users can only publish the canteens they manage
        """
        canteen = CanteenFactory.create(publication_comments="test")
        payload = {"publication_comments": "Hello, world?"}
        response = self.client.post(reverse("publish_canteen", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_comments, "test")

    @authenticate
    def test_publish_canteen(self):
        """
        Users can publish the canteens they manage and add additional notes
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        payload = {
            "publication_comments": "Hello, world!",
            "quality_comments": "Quality",
            "waste_comments": "Something about waste",
            "diversification_comments": "Diversification",
            "plastics_comments": "Plastics",
            "information_comments": "Information",
        }
        response = self.client.post(reverse("publish_canteen", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, "published")
        self.assertEqual(persisted_canteen.publication_comments, "Hello, world!")
        self.assertEqual(persisted_canteen.quality_comments, "Quality")
        self.assertEqual(persisted_canteen.waste_comments, "Something about waste")
        self.assertEqual(persisted_canteen.diversification_comments, "Diversification")
        self.assertEqual(persisted_canteen.plastics_comments, "Plastics")
        self.assertEqual(persisted_canteen.information_comments, "Information")
        self.assertEqual(response.json()["publicationComments"], "Hello, world!")

    @authenticate
    def test_unpublish_canteen(self):
        """
        Calling the unpublish endpoint moves canteens from published
        to draft, optionally updating comments
        """
        canteen = CanteenFactory.create(publication_status="published")
        canteen.managers.add(authenticate.user)
        response = self.client.post(
            reverse("unpublish_canteen", kwargs={"pk": canteen.id}),
            {"publication_comments": "Hello, world!"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, "draft")
        self.assertEqual(persisted_canteen.publication_comments, "Hello, world!")

    @authenticate
    def test_publish_many_canteens(self):
        """
        Given a list of canteen ids, publish those canteens and return list of successful publication ids
        """
        canteen_1 = CanteenFactory.create(publication_status=Canteen.PublicationStatus.DRAFT)
        # doesn't matter initial state
        canteen_2 = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED)
        for canteen in [canteen_1, canteen_2]:
            canteen.managers.add(authenticate.user)

        payload = {"ids": [canteen_1.id, canteen_2.id]}
        response = self.client.post(reverse("publish_canteens"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        canteen_ids = body["ids"]
        self.assertEqual(len(canteen_ids), 2)

        self.assertIn(canteen_1.id, canteen_ids)
        self.assertIn(canteen_2.id, canteen_ids)

        canteen_1.refresh_from_db()
        self.assertEqual(canteen_1.publication_status, Canteen.PublicationStatus.PUBLISHED)

        canteen_2.refresh_from_db()
        self.assertEqual(canteen_2.publication_status, Canteen.PublicationStatus.PUBLISHED)

    def test_publish_many_canteens_unauthenticated(self):
        """
        Require user to be authenticated to access endpoint
        """
        response = self.client.post(reverse("publish_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_multi_publish_empty_payload(self):
        """
        Should get 400 if payload does not contain an array of ids
        """
        response = self.client.post(reverse("publish_canteens"), {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_multi_publish_no_ids(self):
        """
        Should get 400 if an empty array of ids is provided to the endpoint
        """
        response = self.client.post(reverse("publish_canteens"), {"ids": []}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_multi_publish_ids_bad_format(self):
        """
        Should get 400 if something other than an array is provided to endpoint
        """
        response = self.client.post(reverse("publish_canteens"), {"ids": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_publish_unmanaged_canteen(self):
        """
        If there are some canteens that aren't managed by the current user, publish what can be published
        and return list of the canteens that are either non-existant or not managed by the user.
        """
        canteen_1 = CanteenFactory.create(publication_status=Canteen.PublicationStatus.DRAFT)
        canteen_1.managers.add(authenticate.user)
        canteen_2 = CanteenFactory.create(publication_status=Canteen.PublicationStatus.DRAFT)

        payload = {"ids": [canteen_1.id, canteen_2.id, 999]}
        response = self.client.post(reverse("publish_canteens"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = response.json()["unknown_ids"]
        self.assertEqual(len(ids), 2)
        self.assertIn(canteen_2.id, ids)
        self.assertIn(999, ids)
        self.assertNotIn(canteen_1.id, ids)
        canteen_1.refresh_from_db()
        self.assertEqual(canteen_1.publication_status, Canteen.PublicationStatus.PUBLISHED)
        canteen_2.refresh_from_db()
        self.assertEqual(canteen_2.publication_status, Canteen.PublicationStatus.DRAFT)
