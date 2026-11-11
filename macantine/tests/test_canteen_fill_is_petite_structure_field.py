from django.core.management import call_command
from django.test import TestCase

from data.factories import CanteenFactory
from data.models import Canteen, Sector


class CanteenFillIsPetiteStructureFieldCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.canteen_petite_structure = CanteenFactory(
            management_type=Canteen.ManagementType.DIRECT,
            production_type=Canteen.ProductionType.ON_SITE,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            daily_meal_count=20,
        )
        cls.canteen_not_petite_structure = CanteenFactory(
            management_type=Canteen.ManagementType.CONCEDED,
            production_type=Canteen.ProductionType.ON_SITE,
            sector_list=[Sector.EDUCATION_PRIMAIRE],
            daily_meal_count=20,
        )
        # simulate existing data (field not computed yet, or wrongly)
        Canteen.objects.filter(id=cls.canteen_petite_structure.id).update(is_petite_structure=False)
        Canteen.objects.filter(id=cls.canteen_not_petite_structure.id).update(is_petite_structure=True)

    def test_dry_run(self):
        call_command("canteen_fill_is_petite_structure_field")
        self.assertFalse(Canteen.objects.get(id=self.canteen_petite_structure.id).is_petite_structure)
        self.assertTrue(Canteen.objects.get(id=self.canteen_not_petite_structure.id).is_petite_structure)

    def test_apply(self):
        call_command("canteen_fill_is_petite_structure_field", "--apply")
        self.assertTrue(Canteen.objects.get(id=self.canteen_petite_structure.id).is_petite_structure)
        self.assertFalse(Canteen.objects.get(id=self.canteen_not_petite_structure.id).is_petite_structure)
