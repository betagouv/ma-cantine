from django.test import TestCase
from freezegun import freeze_time

from common.tests.utils import (
    date_after_campaign,
    date_before_campaign,
    date_between_campaign_and_campaign_correction,
    date_in_campaign,
    date_in_campaign_correction,
)
from data.models.diagnostic_teledeclaration_dates import (
    CAMPAIGN_DATES,
    get_current_campaign_year,
    is_in_correction,
    is_in_teledeclaration,
)


class CampaignDatesTest(TestCase):
    def assert_campaign_state(self, year, in_teledeclaration, in_correction):
        self.assertEqual(get_current_campaign_year(), year)
        self.assertEqual(is_in_teledeclaration(year), in_teledeclaration)
        self.assertEqual(is_in_correction(year), in_correction)

    def test_date_before_campaign(self):
        for year in [2023, 2024, 2025]:
            with self.subTest(year=year), freeze_time(date_before_campaign(year)):
                self.assert_campaign_state(year, False, False)

    def test_date_before_campaign_starting_on_january_first(self):
        with self.assertRaises(AssertionError):
            date_before_campaign(2026)

    def test_date_in_campaign(self):
        for year in CAMPAIGN_DATES:
            with self.subTest(year=year), freeze_time(date_in_campaign(year)):
                self.assert_campaign_state(year, True, False)

    def test_date_between_campaign_and_correction(self):
        with freeze_time(date_between_campaign_and_campaign_correction(2024)):
            self.assert_campaign_state(2024, False, False)
        for year in [2022, 2025]:  # no correction, or no gap
            with self.subTest(year=year), self.assertRaises(AssertionError):
                date_between_campaign_and_campaign_correction(year)

    def test_date_in_correction(self):
        for year in [2023, 2024, 2025]:
            with self.subTest(year=year), freeze_time(date_in_campaign_correction(year)):
                self.assert_campaign_state(year, False, True)
        with self.assertRaises(AssertionError):
            date_in_campaign_correction(2022)

    def test_date_after_campaign(self):
        for year in CAMPAIGN_DATES:
            with self.subTest(year=year), freeze_time(date_after_campaign(year)):
                self.assert_campaign_state(year, False, False)
