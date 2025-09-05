from django.core.cache import cache
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from common.cache.utils import CACHE_GET_QUERY_COUNT, CACHE_SET_QUERY_COUNT
from data.department_choices import Department
from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector
from data.region_choices import Region

year_data = 2023
date_in_2023_teledeclaration_campaign = "2024-04-01"  # during the 2023 campaign
STATS_ENDPOINT_QUERY_COUNT = 8


class TestCanteenStatsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector_education_primary = SectorFactory(name="Primary", category=Sector.Categories.EDUCATION)
        cls.sector_education_secondary = SectorFactory(name="Secondary", category=Sector.Categories.EDUCATION)
        cls.sector_enterprise = SectorFactory(name="Enterprise", category=Sector.Categories.ENTERPRISE)
        cls.sector_social = SectorFactory(name="Social", category=Sector.Categories.SOCIAL)
        cls.sector_other = SectorFactory(name="Other", category=None)
        with freeze_time(date_in_2023_teledeclaration_campaign):
            canteen_1 = CanteenFactory(
                siret="21010034300016",
                city_insee_code="01034",
                epci="1",
                pat_list=["1"],
                department="01",
                region="84",
                sectors=[cls.sector_education_primary],
                management_type=Canteen.ManagementType.DIRECT,
                production_type=Canteen.ProductionType.CENTRAL,
                economic_model=Canteen.EconomicModel.PUBLIC,
            )
            canteen_diagnostic_1 = DiagnosticFactory(
                canteen=canteen_1,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
                value_total_ht=100,
                value_bio_ht=20,
                value_sustainable_ht=30,
                value_externality_performance_ht=None,
                value_egalim_others_ht=None,
                has_waste_diagnostic=False,
                waste_actions=[],
                vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.DAILY,
                plastic_tableware_substituted=False,
                communicates_on_food_quality=False,
            )
            canteen_diagnostic_1.teledeclare(applicant=UserFactory())
            canteen_2 = CanteenFactory(
                siret="75665621899905",
                city_insee_code="69123",
                epci="1",
                pat_list=["1", "2"],
                department="69",
                region="84",
                sectors=[cls.sector_enterprise],
                management_type=Canteen.ManagementType.DIRECT,
                production_type=Canteen.ProductionType.CENTRAL_SERVING,
                economic_model=Canteen.EconomicModel.PUBLIC,
            )
            canteen_diagnostic_2 = DiagnosticFactory(
                canteen=canteen_2,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
                value_total_ht=1000,
                value_bio_ht=400,
                value_sustainable_ht=500,
                value_externality_performance_ht=0,
                value_egalim_others_ht=0,
                has_waste_diagnostic=True,
                waste_actions=["action1", "action2"],
                has_donation_agreement=True,
                vegetarian_weekly_recurrence=Diagnostic.VegetarianMenuFrequency.LOW,
                cooking_plastic_substituted=True,
                serving_plastic_substituted=True,
                plastic_bottles_substituted=True,
                plastic_tableware_substituted=True,
                communicates_on_food_quality=True,
            )
            canteen_diagnostic_2.teledeclare(applicant=UserFactory())
            canteen_3 = CanteenFactory(
                siret="11007001800012",
                city_insee_code="38185",
                epci="2",
                pat_list=["2"],
                department="38",
                region="84",
                sectors=[cls.sector_enterprise, cls.sector_social, cls.sector_education_primary],
                management_type=Canteen.ManagementType.CONCEDED,
                production_type=Canteen.ProductionType.ON_SITE,
                economic_model=Canteen.EconomicModel.PRIVATE,
            )
            canteen_diagnostic_3 = DiagnosticFactory(
                canteen=canteen_3,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=year_data,
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
            canteen_diagnostic_3.teledeclare(applicant=UserFactory())
            CanteenFactory(
                siret="21590350100017",
                city_insee_code="59350",
                epci="3",
                pat_list=["3"],
                department="59",
                region="32",
                sectors=[cls.sector_social],
                management_type=Canteen.ManagementType.CONCEDED,
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                economic_model=Canteen.EconomicModel.PRIVATE,
            )
        with freeze_time("1990-01-01"):
            canteen_5 = CanteenFactory(
                siret="12345678937462",
                city_insee_code="00002",
                epci=None,
                sectors=None,
                management_type=None,
                production_type=None,
                economic_model=None,
                line_ministry=Canteen.Ministries.ARMEE,
            )
            DiagnosticFactory(
                canteen=canteen_5,
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                year=1990,
            )

    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_query_count(self):
        self.assertEqual(Canteen.objects.count(), 5)
        self.assertEqual(Diagnostic.objects.count(), 4)
        self.assertEqual(Diagnostic.objects.teledeclared().count(), 3)
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT + CACHE_GET_QUERY_COUNT + CACHE_SET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_canteen_statistics(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": "84"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        self.assertEqual(body["teledeclarationsCount"], 3)
        self.assertEqual(body["bioPercent"], 43)
        self.assertEqual(body["sustainablePercent"], 44)
        self.assertEqual(body["egalimPercent"], 87)  # 43 + 44
        self.assertEqual(body["approPercent"], 100)
        sector_categories = body["sectorCategories"]
        self.assertEqual(sector_categories[Sector.Categories.EDUCATION], 2)
        self.assertEqual(sector_categories[Sector.Categories.ENTERPRISE], 2)
        self.assertEqual(sector_categories[Sector.Categories.SOCIAL], 1)
        self.assertEqual(sector_categories["inconnu"], 0)

    def test_stats_diagnostic_simple(self):
        """
        The endpoint must take into consideration the simplified diagnostic
        fields for EGalim stats
        """
        past_year = 2021
        date_in_2022_teledeclaration_campaign = "2022-08-30"

        with freeze_time(date_in_2022_teledeclaration_campaign):
            canteen = CanteenFactory(siret="75665621899905")
            # Diagnostic that should display 20% Bio and 45% other EGalim
            canteen_diagnostic = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
                canteen=canteen,
                year=past_year,
                creation_date=date_in_2022_teledeclaration_campaign,
                value_total_ht=100,
                value_bio_ht=20,
                value_sustainable_ht=15,
                value_externality_performance_ht=15,
                value_egalim_others_ht=15,
                value_meat_poultry_ht=200,
                value_meat_poultry_egalim_ht=100,
                value_meat_poultry_france_ht=50,
                value_fish_ht=10,
                value_fish_egalim_ht=8,
            )
            canteen_diagnostic.teledeclare(applicant=UserFactory())

        response = self.client.get(reverse("canteen_statistics"), {"year": past_year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)  # canteens created in 2024 are not returned
        self.assertEqual(body["teledeclarationsCount"], 1)
        self.assertEqual(body["bioPercent"], 20)
        self.assertEqual(body["sustainablePercent"], 45)  # 15 + 15 + 15
        self.assertEqual(body["egalimPercent"], 65)  # 20 + 45
        self.assertEqual(body["meatEgalimPercent"], 50)
        self.assertEqual(body["meatFrancePercent"], 25)
        self.assertEqual(body["fishEgalimPercent"], 80)
        self.assertEqual(body["approPercent"], 100)

    def test_stats_diagnostic_complete(self):
        """
        The endpoint must take into consideration the complete diagnostic
        fields for EGalim stats
        """
        past_year = 2021
        date_in_2022_teledeclaration_campaign = "2022-08-30"

        with freeze_time(date_in_2022_teledeclaration_campaign):
            canteen = CanteenFactory(siret="75665621899905")
            # Diagnostic that should display 20% Bio and 45% other EGalim
            canteen_diagnostic = DiagnosticFactory(
                diagnostic_type=Diagnostic.DiagnosticType.COMPLETE,
                canteen=canteen,
                year=past_year,
                creation_date=date_in_2022_teledeclaration_campaign,
                value_total_ht=100,
                value_viandes_volailles_bio=20,  # value_bio_ht
                value_produits_de_la_mer_label_rouge=15,  # value_sustainable_ht
                value_fruits_et_legumes_externalites=15,  # value_externality_performance_ht
                value_charcuterie_hve=15,  # value_egalim_others_ht
                value_meat_poultry_ht=200,
                value_meat_poultry_egalim_ht=100,
                value_meat_poultry_france_ht=50,
                value_fish_ht=10,
                value_fish_egalim_ht=8,
            )
            canteen_diagnostic.teledeclare(applicant=UserFactory())

        response = self.client.get(reverse("canteen_statistics"), {"year": past_year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)  # canteens created in 2024 are not returned
        self.assertEqual(body["teledeclarationsCount"], 1)
        self.assertEqual(body["bioPercent"], 20)
        self.assertEqual(body["sustainablePercent"], 45)  # 15 + 15 + 15
        self.assertEqual(body["egalimPercent"], 65)  # 20 + 45
        self.assertEqual(body["meatEgalimPercent"], 50)
        self.assertEqual(body["meatFrancePercent"], 25)
        self.assertEqual(body["fishEgalimPercent"], 80)
        self.assertEqual(body["approPercent"], 100)

    def test_filter_out_armee(self):
        # Database
        self.assertEqual(Canteen.objects.count(), 5)
        # API endpoint
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)  # canteen_armee filtered out

    def test_filter_by_year(self):
        # without year: 400
        response = self.client.get(reverse("canteen_statistics"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # year with campaign and report published
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)
        self.assertEqual(body["teledeclarationsCount"], 3)
        self.assertFalse("campaignInfo" in body["notes"])
        # year without campaign (past)
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 0)
        self.assertEqual(body["teledeclarationsCount"], None)
        self.assertTrue("campaignInfo" in body["notes"])
        # year without campaign (future)
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data + 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)
        self.assertEqual(body["teledeclarationsCount"], None)
        self.assertTrue("campaignInfo" in body["notes"])
        # year with campaign but report not published yet
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data + 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)
        self.assertEqual(body["teledeclarationsCount"], 0)
        self.assertTrue("campaignInfo" in body["notes"])

    def test_filter_by_region(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": ["84"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 3)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": ["84", "32"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 3 + 1)

    def test_filter_by_department(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "department": ["01"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "department": ["01", "38"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1 + 1)

    def test_filter_by_epci(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "epci": ["1"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "epci": ["1", "2"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2 + 1)

    def test_filter_by_pat(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "pat": ["1"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "pat": ["1", "2"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2 + 1)

    def test_filter_by_city(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "city": ["01034"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "city": ["01034", "38185"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1 + 1)

    def test_filter_by_sectors(self):
        response = self.client.get(
            reverse("canteen_statistics"),
            {"year": year_data, "sectors": [self.sector_education_primary.id, self.sector_enterprise.id]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        sector_categories = body["sectorCategories"]
        self.assertEqual(sector_categories[Sector.Categories.EDUCATION], 2)
        self.assertEqual(sector_categories[Sector.Categories.ENTERPRISE], 2)
        self.assertEqual(sector_categories["inconnu"], 0)  # because we filtered on sectors beforehand...

    def test_filter_by_management_type(self):
        response = self.client.get(
            reverse("canteen_statistics"),
            {
                "year": year_data,
                "management_type": [Canteen.ManagementType.DIRECT],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)
        management_types = body["managementTypes"]
        self.assertEqual(management_types[Canteen.ManagementType.DIRECT], 2)
        self.assertEqual(management_types[Canteen.ManagementType.CONCEDED], 0)
        self.assertEqual(management_types["inconnu"], 0)

    def test_filter_by_production_type(self):
        response = self.client.get(
            reverse("canteen_statistics"),
            {
                "year": year_data,
                "production_type": [Canteen.ProductionType.CENTRAL, Canteen.ProductionType.CENTRAL_SERVING],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)
        production_types = body["productionTypes"]
        self.assertEqual(production_types[Canteen.ProductionType.CENTRAL], 1)
        self.assertEqual(production_types["centralServing"], 1)  # Canteen.ProductionType.CENTRAL_SERVING
        self.assertEqual(production_types[Canteen.ProductionType.ON_SITE], 0)
        self.assertEqual(production_types["siteCookedElsewhere"], 0)  # Canteen.ProductionType.ON_SITE_CENTRAL
        self.assertEqual(production_types["inconnu"], 0)

    def test_filter_by_economic_model(self):
        response = self.client.get(
            reverse("canteen_statistics"),
            {
                "year": year_data,
                "economic_model": [Canteen.EconomicModel.PUBLIC],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)
        economic_models = body["economicModels"]
        self.assertEqual(economic_models[Canteen.EconomicModel.PUBLIC], 2)
        self.assertEqual(economic_models[Canteen.EconomicModel.PRIVATE], 0)
        self.assertEqual(economic_models["inconnu"], 0)

    def test_notes(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)
        self.assertEqual(body["teledeclarationsCount"], 3)
        self.assertEqual(len(body["notes"]["warnings"]), 1)
        self.assertEqual(
            body["notes"]["canteenCountDescription"], "Au 11 juin 2024"
        )  # dernier jour de la campagne 2024
        self.assertFalse("campaignInfo" in body["notes"])

    def test_cache_mechanism(self):
        # first time: no cache
        self.assertEqual(Canteen.objects.count(), 5)
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT + CACHE_GET_QUERY_COUNT + CACHE_SET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # second time: cache hit
        with self.assertNumQueries(0 + CACHE_GET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # another year: no cache (1 less query because no TDs during this year)
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT - 1 + CACHE_GET_QUERY_COUNT + CACHE_SET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 1})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # another year again: cache hit
        with self.assertNumQueries(0 + CACHE_GET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 1})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # same year, but with extra filters: no cache
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": "84"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # same year, but with extra filters: still no cache
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": "84"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCanteenLocationsApi(APITestCase):
    def test_canteen_locations(self):
        """
        Test that the right subset of regions and departments 'in use' by canteens are returned
        """
        CanteenFactory(department=Department.aisne, department_lib=Department.aisne.label)
        CanteenFactory(department=Department.ain, department_lib=Department.ain.label)
        # set region directly
        CanteenFactory(region=Region.guadeloupe, region_lib=Region.guadeloupe.label, department=None)
        # create extra to check that list returned doesn't contain duplicates
        CanteenFactory(department=Department.aisne, department_lib=Department.aisne.label)
        CanteenFactory(department="999")  # not a department, checking None on region
        CanteenFactory(region="", department="")  # checking exlusion of blank strings

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
