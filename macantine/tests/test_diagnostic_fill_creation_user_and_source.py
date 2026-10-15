from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase

from data.factories import AccessTokenFactory, ApplicationFactory, DiagnosticFactory, RefreshTokenFactory, UserFactory
from data.models import Diagnostic
from data.models.creation_source import CreationSource


class DiagnosticFillCreationUserAndSourceTest(TestCase):
    def test_fill_creation_user_from_history(self):
        user = UserFactory()
        diagnostic = DiagnosticFactory()
        Diagnostic.history.filter(id=diagnostic.id).update(history_user=user)
        Diagnostic.objects.filter(id=diagnostic.id).update(creation_user=None)

        call_command("diagnostic_fill_creation_user_and_source", field="creation_user", apply=True)

        diagnostic.refresh_from_db()
        self.assertEqual(diagnostic.creation_user, user)

    def test_fill_creation_source(self):
        diagnostic_mtm = DiagnosticFactory(creation_mtm_source="newsletter")
        diagnostic_api = DiagnosticFactory()
        Diagnostic.history.filter(id=diagnostic_api.id).update(history_change_reason="OAuth2Authentication")
        diagnostic_unknown = DiagnosticFactory()
        Diagnostic.objects.update(creation_source=None)

        call_command("diagnostic_fill_creation_user_and_source", field="creation_source", apply=True)

        for diagnostic, creation_source in [
            (diagnostic_mtm, CreationSource.APP),
            (diagnostic_api, CreationSource.API),
            (diagnostic_unknown, None),
        ]:
            with self.subTest(creation_source=creation_source):
                diagnostic.refresh_from_db()
                self.assertEqual(diagnostic.creation_source, creation_source)

    def test_dry_run_does_not_change_anything(self):
        diagnostic = DiagnosticFactory(creation_mtm_source="newsletter")
        Diagnostic.objects.filter(id=diagnostic.id).update(creation_source=None)

        call_command("diagnostic_fill_creation_user_and_source", field="creation_source")

        diagnostic.refresh_from_db()
        self.assertIsNone(diagnostic.creation_source)


class DiagnosticFillCreationSourceApiOauth2ApplicationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.application_1 = ApplicationFactory()
        cls.application_2 = ApplicationFactory()

    def setUp(self):
        self.user = UserFactory()
        self.diagnostic = DiagnosticFactory(creation_user=self.user, creation_source=CreationSource.API)
        self.creation_date = self.diagnostic.creation_date

    def run_command(self, apply=True):
        call_command(
            "diagnostic_fill_creation_user_and_source", field="creation_source_api_oauth2_application", apply=apply
        )
        self.diagnostic.refresh_from_db()

    def test_fill_from_history(self):
        Diagnostic.history.filter(id=self.diagnostic.id).update(
            history_source_api_oauth2_application=self.application_2
        )

        self.run_command()

        self.assertEqual(self.diagnostic.creation_source_api_oauth2_application, self.application_2)

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

        self.assertEqual(self.diagnostic.creation_source_api_oauth2_application, self.application_1)

    def test_fill_from_only_application_used(self):
        # no token valid at creation date, but the user only ever used application_2
        RefreshTokenFactory(
            user=self.user,
            application=self.application_2,
            created=self.creation_date + timedelta(days=10),
            revoked=self.creation_date + timedelta(days=11),
        )

        self.run_command()

        self.assertEqual(self.diagnostic.creation_source_api_oauth2_application, self.application_2)

    def test_not_filled_if_ambiguous(self):
        for application in [self.application_1, self.application_2]:
            RefreshTokenFactory(
                user=self.user, application=application, created=self.creation_date - timedelta(days=1)
            )

        self.run_command()

        self.assertIsNone(self.diagnostic.creation_source_api_oauth2_application)

    def test_not_filled_if_not_api(self):
        Diagnostic.objects.filter(id=self.diagnostic.id).update(creation_source=CreationSource.APP)
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command()

        self.assertIsNone(self.diagnostic.creation_source_api_oauth2_application)

    def test_dry_run_does_not_change_anything(self):
        RefreshTokenFactory(
            user=self.user, application=self.application_1, created=self.creation_date - timedelta(days=1)
        )

        self.run_command(apply=False)

        self.assertIsNone(self.diagnostic.creation_source_api_oauth2_application)


class DiagnosticFillHistorySourceTest(TestCase):
    def setUp(self):
        self.creator = UserFactory()
        self.application = ApplicationFactory()
        self.diagnostic = DiagnosticFactory()
        # an API update (old row: no history_source, no application)
        self.diagnostic.save()
        Diagnostic.objects.filter(id=self.diagnostic.id).update(
            creation_user=self.creator,
            creation_source=CreationSource.API,
            creation_source_api_oauth2_application=self.application,
        )
        self.history_row = Diagnostic.history.filter(id=self.diagnostic.id).latest("history_date")
        Diagnostic.history.filter(history_id=self.history_row.history_id).update(
            history_change_reason="OAuth2Authentication",
            history_user=self.creator,
            history_source=None,
            history_source_api_oauth2_application=None,
        )

    def run_command(self, apply=True):
        call_command("diagnostic_fill_creation_user_and_source", field="history_source", apply=apply)
        self.history_row.refresh_from_db()

    def test_fill_history_source_and_application_from_creation(self):
        self.run_command()

        self.assertEqual(self.history_row.history_source, CreationSource.API)
        self.assertEqual(self.history_row.history_source_api_oauth2_application, self.application)

    def test_fill_application_from_tokens_if_other_user(self):
        other_user = UserFactory()
        other_application = ApplicationFactory()
        Diagnostic.history.filter(history_id=self.history_row.history_id).update(history_user=other_user)
        AccessTokenFactory(
            user=other_user,
            application=other_application,
            created=self.history_row.history_date - timedelta(minutes=10),
            expires=self.history_row.history_date + timedelta(minutes=50),
        )

        self.run_command()

        self.assertEqual(self.history_row.history_source_api_oauth2_application, other_application)

    def test_application_stays_empty_if_unknown(self):
        Diagnostic.history.filter(history_id=self.history_row.history_id).update(history_user=UserFactory())

        self.run_command()

        self.assertEqual(self.history_row.history_source, CreationSource.API)
        self.assertIsNone(self.history_row.history_source_api_oauth2_application)

    def test_does_not_change_filled_rows(self):
        other_application = ApplicationFactory()
        Diagnostic.history.filter(history_id=self.history_row.history_id).update(
            history_source=CreationSource.API, history_source_api_oauth2_application=other_application
        )

        self.run_command()

        self.assertEqual(self.history_row.history_source_api_oauth2_application, other_application)

    def test_ignores_non_api_rows(self):
        Diagnostic.history.filter(history_id=self.history_row.history_id).update(
            history_change_reason="SessionAuthentication"
        )

        self.run_command()

        self.assertIsNone(self.history_row.history_source)
        self.assertIsNone(self.history_row.history_source_api_oauth2_application)

    def test_dry_run_does_not_change_anything(self):
        self.run_command(apply=False)

        self.assertIsNone(self.history_row.history_source)
        self.assertIsNone(self.history_row.history_source_api_oauth2_application)
