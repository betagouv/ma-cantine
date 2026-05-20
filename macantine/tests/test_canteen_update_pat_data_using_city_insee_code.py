import requests_mock
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from common.api.datagouv import mock_get_pat_csv, mock_get_pat_dataset_resource
from data.factories import CanteenFactory


@requests_mock.Mocker()
class CanteenUpdatePATDataUsingCityInseeCodeCommandTest(TestCase):
    def test_canteen_ok(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(
            city_insee_code="38039",
            pat_list=["1294", "1295"],
            pat_lib_list=[
                "PAT du Département de l'Isère",
                "Projet Alimentaire inter Territorial de la Grande région grenobloise",
            ],
        )

        self.assertEqual(len(canteen.pat_list), 2)
        self.assertEqual(len(canteen.pat_lib_list), 2)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 2)
        self.assertEqual(len(canteen.pat_lib_list), 2)

    def test_canteen_with_pat_lib_missing(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(city_insee_code="38039", pat_list=["1294", "1295"], pat_lib_list=[])

        self.assertEqual(len(canteen.pat_list), 2)
        self.assertEqual(len(canteen.pat_lib_list), 0)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 2)
        self.assertEqual(len(canteen.pat_lib_list), 2)  # updated

    def test_canteen_with_pat_half_missing(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(
            city_insee_code="38039", pat_list=["1294"], pat_lib_list=["PAT du Département de l'Isère"]
        )

        self.assertEqual(len(canteen.pat_list), 1)
        self.assertEqual(len(canteen.pat_lib_list), 1)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 2)  # updated
        self.assertEqual(len(canteen.pat_lib_list), 2)  # updated

    def test_canteen_with_pat_missing(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(city_insee_code="38039", pat_list=[], pat_lib_list=[])

        self.assertEqual(len(canteen.pat_list), 0)
        self.assertEqual(len(canteen.pat_lib_list), 0)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 2)  # updated
        self.assertEqual(len(canteen.pat_lib_list), 2)  # updated

    def test_canteen_with_pat_wrong(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(city_insee_code="38039", pat_list=["9999"], pat_lib_list=["PAT Inconnu"])

        self.assertEqual(len(canteen.pat_list), 1)
        self.assertEqual(len(canteen.pat_lib_list), 1)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 2)  # updated
        self.assertEqual(len(canteen.pat_lib_list), 2)  # updated

    def test_canteen_without_pat(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(city_insee_code="13209", pat_list=[], pat_lib_list=[])

        self.assertEqual(len(canteen.pat_list), 0)
        self.assertEqual(len(canteen.pat_lib_list), 0)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 0)
        self.assertEqual(len(canteen.pat_lib_list), 0)

    def test_canteen_with_pat_to_remove(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(
            city_insee_code="13209", pat_list=["1294"], pat_lib_list=["PAT du Département de l'Isère"]
        )

        self.assertEqual(len(canteen.pat_list), 1)
        self.assertEqual(len(canteen.pat_lib_list), 1)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 0)  # updated
        self.assertEqual(len(canteen.pat_lib_list), 0)  # updated

    def test_canteen_with_no_city_insee_code(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(city_insee_code=None, pat_list=[], pat_lib_list=[])

        self.assertEqual(len(canteen.pat_list), 0)
        self.assertEqual(len(canteen.pat_lib_list), 0)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 0)
        self.assertEqual(len(canteen.pat_lib_list), 0)

    def test_canteen_with_pat_missing_deleted(self, mock):
        mock_get_pat_dataset_resource(mock)
        mock_get_pat_csv(mock)

        canteen = CanteenFactory(city_insee_code="38039", pat_list=[], pat_lib_list=[], deletion_date=timezone.now())

        self.assertEqual(len(canteen.pat_list), 0)
        self.assertEqual(len(canteen.pat_lib_list), 0)

        call_command("canteen_update_pat_data_using_city_insee_code", apply=True)

        canteen.refresh_from_db()

        self.assertEqual(len(canteen.pat_list), 2)  # updated
        self.assertEqual(len(canteen.pat_lib_list), 2)  # updated
