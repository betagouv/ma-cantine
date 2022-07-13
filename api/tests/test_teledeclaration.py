from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
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
        response = self.client.post(reverse("teledeclaration_cancel"), payload)
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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        teledeclaration = Teledeclaration.createFromDiagnostic(diagnostic, manager)

        payload = {"teledeclarationId": teledeclaration.id}
        response = self.client.post(reverse("teledeclaration_cancel"), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_generate_pdf_unauthorized(self):
        """
        Only managers of the canteen can get PDF documents
        """
        manager = UserFactory.create()
        canteen = CanteenFactory.create()
        canteen.managers.add(manager)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        teledeclaration = Teledeclaration.createFromDiagnostic(diagnostic, manager)

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
    def test_cancel_missing_teledeclaration_id(self):
        """
        A validation error is returned if the teledeclaration ID is missing
        """
        payload = {}
        response = self.client.post(reverse("teledeclaration_cancel"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_incomplete_diagnostic(self):
        """
        A diagnostic missing approvisionnement information cannot be used to
        create a teledeclaration
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020, value_bio_ht=None)
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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
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
            json_teledeclaration["value_siqo_ht"],
            diagnostic.value_siqo_ht,
        )
        self.assertEqual(json_teledeclaration["value_total_ht"], diagnostic.value_total_ht)
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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        teledeclaration = Teledeclaration.createFromDiagnostic(diagnostic, user)

        payload = {"teledeclarationId": teledeclaration.id}
        response = self.client.post(reverse("teledeclaration_cancel"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED)

        body = response.json()
        self.assertEqual(body["teledeclaration"]["status"], "CANCELLED")

    @authenticate
    def test_generate_pdf(self):
        """
        The user can get a justificatif in PDF for a teledeclaration
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        teledeclaration = Teledeclaration.createFromDiagnostic(diagnostic, authenticate.user)

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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        Teledeclaration.createFromDiagnostic(diagnostic, user)

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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        Teledeclaration.createFromDiagnostic(diagnostic, user)

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        canteen2 = CanteenFactory.create(siret="")
        canteen2.managers.add(user)
        diagnostic2 = DiagnosticFactory.create(canteen=canteen2, year=2020)

        payload = {"diagnosticId": diagnostic2.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
