import datetime
import os
from datetime import date

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory
from data.models import Canteen
from data.region_choices import Region

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestPublicCanteenPreviewsApi(APITestCase):
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

    # TODO: test satellites: CC APPRO, CC ALL, own diag


class TestPublicCanteenSearchApi(APITestCase):
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
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        social = SectorFactory.create(name="Social")
        CanteenFactory(sectors=[school], name="Shiso")
        CanteenFactory(sectors=[enterprise], name="Wasabi")
        CanteenFactory(sectors=[social], name="Mochi")
        CanteenFactory(sectors=[school, social], name="Umami")

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
        CanteenFactory.create(
            daily_meal_count=None,
            name="Shiso",
            creation_date=(timezone.now() - datetime.timedelta(days=10)),
        )
        CanteenFactory.create(
            daily_meal_count=0,
            name="Wasabi",
            creation_date=(timezone.now() - datetime.timedelta(days=8)),
        )
        CanteenFactory.create(
            daily_meal_count=1,
            name="Mochi",
            creation_date=(timezone.now() - datetime.timedelta(days=6)),
        )
        CanteenFactory.create(
            daily_meal_count=2,
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
        good_canteen_empty_siret = CanteenFactory.create(
            name="Cantine avec bilan mais siret vide",
            siret="",
        )
        good_canteen_siret_none = CanteenFactory.create(name="Cantine avec bilan mais siret null", siret=None)
        CanteenFactory.create(
            name="Cantine sans bilan avec siret cuisine centrale vide",
            siret="12345678937462",
            central_producer_siret="",
        )
        CanteenFactory.create(
            name="Cantine sans bilan avec siret cuisine centrale null",
            siret="12345678937463",
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
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        administration = SectorFactory.create(name="Administration")
        # unused sectors shouldn't show up as an option
        SectorFactory.create(name="Unused")
        CanteenFactory(sectors=[school, enterprise], name="Shiso")
        CanteenFactory(sectors=[school], name="Wasabi")
        CanteenFactory(sectors=[school], name="Mochi")
        CanteenFactory(sectors=[administration], name="Umami")

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
        school = SectorFactory.create(name="School")
        enterprise = SectorFactory.create(name="Enterprise")
        administration = SectorFactory.create(name="Administration")
        # unused sectors shouldn't show up as an option
        unused = SectorFactory.create(name="Unused")
        CanteenFactory.create(line_ministry=None, sectors=[school, enterprise], name="Shiso")
        CanteenFactory.create(line_ministry=None, sectors=[school, administration], name="Umami")

        CanteenFactory.create(line_ministry=Canteen.Ministries.ARMEE, sectors=[unused], name="Secret")

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
        CanteenFactory(management_type=None, name="Wasabi")

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
