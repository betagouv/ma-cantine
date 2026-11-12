import requests_mock
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from common.api.decoupage_administratif import mock_fetch_communes, mock_fetch_epcis
from data.factories import CanteenFactory

COMMAND_NAME = "canteen_fill_missing_geo_data_using_city_insee_code"
GEO_FIELDS_EMPTY = {
    "city": None,
    "postal_code": None,
    "epci": None,
    "epci_lib": None,
    "pat_list": [],
    "pat_lib_list": [],
    "department": None,
    "department_lib": None,
    "region": None,
    "region_lib": None,
}


@requests_mock.Mocker()
class CanteenFillMissingGeoDataUsingCityInseeCodeCommandTest(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    def mock_apis(self, mock):
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

    def test_canteen_with_missing_geo_data(self, mock):
        self.mock_apis(mock)
        # e.g. SIRET canteen created via the frontend: city_insee_code, city & postal_code already filled
        canteen = CanteenFactory(
            siret="21340172201787",
            city_insee_code="34172",
            **{**GEO_FIELDS_EMPTY, "city": "Montpellier", "postal_code": "34000"},
        )
        modification_date = canteen.modification_date

        call_command(COMMAND_NAME, apply=True)

        canteen.refresh_from_db()
        self.assertEqual(canteen.city, "Montpellier")
        self.assertEqual(canteen.postal_code, "34000")
        self.assertEqual(canteen.epci, "243400017")
        self.assertEqual(canteen.epci_lib, "Montpellier Méditerranée Métropole")
        self.assertEqual(canteen.pat_list, ["1554", "1555"])
        self.assertEqual(len(canteen.pat_lib_list), 2)
        self.assertEqual(canteen.department, "34")
        self.assertEqual(canteen.department_lib, "Hérault")
        self.assertEqual(canteen.region, "76")
        self.assertEqual(canteen.region_lib, "Occitanie")
        # saved with update_fields
        self.assertEqual(canteen.modification_date, modification_date)
        self.assertEqual(canteen.history.count(), 1)
        self.assertIn(COMMAND_NAME, canteen.history.first().history_change_reason)

    def test_canteen_existing_geo_data_not_overwritten(self, mock):
        self.mock_apis(mock)
        canteen = CanteenFactory(
            siret="21340172201787",
            city_insee_code="34172",
            **{**GEO_FIELDS_EMPTY, "city": "Montpellier", "postal_code": "34070", "department": "34"},
        )

        call_command(COMMAND_NAME, apply=True)

        canteen.refresh_from_db()
        self.assertEqual(canteen.postal_code, "34070")  # not overwritten (the commune's 1st postal code is 34000)
        self.assertEqual(canteen.department, "34")
        self.assertEqual(canteen.department_lib, "Hérault")  # filled
        self.assertEqual(canteen.region, "76")  # filled

    def test_canteen_with_complete_geo_data_not_saved(self, mock):
        self.mock_apis(mock)
        canteen = CanteenFactory(siret="21340172201787", city_insee_code="34172", **GEO_FIELDS_EMPTY)
        call_command(COMMAND_NAME, apply=True)
        canteen.refresh_from_db()
        self.assertEqual(canteen.history.count(), 1)

        # 2nd run: nothing left to fill
        call_command(COMMAND_NAME, apply=True)

        canteen.refresh_from_db()
        self.assertEqual(canteen.history.count(), 1)

    def test_canteen_with_unknown_city_insee_code(self, mock):
        self.mock_apis(mock)
        canteen = CanteenFactory(siret="21340172201787", city_insee_code="12345", **GEO_FIELDS_EMPTY)

        call_command(COMMAND_NAME, apply=True)

        canteen.refresh_from_db()
        self.assertIsNone(canteen.department)
        self.assertEqual(canteen.history.count(), 0)

    def test_canteen_deleted(self, mock):
        self.mock_apis(mock)
        canteen = CanteenFactory(
            siret="21340172201787", city_insee_code="34172", deletion_date=timezone.now(), **GEO_FIELDS_EMPTY
        )

        call_command(COMMAND_NAME, apply=True)

        canteen.refresh_from_db()
        self.assertEqual(canteen.department, "34")

    def test_dry_run(self, mock):
        self.mock_apis(mock)
        canteen = CanteenFactory(siret="21340172201787", city_insee_code="34172", **GEO_FIELDS_EMPTY)

        call_command(COMMAND_NAME)

        canteen.refresh_from_db()
        self.assertIsNone(canteen.department)
        self.assertEqual(canteen.history.count(), 0)
