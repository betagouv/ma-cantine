from django.urls import reverse
from rest_framework.test import APITestCase
from data.factories import CanteenFactory, ReviewFactory, DiagnosticFactory
from data.models import Review
from rest_framework import status
from .utils import authenticate


class TestReviews(APITestCase):
    @authenticate
    def test_create_review(self):
        """
        Test that authenticated user can submit a review and the state of
        having a canteen/diagnostic is saved automatically.
        """
        CanteenFactory.create(managers=[authenticate.user])
        payload = {
            "page": "CanteensHome",
            "rating": 5,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(reverse("create_review"), payload)
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
        canteen = CanteenFactory.create(managers=[authenticate.user])
        ReviewFactory.create(
            user=authenticate.user, page="CanteensHome", rating=3, hasCanteen=True, hasDiagnostic=False
        )
        DiagnosticFactory.create(canteen=canteen)

        payload = {
            "page": "DiagnosticsHome",
            "rating": 1,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(reverse("create_review"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(user=authenticate.user, page="DiagnosticsHome")
        self.assertEqual(review.hasCanteen, True)
        self.assertEqual(review.hasDiagnostic, True)

    def test_fail_create_review_unauthenticated(self):
        """
        Test that unauthenticated user cannot submit a review
        """
        payload = {
            "page": "CanteensHome",
            "rating": 3,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(reverse("create_review"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_fail_no_rating(self):
        """
        Test that user cannot submit a review without the required fields
        """
        payload = {
            "page": "CanteensHome",
            "suggestion": "Make it read my mind",
        }  # no rating
        response = self.client.post(reverse("create_review"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        payload = {"rating": 5}  # no page
        response = self.client.post(reverse("create_review"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_fail_too_high_rating(self):
        """
        Test that user cannot submit a review without the required fields
        """
        payload = {
            "page": "CanteensHome",
            "rating": 6,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(reverse("create_review"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_reviews_in_user_fetch(self):
        """
        Test that user can get the review they've submitted for a page
        """
        ReviewFactory.create(user=authenticate.user, hasCanteen=True, hasDiagnostic=False)
        ReviewFactory.create(hasCanteen=False, hasDiagnostic=True)  # should not be fetched
        response = self.client.get(reverse("logged_user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["reviews"]), 1)
        self.assertEqual(body["reviews"][0]["hasCanteen"], True)
        self.assertEqual(body["reviews"][0]["hasDiagnostic"], False)
