import json
import os

import pandas as pd
import requests_mock
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from freezegun import freeze_time

from common.api.datagouv import update_dataset_resources
from data.models import Canteen, Diagnostic
from macantine.etl.open_data import ETL_OPEN_DATA_CANTEEN, ETL_OPEN_DATA_TELEDECLARATIONS
from macantine.tests.test_etl_common import setUpTestData as ETLCommonSetUpTestData


@requests_mock.Mocker()
class CanteenETLOpenDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls)

    def test_canteen_extract(self, mock):
        self.assertEqual(Canteen.all_objects.count(), 7)
        self.assertEqual(Canteen.objects.count(), 6)  # 1 is deleted

        etl = ETL_OPEN_DATA_CANTEEN()

        self.assertEqual(etl.len_dataset(), 0)  # before extraction

        etl.extract_dataset()

        self.assertEqual(etl.len_dataset(), 4)  # 1 is deleted, 2 are private (armee & groupe)
        self.assertEqual(
            etl.get_dataset().iloc[0]["id"], self.canteen_site_earlier.id
        )  # Order by created date ascending

    def test_canteen_transform(self, mock):
        schema = json.load(open("data/schemas/export_opendata/schema_cantines.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        etl = ETL_OPEN_DATA_CANTEEN()
        etl.extract_dataset()
        etl.transform_dataset()

        # Check the schema matching
        self.assertEqual(len(etl.df.columns), len(schema_cols))

        canteen_site = etl.df[etl.df.id == self.canteen_site.id].iloc[0]
        self.assertEqual(canteen_site["epci"], "200040715")
        self.assertEqual(canteen_site["epci_lib"], "Grenoble-Alpes-Métropole")
        self.assertEqual(canteen_site["pat_list"], "1294,1295")
        self.assertEqual(
            canteen_site["pat_lib_list"],
            "PAT du Département de l'Isère,Projet Alimentaire inter Territorial de la Grande région grenobloise",
        )
        self.assertEqual(canteen_site["department"], "38")
        self.assertEqual(canteen_site["department_lib"], "Isère")
        self.assertEqual(canteen_site["region"], "84")
        self.assertEqual(canteen_site["region_lib"], "Auvergne-Rhône-Alpes")
        self.assertEqual(canteen_site["management_type"], "direct")
        self.assertEqual(canteen_site["production_type"], "site")
        self.assertEqual(canteen_site["economic_model"], "public")
        self.assertEqual(canteen_site["sector_list"], "Hôpitaux,Crèche")
        self.assertEqual(canteen_site["line_ministry"], None)
        self.assertTrue(canteen_site["declaration_donnees_2022"])
        self.assertFalse(canteen_site["declaration_donnees_2025"])
        self.assertTrue(canteen_site["active_on_ma_cantine"])

        canteen_site_without_manager = etl.df[etl.df.id == self.canteen_site_without_manager.id].iloc[0]
        self.assertFalse(canteen_site_without_manager["active_on_ma_cantine"])

        canteen_satellite = etl.df[etl.df.id == self.canteen_satellite.id].iloc[0]
        self.assertEqual(canteen_satellite["groupe_id"], self.canteen_groupe.id)

    @override_settings(STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage")
    def test_canteen_load_dataset(self, mock):
        # Making sure the code will not enter online dataset validation by forcing local filesystem management
        test_cases = [
            {
                "name": " Load valid dataset",
                "data": pd.DataFrame({"index": [0], "name": ["a valid name"]}),
                "expected_length": 1,
            },
            {
                "name": " Load valid dataset with special characters",
                "data": pd.DataFrame({"index": [0], "name": ["a valid name with our csv sep ;"]}),
                "expected_length": 1,
            },
        ]
        etl = ETL_OPEN_DATA_CANTEEN()
        etl.dataset_name += "_test"  # Avoid interferring with other files

        for tc in test_cases:
            etl.df = tc["data"]
            etl.load_dataset()
            with default_storage.open(f"open_data/{etl.dataset_name}.csv", "r") as csv_file:
                output_dataframe = pd.read_csv(csv_file, sep=";")
            self.assertEqual(tc["expected_length"], len(output_dataframe))

            self.assertTrue(default_storage.exists(f"open_data/{etl.dataset_name}.xlsx"))

            # Cleaning files
            for file_extension in ["csv", "xlsx"]:
                default_storage.delete(f"open_data/{etl.dataset_name}.{file_extension}")


@requests_mock.Mocker()
class TeledeclarationETLOpenDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETLCommonSetUpTestData(cls, with_diagnostics=True)

    def test_teledeclaration_extract(self, mock):
        # 2022: 3 teledeclarations (1 is hidden (groupe))
        etl_td_2022 = ETL_OPEN_DATA_TELEDECLARATIONS(2022)
        etl_td_2022.extract_dataset()

        self.assertEqual(Diagnostic.objects.filter(year=2022).count(), 3)
        self.assertEqual(Diagnostic.objects.filter(year=2022).teledeclared().count(), 3)
        self.assertEqual(etl_td_2022.len_dataset(), 2)
        self.assertEqual(
            etl_td_2022.df.iloc[0]["id"], self.canteen_site_earlier_diagnostic_2022.teledeclaration_id
        )  # Order by teledeclaration created date ascending

        # 2023: 1 teledeclaration (1 is cancelled, 1 is hidden (armee))
        etl_td_2023 = ETL_OPEN_DATA_TELEDECLARATIONS(2023)
        etl_td_2023.extract_dataset()

        self.assertEqual(Diagnostic.objects.filter(year=2023).count(), 2)
        self.assertEqual(Diagnostic.objects.filter(year=2023).teledeclared().count(), 1)
        self.assertEqual(etl_td_2023.len_dataset(), 0)

        # 2024: 1 teledeclaration
        etl_td_2024 = ETL_OPEN_DATA_TELEDECLARATIONS(2024)
        etl_td_2024.extract_dataset()

        self.assertEqual(Diagnostic.objects.filter(year=2024).count(), 1)
        self.assertEqual(Diagnostic.objects.filter(year=2024).teledeclared().count(), 1)
        self.assertEqual(etl_td_2024.len_dataset(), 1)

    def test_teledeclaration_transform(self, mock):
        mock.get(
            "https://geo.api.gouv.fr/communes",
            text=json.dumps(""),
            status_code=200,
        )
        mock.get(
            "https://geo.api.gouv.fr/epcis?fields=nom,code",
            text=json.dumps(""),
            status_code=200,
        )

        schema = json.load(open("data/schemas/export_opendata/schema_teledeclarations.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        etl_td_2024 = ETL_OPEN_DATA_TELEDECLARATIONS(2024)
        etl_td_2024.extract_dataset()
        etl_td_2024.transform_dataset()

        # Check the schema matching
        self.assertEqual(len(etl_td_2024.df.columns), len(schema_cols))
        self.assertEqual(set(etl_td_2024.df.columns), set(schema_cols))
        self.assertEqual(etl_td_2024.len_dataset(), 1)

        canteen_site_diagnostic_2024 = etl_td_2024.df[etl_td_2024.df.canteen_id == self.canteen_site.id].iloc[0]
        self.assertEqual(canteen_site_diagnostic_2024["applicant_id"], self.canteen_site_manager_1.id)
        self.assertEqual(canteen_site_diagnostic_2024["canteen_siret"], "21380185500015")
        self.assertEqual(canteen_site_diagnostic_2024["canteen_name"], "Cantine")
        self.assertEqual(canteen_site_diagnostic_2024["canteen_central_kitchen_siret"], None)
        self.assertEqual(canteen_site_diagnostic_2024["canteen_sector_list"], "Hôpitaux,Crèche")
        self.assertEqual(canteen_site_diagnostic_2024["canteen_line_ministry"], None)
        self.assertGreater(
            canteen_site_diagnostic_2024["teledeclaration_ratio_bio"],
            0,
            "The bio value is aggregated from bio fields and should be greater than 0",
        )

    @freeze_time("2023-05-14")  # during the 2022 campaign
    def test_update_ressource(self, mock):
        dataset_id = "expected_dataset_id"
        api_key = "expected_api_key"
        os.environ["DATAGOUV_API_KEY"] = api_key
        expected_header = {"X-API-KEY": api_key}
        resource_id = "expected_resource_id"

        mock.get(
            f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}",
            headers=expected_header,
            json={
                "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. You have requested this URI [/api/1/datasets/6482def590d4cf8cea/] but did you mean /api/1/datasets/schemas/ or /api/1/datasets/<dataset:dataset>/featured/ or /api/1/datasets/<dataset:dataset>/resources/<uuid:rid>/ ?"
            },
            status_code=404,
        )

        os.environ["ENVIRONMENT"] = "prod"

        # 404 error
        number_of_updated_resources = update_dataset_resources(dataset_id)
        self.assertIsNone(number_of_updated_resources)

        mock.get(
            f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}",
            headers=expected_header,
            text=json.dumps(
                {
                    "resources": [
                        {
                            "id": "a_resource_id",
                            "format": "wrong_format",
                            "url": "https://my-url.org/fichier.txt?v=old_date",
                        },
                        {
                            "id": "expected_resource_id",
                            "format": "csv",
                            "url": "https://my-url.org/fichier.csv?v=old_date",
                        },
                    ]
                }
            ),
            status_code=200,
        )
        mock.put(
            f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}/resources/{resource_id}",
            headers=expected_header,
            json={
                "url": "https://cellar-c2.services.clever-cloud.com/ma-cantine-egalim-prod/media/open_data/registre_cantines.xlsx?v=230514"
            },
            status_code=200,
        )

        # empty dataset_id
        number_of_updated_resources = update_dataset_resources(dataset_id="")
        self.assertIsNone(
            number_of_updated_resources, "No resource should be updated as the parameter dataset_id is not set"
        )

        # with dataset_id
        number_of_updated_resources = update_dataset_resources(dataset_id)
        self.assertEqual(number_of_updated_resources, 1, "Only the csv resource should be updated")
