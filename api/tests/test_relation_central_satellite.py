from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, SectorFactory, UserFactory
from data.models import Canteen
from .utils import authenticate


# This test case examines the relationship between
# central/central_serving canteen production types with
# their satellites
class TestRelationCentralSatellite(APITestCase):
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
        satellite_1 = CanteenFactory.create(central_producer_siret=central_siret, sectors=[school, enterprise])
        # although user does not have mgmt rights on this, can get same data
        satellite_2 = CanteenFactory.create(central_producer_siret=central_siret)
        # the following canteen should not be returned
        CanteenFactory.create()
        user = authenticate.user
        for canteen in [central, satellite_1]:
            canteen.managers.add(user)

        response = self.client.get(reverse("user_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json().get("results")

        self.assertEqual(len(body), 2)
        central_result = next(canteen for canteen in body if canteen["siret"] == central_siret)
        satellites = central_result["satellites"]
        self.assertEqual(len(satellites), 2)
        satellite_1_result = next(canteen for canteen in satellites if canteen["id"] == satellite_1.id)
        self.assertEqual(satellite_1_result["siret"], satellite_1.siret)
        self.assertEqual(satellite_1_result["name"], satellite_1.name)
        self.assertEqual(satellite_1_result["dailyMealCount"], satellite_1.daily_meal_count)
        self.assertEqual(satellite_1_result["sectors"], [school.id, enterprise.id])
        # just checking if satellite 2 is in there too
        satellite_2_result = next(canteen for canteen in satellites if canteen["id"] == satellite_2.id)
        self.assertEqual(satellite_2_result["siret"], satellite_2.siret)

    def test_create_satellites_unauthenticated(self):
        """
        Shouldn't be able to create satellites if not logged in
        """
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("create_update_satellites", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_satellites_not_manager(self):
        canteen = CanteenFactory.create()
        response = self.client.post(reverse("create_update_satellites", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_satellites(self):
        """
        When the endpoint is called, create new canteens, adding in some additional helpful information
        """
        central_siret = "08376514425566"
        canteen = CanteenFactory.create(siret=central_siret)
        canteen.managers.add(authenticate.user)
        second_manager = UserFactory.create()
        canteen.managers.add(second_manager)
        # all the mgmt team of the cuisine centrale should be added to the satellite team

        satellite_siret = "38782537682311"
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        request = {
            "satellites": [
                {
                    "name": "Wanderer",
                    "siret": satellite_siret,
                    "dailyMealCount": 30,
                    "sectors": [school.id, enterprise.id],
                }
            ]
        }
        response = self.client.post(reverse("create_update_satellites", kwargs={"canteen_pk": canteen.id}), request)
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

    @authenticate
    def test_add_existing_satellite(self):
        """
        Ability to create a link between a central and a satellite that already exists,
        sending off a request to join the mgmt team if necessary (200)
        """
        pass

    @authenticate
    def test_add_existing_satellite_already_linked(self):
        """
        If the satellite targeted already has a central siret listed, don't change anything (404)
        """
        pass
