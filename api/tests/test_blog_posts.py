from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import BlogPostFactory, BlogTagFactory


class BlogPostListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("blog_posts_list")

    def test_can_list_blog_posts_if_published(self):
        published_blog_posts = [
            BlogPostFactory(published=True),
            BlogPostFactory(published=True),
        ]
        draft_blog_posts = [
            BlogPostFactory(published=False),
            BlogPostFactory(published=False),
            BlogPostFactory(published=False),
        ]
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body.get("count"), 2)
        results = body["results"]

        for published_blog_post in published_blog_posts:
            self.assertTrue(any(x["id"] == published_blog_post.id for x in results))

        for draft_blog_post in draft_blog_posts:
            self.assertFalse(any(x["id"] == draft_blog_post.id for x in results))

    def test_can_filter_blog_posts_by_tag(self):
        tag = BlogTagFactory(name="Test")
        other = BlogTagFactory()
        good_post = BlogPostFactory(published=True)
        good_post.tags.add(tag)
        good_post.tags.add(other)
        post = BlogPostFactory(published=True)
        post.tags.add(other)

        response = self.client.get(self.url, {"tag": "Test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["id"], good_post.id)

    def test_get_blog_tags_in_use(self):
        """
        The API should also return names of tags that are used by published blog posts
        """
        used_tag = BlogTagFactory(name="Used")
        draft_tag = BlogTagFactory(name="Draft")
        BlogTagFactory(name="Unused")

        published_blog_post = BlogPostFactory(published=True)
        published_blog_post.tags.add(used_tag)
        draft_blog_post = BlogPostFactory(published=False)
        draft_blog_post.tags.add(draft_tag)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        tags = body.get("tags", [])
        self.assertIn("Used", tags)
        self.assertNotIn("Unused", tags)
        self.assertNotIn("Draft", tags)


class BlogPostDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog_post = BlogPostFactory(published=False)
        cls.url = reverse("single_blog_post", kwargs={"pk": cls.blog_post.id})

    def test_cannot_get_blog_post_if_not_published(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_get_blog_post_if_published(self):
        tag = BlogTagFactory(name="Test tag")
        self.blog_post.published = True
        self.blog_post.save()
        self.blog_post.tags.add(tag)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("Test tag", body["tags"])
