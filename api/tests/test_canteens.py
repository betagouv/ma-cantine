import os
import base64
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, ManagerInvitationFactory
from data.factories import DiagnosticFactory
from data.models import Canteen, Teledeclaration
from .utils import authenticate

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCanteenApi(APITestCase):
    def test_get_canteens_unauthenticated(self):
        """
        If the user is not authenticated, they will not be able to
        access the full representation of the canteens
        """
        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertNotIn("isManagedByUser", body)
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
        self.assertNotIn("isManagedByUser", body)

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
        Teledeclaration.createFromDiagnostic(diagnostic, user, Teledeclaration.TeledeclarationStatus.CANCELLED)

        new_teledeclaration = Teledeclaration.createFromDiagnostic(diagnostic, user)
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
