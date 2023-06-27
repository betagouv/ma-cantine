from django.test import TestCase
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory, SectorFactory
from data.models import Teledeclaration
from macantine.tasks import _extract_dataset_teledeclaration, _extract_dataset_canteen
import json


class TestExtractionOpenData(TestCase):
    def test_extraction_teledeclaration(self):
        schema = json.load(open("data/schemas/schema_teledeclaration.json"))
        schema_cols = [i["name"] for i in schema["fields"]]
        canteen = CanteenFactory.create()
        applicant = UserFactory.create()

        self.assertEqual(len(_extract_dataset_teledeclaration(year=1990)), 0, "There should be no teledeclaration")

        diagnostic_2021 = DiagnosticFactory.create(canteen=canteen, year=2021, diagnostic_type=None)
        Teledeclaration.create_from_diagnostic(diagnostic_2021, applicant)
        diagnostic_2022 = DiagnosticFactory.create(canteen=canteen, year=2022, diagnostic_type=None)
        teledeclaration = Teledeclaration.create_from_diagnostic(diagnostic_2022, applicant)

        td = _extract_dataset_teledeclaration(year=diagnostic_2022.year)
        self.assertEqual(len(td), 1, "There should be one teledeclaration for 2021")
        self.assertEqual(len(td.columns), len(schema_cols), "The columns should match the schema")

        teledeclaration.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        teledeclaration.save()
        td = _extract_dataset_teledeclaration(year=diagnostic_2022.year)
        self.assertEqual(len(td), 0)

        canteen.sectors.clear()
        Teledeclaration.create_from_diagnostic(diagnostic_2022, applicant)
        td = _extract_dataset_teledeclaration(year=diagnostic_2022.year)
        self.assertEqual(td.iloc[0]["canteen_sectors"], list(), "The sectors should be an empty list")

    def test_extraction_canteen(self):
        schema = json.load(open("data/schemas/schema_cantine.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        canteens = _extract_dataset_canteen()
        self.assertEqual(len(canteens), 0, "There shoud be an empty dataframe")

        # Adding data in the db
        canteen_1 = CanteenFactory.create()
        canteen_1.managers.add(UserFactory.create())

        canteen_2 = CanteenFactory.create()  # Another canteen, but without a manager
        canteen_2.managers.clear()

        canteens = _extract_dataset_canteen()
        self.assertEqual(len(canteens), 2, "There should be two canteens")
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

        canteen_2.sectors.clear()

        canteens = _extract_dataset_canteen()
        self.assertEqual(
            canteens[canteens.id == canteen_2.id].iloc[0]["sectors"], [], "The sectors should be an empty list"
        )

        canteen_1.sectors.clear()
        try:
            _extract_dataset_canteen()
        except Exception:
            self.fail(
                "The extraction should not fail if one column is completely empty. In this case, there is no sector"
            )

        canteen_1.delete()
        canteens = _extract_dataset_canteen()
        self.assertEqual(len(canteens), 1, "There should be one canteen less after soft deletion")

        canteen_2.hard_delete()
        canteens = _extract_dataset_canteen()
        self.assertEqual(len(canteens), 0, "There should be one canteen less after hard deletion")

        CanteenFactory.create(sectors=[SectorFactory.create(name="Restaurants des armées/police/gendarmerie")])
        canteens = _extract_dataset_canteen()
        self.assertEqual(
            len(canteens), 0, "There should be one canteen less as this specific sector has to remain private"
        )
