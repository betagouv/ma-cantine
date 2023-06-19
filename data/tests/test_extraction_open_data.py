from django.test import TestCase
from django.core import mail
from django.test.utils import override_settings
from django.utils.timezone import now
from data.factories import DiagnosticFactory, CanteenFactory, UserFactory, TeledeclarationFactory
from data.models import Teledeclaration
from macantine.tasks import extract_datasets


class TestExtractionOpenData(TestCase):

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