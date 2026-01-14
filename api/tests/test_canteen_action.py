from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory


class CanteenActionListApiTest(APITestCase):
    def test_cannot_list_canteen_actions_if_unauthenticated(self):
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_list_canteen_actions(self):
        CanteenFactory()
        CanteenFactory(managers=[authenticate.user])
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertTrue("action" in response.data["results"][0])


class CanteenActionDetailApiTest(APITestCase):
    def test_cannot_retrieve_actionable_canteen_if_unauthenticated(self):
        canteen = CanteenFactory()
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": canteen.id, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_actionable_canteen_if_not_manager(self):
        canteen = CanteenFactory()
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": canteen.id, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_retrieve_actionable_canteen_if_manager(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": canteen.id, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("action" in response.data)


class UserCanteenActionListApiTest(APITestCase):
    def test_cannot_list_user_canteen_actions_if_unauthenticated(self):
        response = self.client.get(reverse("user_canteens_actions", kwargs={"year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_list_user_canteen_actions(self):
        CanteenFactory()
        CanteenFactory(managers=[authenticate.user])
        response = self.client.get(reverse("user_canteens_actions", kwargs={"year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue("action" in response.data[0])
