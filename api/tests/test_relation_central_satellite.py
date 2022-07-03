from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data.factories import CanteenFactory, SectorFactory
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
