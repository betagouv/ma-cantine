from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers.teledeclaration import TeledeclarationAnalysisSerializer
from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    SectorFactory,
    TeledeclarationFactory,
    UserFactory,
)
from data.models import Canteen, Diagnostic, Teledeclaration

from .utils import authenticate


class TestTeledeclarationCreateApi(APITestCase):
    def test_create_unauthenticated(self):
        """
        The creation of a teledeclaration is only available
        to authenticated users
        """
        payload = {"diagnosticId": 1}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_unexistent_diagnostic(self):
        """
        A permission error is returned if the diagnostic does not exist
        So that can't find out if diagnostics exist
        """
        payload = {"diagnosticId": 1}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_create_unauthorized(self):
        """
        Only managers of the canteen can create teledeclarations
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_missing_diagnostic_id(self):
        """
        A validation error is returned if the diagnostic ID is missing
        """
        payload = {}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_create_incomplete_diagnostic(self):
        """
        A diagnostic with missing total_ht information cannot be used to
        create a teledeclaration
        """
        canteen = CanteenFactory.create(central_producer_siret=None, managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, value_total_ht=None, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_create_bad_year(self):
        """
        A diagnostic with a bad year cannot be used to create a teledeclaration
        """
        canteen = CanteenFactory.create(central_producer_siret=None, managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2019, value_total_ht=100, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_create_during_campaign(self):
        """
        A teledeclaration can be created from a valid Diagnostic
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            value_externality_performance_ht=0,
            canteen=canteen,
            year=2021,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            value_bio_ht=20,
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
        self.assertEqual(teledeclaration.year, 2021)
        self.assertEqual(teledeclaration.applicant, authenticate.user)
        self.assertEqual(teledeclaration.canteen_siret, canteen.siret)
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

        declared_data = teledeclaration.declared_data
        self.assertEqual(declared_data["year"], 2021)

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
        self.assertEqual(json_teledeclaration["total_leftovers"], diagnostic.total_leftovers)
        self.assertEqual(
            json_teledeclaration["duration_leftovers_measurement"], diagnostic.duration_leftovers_measurement
        )
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
        # Test the aggregated values, as it is a SIMPLE diag, the value should match directly the non agg ones
        self.assertEqual(teledeclaration.value_bio_ht_agg, diagnostic.value_bio_ht)

    @freeze_time("2022-12-25")  # after the 2021 campaign
    @authenticate
    def test_create_after_the_campaign(self):
        """
        A teledeclaration cannot be created after the campaign
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            value_externality_performance_ht=0,
            canteen=canteen,
            year=2021,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_during_the_correction_campaign(self):
        """
        A teledeclaration can be created during the correction campaign
        ONLY if a teledeclaration was already created during the campaign
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            value_externality_performance_ht=0,
            canteen=canteen,
            year=2024,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        # no teledeclaration created during the campaign
        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            payload = {"diagnosticId": diagnostic.id}
            response = self.client.post(reverse("teledeclaration_create"), payload)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # submit a teledeclaration during the campaign
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        # teledeclaration created during the campaign
        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            # first cancel the teledeclaration (correction)
            response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # then re-submit it
            payload = {"diagnosticId": diagnostic.id}
            response = self.client.post(reverse("teledeclaration_create"), payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_create_duplicate(self):
        """
        We can only have one submitted teledeclaration per canteen per year
        """
        canteen = CanteenFactory.create(siret="12345678912345", managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "Il existe déjà une télédéclaration en cours pour cette année")

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_canteen_with_no_siret(self):
        """
        A few canteens don't have SIRETs - make sure teledeclarations for
        different canteens with no SIRET aren't flagged as duplicates
        """
        canteen = CanteenFactory.create(siret="", managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        canteen2 = CanteenFactory.create(siret="", managers=[authenticate.user])
        diagnostic2 = DiagnosticFactory.create(canteen=canteen2, year=2021)

        payload = {"diagnosticId": diagnostic2.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_complete_diagnostic(self):
        """
        When doing a TD with a complete diagnostic, the adequate fields must be
        present in the teledeclaration
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
            value_total_ht=1000,
            value_sustainable_ht=None,
        )
        # Making sure we will aggregate
        diagnostic.value_sustainable_ht = None
        diagnostic.value_boissons_label_rouge = 10
        diagnostic.value_boulangerie_aocaop_igp_stg = 10
        diagnostic.save()
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        teledeclaration = Teledeclaration.objects.first()

        self.assertEqual(body["teledeclaration"]["id"], teledeclaration.id)
        self.assertEqual(body["teledeclaration"]["status"], "SUBMITTED")

        self.assertEqual(teledeclaration.diagnostic, diagnostic)
        self.assertEqual(teledeclaration.canteen, canteen)
        self.assertEqual(teledeclaration.year, 2021)
        self.assertEqual(teledeclaration.applicant, authenticate.user)
        self.assertEqual(teledeclaration.canteen_siret, canteen.siret)
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

        declared_data = teledeclaration.declared_data
        self.assertEqual(declared_data["year"], 2021)

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

        # Checking the aggregation
        self.assertEqual(teledeclaration.value_total_ht, 1000)
        self.assertIsNone(teledeclaration.value_bio_ht_agg)
        self.assertEqual(
            teledeclaration.value_sustainable_ht_agg,
            json_teledeclaration["value_boissons_label_rouge"]
            + json_teledeclaration["value_boulangerie_aocaop_igp_stg"],
        )

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_central_kitchen_incomplete_diagnostic(self):
        """
        A diagnostic without total value HT can be teledeclared if a central kitchen
        gave the details.
        """
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="79300704800044")
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="79300704800044",
            managers=[authenticate.user],
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2021,
            value_total_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        diagnostic = DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            value_total_ht=None,  # missing
            diagnostic_type=None,
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        self.assertEqual(
            teledeclaration.teledeclaration_mode, Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        )

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_central_kitchen_contains_satellites(self):
        """
        A diagnostic from a central kitchen must contain the satellites added at that moment
        """
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            siret="79300704800044",
            satellite_canteens_count=3,
            managers=[authenticate.user],
        )
        satellite_1 = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="79300704800044"
        )
        satellite_2 = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="79300704800044"
        )

        diagnostic = DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2021,
            value_total_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        data = teledeclaration.declared_data
        self.assertEqual(len(data.get("satellites")), 2)
        self.assertEqual(data.get("satellite_canteens_count"), 3)

        satellite_1_data = next(filter(lambda x: x["id"] == satellite_1.id, data["satellites"]), None)
        satellite_2_data = next(filter(lambda x: x["id"] == satellite_2.id, data["satellites"]), None)

        self.assertIsNotNone(satellite_1_data)
        self.assertIsNotNone(satellite_2_data)

        self.assertEqual(satellite_1_data["name"], satellite_1.name)
        self.assertEqual(satellite_1_data["siret"], satellite_1.siret)

        self.assertEqual(satellite_2_data["name"], satellite_2.name)
        self.assertEqual(satellite_2_data["siret"], satellite_2.siret)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_central_kitchen_without_cc_mode(self):
        """
        A diagnostic made by a central kitchen cannot be teledeclared if the mode is null or blank
        """
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, siret="79300704800044", managers=[authenticate.user]
        )

        diagnostic = DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2021,
            value_total_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=None,  # missing
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        diagnostic.central_kitchen_diagnostic_mode = ""
        diagnostic.save()
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        diagnostic.central_kitchen_diagnostic_mode = "APPRO"
        diagnostic.save()
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_does_not_contain_irrelevant_data(self):
        # We create a site canteen that contains irrelevant data "central_producer_siret" and
        # "satellite_canteens_count" - this can happen after a change of data
        canteen = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
            siret="79300704800044",
            satellite_canteens_count=3,
            central_producer_siret="18704793618411",
            daily_meal_count=10,
            managers=[authenticate.user],
        )
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, value_total_ht=100, central_kitchen_diagnostic_mode="ALL"
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        canteen_json = teledeclaration.declared_data.get("canteen")
        self.assertIsNone(canteen_json["satellite_canteens_count"])
        self.assertIsNone(canteen_json["central_producer_siret"])
        self.assertIsNone(teledeclaration.declared_data["central_kitchen_siret"])
        self.assertEqual(canteen_json["daily_meal_count"], 10)
        self.assertEqual(teledeclaration.teledeclaration_mode, "SITE")

        # If we change its type to cuisine centrale we should get the satellite count and mode
        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic).delete()

        canteen.production_type = Canteen.ProductionType.CENTRAL
        canteen.save()
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        canteen_json = teledeclaration.declared_data.get("canteen")
        self.assertEqual(canteen_json["satellite_canteens_count"], 3)
        self.assertIsNone(canteen_json["central_producer_siret"])
        self.assertIsNone(teledeclaration.declared_data["central_kitchen_siret"])
        self.assertEqual(teledeclaration.teledeclaration_mode, "CENTRAL_ALL")

        # If we change its type to satellite we should get the central_producer_siret
        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic).delete()

        canteen.production_type = Canteen.ProductionType.ON_SITE_CENTRAL
        canteen.save()
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        canteen_json = teledeclaration.declared_data.get("canteen")
        self.assertIsNone(canteen_json["satellite_canteens_count"])
        self.assertEqual(canteen_json["central_producer_siret"], "18704793618411")
        self.assertEqual(teledeclaration.declared_data["central_kitchen_siret"], "18704793618411")
        self.assertEqual(canteen_json["daily_meal_count"], 10)
        self.assertEqual(teledeclaration.teledeclaration_mode, "SITE")

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_calculate_teledeclaration_mode(self):
        """
        The teledeclaration mode is automatically calculated based on production type and
        diagnostic mode
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL_SERVING, siret="18704793618411")
        DiagnosticFactory.create(
            canteen=central,
            year=2021,
            value_total_ht=100,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        ),
        cases = [
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.ON_SITE,
                    siret="79300704800044",
                    managers=[authenticate.user],
                ),
                "diagnostic": DiagnosticFactory.create(year=2021, value_total_ht=100),
                "expected_teledeclaration_mode": "SITE",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                    siret="79300704800044",
                    managers=[authenticate.user],
                ),
                "diagnostic": DiagnosticFactory.create(year=2021, value_total_ht=100),
                "expected_teledeclaration_mode": "SITE",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                    siret="79300704800044",
                    central_producer_siret="18704793618411",
                    managers=[authenticate.user],
                ),
                "diagnostic": DiagnosticFactory.create(year=2021),
                "expected_teledeclaration_mode": "SATELLITE_WITHOUT_APPRO",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.CENTRAL,
                    siret="79300704800044",
                    managers=[authenticate.user],
                ),
                "diagnostic": DiagnosticFactory.create(
                    year=2021,
                    value_total_ht=100,
                    central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                ),
                "expected_teledeclaration_mode": "CENTRAL_ALL",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.CENTRAL_SERVING,
                    siret="79300704800044",
                    managers=[authenticate.user],
                ),
                "diagnostic": DiagnosticFactory.create(
                    year=2021,
                    value_total_ht=100,
                    central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
                ),
                "expected_teledeclaration_mode": "CENTRAL_APPRO",
            },
        ]
        for case in cases:
            canteen = case["canteen"]
            diagnostic = case["diagnostic"]
            expected_td_mode = case["expected_teledeclaration_mode"]
            diagnostic.canteen = canteen
            diagnostic.save()

            payload = {"diagnosticId": diagnostic.id}
            self.client.post(reverse("teledeclaration_create"), payload)

            teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
            self.assertEqual(
                teledeclaration.teledeclaration_mode,
                expected_td_mode,
                f"Incorrect mode for canteen with prod type {canteen.production_type}",
            )

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_line_ministry_does_not_depend_on_sector_anymore(self):
        sector_ministry = SectorFactory.create(has_line_ministry=True)
        canteen = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
            siret="79300704800044",
            satellite_canteens_count=3,
            sectors=[sector_ministry],
            line_ministry=None,
            managers=[authenticate.user],
        )
        diagnostic = DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            value_total_ht=100,
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        canteen_json = teledeclaration.declared_data.get("canteen")
        self.assertIsNone(canteen_json["line_ministry"])

        # If we add the sector_ministry we should have the line_ministry in the canteen
        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic).delete()

        canteen.line_ministry = Canteen.Ministries.AFFAIRES_ETRANGERES
        canteen.save()
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        canteen_json = teledeclaration.declared_data.get("canteen")
        self.assertEqual(canteen_json["line_ministry"], "affaires_etrangeres")


class TestTeledeclarationCancel(APITestCase):
    def test_cancel_unauthenticated(self):
        payload = {"teledeclarationId": 1}
        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": 1}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cancel_unexistent_teledeclaration(self):
        """
        A validation error is returned if the teledeclaration does not exist
        """
        payload = {"teledeclarationId": 1}
        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": 1}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cancel_unauthorized(self):
        """
        Only managers of the canteen can cancel teledeclarations
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, manager)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_cancel_during_campaign(self):
        """
        A submitted teledeclaration can be cancelled
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED)

        body = response.json()
        self.assertIsNone(body["teledeclaration"])

    @freeze_time("2023-03-30")  # during the 2022 campaign
    @authenticate
    def test_cancel_previous_year(self):
        """
        A submitted teledeclaration cannot be cancelled for a previous campaign
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

    @freeze_time("2022-12-25")  # after the 2021 campaign
    @authenticate
    def test_cancel_after_the_campaign(self):
        """
        A submitted teledeclaration cannot be cancelled after the campaign
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

    @authenticate
    def test_cancel_during_correction_campaign(self):
        """
        A submitted teledeclaration can be cancelled during the correction campaign
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
            self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED)

            body = response.json()
            self.assertIsNone(body["teledeclaration"])


class TestTeledeclarationPdfApi(APITestCase):
    def test_generate_pdf_unauthenticated(self):
        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_generate_pdf_unexistent_teledeclaration(self):
        """
        A validation error is returned if the teledeclaration does not exist
        """
        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_generate_pdf_unauthorized(self):
        """
        Only managers of the canteen can get PDF documents
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, manager)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_generate_pdf(self):
        """
        The user can get a justificatif in PDF for a teledeclaration
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2023-03-30")  # during the 2022 campaign
    @authenticate
    def test_generate_pdf_legacy_teledeclaration(self):
        """
        The user can get a justificatif in PDF for a teledeclaration
        with minimal information
        """
        canteen = CanteenFactory.create(managers=[authenticate.user])
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

    @freeze_time("2022-12-25")  # after the 2021 campaign
    @authenticate
    def test_generate_pdf_central(self):
        """
        A central kitchen should be able to generate a PDF
        """
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, daily_meal_count=345, managers=[authenticate.user]
        )
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTeledeclarationCampaignDatesApi(APITestCase):
    def test_campaign_dates_list(self):
        response = self.client.get(reverse("list_teledeclaration_campaign_dates"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body), 4)
        self.assertEqual(body[-1]["year"], 2024)

    def test_campaign_dates_retrieve(self):
        for date_freeze in [
            {"date": "2025-01-01", "in_teledeclaration": False, "in_correction": False},
            {"date": "2025-02-28", "in_teledeclaration": True, "in_correction": False},
            {"date": "2025-04-20", "in_teledeclaration": False, "in_correction": True},
        ]:
            with self.subTest(DATE=date_freeze["date"]):
                with freeze_time(date_freeze["date"]):
                    response = self.client.get(
                        reverse("retrieve_teledeclaration_campaign_dates", kwargs={"year": 2024})
                    )
                    self.assertEqual(response.status_code, status.HTTP_200_OK)

                    body = response.json()
                    self.assertEqual(body["year"], 2024)
                    self.assertEqual(body["inTeledeclaration"], date_freeze["in_teledeclaration"])
                    self.assertEqual(body["inCorrection"], date_freeze["in_correction"])


class TeledeclarationAnalysisSerializerTest(APITestCase):
    def test_get_diagnostic_type_with_valid_data(self):
        declared_data = {
            "teledeclaration": {
                "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
            }
        }
        teledeclaration = Teledeclaration(declared_data=declared_data)
        serializer = TeledeclarationAnalysisSerializer(instance=teledeclaration)
        self.assertEqual(serializer.get_diagnostic_type(teledeclaration), Diagnostic.DiagnosticType.SIMPLE)

    def test_get_diagnostic_type_with_empty_string(self):
        declared_data = {
            "teledeclaration": {
                "diagnostic_type": "",
            }
        }
        teledeclaration = Teledeclaration(declared_data=declared_data)
        serializer = TeledeclarationAnalysisSerializer(instance=teledeclaration)
        self.assertEqual(serializer.get_diagnostic_type(teledeclaration), Diagnostic.DiagnosticType.SIMPLE)

    def test_get_diagnostic_type_with_missing_key(self):
        declared_data = {"teledeclaration": {}}
        teledeclaration = Teledeclaration(declared_data=declared_data)
        serializer = TeledeclarationAnalysisSerializer(instance=teledeclaration)
        self.assertIsNone(serializer.get_diagnostic_type(teledeclaration))

    def test_get_diagnostic_type_with_none(self):
        declared_data = {
            "teledeclaration": {
                "diagnostic_type": None,
            }
        }
        teledeclaration = Teledeclaration(declared_data=declared_data)
        serializer = TeledeclarationAnalysisSerializer(instance=teledeclaration)
        self.assertEqual(serializer.get_diagnostic_type(teledeclaration), Diagnostic.DiagnosticType.SIMPLE)

    def test_get_actions_gaspi(self):
        all_actions = [choice for choice, _ in Diagnostic.WasteActions.choices]
        test_cases = [
            (None, {action: False for action in all_actions}),
            ([], {action: False for action in all_actions}),
            (
                [Diagnostic.WasteActions.INSCRIPTION],
                {action: action == Diagnostic.WasteActions.INSCRIPTION for action in all_actions},
            ),
            (
                [Diagnostic.WasteActions.AWARENESS, Diagnostic.WasteActions.DISTRIBUTION],
                {
                    action: action in [Diagnostic.WasteActions.AWARENESS, Diagnostic.WasteActions.DISTRIBUTION]
                    for action in all_actions
                },
            ),
            (all_actions, {action: True for action in all_actions}),
        ]
        for actions_list, expected in test_cases:
            teledeclaration = Teledeclaration(declared_data={"teledeclaration": {"waste_actions": actions_list}})
            serializer = TeledeclarationAnalysisSerializer(instance=teledeclaration)
            self.assertEqual(
                serializer.get_action_gaspi_inscription(teledeclaration),
                expected[Diagnostic.WasteActions.INSCRIPTION],
                msg=f"Failed for input: {actions_list}",
            )
            self.assertEqual(
                serializer.get_action_gaspi_sensibilisation(teledeclaration),
                expected[Diagnostic.WasteActions.AWARENESS],
                msg=f"Failed for input: {actions_list}",
            )
            self.assertEqual(
                serializer.get_action_gaspi_formation(teledeclaration),
                expected[Diagnostic.WasteActions.TRAINING],
                msg=f"Failed for input: {actions_list}",
            )
            self.assertEqual(
                serializer.get_action_gaspi_distribution(teledeclaration),
                expected[Diagnostic.WasteActions.DISTRIBUTION],
                msg=f"Failed for input: {actions_list}",
            )
            self.assertEqual(
                serializer.get_action_gaspi_portions(teledeclaration),
                expected[Diagnostic.WasteActions.PORTIONS],
                msg=f"Failed for input: {actions_list}",
            )
            self.assertEqual(
                serializer.get_action_gaspi_reutilisation(teledeclaration),
                expected[Diagnostic.WasteActions.REUSE],
                msg=f"Failed for input: {actions_list}",
            )
