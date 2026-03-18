import requests_mock
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase
from freezegun import freeze_time

from common.api.datagouv import (
    mock_get_pat_csv,
    mock_get_pat_dataset_resource,
)
from common.api.decoupage_administratif import mock_fetch_communes
from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Diagnostic


class TestTeledeclarationFixOldCommandTest(TestCase):
    def setUp(self):
        cache.clear()  # clear cache before each test

    @requests_mock.Mocker()
    def test_set_canteen_snapshot_epci_and_pat_list_from_city_insee_code(self, mock):
        mock_fetch_communes(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen_with_geo_data = CanteenFactory(
            city_insee_code="38185",
            epci="200040715",
            epci_lib="Grenoble-Alpes-Métropole",
            pat_list=["1294", "1295"],
            pat_lib_list=[
                "PAT du Département de l'Isère",
                "Projet Alimentaire inter Territorial de la Grande région grenobloise",
            ],
            department="38",
            department_lib="Isère",
            region="84",
            region_lib="Auvergne-Rhône-Alpes",
        )
        canteen_half_geo_data = CanteenFactory(
            city_insee_code="38185",
            epci="200040715",
            epci_lib=None,
            pat_list=["1294", "1295"],
            pat_lib_list=[],
            department="38",
            department_lib=None,
            region="84",
            region_lib=None,
        )
        canteen_without_geo_data = CanteenFactory(
            city_insee_code="38185",
            epci=None,
            epci_lib=None,
            pat_list=[],
            pat_lib_list=[],
            department=None,
            department_lib=None,
            region=None,
            region_lib=None,
        )
        diagnostic_canteen_with_geo_data = DiagnosticFactory(year=2024, canteen=canteen_with_geo_data)
        diagnostic_canteen_half_geo_data = DiagnosticFactory(year=2024, canteen=canteen_half_geo_data)
        diagnostic_canteen_without_geo_data = DiagnosticFactory(year=2024, canteen=canteen_without_geo_data)
        user = UserFactory()
        diagnostic_list = [
            diagnostic_canteen_with_geo_data,
            diagnostic_canteen_half_geo_data,
            diagnostic_canteen_without_geo_data,
        ]
        with freeze_time("2025-03-30"):  # during the 2024 campaign
            for diagnostic in diagnostic_list:
                diagnostic.teledeclare(applicant=user)
                # at that time, the snapshots did not store epci & pat_list
                canteen_snapshot_temp = diagnostic.canteen_snapshot
                del canteen_snapshot_temp["epci"]
                del canteen_snapshot_temp["pat_list"]
                Diagnostic.objects.filter(id=diagnostic.id).update(canteen_snapshot=canteen_snapshot_temp)

        # before
        for diagnostic in diagnostic_list:
            diagnostic.refresh_from_db()
            self.assertNotIn("epci", diagnostic.canteen_snapshot)
            self.assertNotIn("pat_list", diagnostic.canteen_snapshot)

        # call command
        call_command(
            "teledeclaration_fix_old",
            command="set_canteen_snapshot_epci_and_pat_list_from_city_insee_code",
            apply=True,
        )

        # after
        for diagnostic in diagnostic_list:
            diagnostic.refresh_from_db()
            self.assertEqual(diagnostic.canteen_snapshot.get("epci"), "200040715")
            self.assertEqual(diagnostic.canteen_snapshot.get("pat_list"), ["1294", "1295"])
