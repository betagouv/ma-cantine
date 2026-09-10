from django.test import Client, TestCase, override_settings
from django.urls import reverse
from rest_framework import status


class RobotsTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(ENVIRONMENT="prod")
    def test_robots_prod_allows_indexing(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Allow: /", response.content)

    @override_settings(ENVIRONMENT="staging")
    def test_robots_non_prod_disallows_indexing(self):
        response = self.client.get(reverse("robots_txt"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Disallow: /", response.content)
