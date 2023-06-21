from django.test import TestCase
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory
from data.models import Teledeclaration, Canteen
from macantine.tasks import _extract_dataset_teledeclaration, _extract_dataset_canteen
import json
import pandas as pd


class TestExtractionOpenData(TestCase):

    # def test_extraction_teledeclaration(self):
    #     schema = json.load(open("data/schemas/schema_teledeclaration.json"))
    #     schema_cols = [i["name"] for i in schema["fields"]]
    #     canteen = CanteenFactory.create()
    #     applicant = UserFactory.create()
    #     for year_td in [2021, 2022]:
    #         diagnostic = DiagnosticFactory.create(canteen=canteen, year=year_td, diagnostic_type=None)
    #         Teledeclaration.create_from_diagnostic(diagnostic, applicant)

    #     td = _extract_dataset_teledeclaration(year=diagnostic.year)
    #     assert len(td) == 1, "There should be one teledeclaration for 2021"
    #     assert len(td.columns) == len(schema_cols) + 1, "The columns should match the schema. Adding the index"

    def test_extraction_canteen(self):
        schema = json.load(open("data/schemas/schema_cantine.json"))
        schema_cols = [i["name"] for i in schema["fields"]]

        canteen_1 = CanteenFactory.create()
        canteen_1.managers.add(UserFactory.create())

        canteen_2 = CanteenFactory.create()  # Another canteen, but without a manager
        canteen_2.managers.clear()
        
        canteens = _extract_dataset_canteen()
        assert len(canteens) == 2, "There should be two canteens"
        assert canteens[canteens.id == canteen_1.id].iloc[0]['active_on_ma_cantine'], "The canteen should be active because there is at least one manager"
        assert not canteens[canteens.id == canteen_2.id].iloc[0]['active_on_ma_cantine'], "The canteen should not be active because there no manager"
        assert isinstance(canteens['sectors'][0], list), "The sectors should be a list"