from django.core.management import call_command
from django.test import TestCase

from data.factories import DiagnosticFactory, UserFactory
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
