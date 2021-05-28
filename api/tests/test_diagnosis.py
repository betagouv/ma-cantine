from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, DiagnosisFactory
from data.models import Diagnosis
from .utils import authenticate


class TestDiagnosisApi(APITestCase):
    def test_unauthenticated_create_diagnosis_call(self):
        """
        When calling this API unathenticated we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(
            reverse("diagnosis_creation", kwargs={"canteen_pk": canteen.id}), {}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_diagnosis_missing_canteen(self):
        """
        When calling this API on an unexistent canteen we expect a 404
        """
        response = self.client.post(
            reverse("diagnosis_creation", kwargs={"canteen_pk": 999}), {}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_diagnosis_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(
            reverse("diagnosis_creation", kwargs={"canteen_pk": canteen.id}), {}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_diagnosis(self):
        """
        When calling this API on a canteen that the user manages
        we expect a diagnostic to be created
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "year": 2020,
            "value_bio_ht": 1000,
            "value_fair_trade_ht": 2000,
            "value_sustainable_ht": 3000,
            "value_total_ht": 10000,
            "has_waste_diagnostic": True,
            "has_waste_plan": False,
            "waste_actions": ["INSCRIPTION", "AWARENESS"],
            "has_donation_agreement": False,
            "has_diversification_plan": True,
            "vegetarian_weekly_recurrence": "LOW",
            "vegetarian_menu_type": "UNIQUE",
            "cooking_plastic_substituted": True,
            "serving_plastic_substituted": False,
            "plastic_bottles_substituted": True,
            "plastic_tableware_substituted": False,
            "communication_supports": ["EMAIL", "WEBSITE"],
            "communication_support_url": "https://example.com",
            "comunicates_on_food_plan": True,
        }
        response = self.client.post(
            reverse("diagnosis_creation", kwargs={"canteen_pk": canteen.id}), payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        diagnosis = Diagnosis.objects.get(canteen__id=canteen.id)

        self.assertEqual(diagnosis.year, 2020)
        self.assertTrue(diagnosis.cooking_plastic_substituted)
        self.assertFalse(diagnosis.has_donation_agreement)
        self.assertIn("AWARENESS", diagnosis.waste_actions)

    @authenticate
    def test_edit_diagnosis_unauthorized(self):
        """
        The user can only edit diagnosis of canteens they
        manage
        """
        diagnosis = DiagnosisFactory.create()
        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnosis_edition",
                kwargs={"canteen_pk": diagnosis.canteen.id, "pk": diagnosis.id},
            ),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_edit_diagnosis(self):
        """
        The user can edit a diagnosis of a canteen they manage
        """
        diagnosis = DiagnosisFactory.create(year=2019)
        diagnosis.canteen.managers.add(authenticate.user)
        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnosis_edition",
                kwargs={"canteen_pk": diagnosis.canteen.id, "pk": diagnosis.id},
            ),
            payload,
        )
        diagnosis.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(diagnosis.year, 2020)
