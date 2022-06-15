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
            "viandes_volailles_bio": 10,
            "produits_de_la_mer_bio": 10,
            "produits_laitiers_bio": 10,
            "boulangerie_bio": 10,
            "boissons_bio": 10,
            "autres_bio": 10,
            "viandes_volailles_label_rouge": 10,
            "produits_de_la_mer_label_rouge": 10,
            "produits_laitiers_label_rouge": 10,
            "boulangerie_label_rouge": 10,
            "boissons_label_rouge": 10,
            "autres_label_rouge": 10,
            "viandes_volailles_aocaop_igp_stg": 10,
            "produits_de_la_mer_aocaop_igp_stg": 10,
            "produits_laitiers_aocaop_igp_stg": 10,
            "boulangerie_aocaop_igp_stg": 10,
            "boissons_aocaop_igp_stg": 10,
            "autres_aocaop_igp_stg": 10,
            "viandes_volailles_hve": 10,
            "produits_de_la_mer_hve": 10,
            "produits_laitiers_hve": 10,
            "boulangerie_hve": 10,
            "boissons_hve": 10,
            "autres_hve": 10,
            "viandes_volailles_peche_durable": 10,
            "produits_de_la_mer_peche_durable": 10,
            "produits_laitiers_peche_durable": 10,
            "boulangerie_peche_durable": 10,
            "boissons_peche_durable": 10,
            "autres_peche_durable": 10,
            "viandes_volailles_rup": 10,
            "produits_de_la_mer_rup": 10,
            "produits_laitiers_rup": 10,
            "boulangerie_rup": 10,
            "boissons_rup": 10,
            "autres_rup": 10,
            "viandes_volailles_fermier": 10,
            "produits_de_la_mer_fermier": 10,
            "produits_laitiers_fermier": 10,
            "boulangerie_fermier": 10,
            "boissons_fermier": 10,
            "autres_fermier": 10,
            "viandes_volailles_externalites": 10,
            "produits_de_la_mer_externalites": 10,
            "produits_laitiers_externalites": 10,
            "boulangerie_externalites": 10,
            "boissons_externalites": 10,
            "autres_externalites": 10,
            "viandes_volailles_commerce_equitable": 10,
            "produits_de_la_mer_commerce_equitable": 10,
            "produits_laitiers_commerce_equitable": 10,
            "boulangerie_commerce_equitable": 10,
            "boissons_commerce_equitable": 10,
            "autres_commerce_equitable": 10,
            "viandes_volailles_performance": 10,
            "produits_de_la_mer_performance": 10,
            "produits_laitiers_performance": 10,
            "boulangerie_performance": 10,
            "boissons_performance": 10,
            "autres_performance": 10,
            "viandes_volailles_equivalents": 10,
            "produits_de_la_mer_equivalents": 10,
            "produits_laitiers_equivalents": 10,
            "boulangerie_equivalents": 10,
            "boissons_equivalents": 10,
            "autres_equivalents": 10,
            "viandes_volailles_france": 10,
            "produits_de_la_mer_france": 10,
            "produits_laitiers_france": 10,
            "boulangerie_france": 10,
            "boissons_france": 10,
            "autres_france": 10,
            "viandes_volailles_short_distribution": 10,
            "produits_de_la_mer_short_distribution": 10,
            "produits_laitiers_short_distribution": 10,
            "boulangerie_short_distribution": 10,
            "boissons_short_distribution": 10,
            "autres_short_distribution": 10,
            "viandes_volailles_local": 10,
            "produits_de_la_mer_local": 10,
            "produits_laitiers_local": 10,
            "boulangerie_local": 10,
            "boissons_local": 10,
            "autres_local": 10,
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
        self.assertEqual(diagnostic.total_label_bio, 60)
        self.assertEqual(diagnostic.total_label_label_rouge, 60)
        self.assertEqual(diagnostic.total_label_aocaop_igp_stg, 60)
        self.assertEqual(diagnostic.total_label_hve, 60)
        self.assertEqual(diagnostic.total_label_peche_durable, 60)
        self.assertEqual(diagnostic.total_label_rup, 60)
        self.assertEqual(diagnostic.total_label_fermier, 60)
        self.assertEqual(diagnostic.total_label_externalites, 60)
        self.assertEqual(diagnostic.total_label_commerce_equitable, 60)
        self.assertEqual(diagnostic.total_label_performance, 60)
        self.assertEqual(diagnostic.total_label_equivalents, 60)
        self.assertEqual(diagnostic.total_label_france, 60)
        self.assertEqual(diagnostic.total_label_short_distribution, 60)
        self.assertEqual(diagnostic.total_label_local, 60)
        self.assertEqual(diagnostic.total_family_viandes_volailles, 140)
        self.assertEqual(diagnostic.total_family_produits_de_la_mer, 140)
        self.assertEqual(diagnostic.total_family_produits_laitiers, 140)
        self.assertEqual(diagnostic.total_family_boulangerie, 140)
        self.assertEqual(diagnostic.total_family_boissons, 140)
        self.assertEqual(diagnostic.total_family_autres, 140)

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
        Diagnostic creation campaign info cannot be updated
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
