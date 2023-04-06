from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import VideoTutorialFactory


class TestVideoTutorial(APITestCase):
    def test_get_published_video_tutorials(self):
        published_video_tutorials = [
            VideoTutorialFactory.create(published=True),
            VideoTutorialFactory.create(published=True),
        ]
        draft_video_tutorials = [
            VideoTutorialFactory.create(published=False),
            VideoTutorialFactory.create(published=False),
            VideoTutorialFactory.create(published=False),
        ]
        response = self.client.get(reverse("video_tutorials"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 2)

        for published_video_tutorial in published_video_tutorials:
            self.assertTrue(any(x["id"] == published_video_tutorial.id for x in body))

        for draft_video_tutorial in draft_video_tutorials:
            self.assertFalse(any(x["id"] == draft_video_tutorial.id for x in body))
