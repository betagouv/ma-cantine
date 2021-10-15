from data.models.canteen import Canteen
from data.factories.canteen import CanteenFactory
from django.urls import reverse
from django.test.utils import override_settings
from django.core import mail
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
        self.assertEqual(persisted_canteen.publication_status, "pending")
        self.assertEqual(persisted_canteen.publication_comments, "Hello, world!")
        self.assertEqual(persisted_canteen.quality_comments, "Quality")
        self.assertEqual(persisted_canteen.waste_comments, "Something about waste")
        self.assertEqual(persisted_canteen.diversification_comments, "Diversification")
        self.assertEqual(persisted_canteen.plastics_comments, "Plastics")
        self.assertEqual(persisted_canteen.information_comments, "Information")
        self.assertEqual(response.json()["publicationComments"], "Hello, world!")

    @override_settings(CONTACT_EMAIL="contact-test@example.com")
    @authenticate
    def test_publish_email(self):
        """
        An email should be sent to the team when a manager has requested publication
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        response = self.client.post(reverse("publish_canteen", kwargs={"pk": canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], "contact-test@example.com")
        self.assertIn(
            "La cantine « %s » a demandé d'être publiée" % canteen.name,
            mail.outbox[0].body,
        )

    @override_settings(CONTACT_EMAIL="contact-test@example.com")
    @authenticate
    def test_publish_canteen_twice(self):
        """
        Calling the publish endpoint twice will only send one email but allows
        edits to comments
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        self.client.post(
            reverse("publish_canteen", kwargs={"pk": canteen.id}),
            {
                "publication_comments": "First version",
            },
        )
        response = self.client.post(
            reverse("publish_canteen", kwargs={"pk": canteen.id}),
            {"publication_comments": "Hello, world!"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, "pending")
        self.assertEqual(persisted_canteen.publication_comments, "Hello, world!")
        self.assertEqual(response.json()["publicationComments"], "Hello, world!")

    @authenticate
    def test_unpublish_canteen(self):
        """
        Calling the unpublish endpoint moves canteens from published or pending
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

        canteen = CanteenFactory.create(publication_status="pending")
        canteen.managers.add(authenticate.user)
        response = self.client.post(
            reverse("unpublish_canteen", kwargs={"pk": canteen.id}),
            {"publication_comments": "Hello, world!"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, "draft")
        self.assertEqual(persisted_canteen.publication_comments, "Hello, world!")
        self.assertEqual(response.json()["publicationComments"], "Hello, world!")
