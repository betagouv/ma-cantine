from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic


class DiagnosticTeledeclarationPdfApiTest(APITestCase):
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_generate_pdf_if_unauthenticated(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_unknown_canteen_or_diagnostic(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        response = self.client.get(
            reverse("diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": 9999, "pk": diagnostic.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(
            reverse("diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_not_canteen_manager(self):
        diagnostic = DiagnosticFactory(year=2024)
        # authenticate.user is not a manager of the canteen
        diagnostic.teledeclare(authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_can_generate_pdf(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2022-08-30")  # during the 2021 campaign
    @authenticate
    def test_can_generate_pdf_legacy_teledeclaration(self):
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2021, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        diagnostic.teledeclare(applicant=authenticate.user)
        # simulate legacy diagnostic without type
        Diagnostic.objects.filter(id=diagnostic.id).update(
            diagnostic_type=None, canteen_snapshot={"name": ""}, applicant_snapshot={"name": ""}
        )

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_can_generate_pdf_central(self):
        canteen = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE)
        diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )
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
