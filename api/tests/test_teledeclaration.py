from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory, TeledeclarationFactory
from data.models import Teledeclaration
from .utils import authenticate


class TestTeledeclarationApi(APITestCase):
    def test_create_unauthenticated(self):
        """
        The creation of a teledeclaration is only available
        to authenticated users
        """
        payload = {"diagnosticId": 1}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cancel_unauthenticated(self):
        payload = {"teledeclarationId": 1}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_generate_pdf_unauthenticated(self):
        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_unexistent_diagnostic(self):
        """
        A validation error is returned if the diagnostic does not exist
        """
        payload = {"diagnosticId": 1}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cancel_unexistent_teledeclaration(self):
        """
        A validation error is returned if the teledeclaration does not exist
        """
        payload = {"teledeclarationId": 1}
        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": 1}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_generate_pdf_unexistent_teledeclaration(self):
        """
        A validation error is returned if the teledeclaration does not exist
        """
        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_unauthorized(self):
        """
        Only managers of the canteen can create teledeclarations
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cancel_unauthorized(self):
        """
        Only managers of the canteen can cancel teledeclarations
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, manager)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_generate_pdf_unauthorized(self):
        """
        Only managers of the canteen can get PDF documents
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, manager)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_missing_diagnostic_id(self):
        """
        A validation error is returned if the diagnostic ID is missing
        """
        payload = {}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_incomplete_diagnostic(self):
        """
        A diagnostic with missing total_ht information cannot be used to
        create a teledeclaration
        """
        user = authenticate.user
        canteen = CanteenFactory.create(central_producer_siret=None)
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2020, value_total_ht=None, diagnostic_type="SIMPLE"
        )
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create(self):
        """
        A teledeclaration can be created from a valid Diagnostic
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(
            value_externality_performance_ht=0, canteen=canteen, year=2020, diagnostic_type="SIMPLE"
        )
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        teledeclaration = Teledeclaration.objects.first()

        self.assertEqual(body["teledeclaration"]["id"], teledeclaration.id)
        self.assertEqual(body["teledeclaration"]["status"], "SUBMITTED")

        self.assertEqual(teledeclaration.diagnostic, diagnostic)
        self.assertEqual(teledeclaration.canteen, canteen)
        self.assertEqual(teledeclaration.year, 2020)
        self.assertEqual(teledeclaration.applicant, user)
        self.assertEqual(teledeclaration.canteen_siret, canteen.siret)
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

        declared_data = teledeclaration.declared_data
        self.assertEqual(declared_data["year"], 2020)

        json_canteen = declared_data["canteen"]
        self.assertEqual(json_canteen["name"], canteen.name)
        self.assertEqual(json_canteen["siret"], canteen.siret)
        self.assertEqual(json_canteen["city_insee_code"], canteen.city_insee_code)

        json_teledeclaration = declared_data["teledeclaration"]
        self.assertEqual(json_teledeclaration["value_bio_ht"], diagnostic.value_bio_ht)
        self.assertEqual(
            json_teledeclaration["value_sustainable_ht"],
            diagnostic.value_sustainable_ht,
        )
        self.assertEqual(json_teledeclaration["value_total_ht"], diagnostic.value_total_ht)
        self.assertEqual(
            json_teledeclaration["value_externality_performance_ht"], diagnostic.value_externality_performance_ht
        )
        self.assertEqual(json_teledeclaration["value_egalim_others_ht"], diagnostic.value_egalim_others_ht)
        self.assertEqual(json_teledeclaration["value_meat_poultry_ht"], diagnostic.value_meat_poultry_ht)
        self.assertEqual(json_teledeclaration["value_meat_poultry_egalim_ht"], diagnostic.value_meat_poultry_egalim_ht)
        self.assertEqual(json_teledeclaration["value_meat_poultry_france_ht"], diagnostic.value_meat_poultry_france_ht)
        self.assertEqual(json_teledeclaration["value_fish_ht"], diagnostic.value_fish_ht)
        self.assertEqual(json_teledeclaration["value_fish_egalim_ht"], diagnostic.value_fish_egalim_ht)
        self.assertEqual(
            json_teledeclaration["has_waste_diagnostic"],
            diagnostic.has_waste_diagnostic,
        )
        self.assertEqual(json_teledeclaration["has_waste_plan"], diagnostic.has_waste_plan)
        self.assertEqual(
            json_teledeclaration["has_donation_agreement"],
            diagnostic.has_donation_agreement,
        )
        self.assertEqual(json_teledeclaration["has_waste_measures"], diagnostic.has_waste_measures)
        self.assertEqual(
            json_teledeclaration["has_diversification_plan"],
            diagnostic.has_diversification_plan,
        )
        self.assertEqual(
            json_teledeclaration["cooking_plastic_substituted"],
            diagnostic.cooking_plastic_substituted,
        )
        self.assertEqual(
            json_teledeclaration["serving_plastic_substituted"],
            diagnostic.serving_plastic_substituted,
        )
        self.assertEqual(
            json_teledeclaration["plastic_bottles_substituted"],
            diagnostic.plastic_bottles_substituted,
        )
        self.assertEqual(
            json_teledeclaration["plastic_tableware_substituted"],
            diagnostic.plastic_tableware_substituted,
        )
        self.assertEqual(
            json_teledeclaration["communicates_on_food_plan"],
            diagnostic.communicates_on_food_plan,
        )
        self.assertEqual(
            json_teledeclaration["communicates_on_food_quality"],
            diagnostic.communicates_on_food_quality,
        )

    @authenticate
    def test_cancel(self):
        """
        A submitted teledeclaration can be cancelled
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, user)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED)

        body = response.json()
        self.assertIsNone(body["teledeclaration"])

    @authenticate
    def test_generate_pdf(self):
        """
        The user can get a justificatif in PDF for a teledeclaration
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_generate_pdf_legacy_teledeclaration(self):
        """
        The user can get a justificatif in PDF for a teledeclaration
        with minimal information
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2021, diagnostic_type=None)
        teledeclaration = TeledeclarationFactory(
            canteen=canteen,
            diagnostic=diagnostic,
            year=2021,
            declared_data={
                "year": 2021,
                "canteen": {
                    "name": "",
                },
                "applicant": {
                    "name": "",
                },
                "teledeclaration": {},
            },
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
        )

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_create_duplicate(self):
        """
        We can only have one submitted teledeclaration per canteen/year
        """
        user = authenticate.user
        canteen = CanteenFactory.create(siret="12345678912345")
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        Teledeclaration.create_from_diagnostic(diagnostic, user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_no_siret(self):
        """
        A few canteens don't have SIRETs - make sure teledeclarations for
        different canteens with no SIRET aren't flagged as duplicates
        """
        user = authenticate.user
        canteen = CanteenFactory.create(siret="")
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        Teledeclaration.create_from_diagnostic(diagnostic, user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        canteen2 = CanteenFactory.create(siret="")
        canteen2.managers.add(user)
        diagnostic2 = DiagnosticFactory.create(canteen=canteen2, year=2020)

        payload = {"diagnosticId": diagnostic2.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @authenticate
    def test_complete_diagnostic(self):
        """
        When doing a TD with a complete diagnostic, the adequate fields must be
        present in the teledeclaration
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="COMPLETE")
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        teledeclaration = Teledeclaration.objects.first()

        self.assertEqual(body["teledeclaration"]["id"], teledeclaration.id)
        self.assertEqual(body["teledeclaration"]["status"], "SUBMITTED")

        self.assertEqual(teledeclaration.diagnostic, diagnostic)
        self.assertEqual(teledeclaration.canteen, canteen)
        self.assertEqual(teledeclaration.year, 2020)
        self.assertEqual(teledeclaration.applicant, user)
        self.assertEqual(teledeclaration.canteen_siret, canteen.siret)
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

        declared_data = teledeclaration.declared_data
        self.assertEqual(declared_data["year"], 2020)

        json_canteen = declared_data["canteen"]
        self.assertEqual(json_canteen["name"], canteen.name)
        self.assertEqual(json_canteen["siret"], canteen.siret)
        self.assertEqual(json_canteen["city_insee_code"], canteen.city_insee_code)

        json_teledeclaration = declared_data["teledeclaration"]

        # Fields pertaining to the simplified declaration should not be present
        self.assertNotIn("value_bio_ht", json_teledeclaration)
        self.assertNotIn("value_sustainable_ht", json_teledeclaration)

        # Fields pertaining to the complete declaration should be in the payload
        self.assertIn("value_fruits_et_legumes_bio", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_label_rouge", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_aocaop_igp_stg", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_hve", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_peche_durable", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_rup", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_fermier", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_externalites", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_commerce_equitable", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_performance", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_non_egalim", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_france", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_short_distribution", json_teledeclaration)
        self.assertIn("value_fruits_et_legumes_local", json_teledeclaration)

    @authenticate
    def test_create_incomplete_diagnostic_central_kitchen(self):
        """
        A diagnostic without total value HT can be teledeclared if a central kitchen
        gave the details.
        """
        user = authenticate.user
        central_kitchen = CanteenFactory.create(production_type="central", siret="79300704800044")
        canteen = CanteenFactory.create(
            production_type="site_cooked_elsewhere", central_producer_siret="79300704800044"
        )
        canteen.managers.add(user)

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=100,
            diagnostic_type="SIMPLE",
            central_kitchen_diagnostic_mode="APPRO",
        )

        diagnostic = DiagnosticFactory.create(
            canteen=canteen,
            year=2020,
            value_total_ht=None,
            diagnostic_type="SIMPLE",
        )
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        self.assertTrue(teledeclaration.uses_central_kitchen_appro)
