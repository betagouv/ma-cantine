import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, CommunityEventFactory, PartnerTypeFactory, VideoTutorialFactory
from data.models import Canteen


INITIAL_DATA_BODY_KEYS = [
    "loggedUser",
    "sectors",
    "partnerTypes",
    "communityEvents",
    "videoTutorials",
    "canteenPreviews",
    "lineMinistries",
]


class InitialDataApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.partner_type = PartnerTypeFactory()
        cls.community_event = CommunityEventFactory(start_date=timezone.now() - datetime.timedelta(days=10), end_date=timezone.now() + datetime.timedelta(days=10))
        cls.video_tutorial = VideoTutorialFactory(published=True)
        cls.url = reverse("initial_data")

    def test_unauthenticated_initial_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for key in INITIAL_DATA_BODY_KEYS:
            with self.subTest(key=key):
                self.assertIn(key, body)

        # unauthenticated: loggedUser & canteenPreviews should be null
        self.assertIsNone(body["loggedUser"])
        self.assertIsNone(body["canteenPreviews"])

        self.assertEqual(len(body["sectors"]), 26)
        self.assertEqual(body["sectors"][0]["name"], "Restaurants des prisons")

        self.assertEqual(len(body["partnerTypes"]), 1)
        self.assertEqual(body["partnerTypes"][0]["name"], self.partner_type.name)

        self.assertEqual(len(body["communityEvents"]), 1)
        self.assertEqual(body["communityEvents"][0]["title"], self.community_event.title)

        self.assertEqual(len(body["videoTutorials"]), 1)
        self.assertEqual(body["videoTutorials"][0]["title"], self.video_tutorial.title)

        self.assertEqual(len(body["lineMinistries"]), len(Canteen.Ministries))

    @authenticate
    def test_authenticated_initial_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for key in INITIAL_DATA_BODY_KEYS:
            with self.subTest(key=key):
                self.assertIn(key, body)

        self.assertIsNotNone(body["loggedUser"])
        self.assertEqual(body["loggedUser"]["id"], authenticate.user.id)
        self.assertEqual(body["loggedUser"]["email"], authenticate.user.email)
        self.assertEqual(body["loggedUser"]["username"], authenticate.user.username)
        self.assertEqual(body["loggedUser"]["firstName"], authenticate.user.first_name)

        # authenticated but not manager: canteenPreviews should be empty
        self.assertIsNotNone(body["canteenPreviews"])
        self.assertEqual(len(body["canteenPreviews"]), 0)

    @authenticate
    def test_authenticated_and_manager(self):
        self.canteen.managers.set([authenticate.user])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        for key in INITIAL_DATA_BODY_KEYS:
            with self.subTest(key=key):
                self.assertIn(key, body)

        # authenticated and manager: canteenPreviews filled
        self.assertIsNotNone(body["canteenPreviews"])
        self.assertEqual(len(body["canteenPreviews"]), 1)
        self.assertEqual(body["canteenPreviews"][0]["name"], self.canteen.name)
