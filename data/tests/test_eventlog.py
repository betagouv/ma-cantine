from unittest import mock

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from freezegun import freeze_time

from data.factories import EventLogFactory, UserFactory
from data.models import EventLog


class EventLogMessageShortTest(TestCase):
    def test_message_short(self):
        self.assertEqual(EventLogFactory(data={"message": "Erreur"}).message_short, "Erreur")
        self.assertEqual(EventLogFactory(data={"message": "x" * 100}).message_short, "x" * 75 + "...")
        self.assertIsNone(EventLogFactory(data={"count": 3}).message_short)
        self.assertIsNone(EventLogFactory(data={}).message_short)


class EventLogLogTest(TestCase):
    def test_log_creates_event(self):
        user = UserFactory()

        event_log = EventLog.log(
            EventLog.Category.IMPORT, "PURCHASE_SIRET", EventLog.Status.SUCCESS, user=user, data={"count": 3}
        )

        self.assertEqual(EventLog.objects.count(), 1)
        self.assertEqual(event_log.category, EventLog.Category.IMPORT)
        self.assertEqual(event_log.name, "PURCHASE_SIRET")
        self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
        self.assertEqual(event_log.user, user)
        self.assertEqual(event_log.data, {"count": 3})

    def test_log_without_user_or_data(self):
        event_log = EventLog.log(EventLog.Category.TASK, "macantine.tasks.update_user_data", EventLog.Status.SUCCESS)

        self.assertIsNone(event_log.user)
        self.assertEqual(event_log.data, {})

    def test_log_anonymous_user(self):
        event_log = EventLog.log(
            EventLog.Category.API, "POST api/v1/canteens/", EventLog.Status.FAILURE, user=AnonymousUser()
        )

        self.assertIsNone(event_log.user)

    def test_log_never_raises(self):
        with mock.patch.object(EventLog.objects, "create", side_effect=Exception("DB down")):
            with mock.patch("data.models.eventlog.logger") as mock_logger:
                event_log = EventLog.log(EventLog.Category.IMPORT, "PURCHASE_SIRET", EventLog.Status.SUCCESS)

        self.assertIsNone(event_log)
        mock_logger.exception.assert_called_once()
        self.assertEqual(EventLog.objects.count(), 0)

    def test_log_failure_does_not_break_outer_transaction(self):
        with transaction.atomic():
            # invalid value for a JSONField: raises at insert time
            EventLog.log(EventLog.Category.IMPORT, "PURCHASE_SIRET", EventLog.Status.SUCCESS, data={"value": object()})
            EventLog.log(EventLog.Category.IMPORT, "PURCHASE_SIRET", EventLog.Status.SUCCESS)

        self.assertEqual(EventLog.objects.count(), 1)

    @freeze_time("2026-10-13")
    def test_log_with_file(self):
        file = SimpleUploadedFile("achats.csv", b"siret,description\n", content_type="text/csv")

        event_log = EventLog.log(EventLog.Category.IMPORT, "PURCHASE_SIRET", EventLog.Status.FAILURE, file=file)

        self.assertTrue(event_log.file.name.startswith("event-logs/import/2026/10/13/achats"))
        with event_log.file.open("rb") as stored_file:
            self.assertEqual(stored_file.read(), b"siret,description\n")
        event_log.file.delete()

    def test_log_without_file(self):
        event_log = EventLog.log(EventLog.Category.IMPORT, "PURCHASE_SIRET", EventLog.Status.SUCCESS)

        self.assertFalse(event_log.file)
