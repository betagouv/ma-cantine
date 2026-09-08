import requests_mock
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase

from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData
from common.api.datagouv import (
    mock_get_pat_csv,
    mock_get_pat_dataset_resource,
)
from common.api.decoupage_administratif import mock_fetch_communes
from data.models import Diagnostic


class TestTeledeclarationFixOldCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)

    def setUp(self):
        cache.clear()  # clear cache before each test

    @requests_mock.Mocker()
    def test_set_canteen_snapshot_epci_and_pat_list_from_city_insee_code(self, mock):
        mock_fetch_communes(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        # before (at that time, the canteen_snapshot did not store epci & pat_list)
        canteen_snapshot_temp = self.canteen_site_diagnostic_2024.canteen_snapshot
        del canteen_snapshot_temp["epci"]
        del canteen_snapshot_temp["pat_list"]
        Diagnostic.objects.filter(id=self.canteen_site_diagnostic_2024.id).update(
            canteen_snapshot=canteen_snapshot_temp
        )
        self.assertEqual(self.canteen_site_diagnostic_2024.canteen_snapshot.get("city_insee_code"), "38185")
        self.assertNotIn("epci", self.canteen_site_diagnostic_2024.canteen_snapshot)
        self.assertNotIn("pat_list", self.canteen_site_diagnostic_2024.canteen_snapshot)

        # call command
        call_command(
            "teledeclaration_fix_old",
            command="set_canteen_snapshot_epci_and_pat_list_from_city_insee_code",
            apply=True,
        )

        # after
        self.canteen_site_diagnostic_2024.refresh_from_db()
        self.assertEqual(self.canteen_site_diagnostic_2024.canteen_snapshot.get("city_insee_code"), "38185")
        self.assertEqual(self.canteen_site_diagnostic_2024.canteen_snapshot.get("epci"), "200040715")
        self.assertEqual(self.canteen_site_diagnostic_2024.canteen_snapshot.get("pat_list"), ["1294", "1295"])

    @requests_mock.Mocker()
    def test_set_satellites_snapshot_epci_and_pat_list_from_city_insee_code(self, mock):
        mock_fetch_communes(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        # before (at that time, the satellites_snapshot did not store epci & pat_list)
        satellites_snapshot_temp = self.canteen_groupe_diagnostic_2025.satellites_snapshot
        for satellite in satellites_snapshot_temp:
            del satellite["epci"]
            del satellite["pat_list"]
        Diagnostic.objects.filter(id=self.canteen_groupe_diagnostic_2025.id).update(
            satellites_snapshot=satellites_snapshot_temp
        )
        self.assertEqual(self.canteen_groupe_diagnostic_2025.satellites_snapshot[0].get("city_insee_code"), "38185")
        self.assertNotIn("epci", self.canteen_groupe_diagnostic_2025.satellites_snapshot[0])
        self.assertNotIn("pat_list", self.canteen_groupe_diagnostic_2025.satellites_snapshot[0])

        # call command
        call_command(
            "teledeclaration_fix_old",
            command="set_satellites_snapshot_epci_and_pat_list_from_city_insee_code",
            apply=True,
        )

        # after
        self.canteen_groupe_diagnostic_2025.refresh_from_db()
        self.assertEqual(self.canteen_groupe_diagnostic_2025.satellites_snapshot[0].get("city_insee_code"), "38185")
        self.assertEqual(self.canteen_groupe_diagnostic_2025.satellites_snapshot[0].get("epci"), "200040715")
        self.assertEqual(self.canteen_groupe_diagnostic_2025.satellites_snapshot[0].get("pat_list"), ["1294", "1295"])
