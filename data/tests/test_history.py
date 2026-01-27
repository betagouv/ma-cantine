from datetime import timedelta

from django.test import TestCase
from django.core.management import call_command
from django.test.utils import override_settings

from data.factories import CanteenFactory
from macantine import tasks


class HistoryModelTest(TestCase):
    def test_canteen_history_on_save(self):
        # create canteen
        canteen = CanteenFactory(
            siret="21340172201787",
            city_insee_code="34172",
            city=None,
            department=None,
            region=None,
            managers=[],
            sectors_m2m=[],
        )

        # why 2 and not 1?
        # because of the factory's post_generation hooks
        # see https://factoryboy.readthedocs.io/en/stable/recipes.html
        self.assertEqual(canteen.history.count(), 1 + 1)
        self.assertEqual(canteen.history.all().order_by("history_date")[0].history_type, "+")
        delta = canteen.history.first().diff_against(canteen.history.all().order_by("history_date")[0])
        self.assertEqual(len(delta.changes), 0)

        # update canteen: adds a new history record
        canteen.name = "Updated name"
        canteen.save()

        self.assertEqual(canteen.history.count(), 2 + 1)
        self.assertEqual(canteen.history.first().history_type, "~")

        # empty save: adds a new history record
        canteen.save()

        self.assertEqual(canteen.history.count(), 3 + 1)
        self.assertEqual(canteen.history.first().history_type, "~")
        delta = canteen.history.first().diff_against(canteen.history.all().order_by("history_date")[2])
        self.assertEqual(len(delta.changes), 0)

        # change field from None to empty string: adds a new history record
        canteen.city = ""
        canteen.save()

        self.assertEqual(canteen.history.count(), 4 + 1)
        self.assertEqual(canteen.history.first().history_type, "~")
        delta = canteen.history.first().diff_against(canteen.history.all().order_by("history_date")[3])
        self.assertEqual(len(delta.changes), 1)
        self.assertEqual(delta.changes[0].field, "city")

    def test_history_clean_duplicate_command(self):
        # create canteen
        canteen = CanteenFactory(
            siret="21340172201787",
            city_insee_code="34172",
            city=None,
            department=None,
            region=None,
            managers=[],
            sectors_m2m=[],
        )

        # why 2 and not 1?
        # because of the factory's post_generation hooks
        # see https://factoryboy.readthedocs.io/en/stable/recipes.html
        self.assertEqual(canteen.history.count(), 1 + 1)
        self.assertEqual(canteen.history.all().order_by("history_date")[0].history_type, "+")
        delta = canteen.history.first().diff_against(canteen.history.all().order_by("history_date")[0])
        self.assertEqual(len(delta.changes), 0)

        call_command("clean_duplicate_history", "--auto")

        self.assertEqual(canteen.history.count(), 1)
        self.assertEqual(canteen.history.first().history_type, "+")

    @override_settings(MAX_DAYS_HISTORICAL_RECORDS=1)
    def test_old_history_removal(self):
        canteen = CanteenFactory()
        canteen.name = "Updated name"
        canteen.save()

        self.assertGreaterEqual(canteen.history.count(), 2)

        # Modify the creation history record to set it back two days
        creation_history_item = canteen.history.get(history_type="+")
        creation_history_item.history_date = creation_history_item.history_date - timedelta(days=2)
        creation_history_item.save()

        # Verify the creation historical record does not exist anymore
        tasks.delete_old_historical_records()
        self.assertFalse(canteen.history.filter(history_type="+").exists())
        self.assertTrue(canteen.history.filter(history_type="~").exists())

    @override_settings(MAX_DAYS_HISTORICAL_RECORDS=None)
    def test_keep_history_if_env_var_not_set(self):
        canteen = CanteenFactory()

        history_count = canteen.history.count()

        # Modify the creation history record to set it back many days
        creation_history_item = canteen.history.get(history_type="+")
        creation_history_item.history_date = creation_history_item.history_date - timedelta(days=160)
        creation_history_item.save()

        # Verify all history items are still there
        tasks.delete_old_historical_records()
        self.assertEqual(canteen.history.count(), history_count)
