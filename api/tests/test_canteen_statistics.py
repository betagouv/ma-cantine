from django.core.cache import cache
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from common.cache.utils import CACHE_GET_QUERY_COUNT, CACHE_SET_QUERY_COUNT
from data.department_choices import Department
from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector, Teledeclaration
from data.region_choices import Region

year_data = 2024
date_in_teledeclaration_campaign = "2025-03-30"
STATS_ENDPOINT_QUERY_COUNT = 7


class TestCanteenStatsApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector_school = SectorFactory.create(name="School", category=Sector.Categories.EDUCATION)
        cls.sector_enterprise = SectorFactory.create(name="Enterprise", category=Sector.Categories.ENTERPRISE)
        cls.sector_social = SectorFactory.create(name="Social", category=None)
        CanteenFactory.create(
            city_insee_code="12345",
            epci="1",
            pat_list=["1"],
            department="01",
            region="84",
            sectors=[cls.sector_school],
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL,
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        CanteenFactory.create(
            city_insee_code="67890",
            epci="1",
            pat_list=["1", "2"],
            department="02",
            region="32",
            sectors=[cls.sector_enterprise],
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.CENTRAL_SERVING,
            economic_model=Canteen.EconomicModel.PUBLIC,
        )
        CanteenFactory.create(
            city_insee_code="11223",
            epci="2",
            pat_list=["2"],
            sectors=[cls.sector_enterprise, cls.sector_social, cls.sector_school],
            management_type=Canteen.ManagementType.CONCEDED,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PRIVATE,
        )
        CanteenFactory.create(
            city_insee_code="11224",
            epci="2",
            pat_list=["2"],
            sectors=[cls.sector_social],
            management_type=Canteen.ManagementType.CONCEDED,
            production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            economic_model=Canteen.EconomicModel.PRIVATE,
        )
        CanteenFactory.create(
            city_insee_code="00000",
            epci=None,
            sectors=None,
            management_type=None,
            production_type=None,
            economic_model=None,
            line_ministry=Canteen.Ministries.ARMEE,
        )

    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_query_count(self):
        self.assertEqual(Canteen.objects.count(), 5)
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT + CACHE_GET_QUERY_COUNT + CACHE_SET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_canteen_statistics(self):
        """
        This public endpoint returns some summary statistics for a region and a location
        """
        # create 5 canteens (3 in region of interest), 1 unpublished
        # Test case definitions
        sectors = {
            "primary_school": {"name": "Primary", "category": Sector.Categories.EDUCATION},
            "secondary_school": {"name": "Secondary", "category": Sector.Categories.EDUCATION},
            "enterprise": {"name": "Enterprise", "category": Sector.Categories.ENTERPRISE},
            "social": {"name": "Social", "category": Sector.Categories.SOCIAL},
        }

        canteen_cases = [
            {
                "description": "First diag should be counted",
                "canteen": {
                    "region": "01",
                    "sectors": ["primary_school", "enterprise"],
                },
                "diagnostic": {
                    "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
                    "year": year_data,
                    "creation_date": date_in_teledeclaration_campaign,
                    "value_total_ht": 100,
                    "value_bio_ht": 20,
                    "value_sustainable_ht": 30,
                    "value_externality_performance_ht": None,
                    "value_egalim_others_ht": None,
                    "has_waste_diagnostic": False,
                    "waste_actions": [],
                    "vegetarian_weekly_recurrence": Diagnostic.VegetarianMenuFrequency.DAILY,
                    "plastic_tableware_substituted": False,
                    "communicates_on_food_quality": False,
                },
            },
            {
                "description": "Should be counted in the stats",
                "canteen": {
                    "region": "01",
                    "sectors": ["primary_school", "secondary_school"],
                },
                "diagnostic": {
                    "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
                    "year": year_data,
                    "creation_date": date_in_teledeclaration_campaign,
                    "value_total_ht": 1000,
                    "value_bio_ht": 400,
                    "value_sustainable_ht": 500,
                    "value_externality_performance_ht": 0,
                    "value_egalim_others_ht": 0,
                    "has_waste_diagnostic": True,
                    "waste_actions": ["action1", "action2"],
                    "has_donation_agreement": True,
                    "vegetarian_weekly_recurrence": Diagnostic.VegetarianMenuFrequency.LOW,
                    "cooking_plastic_substituted": True,
                    "serving_plastic_substituted": True,
                    "plastic_bottles_substituted": True,
                    "plastic_tableware_substituted": True,
                    "communicates_on_food_quality": True,
                },
            },
            {
                "description": "Should not be counted in the stats as its creation date is not part of a campaign",
                "canteen": {
                    "region": "01",
                    "sectors": ["secondary_school"],
                },
                "diagnostic": {
                    "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
                    "year": 1990,
                    "creation_date": "1990-01-01",
                },
            },
            {
                "description": "Should not be counted in the stats of the region 01",
                "canteen": {
                    "region": "03",
                    "sectors": ["social"],
                },
                "diagnostic": {
                    "diagnostic_type": Diagnostic.DiagnosticType.SIMPLE,
                    "year": year_data,
                    "creation_date": date_in_teledeclaration_campaign,
                    "value_total_ht": 100,
                    "value_bio_ht": 100,
                    "value_sustainable_ht": 0,
                    "value_externality_performance_ht": 0,
                    "value_egalim_others_ht": 0,
                    "cooking_plastic_substituted": True,
                    "serving_plastic_substituted": True,
                    "plastic_bottles_substituted": True,
                    "plastic_tableware_substituted": True,
                    "communicates_on_food_quality": True,
                },
            },
        ]

        # Create the sectors
        sector_objects = {key: SectorFactory.create(**attributes) for key, attributes in sectors.items()}

        # Create the canteens and diagnostics
        for i, case in enumerate(canteen_cases):
            canteen_sectors = [sector_objects[sector] for sector in case["canteen"].pop("sectors")]
            canteen = CanteenFactory.create(
                **case["canteen"],
                sectors=canteen_sectors,
                siret=str(i)
            )
            diagnostic_data = case["diagnostic"]
            diag = DiagnosticFactory.create(canteen=canteen, **diagnostic_data)
            with freeze_time(date_in_teledeclaration_campaign):
                Teledeclaration.create_from_diagnostic(diag, applicant=UserFactory.create())

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": "01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        self.assertEqual(body["teledeclarationsCount"], 2)
        self.assertEqual(body["bioPercent"], 38)
        self.assertEqual(body["sustainablePercent"], 48)
        self.assertEqual(body["egalimPercent"], 86)  # 38 + 48
        self.assertEqual(body["approPercent"], 100)
        sector_categories = body["sectorCategories"]
        self.assertEqual(sector_categories[Sector.Categories.EDUCATION], 3)
        self.assertEqual(sector_categories[Sector.Categories.ENTERPRISE], 1)
        self.assertEqual(sector_categories[Sector.Categories.SOCIAL], 0)
        self.assertEqual(sector_categories["inconnu"], 0)

        # can also call without location info
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test a year without campaign
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["teledeclarationsCount"], 0)

    def test_stats_simple_diagnostic(self):
        """
        The endpoint must take into consideration the simplified diagnostic
        fields for EGalim stats
        """
        published = CanteenFactory.create(siret="75665621899905")

        # Diagnostic that should display 20% Bio and 45% other EGalim
        diag = DiagnosticFactory.create(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            canteen=published,
            year=year_data,
            creation_date=date_in_teledeclaration_campaign,
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
        with freeze_time(date_in_teledeclaration_campaign):
            Teledeclaration.create_from_diagnostic(diag, applicant=UserFactory.create())

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4 + 1)
        self.assertEqual(body["teledeclarationsCount"], 1)
        self.assertEqual(body["bioPercent"], 20)
        self.assertEqual(body["sustainablePercent"], 45)
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

    def test_filter_by_year_mandatory(self):
        # without year
        response = self.client.get(reverse("canteen_statistics"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # with year
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)

    def test_filter_by_region(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": ["84"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": ["84", "32"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

    def test_filter_by_department(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "department": ["01"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "department": ["01", "02"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

    def test_filter_by_epci(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "epci": ["1"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "epci": ["1", "2"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)

    def test_filter_by_pat(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "pat": ["1"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "pat": ["1", "2"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)

    def test_filter_by_city(self):
        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 4)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "city": ["12345"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 1)

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "city": ["12345", "11223"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

    def test_filter_by_sectors(self):
        response = self.client.get(
            reverse("canteen_statistics"),
            {"year": year_data, "sectors": [self.sector_school.id, self.sector_enterprise.id]},
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
        # another year: no cache
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT + CACHE_GET_QUERY_COUNT + CACHE_SET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 1})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # another year again: cache hit
        with self.assertNumQueries(0 + CACHE_GET_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 1})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # another year with different filters: no cache
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": "01"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        # another year with different filters: still no cache
        with self.assertNumQueries(STATS_ENDPOINT_QUERY_COUNT):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "region": "01"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCanteenLocationsApi(APITestCase):
    def test_canteen_locations(self):
        """
        Test that the right subset of regions and departments 'in use' by canteens are returned
        """
        CanteenFactory.create(department=Department.aisne, department_lib=Department.aisne.label)
        CanteenFactory.create(department=Department.ain, department_lib=Department.ain.label)
        # set region directly
        CanteenFactory.create(region=Region.guadeloupe, region_lib=Region.guadeloupe.label, department=None)
        # create extra to check that list returned doesn't contain duplicates
        CanteenFactory.create(department=Department.aisne, department_lib=Department.aisne.label)
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
