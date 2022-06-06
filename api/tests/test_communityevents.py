from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CommunityEventFactory


class TestBlogApi(APITestCase):
    def test_community_event_format(self):
        today = timezone.now()
        CommunityEventFactory.create(date=today)

        response = self.client.get(reverse("community_event_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        community_event = body[0]
        self.assertIn("title", community_event)
        self.assertIn("description", community_event)
        self.assertIn("date", community_event)
        self.assertIn("link", community_event)

    def test_get_upcoming_community_events(self):
        """
        The API should only return upcoming community events
        """
        today = timezone.now()
        # past community event
        CommunityEventFactory.create(date=(today - timedelta(days=1)))
        upcoming_community_events = [
            CommunityEventFactory.create(date=(today + timedelta(days=10))),
            CommunityEventFactory.create(date=today),
            CommunityEventFactory.create(date=(today + timedelta(days=20))),
        ]

        response = self.client.get(reverse("community_event_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
        # test that community_events are returned in ascending date order
        self.assertEquals(body[0]["id"], upcoming_community_events[1].id)
        self.assertEquals(body[1]["id"], upcoming_community_events[0].id)
        self.assertEquals(body[2]["id"], upcoming_community_events[2].id)
