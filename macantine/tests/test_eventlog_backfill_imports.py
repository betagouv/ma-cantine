import datetime

from django.core.management import CommandError, call_command
from django.test import TestCase
from django.utils import timezone

from data.factories import CanteenFactory, DiagnosticFactory, PurchaseFactory, UserFactory
from data.models import EventLog, ImportType, Purchase
from data.models.creation_source import CreationSource

BEFORE = "2026-10-20T00:00"
DATE = timezone.make_aware(datetime.datetime(2025, 3, 1, 10, 0))


def run_command(source, apply=True, before=BEFORE):
    call_command("eventlog_backfill_imports", before=before, source=source, apply=apply)


def create_imported_purchases(user, file_digest, creation_date, count, canteen=None):
    """Without canteen: each purchase is for a different canteen"""
    extra = {"canteen": canteen} if canteen else {}
    purchases = PurchaseFactory.create_batch(
        count, creation_user=user, creation_source=CreationSource.IMPORT, import_source=file_digest, **extra
    )
    Purchase.objects.filter(id__in=[p.id for p in purchases]).update(creation_date=creation_date)
    return purchases


def set_import_history(obj, user, reason, date):
    """
    Make obj have a single history row, as if written by a past import
    (CanteenFactory mutes post_save, so no history is created on creation: bulk_history_create writes it directly)
    """
    model = type(obj)
    model.history.model.objects.filter(id=obj.id).delete()
    model.history.bulk_history_create([obj], default_user=user, default_change_reason=reason, default_date=date)


class EventLogBackfillImportsPurchaseTest(TestCase):
    def setUp(self):
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.date_2 = timezone.make_aware(datetime.datetime(2026, 1, 15, 9, 30))
        self.canteen = CanteenFactory()
        create_imported_purchases(self.user_1, "digest_1", DATE, 3, canteen=self.canteen)
        create_imported_purchases(self.user_2, "digest_2", self.date_2, 2)

    def test_one_event_log_per_file_digest(self):
        run_command("purchase")

        self.assertEqual(EventLog.objects.count(), 2)
        event_log_1 = EventLog.objects.get(data__file_digest="digest_1")
        self.assertEqual(event_log_1.category, EventLog.Category.IMPORT)
        self.assertEqual(event_log_1.status, EventLog.Status.SUCCESS)
        self.assertEqual(event_log_1.name, ImportType.PURCHASE)
        self.assertEqual(event_log_1.user, self.user_1)
        self.assertEqual(event_log_1.creation_date, DATE)
        self.assertEqual(
            event_log_1.data,
            {
                "message": None,
                "count": 3,
                "seconds": None,
                "backfilled": True,
                "source": "purchase",
                "import_type_uncertain": True,
                "file_digest": "digest_1",
            },
        )
        event_log_2 = EventLog.objects.get(data__file_digest="digest_2")
        self.assertEqual(event_log_2.user, self.user_2)
        self.assertEqual(event_log_2.data["count"], 2)

    def test_canteen_only_if_single_canteen(self):
        run_command("purchase")

        self.assertEqual(EventLog.objects.get(data__file_digest="digest_1").canteen, self.canteen)  # 1 canteen
        self.assertIsNone(EventLog.objects.get(data__file_digest="digest_2").canteen)  # 2 canteens

    def test_only_before_date(self):
        run_command("purchase", before="2026-01-01T00:00")

        self.assertEqual(list(EventLog.objects.values_list("data__file_digest", flat=True)), ["digest_1"])

    def test_ignores_non_imported_purchases(self):
        PurchaseFactory(creation_user=self.user_1, creation_source=CreationSource.APP, import_source=None)
        PurchaseFactory(creation_user=self.user_1, creation_source=CreationSource.API, import_source="digest_api")
        PurchaseFactory(creation_user=self.user_1, creation_source=CreationSource.IMPORT, import_source=None)

        run_command("purchase")

        self.assertEqual(EventLog.objects.count(), 2)

    def test_counts_soft_deleted_purchases(self):
        Purchase.objects.filter(import_source="digest_1").first().delete()  # soft delete

        run_command("purchase")

        self.assertEqual(EventLog.objects.get(data__file_digest="digest_1").data["count"], 3)


class EventLogBackfillImportsHistoryTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_one_event_log_per_import(self):
        # 2 imports of the same user & view, 1 hour apart, 2 canteens each
        for date in [DATE, DATE + datetime.timedelta(hours=1)]:
            for seconds in [0, 1]:
                canteen = CanteenFactory()
                reason = "Mass CSV import. CanteensUpdateImportView"
                set_import_history(canteen, self.user, reason, date + datetime.timedelta(seconds=seconds))

        run_command("history")

        self.assertEqual(EventLog.objects.count(), 2)
        event_log = EventLog.objects.order_by("creation_date").first()
        self.assertEqual(event_log.category, EventLog.Category.IMPORT)
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertEqual(event_log.name, ImportType.CANTEEN_UPDATE)
        self.assertEqual(event_log.user, self.user)
        self.assertEqual(event_log.creation_date, DATE)
        self.assertIsNone(event_log.canteen)  # 2 canteens
        self.assertEqual(
            event_log.data,
            {
                "message": None,
                "count": 2,
                "seconds": None,
                "backfilled": True,
                "source": "history",
                "import_type_uncertain": False,
                "view": "CanteensUpdateImportView",
            },
        )

    def test_canteen_if_single_canteen(self):
        canteen = CanteenFactory()
        set_import_history(canteen, self.user, "Mass CSV import. CanteensManagersImportView", DATE)

        run_command("history")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.name, ImportType.CANTEEN_MANAGERS)
        self.assertEqual(event_log.canteen, canteen)

    def test_old_diagnostic_import_rows_of_both_models_are_grouped(self):
        # old simple diagnostic import: canteen creation + diagnostic, in the same request
        for index in range(3):
            canteen = CanteenFactory()
            diagnostic = DiagnosticFactory(canteen=canteen)
            date = DATE + datetime.timedelta(seconds=index)
            reason = "Mass CSV import - canteen creation. ImportSimpleDiagnosticsView"
            set_import_history(canteen, self.user, reason, date)
            set_import_history(diagnostic, self.user, "Mass CSV import. ImportSimpleDiagnosticsView", date)

        run_command("history")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.name, ImportType.DIAGNOSTIC_SIMPLE_SIRET)
        self.assertEqual(event_log.data["count"], 3)  # diagnostics
        self.assertFalse(event_log.data["import_type_uncertain"])

    def test_current_simple_diagnostic_import_type_is_uncertain(self):
        diagnostic = DiagnosticFactory()
        set_import_history(diagnostic, self.user, "Mass CSV import. DiagnosticsSimpleImportView", DATE)

        run_command("history")

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.name, ImportType.DIAGNOSTIC_SIMPLE_SIRET)
        self.assertTrue(event_log.data["import_type_uncertain"])
        self.assertEqual(event_log.canteen, diagnostic.canteen)

    def test_different_users_are_different_imports(self):
        for user in [self.user, UserFactory()]:
            set_import_history(CanteenFactory(), user, "Mass CSV import. CanteensUpdateImportView", DATE)

        run_command("history")

        self.assertEqual(EventLog.objects.count(), 2)

    def test_ignores_other_history_rows(self):
        set_import_history(CanteenFactory(), self.user, "Données de localisation MAJ par bot", DATE)
        set_import_history(CanteenFactory(), self.user, "Mass CSV import. UnknownImportView", DATE)
        CanteenFactory()  # no history

        run_command("history")

        self.assertFalse(EventLog.objects.exists())

    def test_only_before_date(self):
        set_import_history(CanteenFactory(), self.user, "Mass CSV import. CanteensUpdateImportView", DATE)

        run_command("history", before="2025-01-01T00:00")

        self.assertFalse(EventLog.objects.exists())

    def test_hard_deleted_canteen_is_not_linked(self):
        canteen = CanteenFactory()
        set_import_history(canteen, self.user, "Mass CSV import. CanteensUpdateImportView", DATE)
        canteen.hard_delete()  # history kept

        run_command("history")

        event_log = EventLog.objects.get()
        self.assertIsNone(event_log.canteen)
        self.assertEqual(event_log.data["count"], 1)


class EventLogBackfillImportsCommandTest(TestCase):
    def setUp(self):
        user = UserFactory()
        create_imported_purchases(user, "digest_1", DATE, 2)
        set_import_history(CanteenFactory(), user, "Mass CSV import. CanteensUpdateImportView", DATE)

    def test_only_the_given_source(self):
        run_command("history")

        self.assertEqual(list(EventLog.objects.values_list("data__source", flat=True)), ["history"])

    def test_dry_run_creates_nothing(self):
        run_command("history", apply=False)

        self.assertFalse(EventLog.objects.exists())

    def test_source_is_required(self):
        with self.assertRaises(CommandError):
            call_command("eventlog_backfill_imports", before=BEFORE)
