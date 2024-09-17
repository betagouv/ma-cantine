from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class TestSitemaps(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sitemap_status(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
