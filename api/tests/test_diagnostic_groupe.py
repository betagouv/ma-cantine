from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Canteen, Diagnostic


class DiagnosticGroupeCouvertsAnnuelsApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_satellite_1 = CanteenFactory(
            name="B", production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=cls.canteen_groupe
        )
        cls.canteen_satellite_2 = CanteenFactory(
            name="A", production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=cls.canteen_groupe
        )
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def setUp(self):
        self.diagnostic_groupe = DiagnosticFactory(
            canteen=self.canteen_groupe,
            year=2026,
            satellites_nombre_repas_an={str(self.canteen_satellite_1.id): 1000},
        )
        self.diagnostic_site = DiagnosticFactory(canteen=self.canteen_site, year=2026)

    def _url(self, canteen, diagnostic):
        return reverse("diagnostic_groupe_couverts_annuels", kwargs={"canteen_pk": canteen.id, "pk": diagnostic.id})

    def test_cannot_get_if_unauthenticated(self):
        response = self.client.get(self._url(self.canteen_groupe, self.diagnostic_groupe))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_if_not_canteen_manager(self):
        response = self.client.get(self._url(self.canteen_groupe, self.diagnostic_groupe))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_diagnostic_of_another_canteen(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.get(self._url(self.canteen_groupe, self.diagnostic_site))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_if_not_groupe(self):
        self.canteen_site.managers.add(authenticate.user)
        response = self.client.get(self._url(self.canteen_site, self.diagnostic_site))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_get(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.get(self._url(self.canteen_groupe, self.diagnostic_groupe))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 2)
        # ordered by name
        self.assertEqual(body[0]["id"], self.canteen_satellite_2.id)
        self.assertEqual(body[0]["nombreRepasAn"], None)
        self.assertEqual(body[1]["id"], self.canteen_satellite_1.id)
        self.assertEqual(body[1]["nombreRepasAn"], 1000)
        self.assertEqual(set(body[1].keys()), {"id", "siret", "sirenUniteLegale", "name", "nombreRepasAn"})

    @authenticate
    def test_patch(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe),
            {"id": self.canteen_satellite_2.id, "nombreRepasAn": 2000},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diagnostic_groupe.refresh_from_db()
        self.assertEqual(
            self.diagnostic_groupe.satellites_nombre_repas_an,
            {str(self.canteen_satellite_1.id): 1000, str(self.canteen_satellite_2.id): 2000},
        )
        self.assertEqual(self.diagnostic_groupe.satellites_nombre_repas_an_total, 3000)

    @authenticate
    def test_patch_empty_value(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe),
            {"id": self.canteen_satellite_1.id, "nombreRepasAn": None},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diagnostic_groupe.refresh_from_db()
        self.assertIsNone(self.diagnostic_groupe.satellites_nombre_repas_an_total)

    @authenticate
    def test_cannot_patch_canteen_not_satellite_of_the_groupe(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe),
            {"id": self.canteen_site.id, "nombreRepasAn": 2000},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.diagnostic_groupe.refresh_from_db()
        self.assertNotIn(str(self.canteen_site.id), self.diagnostic_groupe.satellites_nombre_repas_an)

    @authenticate
    def test_cannot_patch_if_not_groupe(self):
        self.canteen_site.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_site, self.diagnostic_site),
            {"id": self.canteen_satellite_1.id, "nombreRepasAn": 2000},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_patch_if_teledeclared(self):
        self.canteen_groupe.managers.add(authenticate.user)
        Diagnostic.objects.filter(id=self.diagnostic_groupe.id).update(status=Diagnostic.DiagnosticStatus.SUBMITTED)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe),
            {"id": self.canteen_satellite_2.id, "nombreRepasAn": 2000},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_patch_negative_value(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe),
            {"id": self.canteen_satellite_2.id, "nombreRepasAn": -1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DiagnosticGroupeNombreRepasAnApiTest(APITestCase):
    """
    [NEW in 2026] Groupe: nombre_repas_an can only be edited via an external application (OAuth2)
    """

    @classmethod
    def setUpTestData(cls):
        cls.canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def setUp(self):
        self.diagnostic_groupe = DiagnosticFactory(canteen=self.canteen_groupe, year=2026, nombre_repas_an=1000)
        self.diagnostic_groupe_2025 = DiagnosticFactory(canteen=self.canteen_groupe, year=2025)
        self.diagnostic_site = DiagnosticFactory(canteen=self.canteen_site, year=2026, nombre_repas_an=1000)

    def _url(self, canteen, diagnostic):
        return reverse("diagnostic_retrieve_update", kwargs={"canteen_pk": canteen.id, "pk": diagnostic.id})

    @authenticate
    def test_groupe_cannot_edit_nombre_repas_an_from_the_app(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe), {"nombreRepasAn": 2000}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nombreRepasAn", response.json())
        self.diagnostic_groupe.refresh_from_db()
        self.assertEqual(self.diagnostic_groupe.nombre_repas_an, 1000)

    @authenticate
    def test_groupe_can_send_the_same_nombre_repas_an_from_the_app(self):
        self.canteen_groupe.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe), {"nombreRepasAn": 1000}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_groupe_can_edit_nombre_repas_an_from_an_external_application(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen_groupe.managers.add(user)
        self.client.credentials(Authorization=f"Bearer {token.token}")
        response = self.client.patch(
            self._url(self.canteen_groupe, self.diagnostic_groupe), {"nombreRepasAn": 2000}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diagnostic_groupe.refresh_from_db()
        self.assertEqual(self.diagnostic_groupe.nombre_repas_an, 2000)

    @authenticate
    def test_site_can_edit_nombre_repas_an_from_the_app(self):
        self.canteen_site.managers.add(authenticate.user)
        response = self.client.patch(
            self._url(self.canteen_site, self.diagnostic_site), {"nombreRepasAn": 2000}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diagnostic_site.refresh_from_db()
        self.assertEqual(self.diagnostic_site.nombre_repas_an, 2000)
