import base64
import os
from decimal import Decimal

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory, ManagerInvitationFactory
from data.models import Canteen, Diagnostic, Sector, Teledeclaration
from data.models.creation_source import CreationSource

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


CANTEEN_SITE_DEFAULT_PAYLOAD = {
    "name": "My canteen",
    "city": "Roubaix",
    "siret": "92341284500011",
    "daily_meal_count": 12,
    "yearly_meal_count": 1000,
    "management_type": Canteen.ManagementType.DIRECT,
    "production_type": Canteen.ProductionType.ON_SITE,
    "economic_model": Canteen.EconomicModel.PUBLIC,
    "sector_list": [Sector.EDUCATION_PRIMAIRE, Sector.ENTERPRISE_ENTREPRISE],
}


class CanteenListApiTest(APITestCase):
    def test_cannot_get_user_canteens_unauthenticated(self):
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_canteens_wrong_token(self):
        _, token = get_oauth2_token("user:read")
        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_canteens_correct_token(self):
        user, token = get_oauth2_token("canteen:read")
        canteen = CanteenFactory(managers=[user])

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["count"], 1)
        self.assertEqual(body["results"][0]["id"], canteen.id)

    @authenticate
    def test_get_user_canteens(self):
        """
        Users can have access to the full representation of their
        canteens (even if they are not published). This endpoint
        is paginated
        """
        user_canteens = [
            ManagerInvitationFactory().canteen,
            ManagerInvitationFactory().canteen,
        ]
        other_canteens = [
            CanteenFactory(),
            CanteenFactory(),
        ]
        for canteen in user_canteens:
            canteen.managers.set([authenticate.user])

        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results")

        for user_canteen in user_canteens:
            self.assertTrue(any(x["id"] == user_canteen.id for x in body))

        for received_canteen in body:
            self.assertEqual(received_canteen["managers"][0]["email"], authenticate.user.email)
            self.assertTrue("email" in received_canteen["managerInvitations"][0])

        for other_canteen in other_canteens:
            self.assertFalse(any(x["id"] == other_canteen.id for x in body))

    @authenticate
    def test_get_canteens_without_tracking_info(self):
        """
        Full representation should not contain the tracking info
        """
        CanteenFactory(
            creation_mtm_source="mtm_source_value",
            creation_mtm_campaign="mtm_campaign_value",
            creation_mtm_medium="mtm_medium_value",
            managers=[authenticate.user],
        )
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results")[0]

        self.assertNotIn("mtm_source_value", body)
        self.assertNotIn("mtm_campaign_value", body)
        self.assertNotIn("mtm_medium_value", body)


class CanteenListFilterApiTest(APITestCase):
    @authenticate
    def test_get_canteens_filter_production_type(self):
        CanteenFactory(production_type="site", managers=[authenticate.user])
        user_central_cuisine = CanteenFactory(production_type="central", managers=[authenticate.user])
        user_central_serving_cuisine = CanteenFactory(production_type="central_serving", managers=[authenticate.user])

        response = self.client.get(f"{reverse('user_canteens')}?production_type=central,central_serving")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["count"], 2)
        ids = list(map(lambda x: x["id"], body["results"]))
        self.assertIn(user_central_cuisine.id, ids)
        self.assertIn(user_central_serving_cuisine.id, ids)


class CanteenListPreviewApiTest(APITestCase):
    @authenticate
    def test_get_canteens_preview(self):
        """
        Users can have access to the preview of their
        canteens (even if they are not published).
        """
        user_canteens = [
            CanteenFactory(managers=[authenticate.user]),
            CanteenFactory(managers=[authenticate.user]),
        ]
        _ = [
            CanteenFactory(),
            CanteenFactory(),
        ]

        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 2)
        self.assertEqual(body[0].get("id"), user_canteens[1].id)
        self.assertEqual(body[1].get("id"), user_canteens[0].id)

    def test_canteen_preview_wrong_token(self):
        user, token = get_oauth2_token("user:read")
        CanteenFactory(managers=[user])

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_canteen_preview_correct_token(self):
        user, token = get_oauth2_token("canteen:read")
        canteen = CanteenFactory(managers=[user])

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["id"], canteen.id)


class CanteenDetailApiTest(APITestCase):
    def test_cannot_get_single_user_canteen_unauthorized(self):
        """
        Users cannot access to the full representation of a single
        canteen if they are not authenticated
        """
        canteen = CanteenFactory()

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_get_single_user_canteen_unknown(self):
        """
        Users cannot access the full representation of a single
        canteen that does not exist.
        """
        response = self.client.get(reverse("single_canteen", kwargs={"pk": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_cannot_get_single_user_canteen_if_not_manager(self):
        """
        Users cannot access the full representation of a single
        canteen if they do not manage it.
        """
        canteen = CanteenFactory()

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_single_user_canteen(self):
        """
        Users can access the full representation of a single
        canteen as long as they manage it.
        """
        user_canteen = CanteenFactory(managers=[authenticate.user])

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], user_canteen.id)
        self.assertEqual(body["managers"][0]["email"], authenticate.user.email)

    @authenticate
    def test_get_single_user_canteen_groupe(self):
        """
        The full representation of a canteen contains the groupe info
        """
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        user_canteen = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, groupe=canteen_groupe, managers=[authenticate.user]
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], user_canteen.id)
        self.assertEqual(body["groupe"]["id"], canteen_groupe.id)
        self.assertEqual(body["groupe"]["name"], canteen_groupe.name)
        self.assertEqual(body["satellitesCount"], 0)

        # make user the manager of the groupe canteen as well
        canteen_groupe.managers.add(authenticate.user)
        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen_groupe.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen_groupe.id)
        self.assertIsNone(body["groupe"])
        self.assertEqual(body["satellitesCount"], 1)

    @authenticate
    def test_get_numeric_appro_values(self):
        """
        The endpoint for canteen managers should return the economic data of the appro
        values - as opposed to the published endpoint which returns percentage values
        """
        user_canteen = CanteenFactory(managers=[authenticate.user])
        DiagnosticFactory(
            canteen=user_canteen,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            year=2021,
            valeur_totale=1200,
            valeur_bio=600,
            valeur_siqo=300,
            total_leftovers=Decimal("1.23456"),
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))

        body = response.json()
        self.assertEqual(len(body.get("diagnostics")), 1)
        serialized_diag = body.get("diagnostics")[0]
        self.assertEqual(serialized_diag["valeurTotale"], 1200)
        self.assertEqual(serialized_diag["valeurBio"], 600)
        self.assertEqual(serialized_diag["valeurSiqo"], 300)
        # total_leftovers should be converted from ton to kg
        self.assertEqual(serialized_diag["totalLeftovers"], 1234.56)

    @authenticate
    def test_get_canteen_without_tracking(self):
        """
        Full representation should not contain the tracking info
        """
        user_canteen = CanteenFactory(
            creation_mtm_source="mtm_source_value",
            creation_mtm_campaign="mtm_campaign_value",
            creation_mtm_medium="mtm_medium_value",
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("mtm_source_value", body)
        self.assertNotIn("mtm_campaign_value", body)
        self.assertNotIn("mtm_medium_value", body)

    @authenticate
    def test_user_canteen_teledeclaration(self):
        """
        Only submitted TDs are returned to the managers
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        diagnostic = DiagnosticFactory(canteen=canteen, year=2020)

        # submit a teledeclaration
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("user_canteens"))
        body = response.json().get("results")
        json_canteen = next(filter(lambda x: x["id"] == canteen.id, body))
        json_diagnostic = next(filter(lambda x: x["id"] == diagnostic.id, json_canteen["diagnostics"]))
        self.assertEqual(json_diagnostic["teledeclaration"]["id"], teledeclaration.id)

        # cancel the teledeclaration
        teledeclaration.cancel()

        response = self.client.get(reverse("user_canteens"))
        body = response.json().get("results")
        json_canteen = next(filter(lambda x: x["id"] == canteen.id, body))
        json_diagnostic = next(filter(lambda x: x["id"] == diagnostic.id, json_canteen["diagnostics"]))
        self.assertIsNone(json_diagnostic["teledeclaration"])

    @authenticate
    def test_get_central_kitchen(self):
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe,
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen_satellite.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["centralKitchen"]["name"], canteen_groupe.name)
        self.assertEqual(body["centralKitchen"]["id"], canteen_groupe.id)

    @authenticate
    @freeze_time("2024-01-20")
    def test_canteen_badges(self):
        """
        The full representation of a canteen contains the badges earned for last year
        A badge can be True, False, or None. None = !True and the tunnel wasn't started,
        False = !True and the tunnel was started.
        """
        user_canteen = CanteenFactory(managers=[authenticate.user])

        DiagnosticFactory(
            canteen=user_canteen,
            year=2023,
            # test appro badge as true
            valeur_totale=100,
            valeur_bio=20,
            valeur_siqo=30,
            # test plastic badge as false
            tunnel_plastic="something",
            cooking_plastic_substituted=False,
            # test vege badge as null
            tunnel_diversification=None,
            vegetarian_weekly_recurrence=None,
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        badges = body["badges"]
        self.assertTrue(badges["appro"])
        self.assertIs(badges["plastic"], False)
        self.assertIsNone(badges["diversification"])

    @authenticate
    @freeze_time("2024-01-20")
    def test_canteen_badges_vegetarian_diversification_plan_rule(self):
        canteen_199_daily_meals = CanteenFactory(managers=[authenticate.user], daily_meal_count=199)
        DiagnosticFactory(
            canteen=canteen_199_daily_meals,
            year=2023,
            has_diversification_plan=True,
            vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.NEVER,
        )

        canteen_200_daily_meals = CanteenFactory(managers=[authenticate.user], daily_meal_count=200)
        DiagnosticFactory(
            canteen=canteen_200_daily_meals,
            year=2023,
            has_diversification_plan=True,
            vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.NEVER,
        )

        canteen_201_daily_meals = CanteenFactory(managers=[authenticate.user], daily_meal_count=201)
        DiagnosticFactory(
            canteen=canteen_201_daily_meals,
            year=2023,
            has_diversification_plan=True,
            vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.NEVER,
        )

        response_canteen_199 = self.client.get(reverse("single_canteen", kwargs={"pk": canteen_199_daily_meals.id}))
        self.assertEqual(response_canteen_199.status_code, status.HTTP_200_OK)
        body = response_canteen_199.json()
        self.assertIs(body["dailyMealCount"], 199)
        self.assertIs(body["badges"]["diversification"], None)

        response_canteen_200 = self.client.get(reverse("single_canteen", kwargs={"pk": canteen_200_daily_meals.id}))
        self.assertEqual(response_canteen_200.status_code, status.HTTP_200_OK)
        body = response_canteen_200.json()
        self.assertIs(body["dailyMealCount"], 200)
        self.assertIs(body["badges"]["diversification"], True)

        response_canteen_201 = self.client.get(reverse("single_canteen", kwargs={"pk": canteen_201_daily_meals.id}))
        self.assertEqual(response_canteen_201.status_code, status.HTTP_200_OK)
        body = response_canteen_201.json()
        self.assertIs(body["dailyMealCount"], 201)
        self.assertIs(body["badges"]["diversification"], True)

    @authenticate
    def test_canteen_returns_latest_diagnostic_year(self):
        """
        Test whether the canteen returns the latest year it has data for
        """
        canteen_groupe = CanteenFactory(production_type=Canteen.ProductionType.GROUPE)
        canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            groupe=canteen_groupe,
            managers=[authenticate.user],
        )
        DiagnosticFactory(
            canteen=canteen_satellite,
            year=2021,
            valeur_totale=100,
            valeur_bio=0,
            valeur_siqo=30,
        )
        DiagnosticFactory(
            canteen=canteen_groupe,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            year=2022,
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen_satellite.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["badges"]["year"], 2022)


class CanteenCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_cannot_create_canteen_unauthenticated(self):
        response = self.client.post(reverse("user_canteens"), CANTEEN_SITE_DEFAULT_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_create_canteen_central(self):
        response = self.client.post(
            reverse("user_canteens"),
            {**CANTEEN_SITE_DEFAULT_PAYLOAD, "productionType": Canteen.ProductionType.CENTRAL},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(
            body["production_type"],
            ["La création de cantines de type CENTRAL ou CENTRAL_SERVING n'est plus autorisée."],
        )

    @authenticate
    def test_create_canteen(self):
        response = self.client.post(reverse("user_canteens"), CANTEEN_SITE_DEFAULT_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertIn(authenticate.user, created_canteen.managers.all())

    @authenticate
    def test_create_canteen_creation_source(self):
        # from the APP
        response = self.client.post(
            reverse("user_canteens"), {**CANTEEN_SITE_DEFAULT_PAYLOAD, "creation_source": "APP"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_source, CreationSource.APP)
        created_canteen.hard_delete()

        # defaults to API
        response = self.client.post(reverse("user_canteens"), CANTEEN_SITE_DEFAULT_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_source, CreationSource.API)
        created_canteen.hard_delete()

        # returns a 404 if the creation_source is not valid
        response = self.client.post(
            reverse("user_canteens"), {**CANTEEN_SITE_DEFAULT_PAYLOAD, "creation_source": "UNKNOWN"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_cannot_create_canteen_without_siret(self):
        payload = CANTEEN_SITE_DEFAULT_PAYLOAD.copy()
        del payload["siret"]

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Ce champ est obligatoire."])

    @authenticate
    def test_cannot_create_canteen_with_bad_siret(self):
        response = self.client.post(reverse("user_canteens"), {**CANTEEN_SITE_DEFAULT_PAYLOAD, "siret": "0123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["14 caractères numériques sont attendus"])

        response = self.client.post(
            reverse("user_canteens"), {**CANTEEN_SITE_DEFAULT_PAYLOAD, "siret": "01234567891011"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(
            body["siret"][0],
            "Le numéro SIRET est invalide et semble ne pas exister dans les registres officiels, vous pouvez vérifier sa validité depuis le site : https://annuaire-entreprises.data.gouv.fr",
        )

        response = self.client.post(
            reverse("user_canteens"),
            {
                **CANTEEN_SITE_DEFAULT_PAYLOAD,
                "siret": "01234567891011",
                "productionType": Canteen.ProductionType.ON_SITE_CENTRAL,
                "centralProducerSiret": "01234567891011",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(
            body["centralProducerSiret"][0],
            "Le numéro SIRET est invalide et semble ne pas exister dans les registres officiels, vous pouvez vérifier sa validité depuis le site : https://annuaire-entreprises.data.gouv.fr",
        )

    @authenticate
    def test_cannot_create_canteen_with_duplicate_siret(self):
        """
        If attempt to create a canteen with the same SIRET as one that I manage already, give
        me 400 with canteen name and id
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret)

        response = self.client.post(reverse("user_canteens"), {**CANTEEN_SITE_DEFAULT_PAYLOAD, "siret": siret})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertFalse(body["isManagedByUser"])
        self.assertEqual(Canteen.objects.count(), 1)

        # make the user the manager of the canteen
        canteen.managers.add(authenticate.user)

        response = self.client.post(reverse("user_canteens"), {**CANTEEN_SITE_DEFAULT_PAYLOAD, "siret": siret})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertTrue(body["isManagedByUser"])
        self.assertEqual(Canteen.objects.count(), 1)

    @authenticate
    def test_create_canteen_with_images(self):
        """
        The app should create the necessary image models upon the creation of a canteen
        """
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = CANTEEN_SITE_DEFAULT_PAYLOAD.copy()
        payload["images"] = [
            {
                "image": "data:image/jpeg;base64," + image_base_64,
            }
        ]

        response = self.client.post(reverse("user_canteens"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.images.count(), 1)

    @authenticate
    def test_create_canteen_with_tracking_info(self):
        """
        The app should store the mtm parameters on creation
        """
        payload = CANTEEN_SITE_DEFAULT_PAYLOAD.copy()
        payload["creation_mtm_source"] = "mtm_source_value"
        payload["creation_mtm_campaign"] = "mtm_campaign_value"
        payload["creation_mtm_medium"] = "mtm_medium_value"

        response = self.client.post(reverse("user_canteens"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_mtm_source, "mtm_source_value")
        self.assertEqual(created_canteen.creation_mtm_campaign, "mtm_campaign_value")
        self.assertEqual(created_canteen.creation_mtm_medium, "mtm_medium_value")


class CanteenUpdateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen = CanteenFactory(**CANTEEN_SITE_DEFAULT_PAYLOAD)

    @authenticate
    def test_cannot_update_canteen_with_put(self):
        payload = {"management_type": Canteen.ManagementType.CONCEDED}

        response = self.client.put(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_update_canteen_if_unauthenticated(self):
        payload = {"management_type": Canteen.ManagementType.CONCEDED}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_cannot_update_canteen_if_not_manager(self):
        payload = {"management_type": Canteen.ManagementType.CONCEDED}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_update_canteen(self):
        self.assertEqual(self.canteen.city, "Roubaix")
        self.canteen.managers.add(authenticate.user)

        payload = {
            "siret": "21340172201787",
            "city": "Montpellier",  # siret changed, geo fields will be reset
            "managementType": Canteen.ManagementType.CONCEDED,
            "reservationExpeParticipant": True,
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.siret, "21340172201787")
        self.assertEqual(self.canteen.city, None)
        self.assertEqual(self.canteen.management_type, Canteen.ManagementType.CONCEDED)
        self.assertEqual(self.canteen.reservation_expe_participant, True)

    @authenticate
    def test_update_canteen_production_type(self):
        self.assertEqual(self.canteen.production_type, Canteen.ProductionType.ON_SITE)
        self.canteen.managers.add(authenticate.user)

        payload = {
            "productionType": Canteen.ProductionType.ON_SITE_CENTRAL,
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.production_type, Canteen.ProductionType.ON_SITE_CENTRAL)

    @authenticate
    def test_cannot_update_canteen_with_new_empty_siret(self):
        self.assertEqual(self.canteen.siret, "92341284500011")
        self.canteen.managers.add(authenticate.user)

        for siret in ["", None]:
            payload = {"siret": siret}
            response = self.client.patch(
                reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json"
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            body = response.json()
            self.assertEqual(body["siret"], ["Le numéro SIRET ne peut pas être vide."])
            self.canteen.refresh_from_db()
            self.assertEqual(self.canteen.siret, "92341284500011")

    @authenticate
    def test_cannot_update_canteen_if_duplicate_siret(self):
        siret_2 = "21340172201787"
        canteen_2 = CanteenFactory(siret=siret_2)
        self.assertEqual(self.canteen.siret, "92341284500011")
        self.canteen.managers.add(authenticate.user)

        payload = {"siret": siret_2}
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen_2.name)
        self.assertEqual(body["id"], canteen_2.id)
        self.assertEqual(body["detail"], "La resource que vous souhaitez créer existe déjà")
        self.assertFalse(body["isManagedByUser"])

        # same if the user is manager of the other canteen
        canteen_2.managers.add(authenticate.user)

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen_2.name)
        self.assertEqual(body["id"], canteen_2.id)
        self.assertTrue(body["isManagedByUser"])  # changed

    @authenticate
    def test_update_canteen_with_own_siret(self):
        self.assertEqual(self.canteen.siret, "92341284500011")
        self.canteen.managers.add(authenticate.user)

        payload = {"siret": self.canteen.siret}
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_update_canteen_with_new_siret(self):
        siret_2 = "21340172201787"
        self.assertEqual(self.canteen.siret, "92341284500011")
        self.canteen.managers.add(authenticate.user)

        payload = {"siret": siret_2}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.siret, siret_2)
        self.assertEqual(self.canteen.city_insee_code, None)

    @authenticate
    def test_cannot_update_canteen_image_if_not_manager(self):
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "images": [
                {
                    "image": "data:image/jpeg;base64," + image_base_64,
                }
            ]
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.images.count(), 0)

    @authenticate
    def test_update_canteen_image_if_manager(self):
        self.canteen.managers.add(authenticate.user)
        self.assertEqual(self.canteen.images.count(), 0)

        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        # Create image
        payload = {
            "images": [
                {
                    "image": "data:image/jpeg;base64," + image_base_64,
                }
            ]
        }
        self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.images.count(), 1)

        # Delete image
        payload = {"images": []}
        self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.canteen.refresh_from_db()
        self.assertEqual(self.canteen.images.count(), 0)

    @authenticate
    def test_update_canteen_tracking_info(self):
        """
        The app should not allow the tracking info to be updated
        """
        self.assertEqual(self.canteen.creation_mtm_source, None)
        self.assertEqual(self.canteen.creation_mtm_campaign, None)
        self.assertEqual(self.canteen.creation_mtm_medium, None)
        self.canteen.managers.add(authenticate.user)

        payload = {
            "managementType": Canteen.ManagementType.CONCEDED,
            "creation_mtm_source": "mtm_source_value",
            "creation_mtm_campaign": "mtm_campaign_value",
            "creation_mtm_medium": "mtm_medium_value",
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": self.canteen.id}), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.canteen.refresh_from_db()
        self.assertIsNone(self.canteen.creation_mtm_source)
        self.assertIsNone(self.canteen.creation_mtm_campaign)
        self.assertIsNone(self.canteen.creation_mtm_medium)


class CanteenDeleteApiTest(APITestCase):
    @authenticate
    def test_soft_delete(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        response = self.client.delete(reverse("single_canteen", kwargs={"pk": canteen.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Model was only soft-deleted but remains in the DB
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
