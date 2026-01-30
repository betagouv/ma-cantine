from unittest.mock import patch

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector, Teledeclaration


class DiagnosticToTeledeclareApiTest(APITestCase):
    @freeze_time("2022-08-30")  # during the 2021 campaign  # but this endpoint doesn't seem to check
    @authenticate
    def test_get_diagnostics_to_td(self):
        """
        Check that the endpoint includes a list of diagnostics that could be teledeclared
        """
        last_year = 2021
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
        DiagnosticFactory(canteen=canteen_with_incomplete_diag, year=last_year, valeur_totale=None)
        canteen_with_complete_diag = CanteenFactory(
            siret="21010034300016",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        complete_diag = DiagnosticFactory(canteen=canteen_with_complete_diag, year=last_year, valeur_totale=10000)

        # siret needs to be filled for the diag to be teledeclarable
        canteen_with_missing_data = CanteenFactory(
            # siret=None,
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        canteen_with_missing_data.siret = None
        canteen_with_missing_data.save(skip_validations=True)
        canteen_with_missing_data.refresh_from_db()
        DiagnosticFactory(canteen=canteen_with_missing_data, year=last_year, valeur_totale=10000)

        canteen_without_line_ministry = CanteenFactory(
            siret="31285246765507",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sector_list=[Sector.ADMINISTRATION_PRISON],
            line_ministry=Canteen.Ministries.SPORT,
            managers=[authenticate.user],
        )
        canteen_without_line_ministry.line_ministry = None
        canteen_without_line_ministry.save(skip_validations=True)
        canteen_without_line_ministry.refresh_from_db()
        DiagnosticFactory(canteen=canteen_without_line_ministry, year=last_year, valeur_totale=10000)

        # to verify we are returning the correct diag for the canteen, create another diag for a different year
        DiagnosticFactory(canteen=canteen_with_complete_diag, year=last_year - 1, valeur_totale=10000)
        canteen_with_td = CanteenFactory(
            siret="55476895458384",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        td_diag = DiagnosticFactory(canteen=canteen_with_td, year=last_year, valeur_totale=2000)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)

        response = self.client.get(reverse("diagnostics_to_teledeclare", kwargs={"year": last_year}))
        diagnostics = response.json().get("results")

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["id"], complete_diag.id)

    @authenticate
    def test_get_diagnostics_to_td_none(self):
        """
        Check that the actions endpoint includes an empty list of diagnostics that could be teledeclared
        if there are no diags to TD
        """
        last_year = 2021

        response = self.client.get(reverse("diagnostics_to_teledeclare", kwargs={"year": last_year}))
        body = response.json().get("results")

        self.assertEqual(body, [])

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
    def test_cannot_teledeclare_if_unauthenticated(self):
        # not canteen manager
        diagnostic = DiagnosticFactory(year=2024)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # canteen manager
        user = UserFactory()
        diagnostic.canteen.managers.add(user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_unknown_canteen_or_diagnostic(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": 9999, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": 9999},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_not_canteen_manager(self):
        diagnostic = DiagnosticFactory(year=2024)
        # authenticate.user is not a manager of the canteen

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_with_oauth2_token(self):
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-01-01")  # before the 2024 campaign
    def test_cannot_teledeclare_before_campaign(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
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
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], ["Ce diagnostic a déjà été télédéclaré"])

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_teledeclare_if_diagnostic_not_filled(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        Diagnostic.objects.filter(id=diagnostic.id).update(valeur_totale=0)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["detail"], ["Ce diagnostic n'est pas rempli"])

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_can_teledeclare_during_campaign(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertTrue(diagnostic.is_teledeclared)

    @authenticate
    @freeze_time("2025-04-20")  # during the 2024 correction campaign
    def test_can_teledeclare_during_correction_campaign(self):
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_create",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertTrue(diagnostic.is_teledeclared)


class DiagnosticTeledeclarationCancelView(APITestCase):
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_unauthenticated(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)

        # unauthenticated request
        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_if_not_canteen_manager(self):
        diagnostic = DiagnosticFactory(year=2024)
        # authenticate.user is not a manager of the canteen
        diagnostic.teledeclare(authenticate.user)

        response = self.client.post(
            reverse(
                "diagnostic_teledeclaration_cancel",
                kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2025-03-30")  # during the 2024 campaign
    def test_cannot_cancel_teledeclaration_with_oauth2_token(self):
        user, token = get_oauth2_token("canteen:write")
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(user)
        diagnostic.teledeclare(user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
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
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
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
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
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
        diagnostic = DiagnosticFactory(year=2024)
        diagnostic.canteen.managers.add(authenticate.user)
        diagnostic.teledeclare(authenticate.user)

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
