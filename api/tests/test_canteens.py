import base64
import os
from unittest import mock

import requests
import requests_mock
from django.test.utils import override_settings
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

from .utils import authenticate, get_oauth2_token

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCanteenApi(APITestCase):
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
        canteen = CanteenFactory.create()
        canteen.managers.add(user)

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
            CanteenFactory.create(),
            CanteenFactory.create(),
        ]
        _ = [
            CanteenFactory.create(),
            CanteenFactory.create(),
        ]
        user = authenticate.user
        for canteen in user_canteens:
            canteen.managers.add(user)

        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 2)
        self.assertEqual(body[0].get("id"), user_canteens[1].id)
        self.assertEqual(body[1].get("id"), user_canteens[0].id)

    def test_canteen_preview_wrong_token(self):
        user, token = get_oauth2_token("user:read")
        canteen = CanteenFactory.create()
        canteen.managers.add(user)

        self.client.credentials(Authorization=f"Bearer {token}")
        response = self.client.get(reverse("user_canteen_previews"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_canteen_preview_correct_token(self):
        user, token = get_oauth2_token("canteen:read")
        canteen = CanteenFactory.create()
        canteen.managers.add(user)

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
        user = authenticate.user
        for canteen in user_canteens:
            canteen.managers.add(user)

        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results")

        for user_canteen in user_canteens:
            self.assertTrue(any(x["id"] == user_canteen.id for x in body))

        for recieved_canteen in body:
            self.assertEqual(recieved_canteen["managers"][0]["email"], user.email)
            self.assertTrue("email" in recieved_canteen["managerInvitations"][0])

        for other_canteen in other_canteens:
            self.assertFalse(any(x["id"] == other_canteen.id for x in body))

    @authenticate
    def test_get_single_user_canteen(self):
        """
        Users can access to the full representation of a single
        canteen as long as they manage it.
        """
        user_canteen = CanteenFactory.create()
        user_canteen.managers.add(authenticate.user)

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
        user_canteen = CanteenFactory.create()
        user_canteen.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create(city="Paris")
        canteen.managers.add(authenticate.user)
        payload = {
            "city": "Lyon",
            "siret": "21340172201787",
            "managementType": "direct",
            "reservationExpeParticipant": True,
            "satelliteCanteensCount": 130,
            "productionType": "central",
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
        central_kitchen = CanteenFactory.create(siret="03201976246133", production_type=Canteen.ProductionType.CENTRAL)
        central_kitchen.managers.add(authenticate.user)

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
        central_kitchen = CanteenFactory.create(siret=None, production_type=Canteen.ProductionType.CENTRAL)
        central_kitchen.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)

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
        }

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = response.json()
        created_canteen = Canteen.objects.get(pk=body["id"])
        self.assertIn(authenticate.user, created_canteen.managers.all())

    @authenticate
    def test_create_canteen_missing_siret(self):
        payload = {
            "name": "My canteen",
            "city": "Lyon",
        }

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body = response.json()
        self.assertEqual(body["siret"], ["Ce champ est obligatoire."])

    @authenticate
    def test_create_canteen_bad_siret(self):
        payload = {"name": "My canteen", "siret": "0123"}

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["14 caractères numériques sont attendus"])

        payload = {"name": "My canteen", "siret": "01234567891011"}

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["siret"], ["Le numéro SIRET n'est pas valide."])

        payload = {"name": "My canteen", "centralProducerSiret": "01234567891011"}

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
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.add(authenticate.user)

        payload = {"name": "New canteen", "siret": siret}
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

        payload = {"name": "New canteen", "siret": siret}
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
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.add(authenticate.user)
        canteen_to_test = CanteenFactory.create()
        canteen_to_test.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.add(authenticate.user)

        payload = {"siret": siret}
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_refuse_patch_with_blank_siret(self):
        """
        A canteen modification shouldn't allow deleting a SIRET with sending blank value
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.add(authenticate.user)

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
        canteen = CanteenFactory.create(siret="21340172201787")
        canteen.managers.add(authenticate.user)
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
        canteen_to_test = CanteenFactory.create()
        canteen_to_test.managers.add(authenticate.user)

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
    def test_check_siret_managed(self):
        """
        If checking a siret of a canteen that exists and I manage, give me canteen info
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("canteen_status", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertTrue(body["isManagedByUser"])

    @authenticate
    def test_check_siret_unmanaged(self):
        """
        If checking a siret of a canteen that exists but no one manages,
        give me minimal canteen info and an indication that the canteen can be claimed
        """
        siret = "26566234910966"
        canteen = CanteenFactory.create(siret=siret)
        canteen.managers.clear()

        response = self.client.get(reverse("canteen_status", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
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

        response = self.client.get(reverse("canteen_status", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], canteen.name)
        self.assertEqual(body["id"], canteen.id)
        self.assertFalse(body["isManagedByUser"])
        # the CanteenFactory creates canteens with managers
        self.assertFalse(body["canBeClaimed"])

    @override_settings(SIRET_API_KEY="dummy")
    @override_settings(SIRET_API_SECRET="dummy")
    @requests_mock.Mocker()
    @authenticate
    def test_check_siret_new_canteen(self, mock):
        siret = "34974603058674"
        city = "Paris 15e Arrondissement"
        postcode = "75015"
        insee_code = "75115"
        sirene_api_url = f"https://api.insee.fr/entreprises/sirene/siret/{siret}"
        sirene_mocked_response = {
            "etablissement": {
                "uniteLegale": {"denominationUniteLegale": "Canteen Name"},
                "adresseEtablissement": {
                    "codeCommuneEtablissement": insee_code,
                    "codePostalEtablissement": postcode,
                    "libelleCommuneEtablissement": city,
                },
            },
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
        token_api_url = "https://api.insee.fr/token"
        token_mocked_response = {"access_token": "test"}
        mock.post(token_api_url, json=token_mocked_response)

        response = self.client.get(reverse("canteen_status", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["name"], "Canteen Name")
        self.assertEqual(body["siret"], siret)
        self.assertEqual(body["postalCode"], postcode)
        self.assertEqual(body["city"], city)
        self.assertEqual(body["cityInseeCode"], insee_code)
        self.assertEqual(body["department"], "38")

    @mock.patch("requests.get", side_effect=requests.exceptions.ConnectTimeout)
    @mock.patch("requests.post", side_effect=requests.exceptions.ConnectTimeout)
    @authenticate
    def test_external_api_down(self, mock_get, mock_post):
        siret = "34974603058674"

        response = self.client.get(reverse("canteen_status", kwargs={"siret": siret}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["siret"], "34974603058674")
        self.assertNotIn("name", body)
        self.assertNotIn("postalCode", body)
        self.assertNotIn("city", body)
        self.assertNotIn("cityInseeCode", body)
        self.assertNotIn("department", body)

    @authenticate
    def test_user_canteen_teledeclaration(self):
        """
        The teledeclaration information should only be visible to
        managers of the canteen
        """
        user = authenticate.user
        canteen = CanteenFactory.create()
        canteen.managers.add(user)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2020)
        Teledeclaration.create_from_diagnostic(diagnostic, user, Teledeclaration.TeledeclarationStatus.CANCELLED)

        new_teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic, user)
        response = self.client.get(reverse("user_canteens"))
        body = response.json().get("results")
        json_canteen = next(filter(lambda x: x["id"] == canteen.id, body))
        json_diagnostic = next(filter(lambda x: x["id"] == diagnostic.id, json_canteen["diagnostics"]))

        self.assertEqual(json_diagnostic["teledeclaration"]["id"], new_teledeclaration.id)

    @authenticate
    def test_canteen_image_modification(self):
        """
        The API should allow image addition and deletion for canteen managers
        """
        canteen = CanteenFactory.create()
        canteen.managers.add(authenticate.user)
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
    def test_create_cantine_with_images(self):
        """
        The app should create the necessary image models upon the creation of a cantine
        """
        image_path = os.path.join(CURRENT_DIR, "files/test-image-1.jpg")
        image_base_64 = None
        with open(image_path, "rb") as image:
            image_base_64 = base64.b64encode(image.read()).decode("utf-8")

        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "managementType": "direct",
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
    def test_create_cantine_with_tracking_info(self):
        """
        The app should store the mtm paramteres on creation
        """
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "siret": "21340172201787",
            "managementType": "direct",
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
    def test_update_cantines_tracking_info(self):
        """
        The app should not allow the tracking info to be updated
        """
        canteen = CanteenFactory.create(
            creation_mtm_source=None,
            creation_mtm_campaign=None,
            creation_mtm_medium=None,
        )
        canteen.managers.add(authenticate.user)
        payload = {
            "name": "My canteen",
            "city": "Lyon",
            "managementType": "direct",
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
        canteen = CanteenFactory.create(
            creation_mtm_source="mtm_source_value",
            creation_mtm_campaign="mtm_campaign_value",
            creation_mtm_medium="mtm_medium_value",
        )
        canteen.managers.add(authenticate.user)
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
        )
        user_canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertNotIn("mtm_source_value", body)
        self.assertNotIn("mtm_campaign_value", body)
        self.assertNotIn("mtm_medium_value", body)

    @authenticate
    def test_get_canteens_filter_production_type(self):
        user_satellite_canteen = CanteenFactory.create(production_type="site")
        user_satellite_canteen.managers.add(authenticate.user)

        user_central_cuisine = CanteenFactory.create(production_type="central")
        user_central_cuisine.managers.add(authenticate.user)

        user_central_serving_cuisine = CanteenFactory.create(production_type="central_serving")
        user_central_serving_cuisine.managers.add(authenticate.user)
        response = self.client.get(f"{reverse('user_canteens')}?production_type=central,central_serving")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["count"], 2)
        ids = list(map(lambda x: x["id"], body["results"]))
        self.assertIn(user_central_cuisine.id, ids)
        self.assertIn(user_central_serving_cuisine.id, ids)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @override_settings(PUBLISH_BY_DEFAULT=False)
    @authenticate
    def test_get_canteen_actions(self):
        """
        Check that this endpoint returns the user's canteens and the next action required
        """
        # these canteens aren't in a very logical order, because want to test sorting by action
        # create diag (has one for 2020)
        needs_last_year_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.DRAFT,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        # nothing to do
        complete = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        # complete diag
        needs_to_complete_diag = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.DRAFT,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        needs_diagnostic_mode = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            siret="75665621899905",
        )
        # publish
        needs_to_publish = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.DRAFT,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        # TD
        needs_td = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        # create satellites
        central_siret = "78146469373706"
        needs_additional_satellites = CanteenFactory.create(
            siret=central_siret,
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=3,
        )
        CanteenFactory.create(name="Not my canteen")
        for canteen in [
            needs_last_year_diag,
            complete,
            needs_to_complete_diag,
            needs_diagnostic_mode,
            needs_to_publish,
            needs_td,
            needs_additional_satellites,
        ]:
            canteen.managers.add(authenticate.user)

        last_year = 2021
        DiagnosticFactory.create(year=last_year - 1, canteen=needs_last_year_diag)

        td_diag = DiagnosticFactory.create(year=last_year, canteen=complete, value_total_ht=1000)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)

        DiagnosticFactory.create(year=last_year, canteen=needs_to_complete_diag, value_total_ht=None)
        # make sure the endpoint only looks at diagnostics of the year requested
        DiagnosticFactory.create(year=last_year - 1, canteen=needs_to_complete_diag, value_total_ht=1000)

        DiagnosticFactory.create(
            year=last_year, canteen=needs_diagnostic_mode, central_kitchen_diagnostic_mode=None, value_total_ht=100
        )

        td_diag = DiagnosticFactory.create(year=last_year, canteen=needs_to_publish, value_total_ht=10)
        Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)

        DiagnosticFactory.create(year=last_year, canteen=needs_td, value_total_ht=100)

        # has a diagnostic but this canteen registered only two of three satellites
        DiagnosticFactory.create(year=last_year, canteen=needs_additional_satellites, value_total_ht=100)
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_siret
        )
        CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_siret
        )

        response = self.client.get(
            reverse("list_actionable_canteens", kwargs={"year": last_year}) + "?ordering=action,modification_date"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        returned_canteens = body["results"]
        self.assertEqual(len(returned_canteens), 7)

        expected_actions = [
            (needs_additional_satellites, "10_add_satellites"),
            (needs_last_year_diag, "20_create_diagnostic"),
            (needs_to_complete_diag, "30_complete_diagnostic"),
            (needs_diagnostic_mode, "30_complete_diagnostic"),
            (needs_td, "40_teledeclare"),
            (needs_to_publish, "50_publish"),
            (complete, "95_nothing"),
        ]
        for index, (canteen, action) in zip(range(len(expected_actions)), expected_actions):
            self.assertEqual(returned_canteens[index]["id"], canteen.id)
            self.assertEqual(returned_canteens[index]["action"], action)
            self.assertIn("sectors", returned_canteens[index])
        self.assertTrue(body["hasPendingActions"])

    @override_settings(PUBLISH_BY_DEFAULT=True)
    @authenticate
    def test_no_canteens_to_publish(self):
        """
        When publish by default is set, don't send publication actions
        """
        # make them all on site to avoid having to create satellites
        previously_published = CanteenFactory.create(
            name="published canteen",
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            line_ministry=None,
        )
        previously_draft = CanteenFactory.create(
            name="supposedly draft canteen",
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            line_ministry=None,
        )
        public_ministry = CanteenFactory.create(
            name="canteen with administration ministry",
            production_type=Canteen.ProductionType.ON_SITE,
            line_ministry=Canteen.Ministries.ADMINISTRATION_TERRITORIALE,
        )
        private_ministry = CanteenFactory.create(
            name="a private canteen",
            production_type=Canteen.ProductionType.ON_SITE,
            line_ministry=Canteen.Ministries.ARMEE,
        )
        diag_year = 2023
        for canteen in [
            previously_published,
            previously_draft,
            public_ministry,
            private_ministry,
        ]:
            canteen.managers.add(authenticate.user)
            # give them all teledeclarations to skip to final action
            td_diag = DiagnosticFactory.create(year=diag_year, canteen=canteen, value_total_ht=10)
            Teledeclaration.create_from_diagnostic(td_diag, authenticate.user)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": diag_year}) + "?ordering=name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body["canteensToPublish"]), 0)
        returned_canteens = body["results"]
        for canteen in returned_canteens:
            canteen["action"] = "95_nothing"

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_central_without_satellites_has_complete_satellites_action(self):
        """
        Test for a bug fix. A central that doesn't have any satellites at all should get the complete satellite action.
        """
        has_no_satellites = CanteenFactory.create(
            siret="45467900121441",
            production_type=Canteen.ProductionType.CENTRAL,
            satellite_canteens_count=3,
        )
        has_no_satellites.managers.add(authenticate.user)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}) + "?ordering=action")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["results"][0]["action"], "10_add_satellites")

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_get_actions_missing_data(self):
        """
        Even if the diagnostic is complete, the mandatory information on the canteen level should
        return a "35_fill_canteen_data"
        """
        # First a case in which the canteen is complete
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        diagnostic = DiagnosticFactory.create(year=2021, canteen=canteen, value_total_ht=1000)
        canteen.managers.add(authenticate.user)
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "40_teledeclare")

        # If mandatory data on the canteen is missing, we need a 35_fill_canteen_data
        canteen.yearly_meal_count = None
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "35_fill_canteen_data")

        # Central cuisines should have the number of satellites filled in
        canteen.yearly_meal_count = 1000
        canteen.production_type = Canteen.ProductionType.CENTRAL
        canteen.satellite_canteens_count = None
        canteen.save()
        diagnostic.central_kitchen_diagnostic_mode = "APPRO"
        diagnostic.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "35_fill_canteen_data")

        # reset diag from above change.
        diagnostic.central_kitchen_diagnostic_mode = None
        diagnostic.save()

        # Central kitchens with missing satellites should return the add satellite action
        canteen.satellite_canteens_count = 123
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "10_add_satellites")

        # Satellites should have the SIRET of the central cuisine
        canteen.production_type = Canteen.ProductionType.ON_SITE_CENTRAL
        canteen.central_producer_siret = None
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "35_fill_canteen_data")

        canteen.central_producer_siret = "75665621899905"
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "40_teledeclare")

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_get_actions_satellite(self):
        """
        If a satellite's CC has teledeclared there is no pending action for the satellite
        """
        central_kitchen = CanteenFactory.create(
            production_type=Canteen.ProductionType.CENTRAL,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            satellite_canteens_count=1,
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        central_kitchen.managers.add(authenticate.user)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=10,
            daily_meal_count=2,
            siret="99569440745111",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            central_producer_siret="96766910375238",
        )
        satellite.managers.add(authenticate.user)
        diagnostic = DiagnosticFactory.create(
            year=2021,
            canteen=central_kitchen,
            value_total_ht=1000,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
        )
        Teledeclaration.create_from_diagnostic(diagnostic, authenticate.user)

        DiagnosticFactory.create(
            year=2021,
            canteen=satellite,
            value_total_ht=1200,
        )

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        satellite_action = next(x for x in returned_canteens if x["id"] == satellite.id)["action"]
        self.assertEqual(satellite_action, "95_nothing")

    @authenticate
    def test_get_canteens_with_purchases_no_diagnostics_for_year(self):
        """
        Return a list of canteens I manage who do have purchases for the given year,
        but have not yet created a diagnostic
        """
        year = 2023
        canteen_without_diag = CanteenFactory.create()
        canteen_with_diag = CanteenFactory.create()
        canteen_without_purchases = CanteenFactory.create()
        not_my_canteen = CanteenFactory.create()
        canteens = [canteen_with_diag, canteen_without_diag, canteen_without_purchases]
        for canteen in canteens:
            canteen.managers.add(authenticate.user)
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

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_filter_td_bad_sirets(self):
        """
        Check that canteens with SIRET issues (no SIRET, SIRET = central_producer_siret) have complete canteen actions and not TD actions
        """
        last_year = 2021
        canteen_with_no_siret = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            siret=None,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        # complete diag
        DiagnosticFactory.create(canteen=canteen_with_no_siret, year=last_year, value_total_ht=10000)
        canteen_with_bad_central_siret = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            siret="59282615314394",
            central_producer_siret="59282615314394",
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        # complete diag
        DiagnosticFactory.create(canteen=canteen_with_bad_central_siret, year=last_year, value_total_ht=10000)
        canteen_to_td = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            siret="55314169703815",
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
        )

        for canteen in [
            canteen_with_no_siret,
            canteen_with_bad_central_siret,
            canteen_to_td,
        ]:
            canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": last_year}))
        body = response.json()

        returned_canteens = body["results"]
        self.assertEqual(returned_canteens[0]["action"], "35_fill_canteen_data")
        self.assertEqual(returned_canteens[1]["action"], "35_fill_canteen_data")

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
        canteen = CanteenFactory.create(id=3, production_type=Canteen.ProductionType.ON_SITE)
        canteen.managers.add(authenticate.user)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], "20_create_diagnostic")

    @override_settings(ENABLE_TELEDECLARATION=False)
    @authenticate
    def test_omit_teledeclaraion_action(self):
        """
        Check that when the ENABLE_TELEDECLARATION setting is False we don't return that type of action
        """
        canteen = CanteenFactory.create(
            id=3,
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            yearly_meal_count="123",
            daily_meal_count="12",
            siret="75665621899905",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            management_type=Canteen.ManagementType.DIRECT,
        )
        canteen.managers.add(authenticate.user)
        DiagnosticFactory.create(canteen=canteen, year=2021, value_total_ht=10000)

        response = self.client.get(reverse("retrieve_actionable_canteen", kwargs={"pk": 3, "year": 2021}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], 3)
        self.assertEqual(body["action"], "95_nothing")

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
    def test_get_central_kitchen(self):
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret="96953195898254")
        satellite = CanteenFactory.create(
            central_producer_siret=central_kitchen.siret, production_type=Canteen.ProductionType.ON_SITE_CENTRAL
        )
        satellite.managers.add(authenticate.user)

        response = self.client.get(reverse("single_canteen", kwargs={"pk": satellite.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["centralKitchen"]["name"], central_kitchen.name)
        self.assertEqual(body["centralKitchen"]["id"], central_kitchen.id)

    @override_settings(ENABLE_TELEDECLARATION=True)
    @authenticate
    def test_get_actions_missing_line_ministry(self):
        """
        Even if the diagnostic is complete, the mandatory information on the canteen level should
        return a "35_fill_canteen_data" if line ministry is not there
        """
        with_lm = SectorFactory.create(has_line_ministry=True)
        without_lm = SectorFactory.create(has_line_ministry=False)
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
            management_type=Canteen.ManagementType.DIRECT,
            yearly_meal_count=1000,
            daily_meal_count=12,
            siret="96766910375238",
            city_insee_code="69123",
            economic_model=Canteen.EconomicModel.PUBLIC,
            sectors=[with_lm, without_lm],
            line_ministry=None,
        )
        DiagnosticFactory.create(year=2021, canteen=canteen, value_total_ht=1000)
        canteen.managers.add(authenticate.user)
        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "35_fill_canteen_data")

        # a canteen that has a line ministry should be complete
        canteen.line_ministry = Canteen.Ministries.AFFAIRES_ETRANGERES
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "40_teledeclare")

        # a canteen without a line ministry and without a sector that demands one is also complete
        canteen.line_ministry = None
        canteen.sectors.clear()
        canteen.sectors.set([without_lm])
        canteen.save()

        response = self.client.get(reverse("list_actionable_canteens", kwargs={"year": 2021}))
        returned_canteens = response.json()["results"]
        self.assertEqual(returned_canteens[0]["action"], "40_teledeclare")

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
        published_canteen = CanteenFactory.create(
            department="01", publication_status=Canteen.PublicationStatus.PUBLISHED
        )
        unpublished_canteen = CanteenFactory.create(
            department="02", publication_status=Canteen.PublicationStatus.DRAFT
        )
        out_of_place_canteen = CanteenFactory.create(department="03")

        # Make request
        response = self.client.get(reverse("territory_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()["results"]

        self.assertEqual(len(body), 2)
        ids = list(map(lambda x: x["id"], body))

        self.assertIn(published_canteen.id, ids)
        self.assertIn(unpublished_canteen.id, ids)
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

    @authenticate
    @freeze_time("2024-01-20")
    def test_canteen_badges(self):
        """
        The full representation of a canteen contains the badges earned for last year
        """
        user_canteen = CanteenFactory.create()
        user_canteen.managers.add(authenticate.user)

        DiagnosticFactory.create(
            canteen=user_canteen,
            year=2023,
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=30,
        )

        response = self.client.get(reverse("single_canteen", kwargs={"pk": user_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        badges = body["badges"]
        self.assertTrue("appro" in badges)

    @authenticate
    def test_canteen_returns_latest_diagnostic_year(self):
        """
        Test whether the canteen returns the latest year it has data for
        """
        central = CanteenFactory.create(siret="21340172201787", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret="21340172201787", production_type=Canteen.ProductionType.ON_SITE_CENTRAL
        )
        satellite.managers.add(authenticate.user)

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
