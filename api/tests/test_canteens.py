import base64
import os
from unittest import mock

import requests
import requests_mock
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import (
    CanteenFactory,
    DiagnosticFactory,
    ManagerInvitationFactory,
    PurchaseFactory,
    SectorFactory,
)
from data.models import Canteen, Diagnostic, Teledeclaration
from data.utils import CreationSource

from .utils import authenticate, get_oauth2_token

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class CanteenApiTest(APITestCase):
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
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="03201976246133"
            ),
            CanteenFactory.create(
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret="03201976246133"
            ),
            CanteenFactory.create(
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
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        Canteen.objects.filter(id=central_kitchen.id).update(siret=None)
        central_kitchen.refresh_from_db()

        other_canteens = [
            CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=None),
            CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL_SERVING, central_producer_siret=None),
            CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE, central_producer_siret=None),
        ]

        payload = {"siret": "35662897196149"}
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": central_kitchen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for canteen in other_canteens:
            canteen.refresh_from_db()
            self.assertIsNone(canteen.central_producer_siret)

    @authenticate
    def test_soft_delete(self):
        canteen = CanteenFactory.create(managers=[authenticate.user])

        response = self.client.delete(reverse("single_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Model was only soft-deleted but remains in the DB
        self.assertIsNotNone(Canteen.all_objects.get(pk=canteen.id).deletion_date)

    @authenticate
    def test_create_canteen(self):
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertIn(authenticate.user, created_canteen.managers.all())

    @authenticate
    def test_create_canteen_creation_source(self):
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }

        # from the APP
        response = self.client.post(reverse("user_canteens"), {**payload, "creation_source": "APP"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_source, CreationSource.APP)
        created_canteen.hard_delete()

        # defaults to API
        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_source, CreationSource.API)
        created_canteen.hard_delete()

        # returns a 404 if the creation_source is not valid
        response = self.client.post(reverse("user_canteens"), {**payload, "creation_source": "UNKNOWN"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @authenticate
    def test_create_canteen_missing_siret(self):
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            # "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertEqual(body["siret"], ["Ce champ est obligatoire."])

    @authenticate
    def test_create_canteen_bad_siret(self):
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "0123",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["14 caractères numériques sont attendus"])

        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "01234567891011",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET n'est pas valide."])

        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "01234567891011",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE_CENTRAL,
            "economicModel": Canteen.EconomicModel.PUBLIC,
            "centralProducerSiret": "01234567891011",
        }

        response = self.client.post(reverse("user_canteens"), payload)
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

        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": siret,
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }
        response = self.client.post(reverse("user_canteens"), payload)
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

        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": siret,
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
        }
        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertFalse(body["isManagedByUser"])
        self.assertEqual(Canteen.objects.count(), 1)

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
    def test_refuse_patch_with_blank_siret(self):
        """
        A canteen modification shouldn't allow deleting a SIRET with sending blank value
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])

        payload = {"siret": ""}
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET ne peut pas être vide."])

    @authenticate
    def test_refuse_patch_with_no_siret(self):
        """
        A canteen modification shouldn't allow deleting a SIRET with sending null value
        """
        canteen = CanteenFactory.create(siret="21340172201787", managers=[authenticate.user])
        payload = {
            "siret": None,
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET ne peut pas être vide."])
        canteen.refresh_from_db()
        self.assertEqual(canteen.siret, "21340172201787")

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
    def test_create_canteen_with_images(self):
        """
        The app should create the necessary image models upon the creation of a canteen
        """
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
            "images": [
                {
                    "image": "data:image/jpeg;base64," + image_base_64,
                }
            ],
        }
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
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "productionType": Canteen.ProductionType.ON_SITE,
            "economicModel": Canteen.EconomicModel.PUBLIC,
            "creation_mtm_source": "mtm_source_value",
            "creation_mtm_campaign": "mtm_campaign_value",
            "creation_mtm_medium": "mtm_medium_value",
        }
        response = self.client.post(reverse("user_canteens"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertEqual(created_canteen.creation_mtm_source, "mtm_source_value")
        self.assertEqual(created_canteen.creation_mtm_campaign, "mtm_campaign_value")
        self.assertEqual(created_canteen.creation_mtm_medium, "mtm_medium_value")

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
    def test_get_central_kitchen(self):
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="96953195898254")
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


class TestCanteenActionApi(APITestCase):
    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_canteen_actions(self):
        """
        Check that this endpoint returns the user's canteens and the next action required
        """
        # these canteens aren't in a very logical order, because want to test sorting by action
        # create diag (has one for 2020)
        needs_last_year_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        # nothing to do
        complete = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21340172201787",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        central_no_sectors_siret = "21380185500015"
        complete_central_no_sectors = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=365,
            siret=central_no_sectors_siret,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
            satellite_canteens_count=1,
            sectors=None,
        )
        central_with_one_sat_siret = "21670482500019"
        complete_central_with_diff_sat_count = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            yearly_meal_count=365,
            siret=central_with_one_sat_siret,
            managers=[authenticate.user],
            satellite_canteens_count=10,
            sectors=None,
        )
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_with_one_sat_siret
        )
        complete_site_one_sector = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21640122400011",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
            sectors=[SectorFactory.create()],
        )
        # complete diag
        needs_to_fill_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        central_siret = "92341284500011"
        needs_diagnostic_mode = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL, siret=central_siret, managers=[authenticate.user]
        )
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_siret
        )
        # complete establishement
        needs_sectors = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            daily_meal_count=1,
            yearly_meal_count=365,
            siret="37856520465586",
            managers=[authenticate.user],
            sectors=[],
        )
        needs_daily_meal_count = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            daily_meal_count=12,
            yearly_meal_count=365,
            siret="40419443300078",
            managers=[authenticate.user],
        )
        Canteen.objects.filter(id=needs_daily_meal_count.id).update(daily_meal_count=None)
        needs_daily_meal_count.refresh_from_db()
        too_many_sectors = CanteenFactory.create(
            siret="83014132100034",
            managers=[authenticate.user],
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PRIVATE,
            city_insee_code="69123",
            daily_meal_count=10,
            yearly_meal_count=365,
            sectors=[
                SectorFactory.create(name="1"),
                SectorFactory.create(name="2"),
                SectorFactory.create(name="3"),
                SectorFactory.create(name="4"),
            ],
        )
        # TD
        needs_td = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        # create satellites
        needs_additional_satellites = CanteenFactory.create(
            siret="78146469373706",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=3,
            daily_meal_count=12,
            managers=[authenticate.user],
        )
        CanteenFactory.create(name="Not my canteen")

        last_year = 2021
        DiagnosticFactory.create(year=last_year - 1, canteen=needs_last_year_diag)

        td_diag = DiagnosticFactory.create(year=last_year, canteen=complete, value_total_ht=1000)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)
        td_diag_central_no_sectors = DiagnosticFactory.create(
            year=last_year,
            canteen=complete_central_no_sectors,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        Teledeclaration.create_from_diagnostic(td_diag_central_no_sectors, authenticate.user)
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_no_sectors_siret
        )

        td_diag_central_with_one_sat = DiagnosticFactory.create(
            year=last_year,
            canteen=complete_central_with_diff_sat_count,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )
        Teledeclaration.create_from_diagnostic(td_diag_central_with_one_sat, authenticate.user)

        td_diag_one_sector = DiagnosticFactory.create(
            year=last_year,
            canteen=complete_site_one_sector,
            value_total_ht=1000,
        )
        Teledeclaration.create_from_diagnostic(td_diag_one_sector, authenticate.user)

        DiagnosticFactory.create(year=last_year, canteen=needs_to_fill_diag, value_total_ht=None)
        # make sure the endpoint only looks at diagnostics of the year requested
        DiagnosticFactory.create(year=last_year - 1, canteen=needs_to_fill_diag, value_total_ht=1000)

        DiagnosticFactory.create(
            year=last_year, canteen=needs_diagnostic_mode, central_kitchen_diagnostic_mode=None, value_total_ht=100
        )

        DiagnosticFactory.create(year=last_year, canteen=needs_td, value_total_ht=100)

        DiagnosticFactory.create(year=last_year, canteen=needs_sectors, value_total_ht=100)

        DiagnosticFactory.create(year=last_year, canteen=needs_daily_meal_count, value_total_ht=100)

        DiagnosticFactory.create(year=last_year, canteen=too_many_sectors, value_total_ht=100)

        # has a diagnostic but this canteen did not register any satellites
        DiagnosticFactory.create(year=last_year, canteen=needs_additional_satellites, value_total_ht=100)

        response = self.client.get(
            reverse("list_actionable_canteens", kwargs={"year": last_year}) + "?ordering=action,modification_date"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        returned_canteens = body["results"]
        self.assertEqual(len(returned_canteens), 12)

        expected_actions = [
            (needs_additional_satellites, Canteen.Actions.ADD_SATELLITES),
            (needs_last_year_diag, Canteen.Actions.CREATE_DIAGNOSTIC),
            (needs_to_fill_diag, Canteen.Actions.FILL_DIAGNOSTIC),
            (needs_diagnostic_mode, Canteen.Actions.FILL_DIAGNOSTIC),
            (needs_sectors, Canteen.Actions.FILL_CANTEEN_DATA),
            (needs_daily_meal_count, Canteen.Actions.FILL_CANTEEN_DATA),
            (too_many_sectors, Canteen.Actions.FILL_CANTEEN_DATA),
            (needs_td, Canteen.Actions.TELEDECLARE),
            (complete, Canteen.Actions.NOTHING),
            (complete_central_no_sectors, Canteen.Actions.NOTHING),
            (complete_central_with_diff_sat_count, Canteen.Actions.NOTHING),
            (complete_site_one_sector, Canteen.Actions.NOTHING),
        ]
        for index, (canteen, action) in zip(range(len(expected_actions)), expected_actions):
            with self.subTest(canteen=canteen, action=action):
                self.assertEqual(returned_canteens[index]["id"], canteen.id)
                self.assertEqual(returned_canteens[index]["action"], action)
                self.assertIn("sectors", returned_canteens[index])
        self.assertTrue(body["hasPendingActions"])

    @authenticate
    def test_central_without_satellites_has_complete_satellites_action(self):
        """
        Test for a bug fix. A central that doesn't have any satellites at all should get the complete satellite action.
        """
        CanteenFactory.create(
            siret="45467900121441",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=3,
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}) + "?ordering=action")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["results"][0]["action"], Canteen.Actions.ADD_SATELLITES)

    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_actions_missing_data(self):
        """
        Even if the diagnostic is complete, the mandatory information on the canteen level should
        return a Canteen.Actions.FILL_CANTEEN_DATA
        """
        # First a case in which the canteen is complete
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        last_year = 2021
        diagnostic = DiagnosticFactory.create(year=last_year, canteen=canteen, value_total_ht=1000)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)

        # If mandatory data on the canteen is missing, we need a 35_fill_canteen_data
        Canteen.objects.filter(id=canteen.id).update(yearly_meal_count=None)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        # Central cuisines should have the number of satellites filled in
        canteen.yearly_meal_count = 1000
        canteen.production_type = Canteen.ProductionType.CENTRAL
        canteen.satellite_canteens_count = None
        canteen.save()
        canteen_sat = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            yearly_meal_count=1000,
            daily_meal_count=12,
            central_producer_siret=canteen.siret,
            managers=[authenticate.user],
        )
        diagnostic.central_kitchen_diagnostic_mode = "APPRO"
        diagnostic.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        # reset diag from above change.
        diagnostic.central_kitchen_diagnostic_mode = None
        diagnostic.save()

        # Central kitchens with missing satellites should return the add satellite action
        canteen_sat.delete()
        canteen.satellite_canteens_count = 123
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.ADD_SATELLITES)

        # Satellites should have the SIRET of the central cuisine
        canteen.production_type = Canteen.ProductionType.ON_SITE_CENTRAL
        canteen.central_producer_siret = None
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        canteen.central_producer_siret = "21590350100017"
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)

    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_actions_satellite(self):
        """
        If a satellite's CC has teledeclared there is no pending action for the satellite
        """
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            satellite_canteens_count=1,
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[authenticate.user],
        )
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=10,
            daily_meal_count=2,
            siret="99569440745111",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            central_producer_siret="96766910375238",
            managers=[authenticate.user],
        )
        diagnostic = DiagnosticFactory.create(
            year=2021,
            canteen=central_kitchen,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
        )

        last_year = 2021
        DiagnosticFactory.create(
            year=last_year,
            canteen=satellite,
            value_total_ht=1200,
        )

        # cc diagnostic not teledeclared
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        satellite_action = next(x for x in returned_canteens if x["id"] == satellite.id)["action"]
        self.assertEqual(satellite_action, Canteen.Actions.NOTHING_SATELLITE)

        # cc diagnostic teledeclared
        Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        satellite_action = next(x for x in returned_canteens if x["id"] == satellite.id)["action"]
        self.assertEqual(satellite_action, Canteen.Actions.NOTHING_SATELLITE_TELEDECLARED)

    @authenticate
    def test_get_canteens_with_purchases_no_diagnostics_for_year(self):
        """
        Return a list of canteens I manage who do have purchases for the given year,
        but have not yet created a diagnostic
        """
        year = 2023
        canteen_without_diag = CanteenFactory.create(managers=[authenticate.user])
        canteen_with_diag = CanteenFactory.create(managers=[authenticate.user])
        CanteenFactory.create(managers=[authenticate.user])  # canteen_without_purchases
        not_my_canteen = CanteenFactory.create()
        DiagnosticFactory.create(canteen=canteen_with_diag, year=year)
        PurchaseFactory.create(canteen=canteen_without_diag, date=f"{year}-01-01")
        # add second purchase to check canteen id deduplication
        PurchaseFactory.create(canteen=canteen_without_diag, date=f"{year}-12-01")
        PurchaseFactory.create(canteen=canteen_with_diag, date=f"{year}-01-01")
        PurchaseFactory.create(canteen=not_my_canteen, date=f"{year}-01-01")

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["undiagnosedCanteensWithPurchases"], [canteen_without_diag.id])

    @authenticate
    def test_filter_td_bad_sirets(self):
        """
        Check that canteens with SIRET issues (no SIRET, SIRET = central_producer_siret) have complete canteen actions and not TD actions
        """
        last_year = 2021
        # canteen not ok with diag
        canteen_with_no_siret = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            managers=[authenticate.user],
        )
        Canteen.objects.filter(id=canteen_with_no_siret.id).update(siret=None)
        canteen_with_no_siret.refresh_from_db()
        DiagnosticFactory.create(canteen=canteen_with_no_siret, year=last_year, value_total_ht=10000)
        # canteen not ok with diag
        canteen_with_bad_central_siret = CanteenFactory.create(
            siret="59282615314394",
            central_producer_siret="59282615314394",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            managers=[authenticate.user],
        )
        DiagnosticFactory.create(canteen=canteen_with_bad_central_siret, year=last_year, value_total_ht=10000)
        # canteen ok without diag
        CanteenFactory.create(
            siret="55314169703815",
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            economic_model=Canteen.EconomicModel.PUBLIC,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        body = response.json()

        returned_canteens = body["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)
        self.assertEqual(returned_canteens[1]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

    def test_list_canteen_actions_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the canteens actions view
        """
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_single_canteen_actions(self):
        """
        Check that this endpoint can return the summary for a specified canteen
        """
        CanteenFactory.create(
            id=3,
            production_type=Canteen.ProductionType.ON_SITE,
            sectors=[SectorFactory.create()],
            managers=[authenticate.user],
        )

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], Canteen.Actions.CREATE_DIAGNOSTIC)

    @authenticate
    @freeze_time("2025-01-01")  # before the 2024 campaign
    def test_before_campaign_dates(self):
        complete = CanteenFactory.create(
            id=2,
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sectors=[SectorFactory.create()],
            managers=[authenticate.user],
        )
        last_year = 2024
        DiagnosticFactory.create(canteen=complete, year=last_year, value_total_ht=10000)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

        # last_year -1
        DiagnosticFactory.create(canteen=complete, year=last_year - 1, value_total_ht=10000)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year - 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

    @authenticate
    @freeze_time("2025-04-20")  # during the 2024 correction campaign
    def test_during_the_correction_campaign(self):
        complete = CanteenFactory.create(
            id=2,
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sectors=[SectorFactory.create()],
            managers=[authenticate.user],
        )
        last_year = 2024
        diagnostic = DiagnosticFactory.create(canteen=complete, year=last_year, value_total_ht=10000)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)  # not allowed to teledeclare

        # submit a teledeclaration during the campaign
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.NOTHING)

        # cancel the teledeclaration
        teledeclaration.cancel()

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.TELEDECLARE)  # allowed to teledeclare

    @authenticate
    @freeze_time("2025-12-30")  # after the 2024 campaign
    def test_after_campaign_dates(self):
        """
        Check that when we are after the campaign we don't return the teledeclaration action
        """
        canteen_td = CanteenFactory.create(
            id=2,
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sectors=[SectorFactory.create()],
            managers=[authenticate.user],
        )
        canteen_did_not_td = CanteenFactory.create(
            id=3,
            production_type=Canteen.ProductionType.ON_SITE,
            yearly_meal_count="123",
            daily_meal_count="12",
            siret="21590350100017",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            management_type=Canteen.ManagementType.DIRECT,
            sectors=[SectorFactory.create()],
            managers=[authenticate.user],
        )
        last_year = 2024
        for canteen in [canteen_td, canteen_did_not_td]:
            DiagnosticFactory.create(canteen=canteen, year=last_year, value_total_ht=10000)
        Teledeclaration.create_from_diagnostic(
            Diagnostic.objects.get(canteen=canteen_td, year=last_year), authenticate.user
        )

        # canteen_td
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 2, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 2)
        self.assertEqual(body["action"], Canteen.Actions.NOTHING)

        # canteen_did_not_td (last_year)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": last_year}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

        # canteen_did_not_td (last_year + 1)
        DiagnosticFactory.create(canteen=canteen, year=last_year + 1, value_total_ht=10000)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": last_year + 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], Canteen.Actions.DID_NOT_TELEDECLARE)

    def test_get_retrieve_actionable_canteen_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the canteen actions view
        """
        CanteenFactory.create(id=3, production_type=Canteen.ProductionType.ON_SITE)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_retrieve_actionable_canteen_unauthorized(self):
        """
        If the user is not the manager, they will not be able to
        access the canteen actions view
        """
        CanteenFactory.create(id=3, production_type=Canteen.ProductionType.ON_SITE)
        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    @freeze_time("2022-08-30")  # during the 2021 campaign
    def test_get_actions_missing_line_ministry(self):
        """
        Even if the diagnostic is complete, the mandatory information on the canteen level should
        return a Canteen.Actions.FILL_CANTEEN_DATA if line ministry is not there
        """
        with_lm = SectorFactory.create(has_line_ministry=True)
        without_lm = SectorFactory.create(has_line_ministry=False)
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sectors=[with_lm, without_lm],
            line_ministry=None,
            managers=[authenticate.user],
        )
        last_year = 2021
        DiagnosticFactory.create(year=last_year, canteen=canteen, value_total_ht=1000)
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.FILL_CANTEEN_DATA)

        # a canteen that has a line ministry should be complete
        canteen.line_ministry = Canteen.Ministries.AFFAIRES_ETRANGERES
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)

        # a canteen without a line ministry and without a sector that demands one is also complete
        canteen.line_ministry = None
        canteen.sectors.clear()
        canteen.sectors.set([without_lm])
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], Canteen.Actions.TELEDECLARE)


class TestCanteenTerritoryApi(APITestCase):
    @authenticate
    def test_territory_canteens_list(self):
        """
        Elected profiles should get information on canteens in their
        geographical area even if they are not the managers
        """

        # Set an elected profile
        user = authenticate.user
        user.is_elected_official = True
        user.departments = ["01", "02"]
        user.save()

        # Create canteens
        canteen_01 = CanteenFactory.create(department="01")
        canteen_02 = CanteenFactory.create(department="02")
        out_of_place_canteen = CanteenFactory.create(department="03")

        # Make request
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()["results"]

        self.assertEqual(len(body), 2)
        ids = list(map(lambda x: x["id"], body))

        self.assertIn(canteen_01.id, ids)
        self.assertIn(canteen_02.id, ids)
        self.assertNotIn(out_of_place_canteen.id, ids)

    @authenticate
    def test_not_elected_official_territory_canteens_list(self):
        """
        Profiles not enabled as "elected" should not get information on
        canteens via the territory_canteens API endpoint
        """

        # Set an elected profile
        user = authenticate.user
        user.is_elected_official = False
        user.save()

        # Make request
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_territory_canteens_list(self):
        """
        Profiles not authenticated should not be able to use the endpoint
        territory_canteens
        """
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCanteenStatusApi(APITestCase):
    @authenticate
    def test_check_siret_managed(self):
        """
        If checking a siret of a canteen that exists and I manage, give me canteen info
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret, managers=[authenticate.user])

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertTrue(body["isManagedByUser"])
        self.assertFalse(body["canBeClaimed"])

    @authenticate
    def test_check_siret_unmanaged(self):
        """
        If checking a siret of a canteen that exists but no one manages,
        give me minimal canteen info and an indication that the canteen can be claimed
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.clear()

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertFalse(body["isManagedByUser"])
        self.assertTrue(body["canBeClaimed"])

    @authenticate
    def test_check_siret_managed_by_someone_else(self):
        """
        If checking a siret of a canteen that exists but is managed by someone else,
        give me minimal canteen info and an indication that the canteen can't be claimed
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        self.assertFalse(body["isManagedByUser"])
        self.assertFalse(body["canBeClaimed"])  # CanteenFactory creates canteens with managers

    @requests_mock.Mocker()
    @authenticate
    def test_check_siret_new_canteen(self, mock):
        siret = "34974603058674"
        city = "Paris 15e Arrondissement"
        postcode = "75015"
        insee_code = "75115"
        sirene_api_url = f"https://recherche-entreprises.api.gouv.fr/search?etat_administratif=A&page=1&per_page=1&mtm_campaign=ma-cantine&q={siret}"
        sirene_mocked_response = {
            "results": [
                {
                    "siren": "923412845",
                    "nom_complet": "Wrong name",
                    "matching_etablissements": [
                        {
                            "commune": insee_code,
                            "code_postal": postcode,
                            "libelle_commune": city,
                            "liste_enseignes": ["Legal unit name"],
                            "etat_administratif": "A",
                        }
                    ],
                }
            ],
            "total_results": 1,
        }
        mock.get(sirene_api_url, json=sirene_mocked_response)
        geo_api_url = f"https://api-adresse.data.gouv.fr/search/?q={insee_code}&citycode={insee_code}&type=municipality&autocomplete=1"
        geo_mocked_response = {
            "features": [
                {
                    "properties": {
                        "label": city,
                        "citycode": insee_code,
                        "postcode": postcode,
                        "context": "38, Isère, Auvergne-Rhône-Alpes",
                    }
                }
            ],
        }
        mock.get(geo_api_url, json=geo_mocked_response)

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertEqual(body["name"], "Legal unit name")
        self.assertEqual(body["siret"], siret)
        self.assertEqual(body["postalCode"], postcode)
        self.assertEqual(body["city"], city)
        self.assertEqual(body["cityInseeCode"], insee_code)
        self.assertEqual(body["department"], "38")

        # Check the given name if the canteen is an etablissement (sub of an unite legale)
        sirene_mocked_response = {
            "results": [
                {
                    "siren": "923412845",
                    "nom_complet": "A name",
                    "matching_etablissements": [
                        {
                            "commune": insee_code,
                            "code_postal": postcode,
                            "libelle_commune": city,
                            "liste_enseignes": ["ECOLE PRIMAIRE PUBLIQUE"],
                            "etat_administratif": "A",
                        }
                    ],
                }
            ],
            "total_results": 1,
        }
        mock.get(sirene_api_url, json=sirene_mocked_response)
        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        body = response.json()
        self.assertEqual(body["name"], "ECOLE PRIMAIRE PUBLIQUE")

    @mock.patch("requests.get", side_effect=requests.exceptions.ConnectTimeout)
    @mock.patch("requests.post", side_effect=requests.exceptions.ConnectTimeout)
    @authenticate
    def test_external_api_down(self, mock_get, mock_post):
        siret = "34974603058674"

        response = self.client.get(reverse("canteen_status_by_siret", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertNotIn("id", body)
        self.assertNotIn("name", body)
        self.assertEqual(body["siret"], "34974603058674")
        self.assertNotIn("postalCode", body)
        self.assertNotIn("city", body)
        self.assertNotIn("cityInseeCode", body)
        self.assertNotIn("department", body)
