from django.core.management import call_command
from django.test import TestCase

from data.factories import CanteenFactory
from data.models import Canteen, Sector


class CanteenFillComputedFieldsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_ok = CanteenFactory(
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            daily_meal_count=20,
        )
        cls.canteen_not_ok = CanteenFactory(
            siret=None,  # missing data: not filled & not clean
            management_type=Canteen.ManagementType.CONCEDED,  # not a petite structure
            production_type=Canteen.ProductionType.ON_SITE,
            skip_validations=True,
        )

    def setUp(self):
        # simulate existing data (fields not computed yet, or wrongly)
        Canteen.objects.filter(id=self.canteen_ok.id).update(
            is_filled=False, is_clean=False, is_petite_structure=False
        )
        Canteen.objects.filter(id=self.canteen_not_ok.id).update(
            is_filled=True, is_clean=True, is_petite_structure=True
        )

    def test_dry_run(self):
        call_command("canteen_fill_computed_fields")

        canteen_ok = Canteen.objects.get(id=self.canteen_ok.id)
        self.assertFalse(canteen_ok.is_filled)
        self.assertFalse(canteen_ok.is_clean)
        self.assertFalse(canteen_ok.is_petite_structure)
        canteen_not_ok = Canteen.objects.get(id=self.canteen_not_ok.id)
        self.assertTrue(canteen_not_ok.is_filled)
        self.assertTrue(canteen_not_ok.is_clean)
        self.assertTrue(canteen_not_ok.is_petite_structure)

    def test_fill_all_fields(self):
        modification_date_before = Canteen.objects.get(id=self.canteen_ok.id).modification_date
        history_count_before = Canteen.history.count()

        call_command("canteen_fill_computed_fields", "--apply")

        canteen_ok = Canteen.objects.get(id=self.canteen_ok.id)
        self.assertTrue(canteen_ok.is_filled)
        self.assertTrue(canteen_ok.is_clean)
        self.assertTrue(canteen_ok.is_petite_structure)
        self.assertEqual(canteen_ok.modification_date, modification_date_before)  # unchanged
        canteen_not_ok = Canteen.objects.get(id=self.canteen_not_ok.id)
        self.assertFalse(canteen_not_ok.is_filled)
        self.assertFalse(canteen_not_ok.is_clean)
        self.assertFalse(canteen_not_ok.is_petite_structure)
        self.assertEqual(Canteen.history.count(), history_count_before)  # no historical record

    def test_fill_only_some_fields(self):
        call_command("canteen_fill_computed_fields", "--field", "is_clean", "--apply")

        canteen_ok = Canteen.objects.get(id=self.canteen_ok.id)
        self.assertTrue(canteen_ok.is_clean)
        self.assertFalse(canteen_ok.is_filled)  # unchanged
        self.assertFalse(canteen_ok.is_petite_structure)  # unchanged
        canteen_not_ok = Canteen.objects.get(id=self.canteen_not_ok.id)
        self.assertFalse(canteen_not_ok.is_clean)
        self.assertTrue(canteen_not_ok.is_filled)  # unchanged
        self.assertTrue(canteen_not_ok.is_petite_structure)  # unchanged
