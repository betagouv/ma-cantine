import datetime
import json

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CanteenFactory,
    CommunityEventFactory,
    PartnerTypeFactory,
    SectorFactory,
    VideoTutorialFactory,
)
from data.models import Canteen

from .utils import authenticate


class TestInitialDataApi(APITestCase):
    def test_unauthenticated_initial_data(self):
        """
        The initial data request must contain data that is individually managed
        by other views. If the call isn't authenticated, "loggedUser" should be None
        """
        sector = SectorFactory.create()
        partner_type = PartnerTypeFactory.create()
        community_event = CommunityEventFactory.create(end_date=timezone.now() + datetime.timedelta(days=10))
        video_tutorial = VideoTutorialFactory.create(published=True)

        response = self.client.get(reverse("initial_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertIn("loggedUser", body)
        self.assertIsNone(body["loggedUser"])

        self.assertIn("sectors", body)
        self.assertEqual(len(body["sectors"]), 1)
        self.assertEqual(body["sectors"][0]["name"], sector.name)

        self.assertIn("partnerTypes", body)
        self.assertEqual(len(body["partnerTypes"]), 1)
        self.assertEqual(body["partnerTypes"][0]["name"], partner_type.name)

        self.assertIn("communityEvents", body)
        self.assertEqual(len(body["communityEvents"]), 1)
        self.assertEqual(body["communityEvents"][0]["title"], community_event.title)

        self.assertIn("videoTutorials", body)
        self.assertEqual(len(body["videoTutorials"]), 1)
        self.assertEqual(body["videoTutorials"][0]["title"], video_tutorial.title)

        self.assertIn("canteenPreviews", body)
        self.assertIsNone(body["canteenPreviews"])

        self.assertIn("lineMinistries", body)
        self.assertEqual(len(body["lineMinistries"]), len(Canteen.Ministries))

    @authenticate
    def test_authenticated_logged_initial_data(self):
        """
        Same endpoint, this time with data in the "loggedUser" property. Not needed
        to thoroughly test the other keys, just making sure they are present.
        The cantine previews should also be present in this case.
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("initial_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content.decode())
        self.assertIn("loggedUser", body)
        self.assertEqual(body["loggedUser"]["id"], authenticate.user.id)
        self.assertEqual(body["loggedUser"]["email"], authenticate.user.email)
        self.assertEqual(body["loggedUser"]["username"], authenticate.user.username)
        self.assertEqual(body["loggedUser"]["firstName"], authenticate.user.first_name)

        self.assertIn("canteenPreviews", body)
        self.assertEqual(len(body["canteenPreviews"]), 1)
        self.assertEqual(body["canteenPreviews"][0]["name"], canteen.name)

        self.assertIn("sectors", body)
        self.assertIn("partnerTypes", body)
        self.assertIn("communityEvents", body)
        self.assertIn("videoTutorials", body)
