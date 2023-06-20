from django.test import TestCase
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory
from data.models import Teledeclaration
from macantine.tasks import _extract_dataset_teledeclaration#, _extract_dataset_canteen
import json


class TestExtractionOpenData(TestCase):

    def test_extraction_teledeclaration(self):
        schema = json.load(open("data/schemas/schema_teledeclaration.json"))
        schema_cols = [i["name"] for i in schema["fields"]]
        canteen = CanteenFactory.create()
        applicant = UserFactory.create()
        for year_td in [2021, 2022]:
            diagnostic = DiagnosticFactory.create(canteen=canteen, year=year_td, diagnostic_type=None)
            Teledeclaration.create_from_diagnostic(diagnostic, applicant)

        td = _extract_dataset_teledeclaration(year=diagnostic.year)
        assert len(td) == 1, "There should be one teledeclaration for 2021"
        assert len(td.columns) == len(schema_cols) + 1, "The columns should match the schema. Adding the index"
