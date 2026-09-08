import requests_mock
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from common.api.decoupage_administratif import mock_fetch_communes, mock_fetch_epcis
from common.api.recherche_entreprises import mock_fetch_geo_data_from_siret
from data.factories import CanteenFactory
from data.models import Canteen


@requests_mock.Mocker()
class CanteenUpdateGeolocationDataUsingSiretCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_siren = CanteenFactory(siret=None, siren_unite_legale="123456789", city_insee_code="59512")
        cls.canteen_siret_unknown = CanteenFactory(siret="00000000000000", city_insee_code="12345")
        cls.canteen_siret_closed_deleted = CanteenFactory(
            siret="21380185500072", city_insee_code="38185", deletion_date=timezone.now()
        )
        cls.canteen_siret_city_insee_code_ok = CanteenFactory(siret="92341284500011", city_insee_code="59512")
        cls.canteen_siret_city_insee_code_mismatch = CanteenFactory(city_insee_code="12345")
        cls.canteen_siret_postal_code_ok = CanteenFactory(
            siret="21340172201787", city_insee_code="34172", postal_code="34070"
        )
        cls.canteen_siret_postal_code_mismatch = CanteenFactory(city_insee_code="34172", postal_code="99999")
        Canteen.objects.filter(
            id__in=[cls.canteen_siret_city_insee_code_mismatch.id, cls.canteen_siret_postal_code_mismatch.id]
        ).update(siret="92341284500011")

    def test_command(self, mock):
        mock_fetch_geo_data_from_siret(mock, siret="00000000000000", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="21380185500072", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="92341284500011", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="21340172201787", success=True)
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        self.assertEqual(Canteen.all_objects.count(), 7)
        self.assertEqual(Canteen.objects.count(), 6)

        self.assertEqual(self.canteen_siret_unknown.city_insee_code, "12345")
        self.assertEqual(self.canteen_siret_unknown.siret_inconnu, False)
        self.assertEqual(self.canteen_siret_unknown.siret_etat_administratif, None)
        self.assertEqual(self.canteen_siret_closed_deleted.siret_etat_administratif, None)
        self.assertEqual(self.canteen_siret_city_insee_code_ok.city_insee_code, "59512")
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.city_insee_code, "12345")
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.siret_etat_administratif, None)
        self.assertEqual(self.canteen_siret_postal_code_ok.postal_code, "34070")
        self.assertEqual(self.canteen_siret_postal_code_mismatch.postal_code, "99999")
        self.assertEqual(self.canteen_siret_postal_code_mismatch.siret_etat_administratif, None)

        call_command("canteen_update_geolocation_data_using_siret", apply=True)

        self.canteen_siret_unknown.refresh_from_db()
        self.canteen_siret_closed_deleted.refresh_from_db()
        self.canteen_siret_city_insee_code_ok.refresh_from_db()
        self.canteen_siret_city_insee_code_mismatch.refresh_from_db()
        self.canteen_siret_postal_code_ok.refresh_from_db()
        self.canteen_siret_postal_code_mismatch.refresh_from_db()

        self.assertEqual(self.canteen_siret_unknown.city_insee_code, "12345")  # not reset (yet ?)
        self.assertEqual(self.canteen_siret_unknown.siret_inconnu, True)  # updated
        self.assertEqual(self.canteen_siret_unknown.siret_etat_administratif, None)  # unchanged
        self.assertEqual(self.canteen_siret_closed_deleted.siret_etat_administratif, "F")  # updated
        self.assertEqual(self.canteen_siret_city_insee_code_ok.city_insee_code, "59512")  # unchanged
        self.assertEqual(self.canteen_siret_city_insee_code_ok.siret_etat_administratif, "A")  # updated
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.city_insee_code, "59512")  # reset & updated
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.siret_etat_administratif, "A")  # updated
        self.assertEqual(self.canteen_siret_postal_code_ok.postal_code, "34070")  # unchanged
        self.assertEqual(self.canteen_siret_postal_code_mismatch.postal_code, "59100")  # reset & updated
        self.assertEqual(self.canteen_siret_postal_code_mismatch.siret_etat_administratif, "A")  # updated

    def test_command_dry_run(self, mock):
        mock_fetch_geo_data_from_siret(mock, siret="00000000000000", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="21380185500072", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="92341284500011", success=True)
        mock_fetch_geo_data_from_siret(mock, siret="21340172201787", success=True)
        mock_fetch_communes(mock)
        mock_fetch_epcis(mock)
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        call_command("canteen_update_geolocation_data_using_siret")

        self.canteen_siret_unknown.refresh_from_db()
        self.canteen_siret_closed_deleted.refresh_from_db()
        self.canteen_siret_city_insee_code_ok.refresh_from_db()
        self.canteen_siret_city_insee_code_mismatch.refresh_from_db()
        self.canteen_siret_postal_code_ok.refresh_from_db()
        self.canteen_siret_postal_code_mismatch.refresh_from_db()

        self.assertEqual(self.canteen_siret_unknown.siret_inconnu, False)
        self.assertEqual(self.canteen_siret_closed_deleted.siret_etat_administratif, None)
        self.assertEqual(self.canteen_siret_city_insee_code_ok.city_insee_code, "59512")
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.city_insee_code, "12345")
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.siret_etat_administratif, None)
        self.assertEqual(self.canteen_siret_postal_code_ok.postal_code, "34070")
        self.assertEqual(self.canteen_siret_postal_code_mismatch.postal_code, "99999")
        self.assertEqual(self.canteen_siret_postal_code_mismatch.siret_etat_administratif, None)
