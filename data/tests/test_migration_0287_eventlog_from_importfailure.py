import datetime
import importlib

from django.apps import apps
from django.test import TestCase
from django.utils import timezone

from data.factories import ImportFailureFactory, UserFactory
from data.models import EventLog, ImportFailure, ImportType

migration = importlib.import_module("data.migrations.0287_eventlog_from_importfailure")


class EventLogFromImportFailureMigrationTest(TestCase):
    def test_copy_import_failures(self):
        user = UserFactory()
        import_failure = ImportFailureFactory(user=user, import_type=ImportType.PURCHASE, details="Fichier invalide")
        creation_date = timezone.make_aware(datetime.datetime(2024, 3, 1, 10, 0))
        ImportFailure.objects.filter(id=import_failure.id).update(creation_date=creation_date)
        ImportFailureFactory(user=None, import_type=None, details=None)

        migration.copy_import_failures_to_event_logs(apps, None)

        self.assertEqual(EventLog.objects.count(), 2)
        event_log = EventLog.objects.get(data__import_failure_id=import_failure.id)
        self.assertEqual(event_log.category, EventLog.Category.IMPORT)
        self.assertEqual(event_log.status, EventLog.Status.FAILURE)
        self.assertEqual(event_log.name, ImportType.PURCHASE)
        self.assertEqual(event_log.user, user)
        self.assertEqual(
            event_log.data,
            {"message": "Fichier invalide", "count": None, "seconds": None, "import_failure_id": import_failure.id},
        )
        self.assertEqual(event_log.creation_date, creation_date)

        event_log_without_type = EventLog.objects.exclude(id=event_log.id).get()
        self.assertEqual(event_log_without_type.name, "UNKNOWN")
        self.assertIsNone(event_log_without_type.user)

    def test_copy_is_idempotent(self):
        ImportFailureFactory.create_batch(3)

        migration.copy_import_failures_to_event_logs(apps, None)
        migration.copy_import_failures_to_event_logs(apps, None)

        self.assertEqual(EventLog.objects.count(), 3)

    def test_copy_in_batches(self):
        ImportFailureFactory.create_batch(5)

        original_batch_size = migration.BATCH_SIZE
        migration.BATCH_SIZE = 2
        try:
            migration.copy_import_failures_to_event_logs(apps, None)
        finally:
            migration.BATCH_SIZE = original_batch_size

        self.assertEqual(EventLog.objects.count(), 5)
        self.assertEqual(
            sorted(EventLog.objects.values_list("data__import_failure_id", flat=True)),
            sorted(ImportFailure.objects.values_list("id", flat=True)),
        )

    def test_reverse_deletes_only_copied_event_logs(self):
        ImportFailureFactory.create_batch(2)
        migration.copy_import_failures_to_event_logs(apps, None)
        EventLog.log(EventLog.Category.IMPORT, ImportType.PURCHASE, EventLog.Status.SUCCESS)

        migration.delete_copied_event_logs(apps, None)

        self.assertEqual(EventLog.objects.count(), 1)
        self.assertEqual(ImportFailure.objects.count(), 2)
