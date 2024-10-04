import requests_mock
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.views.canteen import badges_for_queryset
from data.department_choices import Department
from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory
from data.models import Canteen, Diagnostic, Sector
from data.region_choices import Region


class TestCanteenStatsApi(APITestCase):
    @override_settings(PUBLISH_BY_DEFAULT=False)
    def test_canteen_statistics(self):
        """
        This public endpoint returns some summary statistics for a region and a location
        """
        # create 5 canteens (3 in region of interest), 1 unpublished
        region = "01"
        year = 2020
        primary_school = SectorFactory.create(name="Primary", category=Sector.Categories.EDUCATION)
        secondary_school = SectorFactory.create(name="Secondary", category=Sector.Categories.EDUCATION)
        enterprise = SectorFactory.create(name="Enterprise", category=Sector.Categories.ENTERPRISE)
        social = SectorFactory.create(name="Social", category=Sector.Categories.SOCIAL)

        published = CanteenFactory.create(
            region=region,
            publication_status=Canteen.PublicationStatus.PUBLISHED.value,
            sectors=[primary_school, enterprise],
        )
        unpublished = CanteenFactory.create(
            region=region,
            publication_status=Canteen.PublicationStatus.DRAFT.value,
            sectors=[primary_school, secondary_school],
        )
        # this canteen will be included in the canteen count, but not the diagnostic count
        # which is used to calculate the measure success percentages
        out_of_date = CanteenFactory.create(
            region=region,
            publication_status=Canteen.PublicationStatus.PUBLISHED.value,
            sectors=[secondary_school],
        )
        other_region = CanteenFactory.create(region="03", sectors=[social])

        # relevant diagnostics
        DiagnosticFactory.create(
            canteen=published,
            year=year,
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=30,
            value_externality_performance_ht=None,
            value_egalim_others_ht=None,
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
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
            has_waste_diagnostic=True,
            waste_actions=["action1", "action2"],
            has_donation_agreement=True,
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
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
            vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.DAILY,
        )
        DiagnosticFactory.create(
            canteen=out_of_date,
            year=2019,
        )
        DiagnosticFactory.create(
            canteen=other_region,
            year=year,
            value_total_ht=100,
            value_bio_ht=100,
            value_sustainable_ht=0,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
            cooking_plastic_substituted=True,
            serving_plastic_substituted=True,
            plastic_bottles_substituted=True,
            plastic_tableware_substituted=True,
            communicates_on_food_quality=True,
        )

        response = self.client.get(reverse("canteen_statistics"), {"region": region, "year": year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        self.assertEqual(body["publishedCanteenCount"], 2)
        self.assertEqual(body["diagnosticsCount"], 2)
        self.assertEqual(body["bioPercent"], 30)
        self.assertEqual(body["sustainablePercent"], 40)
        self.assertEqual(body["approPercent"], 100)
        self.assertEqual(body["wastePercent"], 50)
        self.assertEqual(body["diversificationPercent"], 50)
        self.assertEqual(body["plasticPercent"], 50)
        self.assertEqual(body["infoPercent"], 50)
        sector_categories = body["sectorCategories"]
        self.assertEqual(sector_categories[Sector.Categories.EDUCATION], 3)
        self.assertEqual(sector_categories[Sector.Categories.ENTERPRISE], 1)
        self.assertEqual(sector_categories[Sector.Categories.SOCIAL], 0)

        # can also call without location info
        response = self.client.get(reverse("canteen_statistics"), {"year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(PUBLISH_BY_DEFAULT=True)
    def test_publication_filter_new_rules(self):
        """
        When canteens are published by default, test that the publication count is filtered on ministry
        """
        region = "01"

        CanteenFactory.create(
            region=region,
            publication_status=Canteen.PublicationStatus.DRAFT,
        )
        CanteenFactory.create(
            region=region,
            line_ministry=Canteen.Ministries.ARMEE,
            publication_status=Canteen.PublicationStatus.DRAFT,
        )

        response = self.client.get(reverse("canteen_statistics"), {"region": region, "year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 2)
        self.assertEqual(body["publishedCanteenCount"], 1)

    def test_canteen_stats_by_departments(self):
        department = "01"
        department_2 = "02"
        year = 2020
        CanteenFactory.create(department=department, publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        CanteenFactory.create(department=department_2, publication_status=Canteen.PublicationStatus.PUBLISHED.value)

        response = self.client.get(
            reverse("canteen_statistics"), {"department": [department, department_2], "year": year}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

    def test_canteen_stats_by_sectors(self):
        year = 2020
        school = SectorFactory.create(name="School", category=Sector.Categories.EDUCATION)
        enterprise = SectorFactory.create(name="Enterprise", category=Sector.Categories.ENTERPRISE)
        social = SectorFactory.create(name="Social", category=None)
        CanteenFactory.create(sectors=[school])
        CanteenFactory.create(sectors=[enterprise])
        CanteenFactory.create(sectors=[enterprise, social, school])
        CanteenFactory.create(sectors=[social])

        response = self.client.get(
            reverse("canteen_statistics"), {"sectors": [school.id, enterprise.id], "year": year}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        sector_categories = body["sectorCategories"]
        self.assertEqual(sector_categories[Sector.Categories.EDUCATION], 2)
        self.assertEqual(sector_categories[Sector.Categories.ENTERPRISE], 2)
        self.assertEqual(sector_categories["inconnu"], 1)

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
        zero_total = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        DiagnosticFactory.create(year=2020, canteen=zero_total, value_total_ht=0)
        null_total = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        DiagnosticFactory.create(year=2020, canteen=null_total, value_total_ht=None)
        bio_lacking = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        DiagnosticFactory.create(
            year=2020,
            canteen=bio_lacking,
            value_total_ht=100,
            value_bio_ht=19,
            value_sustainable_ht=31,
            value_externality_performance_ht=None,
            value_egalim_others_ht=None,
        )

        # --- Canteens which earn appro badge:
        null_sustainable = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value, region=Region.ile_de_france.value
        )
        DiagnosticFactory.create(
            year=2020,
            canteen=null_sustainable,
            value_total_ht=100,
            value_bio_ht=50,
            value_sustainable_ht=None,
            value_externality_performance_ht=None,
            value_egalim_others_ht=None,
        )

        earned = CanteenFactory.create(publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        DiagnosticFactory.create(
            year=2020,
            canteen=earned,
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=30,
            value_externality_performance_ht=None,
            value_egalim_others_ht=None,
        )
        # rules per outre mer territories
        guadeloupe = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value, region=Region.guadeloupe.value
        )
        DiagnosticFactory.create(
            year=2020,
            canteen=guadeloupe,
            value_total_ht=100,
            value_bio_ht=5,
            value_sustainable_ht=15,
            value_externality_performance_ht=None,
            value_egalim_others_ht=0,
        )
        # same rules as for Guadeloupe, but Saint-Martin is considered a department, not a region (in reality it's neither)
        saint_martin = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value, department=Department.saint_martin.value
        )
        DiagnosticFactory.create(
            year=2020,
            canteen=saint_martin,
            value_total_ht=100,
            value_bio_ht=5,
            value_sustainable_ht=15,
            value_externality_performance_ht=None,
            value_egalim_others_ht=0,
        )
        mayotte = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value, region=Region.mayotte.value
        )
        DiagnosticFactory.create(
            year=2020,
            canteen=mayotte,
            value_total_ht=100,
            value_bio_ht=2,
            value_sustainable_ht=3,
            value_externality_performance_ht=0,
            value_egalim_others_ht=None,
        )
        saint_pierre_et_miquelon = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value,
            department=Department.saint_pierre_et_miquelon.value,
        )
        DiagnosticFactory.create(
            canteen=saint_pierre_et_miquelon,
            year=2020,
            value_total_ht=100,
            value_bio_ht=10,
            value_sustainable_ht=20,
            value_externality_performance_ht=0,
            value_egalim_others_ht=0,
        )

        badges = badges_for_queryset(Diagnostic.objects.all())

        appro_badge_qs = badges["appro"]
        self.assertTrue(appro_badge_qs.filter(canteen=null_sustainable).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=earned).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=guadeloupe).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=saint_martin).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=mayotte).exists())
        self.assertTrue(appro_badge_qs.filter(canteen=saint_pierre_et_miquelon).exists())
        self.assertEqual(appro_badge_qs.count(), 6)

        response = self.client.get(reverse("canteen_statistics"), {"year": 2020})
        body = response.json()
        # there are 3 canteens that do not meet criteria, and 6 which do = 66.6% meet appro, rounded down
        self.assertEqual(body["approPercent"], 66)

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
        primaire = SectorFactory(name="Scolaire primaire", category="education")
        secondaire = SectorFactory(name="Scolaire secondaire", category="education")

        # --- canteens which don't earn diversification badge:
        high_canteen = CanteenFactory.create()
        high_canteen.sectors.remove(primaire)
        high_canteen.sectors.remove(secondaire)
        DiagnosticFactory.create(
            canteen=high_canteen, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.HIGH.value
        )

        low_canteen = CanteenFactory.create()
        low_canteen.sectors.add(primaire)
        DiagnosticFactory.create(canteen=low_canteen, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.LOW.value)

        # --- canteens which earn diversification badge:
        daily_vege = CanteenFactory.create()
        daily_vege.sectors.remove(primaire)
        daily_vege.sectors.remove(secondaire)
        DiagnosticFactory.create(canteen=daily_vege, vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.DAILY.value)

        scolaire_mid_vege = CanteenFactory.create()
        scolaire_mid_vege.sectors.add(secondaire)
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

    def test_stats_simple_diagnostic(self):
        """
        The endpoint must take into consideration the simplified diagnostic
        fields for EGAlim stats
        """
        year = 2021

        published = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value,
        )

        # Diagnostic that should display 20% Bio and 45% other EGAlim
        DiagnosticFactory.create(
            canteen=published,
            year=year,
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=15,
            value_externality_performance_ht=15,
            value_egalim_others_ht=15,
        )

        response = self.client.get(reverse("canteen_statistics"), {"year": year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["bioPercent"], 20)
        self.assertEqual(body["sustainablePercent"], 45)

    @requests_mock.Mocker()
    def test_epci(self, mock):
        """
        Test that can get canteens with cities that are in EPCIs requested
        """
        # test multiple cities for 1 epci
        CanteenFactory.create(city_insee_code="12345", publication_status=Canteen.PublicationStatus.PUBLISHED)
        CanteenFactory.create(city_insee_code="67890", publication_status=Canteen.PublicationStatus.PUBLISHED)
        # 'belongs to' epci 2
        CanteenFactory.create(city_insee_code="11223", publication_status=Canteen.PublicationStatus.PUBLISHED)
        CanteenFactory.create(city_insee_code="11224", publication_status=Canteen.PublicationStatus.PUBLISHED)
        # shouldn't be included
        CanteenFactory.create(city_insee_code="00000", publication_status=Canteen.PublicationStatus.PUBLISHED)
        epcis = ["1", "2"]
        # mock the API response for these two 'EPCI's
        api_url = "https://geo.api.gouv.fr/epcis"
        mock.get(api_url + "/1/communes", json=[{"code": "12345"}, {"code": "67890"}])
        mock.get(api_url + "/2/communes", json=[{"code": "11223"}, {"code": "11224"}])

        response = self.client.get(reverse("canteen_statistics"), {"year": 2021, "epci": epcis})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 4)

    @requests_mock.Mocker()
    def test_epci_error(self, mock):
        """
        Test that can get canteens with postcodes that are in EPCIs requested
        """
        # test multiple postcodes for 1 epci
        CanteenFactory.create(postal_code="12345", publication_status=Canteen.PublicationStatus.PUBLISHED)
        CanteenFactory.create(postal_code="67890", publication_status=Canteen.PublicationStatus.PUBLISHED)
        # 'belongs to' epci 2
        CanteenFactory.create(postal_code="11223", publication_status=Canteen.PublicationStatus.PUBLISHED)
        CanteenFactory.create(postal_code="11224", publication_status=Canteen.PublicationStatus.PUBLISHED)
        # ends up being included because filter will fail
        CanteenFactory.create(postal_code="00000", publication_status=Canteen.PublicationStatus.PUBLISHED)
        epcis = ["1", "2"]
        # mock the API response for these two 'EPCI's
        api_url = "https://geo.api.gouv.fr/epcis"
        mock.get(api_url + "/1/communes", json=[{"codesPostaux": ["12345", "67890"]}])
        mock.get(api_url + "/2/communes", status_code=500)

        response = self.client.get(reverse("canteen_statistics"), {"year": 2021, "epci": epcis})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 5)
        self.assertEqual(body["epciError"], "Une erreur est survenue")

    @override_settings(PUBLISH_BY_DEFAULT=True)
    def test_published_canteen_count(self):
        """
        The summary published canteen count should be the sum of all canteens not with ARMEE
        """
        CanteenFactory.create(
            line_ministry=Canteen.Ministries.AGRICULTURE,
            publication_status=Canteen.PublicationStatus.DRAFT,
        )
        CanteenFactory.create(line_ministry=None)
        CanteenFactory.create(
            line_ministry=Canteen.Ministries.ARMEE,
            publication_status=Canteen.PublicationStatus.PUBLISHED,
        )

        response = self.client.get(reverse("canteen_statistics"), {"year": 2024})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        self.assertEqual(body["publishedCanteenCount"], 2)
