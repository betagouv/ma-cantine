from django.test import TestCase
from freezegun import freeze_time

from macantine.utils import (
    is_in_correction,
    is_in_teledeclaration,
    is_in_teledeclaration_or_correction,
)


class TestCampaignDates(TestCase):
    def test_campaign_in_2O25(self):
        with freeze_time("2025-01-06"):  # before campaign
            self.assertFalse(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertFalse(is_in_teledeclaration_or_correction())

        with freeze_time("2025-01-07"):  # first day of campaign
            self.assertTrue(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertTrue(is_in_teledeclaration_or_correction())

        with freeze_time("2025-04-06"):  # last day of campaign
            self.assertTrue(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertTrue(is_in_teledeclaration_or_correction())

        with freeze_time("2025-04-07"):  # after campaign
            self.assertFalse(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertFalse(is_in_teledeclaration_or_correction())

        with freeze_time("2025-04-20"):  # middle of correction campaign
            self.assertFalse(is_in_teledeclaration())
            self.assertTrue(is_in_correction())
            self.assertTrue(is_in_teledeclaration_or_correction())
