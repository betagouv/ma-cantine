from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from data.factories import CanteenFactory, UserFactory
from data.models import Canteen, User


class UserUpdateDataCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_with_canteens = UserFactory()
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE, managers=[cls.user_with_canteens])
        CanteenFactory(production_type=Canteen.ProductionType.ON_SITE_CENTRAL, managers=[cls.user_with_canteens])
        cls.user_without_canteen = UserFactory()
        cls.user_other = UserFactory()

    @mock.patch("macantine.management.commands.user_update_data.BATCH_SIZE", 2)
    def test_update_data_by_batches(self):
        # 3 users, batches of 2: the last (incomplete) batch is also saved
        call_command("user_update_data")

        user_with_canteens = User.objects.get(id=self.user_with_canteens.id)
        self.assertEqual(user_with_canteens.data["nb_cantines"], 2)
        self.assertEqual(user_with_canteens.data["nb_cantines_site"], 1)
        self.assertEqual(user_with_canteens.data["nb_cantines_satellite"], 1)
        self.assertIn("modification_date", user_with_canteens.data)
        for user_id in [self.user_without_canteen.id, self.user_other.id]:
            user = User.objects.get(id=user_id)
            self.assertEqual(user.data["nb_cantines"], 0)

    def test_update_data_skips_user_save(self):
        # bulk_update: no User.save() (validations, avatar optimization...)
        with mock.patch.object(User, "save") as save_mock:
            call_command("user_update_data")
        save_mock.assert_not_called()
        self.assertEqual(User.objects.filter(data__isnull=True).count(), 0)
