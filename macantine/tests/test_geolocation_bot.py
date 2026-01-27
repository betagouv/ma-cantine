import requests_mock
from django.test import TestCase
from django.core.cache import cache

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from common.api.decoupage_administratif import mock_fetch_communes, mock_fetch_epcis
from common.api.recherche_entreprises import fetch_geo_data_from_siret, mock_fetch_geo_data_from_siret
from data.factories import CanteenFactory, UserFactory
from macantine import tasks
from data.models import Canteen


@requests_mock.Mocker()
class SiretToGeoDataBotTest(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_get_geo_data(self, mock):
        canteen_without_city_insee_code = CanteenFactory(siret="92341284500011")
        Canteen.objects.filter(id=canteen_without_city_insee_code.id).update(
            city_insee_code=None, city=None, postal_code=None, department=None, region=None
        )
        canteen_without_city_insee_code.refresh_from_db()
        mock_fetch_geo_data_from_siret(mock, canteen_without_city_insee_code.siret)
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.update_canteen_geo_fields_from_siret(canteen_without_city_insee_code)

        self.assertEqual(mock.call_count, 5)
        canteen_without_city_insee_code.refresh_from_db()
        self.assertEqual(canteen_without_city_insee_code.city_insee_code, "59512")
        self.assertEqual(canteen_without_city_insee_code.city, "Roubaix")
        self.assertEqual(canteen_without_city_insee_code.postal_code, "59100")
        self.assertEqual(canteen_without_city_insee_code.department, "59")
        self.assertEqual(canteen_without_city_insee_code.region, "32")


@requests_mock.Mocker()
class SiretToCityInseeCodeGeoBotTest(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_candidate_canteens_queryset(self, _):
        """
        Only canteens with SIRET but without city_insee_code
        """
        # candidate canteen
        candidate_canteen = CanteenFactory(siret="89394682276911")
        candidate_canteen.city_insee_code = None  # missing data
        candidate_canteen.save(skip_validations=True)
        # ignored canteens
        CanteenFactory(city_insee_code=29890)  # canteen with siret & city_insee_code
        canteen_without_siret = CanteenFactory()
        canteen_without_siret.siret = None  # missing data
        canteen_without_siret.city_insee_code = None  # missing data
        canteen_without_siret.save(skip_validations=True)

        self.assertEqual(Canteen.objects.count(), 3)

        result = list(Canteen.objects.candidates_for_siret_to_city_insee_code_bot())

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, candidate_canteen.id)

    def test_get_geo_data(self, mock):
        """
        Should retrieve geo info for a canteen with SIRET & without city_insee_code
        """
        candidate_canteen = CanteenFactory(siret="92341284500011")
        candidate_canteen.city_insee_code = None  # missing data
        candidate_canteen.save(skip_validations=True)

        mock_fetch_geo_data_from_siret(mock, candidate_canteen.siret)

        response = fetch_geo_data_from_siret(candidate_canteen.siret)

        self.assertEqual(response["cityInseeCode"], "59512")


@requests_mock.Mocker()
class CityInseeCodeToGeoFieldsGeoBotTest(TestCase):
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

    def test_candidate_canteens_queryset(self, _):
        """
        Only canteens with INSEE code
        that have not been queried more than ten times
        are considered candidates.
        Data that we want to recover is: city, postal code, department, region
        """
        # candidate canteens
        CanteenFactory(city_insee_code="69383", postal_code=None, geolocation_bot_attempts=0)
        CanteenFactory(city_insee_code="69383", city=None, geolocation_bot_attempts=5)
        CanteenFactory(city_insee_code="69883", department=None, geolocation_bot_attempts=10)
        CanteenFactory(city_insee_code="69883", region=None, geolocation_bot_attempts=15)
        # ignored canteens
        canteen_without_insee_code = CanteenFactory()
        canteen_without_insee_code.city_insee_code = None  # missing insee code
        canteen_without_insee_code.save(skip_validations=True)
        CanteenFactory(city_insee_code="69999", postal_code=None, geolocation_bot_attempts=20)  # too many attempts

        self.assertEqual(Canteen.objects.count(), 6)

        result = list(Canteen.objects.candidates_for_city_insee_code_to_geo_data_bot())

        self.assertEqual(len(result), 4)

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
