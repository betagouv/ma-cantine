from decimal import Decimal

from django.core.exceptions import BadRequest
from django.db import transaction
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory
from data.models import Canteen, Diagnostic, Teledeclaration

from .utils import authenticate, get_oauth2_token


class TestDiagnosticsApi(APITestCase):
    def test_unauthenticated_create_diagnostic_call(self):
        """
        When calling this API unathenticated we expect a 403
        """
        canteen = CanteenFactory.create()
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
        canteen = CanteenFactory.create()
        payload = {"year": 2020}
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_empty_diagnostic_error(self):
        """
        When calling this API on a canteen that the user manages
        we need to provide the required field(s)
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {"year": 2020}

        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @authenticate
    def test_create_full_diagnostic(self):
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
            "value_total_ht": 10000,
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
            "value_viandes_volailles_bio": 10,
            "value_produits_de_la_mer_bio": 10,
            "value_fruits_et_legumes_bio": 10,
            "value_charcuterie_bio": 10,
            "value_produits_laitiers_bio": 10,
            "value_boulangerie_bio": 10,
            "value_boissons_bio": 10,
            "value_autres_bio": 10,
            "value_viandes_volailles_label_rouge": 10,
            "value_produits_de_la_mer_label_rouge": 10,
            "value_fruits_et_legumes_label_rouge": 10,
            "value_charcuterie_label_rouge": 10,
            "value_produits_laitiers_label_rouge": 10,
            "value_boulangerie_label_rouge": 10,
            "value_boissons_label_rouge": 10,
            "value_autres_label_rouge": 10,
            "value_viandes_volailles_aocaop_igp_stg": 10,
            "value_produits_de_la_mer_aocaop_igp_stg": 10,
            "value_fruits_et_legumes_aocaop_igp_stg": 10,
            "value_charcuterie_aocaop_igp_stg": 10,
            "value_produits_laitiers_aocaop_igp_stg": 10,
            "value_boulangerie_aocaop_igp_stg": 10,
            "value_boissons_aocaop_igp_stg": 10,
            "value_autres_aocaop_igp_stg": 10,
            "value_viandes_volailles_hve": 10,
            "value_produits_de_la_mer_hve": 10,
            "value_fruits_et_legumes_hve": 10,
            "value_charcuterie_hve": 10,
            "value_produits_laitiers_hve": 10,
            "value_boulangerie_hve": 10,
            "value_boissons_hve": 10,
            "value_autres_hve": 10,
            "value_viandes_volailles_peche_durable": 10,
            "value_produits_de_la_mer_peche_durable": 10,
            "value_fruits_et_legumes_peche_durable": 10,
            "value_charcuterie_peche_durable": 10,
            "value_produits_laitiers_peche_durable": 10,
            "value_boulangerie_peche_durable": 10,
            "value_boissons_peche_durable": 10,
            "value_autres_peche_durable": 10,
            "value_viandes_volailles_rup": 10,
            "value_produits_de_la_mer_rup": 10,
            "value_fruits_et_legumes_rup": 10,
            "value_charcuterie_rup": 10,
            "value_produits_laitiers_rup": 10,
            "value_boulangerie_rup": 10,
            "value_boissons_rup": 10,
            "value_autres_rup": 10,
            "value_viandes_volailles_fermier": 10,
            "value_produits_de_la_mer_fermier": 10,
            "value_fruits_et_legumes_fermier": 10,
            "value_charcuterie_fermier": 10,
            "value_produits_laitiers_fermier": 10,
            "value_boulangerie_fermier": 10,
            "value_boissons_fermier": 10,
            "value_autres_fermier": 10,
            "value_viandes_volailles_externalites": 10,
            "value_produits_de_la_mer_externalites": 10,
            "value_fruits_et_legumes_externalites": 10,
            "value_charcuterie_externalites": 10,
            "value_produits_laitiers_externalites": 10,
            "value_boulangerie_externalites": 10,
            "value_boissons_externalites": 10,
            "value_autres_externalites": 10,
            "value_viandes_volailles_commerce_equitable": 10,
            "value_produits_de_la_mer_commerce_equitable": 10,
            "value_fruits_et_legumes_commerce_equitable": 10,
            "value_charcuterie_commerce_equitable": 10,
            "value_produits_laitiers_commerce_equitable": 10,
            "value_boulangerie_commerce_equitable": 10,
            "value_boissons_commerce_equitable": 10,
            "value_autres_commerce_equitable": 10,
            "value_viandes_volailles_performance": 10,
            "value_produits_de_la_mer_performance": 10,
            "value_fruits_et_legumes_performance": 10,
            "value_charcuterie_performance": 10,
            "value_produits_laitiers_performance": 10,
            "value_boulangerie_performance": 10,
            "value_boissons_performance": 10,
            "value_autres_performance": 10,
            "value_viandes_volailles_non_egalim": 10,
            "value_produits_de_la_mer_non_egalim": 10,
            "value_fruits_et_legumes_non_egalim": 10,
            "value_charcuterie_non_egalim": 10,
            "value_produits_laitiers_non_egalim": 10,
            "value_boulangerie_non_egalim": 10,
            "value_boissons_non_egalim": 10,
            "value_autres_non_egalim": 10,
            "value_viandes_volailles_france": 10,
            "value_produits_de_la_mer_france": 10,
            "value_fruits_et_legumes_france": 10,
            "value_charcuterie_france": 10,
            "value_produits_laitiers_france": 10,
            "value_boulangerie_france": 10,
            "value_boissons_france": 10,
            "value_autres_france": 10,
            "value_viandes_volailles_short_distribution": 10,
            "value_produits_de_la_mer_short_distribution": 10,
            "value_fruits_et_legumes_short_distribution": 10,
            "value_charcuterie_short_distribution": 10,
            "value_produits_laitiers_short_distribution": 10,
            "value_boulangerie_short_distribution": 10,
            "value_boissons_short_distribution": 10,
            "value_autres_short_distribution": 10,
            "value_viandes_volailles_local": 10,
            "value_produits_de_la_mer_local": 10,
            "value_fruits_et_legumes_local": 10,
            "value_charcuterie_local": 10,
            "value_produits_laitiers_local": 10,
            "value_boulangerie_local": 10,
            "value_boissons_local": 10,
            "value_autres_local": 10,
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
        self.assertEqual("DAILY", diagnostic.vegetarian_weekly_recurrence)
        self.assertIn("GRAIN", diagnostic.vegetarian_menu_bases)
        self.assertIn("CHEESE", diagnostic.vegetarian_menu_bases)
        self.assertEqual(diagnostic.donation_quantity, Decimal("60.6"))
        self.assertEqual(diagnostic.communication_frequency, "YEARLY")
        self.assertTrue(diagnostic.communicates_on_food_quality)
        self.assertEqual(diagnostic.creation_mtm_source, "mtm_source_value")
        self.assertEqual(diagnostic.creation_mtm_campaign, "mtm_campaign_value")
        self.assertEqual(diagnostic.creation_mtm_medium, "mtm_medium_value")
        self.assertEqual(diagnostic.total_label_bio, 80)
        self.assertEqual(diagnostic.total_label_label_rouge, 80)
        self.assertEqual(diagnostic.total_label_aocaop_igp_stg, 80)
        self.assertEqual(diagnostic.total_label_hve, 80)
        self.assertEqual(diagnostic.total_label_peche_durable, 80)
        self.assertEqual(diagnostic.total_label_rup, 80)
        self.assertEqual(diagnostic.total_label_fermier, 80)
        self.assertEqual(diagnostic.total_label_externalites, 80)
        self.assertEqual(diagnostic.total_label_commerce_equitable, 80)
        self.assertEqual(diagnostic.total_label_performance, 80)
        self.assertEqual(diagnostic.total_label_france, 80)
        self.assertEqual(diagnostic.total_label_short_distribution, 80)
        self.assertEqual(diagnostic.total_label_local, 80)
        self.assertEqual(diagnostic.total_family_viandes_volailles, 110)
        self.assertEqual(diagnostic.total_family_produits_de_la_mer, 110)
        self.assertEqual(diagnostic.total_family_fruits_et_legumes, 110)
        self.assertEqual(diagnostic.total_family_charcuterie, 110)
        self.assertEqual(diagnostic.total_family_produits_laitiers, 110)
        self.assertEqual(diagnostic.total_family_boulangerie, 110)
        self.assertEqual(diagnostic.total_family_boissons, 110)
        self.assertEqual(diagnostic.total_family_autres, 110)

    @authenticate
    def test_create_duplicate_diagnostic(self):
        """
        Shouldn't be able to add a diagnostic with the same canteen and year
        as an existing diagnostic
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

        payload = {"year": 2020, "value_bio_ht": 10}
        self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)

        try:
            with transaction.atomic():
                payload = {"year": 2020, "value_bio_ht": 1000}
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
            "value_sustainable_ht": 1000,
            "value_egalim_others_ht": 1000,
            "value_total_ht": 2000,
        }
        response = self.client.post(reverse("diagnostic_creation", kwargs={"canteen_pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_edit_diagnostic_unauthorized(self):
        """
        The user can only edit diagnostics of canteens they manage
        """
        diagnostic = DiagnosticFactory.create(year=2019)

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

    def test_edit_diagnostic_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory.create(year=2019)
        diagnostic.canteen.managers.add(user)

        payload = {"year": 2020}

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.patch(
            reverse(
                "diagnostic_edition",
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
        Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

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
        Teledeclaration.create_from_diagnostic(
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_get_diagnostics_to_td(self):
        """
        Check that the endpoint includes a list of diagnostics that could be teledeclared
        """
        last_year = 2021
        no_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        canteen_with_incomplete_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        DiagnosticFactory.create(canteen=canteen_with_incomplete_diag, year=last_year, value_total_ht=None)
        canteen_with_complete_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        complete_diag = DiagnosticFactory.create(
            canteen=canteen_with_complete_diag, year=last_year, value_total_ht=10000
        )

        canteen_with_incomplete_data = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            siret=None,  # this needs to be completed for the diag to be teledeclarable
        )
        DiagnosticFactory.create(canteen=canteen_with_incomplete_data, year=last_year, value_total_ht=10000)

        canteen_without_line_ministry = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            siret="31285246765507",
            line_ministry=None,
        )
        sector = SectorFactory(has_line_ministry=True)
        canteen_without_line_ministry.sectors.set([sector])
        canteen_without_line_ministry.save()
        DiagnosticFactory.create(canteen=canteen_without_line_ministry, year=last_year, value_total_ht=10000)

        # to verify we are returning the correct diag for the canteen, create another diag for a different year
        DiagnosticFactory.create(canteen=canteen_with_complete_diag, year=last_year - 1, value_total_ht=10000)
        canteen_with_td = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="55476895458384",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        td_diag = DiagnosticFactory.create(canteen=canteen_with_td, year=last_year, value_total_ht=2000)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)

        for canteen in [
            no_diag,
            canteen_with_incomplete_diag,
            canteen_with_complete_diag,
            canteen_with_incomplete_data,
            canteen_without_line_ministry,
            canteen_with_td,
        ]:
            canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("diagnostics_to_teledeclare", kwargs={"year": last_year}))
        diagnostics = response.json().get("results")

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["id"], complete_diag.id)

    @authenticate
    def test_get_diagnostics_to_td_none(self):
        """
        Check that the actions endpoint includes an empty list of diagnostics that could be teledeclared
        if there are no diags to TD
        """
        last_year = 2021

        response = self.client.get(reverse("diagnostics_to_teledeclare", kwargs={"year": last_year}))
        body = response.json().get("results")

        self.assertEqual(body, [])

    # Tests for unit conversion for total_leftovers. This is because the field was first
    # made in ton but then it was decided that it is best for the users to work in kg
    # for consistency.
    @authenticate
    def test_total_leftovers_conversion_create_diagnostic(self):
        """
        On CREATE, total_leftovers should be converted from kg to ton
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

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
    def test_total_leftovers_conversion_update_diagnostic(self):
        """
        On UPDATE, total_leftovers should be converted from kg to ton
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, total_leftovers=Decimal("1.23456"))

        payload = {
            "total_leftovers": 6666.66,
        }
        response = self.client.patch(
            reverse(
                "diagnostic_edition",
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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, total_leftovers=Decimal("1.23456"))

        payload = {
            "bread_leftovers": 100,
        }
        response = self.client.patch(
            reverse(
                "diagnostic_edition",
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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, total_leftovers=Decimal("1.23456"))

        payload = {
            "total_leftovers": 6666.666,
        }
        response = self.client.patch(
            reverse(
                "diagnostic_edition",
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
                "diagnostic_edition",
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
    def test_total_leftovers_conversion_get_diagnostic(self):
        """
        On GET, total_leftovers should be converted from ton to kg
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        DiagnosticFactory.create(canteen=canteen, total_leftovers=Decimal("1.23456"))
        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        self.assertEqual(len(body.get("diagnostics")), 1)
        serialized_diag = body.get("diagnostics")[0]

        self.assertEqual(serialized_diag["totalLeftovers"], 1234.56)
