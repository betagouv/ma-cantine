import requests_mock
from django.test import TestCase
from macantine.extract_open_data import map_communes_infos, update_datagouv_resources
from data.factories import CompleteDiagnosticFactory, DiagnosticFactory, CanteenFactory, UserFactory, SectorFactory
from data.models import Teledeclaration
from macantine.extract_open_data import ETL_CANTEEN, ETL_TD
from freezegun import freeze_time
import json
import os


@requests_mock.Mocker()
class TestExtractionOpenData(TestCase):

    @freeze_time("2023-05-14")  # Faking time to mock creation_date
    def test_extraction_teledeclaration(self, mock):

        mock.get(
            "https://geo.api.gouv.fr/communes",
            text=json.dumps(""),
            status_code=200,
        )
        mock.get(
            "https://geo.api.gouv.fr/epcis/?fields=nom",
            text=json.dumps(""),
            status_code=200,
        )
        schema = json.load(open("data/schemas/schema_teledeclaration.json"))
        schema_cols = [i["name"] for i in schema["fields"]]
        canteen = CanteenFactory.create()
        applicant = UserFactory.create()

        etl_td = ETL_TD(1990)
        self.assertEqual(len(etl_td.extract_dataset()), 0, "There should be no teledeclaration")

        diagnostic_2021 = DiagnosticFactory.create(canteen=canteen, year=2021, diagnostic_type=None)
        Teledeclaration.create_from_diagnostic(diagnostic_2021, applicant)

        diagnostic_2022 = DiagnosticFactory.create(canteen=canteen, year=2022, diagnostic_type=None)
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic_2022, applicant)

        etl_td = ETL_TD(diagnostic_2022.year)
        etl_td.extract_dataset()
        self.assertEqual(etl_td.len_dataset(), 1, "There should be one teledeclaration for 2022")
        self.assertEqual(len(etl_td.get_dataset().columns), len(schema_cols), "The columns should match the schema")

        teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        teledeclaration.save()
        etl_td.extract_dataset()
        self.assertEqual(etl_td.len_dataset(), 0, "The list should be empty as the only td has the CANCELLED status")

        canteen.sectors.clear()
        Teledeclaration.create_from_diagnostic(diagnostic_2022, applicant)
        etl_td.extract_dataset()
        self.assertEqual(
            etl_td.get_dataset().iloc[0]["canteen_sectors"], '"[]"', "The sectors should be an empty list"
        )

        canteen = CanteenFactory.create()
        complete_diagnostic = CompleteDiagnosticFactory.create(canteen=canteen, year=2022, diagnostic_type=None)
        etl_td = ETL_TD(complete_diagnostic.year)
        etl_td.extract_dataset()
        self.assertGreater(
            etl_td.get_dataset().iloc[0]["teledeclaration_ratio_bio"],
            0,
            "The bio value is aggregated from bio fields and should be greater than 0",
        )

    @freeze_time("2022-08-14")  # Faking time to mock creation_date, must be in the campaign dates of 2023
    def test_extraction_canteen(self, mock):
        mock.get(
            "https://geo.api.gouv.fr/communes",
            text=json.dumps([{"code": "29021", "codeEpci": "242900793"}]),
            status_code=200,
        )
        mock.get(
            "https://geo.api.gouv.fr/epcis/?fields=nom",
            text=json.dumps([{"nom": "CC Communauté Lesneven Côte des Légendes", "code": "242900793"}]),
            status_code=200,
        )

        schema = json.load(open("data/schemas/schema_cantine.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        etl_canteen = ETL_CANTEEN()
        etl_canteen.extract_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 0, "There shoud be an empty dataframe")

        # Adding data in the db
        canteen_1 = CanteenFactory.create()
        canteen_1.managers.add(UserFactory.create())

        canteen_2 = CanteenFactory.create()  # Another canteen, but without a manager
        canteen_2.managers.clear()

        etl_canteen.extract_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 2, "There should be two canteens")
        canteens = etl_canteen.get_dataset()
        self.assertTrue(
            canteens[canteens.id == canteen_1.id].iloc[0]["active_on_ma_cantine"],
            "The canteen should be active because there is at least one manager",
        )
        self.assertFalse(
            canteens[canteens.id == canteen_2.id].iloc[0]["active_on_ma_cantine"],
            "The canteen should not be active because there no manager",
        )
        self.assertEqual(len(canteens.columns), len(schema_cols), "The columns should match the schema.")

        self.assertIsInstance(canteens["sectors"][0], str, "The sectors should be a list of sectors")

        # Cheking the geo data transformations
        canteen_1.city_insee_code = "29021"
        canteen_1.save()

        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()

        # Checking that the geo data has been fetched from the city insee code
        self.assertEqual(canteens[canteens.id == canteen_1.id].iloc[0]["epci"], "242900793")

        # Check that the names of the region and departments are fetched from the code
        self.assertEqual(
            canteens[canteens.id == canteen_1.id].iloc[0]["epci_lib"], "CC Communauté Lesneven Côte des Légendes"
        )

        # Checking the campaign participation
        etl_canteen = ETL_CANTEEN()
        applicant = UserFactory.create()
        diagnostic_2021 = DiagnosticFactory.create(canteen=canteen_1, year=2021, diagnostic_type=None)
        _ = Teledeclaration.create_from_diagnostic(diagnostic_2021, applicant)
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(
            canteens[canteens.id == canteen_1.id].iloc[0]["declaration_donnees_2021"],
            True,
            "The canteen has participated in the campain",
        )
        self.assertEqual(
            canteens[canteens.id == canteen_2.id].iloc[0]["declaration_donnees_2021"],
            False,
            "The canteen hasn't participated in the campain",
        )

        canteen_2.sectors.clear()
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(
            canteens[canteens.id == canteen_2.id].iloc[0]["sectors"], '"[]"', "The sectors should be an empty list"
        )

        canteen_1.sectors.clear()
        try:
            etl_canteen.extract_dataset()
        except Exception:
            self.fail(
                "The extraction should not fail if one column is completely empty. In this case, there is no sector"
            )

        # Checking the deletion
        canteen_1.delete()
        etl_canteen.extract_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 1, "There should be one canteen less after soft deletion")

        canteen_2.hard_delete()
        etl_canteen = ETL_CANTEEN()
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 0, "There should be one canteen less after hard deletion")

        CanteenFactory.create(sectors=[SectorFactory.create(id=22)])
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(
            etl_canteen.len_dataset(),
            0,
            "There should be one canteen less as this specific sector has to remain private",
        )

    def test_map_communes_infos(self, mock):
        mock.get(
            "https://geo.api.gouv.fr/communes",
            text=json.dumps(
                [
                    {
                        "nom": "L'Abergement-Clémenciat",
                        "code": "01001",
                        "codeDepartement": "01",
                        "siren": "210100012",
                        "codeEpci": "200069193",
                        "codeRegion": "84",
                        "codesPostaux": ["01400"],
                        "population": "832",
                    },
                    {
                        "nom": "L'Abergement-de-Varey",
                        "code": "01002",
                        "codeDepartement": "01",
                        "siren": "210100020",
                        "codeRegion": "84",
                        "codesPostaux": ["01640"],
                        "population": "267",
                    },
                ]
            ),
        )

        communes_details = map_communes_infos()
        self.assertEqual(len(communes_details), 2)
        self.assertCountEqual(list(communes_details.keys()), ["01001", "01002"])
        self.assertEqual(communes_details["01001"]["department"], "01")
        self.assertEqual(communes_details["01001"]["region"], "84")
        self.assertEqual(communes_details["01001"]["epci"], "200069193")

        self.assertNotIn("epci", communes_details["01002"].keys(), "Not all cities are part of an EPCI")

    @freeze_time("2023-05-14")  # Faking date to check new url
    def test_update_ressource(self, mock):
        dataset_id = "expected_dataset_id"
        os.environ["DATAGOUV_DATASET_ID"] = dataset_id

        api_key = "expected_api_key"
        os.environ["DATAGOUV_API_KEY"] = api_key
        expected_header = {"X-API-KEY": api_key}

        ressource_id = "expected_resource_id"

        mock.get(
            f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}",
            headers=expected_header,
            json={
                "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. You have requested this URI [/api/1/datasets/6482def590d4cf8cea/] but did you mean /api/1/datasets/schemas/ or /api/1/datasets/<dataset:dataset>/featured/ or /api/1/datasets/<dataset:dataset>/resources/<uuid:rid>/ ?"
            },
            status_code=404,
        )

        number_of_updated_resources = update_datagouv_resources()
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
            f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}/resources/{ressource_id}",
            headers=expected_header,
            json={
                "url": "https://cellar-c2.services.clever-cloud.com/ma-cantine-egalim-prod/media/open_data/registre_cantines.xlsx?v=230514"
            },
            status_code=200,
        )
        number_of_updated_resources = update_datagouv_resources()
        self.assertEqual(number_of_updated_resources, 1, "Only the csv resource should be updated")
