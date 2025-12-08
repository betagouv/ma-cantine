from decimal import Decimal

from django.core.exceptions import BadRequest
from django.db import transaction
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic
from data.models.creation_source import CreationSource


class DiagnosticCreateApiTest(APITestCase):
    def test_unauthenticated_create_diagnostic_call(self):
        """
        When calling this API unathenticated we expect a 403
        """
        canteen = CanteenFactory()

        payload = {"year": 2020}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_diagnostic_missing_canteen(self):
        """
        When calling this API on an unexistent canteen we expect a 404
        """
        payload = {"year": 2020}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": 999}), payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_diagnostic_forbidden_canteen(self):
        """
        When calling this API on a canteen that the user doesn't manage,
        we expect a 403
        """
        canteen = CanteenFactory()

        payload = {"year": 2020}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_empty_diagnostic_error(self):
        """
        When calling this API on a canteen that the user manages
        we need to provide the required field(s)
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_minimal_diagnostic(self):
        """
        When calling this API on a canteen that the user manages
        we expect a diagnostic to be created
        (minimal required fields)
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {"year": 2020}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_minimal_diagnostic_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        canteen = CanteenFactory(managers=[user])

        payload = {"year": 2020}
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @authenticate
    def test_create_diagnostic_creation_source(self):
        canteen = CanteenFactory()
        canteen.managers.add(authenticate.user)

        # from the APP
        payload = {"year": 2020, "creation_source": "APP"}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id)
        self.assertEqual(diagnostic.creation_source, CreationSource.APP)

        # defaults to API
        payload = {"year": 2021}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id, year=2021)
        self.assertEqual(diagnostic.creation_source, CreationSource.API)

        # returns a 404 if the creation_source is not valid
        payload = {"year": 2022, "creation_source": "UNKNOWN"}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_full_diagnostic(self):
        """
        When calling this API on a canteen that the user manages
        we expect a diagnostic to be created
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "year": 2020,
            "diagnostic_type": Diagnostic.DiagnosticType.COMPLETE,
            "valeur_bio": 1000,
            "valeur_siqo": 3000,
            "valeur_totale": 10000,
            "has_waste_diagnostic": True,
            "has_waste_plan": False,
            "waste_actions": ["INSCRIPTION", "AWARENESS"],
            "other_waste_action": "We compost things",
            "has_donation_agreement": False,
            "has_waste_measures": True,
            "duration_leftovers_measurement": 30,
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
            "service_type": "MULTIPLE_SELF",
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
            # detailed value fields
            "valeur_viandes_volailles_bio": 10,
            "valeur_produits_de_la_mer_bio": 10,
            "valeur_fruits_et_legumes_bio": 10,
            "valeur_charcuterie_bio": 10,
            "valeur_produits_laitiers_bio": 10,
            "valeur_boulangerie_bio": 10,
            "valeur_boissons_bio": 10,
            "valeur_autres_bio": 10,
            "valeur_viandes_volailles_label_rouge": 10,
            "valeur_produits_de_la_mer_label_rouge": 10,
            "valeur_fruits_et_legumes_label_rouge": 10,
            "valeur_charcuterie_label_rouge": 10,
            "valeur_produits_laitiers_label_rouge": 10,
            "valeur_boulangerie_label_rouge": 10,
            "valeur_boissons_label_rouge": 10,
            "valeur_autres_label_rouge": 10,
            "valeur_viandes_volailles_aocaop_igp_stg": 10,
            "valeur_produits_de_la_mer_aocaop_igp_stg": 10,
            "valeur_fruits_et_legumes_aocaop_igp_stg": 10,
            "valeur_charcuterie_aocaop_igp_stg": 10,
            "valeur_produits_laitiers_aocaop_igp_stg": 10,
            "valeur_boulangerie_aocaop_igp_stg": 10,
            "valeur_boissons_aocaop_igp_stg": 10,
            "valeur_autres_aocaop_igp_stg": 10,
            "valeur_viandes_volailles_hve": 10,
            "valeur_produits_de_la_mer_hve": 10,
            "valeur_fruits_et_legumes_hve": 10,
            "valeur_charcuterie_hve": 10,
            "valeur_produits_laitiers_hve": 10,
            "valeur_boulangerie_hve": 10,
            "valeur_boissons_hve": 10,
            "valeur_autres_hve": 10,
            "valeur_viandes_volailles_peche_durable": 10,
            "valeur_produits_de_la_mer_peche_durable": 10,
            "valeur_fruits_et_legumes_peche_durable": 10,
            "valeur_charcuterie_peche_durable": 10,
            "valeur_produits_laitiers_peche_durable": 10,
            "valeur_boulangerie_peche_durable": 10,
            "valeur_boissons_peche_durable": 10,
            "valeur_autres_peche_durable": 10,
            "valeur_viandes_volailles_rup": 10,
            "valeur_produits_de_la_mer_rup": 10,
            "valeur_fruits_et_legumes_rup": 10,
            "valeur_charcuterie_rup": 10,
            "valeur_produits_laitiers_rup": 10,
            "valeur_boulangerie_rup": 10,
            "valeur_boissons_rup": 10,
            "valeur_autres_rup": 10,
            "valeur_viandes_volailles_commerce_equitable": 10,
            "valeur_produits_de_la_mer_commerce_equitable": 10,
            "valeur_fruits_et_legumes_commerce_equitable": 10,
            "valeur_charcuterie_commerce_equitable": 10,
            "valeur_produits_laitiers_commerce_equitable": 10,
            "valeur_boulangerie_commerce_equitable": 10,
            "valeur_boissons_commerce_equitable": 10,
            "valeur_autres_commerce_equitable": 10,
            "valeur_viandes_volailles_fermier": 10,
            "valeur_produits_de_la_mer_fermier": 10,
            "valeur_fruits_et_legumes_fermier": 10,
            "valeur_charcuterie_fermier": 10,
            "valeur_produits_laitiers_fermier": 10,
            "valeur_boulangerie_fermier": 10,
            "valeur_boissons_fermier": 10,
            "valeur_autres_fermier": 10,
            "valeur_viandes_volailles_externalites": 10,
            "valeur_produits_de_la_mer_externalites": 10,
            "valeur_fruits_et_legumes_externalites": 10,
            "valeur_charcuterie_externalites": 10,
            "valeur_produits_laitiers_externalites": 10,
            "valeur_boulangerie_externalites": 10,
            "valeur_boissons_externalites": 10,
            "valeur_autres_externalites": 10,
            "valeur_viandes_volailles_performance": 10,
            "valeur_produits_de_la_mer_performance": 10,
            "valeur_fruits_et_legumes_performance": 10,
            "valeur_charcuterie_performance": 10,
            "valeur_produits_laitiers_performance": 10,
            "valeur_boulangerie_performance": 10,
            "valeur_boissons_performance": 10,
            "valeur_autres_performance": 10,
            "valeur_viandes_volailles_non_egalim": 10,
            "valeur_produits_de_la_mer_non_egalim": 10,
            "valeur_fruits_et_legumes_non_egalim": 10,
            "valeur_charcuterie_non_egalim": 10,
            "valeur_produits_laitiers_non_egalim": 10,
            "valeur_boulangerie_non_egalim": 10,
            "valeur_boissons_non_egalim": 10,
            "valeur_autres_non_egalim": 10,
            "valeur_viandes_volailles_france": 10,
            "valeur_produits_de_la_mer_france": 10,
            "valeur_fruits_et_legumes_france": 10,
            "valeur_charcuterie_france": 10,
            "valeur_produits_laitiers_france": 10,
            "valeur_boulangerie_france": 10,
            "valeur_boissons_france": 10,
            "valeur_autres_france": 10,
            "valeur_viandes_volailles_circuit_court": 10,
            "valeur_produits_de_la_mer_circuit_court": 10,
            "valeur_fruits_et_legumes_circuit_court": 10,
            "valeur_charcuterie_circuit_court": 10,
            "valeur_produits_laitiers_circuit_court": 10,
            "valeur_boulangerie_circuit_court": 10,
            "valeur_boissons_circuit_court": 10,
            "valeur_autres_circuit_court": 10,
            "valeur_viandes_volailles_local": 10,
            "valeur_produits_de_la_mer_local": 10,
            "valeur_fruits_et_legumes_local": 10,
            "valeur_charcuterie_local": 10,
            "valeur_produits_laitiers_local": 10,
            "valeur_boulangerie_local": 10,
            "valeur_boissons_local": 10,
            "valeur_autres_local": 10,
            # end of detailed value fields
        }
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id)

        self.assertEqual(diagnostic.year, 2020)
        self.assertTrue(diagnostic.cooking_plastic_substituted)
        self.assertFalse(diagnostic.has_donation_agreement)
        self.assertIn("AWARENESS", diagnostic.waste_actions)
        self.assertEqual(diagnostic.duration_leftovers_measurement, 30)
        self.assertIn("TRAINING", diagnostic.diversification_plan_actions)
        self.assertEqual("MULTIPLE_SELF", diagnostic.service_type)
        self.assertEqual("DAILY", diagnostic.vegetarian_weekly_recurrence)
        self.assertIn("GRAIN", diagnostic.vegetarian_menu_bases)
        self.assertIn("CHEESE", diagnostic.vegetarian_menu_bases)
        self.assertEqual(diagnostic.donation_quantity, Decimal("60.6"))
        self.assertEqual(diagnostic.communication_frequency, "YEARLY")
        self.assertTrue(diagnostic.communicates_on_food_quality)
        self.assertEqual(diagnostic.creation_source, CreationSource.API)
        self.assertEqual(diagnostic.creation_mtm_source, "mtm_source_value")
        self.assertEqual(diagnostic.creation_mtm_campaign, "mtm_campaign_value")
        self.assertEqual(diagnostic.creation_mtm_medium, "mtm_medium_value")
        self.assertEqual(diagnostic.label_sum("bio"), 80)
        self.assertEqual(diagnostic.label_sum("label_rouge"), 80)
        self.assertEqual(diagnostic.label_sum("aocaop_igp_stg"), 80)
        self.assertEqual(diagnostic.label_sum("hve"), 80)
        self.assertEqual(diagnostic.label_sum("peche_durable"), 80)
        self.assertEqual(diagnostic.label_sum("rup"), 80)
        self.assertEqual(diagnostic.label_sum("commerce_equitable"), 80)
        self.assertEqual(diagnostic.label_sum("fermier"), 80)
        self.assertEqual(diagnostic.label_sum("externalites"), 80)
        self.assertEqual(diagnostic.label_sum("performance"), 80)
        self.assertEqual(diagnostic.label_sum("france"), 80)
        self.assertEqual(diagnostic.label_sum("circuit_court"), 80)
        self.assertEqual(diagnostic.label_sum("local"), 80)
        self.assertEqual(diagnostic.family_sum("viandes_volailles"), 110)
        self.assertEqual(diagnostic.family_sum("produits_de_la_mer"), 110)
        self.assertEqual(diagnostic.family_sum("fruits_et_legumes"), 110)
        self.assertEqual(diagnostic.family_sum("charcuterie"), 110)
        self.assertEqual(diagnostic.family_sum("produits_laitiers"), 110)
        self.assertEqual(diagnostic.family_sum("boulangerie"), 110)
        self.assertEqual(diagnostic.family_sum("boissons"), 110)
        self.assertEqual(diagnostic.family_sum("autres"), 110)

    # Tests for unit conversion for total_leftovers. This is because the field was first
    # made in ton but then it was decided that it is best for the users to work in kg
    # for consistency.
    @authenticate
    def test_total_leftovers_conversion_create_diagnostic(self):
        """
        On CREATE, total_leftovers should be converted from kg to ton
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "year": 2020,
            "total_leftovers": 1234.56,
        }
        response = self.client.post(
            reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id)
        self.assertEqual(diagnostic.total_leftovers, Decimal("1.23456"))

    @authenticate
    def test_create_duplicate_diagnostic(self):
        """
        Shouldn't be able to add a diagnostic with the same canteen and year
        as an existing diagnostic
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {"year": 2020, "valeur_bio": 10}
        self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        try:
            with transaction.atomic():
                payload = {"year": 2020, "valeur_bio": 1000}
                response = self.client.post(
                    reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}),
                    payload,
                )
        except BadRequest:
            pass

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        diagnostic = Diagnostic.objects.get(canteen__id=canteen.id)
        self.assertEqual(diagnostic.valeur_bio, 10)

    @authenticate
    def test_create_diagnostic_bad_total(self):
        """
        Do not create a diagnostic where the sum of the values is > total
        """
        canteen = CanteenFactory(managers=[authenticate.user])

        payload = {
            "year": 2020,
            "valeur_bio": 1000,
            "valeur_siqo": 1000,
            "valeur_egalim_autres": 1000,
            "valeur_totale": 2000,
        }
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DiagnosticUpdateApiTest(APITestCase):
    @authenticate
    def test_edit_diagnostic_unauthorized(self):
        """
        The user can only edit diagnostics of canteens they manage
        """
        diagnostic = DiagnosticFactory(year=2019)

        payload = {"year": 2020}

        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.year, 2019)

    @authenticate
    def test_cannot_update_diagnostic_with_put(self):
        """
        A user cannot update the data from a diagnostic object with PUT
        """
        diagnostic = DiagnosticFactory(year=2019)
        diagnostic.canteen.managers.add(authenticate.user)

        payload = {"year": 2020}
        response = self.client.put(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_edit_diagnostic(self):
        """
        The user can edit a diagnostic of a canteen they manage
        """
        diagnostic = DiagnosticFactory(year=2019)
        diagnostic.canteen.managers.add(authenticate.user)

        payload = {"year": 2020}
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.year, 2020)

    def test_edit_diagnostic_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory(year=2019)
        diagnostic.canteen.managers.add(user)

        payload = {"year": 2020}
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_edit_diagnostic_tracking_info(self):
        """
        Diagnostic creation campaign info cannot be updated
        """
        diagnostic = DiagnosticFactory(
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
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.year, 2020)
        self.assertIsNone(diagnostic.creation_mtm_source)
        self.assertIsNone(diagnostic.creation_mtm_campaign)
        self.assertIsNone(diagnostic.creation_mtm_medium)

    @authenticate
    def test_edit_diagnostic_bad_total(self):
        """
        Do not save edits to a diagnostic which make the sum of the values > total
        """
        diagnostic = DiagnosticFactory(year=2019, valeur_totale=10, valeur_bio=5, valeur_siqo=2)
        diagnostic.canteen.managers.add(authenticate.user)

        payload = {"valeur_siqo": 999}
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.valeur_siqo, 2)

    @authenticate
    def test_total_leftovers_conversion_update_diagnostic(self):
        """
        On UPDATE, total_leftovers should be converted from kg to ton
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, total_leftovers=Decimal("1.23456"))

        payload = {
            "total_leftovers": 6666.66,
        }
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.total_leftovers, Decimal("6.66666"))

    @authenticate
    def test_total_leftovers_conversion_update_diagnostic_no_conversion(self):
        """
        On UPDATE, total_leftovers should be converted from kg to ton
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, total_leftovers=Decimal("1.23456"))

        payload = {
            "bread_leftovers": 100,
        }
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.total_leftovers, Decimal("1.23456"))
        self.assertEqual(diagnostic.bread_leftovers, Decimal("100"))

    @authenticate
    def test_total_leftovers_conversion_update_diagnostic_bad_values(self):
        """
        Should return reasonable error if the given value of total leftovers fails validation
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, total_leftovers=Decimal("1.23456"))

        payload = {
            "total_leftovers": 6666.666,
        }
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.json()
        self.assertEqual(
            errors["totalLeftovers"][0], "Assurez-vous qu'il n'y a pas plus de 2 chiffres après la virgule."
        )
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.total_leftovers, Decimal("1.23456"))

        payload = {
            "total_leftovers": "this shouldn't be a string",
        }
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.json()
        self.assertEqual(errors["totalLeftovers"][0], "Assurez-vous que cette valeur est un chiffre décimal.")
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.total_leftovers, Decimal("1.23456"))

    @authenticate
    def test_edit_submitted_diagnostic(self):
        """
        A diagnostic cannot be edited if it has been teledeclared
        """
        date_in_2022_teledeclaration_campaign = "2022-08-30"
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        with freeze_time(date_in_2022_teledeclaration_campaign):
            diagnostic.teledeclare(applicant=authenticate.user)

        payload = {"year": 2020}
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.year, 2021)

    @authenticate
    def test_edit_cancelled_diagnostic(self):
        """
        A diagnostic can be edited if its teledeclaration has been cancelled
        """
        date_in_2022_teledeclaration_campaign = "2022-08-30"
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        with freeze_time(date_in_2022_teledeclaration_campaign):
            diagnostic.teledeclare(applicant=authenticate.user)
            diagnostic.cancel()

        payload = {"year": 2020}
        response = self.client.patch(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            ),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.year, 2020)


class DiagnosticDeleteApiTest(APITestCase):
    @authenticate
    def test_delete_diagnostic_not_allowed(self):
        diagnostic = DiagnosticFactory(year=2019)
        diagnostic.canteen.managers.add(authenticate.user)

        response = self.client.delete(
            reverse(
                "diagnostic_update",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
