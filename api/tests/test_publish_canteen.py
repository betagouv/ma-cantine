from data.models.canteen import Canteen
from data.factories.canteen import CanteenFactory, SectorFactory
from django.urls import reverse
from django.test.utils import override_settings
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import authenticate
from unittest.mock import patch


@patch("common.utils.create_trello_card")
@override_settings(TRELLO_LIST_ID_PUBLICATION="listId")
class TestPublishCanteen(APITestCase):
    @authenticate
    def test_modify_canteen_unauthorized(self, _):
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
    def test_publish_canteen(self, _):
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

    @override_settings(PROTOCOL="https")
    @override_settings(HOSTNAME="ma-cantine.fr")
    @authenticate
    def test_publish_email(self, mock_create_trello_card):
        """
        An trello card should be created when a manager has requested publication
        """
        scolaire = SectorFactory.create(name="Scolaire")
        entreprise = SectorFactory.create(name="Entreprise")
        canteen = CanteenFactory.create(sectors=[scolaire, entreprise])
        canteen.managers.add(authenticate.user)
        response = self.client.post(reverse("publish_canteen", kwargs={"pk": canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_create_trello_card.assert_called_with(
            "listId",
            canteen.name,
            f"[admin](https://ma-cantine.fr/admin/data/canteen/{canteen.id}/change/)\n\nSecteurs\n\n* Entreprise\n* Scolaire",
        )

    @override_settings(PROTOCOL="https")
    @override_settings(HOSTNAME="ma-cantine.fr")
    @override_settings(ENVIRONMENT="demo")
    @authenticate
    def test_environment_prepend(self, mock_create_trello_card):
        """
        Trello card title should get env prepend if exists
        """
        canteen = CanteenFactory.create()
        canteen.sectors.all().delete()
        canteen.managers.add(authenticate.user)
        response = self.client.post(reverse("publish_canteen", kwargs={"pk": canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_create_trello_card.assert_called_with(
            "listId",
            f"(DEMO) {canteen.name}",
            f"[admin](https://ma-cantine.fr/admin/data/canteen/{canteen.id}/change/)\n\nAucun secteur",
        )

    @override_settings(CONTACT_EMAIL="contact-test@example.com")
    @authenticate
    def test_publish_canteen_twice(self, mock_create_trello_card):
        """
        Calling the publish endpoint twice will only create one trello card but allows user to
        edit comments
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
        mock_create_trello_card.assert_called_once()
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, "pending")
        self.assertEqual(persisted_canteen.publication_comments, "Hello, world!")
        self.assertEqual(response.json()["publicationComments"], "Hello, world!")

    @authenticate
    def test_unpublish_canteen(self, _):
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
