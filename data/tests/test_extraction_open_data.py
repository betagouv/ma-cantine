from django.test import TestCase
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory
from api.serializers import SectorSerializer
from api.views.utils import camelize
from data.models import Teledeclaration
from macantine.tasks import _extract_dataset_teledeclaration, _extract_dataset_canteen
import json


class TestExtractionOpenData(TestCase):
    def test_extraction_teledeclaration(self):
        schema = json.load(open("data/schemas/schema_teledeclaration.json"))
        schema_cols = [i["name"] for i in schema["fields"]]
        canteen = CanteenFactory.create()
        applicant = UserFactory.create()
        for year_td in [2021, 2022]:
            diagnostic = DiagnosticFactory.create(canteen=canteen, year=year_td, diagnostic_type=None)
            td = Teledeclaration.create_from_diagnostic(diagnostic, applicant)

        td = _extract_dataset_teledeclaration(year=diagnostic.year)
        assert len(td) == 1, "There should be one teledeclaration for 2021"
        assert len(td.columns) == len(schema_cols), "The columns should match the schema"

        td.status = Teledeclaration.TeledeclarationStatus.CANCELLED
        td = _extract_dataset_teledeclaration(year=diagnostic.year)
        self.assertEqual(len(td), 0)
        
        canteen.sectors.clear()
        Teledeclaration.create_from_diagnostic(diagnostic, applicant)
        td = _extract_dataset_teledeclaration(year=diagnostic.year)
        self.assertEqual(td.iloc[0]['canteen_sectors'], [''], "The sectors should be an empty list")

    def test_extraction_canteen(self):
        schema = json.load(open("data/schemas/schema_cantine.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        # Adding data in the db
        canteen_1 = CanteenFactory.create()
        canteen_1.managers.add(UserFactory.create())

        canteen_2 = CanteenFactory.create()  # Another canteen, but without a manager
        canteen_2.managers.clear()

        canteens = _extract_dataset_canteen()

        assert len(canteens) == 2, "There should be two canteens"
        assert canteens[canteens.id == canteen_1.id].iloc[0][
            "active_on_ma_cantine"
        ], "The canteen should be active because there is at least one manager"
        assert not canteens[canteens.id == canteen_2.id].iloc[0][
            "active_on_ma_cantine"
        ], "The canteen should not be active because there no manager"
        assert isinstance(canteens["sectors"][0], list), "The sectors should be a list"
        assert len(canteens.columns) == len(schema_cols), "The columns should match the schema."
        self.assertEqual(canteens[canteens.id == canteen_1.id].iloc[0]['sectors'], [camelize(SectorSerializer(x).data) for x in canteen_1.sectors.all()])

        canteen_2.sectors.clear()
        
        canteens = _extract_dataset_canteen()
        assert canteens[canteens.id == canteen_2.id].iloc[0]['sectors'] == [''], "The sectors should be an empty list"

        canteen_1.sectors.clear()
        try:
            _extract_dataset_canteen()
        except Exception:
            self.fail("The extraction should not fail if one column is completely empty. In this case, there is no sector")

