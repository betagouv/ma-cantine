from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import BlogTagFactory


class TestBlogTagApi(APITestCase):
    def test_get_sectors(self):
        """
        The API should return all sectors
        """
        tag1 = BlogTagFactory.create(name="Tag 1")
        BlogTagFactory.create(name="Tag 2")
        BlogTagFactory.create(name="Tag 3")
        tag1.name = "Tag 1 updated"
        tag1.save()

        response = self.client.get(reverse("blog_tags_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)
        # test whether the return order is consistent despite updates
        self.assertEqual(body[0]["name"], "Tag 1 updated")
