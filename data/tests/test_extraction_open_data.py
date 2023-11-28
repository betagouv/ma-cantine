import datetime
from django.test import TestCase
from data.factories import CompleteDiagnosticFactory, DiagnosticFactory, CanteenFactory, UserFactory, SectorFactory
from data.models import Teledeclaration
from macantine.extract_open_data import ETL_CANTEEN, ETL_TD
from freezegun import freeze_time


import json


class TestExtractionOpenData(TestCase):

    @freeze_time("2022-02-14") # Faking time to mock creation_date
    def test_extraction_teledeclaration(self):
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
        self.assertEqual(etl_td.len_dataset(), 1, "There should be one teledeclaration for 2021")
        self.assertEqual(len(etl_td.get_dataset().columns), len(schema_cols), "The columns should match the schema")

        teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        teledeclaration.save()
        etl_td.extract_dataset()
        self.assertEqual(etl_td.len_dataset(), 0, "The list should be empty as the only td has the CANCELLED status")

        canteen.sectors.clear()
        Teledeclaration.create_from_diagnostic(diagnostic_2022, applicant)
        etl_td.extract_dataset()
        self.assertEqual(
            etl_td.get_dataset().iloc[0]["canteen_sectors"], list(), "The sectors should be an empty list"
        )

        canteen = CanteenFactory.create()
        complete_diagnostic = CompleteDiagnosticFactory.create(canteen=canteen, year=2022, diagnostic_type=None)
        etl_td = ETL_TD(complete_diagnostic.year)
        etl_td.extract_dataset()
        self.assertGreater(
            etl_td.get_dataset().iloc[0]["teledeclaration_ratio_bio"], 0, "The bio value is aggregated from bio fields and should be greater than 0"
        )



    def test_extraction_canteen(self):
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

        self.assertIsInstance(canteens["sectors"][0], list, "The sectors should be a list of sectors")
        self.assertEqual(
            list(canteens[canteens.id == canteen_1.id].iloc[0]["sectors"][0].keys()),
            ["id", "name", "category", "hasLineMinistry"],
        )

        canteen_1.department = "29"
        canteen_1.save()
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()

        self.assertEqual(canteens[canteens.id == canteen_1.id].iloc[0]["department_lib"], "Finistère")
        self.assertEqual(canteens[canteens.id == canteen_1.id].iloc[0]["region_lib"], "Bretagne")

        canteen_2.sectors.clear()

        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(
            canteens[canteens.id == canteen_2.id].iloc[0]["sectors"], [], "The sectors should be an empty list"
        )

        canteen_1.sectors.clear()
        try:
            etl_canteen.extract_dataset()
        except Exception:
            self.fail(
                "The extraction should not fail if one column is completely empty. In this case, there is no sector"
            )

        canteen_1.delete()
        etl_canteen.extract_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 1, "There should be one canteen less after soft deletion")

        canteen_2.hard_delete()
        etl_canteen = ETL_CANTEEN()
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(etl_canteen.len_dataset(), 0, "There should be one canteen less after hard deletion")

        CanteenFactory.create(sectors=[SectorFactory.create(name="Restaurants des armées/police/gendarmerie")])
        etl_canteen.extract_dataset()
        canteens = etl_canteen.get_dataset()
        self.assertEqual(
            etl_canteen.len_dataset(),
            0,
            "There should be one canteen less as this specific sector has to remain private",
        )
