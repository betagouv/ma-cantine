from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, TeledeclarationFactory, UserFactory
from data.models import Canteen, Diagnostic, Teledeclaration


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
        manager = UserFactory()
        canteen = CanteenFactory()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, manager)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_generate_pdf(self):
        """
        The user can get a justificatif in PDF for a teledeclaration
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
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
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
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
        canteen = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("teledeclaration_pdf", kwargs={"pk": teledeclaration.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTeledeclarationCampaignDatesApi(APITestCase):
    def test_campaign_dates_list(self):
        response = self.client.get(reverse("list_teledeclaration_campaign_dates"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body), 5)
        self.assertEqual(body[-1]["year"], 2025)

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
                    self.assertEqual(body["inTeledeclaration"], date_freeze["in_teledeclaration"])
                    self.assertEqual(body["inCorrection"], date_freeze["in_correction"])
                    self.assertEqual(body["inTeledeclaration"], date_freeze["in_teledeclaration"])
                    self.assertEqual(body["inCorrection"], date_freeze["in_correction"])
                    self.assertEqual(body["inTeledeclaration"], date_freeze["in_teledeclaration"])
                    self.assertEqual(body["inCorrection"], date_freeze["in_correction"])
                    self.assertEqual(body["inTeledeclaration"], date_freeze["in_teledeclaration"])
                    self.assertEqual(body["inCorrection"], date_freeze["in_correction"])
