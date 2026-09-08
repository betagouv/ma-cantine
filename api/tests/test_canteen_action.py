from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory


class CanteenActionListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("list_actionable_canteens", kwargs={"year": 2021})

    def test_cannot_list_canteen_actions_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_list_canteen_actions(self):
        CanteenFactory()
        CanteenFactory(managers=[authenticate.user])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 1)
        self.assertTrue("action" in body["results"][0])


class CanteenActionDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("retrieve_actionable_canteen", kwargs={"pk": cls.canteen.id, "year": 2021})

    def test_cannot_retrieve_actionable_canteen_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_actionable_canteen_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_can_retrieve_actionable_canteen(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertTrue("action" in body)


class UserCanteenActionListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user_canteens_actions", kwargs={"year": 2021})

    def test_cannot_list_user_canteen_actions_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_list_user_canteen_actions(self):
        CanteenFactory()
        CanteenFactory(managers=[authenticate.user])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertTrue("action" in response.data[0])
