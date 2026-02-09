from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CommunityEventFactory


class TestCommunityEventApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.community_event_past = CommunityEventFactory(
            start_date=timezone.now() - timedelta(days=2), end_date=timezone.now() - timedelta(days=1)
        )
        cls.community_event_ongoing = CommunityEventFactory(
            start_date=timezone.now(), end_date=timezone.now() + timedelta(days=1)
        )
        cls.community_event_upcoming_1 = CommunityEventFactory(
            start_date=(timezone.now() + timedelta(days=9)), end_date=(timezone.now() + timedelta(days=10))
        )
        cls.community_event_upcoming_2 = CommunityEventFactory(
            start_date=(timezone.now() + timedelta(days=8)), end_date=(timezone.now() + timedelta(days=20))
        )
        cls.url = reverse("community_event_list")

    def test_get_community_events(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        # should only return upcoming community events
        self.assertEqual(len(body), 1 + 2)

        # should return community events in ascending start date order
        self.assertLessEqual(body[0]["id"], self.community_event_ongoing.id)
        self.assertLessEqual(body[1]["id"], self.community_event_upcoming_2.id)
        self.assertLessEqual(body[2]["id"], self.community_event_upcoming_1.id)

        community_event = body[0]
        for key in ["id", "title", "startDate", "endDate", "tagline", "link"]:
            with self.subTest(key=key):
                self.assertIn(key, community_event)
