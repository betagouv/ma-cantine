from unittest.mock import patch

from django.core.management import call_command
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from api.views.diagnostic_teledeclaration import DiagnosticTeledeclarationPdfView
from data.models import Canteen, Diagnostic, Sector, Teledeclaration
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_required


class DiagnosticToTeledeclareApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.year = 2021
        cls.url = reverse("diagnostics_to_teledeclare", kwargs={"year": 2021})

    @freeze_time("2022-08-30")  # during the 2021 campaign  # but this endpoint doesn't seem to check
    @authenticate
    def test_can_get_diagnostics_to_td(self):
        CanteenFactory(  # without diag
            siret="21590350100017",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        canteen_with_incomplete_diag = CanteenFactory(
            siret="96766910375238",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        DiagnosticFactory(canteen=canteen_with_incomplete_diag, year=self.year, valeur_totale=None)
        canteen_with_complete_diag = CanteenFactory(
            siret="21010034300016",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        complete_diag = DiagnosticFactory(canteen=canteen_with_complete_diag, year=self.year, valeur_totale=10000)

        # siret needs to be filled for the diag to be teledeclarable
        canteen_with_missing_data = CanteenFactory(
            siret=None,
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
            skip_validations=True,
        )
        DiagnosticFactory(canteen=canteen_with_missing_data, year=self.year, valeur_totale=10000)

        canteen_without_line_ministry = CanteenFactory(
            siret="31285246765507",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.ADMINISTRATION_PRISON],
            line_ministry=None,
            managers=[authenticate.user],
            skip_validations=True,
        )
        DiagnosticFactory(canteen=canteen_without_line_ministry, year=self.year, valeur_totale=10000)

        # to verify we are returning the correct diag for the canteen, create another diag for a different year
        DiagnosticFactory(canteen=canteen_with_complete_diag, year=self.year + 1, valeur_totale=10000)
        canteen_with_td = CanteenFactory(
            siret="55476895458384",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        td_diag = DiagnosticFactory(canteen=canteen_with_td, year=self.year, valeur_totale=2000)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)

        response = self.client.get(self.url)

        body = response.json()
        results = body["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], complete_diag.id)

    @authenticate
    def test_get_diagnostics_to_td_none(self):
        """
        Check that the actions endpoint includes an empty list of diagnostics that could be teledeclared
        if there are no diags to TD
        """
        response = self.client.get(self.url)

        body = response.json()
        results = body["results"]
        self.assertEqual(results, [])

    @authenticate
    def test_get_diagnostics_to_td_in_correction_campaign(self):
        """
        During correction campaign check that the actions endpoint includes only diagnostics cancelled,
        and diagnostics not teledeclared during teledeclaration campaign
        """
        last_year = 2024

        # Canteen with diag not teledeclared
        canteen_with_diag = CanteenFactory(
            name="Canteen with diag",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        DiagnosticFactory(canteen=canteen_with_diag, year=last_year, valeur_totale=1000)

        # Canteen with diag teledeclared
        canteen_with_td = CanteenFactory(
            name="Canteen with TD",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        diag_to_teledeclare = DiagnosticFactory(canteen=canteen_with_td, year=last_year, valeur_totale=10000)
        Teledeclaration.create_from_diagnostic(diag_to_teledeclare, authenticate.user)

        # Canteen with teledeclaration edited
        canteen_with_correction = CanteenFactory(
            name="Canteen with TD cancelled",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            siret="21340172201787",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        diag_cancelled = DiagnosticFactory(canteen=canteen_with_correction, year=last_year, valeur_totale=10000)
        teledeclaration_cancelled = Teledeclaration.create_from_diagnostic(diag_cancelled, authenticate.user)
        teledeclaration_cancelled.cancel()

        # API : Force correction campaign without changing dates
        with patch("api.views.diagnostic.is_in_correction", lambda: True):
            response = self.client.get(reverse("diagnostics_to_teledeclare", kwargs={"year": last_year}))
            results = response.json().get("results")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], diag_cancelled.id)
        self.assertEqual(results[0]["canteenId"], canteen_with_correction.id)


class DiagnosticTeledeclarationCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    def test_cannot_teledeclare_if_unauthenticated(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_canteen_does_not_exist(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": 9999, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_diagnostic_does_not_exist(self):
        DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": 9999},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_not_canteen_manager(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(user)
        # authenticate.user is not a manager of the canteen

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_diagnostic_if_not_corresponding_canteen(self):
        canteen_other = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        diagnostic_other = DiagnosticFactory(canteen=canteen_other, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic_other.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # even if the user manages canteen_other
        canteen_other.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic_other.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.token}")
        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-01-01")  # before the 2024 campaign
    def test_cannot_teledeclare_before_campaign(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["detail"], ["Ce n'est pas possible de télédéclarer hors de la période de la campagne"]
        )

    @authenticate
    @freeze_time("2025-06-30")  # after the 2024 campaign
    def test_cannot_teledeclare_after_campaign(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["detail"], ["Ce n'est pas possible de télédéclarer hors de la période de la campagne"]
        )

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_diagnostic_of_another_year(self):
        diagnostic = DiagnosticFactory(year=2023)
        diagnostic.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], ["Ce diagnostic n'est pas dans la bonne année de télédéclaration"])

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_already_teledeclared(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], ["Ce diagnostic a déjà été télédéclaré"])

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_diagnostic_not_filled(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)
        Diagnostic.objects.filter(id=diagnostic.id).update(valeur_totale=0, is_filled=False)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], ["Ce diagnostic n'est pas rempli"])

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_bad_total(self):
        diagnostic = DiagnosticFactory(
            canteen=self.canteen_site, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        self.canteen_site.managers.add(authenticate.user)
        Diagnostic.objects.filter(id=diagnostic.id).update(valeur_totale=100, valeur_bio=1000)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("valeurTotale", response.json())

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_can_teledeclare_during_campaign(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    @freeze_time("2027-01-30")  # during the 2026 campaign
    def test_can_teledeclare_without_volet_thematique(self):
        diagnostic = DiagnosticFactory(
            canteen=self.canteen_site, year=2026, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        self.canteen_site.managers.add(authenticate.user)
        # empty the required fields of the volets thématiques
        for volet in ["GASPILLAGE", "DIVERSIFICATION", "PLASTIQUE", "INFORMATION"]:
            for field in get_teledeclaration_fields_required(2026, volet):
                setattr(diagnostic, field, None)
        diagnostic.save()

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    @freeze_time("2025-04-20")  # during the 2024 correction campaign
    def test_cannot_teledeclare_draft_during_correction_campaign(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        diagnostic.refresh_from_db()
        self.assertEqual(
            response.json()["year"],
            [
                "Le diagnostic de l'année 2024 ne peut plus être modifié car la campagne de télédéclaration est terminée."
            ],
        )

    @authenticate
    def test_can_teledeclare_correction_during_correction_campaign(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic.teledeclare(authenticate.user)

        self.assertTrue(diagnostic.is_teledeclared)

        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            diagnostic.cancel()

            self.assertFalse(diagnostic.is_teledeclared)
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.CORRECTION)

            response = self.client.post(
                reverse(
                    "diagnostic_teledeclaration_create",
                    kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
                )
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            diagnostic.refresh_from_db()
            self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    def test_cannot_teledeclare_correction_after_correction_campaign(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic.teledeclare(authenticate.user)

        self.assertTrue(diagnostic.is_teledeclared)

        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            diagnostic.cancel()

            self.assertFalse(diagnostic.is_teledeclared)
            self.assertEqual(diagnostic.status, Diagnostic.DiagnosticStatus.CORRECTION)

        with freeze_time("2025-06-30"):  # after the 2024 campaign
            response = self.client.post(
                reverse(
                    "diagnostic_teledeclaration_create",
                    kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic.id},
                )
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            diagnostic.refresh_from_db()
            self.assertFalse(diagnostic.is_teledeclared)


class DiagnosticTeledeclarationCancelView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_unauthenticated(self):
        user = UserFactory()
        self.canteen_site.managers.add(user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        diagnostic.teledeclare(user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_canteen_does_not_exist(self):
        self.canteen_site.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        diagnostic.teledeclare(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": 9999, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_diagnostic_does_not_exist(self):
        self.canteen_site.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        diagnostic.teledeclare(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": 9999},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_not_canteen_manager(self):
        user = UserFactory()
        self.canteen_site.managers.add(user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        diagnostic.teledeclare(user)

        # teledeclared by user, but authenticate.user is not a manager
        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_not_corresponding_canteen(self):
        canteen_other = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        diagnostic_other = DiagnosticFactory(canteen=canteen_other, year=2024)
        self.canteen_site.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic_other.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # even if the user manages canteen_other
        canteen_other.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": self.canteen_site.id, "pk": diagnostic_other.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen_site.managers.add(user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        diagnostic.teledeclare(user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.token}")
        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_diagnostic_not_teledeclared(self):
        self.canteen_site.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        # diagnostic not teledeclared

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], ["Ce diagnostic doit avoir été télédéclaré"])

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_after_campaign(self):
        self.canteen_site.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory(canteen=self.canteen_site, year=2024)
        diagnostic.teledeclare(authenticate.user)

        with freeze_time("2025-06-30"):  # after the 2024 campaign
            response = self.client.post(
                reverse(
                    "diagnostic_teledeclaration_cancel",
                    kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
                )
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.json()["detail"],
                ["Ce n'est pas possible d'annuler une télédéclaration hors de la période de la campagne"],
            )

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_can_cancel_teledeclaration_during_campaign(self):
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen_site, year=2024)
        diagnostic.teledeclare(authenticate.user)

        self.assertTrue(diagnostic.is_teledeclared)
        for field in Diagnostic.TELEDECLARATION_FIELDS:
            with self.subTest(field=field):
                self.assertIsNotNone(getattr(diagnostic, field))

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertFalse(diagnostic.is_teledeclared)
        for field in Diagnostic.TELEDECLARATION_FIELDS:
            with self.subTest(field=field):
                self.assertIsNone(getattr(diagnostic, field))

    @authenticate
    def test_can_cancel_teledeclaration_during_correction_campaign(self):
        canteen_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen_site, year=2024)
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            diagnostic.teledeclare(authenticate.user)

        self.assertTrue(diagnostic.is_teledeclared)

        with freeze_time("2025-04-20"):  # during the 2024 correction campaign
            response = self.client.post(
                reverse(
                    "diagnostic_teledeclaration_cancel",
                    kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
                )
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertFalse(diagnostic.is_teledeclared)


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
    def test_cannot_generate_pdf_if_canteen_does_not_exist(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        url = reverse("diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": 9999, "pk": diagnostic.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_diagnostic_does_not_exist(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        url = reverse("diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    @authenticate
    def test_cannot_generate_pdf_if_not_canteen_manager(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)

        # teledeclared by user, but authenticate.user is not a manager
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
        canteen_central = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user], skip_validations=True
        )
        diagnostic = DiagnosticFactory(
            canteen=canteen_central, year=2024, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2026-03-30")  # during the 2025 campaign
    @authenticate
    def test_can_generate_pdf_groupe_satellite(self):
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE, managers=[authenticate.user])
        canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe, managers=[authenticate.user]
        )
        diagnostic_satellite = DiagnosticFactory(
            canteen=canteen_satellite, year=2025, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic_satellite.teledeclare(applicant=authenticate.user)
        diagnostic_groupe = DiagnosticFactory(
            canteen=canteen_groupe, year=2025, diagnostic_type=Diagnostic.DiagnosticType.SIMPLE
        )
        diagnostic_groupe.teledeclare(applicant=authenticate.user)

        call_command("diagnostic_fill_invalid_warning_reason_list", year=2025, apply=True)
        call_command("teledeclaration_generate_1td1site", year=2025, apply=True)

        # groupe should be able to generate pdf
        url = reverse(
            "diagnostic_teledeclaration_pdf", kwargs={"canteen_pk": canteen_groupe.id, "pk": diagnostic_groupe.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # satellite should be able to generate pdf of initial diagnostic
        # (even if the diagnostic is not valid: DOUBLON_1TD1SITE)
        url = reverse(
            "diagnostic_teledeclaration_pdf",
            kwargs={"canteen_pk": canteen_satellite.id, "pk": diagnostic_satellite.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # satellite should be able to generate pdf of generated diagnostic
        diagnostic_satellite_generated = Diagnostic.all_objects.get(
            canteen=canteen_satellite, year=2025, generated_from_groupe_diagnostic=True
        )

        url = reverse(
            "diagnostic_teledeclaration_pdf",
            kwargs={"canteen_pk": canteen_satellite.id, "pk": diagnostic_satellite_generated.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_pdf_templates_display_the_volet_answers(self):
        """
        The PDF templates read the diagnostic fields by name (diagnostic.__dict__ + overrides):
        a renamed field must be renamed in the templates (& overrides) too
        """
        user = UserFactory()
        canteen = CanteenFactory(daily_meal_count=200)  # the diversification plan question applies
        diagnostic = DiagnosticFactory(
            canteen=canteen,
            year=2024,
            diagnostic_gaspillage_realise=True,
            actions_gaspillage_realisees=[Diagnostic.ActionsGaspillage.SENSIBILISATION],
            plan_diversification_en_place=True,
            plan_diversification_actions=[Diagnostic.PlanDiversificationActions.PLATS_PRODUITS],
            menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.QUOTIDIEN,
            menu_vegetarien_bases=[Diagnostic.MenuVegetarienBase.SOJA],
            information_qualite_nutritionnelle=True,
            information_qualite_durable=True,
            information_supports=[Diagnostic.InformationSupport.AFFICHAGE],
            information_supports_autre="Journal de l'école",
            information_frequence=Diagnostic.InformationFrequence.ANNUELLE,
            information_support_url="https://example.com/menus",
            plastique_contenant_cuisson_remplace=True,
            plastique_contenant_service_remplace=True,
            plastique_bouteille_remplace=False,
            plastique_ustensile_remplace=False,
        )
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)
        context = DiagnosticTeledeclarationPdfView.get_context(diagnostic)

        for template_name in ["teledeclaration_pdf/v2.html", "teledeclaration_pdf/v1.html"]:
            with self.subTest(template_name=template_name):
                html = get_template(template_name).render(context)
                # gaspillage
                self.assertIn("Diagnostic sur le gaspillage réalisé", html)
                if template_name == "teledeclaration_pdf/v2.html":
                    self.assertIn(Diagnostic.ActionsGaspillage.SENSIBILISATION.label, html)
                # diversification
                # only displayed if plan_diversification_en_place
                self.assertIn(Diagnostic.PlanDiversificationActions.PLATS_PRODUITS.label, html)
                self.assertIn(Diagnostic.MenuVegetarienFrequence.QUOTIDIEN.label, html)
                self.assertIn(Diagnostic.MenuVegetarienBase.SOJA.label, html)
                # information
                self.assertIn("Communique sur le plan alimentaire", html)
                self.assertIn("Communique sur les démarches qualité/durables/équitables", html)
                self.assertNotIn("Ne communique pas", html)
                self.assertIn(Diagnostic.InformationSupport.AFFICHAGE.label, html)
                self.assertIn("Journal de l&#x27;école", html)
                self.assertIn(Diagnostic.InformationFrequence.ANNUELLE.label, html)
                self.assertIn("https://example.com/menus", html)
                # plastique
                self.assertIn("Contenants de cuisson en plastique remplacés", html)
                self.assertIn("Contenants de service en plastique remplacés", html)
                self.assertIn("Bouteilles en plastique non remplacées", html)


class DiagnosticTeledeclarationPdfInformation2026Test(SimpleTestCase):
    def test_measure_info_template_since_2026(self):
        template = get_template("teledeclaration_pdf/blocks/measure_info.html")
        context = {
            "information_affichage_permanent": True,
            "information_electronique_annuelle": False,
            "information_part_egalim": True,
            "information_part_pat": None,
            "information_consultation_qualite": True,
            # previous fields (ignored since 2026)
            "information_qualite_nutritionnelle": True,
        }

        html = template.render({"year": 2026, **context})
        for field_name in context:
            if field_name.startswith("information_qualite"):
                continue
            self.assertIn(Diagnostic._meta.get_field(field_name).verbose_name, html)
        self.assertNotIn("Communique sur le plan alimentaire", html)

        html = template.render({"year": 2025, **context})
        self.assertIn("Communique sur le plan alimentaire", html)
        self.assertNotIn("affichage permanent", html)


class DiagnosticTeledeclarationPdfPlastique2026Test(SimpleTestCase):
    def test_measure_plastic_template_since_2026(self):
        template = get_template("teledeclaration_pdf/blocks/measure_plastic.html")
        context = {
            "plastique_bouteille_boisson_remplace": True,
            "plastique_bouteille_remplace": None,
            "plastique_ustensile_remplace": True,
            "plastique_vaisselle_jetable_remplace": False,
            "plastique_contenant_remplace": True,
            "vente_emporter": True,
            "plastique_contenant_emporter_remplace": True,
            # removed in 2026
            "plastique_contenant_cuisson_remplace": True,
        }

        html = template.render({"year": 2026, **context})
        for field_name in NEW_PLASTIQUE_FIELDS_2026:
            self.assertIn(Diagnostic._meta.get_field(field_name).verbose_name, html)
        self.assertIn("Aucune bouteilles d’eau plate en plastique", html)
        self.assertIn("Aucun ustensiles à usage unique en matière plastique", html)
        self.assertNotIn("Contenants de cuisson en plastique remplacés", html)

        html = template.render({"year": 2025, **context})
        self.assertIn("Contenants de cuisson en plastique remplacés", html)
        self.assertNotIn("fontaine d'eau potable", html)

    def test_measure_plastic_template_since_2026_without_vente_emporter(self):
        template = get_template("teledeclaration_campaign_2024/measure_plastic.html")
        html = template.render({"year": 2026, "vente_emporter": False, "plastique_contenant_emporter_remplace": None})
        self.assertIn("L'établissement ne propose pas de repas à emporter", html)
        self.assertNotIn("repas à emporter : Inconnu", html)


NEW_PLASTIQUE_FIELDS_2026 = [
    "plastique_bouteille_boisson_remplace",
    "plastique_vaisselle_jetable_remplace",
    "plastique_contenant_remplace",
    "plastique_contenant_emporter_remplace",
]
