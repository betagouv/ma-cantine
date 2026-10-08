from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from data.factories import AccessTokenFactory, ApplicationFactory, CanteenFactory, RefreshTokenFactory, UserFactory
from data.models import Canteen
from data.models.creation_source import CreationSource


def create_first_version(canteen, **history_fields):
    """
    CanteenFactory mutes post_save signals, so there is no history on creation
    """
    canteen.save()
    Canteen.history.filter(id=canteen.id).update(history_type="+", **history_fields)


class CanteenFillCreationUserAndSourceTest(TestCase):
    def test_fill_creation_user_from_history(self):
        user = UserFactory()
        canteen = CanteenFactory()
        create_first_version(canteen, history_user=user)
        Canteen.all_objects.filter(id=canteen.id).update(creation_user=None)

        call_command("canteen_fill_creation_user_and_source", field="creation_user", apply=True)

        canteen.refresh_from_db()
        self.assertEqual(canteen.creation_user, user)

    def test_fill_creation_source(self):
        canteen_cuisine_centrale = CanteenFactory(import_source="Cuisine centrale : 12345678901234")
        canteen_import = CanteenFactory(import_source="Import massif")
        canteen_api = CanteenFactory()
        create_first_version(canteen_api, history_change_reason="OAuth2Authentication")
        canteen_unknown = CanteenFactory()
        Canteen.all_objects.update(creation_source=None)

        call_command("canteen_fill_creation_user_and_source", field="creation_source", apply=True)

        for canteen, creation_source in [
            (canteen_cuisine_centrale, CreationSource.APP),
            (canteen_import, CreationSource.IMPORT),
            (canteen_api, CreationSource.API),
            (canteen_unknown, None),
        ]:
            with self.subTest(creation_source=creation_source):
                canteen.refresh_from_db()
                self.assertEqual(canteen.creation_source, creation_source)

    def test_dry_run_does_not_change_anything(self):
        canteen = CanteenFactory(import_source="Import massif")
        Canteen.all_objects.filter(id=canteen.id).update(creation_source=None)

        call_command("canteen_fill_creation_user_and_source", field="creation_source")

        canteen.refresh_from_db()
        self.assertIsNone(canteen.creation_source)


class CanteenFillCreationSourceApiOauth2ApplicationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application_1 = ApplicationFactory()
        cls.application_2 = ApplicationFactory()

    def setUp(self):
        self.user = UserFactory()
        self.canteen = CanteenFactory(creation_user=self.user, creation_source=CreationSource.API)
        self.creation_date = self.canteen.creation_date

    def run_command(self, apply=True):
        call_command(
            "canteen_fill_creation_user_and_source", field="creation_source_api_oauth2_application", apply=apply
        )
        self.canteen.refresh_from_db()

    def test_fill_from_history(self):
        create_first_version(self.canteen, history_source_api_oauth2_application=self.application_2)

        self.run_command()

        self.assertEqual(self.canteen.creation_source_api_oauth2_application, self.application_2)

    def test_fill_from_token_valid_at_creation_date(self):
        # application_1: token valid at creation date, application_2: token valid later
        RefreshTokenFactory(
            user=self.user,
            application=self.application_1,
            created=self.creation_date - timedelta(days=1),
            revoked=self.creation_date + timedelta(hours=1),
        )
        AccessTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            expires=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.canteen.creation_source_api_oauth2_application, self.application_1)

    def test_fill_from_only_application_used(self):
        # no token valid at creation date, but the user only ever used application_2
        RefreshTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            revoked=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.canteen.creation_source_api_oauth2_application, self.application_2)

    def test_not_filled_if_ambiguous(self):
        for application in [self.application_1, self.application_2]:
            RefreshTokenFactory(
                user=self.user, application=application, created=self.creation_date - timedelta(days=1)
            )

        self.run_command()

        self.assertIsNone(self.canteen.creation_source_api_oauth2_application)

    def test_not_filled_if_no_token(self):
        self.run_command()

        self.assertIsNone(self.canteen.creation_source_api_oauth2_application)

    def test_not_filled_if_not_api(self):
        Canteen.all_objects.filter(id=self.canteen.id).update(creation_source=CreationSource.APP)
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command()

        self.assertIsNone(self.canteen.creation_source_api_oauth2_application)

    def test_dry_run_does_not_change_anything(self):
        RefreshTokenFactory(user=self.user, application=self.application_1, created=timezone.now() - timedelta(days=1))

        self.run_command(apply=False)

        self.assertIsNone(self.canteen.creation_source_api_oauth2_application)
