import datetime

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from data.factories import PurchaseFactory, UserFactory
from data.models import EventLog, ImportType, Purchase
from data.models.creation_source import CreationSource


def create_imported_purchases(user, file_digest, creation_date, count):
    purchases = PurchaseFactory.create_batch(
        count, creation_user=user, creation_source=CreationSource.IMPORT, import_source=file_digest
    )
    Purchase.objects.filter(id__in=[p.id for p in purchases]).update(creation_date=creation_date)
    return purchases


class EventLogBackfillPurchaseImportsTest(TestCase):
    before = "2026-10-20T00:00"

    def setUp(self):
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.date_1 = timezone.make_aware(datetime.datetime(2025, 3, 1, 10, 0))
        self.date_2 = timezone.make_aware(datetime.datetime(2026, 1, 15, 9, 30))
        create_imported_purchases(self.user_1, "digest_1", self.date_1, 3)
        create_imported_purchases(self.user_2, "digest_2", self.date_2, 2)

    def run_command(self, apply=True, before=None):
        call_command("eventlog_backfill_purchase_imports", before=before or self.before, apply=apply)

    def test_one_event_log_per_file_digest(self):
        self.run_command()

        self.assertEqual(EventLog.objects.count(), 2)
        event_log_1 = EventLog.objects.get(data__file_digest="digest_1")
        self.assertEqual(event_log_1.category, EventLog.Category.IMPORT)
        self.assertEqual(event_log_1.status, EventLog.Status.SUCCESS)
        self.assertEqual(event_log_1.name, ImportType.PURCHASE)
        self.assertEqual(event_log_1.user, self.user_1)
        self.assertEqual(event_log_1.creation_date, self.date_1)
        self.assertEqual(
            event_log_1.data,
            {
                "message": None,
                "count": 3,
                "seconds": None,
                "backfilled": True,
                "file_digest": "digest_1",
                "import_type_uncertain": True,
            },
        )
        event_log_2 = EventLog.objects.get(data__file_digest="digest_2")
        self.assertEqual(event_log_2.user, self.user_2)
        self.assertEqual(event_log_2.data["count"], 2)

    def test_dry_run_creates_nothing(self):
        self.run_command(apply=False)

        self.assertEqual(EventLog.objects.count(), 0)

    def test_is_idempotent(self):
        self.run_command()
        self.run_command()

        self.assertEqual(EventLog.objects.count(), 2)

    def test_only_before_date(self):
        self.run_command(before="2026-01-01T00:00")

        self.assertEqual(list(EventLog.objects.values_list("data__file_digest", flat=True)), ["digest_1"])

    def test_ignores_non_imported_purchases(self):
        PurchaseFactory(creation_user=self.user_1, creation_source=CreationSource.APP, import_source=None)
        PurchaseFactory(creation_user=self.user_1, creation_source=CreationSource.API, import_source="digest_api")
        PurchaseFactory(creation_user=self.user_1, creation_source=CreationSource.IMPORT, import_source=None)

        self.run_command()

        self.assertEqual(EventLog.objects.count(), 2)

    def test_counts_soft_deleted_purchases(self):
        Purchase.objects.filter(import_source="digest_1").first().delete()  # soft delete

        self.run_command()

        self.assertEqual(EventLog.objects.get(data__file_digest="digest_1").data["count"], 3)
