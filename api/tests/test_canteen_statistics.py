from unittest.mock import patch

import requests_mock
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase

from data.department_choices import Department
from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory, UserFactory
from data.models import Canteen, Diagnostic, Sector, Teledeclaration
from data.region_choices import Region

year_data = now().year - 1
mocked_campaign_dates = {
    year_data: {
        "teledeclaration_start_date": now().replace(month=1, day=1, hour=0, minute=0, second=0),
        "teledeclaration_end_date": now().replace(month=12, day=31, hour=23, minute=59, second=59),
    }
}


class TestCanteenStatsApi(APITestCase):
    @override_settings(PUBLISH_BY_DEFAULT=False)
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
                    "year": now().replace(year=1990).year,
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

        with patch("data.models.teledeclaration.CAMPAIGN_DATES", mocked_campaign_dates):
            # Create the canteens and diagnostics
            for i, case in enumerate(canteen_cases):
                canteen_sectors = [sector_objects[sector] for sector in case["canteen"].pop("sectors")]
                canteen = CanteenFactory.create(**case["canteen"], sectors=canteen_sectors, siret=str(i))
                diagnostic_data = case["diagnostic"]
                diag = DiagnosticFactory.create(canteen=canteen, **diagnostic_data)
                Teledeclaration.create_from_diagnostic(diag, applicant=UserFactory.create())

            response = self.client.get(reverse("canteen_statistics"), {"region": "01", "year": year_data})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
        self.assertEqual(body["teledeclarationsCount"], 2)
        self.assertEqual(body["bioPercent"], 38)
        self.assertEqual(body["sustainablePercent"], 48)
        self.assertEqual(body["approPercent"], 100)
        sector_categories = body["sectorCategories"]
        self.assertEqual(sector_categories[Sector.Categories.EDUCATION], 3)
        self.assertEqual(sector_categories[Sector.Categories.ENTERPRISE], 1)
        self.assertEqual(sector_categories[Sector.Categories.SOCIAL], 0)

        # can also call without location info
        with patch("data.models.teledeclaration.CAMPAIGN_DATES", mocked_campaign_dates):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test a year without campaign
        with patch("data.models.teledeclaration.CAMPAIGN_DATES", mocked_campaign_dates):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data - 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(body["teledeclarationsCount"], 0)

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

        response = self.client.get(reverse("canteen_statistics"), {"region": region, "year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

    def test_canteen_stats_by_departments(self):
        department = "01"
        department_2 = "02"
        CanteenFactory.create(department=department, publication_status=Canteen.PublicationStatus.PUBLISHED.value)
        CanteenFactory.create(department=department_2, publication_status=Canteen.PublicationStatus.PUBLISHED.value)

        response = self.client.get(
            reverse("canteen_statistics"), {"department": [department, department_2], "year": year_data}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 2)

    def test_canteen_stats_by_sectors(self):
        school = SectorFactory.create(name="School", category=Sector.Categories.EDUCATION)
        enterprise = SectorFactory.create(name="Enterprise", category=Sector.Categories.ENTERPRISE)
        social = SectorFactory.create(name="Social", category=None)
        CanteenFactory.create(sectors=[school])
        CanteenFactory.create(sectors=[enterprise])
        CanteenFactory.create(sectors=[enterprise, social, school])
        CanteenFactory.create(sectors=[social])

        response = self.client.get(
            reverse("canteen_statistics"), {"sectors": [school.id, enterprise.id], "year": year_data}
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

    def test_stats_simple_diagnostic(self):
        """
        The endpoint must take into consideration the simplified diagnostic
        fields for EGalim stats
        """
        published = CanteenFactory.create(
            publication_status=Canteen.PublicationStatus.PUBLISHED.value, siret="75665621899905"
        )

        # Diagnostic that should display 20% Bio and 45% other EGalim
        diag = DiagnosticFactory.create(
            diagnostic_type=Diagnostic.DiagnosticType.SIMPLE,
            canteen=published,
            year=year_data,
            value_total_ht=100,
            value_bio_ht=20,
            value_sustainable_ht=15,
            value_externality_performance_ht=15,
            value_egalim_others_ht=15,
        )
        Teledeclaration.create_from_diagnostic(diag, applicant=UserFactory.create())

        with patch("data.models.teledeclaration.CAMPAIGN_DATES", mocked_campaign_dates):
            response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
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

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data, "epci": epcis})
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

        response = self.client.get(reverse("canteen_statistics"), {"year": year_data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = response.json()
        self.assertEqual(body["canteenCount"], 3)
