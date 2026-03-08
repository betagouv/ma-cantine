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
            department="38",
            department_lib="Isère",
            region="84",
            region_lib="Auvergne-Rhône-Alpes",
            epci="200040715",
            epci_lib="Grenoble-Alpes-Métropole",
            pat_list=["1294", "1295"],
            pat_lib_list=[
                "PAT du Département de l'Isère",
                "Projet Alimentaire inter Territorial de la Grande région grenobloise",
            ],
        )
        canteen_half_geo_data = CanteenFactory(
            city_insee_code="38185",
            department="38",
            department_lib=None,
            region="84",
            region_lib=None,
            epci="200040715",
            epci_lib=None,
            pat_list=["1294", "1295"],
            pat_lib_list=[],
        )
        canteen_without_geo_data = CanteenFactory(
            city_insee_code="38185",
            department=None,
            department_lib=None,
            region=None,
            region_lib=None,
            epci=None,
            epci_lib=None,
            pat_list=[],
            pat_lib_list=[],
        )
        diagnostic_canteen_with_geo_data = DiagnosticFactory(year=2024, canteen=canteen_with_geo_data)
        diagnostic_canteen_half_geo_data = DiagnosticFactory(year=2024, canteen=canteen_half_geo_data)
        diagnostic_canteen_without_geo_data = DiagnosticFactory(year=2024, canteen=canteen_without_geo_data)
        user = UserFactory()
        with freeze_time("2025-03-30"):
            diagnostic_canteen_with_geo_data.teledeclare(applicant=user)
            diagnostic_canteen_half_geo_data.teledeclare(applicant=user)
            diagnostic_canteen_without_geo_data.teledeclare(applicant=user)

        # before (epci is not in the snapshot fields)
        for diagnostic in [
            diagnostic_canteen_with_geo_data,
            diagnostic_canteen_half_geo_data,
            diagnostic_canteen_without_geo_data,
        ]:
            self.assertIsNone(diagnostic.canteen_snapshot.get("epci"))
            self.assertIsNone(diagnostic.canteen_snapshot.get("pat_list"))

        # call command
        call_command(
            "teledeclaration_fix_old",
            command="set_canteen_snapshot_epci_and_pat_list_from_city_insee_code",
            apply=True,
        )

        # after
        for diagnostic in [
            diagnostic_canteen_with_geo_data,
            diagnostic_canteen_half_geo_data,
            diagnostic_canteen_without_geo_data,
        ]:
            diagnostic.refresh_from_db()
            self.assertIsNotNone(diagnostic.canteen_snapshot.get("epci"))
            self.assertIsNotNone(diagnostic.canteen_snapshot.get("pat_list"))
