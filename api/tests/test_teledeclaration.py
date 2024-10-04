import datetime
import zoneinfo
from unittest.mock import patch

from django.db.utils import IntegrityError
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    SectorFactory,
    TeledeclarationFactory,
    UserFactory,
)
from data.models import Canteen, Diagnostic, Teledeclaration

from .utils import authenticate

LAST_YEAR = datetime.date.today().year - 1


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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_create_unexistent_diagnostic(self):
        """
        A permission error is returned if the diagnostic does not exist
        So that can't find out if diagnostics exist
        """
        payload = {"diagnosticId": 1}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_cancel_unexistent_teledeclaration(self):
        """
        A validation error is returned if the teledeclaration does not exist
        """
        payload = {"teledeclarationId": 1}
        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": 1}), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_generate_pdf_unexistent_teledeclaration(self):
        """
        A validation error is returned if the teledeclaration does not exist
        """
        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ENABLE_TELEDECLARATION=True)
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

        with patch.object(
            timezone,
            "now",
            return_value=datetime.datetime(2021, 4, 1, 11, 00, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        ):
            response = self.client.post(reverse("teledeclaration_create"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ENABLE_TELEDECLARATION=True)
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

    @override_settings(ENABLE_TELEDECLARATION=True)
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_create_missing_diagnostic_id(self):
        """
        A validation error is returned if the diagnostic ID is missing
        """
        payload = {}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ENABLE_TELEDECLARATION=True)
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

        with patch.object(
            timezone,
            "now",
            return_value=datetime.datetime(2021, 4, 1, 11, 00, tzinfo=zoneinfo.ZoneInfo("Europe/Paris")),
        ):
            response = self.client.post(reverse("teledeclaration_create"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2021-01-20")
    @authenticate
    def test_create_bad_year(self):
        """
        A diagnostic with a bad year cannot be used to create a teledeclaration
        """
        user = authenticate.user
        canteen = CanteenFactory.create(central_producer_siret=None)
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2019, value_total_ht=100, diagnostic_type="SIMPLE")
        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2021-01-20")
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

    @override_settings(ENABLE_TELEDECLARATION=False)
    @freeze_time("2021-01-20")
    @authenticate
    def test_create_out_of_campaign(self):
        """
        A teledeclaration cannot be created out of a TD campaign
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(
            value_externality_performance_ht=0, canteen=canteen, year=2020, diagnostic_type="SIMPLE"
        )
        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2021-01-14")
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @freeze_time("2023-01-14")
    @authenticate
    def test_cancel_previous_year(self):
        """
        A submitted teledeclaration cannot be cancelled for a previous campaign
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2021, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, user)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

    @override_settings(ENABLE_TELEDECLARATION=False)
    @freeze_time("2023-01-14")
    @authenticate
    def test_cancel_out_of_campaign(self):
        """
        A submitted teledeclaration cannot be cancelled after the campaign
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2022, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, user)

        response = self.client.post(reverse("teledeclaration_cancel", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_diagnostic_deletion(self):
        """
        If the diagnostic used for the teledeclaration is deleted, the teledeclaration
        should be cancelled
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        diagnostic.delete()
        teledeclaration.refresh_from_db()
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED)
        self.assertIsNone(teledeclaration.diagnostic)

    @override_settings(ENABLE_TELEDECLARATION=True)
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

    @override_settings(ENABLE_TELEDECLARATION=True)
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_generate_pdf_central(self):
        """
        A central kitchen should be able to generate a PDF
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, daily_meal_count=345)
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, diagnostic_type="SIMPLE")
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)
        self.assertIsNone(teledeclaration.declared_data["canteen"]["daily_meal_count"])

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_create_duplicate(self):
        """
        We can only have one submitted teledeclaration per canteen/year
        """
        user = authenticate.user
        canteen = CanteenFactory.create(siret="12345678912345")
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=LAST_YEAR, diagnostic_type="SIMPLE")
        Teledeclaration.create_from_diagnostic(diagnostic, user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_no_siret(self):
        """
        A few canteens don't have SIRETs - make sure teledeclarations for
        different canteens with no SIRET aren't flagged as duplicates
        """
        user = authenticate.user
        canteen = CanteenFactory.create(siret="")
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=LAST_YEAR, diagnostic_type="SIMPLE")
        Teledeclaration.create_from_diagnostic(diagnostic, user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        canteen2 = CanteenFactory.create(siret="")
        canteen2.managers.add(user)
        diagnostic2 = DiagnosticFactory.create(canteen=canteen2, year=LAST_YEAR)

        payload = {"diagnosticId": diagnostic2.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_complete_diagnostic(self):
        """
        When doing a TD with a complete diagnostic, the adequate fields must be
        present in the teledeclaration
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=LAST_YEAR, diagnostic_type="COMPLETE")
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        teledeclaration = Teledeclaration.objects.first()

        self.assertEqual(body["teledeclaration"]["id"], teledeclaration.id)
        self.assertEqual(body["teledeclaration"]["status"], "SUBMITTED")

        self.assertEqual(teledeclaration.diagnostic, diagnostic)
        self.assertEqual(teledeclaration.canteen, canteen)
        self.assertEqual(teledeclaration.year, LAST_YEAR)
        self.assertEqual(teledeclaration.applicant, user)
        self.assertEqual(teledeclaration.canteen_siret, canteen.siret)
        self.assertEqual(teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED)

        declared_data = teledeclaration.declared_data
        self.assertEqual(declared_data["year"], LAST_YEAR)

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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_create_incomplete_diagnostic_central_kitchen(self):
        """
        A diagnostic without total value HT can be teledeclared if a central kitchen
        gave the details.
        """
        user = authenticate.user
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="79300704800044")
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="79300704800044"
        )
        canteen.managers.add(user)

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=LAST_YEAR,
            value_total_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        diagnostic = DiagnosticFactory.create(
            canteen=canteen,
            year=LAST_YEAR,
            value_total_ht=None,
            diagnostic_type=None,
        )
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        self.assertEqual(
            teledeclaration.teledeclaration_mode, Teledeclaration.TeledeclarationMode.SATELLITE_WITHOUT_APPRO
        )

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_central_kitchen_contains_satellites(self):
        """
        A diagnostic from a central kitchen must contain the satellites added at that moment
        """
        user = authenticate.user
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, siret="79300704800044", satellite_canteens_count=3
        )
        satellite_1 = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="79300704800044"
        )
        satellite_2 = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="79300704800044"
        )
        central_kitchen.managers.add(user)

        diagnostic = DiagnosticFactory.create(
            canteen=central_kitchen,
            year=LAST_YEAR,
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_create_diagnostic_without_cc_mode(self):
        """
        A diagnostic made by a central kitchen cannot be teledeclared if the mode is null or blank
        """
        user = authenticate.user
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="79300704800044")
        central_kitchen.managers.add(user)

        diagnostic = DiagnosticFactory.create(
            canteen=central_kitchen,
            year=LAST_YEAR,
            value_total_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=None,
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

    @override_settings(ENABLE_TELEDECLARATION=True)
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
        )
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=LAST_YEAR, value_total_ht=100, central_kitchen_diagnostic_mode="ALL"
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
        self.assertIsNone(canteen_json["daily_meal_count"])
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_calculate_teledeclaration_mode(self):
        """
        The teledeclaration mode is automatically calculated based on production type and
        diagnostic mode
        """
        central = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL_SERVING, siret="18704793618411")
        DiagnosticFactory.create(
            canteen=central,
            year=LAST_YEAR,
            value_total_ht=100,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        ),
        cases = [
            {
                "canteen": CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, siret="79300704800044"),
                "diagnostic": DiagnosticFactory.create(year=LAST_YEAR, value_total_ht=100),
                "expected_teledeclaration_mode": "SITE",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.ON_SITE_CENTRAL, siret="79300704800044"
                ),
                "diagnostic": DiagnosticFactory.create(year=LAST_YEAR, value_total_ht=100),
                "expected_teledeclaration_mode": "SITE",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                    siret="79300704800044",
                    central_producer_siret="18704793618411",
                ),
                "diagnostic": DiagnosticFactory.create(year=LAST_YEAR),
                "expected_teledeclaration_mode": "SATELLITE_WITHOUT_APPRO",
            },
            {
                "canteen": CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, siret="79300704800044"),
                "diagnostic": DiagnosticFactory.create(
                    year=LAST_YEAR,
                    value_total_ht=100,
                    central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
                ),
                "expected_teledeclaration_mode": "CENTRAL_ALL",
            },
            {
                "canteen": CanteenFactory(
                    production_type=Canteen.ProductionType.CENTRAL_SERVING, siret="79300704800044"
                ),
                "diagnostic": DiagnosticFactory.create(
                    year=LAST_YEAR,
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

            canteen.managers.add(authenticate.user)
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_dynamically_include_line_ministry(self):
        sector_ministry = SectorFactory.create(has_line_ministry=True)
        sector_other = SectorFactory.create(has_line_ministry=False)
        canteen = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
            siret="79300704800044",
            satellite_canteens_count=3,
            sectors=[sector_other],
            line_ministry="affaires_etrangeres",
        )
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(
            canteen=canteen,
            year=LAST_YEAR,
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

        canteen.sectors.add(sector_ministry)
        canteen.save()
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        teledeclaration = Teledeclaration.objects.get(diagnostic=diagnostic)
        canteen_json = teledeclaration.declared_data.get("canteen")
        self.assertEqual(canteen_json["line_ministry"], "affaires_etrangeres")

    def test_one_submitted_td_constraint(self):
        """
        Only one TD per canteen and per year can be submitted
        """
        # Doesn't use the TeledeclarationFactory to escape the `clean` function validation
        # bulk_create does not pass through the `save` method, so it allows us to test the
        # actual constraint.
        canteen = CanteenFactory.create()
        diagnostic = DiagnosticFactory.create(canteen=canteen)
        applicant = UserFactory.create()
        teledeclaration_1 = Teledeclaration(
            canteen=canteen,
            year=LAST_YEAR,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        teledeclaration_2 = Teledeclaration(
            canteen=canteen,
            year=LAST_YEAR,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        with self.assertRaises(IntegrityError):
            Teledeclaration.objects.bulk_create([teledeclaration_1, teledeclaration_2])

    def test_several_cancelled_td_constraint(self):
        """
        Cancelled TDs should not influence the constraint
        """
        # Doesn't use the TeledeclarationFactory to escape the `clean` function validation
        # bulk_create does not pass through the `save` method, so it allows us to test the
        # actual constraint.
        canteen = CanteenFactory.create()
        diagnostic = DiagnosticFactory.create(canteen=canteen)
        applicant = UserFactory.create()
        teledeclaration_1 = Teledeclaration(
            canteen=canteen,
            year=LAST_YEAR,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.CANCELLED,
            declared_data={"foo": 1},
        )
        teledeclaration_2 = Teledeclaration(
            canteen=canteen,
            year=LAST_YEAR,
            diagnostic=diagnostic,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        try:
            Teledeclaration.objects.bulk_create([teledeclaration_1, teledeclaration_2])
        except IntegrityError:
            self.fail("Should be able to create a submitted TD if a cancelled one exists already")

    def test_bypass_constraint_if_no_canteen(self):
        """
        A TD that does not have a canteen attached to it (e.g., for deleted canteens) should not be
        considered in the constraint.
        """
        # Doesn't use the TeledeclarationFactory to escape the `clean` function validation
        # bulk_create does not pass through the `save` method, so it allows us to test the
        # actual constraint.
        applicant = UserFactory.create()
        teledeclaration_1 = Teledeclaration(
            canteen=None,
            year=LAST_YEAR,
            diagnostic=None,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        teledeclaration_2 = Teledeclaration(
            canteen=None,
            year=LAST_YEAR,
            diagnostic=None,
            applicant=applicant,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            declared_data={"foo": 1},
        )
        try:
            Teledeclaration.objects.bulk_create([teledeclaration_1, teledeclaration_2])
        except IntegrityError:
            self.fail("Should be able to have several submitted TDs for deleted canteens")
