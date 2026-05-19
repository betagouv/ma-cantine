import requests_mock
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from data.factories import CanteenFactory
from data.models import Canteen


@requests_mock.Mocker()
class CanteenUpdatePATDataUsingCityInseeCodeCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_with_pat = CanteenFactory(
            city_insee_code="38039",
            pat_list=["1294", "1295"],
            pat_lib_list=[
                "PAT du Département de l'Isère",
                "Projet Alimentaire inter Territorial de la Grande région grenobloise",
            ],
        )
        cls.canteen_with_pat_lib_missing = CanteenFactory(
            city_insee_code="38039", pat_list=["1294", "1295"], pat_lib_list=[]
        )
        cls.canteen_with_pat_half_missing = CanteenFactory(
            city_insee_code="38039", pat_list=["1294"], pat_lib_list=["PAT du Département de l'Isère"]
        )
        cls.canteen_with_pat_missing = CanteenFactory(city_insee_code="38039", pat_list=[], pat_lib_list=[])
        cls.canteen_with_pat_wrong = CanteenFactory(
            city_insee_code="38039", pat_list=["9999"], pat_lib_list=["PAT Inconnu"]
        )
        cls.canteen_without_pat = CanteenFactory(city_insee_code="13209", pat_list=[], pat_lib_list=[])
        cls.canteen_wit_pat_to_remove = CanteenFactory(
            city_insee_code="13209", pat_list=["1294"], pat_lib_list=["PAT du Département de l'Isère"]
        )
        cls.canteen_with_no_city_insee_code = CanteenFactory(city_insee_code=None, pat_list=[], pat_lib_list=[])
        cls.canteen_with_pat_missing_deleted = CanteenFactory(
            city_insee_code="38039", pat_list=[], pat_lib_list=[], deletion_date=timezone.now()
        )

    def test_command(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        self.assertEqual(Canteen.all_objects.count(), 9)
        self.assertEqual(Canteen.objects.count(), 8)

        self.assertEqual(len(self.canteen_with_pat.pat_lib_list), 2)
        self.assertEqual(len(self.canteen_with_pat.pat_lib_list), 2)
        self.assertEqual(len(self.canteen_with_pat_lib_missing.pat_list), 2)
        self.assertEqual(len(self.canteen_with_pat_lib_missing.pat_lib_list), 0)
        self.assertEqual(len(self.canteen_with_pat_half_missing.pat_list), 1)
        self.assertEqual(len(self.canteen_with_pat_half_missing.pat_lib_list), 1)
        self.assertEqual(len(self.canteen_with_pat_missing.pat_list), 0)
        self.assertEqual(len(self.canteen_with_pat_missing.pat_lib_list), 0)
        self.assertEqual(len(self.canteen_with_pat_wrong.pat_list), 1)
        self.assertEqual(len(self.canteen_with_pat_wrong.pat_lib_list), 1)
        self.assertEqual(len(self.canteen_without_pat.pat_list), 0)
        self.assertEqual(len(self.canteen_without_pat.pat_lib_list), 0)
        self.assertEqual(len(self.canteen_wit_pat_to_remove.pat_list), 1)
        self.assertEqual(len(self.canteen_wit_pat_to_remove.pat_lib_list), 1)
        self.assertEqual(len(self.canteen_with_no_city_insee_code.pat_list), 0)
        self.assertEqual(len(self.canteen_with_no_city_insee_code.pat_lib_list), 0)
        self.assertEqual(len(self.canteen_with_pat_missing_deleted.pat_list), 0)
        self.assertEqual(len(self.canteen_with_pat_missing_deleted.pat_lib_list), 0)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        self.canteen_with_pat.refresh_from_db()
        self.canteen_with_pat_lib_missing.refresh_from_db()
        self.canteen_with_pat_half_missing.refresh_from_db()
        self.canteen_with_pat_missing.refresh_from_db()
        self.canteen_with_pat_wrong.refresh_from_db()
        self.canteen_without_pat.refresh_from_db()
        self.canteen_wit_pat_to_remove.refresh_from_db()
        self.canteen_with_no_city_insee_code.refresh_from_db()
        self.canteen_with_pat_missing_deleted.refresh_from_db()

        self.assertEqual(len(self.canteen_with_pat.pat_lib_list), 2)
        self.assertEqual(len(self.canteen_with_pat.pat_lib_list), 2)
        self.assertEqual(len(self.canteen_with_pat_lib_missing.pat_list), 2)
        self.assertEqual(len(self.canteen_with_pat_lib_missing.pat_lib_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_half_missing.pat_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_half_missing.pat_lib_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_missing.pat_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_missing.pat_lib_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_wrong.pat_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_wrong.pat_lib_list), 2)  # updated
        self.assertEqual(len(self.canteen_without_pat.pat_list), 0)
        self.assertEqual(len(self.canteen_without_pat.pat_lib_list), 0)
        self.assertEqual(len(self.canteen_wit_pat_to_remove.pat_list), 0)  # updated
        self.assertEqual(len(self.canteen_wit_pat_to_remove.pat_lib_list), 0)  # updated
        self.assertEqual(len(self.canteen_with_no_city_insee_code.pat_list), 0)
        self.assertEqual(len(self.canteen_with_no_city_insee_code.pat_lib_list), 0)
        self.assertEqual(len(self.canteen_with_pat_missing_deleted.pat_list), 2)  # updated
        self.assertEqual(len(self.canteen_with_pat_missing_deleted.pat_lib_list), 2)  # updated
