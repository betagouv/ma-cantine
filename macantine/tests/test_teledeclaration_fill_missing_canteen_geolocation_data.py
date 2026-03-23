import requests_mock

from django.core.management import call_command
from django.test import TestCase

from data.factories import CanteenFactory, DiagnosticFactory, UserFactory
from data.models import Teledeclaration
from common.api.decoupage_administratif import mock_fetch_communes


class TeledeclarationFillMissingCanteenGeolocationDataCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_with_geo_data = CanteenFactory(
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
        cls.canteen_half_geo_data = CanteenFactory(
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
        cls.canteen_without_geo_data = CanteenFactory(
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
        cls.canteen_without_geo_data_old = CanteenFactory(
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

    @requests_mock.Mocker()
    def test_teledeclaration_fill_missing_canteen_geolocation_data_command(self, mock):
        mock_fetch_communes(mock)
        for canteen in [
            self.canteen_with_geo_data,
            self.canteen_half_geo_data,
            self.canteen_without_geo_data,
            self.canteen_without_geo_data_old,
        ]:
            diag = DiagnosticFactory(canteen=canteen)
            td = Teledeclaration.create_from_diagnostic(diag, applicant=UserFactory())
            # Canteen data for 2021 & 2022 TDs did not include department and region
            if canteen == self.canteen_without_geo_data_old:
                td_declared_data = td.declared_data.copy()
                del td_declared_data["canteen"]["epci"]
                del td_declared_data["canteen"]["pat_list"]
                del td_declared_data["canteen"]["department"]
                del td_declared_data["canteen"]["region"]
                td.declared_data = td_declared_data
                td.save()

        self.assertEqual(Teledeclaration.objects.count(), 4)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__city_insee_code=None).count(), 0)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="epci").count(), 3)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="pat_list").count(), 3)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="department").count(), 3)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__department=None).count(), 1)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="region").count(), 3)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__region=None).count(), 1)

        call_command("teledeclaration_fill_missing_canteen_geolocation_data")

        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="epci").count(), 3)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="pat_list").count(), 3)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="department").count(), 4)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__department=None).count(), 0)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__has_key="region").count(), 4)
        self.assertEqual(Teledeclaration.objects.filter(declared_data__canteen__region=None).count(), 0)
