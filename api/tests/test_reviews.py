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
            "rating": 3,
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
            "rating": 3,
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
    def test_fail_duplicate_review(self):
        """
        Test that user cannot submit two reviews for the same page
        """
        ReviewFactory.create(user=authenticate.user, page="CanteensHome")
        payload = {
            "page": "CanteensHome",
            "rating": 3,
            "suggestion": "Make it read my mind",
        }
        response = self.client.post(reverse("create_review"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_get_review_for_page(self):
        """
        Test that user can get the review they've submitted for a page
        """
        ReviewFactory.create(user=authenticate.user, page="CanteensHome", rating=3)
        ReviewFactory.create(page="CanteensHome", rating=5)  # should not be fetched
        response = self.client.get(reverse("get_review", kwargs={"page_pk": "CanteensHome"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["rating"], 3)
