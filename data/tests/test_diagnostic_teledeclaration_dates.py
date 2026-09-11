from django.test import TestCase, override_settings
from freezegun import freeze_time
from data.models.diagnostic_teledeclaration_dates import (
    is_in_correction,
    is_in_teledeclaration,
    is_in_teledeclaration_or_correction,
)


@override_settings(TELEDECLARATION_YEAR_OVERRIDE=2024)
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

        with freeze_time("2025-03-30"):  # during the campaign
            self.assertTrue(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertTrue(is_in_teledeclaration_or_correction())
            # test a diagnostic with the correct year
            self.assertTrue(is_in_teledeclaration(2024))
            self.assertFalse(is_in_correction(2024))
            self.assertTrue(is_in_teledeclaration_or_correction(2024))
            # diagnostic in the future
            self.assertFalse(is_in_teledeclaration(2025))
            self.assertFalse(is_in_correction(2025))
            self.assertFalse(is_in_teledeclaration_or_correction(2025))
            # diagnostic in the past
            self.assertFalse(is_in_teledeclaration(2023))
            self.assertFalse(is_in_correction(2023))
            self.assertFalse(is_in_teledeclaration_or_correction(2023))

        with freeze_time("2025-04-06"):  # last day of campaign
            self.assertTrue(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertTrue(is_in_teledeclaration_or_correction())

        with freeze_time("2025-04-07"):  # after campaign (and not yet in correction)
            self.assertFalse(is_in_teledeclaration())
            self.assertFalse(is_in_correction())
            self.assertFalse(is_in_teledeclaration_or_correction())

        with freeze_time("2025-04-20"):  # during the correction campaign
            self.assertFalse(is_in_teledeclaration())
            self.assertTrue(is_in_correction())
            self.assertTrue(is_in_teledeclaration_or_correction())
            # test a diagnostic with the correct year
            self.assertFalse(is_in_teledeclaration(2024))
            self.assertTrue(is_in_correction(2024))
            self.assertTrue(is_in_teledeclaration_or_correction(2024))
            # diagnostic in the future
            self.assertFalse(is_in_teledeclaration(2025))
            self.assertFalse(is_in_correction(2025))
            self.assertFalse(is_in_teledeclaration_or_correction(2025))
            # diagnostic in the past
            self.assertFalse(is_in_teledeclaration(2023))
            self.assertFalse(is_in_correction(2023))
            self.assertFalse(is_in_teledeclaration_or_correction(2023))


class TestIsInTeledeclarationYearOverride(TestCase):
    @override_settings(TELEDECLARATION_YEAR_OVERRIDE=2025)
    def test_uses_override_year_campaign_dates(self):
        # 2025 campaign runs in early 2026; without override, now.year - 1 would be 2025 too,
        # but override must select CAMPAIGN_DATES[2025] even if env would force another year.
        with freeze_time("2026-02-15"):
            self.assertTrue(is_in_teledeclaration())
            self.assertTrue(is_in_teledeclaration(2025))
            self.assertFalse(is_in_teledeclaration(2024))

        with freeze_time("2025-12-01"):  # before 2025 campaign start
            self.assertFalse(is_in_teledeclaration())
            self.assertFalse(is_in_teledeclaration(2025))

    @override_settings(TELEDECLARATION_YEAR_OVERRIDE=2024)
    def test_override_year_differs_from_calendar_year(self):
        # Frozen in 2026 (calendar campaign year would be 2025), but override forces 2024.
        with freeze_time("2026-02-15"):
            self.assertFalse(is_in_teledeclaration())
            self.assertFalse(is_in_teledeclaration(2025))
            self.assertFalse(is_in_teledeclaration(2024))

        # Still within the 2024 campaign window via override
        with freeze_time("2025-03-30"):
            self.assertTrue(is_in_teledeclaration())
            self.assertTrue(is_in_teledeclaration(2024))
            self.assertFalse(is_in_teledeclaration(2025))

    @override_settings(TELEDECLARATION_YEAR_OVERRIDE=2099)
    def test_unknown_override_year_returns_false(self):
        with freeze_time("2026-02-15"):
            self.assertFalse(is_in_teledeclaration())
            self.assertFalse(is_in_teledeclaration(2099))
