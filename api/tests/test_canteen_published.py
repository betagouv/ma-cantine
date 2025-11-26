import datetime
import os
from datetime import date

from django.core.files import File
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.utils import authenticate
from data.factories import CanteenFactory, DiagnosticFactory, SectorM2MFactory, TeledeclarationFactory, UserFactory
from data.models import Canteen, CanteenImage, Diagnostic, Teledeclaration, Sector
from data.models.geo import Region

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class CanteenPublishedListApiTest(APITestCase):
    def test_get_published_canteens(self):
        """
        All canteens except with line ministry ARMEE should be public
        """
        published_canteens = [
            CanteenFactory(line_ministry=Canteen.Ministries.AFFAIRES_ETRANGERES),
            CanteenFactory(line_ministry=None),
            CanteenFactory(line_ministry=Canteen.Ministries.AGRICULTURE),
        ]
        private_canteens = [
            CanteenFactory(line_ministry=Canteen.Ministries.ARMEE),
            CanteenFactory(line_ministry=Canteen.Ministries.ARMEE),
        ]
        response = self.client.get(reverse("published_canteens"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("count"), 3)

        results = body.get("results", [])

        for published_canteen in published_canteens:
            self.assertTrue(any(x["id"] == published_canteen.id for x in results))

        for private_canteen in private_canteens:
            self.assertFalse(any(x["id"] == private_canteen.id for x in results))

        for received_canteen in results:
            self.assertFalse("managers" in received_canteen)
            self.assertFalse("managerInvitations" in received_canteen)


class CanteenPublishedListFilterApiTest(APITestCase):
    def test_search_single_result(self):
        CanteenFactory(name="Shiso")
        CanteenFactory(name="Wasabi")
        CanteenFactory(name="Mochi")
        CanteenFactory(name="Umami")

        search_term = "mochi"
        response = self.client.get(f"{reverse('published_canteens')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Mochi")

    def test_search_accented_result(self):
        CanteenFactory(name="Wakamé")
        CanteenFactory(name="Shiitaké")

        search_term = "wakame"
        response = self.client.get(f"{reverse('published_canteens')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Wakamé")

    def test_search_multiple_results(self):
        CanteenFactory(name="Sudachi")
        CanteenFactory(name="Wasabi")
        CanteenFactory(name="Mochi")
        CanteenFactory(name="Umami")

        search_term = "chi"
        response = self.client.get(f"{reverse('published_canteens')}?search={search_term}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results", [])

        self.assertEqual(len(results), 2)

        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Mochi", result_names)
        self.assertIn("Sudachi", result_names)

    def test_meal_count_filter(self):
        CanteenFactory(daily_meal_count=10, name="Shiso")
        CanteenFactory(daily_meal_count=15, name="Wasabi")
        CanteenFactory(daily_meal_count=20, name="Mochi")
        CanteenFactory(daily_meal_count=25, name="Umami")

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
        CanteenFactory(department="69", name="Shiso")
        CanteenFactory(department="10", name="Wasabi")
        CanteenFactory(department="75", name="Mochi")
        CanteenFactory(department="31", name="Umami")

        url = f"{reverse('published_canteens')}?department=69"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Shiso")

    def test_sectors_filter(self):
        CanteenFactory(sector_list=[Sector.EDUCATION_PRIMAIRE], name="Shiso")
        CanteenFactory(sector_list=[Sector.ENTERPRISE_ENTREPRISE], name="Wasabi")
        CanteenFactory(sector_list=[Sector.SOCIAL_AUTRE], name="Mochi")
        CanteenFactory(sector_list=[Sector.EDUCATION_PRIMAIRE, Sector.SOCIAL_AUTRE], name="Umami")

        url = f"{reverse('published_canteens')}?sector={Sector.EDUCATION_PRIMAIRE}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 2)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Umami", result_names)

        url = f"{reverse('published_canteens')}?sector={Sector.ENTERPRISE_ENTREPRISE}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Wasabi")

        url = f"{reverse('published_canteens')}?sector={Sector.ENTERPRISE_ENTREPRISE}&sector={Sector.SOCIAL_AUTRE}"
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
            daily_meal_count=200,
            name="Shiso",
            creation_date=(timezone.now() - datetime.timedelta(days=10)),
        )
        CanteenFactory.create(
            daily_meal_count=100,
            name="Wasabi",
            creation_date=(timezone.now() - datetime.timedelta(days=8)),
        )
        last_modified = CanteenFactory.create(
            daily_meal_count=300,
            name="Mochi",
            creation_date=(timezone.now() - datetime.timedelta(days=6)),
        )
        CanteenFactory.create(
            daily_meal_count=150,
            name="Umami",
            creation_date=(timezone.now() - datetime.timedelta(days=4)),
        )

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

        last_modified.daily_meal_count = 900
        last_modified.save()

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

    def test_order_meal_count(self):
        """
        In meal count, "null" values should be placed first
        """
        canteen_daily_meal_count_none = CanteenFactory.create(
            name="Shiso",
            creation_date=(timezone.now() - datetime.timedelta(days=10)),
        )
        Canteen.objects.filter(id=canteen_daily_meal_count_none.id).update(daily_meal_count=None)
        canteen_daily_meal_count_0 = CanteenFactory.create(
            name="Wasabi",
            creation_date=(timezone.now() - datetime.timedelta(days=8)),
        )
        Canteen.objects.filter(id=canteen_daily_meal_count_0.id).update(daily_meal_count=0)
        CanteenFactory.create(
            daily_meal_count=3,
            name="Mochi",
            creation_date=(timezone.now() - datetime.timedelta(days=6)),
        )
        CanteenFactory.create(
            daily_meal_count=4,
            name="Umami",
            creation_date=(timezone.now() - datetime.timedelta(days=4)),
        )

        url = f"{reverse('published_canteens')}?ordering=daily_meal_count"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Shiso")
        self.assertEqual(results[1]["name"], "Wasabi")
        self.assertEqual(results[2]["name"], "Mochi")
        self.assertEqual(results[3]["name"], "Umami")

        url = f"{reverse('published_canteens')}?ordering=-daily_meal_count"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["name"], "Umami")
        self.assertEqual(results[1]["name"], "Mochi")
        self.assertEqual(results[2]["name"], "Wasabi")
        self.assertEqual(results[3]["name"], "Shiso")

    def test_filter_appro_values(self):
        """
        Should be able to filter by bio %, sustainable %, combined % based on last year's diagnostic
        and based on the rules for their region
        """
        good_canteen = CanteenFactory.create(name="Shiso", region=Region.auvergne_rhone_alpes)
        central = CanteenFactory.create(
            name="Central",
            region=Region.auvergne_rhone_alpes,
            production_type=Canteen.ProductionType.CENTRAL,
            siret="22730656663081",
        )
        CanteenFactory.create(
            name="Satellite",
            region=Region.auvergne_rhone_alpes,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret="22730656663081",
        )
        medium_canteen = CanteenFactory.create(name="Wasabi", region=Region.auvergne_rhone_alpes)
        sustainable_canteen = CanteenFactory.create(name="Umami", region=Region.auvergne_rhone_alpes)
        bad_canteen = CanteenFactory.create(name="Mochi", region=Region.auvergne_rhone_alpes)
        secretly_good_canteen = CanteenFactory.create(name="Secret", region=Region.auvergne_rhone_alpes)
        guadeloupe_canteen = CanteenFactory.create(region=Region.guadeloupe, name="Guadeloupe")
        good_canteen_with_siren = CanteenFactory.create(
            name="Siren",
            region=Region.auvergne_rhone_alpes,
            siret="",
            siren_unite_legale="123456789",
        )
        good_canteen_empty_siret = CanteenFactory.create(name="Cantine avec bilan mais siret vide")
        Canteen.objects.filter(id=good_canteen_empty_siret.id).update(siret="")
        good_canteen_empty_siret.refresh_from_db()
        good_canteen_siret_none = CanteenFactory.create(name="Cantine avec bilan mais siret null")
        Canteen.objects.filter(id=good_canteen_siret_none.id).update(siret=None)
        good_canteen_siret_none.refresh_from_db()
        CanteenFactory.create(
            name="Cantine sans bilan avec siret cuisine centrale vide",
            siret="21730065600014",
            central_producer_siret="",
        )
        CanteenFactory.create(
            name="Cantine sans bilan avec siret cuisine centrale null",
            siret="21380185500015",
            central_producer_siret=None,
        )

        publication_year = date.today().year - 1

        DiagnosticFactory.create(
            canteen=good_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=10,
            value_externality_performance_ht=10,
            value_egalim_others_ht=10,
        )
        DiagnosticFactory.create(
            canteen=central,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=10,
            value_externality_performance_ht=10,
            value_egalim_others_ht=10,
        )
        DiagnosticFactory.create(
            canteen=secretly_good_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=30,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
        )
        DiagnosticFactory.create(
            canteen=medium_canteen,
            year=publication_year,
            value_total_ht=1000,
            value_bio_ht=150,
            value_sustainable_ht=350,
            value_externality_performance_ht=None,
            value_egalim_others_ht=None,
        )
        DiagnosticFactory.create(
            canteen=sustainable_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=None,
            value_sustainable_ht=None,
            value_externality_performance_ht=40,
            value_egalim_others_ht=20,
        )
        DiagnosticFactory.create(
            canteen=bad_canteen,
            year=2019,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=30,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
        )
        DiagnosticFactory.create(
            canteen=bad_canteen,
            year=publication_year,
            value_total_ht=10,
            value_bio_ht=0,
            value_sustainable_ht=0,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
        )
        DiagnosticFactory.create(
            canteen=guadeloupe_canteen,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=5,
            value_sustainable_ht=15,
            value_externality_performance_ht=None,
            value_egalim_others_ht=0,
        )
        DiagnosticFactory.create(
            canteen=good_canteen_with_siren,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=30,
            value_sustainable_ht=10,
            value_externality_performance_ht=10,
            value_egalim_others_ht=10,
        )
        DiagnosticFactory.create(
            canteen=good_canteen_empty_siret,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=1,
            value_sustainable_ht=0,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
        )
        DiagnosticFactory.create(
            canteen=good_canteen_siret_none,
            year=publication_year,
            value_total_ht=100,
            value_bio_ht=1,
            value_sustainable_ht=0,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
        )

        self.assertEqual(Canteen.objects.count(), 13)

        url = f"{reverse('published_canteens')}?min_portion_bio={0.2}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 5)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Satellite", result_names)
        self.assertIn("Siren", result_names)

        url = f"{reverse('published_canteens')}?min_portion_combined={0.5}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 7)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Satellite", result_names)
        self.assertIn("Siren", result_names)
        self.assertIn("Wasabi", result_names)
        self.assertIn("Umami", result_names)

        url = f"{reverse('published_canteens')}?min_portion_bio={0.1}&min_portion_combined={0.5}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 6)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Satellite", result_names)
        self.assertIn("Siren", result_names)
        self.assertIn("Wasabi", result_names)

        url = f"{reverse('published_canteens')}?badge=appro"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 6)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Satellite", result_names)
        self.assertIn("Siren", result_names)
        self.assertIn("Guadeloupe", result_names)

        # if both badge and thresholds specified, return the results that match the most strict threshold
        url = f"{reverse('published_canteens')}?badge=appro&min_portion_combined={0.01}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 6)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Satellite", result_names)
        self.assertIn("Siren", result_names)
        self.assertIn("Guadeloupe", result_names)

        url = f"{reverse('published_canteens')}?badge=appro&min_portion_combined={0.5}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 5)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Shiso", result_names)
        self.assertIn("Satellite", result_names)
        self.assertIn("Siren", result_names)

        url = f"{reverse('published_canteens')}?min_portion_bio={0.001}"
        response = self.client.get(url)
        results = response.json().get("results", [])
        self.assertEqual(len(results), 9)
        result_names = list(map(lambda x: x.get("name"), results))
        self.assertIn("Cantine avec bilan mais siret vide", result_names)
        self.assertIn("Cantine avec bilan mais siret null", result_names)
        self.assertNotIn("Cantine sans bilan avec siret cuisine centrale vide", result_names)
        self.assertNotIn("Cantine sans bilan avec siret cuisine centrale null", result_names)

    def test_pagination_departments(self):
        CanteenFactory(department="75", name="Shiso")
        CanteenFactory(department="75", name="Wasabi")
        CanteenFactory(department="69", name="Mochi")
        CanteenFactory(department=None, name="Umami")

        url = f"{reverse('published_canteens')}"
        response = self.client.get(url)
        body = response.json()

        # There are two unique departments : 75 and 69
        self.assertEqual(len(body.get("departments")), 2)
        self.assertIn("75", body.get("departments"))
        self.assertIn("69", body.get("departments"))

    def test_deprecated_pagination_sectors(self):
        """
        The pagination endpoint should return all sectors that are used by canteens, even when the data is filtered by another sector
        """
        school = SectorM2MFactory.create(name="School")
        enterprise = SectorM2MFactory.create(name="Enterprise")
        administration = SectorM2MFactory.create(name="Administration")
        # unused sectors shouldn't show up as an option
        SectorM2MFactory.create(name="Unused")
        CanteenFactory(sectors_m2m=[school, enterprise], name="Shiso")
        CanteenFactory(sectors_m2m=[school], name="Wasabi")
        CanteenFactory(sectors_m2m=[school], name="Mochi")
        CanteenFactory(sectors_m2m=[administration], name="Umami")

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

    def test_pagination_sectors(self):
        """
        The pagination endpoint should return all sectors that are used by canteens, even when the data is filtered by another sector
        It should not return sectors from hidden canteens
        """
        school = SectorM2MFactory.create(name="School")
        enterprise = SectorM2MFactory.create(name="Enterprise")
        administration = SectorM2MFactory.create(name="Administration")
        # unused sectors shouldn't show up as an option
        unused = SectorM2MFactory.create(name="Unused")
        CanteenFactory.create(line_ministry=None, sectors_m2m=[school, enterprise], name="Shiso")
        CanteenFactory.create(line_ministry=None, sectors_m2m=[school, administration], name="Umami")

        CanteenFactory.create(line_ministry=Canteen.Ministries.ARMEE, sectors_m2m=[unused], name="Secret")

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
        CanteenFactory(management_type="conceded", name="Shiso")
        CanteenFactory(management_type="conceded", name="Wasabi")

        url = f"{reverse('published_canteens')}"
        response = self.client.get(url)
        body = response.json()

        self.assertEqual(len(body.get("managementTypes")), 1)
        self.assertIn("conceded", body.get("managementTypes"))

    def test_get_canteens_filter_production_type(self):
        site_canteen = CanteenFactory(production_type="site")
        central_cuisine = CanteenFactory(production_type="central")
        central_serving_cuisine = CanteenFactory.create(production_type="central_serving")

        response = self.client.get(f"{reverse('published_canteens')}?production_type=central,central_serving")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()

        self.assertEqual(body["count"], 2)
        ids = list(map(lambda x: x["id"], body["results"]))
        self.assertIn(central_cuisine.id, ids)
        self.assertIn(central_serving_cuisine.id, ids)
        self.assertNotIn(site_canteen.id, ids)


class PublishedCanteenDetailApiTest(APITestCase):
    def test_get_single_published_canteen(self):
        """
        We are able to get a single published canteen.
        """
        published_canteen = CanteenFactory()
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": published_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body.get("id"), published_canteen.id)
        self.assertIn("badges", body)

    def test_get_single_unpublished_canteen(self):
        """
        A 404 is raised if we try to get a single published canteen
        that has not been published by the manager.
        """
        private_canteen = CanteenFactory(line_ministry=Canteen.Ministries.ARMEE)
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": private_canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @authenticate
    def test_canteen_image_serialization(self):
        """
        A canteen with images should serialize those images
        """
        canteen = CanteenFactory()
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

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(len(body.get("images")), 3)

    def test_satellite_published(self):
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        diagnostic = DiagnosticFactory(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(body.get("id"), satellite.id)
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        self.assertEqual(body.get("centralKitchen").get("id"), central_kitchen.id)

        serialized_diagnostic = body.get("approDiagnostics")[0]
        self.assertEqual(serialized_diagnostic["id"], diagnostic.id)
        self.assertEqual(serialized_diagnostic["percentageValueTotalHt"], 1)
        self.assertEqual(serialized_diagnostic["percentageValueBioHt"], 0.5)

    def test_satellite_published_without_bio(self):
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        diagnostic = DiagnosticFactory(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=None,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(body.get("id"), satellite.id)
        self.assertEqual(len(body.get("approDiagnostics")), 1)

        serialized_diagnostic = body.get("approDiagnostics")[0]
        self.assertEqual(serialized_diagnostic["id"], diagnostic.id)
        self.assertEqual(serialized_diagnostic["percentageValueTotalHt"], 1)
        self.assertNotIn("percentageValueBioHt", serialized_diagnostic)

    def test_satellite_published_no_type(self):
        """
        Central cuisine diagnostics should only be returned if their central_kitchen_diagnostic_mode
        is set. Otherwise it may be an old diagnostic that is not meant for the satellites
        """
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=None,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(body.get("id"), satellite.id)
        self.assertEqual(len(body.get("approDiagnostics")), 0)

    def test_satellite_published_needed_fields(self):
        """
        If the central kitchen diag is set to APPRO, only the appro fields should be included.
        If the central kitchen diag is set to ALL, every fields should be included.
        """
        central_siret = "22730656663081"
        central_kitchen = CanteenFactory.create(siret=central_siret, production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            central_producer_siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2020,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO,
        )

        DiagnosticFactory.create(
            canteen=central_kitchen,
            year=2021,
            value_total_ht=1200,
            value_bio_ht=600,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL,
            value_fish_ht=100,
            value_fish_egalim_ht=80,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(body.get("approDiagnostics")), 2)
        self.assertEqual(len(body.get("serviceDiagnostics")), 1)
        appro_diagnostics = body.get("approDiagnostics")
        appro_diag_2020 = next(filter(lambda x: x["year"] == 2020, appro_diagnostics))
        appro_diag_2021 = next(filter(lambda x: x["year"] == 2021, appro_diagnostics))
        service_diag_2021 = body.get("serviceDiagnostics")[0]

        self.assertIn("percentageValueTotalHt", appro_diag_2020)
        self.assertNotIn("hasWasteDiagnostic", appro_diag_2020)

        self.assertIn("percentageValueTotalHt", appro_diag_2021)
        self.assertIn("hasWasteDiagnostic", service_diag_2021)
        self.assertNotIn("valueFishEgalimHt", appro_diag_2021)
        self.assertIn("percentageValueFishEgalimHt", appro_diag_2021)

    def test_percentage_values(self):
        """
        The published endpoint should not contain the real economic data, only percentages.
        """
        canteen = CanteenFactory.create(production_type=Canteen.ProductionType.ON_SITE)

        DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            value_total_ht=1200,
            value_bio_ht=600,
            value_sustainable_ht=300,
            value_meat_poultry_ht=200,
            value_meat_poultry_egalim_ht=100,
            value_fish_ht=10,
            value_fish_egalim_ht=8,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(body.get("approDiagnostics")), 1)
        serialized_diag = body.get("approDiagnostics")[0]

        self.assertEqual(serialized_diag["percentageValueTotalHt"], 1)
        self.assertEqual(serialized_diag["percentageValueBioHt"], 0.5)
        self.assertEqual(serialized_diag["percentageValueSustainableHt"], 0.25)
        # the following is a percentage of the meat total, not global total
        self.assertEqual(serialized_diag["percentageValueMeatPoultryEgalimHt"], 0.5)
        self.assertEqual(serialized_diag["percentageValueFishEgalimHt"], 0.8)
        # ensure the raw values are not included in the diagnostic
        self.assertNotIn("valueTotalHt", serialized_diag)
        self.assertNotIn("valueBioHt", serialized_diag)
        self.assertNotIn("valueMeatPoultryHt", serialized_diag)
        self.assertNotIn("valueMeatPoultryEgalimHt", serialized_diag)
        self.assertNotIn("valueFishHt", serialized_diag)
        self.assertNotIn("valueFishEgalimHt", serialized_diag)

    def test_remove_raw_values_when_missing_totals(self):
        """
        The published endpoint should not contain the real economic data, only percentages.
        Even when the meat and fish totals are absent, but EGalim and France totals are present.
        """
        central_siret = "22730656663081"
        canteen = CanteenFactory.create(
            siret=central_siret,
            production_type=Canteen.ProductionType.ON_SITE,
        )

        DiagnosticFactory.create(
            canteen=canteen,
            year=2021,
            value_meat_poultry_ht=None,
            value_meat_poultry_egalim_ht=100,
            value_meat_poultry_france_ht=100,
            value_fish_ht=None,
            value_fish_egalim_ht=100,
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()

        serialized_diag = body.get("approDiagnostics")[0]

        self.assertNotIn("valueMeatPoultryEgalimHt", serialized_diag)
        self.assertNotIn("valueMeatPoultryFranceHt", serialized_diag)
        self.assertNotIn("valueFishEgalimHt", serialized_diag)

    def test_return_published_diagnostics(self):
        """
        The published endpoint returns all diagnostic "service" data in one property,
        and the appro data in another. The latter should be filtered on the redacted years.
        """
        canteen = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE,
            redacted_appro_years=[2020, 2021, 2023],
        )

        DiagnosticFactory.create(canteen=canteen, year=2021)
        published_appro_diag = DiagnosticFactory.create(canteen=canteen, year=2022)
        DiagnosticFactory.create(canteen=canteen, year=2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(body.get("serviceDiagnostics")), 3)
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        serialized_diags = body.get("serviceDiagnostics")
        serialized_appro_diags = body.get("approDiagnostics")

        for diag in serialized_diags:
            self.assertNotIn("percentageValueTotalHt", diag)
            self.assertNotIn("valueTotalHt", diag)

        self.assertEqual(serialized_appro_diags[0]["id"], published_appro_diag.id)
        self.assertIn("percentageValueTotalHt", serialized_appro_diags[0])
        self.assertNotIn("valueTotalHt", serialized_appro_diags[0])

    def test_satellites_can_redact_cc_appro_data(self):
        """
        Satellites should be able to redact the appro data provided by a CC, regardless of diagostic mode,
        without impacting other satellites or the CC
        """
        central = CanteenFactory.create(
            siret="96766910375238", production_type=Canteen.ProductionType.CENTRAL, redacted_appro_years=[]
        )
        fully_redacted_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            redacted_appro_years=[2022, 2023],
        )
        partially_redacted_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            redacted_appro_years=[2022],
        )
        other_satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            redacted_appro_years=[],
        )

        DiagnosticFactory.create(
            canteen=central, year=2022, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.ALL
        )
        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        self.assertEqual(fully_redacted_satellite.central_kitchen_diagnostics.count(), 2)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": fully_redacted_satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 0)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": partially_redacted_satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        self.assertEqual(body.get("approDiagnostics")[0]["year"], 2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": other_satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 2)

    def test_cc_can_redact_appro_data(self):
        """
        CCs should be able to redact the appro data without impacting their satellites
        """
        central = CanteenFactory.create(
            siret="96766910375238",
            production_type=Canteen.ProductionType.CENTRAL,
            redacted_appro_years=[2023],
        )
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            redacted_appro_years=[],
        )

        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": central.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 0)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 1)

    def test_satellites_get_correct_appro_diagnostic(self):
        """
        Satellites that have their own diagnostic for one year, and CC diagnostics for another,
        should receive the CC diagnostic where it exists
        """
        central = CanteenFactory.create(siret="96766910375238", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
        )

        DiagnosticFactory.create(canteen=satellite, year=2021)
        DiagnosticFactory.create(
            canteen=central, year=2022, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        DiagnosticFactory.create(canteen=satellite, year=2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        serialized_diagnostics = body.get("approDiagnostics")
        self.assertEqual(len(serialized_diagnostics), 3)
        for diagnostic in serialized_diagnostics:
            if diagnostic["year"] == 2021:
                self.assertEqual(
                    diagnostic["canteenId"], satellite.id, "return satellite diagnostic when only diag for year"
                )
            elif diagnostic["year"] == 2022:
                self.assertEqual(diagnostic["canteenId"], central.id, "return CC diagnostic when only diag for year")
            elif diagnostic["year"] == 2023:
                self.assertEqual(
                    diagnostic["canteenId"], central.id, "priority to central diagnostic where there are both"
                )

    def test_satellites_can_redact_own_appro_data(self):
        """
        Satellites that have their own diagnostic should be able to redact their appro data
        without their CC's diagnostic appro data taking it's place
        """
        central = CanteenFactory.create(siret="96766910375238", production_type=Canteen.ProductionType.CENTRAL)
        satellite = CanteenFactory.create(
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            central_producer_siret=central.siret,
            redacted_appro_years=[2023],
        )

        DiagnosticFactory.create(
            canteen=central, year=2023, central_kitchen_diagnostic_mode=Diagnostic.CentralKitchenDiagnosticMode.APPRO
        )
        DiagnosticFactory.create(canteen=satellite, year=2023)

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": satellite.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 0)

    def test_td_diags_not_redacted(self):
        """
        A teledeclared diagnostic cannot be redacted
        """
        canteen = CanteenFactory.create(redacted_appro_years=[2022, 2023])

        DiagnosticFactory.create(canteen=canteen, year=2022)
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2023, status=Diagnostic.DiagnosticStatus.SUBMITTED)
        TeledeclarationFactory.create(
            diagnostic=diagnostic, status=Teledeclaration.TeledeclarationStatus.SUBMITTED, declared_data={"foo": "bar"}
        )

        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertEqual(len(body.get("approDiagnostics")), 1)
        self.assertEqual(len(body.get("serviceDiagnostics")), 2)


class TestPublishedCanteenClaimApiTest(APITestCase):
    def test_canteen_claim_value(self):
        canteen = CanteenFactory()

        # The factory creates canteens with managers
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertFalse(body.get("canBeClaimed"))

        # Now we will remove the manager to change the claim API value
        canteen.managers.clear()
        response = self.client.get(reverse("single_published_canteen", kwargs={"pk": canteen.id}))
        body = response.json()
        self.assertTrue(body.get("canBeClaimed"))

    @authenticate
    def test_canteen_claim_request(self):
        canteen = CanteenFactory()
        canteen.managers.clear()

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertEqual(body["name"], canteen.name)
        user = authenticate.user
        self.assertEqual(canteen.managers.first().id, user.id)
        self.assertEqual(canteen.managers.count(), 1)
        canteen.refresh_from_db()
        self.assertEqual(canteen.claimed_by, user)
        self.assertTrue(canteen.has_been_claimed)

    @authenticate
    def test_canteen_claim_request_fails_when_already_claimed(self):
        canteen = CanteenFactory()
        self.assertGreater(canteen.managers.count(), 0)
        user = authenticate.user
        self.assertFalse(canteen.managers.filter(id=user.id).exists())

        response = self.client.post(reverse("claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(canteen.managers.filter(id=user.id).exists())
        canteen.refresh_from_db()
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_undo_claim_canteen(self):
        canteen = CanteenFactory.create(
            claimed_by=authenticate.user, has_been_claimed=True, managers=[authenticate.user]
        )

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertIsNone(canteen.claimed_by)
        self.assertFalse(canteen.has_been_claimed)

    @authenticate
    def test_undo_claim_canteen_fails_if_not_original_claimer(self):
        other_user = UserFactory.create()
        canteen = CanteenFactory.create(claimed_by=other_user, has_been_claimed=True, managers=[authenticate.user])

        response = self.client.post(reverse("undo_claim_canteen", kwargs={"canteen_pk": canteen.id}), None)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(canteen.managers.filter(id=authenticate.user.id).exists())
        canteen.refresh_from_db()
        self.assertTrue(canteen.has_been_claimed)
        self.assertEqual(canteen.claimed_by, other_user)


class CanteenPreviewDetailApiTest(APITestCase):
    def test_get_single_public_canteen_preview(self):
        """
        Should be able to get the public summary data for a single published canteen
        """
        canteen = CanteenFactory()

        response = self.client.get(reverse("single_public_canteen_preview", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_to_get_non_existant_canteen_preview(self):
        """
        A request for a canteen that does not exist returns a 404
        """
        response = self.client.get(reverse("single_public_canteen_preview", kwargs={"pk": 99}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_receive_expected_keys_in_preview(self):
        """
        Should get summary data in a public preview
        """
        canteen = CanteenFactory()
        DiagnosticFactory(
            canteen=canteen, year=timezone.now().date().year - 1
        )  # year must be in the past, otherwise canteen.appro_diagnostics is empty

        response = self.client.get(reverse("single_public_canteen_preview", kwargs={"pk": canteen.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["id"], canteen.id)
        self.assertIn("badges", body)
        self.assertIn("year", body["badges"])
        self.assertIn("appro", body["badges"])
        self.assertIn("waste", body["badges"])
        self.assertIn("diversification", body["badges"])
        self.assertIn("plastic", body["badges"])
        self.assertIn("info", body["badges"])
        self.assertIn("approDiagnostic", body)
        self.assertIn("percentageValueBioHt", body["approDiagnostic"])
