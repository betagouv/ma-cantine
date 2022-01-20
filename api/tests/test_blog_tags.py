from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import BlogTagFactory


class TestBlogTagApi(APITestCase):
    def test_get_sectors(self):
        """
        The API should return all sectors
        """
        BlogTagFactory.create()
        BlogTagFactory.create()
        BlogTagFactory.create()

        response = self.client.get(reverse("blog_tags_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
        self.assertIn("id", body[0])
        self.assertIn("name", body[0])
