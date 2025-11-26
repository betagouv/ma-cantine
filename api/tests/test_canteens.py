import base64
import os

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory, ManagerInvitationFactory
from data.models import Canteen, Diagnostic, Sector, Teledeclaration
from data.models.creation_source import CreationSource

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class CanteenListApiTest(APITestCase):
    def test_get_canteens_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the full representation of the canteens
        """
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
    @authenticate
    def test_get_single_user_canteen(self):
        """
        Users can access to the full representation of a single
        canteen as long as they manage it.
        """
        user_canteen = CanteenFactory(managers=[authenticate.user])

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["id"], user_canteen.id)
        self.assertEqual(body["managers"][0]["email"], authenticate.user.email)

    @authenticate
    def test_get_numeric_appro_values(self):
        """
        The endpoint for canteen managers should return the economic data of the appro
        values - as opposed to the published endpoint which returns percentage values
        """
        user_canteen = CanteenFactory(managers=[authenticate.user])

        DiagnosticFactory(
            canteen=user_canteen,
            year=2021,
            value_total_ht=1200,
            value_bio_ht=600,
            value_sustainable_ht=300,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))
        body = response.json()

        self.assertEqual(len(body.get("diagnostics")), 1)
        serialized_diag = body.get("diagnostics")[0]

        self.assertEqual(serialized_diag["valueTotalHt"], 1200)
        self.assertEqual(serialized_diag["valueBioHt"], 600)
        self.assertEqual(serialized_diag["valueSustainableHt"], 300)

    @authenticate
    def test_get_single_user_canteen_unauthorized(self):
        """
        Users cannot access to the full representation of a single
        canteen if they are not managers.
        """
        canteen = CanteenFactory()

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        central_kitchen = CanteenFactory(production_type=Canteen.ProductionType.CENTRAL, siret="96953195898254")
        satellite = CanteenFactory(
            central_producer_siret=central_kitchen.siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": satellite.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["centralKitchen"]["name"], central_kitchen.name)
        self.assertEqual(body["centralKitchen"]["id"], central_kitchen.id)

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
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=30,
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
    def test_canteen_returns_latest_diagnostic_year(self):
        """
        Test whether the canteen returns the latest year it has data for
        """
        central = CanteenFactory(siret="21340172201787", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(
            central_producer_siret="21340172201787",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            managers=[authenticate.user],
        )

        DiagnosticFactory(
            canteen=satellite,
            year=2021,
            value_total_ht=100,
            value_bio_ht=0,
            value_sustainable_ht=30,
        )
        DiagnosticFactory(
            canteen=central,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            year=2022,
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": satellite.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["badges"]["year"], 2022)


class CanteenCreateApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.DEFAULT_PAYLOAD = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
            "sectorList": [Sector.EDUCATION_PRIMAIRE, Sector.ENTERPRISE_ENTREPRISE],
        }

    @authenticate
    def test_create_canteen(self):
        response = self.client.post(reverse("user_canteens"), self.DEFAULT_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertIn(authenticate.user, created_canteen.managers.all())

    @authenticate
    def test_create_canteen_creation_source(self):
        # from the APP
        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "creation_source": "APP"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_source, CreationSource.APP)
        created_canteen.hard_delete()

        # defaults to API
        response = self.client.post(reverse("user_canteens"), self.DEFAULT_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_source, CreationSource.API)
        created_canteen.hard_delete()

        # returns a 404 if the creation_source is not valid
        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "creation_source": "UNKNOWN"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_canteen_missing_siret(self):
        payload = self.DEFAULT_PAYLOAD.copy()
        del payload["siret"]

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Ce champ est obligatoire."])

    @authenticate
    def test_create_canteen_bad_siret(self):
        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "siret": "0123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["14 caractères numériques sont attendus"])

        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "siret": "01234567891011"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET n'est pas valide."])

        response = self.client.post(
            reverse("user_canteens"),
            {
                **self.DEFAULT_PAYLOAD,
                "siret": "01234567891011",
                "productionType": Canteen.ProductionType.ON_SITE_CENTRAL,
                "centralProducerSiret": "01234567891011",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["centralProducerSiret"], ["Le numéro SIRET n'est pas valide."])

    @authenticate
    def test_create_canteen_duplicate_siret_managed(self):
        """
        If attempt to create a canteen with the same SIRET as one that I manage already, give
        me 400 with canteen name and id
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret, managers=[authenticate.user])

        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "siret": siret})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertTrue(body["isManagedByUser"])
        self.assertEqual(Canteen.objects.count(), 1)

    @authenticate
    def test_create_canteen_duplicate_siret_unmanaged(self):
        """
        If attempt to create a canteen with the same SIRET as one that I don't manage, give
        me 400 with canteen name
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret)

        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "siret": siret})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertFalse(body["isManagedByUser"])
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

        payload = self.DEFAULT_PAYLOAD.copy()
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
        The app should store the mtm paramteres on creation
        """
        payload = self.DEFAULT_PAYLOAD.copy()
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
    @authenticate
    def test_modify_canteen_unauthorized(self):
        """
        Users can only modify the canteens they manage
        """
        canteen = CanteenFactory(city="Paris")
        payload = {"city": "Lyon"}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_modify_canteen(self):
        """
        Users can modify the canteens they manage
        """
        canteen = CanteenFactory(city="Paris", managers=[authenticate.user])
        payload = {
            "city": "Lyon",
            "siret": "21340172201787",
            "managementType": Canteen.ManagementType.DIRECT,
            "reservationExpeParticipant": True,
        }

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(updated_canteen.city, "Lyon")
        self.assertEqual(updated_canteen.siret, "21340172201787")
        self.assertEqual(updated_canteen.management_type, "direct")
        self.assertEqual(updated_canteen.reservation_expe_participant, True)

    @authenticate
    def test_modify_canteen_production_type(self):
        """
        Users can modify the production type and related fields of the canteens they manage
        """
        canteen = CanteenFactory(city="Paris", managers=[authenticate.user])
        payload = {
            "productionType": Canteen.ProductionType.CENTRAL,
            "sectorList": [],
            "satelliteCanteensCount": 130,
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(updated_canteen.production_type, "central")
        self.assertEqual(len(updated_canteen.sector_list), 0)
        self.assertEqual(updated_canteen.satellite_canteens_count, 130)

    @authenticate
    def test_modify_central_kitchen_siret(self):
        """
        A change in the SIRET of a central cuisine must update the "central_producer_siret" of
        its satellites
        """
        central_kitchen = CanteenFactory(
            siret="03201976246133", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        satellites = [
            CanteenFactory(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="03201976246133"
            ),
            CanteenFactory(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="03201976246133"
            ),
            CanteenFactory(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="03201976246133"
            ),
        ]
        payload = {"siret": "35662897196149"}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": central_kitchen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for satellite in satellites:
            satellite.refresh_from_db()
            self.assertEqual(satellite.central_producer_siret, "35662897196149")

    @authenticate
    def test_add_siret_to_central_kitchen(self):
        """
        A central cuisine without a SIRET can add one without modifying everybody else
        """
        central_kitchen_without_siret = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        canteen_satellite = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen_without_siret.siret,
        )
        Canteen.objects.filter(id=central_kitchen_without_siret.id).update(siret=None)
        central_kitchen_without_siret.refresh_from_db()
        Canteen.objects.filter(id=canteen_satellite.id).update(central_producer_siret=None)
        canteen_satellite.refresh_from_db()
        canteen_central_serving = CanteenFactory(
            production_type=Canteen.ProductionType.CENTRAL_SERVING, central_producer_siret=None
        )
        canteen_on_site = CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, central_producer_siret=None)
        other_canteens = [canteen_satellite, canteen_central_serving, canteen_on_site]
        payload = {"siret": "35662897196149"}

        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": central_kitchen_without_siret.id}), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for canteen in other_canteens:
            canteen.refresh_from_db()
            self.assertIsNone(canteen.central_producer_siret)

    @authenticate
    def test_refuse_patch_without_siret(self):
        """
        A canteen modification shouldn't allow deleting a SIRET with sending blank or null value
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret, managers=[authenticate.user])

        # Test with blank value
        payload = {"siret": ""}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET ne peut pas être vide."])
        canteen.refresh_from_db()
        self.assertEqual(canteen.siret, siret)

        # Test with missing value
        payload = {"siret": None}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET ne peut pas être vide."])
        canteen.refresh_from_db()
        self.assertEqual(canteen.siret, siret)

    @authenticate
    def test_update_canteen_duplicate_siret_unmanaged(self):
        """
        If attempt to update a canteen with the same SIRET as one that I don't manage, give
        me 400 with canteen name
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret)
        canteen_to_test = CanteenFactory(managers=[authenticate.user])
        payload = {"siret": siret}

        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen_to_test.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["detail"], "La resource que vous souhaitez créer existe déjà")
        self.assertFalse(body["isManagedByUser"])

    @authenticate
    def test_update_canteen_duplicate_siret_managed(self):
        """
        If attempt to update a canteen with the same SIRET as one that I manage already, give
        me 400 with canteen name and id
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret, managers=[authenticate.user])
        canteen_to_test = CanteenFactory(managers=[authenticate.user])
        payload = {"siret": siret}

        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": canteen_to_test.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertTrue(body["isManagedByUser"])

    @authenticate
    def test_patch_with_own_siret(self):
        """
        A canteen modification should pass if the siret in the payload is already the canteen's siret
        """
        siret = "26566234910966"
        canteen = CanteenFactory(siret=siret, managers=[authenticate.user])
        payload = {"siret": siret}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_canteen_image_edition_unauthorized(self):
        """
        The API should not allow image modification for non-managers
        """
        canteen = CanteenFactory()
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

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        canteen.refresh_from_db()
        self.assertEqual(canteen.images.count(), 0)

    @authenticate
    def test_canteen_image_modification(self):
        """
        The API should allow image addition and deletion for canteen managers
        """
        canteen = CanteenFactory(managers=[authenticate.user])
        self.assertEqual(canteen.images.count(), 0)

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

        self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        canteen.refresh_from_db()
        self.assertEqual(canteen.images.count(), 1)

        # Delete image
        payload = {"images": []}

        self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        canteen.refresh_from_db()
        self.assertEqual(canteen.images.count(), 0)

    @authenticate
    def test_update_canteen_tracking_info(self):
        """
        The app should not allow the tracking info to be updated
        """
        canteen = CanteenFactory(
            creation_mtm_source=None,
            creation_mtm_campaign=None,
            creation_mtm_medium=None,
            managers=[authenticate.user],
        )
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "managementType": Canteen.ManagementType.DIRECT,
            "creation_mtm_source": "mtm_source_value",
            "creation_mtm_campaign": "mtm_campaign_value",
            "creation_mtm_medium": "mtm_medium_value",
        }

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen.refresh_from_db()
        self.assertIsNone(canteen.creation_mtm_source)
        self.assertIsNone(canteen.creation_mtm_campaign)
        self.assertIsNone(canteen.creation_mtm_medium)


class CanteenDeleteApiTest(APITestCase):
    @authenticate
    def test_soft_delete(self):
        canteen = CanteenFactory(managers=[authenticate.user])

        response = self.client.delete(reverse("single_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Model was only soft-deleted but remains in the DB
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
