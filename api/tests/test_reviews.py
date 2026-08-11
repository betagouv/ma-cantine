from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, ReviewFactory
from data.models import Review


class ReviewCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("create_review")

    def test_cannot_create_review_if_unauthenticated(self):
        payload = {
            "page": "CanteensHome",
            "rating": 3,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_review(self):
        """
        Test that authenticated user can submit a review and the state of
        having a canteen/diagnostic is saved automatically.
        """
        CanteenFactory(managers=[authenticate.user])

        payload = {
            "page": "CanteensHome",
            "rating": 5,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(user=authenticate.user)
        self.assertEqual(review.hasCanteen, True)
        self.assertEqual(review.hasDiagnostic, False)
        self.assertEqual(review.page, "CanteensHome")

    @authenticate
    def test_create_second_review(self):
        """
        Test that user can create a second review for another page
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        ReviewFactory(user=authenticate.user, page="CanteensHome", rating=3, hasCanteen=True, hasDiagnostic=False)
        DiagnosticFactory(canteen=canteen)

        payload = {
            "page": "DiagnosticsHome",
            "rating": 1,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(user=authenticate.user, page="DiagnosticsHome")
        self.assertEqual(review.hasCanteen, True)
        self.assertEqual(review.hasDiagnostic, True)

    @authenticate
    def test_cannot_create_review_without_rating(self):
        payload = {
            "page": "CanteensHome",
            # "rating": 1,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        payload = {"rating": 5}  # no page
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_create_review_with_too_high_rating(self):
        payload = {
            "page": "CanteensHome",
            "rating": 6,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewInUserFetchApiTest(APITestCase):
    @authenticate
    def test_reviews_in_user_fetch(self):
        """
        Test that user can get the review they've submitted for a page
        """
        ReviewFactory(user=authenticate.user, hasCanteen=True, hasDiagnostic=False)
        ReviewFactory(hasCanteen=False, hasDiagnostic=True)  # should not be fetched

        response = self.client.get(reverse("logged_user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["reviews"]), 1)
        self.assertEqual(body["reviews"][0]["hasCanteen"], True)
        self.assertEqual(body["reviews"][0]["hasDiagnostic"], False)
