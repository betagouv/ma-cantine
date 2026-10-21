import datetime

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from data.factories import (
    ApplicationFactory,
    CanteenFactory,
    DiagnosticFactory,
    PurchaseFactory,
    UserFactory,
    WasteMeasurementFactory,
)
from data.models import Canteen, Diagnostic, EventLog, Purchase
from data.models.creation_source import CreationSource

BEFORE = "2026-10-20T00:00"
DATE = timezone.make_aware(datetime.datetime(2025, 3, 1, 10, 0))


def run_command(apply=True, before=BEFORE):
    call_command("eventlog_backfill_api", before=before, apply=apply)


def set_api_creation(obj, user, application, date=DATE):
    type(obj)._base_manager.filter(id=obj.id).update(
        creation_source=CreationSource.API,
        creation_user=user,
        creation_source_api_oauth2_application=application,
        creation_date=date,
    )


def create_api_update_history(obj, user, date=DATE, application=None, reason="OAuth2Authentication"):
    """An update ("~") history row, as written by an API view"""
    model = type(obj)
    model.history.bulk_history_create([obj], default_user=user, default_change_reason=reason, default_date=date)
    model.history.model.objects.filter(id=obj.id, history_date=date).update(
        history_type="~",
        history_source=CreationSource.API if application else None,
        history_source_api_oauth2_application=application,
    )


class EventLogBackfillApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.canteen = CanteenFactory()

    def test_creations(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        set_api_creation(diagnostic, self.user, self.application)

        run_command()

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.category, EventLog.Category.API)
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertEqual(event_log.name, "POST /api/v1/canteens/{canteen_pk}/diagnostics/")
        self.assertEqual(event_log.user, self.user)
        self.assertEqual(event_log.api_oauth2_application, self.application)
        self.assertEqual(event_log.canteen, self.canteen)
        self.assertEqual(event_log.creation_date, DATE)
        self.assertEqual(
            event_log.data,
            {
                "method": "POST",
                "path": f"/api/v1/canteens/{self.canteen.id}/diagnostics/",
                "status_code": 201,
                "seconds": None,
                "message": None,
                "backfilled": True,
                "source": "creation",
            },
        )

    def test_creations_of_each_model(self):
        set_api_creation(self.canteen, self.user, self.application)
        set_api_creation(DiagnosticFactory(canteen=self.canteen), self.user, self.application)
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, self.application)
        set_api_creation(WasteMeasurementFactory(canteen=self.canteen), self.user, self.application)

        run_command()

        self.assertEqual(
            sorted(EventLog.objects.values_list("name", flat=True)),
            [
                "POST /api/v1/canteens/",
                "POST /api/v1/canteens/{canteen_pk}/diagnostics/",
                "POST /api/v1/canteens/{canteen_pk}/purchases/",
                "POST /api/v1/canteens/{canteen_pk}/wasteMeasurements/",
            ],
        )
        self.assertEqual(EventLog.objects.get(name="POST /api/v1/canteens/").canteen, self.canteen)

    def test_ignores_purchase_and_waste_measurement_creations_without_application(self):
        # creation_source = API alone is not reliable (API by default in the views)
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, None)
        set_api_creation(WasteMeasurementFactory(canteen=self.canteen), self.user, None)

        run_command()

        self.assertFalse(EventLog.objects.exists())

    def test_canteen_and_diagnostic_creations_without_application(self):
        set_api_creation(self.canteen, self.user, None)
        set_api_creation(DiagnosticFactory(canteen=self.canteen), self.user, None)

        run_command()

        self.assertEqual(EventLog.objects.count(), 2)
        self.assertFalse(EventLog.objects.exclude(api_oauth2_application__isnull=True).exists())

    def test_ignores_non_api_creations(self):
        purchase = PurchaseFactory(canteen=self.canteen)
        Purchase.objects.filter(id=purchase.id).update(creation_source=CreationSource.APP)
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        Diagnostic.objects.filter(id=diagnostic.id).update(creation_source=CreationSource.IMPORT)

        run_command()

        self.assertFalse(EventLog.objects.exists())

    def test_updates_from_history(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        create_api_update_history(diagnostic, self.user)  # old row: no application
        create_api_update_history(
            diagnostic, self.user, date=DATE + datetime.timedelta(days=1), application=self.application
        )

        run_command()

        event_logs = EventLog.objects.order_by("creation_date")
        self.assertEqual(event_logs.count(), 2)
        self.assertEqual(event_logs[0].name, "PATCH /api/v1/canteens/{canteen_pk}/diagnostics/{id}")
        self.assertEqual(event_logs[0].data["path"], f"/api/v1/canteens/{self.canteen.id}/diagnostics/{diagnostic.id}")
        self.assertEqual(event_logs[0].data["status_code"], 200)
        self.assertEqual(event_logs[0].data["source"], "history")
        self.assertEqual(event_logs[0].user, self.user)
        self.assertIsNone(event_logs[0].api_oauth2_application)
        self.assertEqual(event_logs[1].api_oauth2_application, self.application)

    def test_canteen_update_from_history(self):
        create_api_update_history(self.canteen, self.user)

        run_command()

        event_log = EventLog.objects.get()
        self.assertEqual(event_log.name, "PATCH /api/v1/canteens/{id}")
        self.assertEqual(event_log.data["path"], f"/api/v1/canteens/{self.canteen.id}")
        self.assertEqual(event_log.canteen, self.canteen)

    def test_ignores_non_api_history(self):
        create_api_update_history(self.canteen, self.user, reason="SessionAuthentication")
        create_api_update_history(self.canteen, self.user, reason="Mass CSV import. CanteensUpdateImportView")

        run_command()

        self.assertFalse(EventLog.objects.exists())

    def test_only_before_date(self):
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, self.application)
        create_api_update_history(self.canteen, self.user)

        run_command(before="2025-01-01T00:00")

        self.assertFalse(EventLog.objects.exists())

    def test_dry_run_creates_nothing(self):
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, self.application)

        run_command(apply=False)

        self.assertFalse(EventLog.objects.exists())

    def test_hard_deleted_canteen_is_not_linked(self):
        create_api_update_history(self.canteen, self.user)
        Canteen.all_objects.get(id=self.canteen.id).hard_delete()

        run_command()

        self.assertIsNone(EventLog.objects.get().canteen)
