from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from web.views import SITEMAP_CACHE_KEY


class SitemapTest(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()

    def test_sitemap_status(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sitemap_is_cached(self):
        self.assertIsNone(cache.get(SITEMAP_CACHE_KEY))
        response = self.client.get(reverse("sitemap"))
        self.assertIsNotNone(cache.get(SITEMAP_CACHE_KEY))
        self.assertIn("Cache-Control", response)
