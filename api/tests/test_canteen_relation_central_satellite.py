from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, UserFactory
from data.models import Canteen, Sector


class TestRelationCentralSatelliteGet(APITestCase):
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
        central = CanteenFactory(
            siret=central_siret, production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        satellite_1 = CanteenFactory(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            managers=[authenticate.user],
        )
        # although user does not have mgmt rights on this, can get same data
        satellite_2 = CanteenFactory(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            managers=[authenticate.user],
        )
        # satellite with siren
        satellite_3 = CanteenFactory(
            central_producer_siret=central_siret,
            siren_unite_legale="227306566",
            siret="",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            managers=[authenticate.user],
        )
        # the following canteen should not be returned
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE)
        # neither should this canteen which isn't the satellite production type
        canteen_on_site_with_central_producer_siret = CanteenFactory(
            production_type=Canteen.ProductionType.ON_SITE,
        )
        Canteen.objects.filter(id=canteen_on_site_with_central_producer_siret.id).update(
            central_producer_siret=central_siret
        )
        canteen_on_site_with_central_producer_siret.refresh_from_db()

        response = self.client.get(reverse("list_create_update_satellite", kwargs={"canteen_pk": central.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(len(body), 3)

        satellite_1_result = next(canteen for canteen in body if canteen["id"] == satellite_1.id)
        self.assertEqual(satellite_1_result["siret"], satellite_1.siret)
        self.assertEqual(satellite_1_result["name"], satellite_1.name)
        self.assertEqual(satellite_1_result["dailyMealCount"], satellite_1.daily_meal_count)

        satellite_3_result = next(canteen for canteen in body if canteen["id"] == satellite_3.id)
        self.assertEqual(satellite_3_result["sirenUniteLegale"], satellite_3.siren_unite_legale)

        # just checking if satellite 2 is in there too
        satellite_2_result = next(canteen for canteen in body if canteen["id"] == satellite_2.id)
        self.assertEqual(satellite_2_result["siret"], satellite_2.siret)


class TestRelationCentralSatelliteCreateUpdate(APITestCase):
    def test_create_satellite_unauthenticated(self):
        """
        Shouldn't be able to create satellites if not logged in
        """
        canteen = CanteenFactory()
        response = self.client.post(reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_satellite_not_manager(self):
        canteen = CanteenFactory()
        response = self.client.post(reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_get_satellites_not_manager(self):
        canteen = CanteenFactory()
        response = self.client.get(reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen.id}), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @authenticate
    def test_create_satellite(self):
        """
        When the endpoint is called, create new canteens, adding in some additional helpful information
        """
        second_manager = UserFactory()
        central_kitchen = CanteenFactory(
            siret="08376514425566",
            production_type=Canteen.ProductionType.CENTRAL,
            managers=[authenticate.user, second_manager],
        )
        # all the mgmt team of the cuisine centrale should be added to the satellite team
        satellite_siret = "38782537682311"
        request = {
            "name": "Wanderer",
            "siret": satellite_siret,
            "dailyMealCount": 12,
            "yearlyMealCount": 1000,
            "managementType": Canteen.ManagementType.DIRECT,
            "economicModel": Canteen.EconomicModel.PUBLIC,
            "sectorList": [Sector.EDUCATION_PRIMAIRE, Sector.ENTERPRISE_ENTREPRISE],
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        satellite = Canteen.objects.get(siret=satellite_siret)
        self.assertEqual(satellite.name, "Wanderer")
        self.assertEqual(len(satellite.sector_list), 2)
        self.assertEqual(satellite.import_source, "Cuisine centrale : 08376514425566")
        self.assertEqual(satellite.central_producer_siret, central_kitchen.siret)
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
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        existing_canteen = CanteenFactory(
            siret="89834106501485",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen.siret,
        )
        Canteen.objects.filter(id=existing_canteen.id).update(central_producer_siret=None)  # clear the link
        existing_canteen.refresh_from_db()

        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertEqual(existing_canteen.central_producer_siret, central_kitchen.siret)

    @authenticate
    def test_add_existing_site_satellite(self):
        """
        If the added canteen exists already and has a "site" production type,
        it will be updated to "satellite"
        """
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        existing_canteen = CanteenFactory(siret="89834106501485", production_type=Canteen.ProductionType.ON_SITE)

        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertEqual(existing_canteen.production_type, Canteen.ProductionType.ON_SITE_CENTRAL)

    @authenticate
    def test_add_existing_satellite_without_managers(self):
        """
        If the satellite has no managers, the CC managers get access to it
        """
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        existing_canteen = CanteenFactory(
            siret="89834106501485",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen.siret,
        )
        existing_canteen.managers.all().delete()
        Canteen.objects.filter(id=existing_canteen.id).update(central_producer_siret=None)  # clear the link
        existing_canteen.refresh_from_db()

        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertIn(authenticate.user, existing_canteen.managers.all())

    @authenticate
    def test_add_existing_satellite_with_managers(self):
        """
        If the satellite already has managers, the CC managers do not get automatic access
        """
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        existing_canteen = CanteenFactory(
            siret="89834106501485",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen.siret,
            managers=[UserFactory()],
        )
        Canteen.objects.filter(id=existing_canteen.id).update(central_producer_siret=None)  # clear the link
        existing_canteen.refresh_from_db()

        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        existing_canteen.refresh_from_db()
        self.assertNotIn(authenticate.user, existing_canteen.managers.all())

    @authenticate
    def test_add_existing_satellite_already_linked(self):
        """
        If the satellite targeted already has a central siret listed, don't change anything
        """
        central_kitchen_1 = CanteenFactory(siret="21822171376603", production_type=Canteen.ProductionType.CENTRAL)
        central_kitchen_2 = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        existing_canteen_satellite = CanteenFactory(
            siret="89834106501485",
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central_kitchen_1.siret,
        )

        request = {
            "name": existing_canteen_satellite.name,
            "siret": existing_canteen_satellite.siret,
            "dailyMealCount": existing_canteen_satellite.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen_2.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "Cette cantine est déjà fourni par une autre cuisine centrale")

        existing_canteen_satellite.refresh_from_db()
        self.assertEqual(existing_canteen_satellite.central_producer_siret, central_kitchen_1.siret)

    @authenticate
    def test_add_central_cuisine_as_satellite(self):
        """
        It should not be possible to add a central cuisine as a satellite of another central cuisine
        """
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        existing_canteen_central = CanteenFactory(
            siret="89834106501485", production_type=Canteen.ProductionType.CENTRAL
        )

        request = {
            "name": existing_canteen_central.name,
            "siret": existing_canteen_central.siret,
            "dailyMealCount": existing_canteen_central.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "La cantine renseignée est une cuisine centrale")

        existing_canteen_central.refresh_from_db()
        self.assertIsNone(existing_canteen_central.central_producer_siret)

    @authenticate
    def test_add_satellites_to_non_central(self):
        """
        It should not be possible to add a satellites to canteens that are not central cuisines
        """
        canteen_not_central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.ON_SITE, managers=[authenticate.user]
        )
        existing_canteen = CanteenFactory(siret="89834106501485", production_type=Canteen.ProductionType.ON_SITE)

        request = {
            "name": existing_canteen.name,
            "siret": existing_canteen.siret,
            "dailyMealCount": existing_canteen.daily_meal_count,
        }
        response = self.client.post(
            reverse("list_create_update_satellite", kwargs={"canteen_pk": canteen_not_central_kitchen.id}), request
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        existing_canteen.refresh_from_db()
        self.assertIsNone(existing_canteen.central_producer_siret)


class TestRelationCentralSatelliteUnlink(APITestCase):
    def test_remove_added_satellite_unauthenticated(self):
        """
        Shouldn't be able to remove satellites if not logged in
        """
        central_kitchen = CanteenFactory(siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(
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
        central_kitchen = CanteenFactory(siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(
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
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
        satellite = CanteenFactory(
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
        central_kitchen = CanteenFactory(
            siret="08376514425566", production_type=Canteen.ProductionType.CENTRAL, managers=[authenticate.user]
        )
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
