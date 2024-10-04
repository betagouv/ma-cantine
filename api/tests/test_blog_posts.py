from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import BlogPostFactory, BlogTagFactory


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

        self.assertEqual(body.get("count"), 2)

        results = body.get("results", [])

        for published_blog_post in published_blog_posts:
            self.assertTrue(any(x["id"] == published_blog_post.id for x in results))

        for draft_blog_post in draft_blog_posts:
            self.assertFalse(any(x["id"] == draft_blog_post.id for x in results))

    def test_get_single_blog_post(self):
        """
        The API should return single blog posts if they are published
        """
        tag = BlogTagFactory.create(name="Test tag")
        published_blog_post = BlogPostFactory.create(published=True)
        published_blog_post.tags.add(tag)
        draft_blog_post = BlogPostFactory.create(published=False)

        response = self.client.get(reverse("single_blog_post", kwargs={"pk": published_blog_post.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test tag", response.json()["tags"])

        response = self.client.get(reverse("single_blog_post", kwargs={"pk": draft_blog_post.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_blog_post(self):
        """
        The API should return filtered blog posts
        """
        tag = BlogTagFactory.create(name="Test")
        other = BlogTagFactory.create()
        good_post = BlogPostFactory.create(published=True)
        good_post.tags.add(tag)
        good_post.tags.add(other)
        post = BlogPostFactory.create(published=True)
        post.tags.add(other)

        response = self.client.get(reverse("blog_posts_list"), {"tag": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], good_post.id)

    def test_get_blog_tags_in_use(self):
        """
        The API should also return names of tags that are used by published blog posts
        """
        used_tag = BlogTagFactory.create(name="Used")
        draft_tag = BlogTagFactory.create(name="Draft")
        BlogTagFactory.create(name="Unused")

        published_blog_post = BlogPostFactory.create(published=True)
        published_blog_post.tags.add(used_tag)
        draft_blog_post = BlogPostFactory.create(published=False)
        draft_blog_post.tags.add(draft_tag)

        response = self.client.get(reverse("blog_posts_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        tags = body.get("tags", [])
        self.assertIn("Used", tags)
        self.assertNotIn("Unused", tags)
        self.assertNotIn("Draft", tags)
