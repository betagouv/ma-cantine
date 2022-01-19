import os
import base64
from datetime import date
from django.urls import reverse
from django.core.files import File
from rest_framework.test import APITestCase
from rest_framework import status
from data.department_choices import Department
from data.factories import CanteenFactory, ManagerInvitationFactory, SectorFactory
from data.factories import DiagnosticFactory
from data.models import Canteen, Teledeclaration, CanteenImage, Diagnostic
from .utils import authenticate
from api.views.canteen import badges_for_queryset
from data.region_choices import Region

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestCanteenApi(APITestCase):
    def test_get_published_canteens(self):
        """
        Only published canteens with public data should be
        returned from this call
        """
        published_canteens = [
            CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value),
            CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value),
        ]
        private_canteens = [
            CanteenFactory.create(),
            CanteenFactory.create(publication_status=Canteen.PublicationStatus.PENDING.value),
        ]
        response = self.client.get(reverse("published_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("count"), 2)

        results = body.get("results", [])

        for published_canteen in published_canteens:
            self.assertTrue(any(x["id"] == published_canteen.id for x in results))

        for private_canteen in private_canteens:
            self.assertFalse(any(x["id"] == private_canteen.id for x in results))

        for recieved_canteen in results:
            self.assertFalse("managers" in recieved_canteen)
            self.assertFalse("managerInvitations" in recieved_canteen)

    def test_get_single_published_canteen(self):
        """
        We are able to get a single published canteen.
        """
        published_canteen = CanteenFactory.create(publication_status="published")
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": published_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("id"), published_canteen.id)

    def test_get_single_unpublished_canteen(self):
        """
        A 404 is raised if we try to get a sinlge published canteen
        that has not been published by the manager.
        """
        private_canteen = CanteenFactory.create()
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": private_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
            "management_type": "direct",
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(created_canteen.city, "Lyon")
        self.assertEqual(created_canteen.siret, "21340172201787")
        self.assertEqual(created_canteen.management_type, "direct")

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
            "management_type": "direct",
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

        payload = {"name": "My canteen", "central_producer_siret": "01234567891011"}

        response = self.client.post(reverse("user_canteens"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        body = response.json()
        self.assertEqual(body["centralProducerSiret"], ["Le numéro SIRET n'est pas valide."])

    def test_search_single_result(self):
        CanteenFactory.create(publication_status="published", name="Shiso")
        CanteenFactory.create(publication_status="published", name="Wasabi")
        CanteenFactory.create(publication_status="published", name="Mochi")
        CanteenFactory.create(publication_status="published", name="Umami")

        search_term = "mochi"
        response = self.client.get(f"{reverse('published_canteens')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Mochi")

    def test_search_accented_result(self):
        CanteenFactory.create(publication_status="published", name="Wakamé")
        CanteenFactory.create(publication_status="published", name="Shiitaké")

        search_term = "wakame"
        response = self.client.get(f"{reverse('published_canteens')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Wakamé")

    def test_search_multiple_results(self):
        CanteenFactory.create(publication_status="published", name="Sudachi")
        CanteenFactory.create(publication_status="published", name="Wasabi")
        CanteenFactory.create(publication_status="published", name="Mochi")
        CanteenFactory.create(publication_status="published", name="Umami")

        search_term = "chi"
        response = self.client.get(f"{reverse('published_canteens')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 2)

        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Mochi", result_names)
        self.assertIn("Sudachi", result_names)

    def test_meal_count_filter(self):
        CanteenFactory.create(publication_status="published", daily_meal_count=10, name="Shiso")
        CanteenFactory.create(publication_status="published", daily_meal_count=15, name="Wasabi")
        CanteenFactory.create(publication_status="published", daily_meal_count=20, name="Mochi")
        CanteenFactory.create(publication_status="published", daily_meal_count=25, name="Umami")

        # Only "Shiso" is between 9 and 11 meal count
        min_meal_count = 9
        max_meal_count = 11
        query_params = f"min_daily_meal_count={min_meal_count}&max_daily_meal_count={max_meal_count}"
        url = f"{reverse('published_canteens')}?{query_params}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Shiso")

        # "Shiso" and "Wasabi" are between 9 and 15 meal count
        min_meal_count = 9
        max_meal_count = 15
        query_params = f"min_daily_meal_count={min_meal_count}&max_daily_meal_count={max_meal_count}"
        url = f"{reverse('published_canteens')}?{query_params}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Wasabi", result_names)

        # No canteen has less than 5 meal count
        max_meal_count = 5
        query_params = f"max_daily_meal_count={max_meal_count}"
        url = f"{reverse('published_canteens')}?{query_params}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 0)

        # Filters are inclusive, so a value of 25 brings "Umami"
        min_meal_count = 25
        query_params = f"min_daily_meal_count={min_meal_count}"
        url = f"{reverse('published_canteens')}?{query_params}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Umami")

    def test_department_filter(self):
        CanteenFactory.create(publication_status="published", department="69", name="Shiso")
        CanteenFactory.create(publication_status="published", department="10", name="Wasabi")
        CanteenFactory.create(publication_status="published", department="75", name="Mochi")
        CanteenFactory.create(publication_status="published", department="31", name="Umami")

        url = f"{reverse('published_canteens')}?department=69"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Shiso")

    def test_sectors_filter(self):
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        social = SectorFactory.create(name="Social")
        CanteenFactory.create(publication_status="published", sectors=[school], name="Shiso")
        CanteenFactory.create(publication_status="published", sectors=[enterprise], name="Wasabi")
        CanteenFactory.create(publication_status="published", sectors=[social], name="Mochi")
        CanteenFactory.create(publication_status="published", sectors=[school, social], name="Umami")

        url = f"{reverse('published_canteens')}?sectors={school.id}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Umami", result_names)

        url = f"{reverse('published_canteens')}?sectors={enterprise.id}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Wasabi")

        url = f"{reverse('published_canteens')}?sectors={enterprise.id}&sectors={social.id}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Wasabi", result_names)
        self.assertIn("Mochi", result_names)
        self.assertIn("Umami", result_names)

    def test_order_search(self):
        """
        By default, list canteens by creation date descending
        Optionally sort by name, modification date, number of meals
        """
        CanteenFactory.create(
            publication_status="published",
            daily_meal_count=200,
            name="Shiso",
        )
        CanteenFactory.create(
            publication_status="published",
            daily_meal_count=100,
            name="Wasabi",
        )
        last_modified = CanteenFactory.create(
            publication_status="published",
            daily_meal_count=300,
            name="Mochi",
        )
        CanteenFactory.create(
            publication_status="published",
            daily_meal_count=100,
            name="Umami",
        )
        last_modified.daily_meal_count = 900
        last_modified.save()

        url = f"{reverse('published_canteens')}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Umami")
        self.assertEqual(results[1]["name"], "Mochi")
        self.assertEqual(results[2]["name"], "Wasabi")
        self.assertEqual(results[3]["name"], "Shiso")

        url = f"{reverse('published_canteens')}?ordering=name"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Mochi")
        self.assertEqual(results[1]["name"], "Shiso")
        self.assertEqual(results[2]["name"], "Umami")
        self.assertEqual(results[3]["name"], "Wasabi")

        url = f"{reverse('published_canteens')}?ordering=-modification_date"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Mochi")
        self.assertEqual(results[1]["name"], "Umami")
        self.assertEqual(results[2]["name"], "Wasabi")
        self.assertEqual(results[3]["name"], "Shiso")

        url = f"{reverse('published_canteens')}?ordering=daily_meal_count"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Wasabi")
        self.assertEqual(results[1]["name"], "Umami")
        self.assertEqual(results[2]["name"], "Shiso")
        self.assertEqual(results[3]["name"], "Mochi")

    def test_filter_appro_values(self):
        """
        Should be able to filter by bio %, sustainable %, combined % based on last year's diagnostic
        """
        good_canteen = CanteenFactory.create(publication_status="published", name="Shiso")
        medium_canteen = CanteenFactory.create(publication_status="published", name="Wasabi")
        sustainable_canteen = CanteenFactory.create(publication_status="published", name="Umami")
        bad_canteen = CanteenFactory.create(publication_status="published", name="Mochi")
        secretly_good_canteen = CanteenFactory.create(publication_status="draft", name="Secret")

        publication_year = date.today().year - 1
        DiagnosticFactory.create(
            canteen=good_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=30,
        )
        DiagnosticFactory.create(
            canteen=secretly_good_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=30,
        )
        DiagnosticFactory.create(
            canteen=medium_canteen,
            year=publication_year,
            value_total_ht=1000,
            value_bio_ht=150,
            value_sustainable_ht=350,
        )
        DiagnosticFactory.create(
            canteen=sustainable_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=0,
            value_sustainable_ht=60,
        )
        DiagnosticFactory.create(
            canteen=bad_canteen,
            year=2019,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=30,
        )
        DiagnosticFactory.create(
            canteen=bad_canteen,
            year=publication_year,
            value_total_ht=10,
            value_bio_ht=0,
            value_sustainable_ht=0,
        )
        url = f"{reverse('published_canteens')}?min_portion_bio={0.2}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)

        url = f"{reverse('published_canteens')}?min_portion_combined={0.5}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 3)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Wasabi", result_names)
        self.assertIn("Umami", result_names)

        url = f"{reverse('published_canteens')}?min_portion_bio={0.1}&min_portion_combined={0.5}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Wasabi", result_names)

    def test_pagination_departments(self):
        CanteenFactory.create(publication_status="published", department="75", name="Shiso")
        CanteenFactory.create(publication_status="published", department="75", name="Wasabi")
        CanteenFactory.create(publication_status="published", department="69", name="Mochi")
        CanteenFactory.create(publication_status="published", department=None, name="Umami")

        url = f"{reverse('published_canteens')}"
        response = self.client.get(url)
        body = response.json()

        # There are two unique departments : 75 and 69
        self.assertEqual(len(body.get("departments")), 2)
        self.assertIn("75", body.get("departments"))
        self.assertIn("69", body.get("departments"))

    def test_pagination_sectors(self):
        """
        The pagination endpoint should return all sectors that are used by canteens, even when the data is filtered by another sector
        """
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        administration = SectorFactory.create(name="Administration")
        # unused sectors shouldn't show up as an option
        SectorFactory.create(name="Unused")
        CanteenFactory.create(publication_status="published", sectors=[school, enterprise], name="Shiso")
        CanteenFactory.create(publication_status="published", sectors=[school], name="Wasabi")
        CanteenFactory.create(publication_status="published", sectors=[school], name="Mochi")
        CanteenFactory.create(publication_status="published", sectors=[administration], name="Umami")

        url = f"{reverse('published_canteens')}"
        response = self.client.get(url)
        body = response.json()

        self.assertEqual(len(body.get("sectors")), 3)
        self.assertIn(school.id, body.get("sectors"))
        self.assertIn(enterprise.id, body.get("sectors"))
        self.assertIn(administration.id, body.get("sectors"))

        url = f"{reverse('published_canteens')}?sectors={enterprise.id}"
        response = self.client.get(url)
        body = response.json()

        self.assertEqual(len(body.get("sectors")), 3)
        self.assertIn(school.id, body.get("sectors"))
        self.assertIn(enterprise.id, body.get("sectors"))
        self.assertIn(administration.id, body.get("sectors"))

    def test_pagination_management_types(self):
        CanteenFactory.create(publication_status="published", management_type="conceded", name="Shiso")
        CanteenFactory.create(publication_status="published", management_type=None, name="Wasabi")

        url = f"{reverse('published_canteens')}"
        response = self.client.get(url)
        body = response.json()

        self.assertEqual(len(body.get("managementTypes")), 1)
        self.assertIn("conceded", body.get("managementTypes"))

    @authenticate
    def test_canteen_publication_fields_read_only(self):
        """
        Users cannot modify canteen publication fields with this endpoint
        """
        canteen = CanteenFactory.create(city="Paris")
        canteen.managers.add(authenticate.user)
        payload = {
            "publication_status": "pending",
            "publication_comments": "Some comments",
        }
        response = self.client.patch(reverse("single_canteen", kwargs={"pk": canteen.id}), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        persisted_canteen = Canteen.objects.get(pk=canteen.id)
        self.assertEqual(persisted_canteen.publication_status, Canteen.PublicationStatus.DRAFT.value)
        self.assertEqual(persisted_canteen.publication_comments, None)

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
    def test_canteen_image_serialization(self):
        """
        A canteen with images should serialize those images
        """
        canteen = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        image_names = [
            "test-image-1.jpg",
            "test-image-2.jpg",
            "test-image-3.png",
        ]
        for image_name in image_names:
            path = os.path.join(CURRENT_DIR, f"files/{image_name}")
            with open(path, "rb") as image:
                file = File(image)
                file.name = image_name
                canteen_image = CanteenImage(image=file)
                canteen_image.canteen = canteen
                canteen_image.save()

        response = self.client.get(reverse("published_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        results = body.get("results", [])

        self.assertEqual(body.get("count"), 1)
        self.assertEqual(len(results[0].get("images")), 3)

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
            "management_type": "direct",
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

    def test_canteen_statistics(self):
        """
        This public endpoint returns some summary statistics for a region and a location
        """
        # TODO: more nuance when choosing canteens to get stats for?
        # How do we know that the canteen diagnostic is done?
        # Could check for total value ht

        # create 5 canteens (3 in region of interest), 1 unpublished
        region = "01"
        year = 2020
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        social = SectorFactory.create(name="Social")

        published = CanteenFactory.create(
            region=region,
            publication_status=Canteen.PublicationStatus.PUBLISHED.value,
            sectors=[school, enterprise],
            daily_meal_count=50,
        )
        unpublished = CanteenFactory.create(
            region=region,
            publication_status=Canteen.PublicationStatus.DRAFT.value,
            sectors=[school],
            daily_meal_count=50,
        )
        other_region = CanteenFactory.create(region="03", sectors=[social], daily_meal_count=50)

        # relevant diagnostics
        DiagnosticFactory.create(
            canteen=published,
            year=year,
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=30,
            has_waste_diagnostic=False,
            waste_actions=[],
            vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.DAILY,
            plastic_tableware_substituted=False,
            communicates_on_food_quality=False,
        )
        DiagnosticFactory.create(
            canteen=unpublished,
            year=year,
            value_total_ht=1000,
            value_bio_ht=400,
            value_sustainable_ht=500,
            has_waste_diagnostic=True,
            waste_actions=["action1", "action2"],
            vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.LOW,
            cooking_plastic_substituted=True,
            serving_plastic_substituted=True,
            plastic_bottles_substituted=True,
            plastic_tableware_substituted=True,
            communicates_on_food_quality=True,
        )
        # irrelevant diagnostics
        DiagnosticFactory.create(
            canteen=published,
            year=2019,
            value_total_ht=100,
            value_bio_ht=100,
            value_sustainable_ht=0,
            vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.DAILY,
        )
        DiagnosticFactory.create(
            canteen=other_region,
            year=year,
            value_total_ht=100,
            value_bio_ht=100,
            value_sustainable_ht=0,
            cooking_plastic_substituted=True,
            serving_plastic_substituted=True,
            plastic_bottles_substituted=True,
            plastic_tableware_substituted=True,
            communicates_on_food_quality=True,
        )

        response = self.client.get(reverse("canteen_statistics"), {"region": region, "year": year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 2)
        self.assertEqual(body["publishedCanteenCount"], 1)
        self.assertEqual(body["bioPercent"], 30)
        self.assertEqual(body["sustainablePercent"], 40)
        self.assertEqual(body["approPercent"], 100)
        self.assertEqual(body["wastePercent"], 50)
        self.assertEqual(body["diversificationPercent"], 50)
        self.assertEqual(body["plasticPercent"], 50)
        self.assertEqual(body["infoPercent"], 50)
        expected_sectors = {}
        expected_sectors[str(school.id)] = 2
        expected_sectors[str(enterprise.id)] = 1
        expected_sectors[str(social.id)] = 0
        self.assertEqual(body["sectors"], expected_sectors)

        # can also call without location info
        response = self.client.get(reverse("canteen_statistics"), {"year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_canteen_stats_by_department(self):
        department = "01"
        year = 2020
        CanteenFactory.create(department=department, publication_status=Canteen.PublicationStatus.PUBLISHED.value)

        response = self.client.get(reverse("canteen_statistics"), {"department": department, "year": year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 1)

    def test_canteen_stats_missing_data(self):
        response = self.client.get(reverse("canteen_statistics"), {"region": "01"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse("canteen_statistics"), {"department": "01"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_appro_badge_earned(self):
        """
        Test that the right canteens are identified in appro badge queryset
        """
        # --- Canteens which don't earn appro badge:
        zero_total = CanteenFactory.create()
        DiagnosticFactory.create(canteen=zero_total, value_total_ht=0)
        null_total = CanteenFactory.create()
        DiagnosticFactory.create(canteen=null_total, value_total_ht=None)
        bio_lacking = CanteenFactory.create()
        DiagnosticFactory.create(canteen=bio_lacking, value_total_ht=100, value_bio_ht=19, value_sustainable_ht=31)
        # not convinced the following shouldn't get a badge but not sure how to make the Sum function work
        null_sustainable = CanteenFactory.create(region=Region.ile_de_france.value)
        DiagnosticFactory.create(
            canteen=null_sustainable, value_total_ht=100, value_bio_ht=50, value_sustainable_ht=None
        )

        # --- Canteens which earn appro badge:
        earned = CanteenFactory.create()
        DiagnosticFactory.create(canteen=earned, value_total_ht=100, value_bio_ht=20, value_sustainable_ht=30)
        # rules per outre mer territories
        guadeloupe = CanteenFactory.create(region=Region.guadeloupe.value)
        DiagnosticFactory.create(canteen=guadeloupe, value_total_ht=100, value_bio_ht=5, value_sustainable_ht=15)
        mayotte = CanteenFactory.create(region=Region.mayotte.value)
        DiagnosticFactory.create(canteen=mayotte, value_total_ht=100, value_bio_ht=2, value_sustainable_ht=3)
        # TODO: rules per outre mer territories: Saint-Pierre-et-Miquelon
        # st_pierre_et_miquelon = CanteenFactory.create(region=Region.st_pierre_et_miquelon.value)
        # DiagnosticFactory.create(canteen=st_pierre_et_miquelon, value_total_ht=100, value_bio_ht=10, value_sustainable_ht=20)

        badges = badges_for_queryset(Diagnostic.objects.all())

        appro_badge_qs = badges["appro"]
        self.assertTrue(appro_badge_qs.filter(canteen=earned).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=guadeloupe).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=mayotte).exists())
        self.assertEqual(appro_badge_qs.count(), 3)

    def test_waste_badge_earned(self):
        """
        Test that the right canteens are identifies in waste badge qs
        """
        # --- Canteens which don't earn waste badge:
        waste_actions_only = CanteenFactory.create(daily_meal_count=2999)
        DiagnosticFactory.create(canteen=waste_actions_only, has_waste_diagnostic=False, waste_actions=["action1"])
        waste_diagnostic_only = CanteenFactory.create(daily_meal_count=2999)
        DiagnosticFactory.create(canteen=waste_diagnostic_only, has_waste_diagnostic=True, waste_actions=[])
        large_canteen_no_badge = CanteenFactory.create(daily_meal_count=3000)
        DiagnosticFactory.create(
            canteen=large_canteen_no_badge,
            has_waste_diagnostic=True,
            waste_actions=["action1"],
            has_donation_agreement=False,
        )
        # --- Canteens which earn waste badge:
        small_canteen = CanteenFactory.create(daily_meal_count=2999)
        DiagnosticFactory.create(canteen=small_canteen, has_waste_diagnostic=True, waste_actions=["action1"])
        large_canteen = CanteenFactory.create(daily_meal_count=3000)
        DiagnosticFactory.create(
            canteen=large_canteen, has_waste_diagnostic=True, waste_actions=["action1"], has_donation_agreement=True
        )

        badges = badges_for_queryset(Diagnostic.objects.all())

        waste_badge_qs = badges["waste"]
        self.assertEqual(waste_badge_qs.count(), 2)
        self.assertTrue(waste_badge_qs.filter(canteen=small_canteen).exists())
        self.assertTrue(waste_badge_qs.filter(canteen=large_canteen).exists())

    def test_diversification_badge_earned(self):
        """
        Test that the right canteens are identifies in diversification badge qs
        """
        scolaire_sector = SectorFactory(name="Scolaire")

        # --- canteens which don't earn diversification badge:
        high_canteen = CanteenFactory.create()
        high_canteen.sectors.remove(scolaire_sector)
        DiagnosticFactory.create(
            canteen=high_canteen, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.HIGH.value
        )

        low_canteen = CanteenFactory.create()
        low_canteen.sectors.add(scolaire_sector)
        DiagnosticFactory.create(canteen=low_canteen, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.LOW.value)

        # --- canteens which earn diversification badge:
        daily_vege = CanteenFactory.create()
        daily_vege.sectors.remove(scolaire_sector)
        DiagnosticFactory.create(canteen=daily_vege, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.DAILY.value)

        scolaire_mid_vege = CanteenFactory.create()
        scolaire_mid_vege.sectors.add(scolaire_sector)
        DiagnosticFactory.create(
            canteen=scolaire_mid_vege, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.MID.value
        )

        badges = badges_for_queryset(Diagnostic.objects.all())

        diversification_badge_qs = badges["diversification"]
        self.assertEqual(diversification_badge_qs.count(), 2)
        self.assertTrue(diversification_badge_qs.filter(canteen=daily_vege).exists())
        self.assertTrue(diversification_badge_qs.filter(canteen=scolaire_mid_vege).exists())

    def test_plastic_badge_earned(self):
        """
        Test that the right canteens are identifies in plastic badge qs
        """
        # --- canteens which don't earn
        no_cooking = CanteenFactory.create()
        DiagnosticFactory.create(canteen=no_cooking, cooking_plastic_substituted=False)
        no_serving = CanteenFactory.create()
        DiagnosticFactory.create(canteen=no_serving, serving_plastic_substituted=False)
        no_bottles = CanteenFactory.create()
        DiagnosticFactory.create(canteen=no_bottles, plastic_bottles_substituted=False)
        no_tableware = CanteenFactory.create()
        DiagnosticFactory.create(canteen=no_tableware, plastic_tableware_substituted=False)
        # --- canteens which earn plastic badge:
        earned = CanteenFactory.create()
        DiagnosticFactory.create(
            canteen=earned,
            cooking_plastic_substituted=True,
            serving_plastic_substituted=True,
            plastic_bottles_substituted=True,
            plastic_tableware_substituted=True,
        )

        badges = badges_for_queryset(Diagnostic.objects.all())

        plastic_badge_qs = badges["plastic"]
        self.assertEqual(plastic_badge_qs.count(), 1)
        self.assertTrue(plastic_badge_qs.filter(canteen=earned).exists())

    def test_info_badge_earned(self):
        """
        Test that the right canteens are identified in info badge qs
        """
        no_communicated = CanteenFactory.create()
        DiagnosticFactory.create(canteen=no_communicated, communicates_on_food_quality=False)
        earned = CanteenFactory.create()
        DiagnosticFactory.create(canteen=earned, communicates_on_food_quality=True)

        badges = badges_for_queryset(Diagnostic.objects.all())

        info_badge_qs = badges["info"]
        self.assertEqual(info_badge_qs.count(), 1)
        self.assertTrue(info_badge_qs.filter(canteen=earned).exists())

    def test_canteen_locations(self):
        """
        Test that the right subset of regions and departments 'in use' by canteens are returned
        """
        CanteenFactory.create(department=Department.aisne)
        CanteenFactory.create(department=Department.ain)
        # set region directly
        CanteenFactory.create(region=Region.guadeloupe, department=None)
        # create extra to check that list returned doesn't contain duplicates
        CanteenFactory.create(department=Department.aisne)
        CanteenFactory.create(department="999")  # not a department, checking None on region
        CanteenFactory.create(region="", department="")  # checking exlusion of blank strings

        response = self.client.get(reverse("canteen_locations"))

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body["regions"]), 3)
        self.assertEqual(Region.guadeloupe, body["regions"][0])
        self.assertEqual(Region.hauts_de_france, body["regions"][1])
        self.assertEqual(Region.auvergne_rhone_alpes, body["regions"][2])
        self.assertEqual(len(body["departments"]), 3)
        self.assertIn(Department.ain, body["departments"][0])
        self.assertIn(Department.aisne, body["departments"][1])
        self.assertIn("999", body["departments"])
