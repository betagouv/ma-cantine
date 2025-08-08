from django.test import TestCase
from freezegun import freeze_time

from data.region_choices import Region
from macantine.utils import (
    get_egalim_group,
    is_in_correction,
    is_in_teledeclaration,
    is_in_teledeclaration_or_correction,
)


class TestEgalimObjectives(TestCase):
    def test_get_egalim_group(self):
        self.assertEqual(get_egalim_group([Region.bretagne]), "hexagone")
        self.assertEqual(get_egalim_group([Region.guadeloupe]), "groupe_1")
        self.assertEqual(get_egalim_group([Region.mayotte]), "groupe_2")
        self.assertEqual(get_egalim_group([Region.saint_pierre_et_miquelon]), "groupe_3")
        self.assertEqual(get_egalim_group([Region.bretagne, Region.guadeloupe]), "hexagone")
        # self.assertEqual(get_egalim_group([Region.guadeloupe, Region.bretagne]), "hexagone")
        self.assertEqual(get_egalim_group([Region.guadeloupe, Region.martinique]), "groupe_1")
        self.assertEqual(get_egalim_group([Region.guadeloupe, Region.mayotte]), "groupe_1")
        self.assertEqual(get_egalim_group([]), "hexagone")
        self.assertEqual(get_egalim_group(None), "hexagone")


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
