from django.test import TestCase
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory, TeledeclarationFactory
from data.models import Teledeclaration
from macantine.tasks import extract_datasets


class TestExtractionOpenData(TestCase):
    td_columns = ["id", "applicant_id", "teledeclaration_mode", "creation_date", "year", "version", "canteen_id", "canteen_siret", "canteen_name", "cantine_central_kitchen_siret", "canteen_department", "canteen_region", "cantine_satellite_canteens_count", "cantine_economic_model", "cantine_management_type", "cantine_production_type", "canteen_sectors", "canteen_line_ministry", "teledeclaration_ratio_bio", "teledeclaration_ratio_egalim_hors_bio"]

    def test_extraction_teledeclaration(self):
        canteen = CanteenFactory.create()
        diagnostic = DiagnosticFactory.create(canteen=canteen, year=2021, diagnostic_type=None)
        applicant = UserFactory.create()
        for year_td in [2021, 2022]:
            TeledeclarationFactory.create(
                applicant=applicant,
                year=year_td,
                canteen=canteen,
                canteen_siret=canteen.siret,
                status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
                diagnostic=diagnostic,
                declared_data={
                    "year": year_td,
                    "canteen": {
                        "name": "",
                    },
                    "applicant": {
                        "name": "",
                    },
                    "teledeclaration": {},
                },
                teledeclaration_mode='SITE',
            )

        td = extract_datasets(year=diagnostic.year)
        assert len(td) == 1, "There should be one teledeclaration for 2021"
        assert td.columns == self.td_columns, "There should be one teledeclaration for 2021"