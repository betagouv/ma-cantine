import json
import os

import pandas as pd
import requests_mock
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from freezegun import freeze_time

from common.api.datagouv import update_dataset_resources
from data.factories import CanteenFactory, DiagnosticFactory, SectorFactory, UserFactory
from data.models import Canteen, Sector
from macantine.etl.open_data import (
    ETL_OPEN_DATA_CANTEEN,
    ETL_OPEN_DATA_TELEDECLARATIONS,
)


@requests_mock.Mocker()
class TestETLOpenData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sector_school = SectorFactory(name="School", category=Sector.Categories.EDUCATION)
        cls.user_manager = UserFactory.create()
        cls.canteen = CanteenFactory.create(
            name="Cantine",
            siret="19382111300027",
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
            sectors=[cls.sector_school],
            line_ministry=Canteen.Ministries.AGRICULTURE,
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            economic_model=Canteen.EconomicModel.PUBLIC,
            managers=[cls.user_manager],
            declaration_donnees_2022=True,
            declaration_donnees_2023=False,
            declaration_donnees_2024=True,
        )
        cls.canteen_2 = CanteenFactory.create(
            name="Cantine 2",
            siret="19382111300035",
            sectors=[],
            managers=[cls.user_manager],
            declaration_donnees_2022=True,
        )
        with freeze_time("2023-05-14"):  # during the 2022 campaign
            diagnostic = DiagnosticFactory.create(canteen=cls.canteen, year=2022, diagnostic_type=None)
            diagnostic.teledeclare(cls.user_manager)
            diagnostic_2 = DiagnosticFactory.create(canteen=cls.canteen_2, year=2022, diagnostic_type=None)
            diagnostic_2.teledeclare(cls.user_manager)
        with freeze_time("2024-04-01"):  # during the 2023 campaign
            diagnostic = DiagnosticFactory.create(canteen=cls.canteen, year=2023, diagnostic_type=None)
            diagnostic.teledeclare(cls.user_manager)
            diagnostic.cancel()  # will not appear in the exports
        with freeze_time("2025-04-20"):  # after the 2024 campaign
            diagnostic = DiagnosticFactory.create(canteen=cls.canteen, year=2024, diagnostic_type=None)
            diagnostic.teledeclare(cls.user_manager)

        cls.canteen_without_manager = CanteenFactory.create(siret="75665621899905", sectors=[])
        cls.canteen_without_manager.managers.clear()

    def test_teledeclaration_extract(self, mock):
        # Only teledeclarations that occurred during one specific teledeclaration campaign should be extracted
        etl_td_2022 = ETL_OPEN_DATA_TELEDECLARATIONS(2022)
        etl_td_2022.extract_dataset()
        self.assertEqual(etl_td_2022.len_dataset(), 2, "2 TDs in the 2022 campaign")
        self.assertEqual(
            etl_td_2022.get_dataset().iloc[0]["canteen_id"],
            self.canteen.id,
            "Order by teledeclaration date ascending",
        )

        # Only non-cancelled teledeclarations should be extracted
        etl_td_2023 = ETL_OPEN_DATA_TELEDECLARATIONS(2023)
        etl_td_2023.extract_dataset()
        self.assertEqual(etl_td_2023.len_dataset(), 0, "The only TD in the 2023 campaign has the CANCELLED status")

        etl_td_2024 = ETL_OPEN_DATA_TELEDECLARATIONS(2024)
        etl_td_2024.extract_dataset()
        self.assertEqual(etl_td_2024.len_dataset(), 1, "Only 1 TD in the 2024 campaign")

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

        etl_td = ETL_OPEN_DATA_TELEDECLARATIONS(2024)
        etl_td.extract_dataset()
        etl_td.transform_dataset()

        self.assertEqual(len(etl_td.get_dataset().columns), len(schema_cols), "The columns should match the schema")
        self.assertEqual(etl_td.len_dataset(), 1, "Only 1 TD in the 2024 campaign")
        self.assertEqual(etl_td.get_dataset().iloc[0]["applicant_id"], self.user_manager.id)
        self.assertEqual(etl_td.get_dataset().iloc[0]["canteen_siret"], "19382111300027")
        self.assertEqual(etl_td.get_dataset().iloc[0]["canteen_name"], "Cantine")
        self.assertEqual(etl_td.get_dataset().iloc[0]["canteen_central_kitchen_siret"], None)
        self.assertEqual(str(etl_td.get_dataset().iloc[0]["canteen_satellite_canteens_count"]), "<NA>")
        self.assertEqual(etl_td.get_dataset().iloc[0]["canteen_sectors"], '"[""School""]"')
        self.assertEqual(etl_td.get_dataset().iloc[0]["canteen_line_ministry"], "Agriculture, Alimentation et Forêts")
        self.assertGreater(
            etl_td.get_dataset().iloc[0]["teledeclaration_ratio_bio"],
            0,
            "The bio value is aggregated from bio fields and should be greater than 0",
        )

    def test_canteen_extract(self, mock):
        etl_canteen = ETL_OPEN_DATA_CANTEEN()
        self.assertEqual(etl_canteen.len_dataset(), 0, "There shoud be an empty dataframe before extraction")

        etl_canteen.extract_dataset()
        self.assertEqual(len(etl_canteen.df.id.unique()), 3, "There should be three different canteens")
        self.assertEqual(etl_canteen.get_dataset().iloc[0]["id"], self.canteen.id, "Order by created date ascending")

        # Only non-deleted canteens should be extracted
        self.canteen.delete()
        etl_canteen.extract_dataset()
        self.assertEqual(len(etl_canteen.df.id.unique()), 2, "There should be one canteen less after soft deletion")

        self.canteen_without_manager.hard_delete()
        etl_canteen = ETL_OPEN_DATA_CANTEEN()
        etl_canteen.extract_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 1, "There should be one canteen less after hard deletion")

    def test_canteen_transform(self, mock):
        schema = json.load(open("data/schemas/export_opendata/schema_cantines.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        mock.get(
            "https://geo.api.gouv.fr/communes",
            text=json.dumps([{"code": "38185", "codeEpci": "200040715"}]),
            status_code=200,
        )
        mock.get(
            "https://geo.api.gouv.fr/epcis?fields=nom,code",
            text=json.dumps([{"nom": "Grenoble-Alpes-Métropole", "code": "200040715"}]),
            status_code=200,
        )

        etl_canteen = ETL_OPEN_DATA_CANTEEN()

        etl_canteen.extract_dataset()
        etl_canteen.transform_dataset()
        canteens = etl_canteen.get_dataset()

        # Check the schema matching
        self.assertEqual(len(canteens.columns), len(schema_cols), "The columns should match the schema.")

        canteen = canteens[canteens.id == self.canteen.id].iloc[0]
        self.assertEqual(canteen["epci"], "200040715")
        self.assertEqual(canteen["epci_lib"], "Grenoble-Alpes-Métropole")
        self.assertEqual(canteen["pat_list"], "1294,1295")
        self.assertEqual(
            canteen["pat_lib_list"],
            "PAT du Département de l'Isère,Projet Alimentaire inter Territorial de la Grande région grenobloise",
        )
        self.assertEqual(canteen["line_ministry"], "Agriculture, Alimentation et Forêts")
        self.assertEqual(canteen["management_type"], "direct")
        self.assertEqual(canteen["production_type"], "site")
        self.assertEqual(canteen["economic_model"], "public")
        self.assertEqual(canteen["sectors"], ["School"])
        self.assertTrue(canteen["declaration_donnees_2022"])
        self.assertFalse(canteen["declaration_donnees_2023"])
        self.assertTrue(canteen["declaration_donnees_2024"])
        self.assertTrue(canteen["active_on_ma_cantine"])

        canteen_without_manager = canteens[canteens.id == self.canteen_without_manager.id].iloc[0]
        self.assertEqual(canteen_without_manager["line_ministry"], None)
        self.assertEqual(canteen_without_manager["management_type"], None)
        self.assertEqual(canteen_without_manager["production_type"], None)
        self.assertEqual(canteen_without_manager["economic_model"], None)
        self.assertEqual(canteen_without_manager["sectors"], [])
        self.assertFalse(canteen_without_manager["active_on_ma_cantine"])

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

            self.assertTrue(default_storage.exists(f"open_data/{etl.dataset_name}.parquet"))
            self.assertTrue(default_storage.exists(f"open_data/{etl.dataset_name}.xlsx"))

            # Cleaning files
            for file_extension in ["csv", "parquet", "xslx"]:
                default_storage.delete(f"open_data/{etl.dataset_name}.{file_extension}")
