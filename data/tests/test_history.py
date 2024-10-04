from datetime import timedelta

from django.test import TestCase
from django.test.utils import override_settings

from data.factories import CanteenFactory, TeledeclarationFactory
from data.models import AuthenticationMethodHistoricalRecords
from macantine import tasks


class TestModelHistory(TestCase):
    @override_settings(MAX_DAYS_HISTORICAL_RECORDS=1)
    def test_old_history_removal(self):
        canteen = CanteenFactory.create()
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
        canteen = CanteenFactory.create()

        history_count = canteen.history.count()

        # Modify the creation history record to set it back many days
        creation_history_item = canteen.history.get(history_type="+")
        creation_history_item.history_date = creation_history_item.history_date - timedelta(days=160)
        creation_history_item.save()

        # Verify all history items are still there
        tasks.delete_old_historical_records()
        self.assertEqual(canteen.history.count(), history_count)

    def test_authentication_method_created_in_code(self):
        """
        Objects created in code should save the corresponding authentication method
        """
        td = TeledeclarationFactory.create()

        self.assertEqual(
            td.history.first().authentication_method, AuthenticationMethodHistoricalRecords.AuthMethodChoices.AUTO
        )
