from django.urls import reverse
from django.db import transaction
from django.core.exceptions import BadRequest
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic, Teledeclaration
from .utils import authenticate
import decimal


class TestDiagnosticsApi(APITestCase):
    def test_unauthenticated_create_diagnostic_call(self):
        """
        When calling this API unathenticated we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_diagnostic_missing_canteen(self):
        """
        When calling this API on an unexistent canteen we expect a 404
        """
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": 999}), {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_diagnostic_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 403
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_diagnostic(self):
        """
        When calling this API on a canteen that the user manages
        we expect a diagnostic to be created
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "year": 2020,
            "value_bio_ht": 1000,
            "value_sustainable_ht": 3000,
            "value_pat_ht": 200,
            "value_total_ht": 10000,
            "value_label_rouge": 10,
            "value_label_aoc_igp": 20,
            "value_label_hve": 30,
            "has_waste_diagnostic": True,
            "has_waste_plan": False,
            "waste_actions": ["INSCRIPTION", "AWARENESS"],
            "other_waste_action": "We compost things",
            "has_donation_agreement": False,
            "has_waste_measures": True,
            "bread_leftovers": 10.1,
            "served_leftovers": 20.2,
            "unserved_leftovers": 30.3,
            "side_leftovers": 40.4,
            "donation_frequency": 50,
            "donation_quantity": 60.6,
            "donation_food_type": "We donate bread and cheese",
            "other_waste_comments": "We do our best",
            "has_diversification_plan": True,
            "diversification_plan_actions": ["PRODUCTS", "TRAINING"],
            "vegetarian_weekly_recurrence": "DAILY",
            "vegetarian_menu_type": "UNIQUE",
            "vegetarian_menu_bases": ["GRAIN", "READYMADE", "CHEESE"],
            "cooking_plastic_substituted": True,
            "serving_plastic_substituted": False,
            "plastic_bottles_substituted": True,
            "plastic_tableware_substituted": False,
            "communication_supports": ["DISPLAY", "DIGITAL"],
            "other_communication_support": "We put on plays",
            "communication_support_url": "https://example.com",
            "communicates_on_food_plan": True,
            "communicates_on_food_quality": True,
            "communication_frequency": "YEARLY",
            "creation_mtm_source": "mtm_source_value",
            "creation_mtm_campaign": "mtm_campaign_value",
            "creation_mtm_medium": "mtm_medium_value",
        }
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id)

        self.assertEqual(diagnostic.year, 2020)
        self.assertTrue(diagnostic.cooking_plastic_substituted)
        self.assertFalse(diagnostic.has_donation_agreement)
        self.assertIn("AWARENESS", diagnostic.waste_actions)
        self.assertIn("TRAINING", diagnostic.diversification_plan_actions)
        self.assertEqual("DAILY", diagnostic.vegetarian_weekly_recurrence)
        self.assertIn("GRAIN", diagnostic.vegetarian_menu_bases)
        self.assertIn("CHEESE", diagnostic.vegetarian_menu_bases)
        self.assertEqual(diagnostic.donation_quantity, decimal.Decimal("60.6"))
        self.assertEqual(diagnostic.communication_frequency, "YEARLY")
        self.assertTrue(diagnostic.communicates_on_food_quality)
        self.assertEqual(diagnostic.value_pat_ht, 200)
        self.assertEqual(diagnostic.value_label_rouge, 10)
        self.assertEqual(diagnostic.value_label_aoc_igp, 20)
        self.assertEqual(diagnostic.value_label_hve, 30)
        self.assertEqual(diagnostic.creation_mtm_source, "mtm_source_value")
        self.assertEqual(diagnostic.creation_mtm_campaign, "mtm_campaign_value")
        self.assertEqual(diagnostic.creation_mtm_medium, "mtm_medium_value")

    @authenticate
    def test_create_duplicate_diagnostic(self):
        """
        Shouldn't be able to add a diagnostic with the same canteen and year
        as an existing diagnostic
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        self.client.post(
            reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}),
            {"year": 2020, "value_bio_ht": 10},
        )

        payload = {
            "year": 2020,
            "value_bio_ht": 1000,
        }
        try:
            with transaction.atomic():
                response = self.client.post(
                    reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}),
                    payload,
                )
        except BadRequest:
            pass
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id)
        self.assertEqual(diagnostic.value_bio_ht, 10)

    @authenticate
    def test_create_diagnostic_bad_total(self):
        """
        Do not create a diagnostic where the sum of the values is > total
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {
            "year": 2020,
            "value_bio_ht": 1000,
            "value_sustainable_ht": 3000,
            "value_total_ht": 1000,
        }
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_edit_diagnostic_unauthorized(self):
        """
        The user can only edit diagnostics of canteens they
        manage
        """
        diagnostic = DiagnosticFactory.create()
        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnostic_edition",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_edit_diagnostic(self):
        """
        The user can edit a diagnostic of a canteen they manage
        """
        diagnostic = DiagnosticFactory.create(year=2019)
        diagnostic.canteen.managers.add(authenticate.user)
        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnostic_edition",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )
        diagnostic.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(diagnostic.year, 2020)

    @authenticate
    def test_edit_diagnostic_tracking_info(self):
        """
        The user can edit a diagnostic of a canteen they manage
        """
        diagnostic = DiagnosticFactory.create(
            year=2019,
            creation_mtm_source=None,
            creation_mtm_campaign=None,
            creation_mtm_medium=None,
        )
        diagnostic.canteen.managers.add(authenticate.user)
        payload = {
            "year": 2020,
            "creation_mtm_source": "mtm_source_value",
            "creation_mtm_campaign": "mtm_campaign_value",
            "creation_mtm_medium": "mtm_medium_value",
        }

        response = self.client.patch(
            reverse(
                "diagnostic_edition",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )
        diagnostic.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(diagnostic.year, 2020)
        self.assertIsNone(diagnostic.creation_mtm_source)
        self.assertIsNone(diagnostic.creation_mtm_campaign)
        self.assertIsNone(diagnostic.creation_mtm_medium)

    @authenticate
    def test_edit_diagnostic_bad_total(self):
        """
        Do not save edits to a diagnostic which make the sum of the values > total
        """
        diagnostic = DiagnosticFactory.create(year=2019, value_total_ht=10, value_bio_ht=5, value_sustainable_ht=2)
        diagnostic.canteen.managers.add(authenticate.user)
        payload = {"value_sustainable_ht": 999}

        response = self.client.patch(
            reverse(
                "diagnostic_edition",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )
        diagnostic.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(diagnostic.value_sustainable_ht, 2)

    @authenticate
    def test_edit_submitted_diagnostic(self):
        """
        A diagnostic cannot be edited if a submitted teledeclaration
        object linked to it exists
        """
        diagnostic = DiagnosticFactory.create(year=2019)
        diagnostic.canteen.managers.add(authenticate.user)
        Teledeclaration.createFromDiagnostic(diagnostic, authenticate.user)

        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnostic_edition",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        diagnostic.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(diagnostic.year, 2019)

    @authenticate
    def test_edit_cancelled_diagnostic(self):
        """
        A diagnostic can be edited if a cancelled teledeclaration
        object linked to it exists
        """
        diagnostic = DiagnosticFactory.create(year=2019)
        diagnostic.canteen.managers.add(authenticate.user)
        Teledeclaration.createFromDiagnostic(
            diagnostic,
            authenticate.user,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
        )

        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnostic_edition",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        diagnostic.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(diagnostic.year, 2020)
