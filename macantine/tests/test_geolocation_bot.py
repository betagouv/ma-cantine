import requests_mock
from django.test import TestCase
from django.core.cache import cache

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from common.api.decoupage_administratif import mock_fetch_communes, mock_fetch_epcis
from common.api.recherche_entreprises import mock_fetch_geo_data_from_siret
from data.factories import CanteenFactory
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

        self.assertEqual(canteen_without_city_insee_code.city_insee_code, None)
        self.assertEqual(canteen_without_city_insee_code.city, None)
        self.assertEqual(canteen_without_city_insee_code.postal_code, None)
        self.assertEqual(canteen_without_city_insee_code.department, None)
        self.assertEqual(canteen_without_city_insee_code.region, None)

        mock_fetch_geo_data_from_siret(mock, canteen_without_city_insee_code.siret)
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.update_canteen_geo_fields_from_siret(canteen_without_city_insee_code)

        self.assertEqual(mock.call_count, 6)
        canteen_without_city_insee_code.refresh_from_db()
        self.assertEqual(canteen_without_city_insee_code.city_insee_code, "59512")
        self.assertEqual(canteen_without_city_insee_code.city, "Roubaix")
        self.assertEqual(canteen_without_city_insee_code.postal_code, "59100")
        self.assertEqual(canteen_without_city_insee_code.department, "59")
        self.assertEqual(canteen_without_city_insee_code.region, "32")


@requests_mock.Mocker()
class CityInseeCodeToGeoDataBotTest(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def test_get_geo_data(self, mock):
        canteen_with_city_insee_code = CanteenFactory(siret="92341284500011", city_insee_code="59512")
        Canteen.objects.filter(id=canteen_with_city_insee_code.id).update(
            city=None, postal_code=None, department=None, region=None
        )
        canteen_with_city_insee_code.refresh_from_db()

        self.assertEqual(canteen_with_city_insee_code.city_insee_code, "59512")
        self.assertEqual(canteen_with_city_insee_code.city, None)
        self.assertEqual(canteen_with_city_insee_code.postal_code, None)
        self.assertEqual(canteen_with_city_insee_code.department, None)
        self.assertEqual(canteen_with_city_insee_code.region, None)

        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        tasks.update_canteen_geo_data_from_insee_code(canteen_with_city_insee_code)

        self.assertEqual(mock.call_count, 5)
        canteen_with_city_insee_code.refresh_from_db()
        self.assertEqual(canteen_with_city_insee_code.city_insee_code, "59512")
        self.assertEqual(canteen_with_city_insee_code.city, "Roubaix")
        self.assertEqual(canteen_with_city_insee_code.postal_code, "59100")
        self.assertEqual(canteen_with_city_insee_code.department, "59")
        self.assertEqual(canteen_with_city_insee_code.region, "32")
