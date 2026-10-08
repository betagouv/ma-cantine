from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase

from data.factories import AccessTokenFactory, ApplicationFactory, PurchaseFactory, RefreshTokenFactory, UserFactory
from data.models import Purchase
from data.models.creation_source import CreationSource


class PurchaseFillCreationSourceApiOauth2ApplicationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application_1 = ApplicationFactory()
        cls.application_2 = ApplicationFactory()

    def setUp(self):
        self.user = UserFactory()
        self.purchase = PurchaseFactory(creation_user=self.user, creation_source=CreationSource.API)
        self.creation_date = self.purchase.creation_date

    def run_command(self, apply=True):
        call_command(
            "purchase_fill_creation_user_and_source", field="creation_source_api_oauth2_application", apply=apply
        )
        self.purchase.refresh_from_db()

    def test_fill_from_token_valid_at_creation_date(self):
        # application_1: token valid at creation date, application_2: token valid later
        AccessTokenFactory(
            user=self.user,
            application=self.application_1,
            created=self.creation_date - timedelta(minutes=10),
            expires=self.creation_date + timedelta(minutes=50),
        )
        AccessTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            expires=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.purchase.creation_source_api_oauth2_application, self.application_1)

    def test_fill_from_only_application_used(self):
        # no token valid at creation date, but the user only ever used application_2
        RefreshTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            revoked=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.purchase.creation_source_api_oauth2_application, self.application_2)

    def test_fill_deleted_purchase(self):
        Purchase.all_objects.filter(id=self.purchase.id).update(deletion_date=self.creation_date + timedelta(days=1))
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command()

        purchase = Purchase.all_objects.get(id=self.purchase.id)
        self.assertEqual(purchase.creation_source_api_oauth2_application, self.application_1)

    def test_not_filled_if_ambiguous(self):
        for application in [self.application_1, self.application_2]:
            RefreshTokenFactory(
                user=self.user, application=application, created=self.creation_date - timedelta(days=1)
            )

        self.run_command()

        self.assertIsNone(self.purchase.creation_source_api_oauth2_application)

    def test_not_filled_if_no_creation_user(self):
        Purchase.all_objects.filter(id=self.purchase.id).update(creation_user=None)
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command()

        self.assertIsNone(self.purchase.creation_source_api_oauth2_application)

    def test_not_filled_if_not_api(self):
        Purchase.all_objects.filter(id=self.purchase.id).update(creation_source=CreationSource.APP)
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command()

        self.assertIsNone(self.purchase.creation_source_api_oauth2_application)

    def test_dry_run_does_not_change_anything(self):
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command(apply=False)

        self.assertIsNone(self.purchase.creation_source_api_oauth2_application)
