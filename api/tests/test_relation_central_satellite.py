from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory, SectorFactory, UserFactory
from data.models import Canteen

from .utils import authenticate


class TestRelationCentralSatellite(APITestCase):
    """
    This test case examines the relationship between central/central_serving canteen production types with
    their satellites
    """

    @authenticate
    def test_get_satellites(self):
        """
        When requesting data for a canteen who is listed as the
        producer for other canteens, return some data for those canteens
        """
        central_siret = "22730656663081"
        central = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        satellite_1 = CanteenFactory.create(
            central_producer_siret=central_siret,
            sectors=[school, enterprise],
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )
        # although user does not have mgmt rights on this, can get same data
        satellite_2 = CanteenFactory.create(
            central_producer_siret=central_siret, production_type=Canteen.ProductionType.ON_SITE_CENTRAL
        )
        # the following canteen should not be returned
        CanteenFactory.create()
        # neither should this canteen which isn't the satellite production type
        not_a_satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE,
        )
        user = authenticate.user
        for canteen in [central, satellite_1, not_a_satellite]:
            canteen.managers.add(user)

        response = self.client.get(reverse("list_create_update_satellite", kwargs={"canteen_pk": central.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()["results"]

        self.assertEqual(len(body), 2)
        satellite_1_result = next(canteen for canteen in body if canteen["id"] == satellite_1.id)
        self.assertEqual(satellite_1_result["siret"], satellite_1.siret)
        self.assertEqual(satellite_1_result["name"], satellite_1.name)
        self.assertEqual(satellite_1_result["dailyMealCount"], satellite_1.daily_meal_count)
        self.assertIn(school.id, satellite_1_result["sectors"])
        self.assertIn(enterprise.id, satellite_1_result["sectors"])

        # just checking if satellite 2 is in there too
        satellite_2_result = next(canteen for canteen in body if canteen["id"] == satellite_2.id)
        self.assertEqual(satellite_2_result["siret"], satellite_2.siret)

    @authenticate
    def test_get_satellites_with_publication_info(self):
        """
        Test that a list of the ids of the publishable satellites, and a count of unpublished
        satellites is returned with the satellite list
        """
        central_siret = "22730656663081"
        central = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite_1 = CanteenFactory.create(
            central_producer_siret=central_siret,
            publication_status=Canteen.PublicationStatus.DRAFT,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )
        # although user does not have mgmt rights on this, can get same data
        CanteenFactory.create(
            central_producer_siret=central_siret,
            publication_status=Canteen.PublicationStatus.DRAFT,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )
        # the following canteen should not be returned
        CanteenFactory.create()
        user = authenticate.user
        for canteen in [central, satellite_1]:
            canteen.managers.add(user)

        response = self.client.get(reverse("list_create_update_satellite", kwargs={"canteen_pk": central.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["unpublishedCount"], 2)
        self.assertEqual(body["satellitesToPublish"], [satellite_1.id])

    def test_create_satellite_unauthenticated(self):
        """
        Shouldn't be able to create satellites if not logged in
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_satellite_not_manager(self):
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_satellites_not_manager(self):
        canteen = CanteenFactory.create()
        response = self.client.get(reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_satellite(self):
        """
        When the endpoint is called, create new canteens, adding in some additional helpful information
        """
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        second_manager = UserFactory.create()
        canteen.managers.add(second_manager)
        # all the mgmt team of the cuisine centrale should be added to the satellite team

        satellite_siret = "38782537682311"
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        request = {
            "name": "Wanderer",
            "siret": satellite_siret,
            "dailyMealCount": 30,
            "sectors": [school.id, enterprise.id],
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        satellite = Canteen.objects.get(siret=satellite_siret)
        self.assertEqual(satellite.name, "Wanderer")
        self.assertEqual(satellite.sectors.count(), 2)
        self.assertIn(school, satellite.sectors.all())
        self.assertIn(enterprise, satellite.sectors.all())
        self.assertEqual(satellite.publication_status, Canteen.PublicationStatus.PUBLISHED)
        self.assertEqual(satellite.import_source, "Cuisine centrale : 08376514425566")
        self.assertEqual(satellite.central_producer_siret, central_siret)
        self.assertEqual(satellite.production_type, Canteen.ProductionType.ON_SITE_CENTRAL)
        self.assertIn(authenticate.user, satellite.managers.all())
        self.assertIn(second_manager, satellite.managers.all())
        self.assertEqual(response.json()["name"], "Wanderer")  # cursory test to check returning new satellite object

    @authenticate
    def test_add_existing_satellite(self):
        """
        Ability to create a link between a central and a satellite that already exists,
        sending off a request to join the mgmt team if necessary (200)
        """
        satellite_siret = "89834106501485"
        existing_canteen = CanteenFactory.create(
            siret=satellite_siret, production_type=Canteen.ProductionType.ON_SITE_CENTRAL
        )
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertEqual(existing_canteen.central_producer_siret, canteen.siret)

    @authenticate
    def test_add_existing_site_satellite(self):
        """
        If the added canteen exists already and has a "site" production type, we must update
        it to "satellite"
        """
        satellite_siret = "89834106501485"
        existing_canteen = CanteenFactory.create(siret=satellite_siret, production_type=Canteen.ProductionType.ON_SITE)
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertEqual(existing_canteen.production_type, Canteen.ProductionType.ON_SITE_CENTRAL)

    @authenticate
    def test_add_existing_satellite_without_managers(self):
        """
        If the satellite has no managers, the CC managers get access to it
        """
        satellite_siret = "89834106501485"
        existing_canteen = CanteenFactory.create(siret=satellite_siret, production_type=Canteen.ProductionType.ON_SITE)
        existing_canteen.managers.all().delete()
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertIn(authenticate.user, existing_canteen.managers.all())

    @authenticate
    def test_add_existing_satellite_with_managers(self):
        """
        If the satellite already has managers, the CC managers do not get automatic access
        """
        satellite_siret = "89834106501485"
        existing_canteen = CanteenFactory.create(siret=satellite_siret, production_type=Canteen.ProductionType.ON_SITE)
        existing_canteen.managers.add(UserFactory.create())
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertNotIn(authenticate.user, existing_canteen.managers.all())

    @authenticate
    def test_add_existing_satellite_already_linked(self):
        """
        If the satellite targeted already has a central siret listed, don't change anything
        """
        existing_central_cuisine_siret = "21822171376603"
        satellite_siret = "89834106501485"
        linked_canteen = CanteenFactory.create(
            siret=satellite_siret,
            production_type=Canteen.ProductionType.ON_SITE,
            central_producer_siret=existing_central_cuisine_siret,
        )
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        request = {
            "name": linked_canteen.name,
            "siret": linked_canteen.siret,
            "dailyMealCount": linked_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "Cette cantine est déjà fourni par une autre cuisine centrale")
        linked_canteen.refresh_from_db()
        self.assertEqual(linked_canteen.central_producer_siret, existing_central_cuisine_siret)

    @authenticate
    def test_add_central_cuisine_as_satellite(self):
        """
        It should not be possible to add a central cuisine as a satellite of another central cuisine
        """
        satellite_siret = "89834106501485"
        central_satellite_canteen = CanteenFactory.create(
            siret=satellite_siret, production_type=Canteen.ProductionType.CENTRAL
        )
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        canteen.managers.add(authenticate.user)
        request = {
            "name": central_satellite_canteen.name,
            "siret": central_satellite_canteen.siret,
            "dailyMealCount": central_satellite_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "La cantine renseignée est une cuisine centrale")
        central_satellite_canteen.refresh_from_db()
        self.assertIsNone(central_satellite_canteen.central_producer_siret)

    @authenticate
    def test_add_satellites_to_non_central(self):
        """
        It should not be possible to add a satellites to canteens that are not central cuisines
        """
        satellite_siret = "89834106501485"
        satellite_canteen = CanteenFactory.create(
            siret=satellite_siret, production_type=Canteen.ProductionType.ON_SITE
        )
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.ON_SITE)
        canteen.managers.add(authenticate.user)
        request = {
            "name": satellite_canteen.name,
            "siret": satellite_canteen.siret,
            "dailyMealCount": satellite_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        satellite_canteen.refresh_from_db()
        self.assertIsNone(satellite_canteen.central_producer_siret)

    def test_remove_added_satellite_unauthenticated(self):
        """
        Shouldn't be able to remove satellites if not logged in
        """
        central_siret = "08376514425566"
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret=central_siret)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
        )

        response = self.client.post(
            reverse("unlink_satellite", kwargs={"canteen_pk": central_kitchen.id, "satellite_pk": satellite.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_remove_added_satellite_not_manager(self):
        """
        Shouldn't be able to remove satellites if the user does not manage the central kitchen
        """
        central_siret = "08376514425566"
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret=central_siret)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
        )

        response = self.client.post(
            reverse("unlink_satellite", kwargs={"canteen_pk": central_kitchen.id, "satellite_pk": satellite.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_remove_added_satellite(self):
        """
        Should be able to remove satellites from a central kitchen
        """
        central_siret = "08376514425566"
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret=central_siret)
        central_kitchen.managers.add(authenticate.user)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL, central_producer_siret=central_kitchen.siret
        )

        response = self.client.post(
            reverse("unlink_satellite", kwargs={"canteen_pk": central_kitchen.id, "satellite_pk": satellite.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        satellite.refresh_from_db()
        self.assertNotEqual(satellite.central_producer_siret, central_kitchen.siret)

        body = response.json()
        self.assertEqual(len(body["satellites"]), 0)

    @authenticate
    def test_remove_unexistent_satellite(self):
        """
        Removing a non-linked satellite from a central kitchen should be a transparent operation
        """
        central_siret = "08376514425566"
        central_kitchen = CanteenFactory.create(production_type=Canteen.ProductionType.CENTRAL, siret=central_siret)
        central_kitchen.managers.add(authenticate.user)
        unlinked_satellite_siret = "86891081916867"

        response = self.client.post(
            reverse(
                "unlink_satellite", kwargs={"canteen_pk": central_kitchen.id, "satellite_pk": unlinked_satellite_siret}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_remove_unexistent_central_kitchen(self):
        """
        Using the ID of a non-existent central kitchen should return a 403
        """
        unexistent_central_kitchen_id = 1234
        unexistent_satellite_id = 2345

        response = self.client.post(
            reverse(
                "unlink_satellite",
                kwargs={"canteen_pk": unexistent_central_kitchen_id, "satellite_pk": unexistent_satellite_id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
