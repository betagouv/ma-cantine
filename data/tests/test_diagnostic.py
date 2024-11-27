from unittest.mock import patch

from django.test import TestCase
from django.utils.timezone import now

from data.factories import UserFactory
from data.models import Canteen, Diagnostic, Teledeclaration

year_data = now().year - 1
mocked_campaign_dates = {
    year_data: {
        "start_date": now().replace(month=1, day=1, hour=0, minute=0, second=0),
        "end_date": now().replace(month=12, day=31, hour=23, minute=59, second=59),
    }
}


class DiagForStatsQuerySetTest(TestCase):
    def setUp(self):
        """
        Set up mock data for testing.
        The date is freezed to an old date in order to have freedom to create teledeclaration with correct date
        (using fake time direclty corrupts the QuerySet Date Range filter)
        """

        # Create canteens and diagnostics
        self.valid_canteen = Canteen.objects.create(id=1, siret="12345678901234", deletion_date=None)
        self.invalid_canteen = Canteen.objects.create(id=2, siret="", deletion_date=None)
        self.deleted_canteen = Canteen.objects.create(
            id=3,
            siret="56789012345678",
            deletion_date=now().replace(month=6, day=1),
        )

        self.valid_diagnostic = Diagnostic.objects.create(
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.valid_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )

        Teledeclaration.create_from_diagnostic(self.valid_diagnostic, applicant=UserFactory.create())

        self.invalid_diagnostic = Diagnostic.objects.create(
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.invalid_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        Teledeclaration.create_from_diagnostic(self.invalid_diagnostic, applicant=UserFactory.create())

        self.deleted_canteen_diagnostic = Diagnostic.objects.create(
            year=year_data,
            creation_date=now().replace(month=3, day=1),
            canteen=self.deleted_canteen,
            value_total_ht=1000.00,
            value_bio_ht=200.00,
        )
        Teledeclaration.create_from_diagnostic(self.deleted_canteen_diagnostic, applicant=UserFactory.create())
        # status ?

    @patch("macantine.utils.CAMPAIGN_DATES")
    def test_diags_for_stat(self, mock_campaign_dates):
        """
        Test the diags_for_stat method.
        """
        with patch("macantine.utils.CAMPAIGN_DATES", mocked_campaign_dates):
            diagnostics = Diagnostic.objects.diags_for_stat(now().year - 1)
        self.assertIn(self.valid_diagnostic, diagnostics)
        self.assertNotIn(self.invalid_diagnostic, diagnostics)
        self.assertNotIn(self.deleted_canteen_diagnostic, diagnostics)
