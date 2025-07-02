from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CanteenFactory,
    ResourceActionFactory,
    UserFactory,
    WasteActionFactory,
)
from data.models import ResourceAction


class TestResourceActionsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_with_canteen = UserFactory()
        cls.canteen = CanteenFactory(managers=[cls.user_with_canteen])
        cls.url = reverse("resource_action_create_or_update", kwargs={"resource_pk": cls.waste_action.id})

    def test_create_resource_action_error(self):
        # user is not authenticated
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # user does not belong to the canteen
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # user is authenticated and belongs to the canteen, but canteen_id missing
        self.client.force_login(user=self.user_with_canteen)
        response = self.client.post(self.url, data={"is_done": True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # user is authenticated and belongs to the canteen, but canteen_id is wrong
        response = self.client.post(self.url, data={"canteen_id": 999, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_resource_action_success(self):
        # user is authenticated and belongs to the canteen
        self.client.force_login(user=self.user_with_canteen)
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
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

    def test_update_resource_action(self):
        # create a ResourceAction
        ResourceActionFactory(resource=self.waste_action, canteen=self.canteen, is_done=True)
        # user is authenticated and belongs to the canteen
        self.client.force_login(user=self.user_with_canteen)
        # update is_done
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertFalse(ResourceAction.objects.first().is_done)
        self.assertIsNone(ResourceAction.objects.first().is_favorite)
        # update is_favorite
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_favorite": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertFalse(ResourceAction.objects.first().is_done)
        self.assertTrue(ResourceAction.objects.first().is_favorite)


class TestCanteenResourceActionApi(APITestCase):
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

    def test_get_single_user_canteen_with_resource_actions(self):
        self.client.force_login(user=self.user_with_canteen)
        # canteen with resource_actions
        response = self.client.get(reverse("single_canteen", kwargs={"pk": self.canteen_with_resource_action.id}))
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

    def test_get_single_published_canteen_with_resource_actions(self):
        # canteen without resource_actions
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": self.canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.canteen.id)
        self.assertTrue("resourceActions" in body)
        self.assertEqual(len(body["resourceActions"]), 0)
        # canteen with resource_actions
        response = self.client.get(
            reverse("single_published_canteen", kwargs={"pk": self.canteen_with_resource_action.id})
        )
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
