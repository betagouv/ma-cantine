import requests_mock
from django.test import TestCase
from django.core.cache import cache

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from common.api.decoupage_administratif import mock_fetch_communes, mock_fetch_epcis
from common.api.recherche_entreprises import fetch_geo_data_from_siret, mock_fetch_geo_data_from_siret
from data.factories import CanteenFactory, UserFactory
from data.models.geo import Department
from macantine import tasks
from data.models import Canteen


@requests_mock.Mocker()
class TestGeolocationUsingInseeCodeBot(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_number_of_api_calls(self, mock):
        """
        There should be one request for every canteens
        """
        manager = UserFactory()  # Avoids integrity errors from user creation
        for i in range(130):
            CanteenFactory(
                city_insee_code="69383",
                city=None,
                managers=[manager],
                geolocation_bot_attempts=0,
            )
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.fill_missing_geolocation_data_using_insee_code()

        self.assertEqual(mock.call_count, 4)

    def test_geolocation_data_filled(self, mock):
        """
        Geolocation data should be filled with the response
        from the API
        """
        canteen = CanteenFactory(city_insee_code="38185", city=None, geolocation_bot_attempts=0)
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.fill_missing_geolocation_data_using_insee_code()

        canteen.refresh_from_db()
        self.assertEqual(canteen.geolocation_bot_attempts, 1)  # incremented
        self.assertEqual(canteen.city, "Grenoble")
        self.assertEqual(canteen.city_insee_code, "38185")
        self.assertEqual(canteen.postal_code, "38000")  # filled
        self.assertEqual(canteen.epci, "200040715")  # filled
        self.assertEqual(canteen.epci_lib, "Grenoble-Alpes-Métropole")  # filled
        self.assertEqual(canteen.pat_list, ["1294"])  # filled
        self.assertEqual(canteen.pat_lib_list, ["PAT du Département de l'Isère"])  # filled
        self.assertEqual(canteen.department, "38")  # filled
        self.assertEqual(canteen.department_lib, "Isère")  # filled
        self.assertEqual(canteen.region, "84")  # filled
        self.assertEqual(canteen.region_lib, "Auvergne-Rhône-Alpes")  # filled
        self.assertEqual(canteen.geolocation_bot_attempts, 1)

    def test_candidate_canteens(self, _):
        """
        Only canteens with INSEE code
        that have not been queried more than ten times
        are considered candidates.
        Data that we want to recover is: city, postal code, department, region
        """
        candidate_canteens = [
            CanteenFactory(city=None, geolocation_bot_attempts=0, postal_code="69003", city_insee_code="69383"),
            CanteenFactory(department=None, geolocation_bot_attempts=9, postal_code="69003", city_insee_code="69383"),
            CanteenFactory(
                department=Department.ain,
                city="Une ville",
                geolocation_bot_attempts=4,
                postal_code=None,
                city_insee_code="69883",
            ),
        ]
        _ = [
            CanteenFactory(
                department=Department.ain,
                city="Une ville",
                geolocation_bot_attempts=1,
                postal_code="69003",
                city_insee_code=None,
            ),
            CanteenFactory(city=None, geolocation_bot_attempts=20, postal_code="69003"),
            CanteenFactory(
                city=None,
                geolocation_bot_attempts=0,
                postal_code="69",
                city_insee_code=None,
            ),
            CanteenFactory(
                city=None,
                geolocation_bot_attempts=0,
                city_insee_code="6009",
                postal_code=None,
            ),
            CanteenFactory(
                department=None,
                geolocation_bot_attempts=1,
                city_insee_code=None,
                postal_code=None,
            ),
        ]

        result = list(Canteen.objects.candidates_for_city_insee_code_to_geo_data_bot())

        self.assertEqual(len(result), 3)
        for canteen in candidate_canteens:
            match = list(filter(lambda x: x.id == canteen.id, result))
            self.assertEqual(len(match), 1)

    def test_geolocation_bot_count(self, mock):
        """
        On every attempt, the geolocation bot count of the
        canteen increases, even if the API returns an error.
        """
        canteen = CanteenFactory(city=None, geolocation_bot_attempts=0, city_insee_code="69883")
        mock_fetch_communes(mock, success=False)
        mock_fetch_epcis(mock, success=False)
        mock_get_pat_dataset_resource(mock, success=False)
        mock_get_pat_csv(mock, success=False)

        tasks.fill_missing_geolocation_data_using_insee_code()

        canteen.refresh_from_db()
        self.assertEqual(canteen.geolocation_bot_attempts, 1)


@requests_mock.Mocker()
class TestGeolocationBotUsingSiret(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_candidate_canteens(self, _):
        """
        Only canteens with SIRET but without city_insee_code
        """
        candidate_canteen = CanteenFactory(siret="89394682276911", city_insee_code=None)
        CanteenFactory(city_insee_code=29890)  # canteen with city_insee_code
        canteen_without_siret = CanteenFactory(city_insee_code=None)
        canteen_without_siret.siret = None  # missing data
        canteen_without_siret.save(skip_validations=True)

        result = list(Canteen.objects.candidates_for_siret_to_city_insee_code_bot())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, candidate_canteen.id)

    def test_get_geo_data(self, mock):
        """
        Should retrieve geo info for a canteen with SIRET but without city_insee_code
        """
        candidate_canteen = CanteenFactory(siret="92341284500011", city_insee_code=None)
        mock_fetch_geo_data_from_siret(mock, candidate_canteen.siret)

        response = fetch_geo_data_from_siret(candidate_canteen.siret)

        self.assertEqual(response["cityInseeCode"], "59512")

    def test_geolocation_with_siret_data_filled(self, mock):
        """
        Geolocation data should be filled with the response
        from the API
        """
        canteen = CanteenFactory(siret="92341284500011", city_insee_code=None, postal_code=None)
        mock_fetch_geo_data_from_siret(mock, canteen.siret)

        tasks.fill_missing_insee_code_using_siret()

        canteen.refresh_from_db()
        self.assertEqual(canteen.city_insee_code, "59512")
        self.assertEqual(canteen.postal_code, None)  # will be filled by the geo bot
