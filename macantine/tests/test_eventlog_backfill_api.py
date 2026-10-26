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


def event_logs():
    """The EventLog created by the backfill (without the COMMAND one of the backfill command run itself)"""
    return EventLog.objects.exclude(category=EventLog.Category.COMMAND)


def run_command(apply=True, before=BEFORE):
    call_command("eventlog_backfill_api", before=before, apply=apply)


def set_api_creation(obj, user, application, date=DATE):
    """Purchase & WasteMeasurement: creation_source = API (with or without an application)"""
    type(obj)._base_manager.filter(id=obj.id).update(
        creation_source=CreationSource.API,
        creation_user=user,
        creation_source_api_oauth2_application=application,
        creation_date=date,
    )


def create_api_history(obj, user, history_type, date=DATE, application=None, reason="OAuth2Authentication"):
    """A history row ("+" creation or "~" update), as written by an API view"""
    model = type(obj)
    model.history.bulk_history_create([obj], default_user=user, default_change_reason=reason, default_date=date)
    model.history.model.objects.filter(id=obj.id, history_date=date).update(
        history_type=history_type,
        history_source=CreationSource.API if application else None,
        history_source_api_oauth2_application=application,
    )


def create_api_update_history(obj, user, date=DATE, application=None, reason="OAuth2Authentication"):
    create_api_history(obj, user, "~", date=date, application=application, reason=reason)


class EventLogBackfillApiTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.application = ApplicationFactory()
        self.canteen = CanteenFactory()

    def test_creation_from_history(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        create_api_history(diagnostic, self.user, "+", application=self.application)

        run_command()

        event_log = event_logs().get()
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
                "source": "history",
            },
        )

    def test_creations_of_each_model(self):
        create_api_history(self.canteen, self.user, "+", application=self.application)
        create_api_history(DiagnosticFactory(canteen=self.canteen), self.user, "+", application=self.application)
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, self.application)
        set_api_creation(WasteMeasurementFactory(canteen=self.canteen), self.user, self.application)

        run_command()

        self.assertEqual(
            sorted(event_logs().values_list("name", flat=True)),
            [
                "POST /api/v1/canteens/",
                "POST /api/v1/canteens/{canteen_pk}/diagnostics/",
                "POST /api/v1/canteens/{canteen_pk}/purchases/",
                "POST /api/v1/canteens/{canteen_pk}/wasteMeasurements/",
            ],
        )
        self.assertEqual(event_logs().get(name="POST /api/v1/canteens/").canteen, self.canteen)
        self.assertEqual(
            event_logs().get(name="POST /api/v1/canteens/{canteen_pk}/purchases/").data["source"], "creation"
        )

    def test_ignores_object_creations_without_application(self):
        # creation_source = API alone is not reliable (API by default in the views)
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, None)
        set_api_creation(WasteMeasurementFactory(canteen=self.canteen), self.user, None)

        run_command()

        self.assertFalse(event_logs().exists())

    def test_ignores_canteen_and_diagnostic_creation_source(self):
        # Canteen & Diagnostic creations only come from the history
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        Diagnostic.objects.filter(id=diagnostic.id).update(
            creation_source=CreationSource.API, creation_source_api_oauth2_application=self.application
        )

        run_command()

        self.assertFalse(event_logs().exists())

    def test_ignores_diagnostics_generated_from_a_groupe(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        Diagnostic.all_objects.filter(id=diagnostic.id).update(generated_from_groupe_diagnostic=True)
        diagnostic.refresh_from_db()
        create_api_history(diagnostic, self.user, "+")
        create_api_update_history(diagnostic, self.user, date=DATE + datetime.timedelta(days=1))

        run_command()

        self.assertFalse(event_logs().exists())

    def test_ignores_non_api_creations(self):
        purchase = PurchaseFactory(canteen=self.canteen)
        Purchase.objects.filter(id=purchase.id).update(
            creation_source=CreationSource.APP, creation_source_api_oauth2_application=self.application
        )
        create_api_history(DiagnosticFactory(canteen=self.canteen), self.user, "+", reason="SessionAuthentication")

        run_command()

        self.assertFalse(event_logs().exists())

    def test_updates_from_history(self):
        diagnostic = DiagnosticFactory(canteen=self.canteen)
        create_api_update_history(diagnostic, self.user)  # old row: no application
        create_api_update_history(
            diagnostic, self.user, date=DATE + datetime.timedelta(days=1), application=self.application
        )

        run_command()

        api_event_logs = event_logs().order_by("creation_date")
        self.assertEqual(api_event_logs.count(), 2)
        self.assertEqual(api_event_logs[0].name, "PATCH /api/v1/canteens/{canteen_pk}/diagnostics/{id}")
        self.assertEqual(
            api_event_logs[0].data["path"], f"/api/v1/canteens/{self.canteen.id}/diagnostics/{diagnostic.id}"
        )
        self.assertEqual(api_event_logs[0].data["status_code"], 200)
        self.assertEqual(api_event_logs[0].data["source"], "history")
        self.assertEqual(api_event_logs[0].user, self.user)
        self.assertIsNone(api_event_logs[0].api_oauth2_application)
        self.assertEqual(api_event_logs[1].api_oauth2_application, self.application)

    def test_canteen_update_from_history(self):
        create_api_update_history(self.canteen, self.user)

        run_command()

        event_log = event_logs().get()
        self.assertEqual(event_log.name, "PATCH /api/v1/canteens/{id}")
        self.assertEqual(event_log.data["path"], f"/api/v1/canteens/{self.canteen.id}")
        self.assertEqual(event_log.canteen, self.canteen)

    def test_ignores_non_api_history(self):
        create_api_update_history(self.canteen, self.user, reason="SessionAuthentication")
        create_api_update_history(self.canteen, self.user, reason="Mass CSV import. CanteensUpdateImportView")

        run_command()

        self.assertFalse(event_logs().exists())

    def test_only_before_date(self):
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, self.application)
        create_api_update_history(self.canteen, self.user)

        run_command(before="2025-01-01T00:00")

        self.assertFalse(event_logs().exists())

    def test_dry_run_creates_nothing(self):
        set_api_creation(PurchaseFactory(canteen=self.canteen), self.user, self.application)

        run_command(apply=False)

        self.assertFalse(event_logs().exists())

    def test_hard_deleted_canteen_is_not_linked(self):
        create_api_update_history(self.canteen, self.user)
        Canteen.all_objects.get(id=self.canteen.id).hard_delete()

        run_command()

        self.assertIsNone(event_logs().get().canteen)
