from unittest.mock import patch

import requests_mock
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from common.api.recherche_entreprises import mock_fetch_geo_data_from_siren, mock_fetch_geo_data_from_siret
from data.factories import CanteenFactory
from data.models import Canteen


@patch("macantine.management.commands.canteen_update_recherche_entreprises_data.time.sleep")
@requests_mock.Mocker()
class CanteenUpdateRechercheEntreprisesDataCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_siret = CanteenFactory(siret="21340172201787", city_insee_code="34172")
        cls.canteen_siret_same = CanteenFactory(city_insee_code="34172", deletion_date=timezone.now())
        cls.canteen_siret_closed_deleted = CanteenFactory(
            siret="21380185500072", city_insee_code="38185", deletion_date=timezone.now()
        )
        cls.canteen_siret_unknown = CanteenFactory(siret="00000000000000", city_insee_code="12345")
        cls.canteen_siret_api_error = CanteenFactory(city_insee_code="59512")
        cls.canteen_siren = CanteenFactory(siret=None, siren_unite_legale="213401722", city_insee_code="34172")
        cls.canteen_siren_unknown = CanteenFactory(siret=None, siren_unite_legale="000000000", city_insee_code="34172")
        cls.canteen_without_siret_siren = CanteenFactory(city_insee_code="34172")
        Canteen.all_objects.filter(id=cls.canteen_siret_same.id).update(siret="21340172201787")  # same SIRET
        Canteen.objects.filter(id=cls.canteen_siret_api_error.id).update(siret="11111111111111")
        Canteen.objects.filter(id=cls.canteen_without_siret_siren.id).update(siret=None, siren_unite_legale=None)

    def _mock_api(self, mock):
        mock_fetch_geo_data_from_siret(mock, siret="21340172201787", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="21380185500072", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="00000000000000", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="11111111111111", success=False)
        mock_fetch_geo_data_from_siren(mock, siren="213401722", success=True)
        mock_fetch_geo_data_from_siren(mock, siren="000000000", success=True)

    def _refresh_all(self):
        for canteen in [
            self.canteen_siret,
            self.canteen_siret_same,
            self.canteen_siret_closed_deleted,
            self.canteen_siret_unknown,
            self.canteen_siret_api_error,
            self.canteen_siren,
            self.canteen_siren_unknown,
            self.canteen_without_siret_siren,
        ]:
            canteen.refresh_from_db()

    def test_command(self, mock_sleep, mock):
        self._mock_api(mock)
        modification_date = Canteen.objects.get(id=self.canteen_siret.id).modification_date

        call_command("canteen_update_recherche_entreprises_data", apply=True)

        self.assertEqual(mock.call_count, 6)  # 1 call per distinct SIRET / SIREN
        self._refresh_all()
        # SIRET: unite_legale & etablissement
        data = self.canteen_siret.recherche_entreprises_data
        self.assertEqual(data["source"], "siret")
        self.assertEqual(data["query"], "21340172201787")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["unite_legale"]["nature_juridique"], "7210")
        self.assertEqual(data["etablissement"]["activite_principale"], "84.11Z")
        self.assertEqual(self.canteen_siret_same.recherche_entreprises_data, data)
        self.assertEqual(self.canteen_siret.modification_date, modification_date)  # unchanged
        self.assertEqual(
            self.canteen_siret_closed_deleted.recherche_entreprises_data["etablissement"]["etat_administratif"], "F"
        )
        self.assertEqual(self.canteen_siret_unknown.recherche_entreprises_data["status"], "not_found")
        self.assertEqual(self.canteen_siret_api_error.recherche_entreprises_data, {})  # unchanged
        # SIREN: unite_legale only
        data = self.canteen_siren.recherche_entreprises_data
        self.assertEqual(data["source"], "siren")
        self.assertEqual(data["query"], "213401722")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["unite_legale"]["etat_administratif"], "A")
        self.assertIsNone(data["etablissement"])
        self.assertEqual(self.canteen_siren_unknown.recherche_entreprises_data["status"], "not_found")
        # no SIRET / SIREN: skipped
        self.assertEqual(self.canteen_without_siret_siren.recherche_entreprises_data, {})

    def test_command_dry_run(self, mock_sleep, mock):
        self._mock_api(mock)

        call_command("canteen_update_recherche_entreprises_data")

        self._refresh_all()
        self.assertEqual(Canteen.all_objects.exclude(recherche_entreprises_data={}).count(), 0)

    def test_command_only_missing(self, mock_sleep, mock):
        self._mock_api(mock)
        already_fetched = {"source": "siret", "query": "21340172201787", "status": "ok", "fetch_date": "2026-01-01"}
        Canteen.all_objects.filter(id__in=[self.canteen_siret.id, self.canteen_siret_same.id]).update(
            recherche_entreprises_data=already_fetched
        )
        # fetched with its previous SIRET: to refetch
        Canteen.objects.filter(id=self.canteen_siren.id).update(
            recherche_entreprises_data={**already_fetched, "query": "21340172201795"}
        )

        call_command("canteen_update_recherche_entreprises_data", only_missing=True, apply=True)

        self.assertEqual(mock.call_count, 5)  # 21340172201787 skipped
        self._refresh_all()
        self.assertEqual(self.canteen_siret.recherche_entreprises_data, already_fetched)  # unchanged
        self.assertEqual(self.canteen_siret_same.recherche_entreprises_data, already_fetched)  # unchanged
        self.assertEqual(self.canteen_siren.recherche_entreprises_data["source"], "siren")  # refetched
        self.assertEqual(self.canteen_siret_unknown.recherche_entreprises_data["status"], "not_found")  # fetched
