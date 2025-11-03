import base64
import os

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate, get_oauth2_token
from data.factories import CanteenFactory, DiagnosticFactory, ManagerInvitationFactory, SectorFactory
from data.models import Canteen, Diagnostic, Teledeclaration
from data.utils import CreationSource

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
        canteen = CanteenFactory.create(managers=[user])

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
            ManagerInvitationFactory.create().canteen,
            ManagerInvitationFactory.create().canteen,
        ]
        other_canteens = [
            CanteenFactory.create(),
            CanteenFactory.create(),
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
        CanteenFactory.create(
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
        CanteenFactory.create(production_type="site", managers=[authenticate.user])
        user_central_cuisine = CanteenFactory.create(production_type="central", managers=[authenticate.user])
        user_central_serving_cuisine = CanteenFactory.create(
            production_type="central_serving", managers=[authenticate.user]
        )

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
            CanteenFactory.create(managers=[authenticate.user]),
            CanteenFactory.create(managers=[authenticate.user]),
        ]
        _ = [
            CanteenFactory.create(),
            CanteenFactory.create(),
        ]

        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 2)
        self.assertEqual(body[0].get("id"), user_canteens[1].id)
        self.assertEqual(body[1].get("id"), user_canteens[0].id)

    def test_canteen_preview_wrong_token(self):
        user, token = get_oauth2_token("user:read")
        CanteenFactory.create(managers=[user])

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_canteen_preview_correct_token(self):
        user, token = get_oauth2_token("canteen:read")
        canteen = CanteenFactory.create(managers=[user])

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
        user_canteen = CanteenFactory.create(managers=[authenticate.user])

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
        user_canteen = CanteenFactory.create(managers=[authenticate.user])

        DiagnosticFactory.create(
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
        canteen = CanteenFactory.create()

        response = self.client.get(reverse("single_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_canteen_without_tracking(self):
        """
        Full representation should not contain the tracking info
        """
        user_canteen = CanteenFactory.create(
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
        canteen = CanteenFactory.create(managers=[authenticate.user])
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)

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
        central_kitchen = CanteenFactory.create(siret="96953195898254", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
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
        user_canteen = CanteenFactory.create(managers=[authenticate.user])

        DiagnosticFactory.create(
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
        central = CanteenFactory.create(siret="21340172201787", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret="21340172201787",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            managers=[authenticate.user],
        )

        DiagnosticFactory.create(
            canteen=satellite,
            year=2021,
            value_total_ht=100,
            value_bio_ht=0,
            value_sustainable_ht=30,
        )
        DiagnosticFactory.create(
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
        cls.sector_1 = SectorFactory()
        cls.sector_2 = SectorFactory()
        cls.sector_3 = SectorFactory()
        cls.sector_4 = SectorFactory()
        cls.DEFAULT_PAYLOAD = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
            "sectors": [cls.sector_1.id, cls.sector_2.id],
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
        payload.pop("siret")

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
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])

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
        canteen = CanteenFactory.create(siret=siret)

        response = self.client.post(reverse("user_canteens"), {**self.DEFAULT_PAYLOAD, "siret": siret})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertFalse(body["isManagedByUser"])
        self.assertEqual(Canteen.objects.count(), 1)

    @authenticate
    def test_create_canteen_with_sectors(self):
        central_kitchen = CanteenFactory.create(siret="03201976246133", production_type=Canteen.ProductionType.CENTRAL)

        for production_type in [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING]:
            # sector should be empty
            for sectors in [[]]:
                with self.subTest(production_type=production_type, sectors=sectors):
                    payload = {
                        **self.DEFAULT_PAYLOAD,
                        "productionType": production_type,
                        "satelliteCanteensCount": 1,  # needed for central kitchens
                        "sectors": sectors,
                    }
                    response = self.client.post(reverse("user_canteens"), payload, format="json")
                    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                    canteen = Canteen.objects.get(pk=response.json()["id"])
                    self.assertEqual(canteen.sectors.count(), len(sectors))
                    canteen.delete()  # to reuse the same SIRET
            for sectors in [
                [self.sector_1.id],
                [self.sector_1.id, self.sector_2.id, self.sector_3.id, self.sector_4.id],
            ]:
                with self.subTest(production_type=production_type, sectors=sectors):
                    payload = {
                        **self.DEFAULT_PAYLOAD,
                        "productionType": production_type,
                        "satelliteCanteensCount": 1,  # needed for central kitchens
                        "sectors": sectors,
                    }
                    response = self.client.post(reverse("user_canteens"), payload, format="json")
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for production_type in [Canteen.ProductionType.ON_SITE, Canteen.ProductionType.ON_SITE_CENTRAL]:
            # sector should be filled (between 1 and 3 sectors)
            for sectors in [
                [self.sector_1.id],
                [self.sector_1.id, self.sector_2.id],
                [self.sector_1.id, self.sector_2.id, self.sector_3.id],
            ]:
                with self.subTest(production_type=production_type, sectors=sectors):
                    payload = {
                        **self.DEFAULT_PAYLOAD,
                        "productionType": production_type,
                        "centralProducerSiret": central_kitchen.siret
                        if production_type == Canteen.ProductionType.ON_SITE_CENTRAL
                        else None,  # needed for satellite kitchens
                        "sectors": sectors,
                    }
                    response = self.client.post(reverse("user_canteens"), payload, format="json")
                    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                    canteen = Canteen.objects.get(pk=response.json()["id"])
                    self.assertEqual(canteen.sectors.count(), len(sectors))
                    canteen.delete()  # to reuse the same SIRET
            for sectors in [[], [self.sector_1.id, self.sector_2.id, self.sector_3.id, self.sector_4.id]]:
                with self.subTest(production_type=production_type, sectors=sectors):
                    payload = {
                        **self.DEFAULT_PAYLOAD,
                        "productionType": production_type,
                        "centralProducerSiret": central_kitchen.siret
                        if production_type == Canteen.ProductionType.ON_SITE_CENTRAL
                        else None,  # needed for satellite kitchens
                        "sectors": sectors,
                    }
                    response = self.client.post(reverse("user_canteens"), payload, format="json")
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        canteen = CanteenFactory.create(city="Paris")
        payload = {"city": "Lyon"}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_modify_canteen(self):
        """
        Users can modify the canteens they manage
        """
        canteen = CanteenFactory.create(city="Paris", managers=[authenticate.user])
        payload = {
            "city": "Lyon",
            "siret": "21340172201787",
            "managementType": Canteen.ManagementType.DIRECT,
            "reservationExpeParticipant": True,
            "satelliteCanteensCount": 130,
            "productionType": Canteen.ProductionType.CENTRAL,
        }

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(created_canteen.city, "Lyon")
        self.assertEqual(created_canteen.siret, "21340172201787")
        self.assertEqual(created_canteen.management_type, "direct")
        self.assertEqual(created_canteen.satellite_canteens_count, 130)
        self.assertEqual(created_canteen.production_type, "central")
        self.assertEqual(created_canteen.reservation_expe_participant, True)

    @authenticate
    def test_modify_central_kitchen_siret(self):
        """
        A change in the SIRET of a central cuisine must update the "central_producer_siret" of
        its satellites
        """
        central_kitchen = CanteenFactory.create(
            siret="03201976246133", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        satellites = [
            CanteenFactory.create(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
            ),
            CanteenFactory.create(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
            ),
            CanteenFactory.create(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
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
        central_kitchen_without_siret = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        canteen_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen_without_siret.siret,
        )
        Canteen.objects.filter(id=central_kitchen_without_siret.id).update(siret=None)
        central_kitchen_without_siret.refresh_from_db()
        Canteen.objects.filter(id=canteen_satellite.id).update(central_producer_siret=None)
        canteen_satellite.refresh_from_db()
        canteen_central_serving = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL_SERVING, central_producer_siret=None
        )
        canteen_on_site = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE, central_producer_siret=None
        )
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
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])

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
        canteen = CanteenFactory.create(siret=siret)
        canteen_to_test = CanteenFactory.create(managers=[authenticate.user])
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
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])
        canteen_to_test = CanteenFactory.create(managers=[authenticate.user])
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
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])
        payload = {"siret": siret}

        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_update_canteen_sectors(self):
        sector_1 = SectorFactory()
        sector_2 = SectorFactory()
        central_kitchen_with_sectors = CanteenFactory.create(
            siret="03201976246133",
            production_type=Canteen.ProductionType.CENTRAL,
            sectors=[sector_1, sector_2],
            managers=[authenticate.user],
        )
        canteen_site = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE, sectors=[], managers=[authenticate.user]
        )

        # central_kitchen: fix sectors (remove them)
        self.assertEqual(central_kitchen_with_sectors.sectors.count(), 2)
        payload = {"sectors": []}
        response = self.client.patch(
            reverse("single_canteen", kwargs={"pk": central_kitchen_with_sectors.id}), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        central_kitchen_with_sectors.refresh_from_db()
        self.assertEqual(central_kitchen_with_sectors.sectors.count(), 0)

        # canteen_site: fix sectors (add some)
        self.assertEqual(canteen_site.sectors.count(), 0)
        payload = {"sectors": [sector_1.id, sector_2.id]}
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen_site.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        canteen_site.refresh_from_db()
        self.assertEqual(canteen_site.sectors.count(), 2)

    @authenticate
    def test_canteen_image_edition_unauthorized(self):
        """
        The API should not allow image modification for non-managers
        """
        canteen = CanteenFactory.create()
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
        canteen = CanteenFactory.create(managers=[authenticate.user])
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
        canteen = CanteenFactory.create(
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
        canteen = CanteenFactory.create(managers=[authenticate.user])

        response = self.client.delete(reverse("single_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Model was only soft-deleted but remains in the DB
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)
