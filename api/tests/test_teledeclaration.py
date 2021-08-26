from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, DiagnosticFactory, TeledeclarationFactory
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
        diagnostic = DiagnosticFactory.create(
            canteen=canteen, year=2020, value_bio_ht=None
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
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        payload = {"diagnosticId": diagnostic.id}

        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        body = response.json()
        teledeclaration = Teledeclaration.objects.first()

        self.assertEqual(body["teledeclaration"]["id"], teledeclaration.id)
        self.assertEqual(body["teledeclaration"]["status"], "SUBMITTED")

        self.assertEqual(teledeclaration.source, diagnostic)
        self.assertEqual(teledeclaration.canteen, canteen)
        self.assertEqual(teledeclaration.year, 2020)
        self.assertEqual(teledeclaration.applicant, user)
        self.assertEqual(
            teledeclaration.status, Teledeclaration.TeledeclarationStatus.SUBMITTED
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
        teledeclaration = TeledeclarationFactory.create(
            source=diagnostic,
            canteen=canteen,
            year=2020,
            applicant=user,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
        )

        payload = {"teledeclarationId": teledeclaration.id}
        response = self.client.post(reverse("teledeclaration_cancel"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_teledeclaration = Teledeclaration.objects.get(pk=teledeclaration.id)
        self.assertEqual(
            db_teledeclaration.status, Teledeclaration.TeledeclarationStatus.CANCELLED
        )

        body = response.json()
        self.assertEqual(body["teledeclaration"]["status"], "CANCELLED")

    @authenticate
    def test_create_duplicate(self):
        """
        We can only have one submitted teledeclaration per canteen/year
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        TeledeclarationFactory.create(
            source=diagnostic,
            canteen=canteen,
            year=2020,
            applicant=user,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
        )

        payload = {"diagnosticId": diagnostic.id}
        response = self.client.post(reverse("teledeclaration_create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
