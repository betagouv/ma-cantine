from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CommunityEventFactory


class TestBlogApi(APITestCase):
    def test_community_event_format(self):
        today = timezone.now()
        CommunityEventFactory.create(end_date=today)

        response = self.client.get(reverse("community_event_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        community_event = body[0]
        self.assertIn("title", community_event)
        self.assertIn("tagline", community_event)
        self.assertIn("startDate", community_event)
        self.assertIn("endDate", community_event)
        self.assertIn("link", community_event)

    def test_get_upcoming_community_events(self):
        """
        The API should only return upcoming community events
        """
        today = timezone.now()
        # past community event
        CommunityEventFactory.create(end_date=(today - timedelta(days=1)))
        upcoming_community_events = [
            CommunityEventFactory.create(
                start_date=(today + timedelta(days=9)), end_date=(today + timedelta(days=10))
            ),
            CommunityEventFactory.create(start_date=today, end_date=(today + timedelta(hours=1))),
            CommunityEventFactory.create(
                start_date=(today + timedelta(days=8)), end_date=(today + timedelta(days=20))
            ),
        ]

        response = self.client.get(reverse("community_event_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
        # community_events should be returned in ascending start date order
        self.assertEquals(body[0]["id"], upcoming_community_events[1].id)
        self.assertEquals(body[1]["id"], upcoming_community_events[2].id)
        self.assertEquals(body[2]["id"], upcoming_community_events[0].id)
