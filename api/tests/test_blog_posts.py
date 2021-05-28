from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import BlogPostFactory


class TestBlogApi(APITestCase):
    def test_get_published_blog_posts(self):
        """
        The API should only return published blog posts
        """
        published_blog_posts = [
            BlogPostFactory.create(published=True),
            BlogPostFactory.create(published=True),
        ]
        draft_blog_posts = [
            BlogPostFactory.create(published=False),
            BlogPostFactory.create(published=False),
            BlogPostFactory.create(published=False),
        ]
        response = self.client.get(reverse("blog_posts_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 2)

        for published_blog_post in published_blog_posts:
            self.assertTrue(any(x["id"] == published_blog_post.id for x in body))

        for draft_blog_post in draft_blog_posts:
            self.assertFalse(any(x["id"] == draft_blog_post.id for x in body))
