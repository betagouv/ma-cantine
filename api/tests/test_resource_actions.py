from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory, UserFactory, WasteActionFactory
from data.models import ResourceAction


class TestReviews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.waste_action = WasteActionFactory()
        cls.user = UserFactory()
        cls.user_canteen = UserFactory()
        cls.canteen = CanteenFactory()
        cls.canteen.managers.add(cls.user_canteen)
        cls.url = reverse("resource_action_create", kwargs={"resource_pk": cls.waste_action.id})

    def test_create_resource_action(self):
        # user is not authenticated
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # user does not belong to the canteen
        self.client.force_login(user=self.user)
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # user is authenticated and belongs to the canteen, but canteen_id missing
        self.client.force_login(user=self.user_canteen)
        response = self.client.post(self.url, data={"is_done": True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # user is authenticated and belongs to the canteen, but canteen_id is wrong
        response = self.client.post(self.url, data={"canteen_id": 999, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # user is authenticated and belongs to the canteen
        self.client.force_login(user=self.user_canteen)
        response = self.client.post(self.url, data={"canteen_id": self.canteen.id, "is_done": True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ResourceAction.objects.count(), 1)
        self.assertEqual(ResourceAction.objects.first().resource, self.waste_action)
        self.assertEqual(ResourceAction.objects.first().canteen, self.canteen)
        self.assertEqual(ResourceAction.objects.first().is_done, True)
