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
        cls.canteen = CanteenFactory()
        cls.canteen.managers.add(cls.user_with_canteen)
        cls.url = reverse("resource_action_create_or_update", kwargs={"resource_pk": cls.waste_action.id})

    def test_create_resource_action(self):
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
        # user is authenticated and belongs to the canteen
        self.client.force_login(user=self.user_with_canteen)
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertEqual(body["resourceId"], self.waste_action.id)
        self.assertEqual(body["canteenId"], self.canteen.id)
        self.assertTrue(body["isDone"])
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertTrue(ResourceAction.objects.first().is_done)

    def test_update_resource_action(self):
        # create an existing ResourceAction
        ResourceActionFactory(resource=self.waste_action, canteen=self.canteen, is_done=True)
        # user is authenticated and belongs to the canteen
        self.client.force_login(user=self.user_with_canteen)
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertFalse(ResourceAction.objects.first().is_done)
