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
        TeledeclarationFactory.create(
            applicant=applicant,
            year=diagnostic.year,
            canteen=canteen,
            canteen_siret=canteen.siret,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            diagnostic=diagnostic,
            declared_data={
                "year": diagnostic.year,
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
        TeledeclarationFactory.create(
            applicant=applicant,
            year=diagnostic.year + 1,
            canteen=canteen,
            canteen_siret=canteen.siret,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
            diagnostic=diagnostic,
            declared_data={
                "year": diagnostic.year + 1,
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