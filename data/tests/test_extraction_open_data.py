from django.test import TestCase
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory
from data.models import Teledeclaration
from macantine.tasks import extract_datasets


class TestExtractionOpenData(TestCase):
    td_columns = ["id", "applicant_id", "teledeclaration_mode", "creation_date", "year", "version", "canteen.id", "canteen.siret", "canteen.name", "canteen.central_producer_siret", "canteen.department", "canteen.region", "canteen.satellite_canteens_count", "canteen.economic_model", "canteen.management_type", "canteen.production_type", "canteen.sectors", "canteen.line_ministry", "teledeclaration.value_bio_ht", "teledeclaration.value_total_ht", "teledeclaration.value_sustainable_ht"]

    def test_extraction_teledeclaration(self):
        canteen = CanteenFactory.create()
        applicant = UserFactory.create()
        for year_td in [2021, 2022]:
            diagnostic = DiagnosticFactory.create(canteen=canteen, year=year_td, diagnostic_type=None)
            Teledeclaration.create_from_diagnostic(diagnostic, applicant)

        td = extract_datasets(year=diagnostic.year)
        assert len(td) == 1, "There should be one teledeclaration for 2021"
        assert len(td.columns) == len(self.td_columns) + 1, "The columns should match the schema. Adding the index"