from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from data.factories import CanteenFactory
from data.models import Canteen
from common.api.recherche_entreprises import mock_fetch_geo_data_from_siret


class CanteenResetGeolocationDataUsingSiretCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_siren = CanteenFactory(siret=None, siren_unite_legale="123456789", city_insee_code="59512")
        cls.canteen_siret_unknown = CanteenFactory(siret="00000000000000", city_insee_code="12345")
        cls.canteen_siret_closed_deleted = CanteenFactory(
            siret="21380185500072", city_insee_code="38185", deletion_date=timezone.now()
        )
        cls.canteen_siret_city_insee_code_mismatch = CanteenFactory(city_insee_code="12345")
        cls.canteen_siret_city_insee_code_ok = CanteenFactory(siret="92341284500011", city_insee_code="59512")
        Canteen.objects.filter(id=cls.canteen_siret_city_insee_code_mismatch.id).update(siret="92341284500011")

    def test_command(self):
        mock_fetch_geo_data_from_siret(self.client, siret="00000000000000", success=True)
        mock_fetch_geo_data_from_siret(self.client, siret="21380185500072", success=True)
        mock_fetch_geo_data_from_siret(self.client, siret="92341284500011", success=True)

        self.assertEqual(Canteen.all_objects.count(), 5)
        self.assertEqual(Canteen.objects.count(), 4)

        self.assertEqual(self.canteen_siret_unknown.city_insee_code, "12345")
        self.assertEqual(self.canteen_siret_unknown.siret_inconnu, False)
        self.assertEqual(self.canteen_siret_closed_deleted.siret_etat_administratif, None)
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.city_insee_code, "12345")
        self.assertEqual(self.canteen_siret_city_insee_code_ok.city_insee_code, "59512")

        call_command("canteen_reset_geolocation_data_using_siret")

        self.canteen_siret_unknown.refresh_from_db()
        self.canteen_siret_closed_deleted.refresh_from_db()
        self.canteen_siret_city_insee_code_mismatch.refresh_from_db()
        self.canteen_siret_city_insee_code_ok.refresh_from_db()

        self.assertEqual(self.canteen_siret_unknown.city_insee_code, None)
        self.assertEqual(self.canteen_siret_unknown.siret_inconnu, True)
        self.assertEqual(self.canteen_siret_closed_deleted.siret_etat_administratif, "F")
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.city_insee_code, "59512")
        self.assertEqual(self.canteen_siret_city_insee_code_mismatch.siret_etat_administratif, "A")
        self.assertEqual(self.canteen_siret_city_insee_code_ok.city_insee_code, "59512")
        self.assertEqual(self.canteen_siret_city_insee_code_ok.siret_etat_administratif, "A")
