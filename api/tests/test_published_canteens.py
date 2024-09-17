import os

from django.core.files import File
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    TeledeclarationFactory,
    UserFactory,
)
from data.models import Canteen, CanteenImage, Diagnostic, Teledeclaration

from .utils import authenticate

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


@override_settings(PUBLISH_BY_DEFAULT=False)
class TestPublishedCanteenApi(APITestCase):
    @authenticate
    def test_canteen_publication_fields_read_only(self):
        """
        Users cannot modify canteen publication status with this endpoint
        """
        canteen = CanteenFactory.create(city="Paris")
        canteen.managers.add(authenticate.user)
        payload = {
            "publication_status": "published",
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, Canteen.PublicationStatus.DRAFT.value)

    def test_get_single_published_canteen(self):
        """
        We are able to get a single published canteen.
        """
        published_canteen = CanteenFactory.create(publication_status="published")
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": published_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("id"), published_canteen.id)

    def test_get_single_unpublished_canteen(self):
        """
        A 404 is raised if we try to get a sinlge published canteen
        that has not been published by the manager.
        """
        private_canteen = CanteenFactory.create(publication_status="draft")
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": private_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_badges_in_single_published_canteen(self):
        """
        Expect to get badge info in response
        """
        published_canteen = CanteenFactory.create(publication_status="published")
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": published_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("badges", body)

    @authenticate
    def test_canteen_image_serialization(self):
        """
        A canteen with images should serialize those images
        """
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        image_names = [
            "test-image-1.jpg",
            "test-image-2.jpg",
            "test-image-3.png",
        ]
        for image_name in image_names:
            path = os.path.join(CURRENT_DIR, f"files/{image_name}")
            with open(path, "rb") as image:
                file = File(image)
                file.name = image_name
                canteen_image = CanteenImage(image=file)
                canteen_image.canteen = canteen
                canteen_image.save()

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body.get("images")), 3)

    def test_satellite_published(self):
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            publication_status="published",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        diagnostic = DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(body.get("id"), satellite.id)
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        self.assertEqual(body.get("centralKitchen").get("id"), central_kitchen.id)

        serialized_diagnostic = body.get("approDiagnostics")[0]
        self.assertEqual(serialized_diagnostic["id"], diagnostic.id)
        self.assertEqual(serialized_diagnostic["percentageValueTotalHt"], 1)
        self.assertEqual(serialized_diagnostic["percentageValueBioHt"], 0.5)

    def test_satellite_published_without_bio(self):
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            publication_status="published",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        diagnostic = DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=None,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(body.get("id"), satellite.id)
        self.assertEqual(len(body.get("approDiagnostics")), 1)

        serialized_diagnostic = body.get("approDiagnostics")[0]
        self.assertEqual(serialized_diagnostic["id"], diagnostic.id)
        self.assertEqual(serialized_diagnostic["percentageValueTotalHt"], 1)
        self.assertNotIn("percentageValueBioHt", serialized_diagnostic)

    def test_satellite_published_no_type(self):
        """
        Central cuisine diagnostics should only be returned if their central_kitchen_diagnostic_mode
        is set. Otherwise it may be an old diagnostic that is not meant for the satellites
        """
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            publication_status="published",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=None,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(body.get("id"), satellite.id)
        self.assertEqual(len(body.get("approDiagnostics")), 0)

    def test_satellite_published_needed_fields(self):
        """
        If the central kitchen diag is set to APPRO, only the appro fields should be included.
        If the central kitchen diag is set to ALL, every fields should be included.
        """
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            publication_status="published",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2021,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            value_fish_ht=100,
            value_fish_egalim_ht=80,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(body.get("approDiagnostics")), 2)
        self.assertEqual(len(body.get("serviceDiagnostics")), 1)
        appro_diagnostics = body.get("approDiagnostics")
        appro_diag_2020 = next(filter(lambda x: x["year"] == 2020, appro_diagnostics))
        appro_diag_2021 = next(filter(lambda x: x["year"] == 2021, appro_diagnostics))
        service_diag_2021 = body.get("serviceDiagnostics")[0]

        self.assertIn("percentageValueTotalHt", appro_diag_2020)
        self.assertNotIn("hasWasteDiagnostic", appro_diag_2020)

        self.assertIn("percentageValueTotalHt", appro_diag_2021)
        self.assertIn("hasWasteDiagnostic", service_diag_2021)
        self.assertNotIn("valueFishEgalimHt", appro_diag_2021)
        self.assertIn("percentageValueFishEgalimHt", appro_diag_2021)

    def test_percentage_values(self):
        """
        The published endpoint should not contain the real economic data, only percentages.
        """
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status="published",
        )

        DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            value_total_ht=1200,
            value_bio_ht=600,
            value_sustainable_ht=300,
            value_meat_poultry_ht=200,
            value_meat_poultry_egalim_ht=100,
            value_fish_ht=10,
            value_fish_egalim_ht=8,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(body.get("approDiagnostics")), 1)
        serialized_diag = body.get("approDiagnostics")[0]

        self.assertEqual(serialized_diag["percentageValueTotalHt"], 1)
        self.assertEqual(serialized_diag["percentageValueBioHt"], 0.5)
        self.assertEqual(serialized_diag["percentageValueSustainableHt"], 0.25)
        # the following is a percentage of the meat total, not global total
        self.assertEqual(serialized_diag["percentageValueMeatPoultryEgalimHt"], 0.5)
        self.assertEqual(serialized_diag["percentageValueFishEgalimHt"], 0.8)
        # ensure the raw values are not included in the diagnostic
        self.assertNotIn("valueTotalHt", serialized_diag)
        self.assertNotIn("valueBioHt", serialized_diag)
        self.assertNotIn("valueMeatPoultryHt", serialized_diag)
        self.assertNotIn("valueMeatPoultryEgalimHt", serialized_diag)
        self.assertNotIn("valueFishHt", serialized_diag)
        self.assertNotIn("valueFishEgalimHt", serialized_diag)

    def test_remove_raw_values_when_missing_totals(self):
        """
        The published endpoint should not contain the real economic data, only percentages.
        Even when the meat and fish totals are absent, but EGAlim and France totals are present.
        """
        central_siret = "22730656663081"
        canteen = CanteenFactory.create(
            siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status="published",
        )

        DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            value_meat_poultry_ht=None,
            value_meat_poultry_egalim_ht=100,
            value_meat_poultry_france_ht=100,
            value_fish_ht=None,
            value_fish_egalim_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        serialized_diag = body.get("approDiagnostics")[0]

        self.assertNotIn("valueMeatPoultryEgalimHt", serialized_diag)
        self.assertNotIn("valueMeatPoultryFranceHt", serialized_diag)
        self.assertNotIn("valueFishEgalimHt", serialized_diag)

    def test_return_published_diagnostics(self):
        """
        The published endpoint returns all diagnostic "service" data in one property,
        and the appro data in another. The latter should be filtered on the redacted years.
        """
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status="published",
            redacted_appro_years=[2020, 2021, 2023],
        )

        DiagnosticFactory.create(canteen=canteen, year=2021)
        published_appro_diag = DiagnosticFactory.create(canteen=canteen, year=2022)
        DiagnosticFactory.create(canteen=canteen, year=2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(body.get("serviceDiagnostics")), 3)
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        serialized_diags = body.get("serviceDiagnostics")
        serialized_appro_diags = body.get("approDiagnostics")

        for diag in serialized_diags:
            self.assertNotIn("percentageValueTotalHt", diag)
            self.assertNotIn("valueTotalHt", diag)

        self.assertEqual(serialized_appro_diags[0]["id"], published_appro_diag.id)
        self.assertIn("percentageValueTotalHt", serialized_appro_diags[0])
        self.assertNotIn("valueTotalHt", serialized_appro_diags[0])

    def test_satellites_can_redact_cc_appro_data(self):
        """
        Satellites should be able to redact the appro data provided by a CC, regardless of diagostic mode,
        without impacting other satellites or the CC
        """
        central = CanteenFactory.create(
            siret="96766910375238", production_type=Canteen.ProductionType.CENTRAL, redacted_appro_years=[]
        )
        fully_redacted_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            publication_status="published",
            redacted_appro_years=[2022, 2023],
        )
        partially_redacted_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            publication_status="published",
            redacted_appro_years=[2022],
        )
        other_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            publication_status="published",
            redacted_appro_years=[],
        )

        DiagnosticFactory.create(
            canteen=central, year=2022, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL
        )
        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        self.assertEqual(fully_redacted_satellite.central_kitchen_diagnostics.count(), 2)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": fully_redacted_satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 0)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": partially_redacted_satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        self.assertEqual(body.get("approDiagnostics")[0]["year"], 2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": other_satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 2)

    def test_cc_can_redact_appro_data(self):
        """
        CCs should be able to redact the appro data without impacting their satellites
        """
        central = CanteenFactory.create(
            siret="96766910375238",
            production_type=Canteen.ProductionType.CENTRAL,
            redacted_appro_years=[2023],
            publication_status="published",
        )
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            publication_status="published",
            redacted_appro_years=[],
        )

        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": central.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 0)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 1)

    def test_satellites_get_correct_appro_diagnostic(self):
        """
        Satellites that have their own diagnostic for one year, and CC diagnostics for another,
        should receive the CC diagnostic where it exists
        """
        central = CanteenFactory.create(siret="96766910375238", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            publication_status="published",
        )

        DiagnosticFactory.create(canteen=satellite, year=2021)
        DiagnosticFactory.create(
            canteen=central, year=2022, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        DiagnosticFactory.create(canteen=satellite, year=2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        serialized_diagnostics = body.get("approDiagnostics")
        self.assertEqual(len(serialized_diagnostics), 3)
        for diagnostic in serialized_diagnostics:
            if diagnostic["year"] == 2021:
                self.assertEqual(
                    diagnostic["canteenId"], satellite.id, "return satellite diagnostic when only diag for year"
                )
            elif diagnostic["year"] == 2022:
                self.assertEqual(diagnostic["canteenId"], central.id, "return CC diagnostic when only diag for year")
            elif diagnostic["year"] == 2023:
                self.assertEqual(
                    diagnostic["canteenId"], central.id, "priority to central diagnostic where there are both"
                )

    def test_satellites_can_redact_own_appro_data(self):
        """
        Satellites that have their own diagnostic should be able to redact their appro data
        without their CC's diagnostic appro data taking it's place
        """
        central = CanteenFactory.create(siret="96766910375238", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            publication_status="published",
            redacted_appro_years=[2023],
        )

        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        DiagnosticFactory.create(canteen=satellite, year=2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 0)

    def test_td_diags_not_redacted(self):
        """
        A teledeclared diagnostic cannot be redacted
        """
        canteen = CanteenFactory.create(publication_status="published", redacted_appro_years=[2022, 2023])

        DiagnosticFactory.create(canteen=canteen, year=2022)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2023)
        TeledeclarationFactory.create(
            diagnostic=diagnostic, status=Teledeclaration.TeledeclarationStatus.SUBMITTED, declared_data={"foo": "bar"}
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        self.assertEqual(len(body.get("serviceDiagnostics")), 2)


@override_settings(PUBLISH_BY_DEFAULT=True)
class TestPublicCanteenApi(APITestCase):
    def test_get_single_published_canteen(self):
        """
        All canteens are published except those with line_ministry of ARMEE
        """
        published_canteen = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.DRAFT, line_ministry=None
        )
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": published_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("id"), published_canteen.id)

    def test_get_single_army_canteen(self):
        """
        Canteens with a line ministry of ARMEE are not available publicly, regardless of publication status
        """
        private_canteen = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            line_ministry=Canteen.Ministries.ARMEE,
        )
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": private_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestPublishedCanteenClaimApi(APITestCase):
    def test_canteen_claim_value(self):
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)

        # The factory creates canteens with managers
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertFalse(body.get("canBeClaimed"))

        # Now we will remove the manager to change the claim API value
        canteen.managers.clear()
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertTrue(body.get("canBeClaimed"))

    @authenticate
    def test_canteen_claim_request(self):
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.DRAFT)
        canteen.managers.clear()

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        user = authenticate.user
        self.assertEqual(canteen.managers.first().id, user.id)
        self.assertEqual(canteen.managers.count(), 1)
        canteen.refresh_from_db()
        self.assertEqual(canteen.claimed_by, user)
        self.assertTrue(canteen.has_been_claimed)

    @authenticate
    def test_canteen_claim_request_fails_when_already_claimed(self):
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        self.assertGreater(canteen.managers.count(), 0)
        user = authenticate.user
        self.assertFalse(canteen.managers.filter(id=user.id).exists())

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(canteen.managers.filter(id=user.id).exists())
        canteen.refresh_from_db()
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_undo_claim_canteen(self):
        canteen = CanteenFactory.create(claimed_by=authenticate.user, has_been_claimed=True)
        canteen.managers.add(authenticate.user)

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertIsNone(canteen.claimed_by)
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_undo_claim_canteen_fails_if_not_original_claimer(self):
        other_user = UserFactory.create()
        canteen = CanteenFactory.create(claimed_by=other_user, has_been_claimed=True)
        canteen.managers.add(authenticate.user)

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertTrue(canteen.has_been_claimed)
        self.assertEqual(canteen.claimed_by, other_user)
