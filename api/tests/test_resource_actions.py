from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import (
    CanteenFactory,
    ResourceActionFactory,
    UserFactory,
    WasteActionFactory,
)
from data.models import ResourceAction


class ResourceActionsCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user_with_canteen])
        cls.url = reverse("resource_action_create_or_update", kwargs={"resource_pk": cls.waste_action.id})

    def test_cannot_create_resource_action_if_unauthenticated(self):
        payload = {"canteen_id": self.canteen.id, "is_done": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_resource_action_if_user_not_canteen_manager(self):
        payload = {"canteen_id": self.canteen.id, "is_done": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_resource_action_if_canteen_does_not_exist(self):
        payload = {"canteen_id": 9999, "is_done": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_create_resource_action_if_canteen_id_is_missing(self):
        payload = {"is_done": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_create_resource_action_if_canteen_id_is_wrong(self):
        payload = {"canteen_id": 9999, "is_done": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_can_create_resource_action(self):
        self.canteen.managers.add(authenticate.user)

        payload = {"canteen_id": self.canteen.id, "is_done": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["resourceId"], self.waste_action.id)
        self.assertEqual(body["canteenId"], self.canteen.id)
        self.assertTrue(body["isDone"])
        self.assertIsNone(body["isFavorite"])
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertTrue(ResourceAction.objects.first().is_done)
        self.assertIsNone(ResourceAction.objects.first().is_favorite)


class ResourceActionsUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user_with_canteen])
        cls.url = reverse("resource_action_create_or_update", kwargs={"resource_pk": cls.waste_action.id})

    @authenticate
    def test_update_resource_action(self):
        self.canteen.managers.add(authenticate.user)
        ResourceActionFactory(resource=self.waste_action, canteen=self.canteen, is_done=True)

        # update is_done
        payload = {"canteen_id": self.canteen.id, "is_done": False}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertFalse(ResourceAction.objects.first().is_done)
        self.assertIsNone(ResourceAction.objects.first().is_favorite)

        # update is_favorite
        payload = {"canteen_id": self.canteen.id, "is_favorite": True}
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertFalse(ResourceAction.objects.first().is_done)
        self.assertTrue(ResourceAction.objects.first().is_favorite)


class CanteenResourceActionGetApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action_1 = WasteActionFactory()
        cls.waste_action_2 = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        cls.canteen = CanteenFactory()
        cls.canteen_with_resource_action = CanteenFactory(managers=[cls.user_with_canteen])
        ResourceActionFactory(resource=cls.waste_action_1, canteen=cls.canteen_with_resource_action, is_done=True)
        ResourceActionFactory(resource=cls.waste_action_2, canteen=cls.canteen_with_resource_action, is_favorite=True)

    @authenticate
    def test_get_single_user_canteen_with_resource_actions(self):
        self.canteen_with_resource_action.managers.add(authenticate.user)
        # canteen with resource_actions
        url = reverse("single_canteen", kwargs={"pk": self.canteen_with_resource_action.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen_with_resource_action.id)
        self.assertTrue("resourceActions" in body)
        self.assertEqual(len(body["resourceActions"]), 2)
        self.assertTrue(body["resourceActions"][0]["isDone"])
        self.assertIsNone(body["resourceActions"][0]["isFavorite"])
        self.assertEqual(body["resourceActions"][0]["resource"]["id"], self.waste_action_1.id)
        self.assertEqual(body["resourceActions"][0]["canteen"]["id"], self.canteen_with_resource_action.id)
        self.assertIsNone(body["resourceActions"][1]["isDone"])
        self.assertTrue(body["resourceActions"][1]["isFavorite"])
        self.assertEqual(body["resourceActions"][1]["resource"]["id"], self.waste_action_2.id)
        self.assertEqual(body["resourceActions"][1]["canteen"]["id"], self.canteen_with_resource_action.id)

    @authenticate
    def test_get_single_published_canteen_with_resource_actions(self):
        self.canteen.managers.add(authenticate.user)
        # canteen without resource_actions
        url = reverse("single_published_canteen", kwargs={"pk": self.canteen.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen.id)
        self.assertTrue("resourceActions" in body)
        self.assertEqual(len(body["resourceActions"]), 0)

        # canteen with resource_actions
        self.canteen_with_resource_action.managers.add(authenticate.user)
        url = reverse("single_published_canteen", kwargs={"pk": self.canteen_with_resource_action.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen_with_resource_action.id)
        self.assertTrue("resourceActions" in body)
        self.assertEqual(len(body["resourceActions"]), 2)
        self.assertTrue(body["resourceActions"][0]["isDone"])
        self.assertIsNone(body["resourceActions"][0]["isFavorite"])
        self.assertEqual(body["resourceActions"][0]["resource"]["id"], self.waste_action_1.id)
        self.assertEqual(body["resourceActions"][0]["canteen"]["id"], self.canteen_with_resource_action.id)
        self.assertIsNone(body["resourceActions"][1]["isDone"])
        self.assertTrue(body["resourceActions"][1]["isFavorite"])
        self.assertEqual(body["resourceActions"][1]["resource"]["id"], self.waste_action_2.id)
        self.assertEqual(body["resourceActions"][1]["canteen"]["id"], self.canteen_with_resource_action.id)
