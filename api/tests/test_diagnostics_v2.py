from decimal import Decimal

from django.db import transaction
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from common.utils.camelize import camelize
from data.factories import CanteenFactory, DiagnosticFactory
from data.models import Diagnostic
from data.models.creation_source import CreationSource
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all


class DiagnosticV2ListApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.diagnostic_2025 = DiagnosticFactory(canteen=cls.canteen, year=2025)
        cls.diagnostic_2024 = DiagnosticFactory(canteen=cls.canteen, year=2024)
        cls.url = reverse("diagnostic_v2_list_create", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_list_diagnostics_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_list_diagnostics_if_canteen_unknown(self):
        response = self.client.get(reverse("diagnostic_v2_list_create", kwargs={"canteen_pk": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_list_diagnostics_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_list_diagnostics_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token.token}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_list_diagnostics(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 2)
        # ordered by year ascending
        self.assertEqual(results[0]["id"], self.diagnostic_2024.id)
        self.assertEqual(results[1]["id"], self.diagnostic_2025.id)
        # no volet fields
        self.assertIn("centralKitchenDiagnosticMode", results[0])
        self.assertNotIn("diagnosticType", results[0])
        self.assertNotIn("valeurTotale", results[0])
        self.assertNotIn("diagnosticGaspillageRealise", results[0])


class DiagnosticV2CreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.url = reverse("diagnostic_v2_list_create", kwargs={"canteen_pk": cls.canteen.id})

    def test_cannot_create_diagnostic_if_unauthenticated(self):
        response = self.client.post(self.url, {"year": 2025})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_diagnostic_if_not_canteen_manager(self):
        response = self.client.post(self.url, {"year": 2025})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_diagnostic_via_oauth2(self):
        user, token = get_oauth2_token("canteen:write")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token.token}")
        response = self.client.post(self.url, {"year": 2025})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_diagnostic_without_year(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("year", response.json())

    @authenticate
    def test_create_diagnostic(self):
        self.canteen.managers.add(authenticate.user)

        payload = {
            "year": 2025,
            "centralKitchenDiagnosticMode": Diagnostic.CentralKitchenDiagnosticMode.ALL,
            "creationSource": CreationSource.APP,
            "creationMtmSource": "mtm_source_value",
            # volet fields are ignored
            "diagnosticType": Diagnostic.DiagnosticType.SIMPLE,
            "valeurTotale": 1000,
            "diagnosticGaspillageRealise": True,
        }
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        self.assertNotIn("creationSource", body)  # write-only
        diagnostic = Diagnostic.objects.get(id=body["id"])
        self.assertEqual(diagnostic.canteen, self.canteen)
        self.assertEqual(diagnostic.year, 2025)
        self.assertEqual(diagnostic.central_kitchen_diagnostic_mode, Diagnostic.CentralKitchenDiagnosticMode.ALL)
        self.assertEqual(diagnostic.creation_user, authenticate.user)
        self.assertEqual(diagnostic.creation_source, CreationSource.APP)
        self.assertEqual(diagnostic.creation_mtm_source, "mtm_source_value")
        self.assertIsNone(diagnostic.diagnostic_type)
        self.assertIsNone(diagnostic.valeur_totale)
        self.assertIsNone(diagnostic.diagnostic_gaspillage_realise)

    @authenticate
    def test_cannot_create_diagnostic_if_already_exists(self):
        self.canteen.managers.add(authenticate.user)
        DiagnosticFactory(canteen=self.canteen, year=2025)

        with transaction.atomic():
            response = self.client.post(self.url, {"year": 2025})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Diagnostic.objects.filter(canteen=self.canteen, year=2025).count(), 1)


class DiagnosticV2RetrieveUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.diagnostic = DiagnosticFactory(canteen=cls.canteen, year=2025, creation_source=CreationSource.APP)
        cls.url = reverse(
            "diagnostic_v2_retrieve_update", kwargs={"canteen_pk": cls.canteen.id, "pk": cls.diagnostic.id}
        )

    def test_cannot_retrieve_diagnostic_if_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_diagnostic_if_not_canteen_manager(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_diagnostic_of_another_canteen(self):
        other_canteen = CanteenFactory(managers=[authenticate.user])

        response = self.client.get(
            reverse("diagnostic_v2_retrieve_update", kwargs={"canteen_pk": other_canteen.id, "pk": self.diagnostic.id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_retrieve_diagnostic(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.diagnostic.id)
        self.assertEqual(body["year"], 2025)
        self.assertNotIn("valeurTotale", body)

    @authenticate
    def test_cannot_update_diagnostic_with_put(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.put(self.url, {"year": 2025})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_update_diagnostic(self):
        self.canteen.managers.add(authenticate.user)

        payload = {
            "centralKitchenDiagnosticMode": Diagnostic.CentralKitchenDiagnosticMode.APPRO,
            # read-only / create-only / volet fields are ignored
            "year": 2024,
            "creationSource": CreationSource.API,
            "valeurTotale": 1,
        }
        response = self.client.patch(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diagnostic.refresh_from_db()
        self.assertEqual(
            self.diagnostic.central_kitchen_diagnostic_mode, Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        self.assertEqual(self.diagnostic.year, 2025)
        self.assertEqual(self.diagnostic.creation_source, CreationSource.APP)
        self.assertNotEqual(self.diagnostic.valeur_totale, 1)

    @authenticate
    def test_cannot_update_diagnostic_teledeclared(self):
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        with freeze_time("2022-08-30"):  # during the 2021 campaign
            diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.patch(
            reverse(
                "diagnostic_v2_retrieve_update", kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id}
            ),
            {"centralKitchenDiagnosticMode": Diagnostic.CentralKitchenDiagnosticMode.APPRO},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DiagnosticVoletApprovisionnementV2ApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.diagnostic_simple_2025 = DiagnosticFactory(
            canteen=cls.canteen,
            year=2025,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            diagnostic_gaspillage_realise=False,
        )
        cls.diagnostic_complete_2026 = DiagnosticFactory(
            canteen=cls.canteen, year=2026, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE
        )
        cls.diagnostic_without_type_2024 = DiagnosticFactory(canteen=cls.canteen, year=2024, diagnostic_type=None)

    def _url(self, diagnostic):
        return reverse(
            "diagnostic_v2_approvisionnement_retrieve_update",
            kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
        )

    def test_cannot_retrieve_approvisionnement_if_unauthenticated(self):
        response = self.client.get(self._url(self.diagnostic_simple_2025))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_approvisionnement_if_not_canteen_manager(self):
        response = self.client.get(self._url(self.diagnostic_simple_2025))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_retrieve_approvisionnement_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token.token}")
        response = self.client.get(self._url(self.diagnostic_simple_2025))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_retrieve_approvisionnement_if_diagnostic_unknown(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(
            reverse(
                "diagnostic_v2_approvisionnement_retrieve_update", kwargs={"canteen_pk": self.canteen.id, "pk": 9999}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_retrieve_approvisionnement_fields_depend_on_year_and_diagnostic_type(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self._url(self.diagnostic_simple_2025))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], self.diagnostic_simple_2025.id)
        self.assertEqual(body["diagnosticType"], Diagnostic.DiagnosticType.SIMPLE)
        self.assertIn("valeurBio", body)
        self.assertIn("pourcentageBio", body)  # stats (read-only)
        self.assertNotIn("valeurViandesVolaillesBio", body)  # COMPLETE only
        self.assertNotIn("nombreRepasAn", body)  # since 2026
        self.assertNotIn("diagnosticGaspillageRealise", body)  # other volet

        response = self.client.get(self._url(self.diagnostic_complete_2026))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("valeurViandesVolaillesBio", body)
        self.assertIn("valeurViandesVolaillesAocaop", body)  # since 2026
        self.assertNotIn("valeurViandesVolaillesAocaopIgpStg", body)  # removed in 2026
        self.assertIn("nombreRepasAn", body)
        self.assertIn("definitionLocal", body)

    @authenticate
    def test_retrieve_approvisionnement_without_diagnostic_type(self):
        self.canteen.managers.add(authenticate.user)

        response = self.client.get(self._url(self.diagnostic_without_type_2024))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIsNone(body["diagnosticType"])
        self.assertNotIn("valeurTotale", body)

    @authenticate
    def test_update_approvisionnement(self):
        self.canteen.managers.add(authenticate.user)

        payload = {
            "valeurTotale": 1000,
            "valeurBio": 200,
            "tunnelAppro": "bio",
            # ignored: read-only, other diagnostic_type, other volet
            "year": 2024,
            "pourcentageBio": 0.99,
            "valeurViandesVolaillesBio": 50,
            "diagnosticGaspillageRealise": True,
        }
        response = self.client.patch(self._url(self.diagnostic_simple_2025), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.diagnostic_simple_2025.refresh_from_db()
        self.assertEqual(self.diagnostic_simple_2025.valeur_totale, 1000)
        self.assertEqual(self.diagnostic_simple_2025.valeur_bio, 200)
        self.assertEqual(self.diagnostic_simple_2025.tunnel_appro, "bio")
        self.assertEqual(self.diagnostic_simple_2025.year, 2025)
        self.assertNotEqual(self.diagnostic_simple_2025.pourcentage_bio, 0.99)  # computed on save
        self.assertNotEqual(self.diagnostic_simple_2025.valeur_viandes_volailles_bio, 50)
        self.assertFalse(self.diagnostic_simple_2025.diagnostic_gaspillage_realise)

    @authenticate
    def test_update_approvisionnement_with_new_diagnostic_type(self):
        """
        The fields of the new diagnostic_type are accepted in the same request
        """
        self.canteen.managers.add(authenticate.user)

        payload = {
            "diagnosticType": Diagnostic.DiagnosticType.COMPLETE,
            "valeurTotale": 1000,
            "valeurViandesVolaillesBio": 50,
        }
        response = self.client.patch(self._url(self.diagnostic_without_type_2024), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        # the response has the fields of the new diagnostic_type
        self.assertEqual(
            len(body.keys() & {camelize(field) for field in Diagnostic.APPRO_FIELDS}),
            len(get_teledeclaration_fields_all(2024, "APPROVISIONNEMENT", Diagnostic.DiagnosticType.COMPLETE)),
        )
        self.assertIn("valeurViandesVolaillesBio", body)
        self.assertNotIn("valeurBio", body)  # SIMPLE only
        self.diagnostic_without_type_2024.refresh_from_db()
        self.assertEqual(self.diagnostic_without_type_2024.diagnostic_type, Diagnostic.DiagnosticType.COMPLETE)
        self.assertEqual(self.diagnostic_without_type_2024.valeur_viandes_volailles_bio, 50)

    @authenticate
    def test_cannot_update_approvisionnement_teledeclared(self):
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        with freeze_time("2022-08-30"):  # during the 2021 campaign
            diagnostic.teledeclare(applicant=authenticate.user)

        response = self.client.patch(self._url(diagnostic), {"valeurTotale": 1}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_can_update_approvisionnement_cancelled(self):
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        with freeze_time("2022-08-30"):  # during the 2021 campaign
            diagnostic.teledeclare(applicant=authenticate.user)
            diagnostic.cancel()

        response = self.client.patch(self._url(diagnostic), {"tunnelAppro": "fin"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.tunnel_appro, "fin")


class DiagnosticV2DocumentationTest(APITestCase):
    def test_v2_endpoints_are_not_in_the_api_docs(self):
        response = self.client.get(reverse("schema"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("/api/v1/canteens/{canteen_pk}/diagnostics/", response.content.decode())
        self.assertNotIn("/api/v2/", response.content.decode())


class DiagnosticV2UrlsTest(APITestCase):
    def test_volet_urls(self):
        for url_name, path in [
            ("diagnostic_v2_approvisionnement_retrieve_update", "approvisionnements"),
            ("diagnostic_v2_gaspillage_retrieve_update", "gaspillage-alimentaire"),
            ("diagnostic_v2_diversification_retrieve_update", "menus-vegetariens"),
            ("diagnostic_v2_plastique_retrieve_update", "substitution-plastique"),
            ("diagnostic_v2_information_retrieve_update", "information-convives"),
        ]:
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    reverse(url_name, kwargs={"canteen_pk": 1, "pk": 2}), f"/api/v2/canteens/1/diagnostics/2/{path}"
                )


class DiagnosticOtherVoletsV2ApiTest(APITestCase):
    """
    Common behaviour of the gaspillage / diversification / plastique / information volets
    """

    VOLETS = [
        # (url name, a field of the volet, its model field, a value, tunnel model field)
        ("gaspillage", "planGaspillageEnPlace", "plan_gaspillage_en_place", True, "tunnel_waste"),
        (
            "diversification",
            "planDiversificationEnPlace",
            "plan_diversification_en_place",
            True,
            "tunnel_diversification",
        ),
        ("plastique", "cookingPlasticSubstituted", "cooking_plastic_substituted", True, "tunnel_plastic"),
        ("information", "communicatesOnFoodPlan", "communicates_on_food_plan", True, "tunnel_info"),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory()
        cls.diagnostic = DiagnosticFactory(
            canteen=cls.canteen,
            year=2025,
            valeur_totale=1000,
            plan_gaspillage_en_place=False,
            plan_diversification_en_place=False,
            cooking_plastic_substituted=False,
            communicates_on_food_plan=False,
        )

    def _url(self, volet, diagnostic):
        return reverse(
            f"diagnostic_v2_{volet}_retrieve_update",
            kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
        )

    def test_cannot_access_volet_if_unauthenticated(self):
        for volet, *_ in self.VOLETS:
            with self.subTest(volet=volet):
                self.assertEqual(self.client.get(self._url(volet, self.diagnostic)).status_code, 403)
                self.assertEqual(self.client.patch(self._url(volet, self.diagnostic), {}).status_code, 403)

    @authenticate
    def test_cannot_access_volet_if_not_canteen_manager(self):
        for volet, *_ in self.VOLETS:
            with self.subTest(volet=volet):
                self.assertEqual(self.client.get(self._url(volet, self.diagnostic)).status_code, 403)

    def test_cannot_access_volet_via_oauth2(self):
        user, token = get_oauth2_token("canteen:read")
        self.canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token.token}")
        for volet, *_ in self.VOLETS:
            with self.subTest(volet=volet):
                self.assertEqual(self.client.get(self._url(volet, self.diagnostic)).status_code, 403)

    @authenticate
    def test_retrieve_volet(self):
        self.canteen.managers.add(authenticate.user)

        for volet, field, _, _, _ in self.VOLETS:
            with self.subTest(volet=volet):
                response = self.client.get(self._url(volet, self.diagnostic))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                body = response.json()
                self.assertEqual(body["id"], self.diagnostic.id)
                self.assertEqual(body["year"], 2025)
                self.assertIn(field, body)
                # other volets
                self.assertNotIn("valeurTotale", body)
                for other_volet, other_field, *_ in self.VOLETS:
                    if other_volet != volet:
                        self.assertNotIn(other_field, body)

    @authenticate
    def test_update_volet(self):
        self.canteen.managers.add(authenticate.user)

        for volet, field, model_field, value, tunnel_field in self.VOLETS:
            with self.subTest(volet=volet):
                payload = {
                    field: value,
                    camelize(tunnel_field): "fin",
                    # ignored: read-only, other volet
                    "year": 2024,
                    "valeurTotale": 1,
                }
                response = self.client.patch(self._url(volet, self.diagnostic), payload, format="json")

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.diagnostic.refresh_from_db()
                self.assertEqual(getattr(self.diagnostic, model_field), value)
                self.assertEqual(getattr(self.diagnostic, tunnel_field), "fin")
                self.assertEqual(self.diagnostic.year, 2025)
                self.assertEqual(self.diagnostic.valeur_totale, 1000)

    @authenticate
    def test_cannot_update_volet_teledeclared(self):
        diagnostic = DiagnosticFactory(year=2021)
        diagnostic.canteen.managers.add(authenticate.user)
        with freeze_time("2022-08-30"):  # during the 2021 campaign
            diagnostic.teledeclare(applicant=authenticate.user)

        for volet, field, _, value, _ in self.VOLETS:
            with self.subTest(volet=volet):
                response = self.client.patch(self._url(volet, diagnostic), {field: value}, format="json")

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DiagnosticVoletGaspillageV2ApiTest(APITestCase):
    @freeze_time("2024-03-01")  # during the 2023 campaign
    @authenticate
    def test_dechets_total_conversion(self):
        """
        dechets_total (legacy, 2023 only): in kg in the API, stored in tons
        """
        diagnostic = DiagnosticFactory(year=2023, dechets_total=Decimal("1.23456"))
        diagnostic.canteen.managers.add(authenticate.user)
        url = reverse(
            "diagnostic_v2_gaspillage_retrieve_update",
            kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(str(response.json()["dechetsTotal"])), Decimal("1234.56"))

        response = self.client.patch(url, {"dechetsTotal": 6666.66}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.dechets_total, Decimal("6.66666"))

    @authenticate
    def test_dechets_fields_only_in_2023(self):
        for year, has_dechets_fields in [(2022, False), (2023, True), (2024, False), (2025, False)]:
            with self.subTest(year=year):
                diagnostic = DiagnosticFactory(year=year)
                diagnostic.canteen.managers.add(authenticate.user)

                response = self.client.get(
                    reverse(
                        "diagnostic_v2_gaspillage_retrieve_update",
                        kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
                    )
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual("dechetsTotal" in response.json(), has_dechets_fields)

    @authenticate
    def test_choice_values_in_french(self):
        diagnostic = DiagnosticFactory(
            year=2025, actions_gaspillage_realisees=[Diagnostic.ActionsGaspillage.SENSIBILISATION]
        )
        diagnostic.canteen.managers.add(authenticate.user)
        url = reverse(
            "diagnostic_v2_gaspillage_retrieve_update",
            kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
        )

        self.assertEqual(self.client.get(url).json()["actionsGaspillageRealisees"], ["SENSIBILISATION"])

        response = self.client.patch(url, {"actionsGaspillageRealisees": ["FORMATION"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.actions_gaspillage_realisees, [Diagnostic.ActionsGaspillage.FORMATION])

        # the v1 (English) values are not accepted
        response = self.client.patch(url, {"actionsGaspillageRealisees": ["TRAINING"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DiagnosticVoletDiversificationV2ApiTest(APITestCase):
    @authenticate
    def test_service_type_only_since_2024(self):
        for year, has_service_type in [(2023, False), (2024, True), (2026, True)]:
            with self.subTest(year=year):
                diagnostic = DiagnosticFactory(year=year)
                diagnostic.canteen.managers.add(authenticate.user)

                response = self.client.get(
                    reverse(
                        "diagnostic_v2_diversification_retrieve_update",
                        kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
                    )
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual("serviceType" in response.json(), has_service_type)

    @authenticate
    def test_choice_values_in_french(self):
        """
        v2 uses the model (French) choice values (v1 keeps the English ones, see V1_CHOICE_VALUE_ALIASES)
        """
        diagnostic = DiagnosticFactory(
            year=2025,
            service_type=Diagnostic.ServiceType.MENU_UNIQUE,
            menu_vegetarien_frequence=Diagnostic.MenuVegetarienFrequence.HEBDO,
        )
        diagnostic.canteen.managers.add(authenticate.user)
        url = reverse(
            "diagnostic_v2_diversification_retrieve_update",
            kwargs={"canteen_pk": diagnostic.canteen.id, "pk": diagnostic.id},
        )

        body = self.client.get(url).json()
        self.assertEqual(body["serviceType"], "MENU_UNIQUE")
        self.assertEqual(body["menuVegetarienFrequence"], "HEBDO")

        payload = {"serviceType": "CHOIX_MULTIPLE_RESERVATION", "menuVegetarienBases": ["SOJA", "OEUFS"]}
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["serviceType"], "CHOIX_MULTIPLE_RESERVATION")
        self.assertEqual(response.json()["menuVegetarienBases"], ["SOJA", "OEUFS"])
        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.service_type, Diagnostic.ServiceType.CHOIX_MULTIPLE_RESERVATION)

        # the v1 (English) values are not accepted
        response = self.client.patch(url, {"serviceType": "MULTIPLE_SELF"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
