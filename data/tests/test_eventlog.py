from unittest import mock

from django.contrib.auth.models import AnonymousUser, Permission
from django.db import transaction
from django.test import TestCase

from data.admin.eventlog import EventLogNameListFilter
from data.factories import EventLogFactory, UserFactory
from data.models import EventLog, ImportType


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


class EventLogAdminNameListFilterTest(TestCase):
    url = "/admin/data/eventlog/"

    def setUp(self):
        # staff but not superuser: superusers need a verified OTP device to access the admin
        staff_user = UserFactory(is_staff=True)
        staff_user.user_permissions.add(Permission.objects.get(codename="view_eventlog"))
        self.client.force_login(staff_user)
        EventLogFactory(category=EventLog.Category.IMPORT, name="PURCHASE_SIRET")
        EventLogFactory(category=EventLog.Category.TASK, name="macantine.tasks.update_user_data")
        EventLogFactory(category=EventLog.Category.TASK, name="macantine.tasks.update_brevo_contacts")
        EventLogFactory(category=EventLog.Category.TASK, name="macantine.tasks.update_brevo_contacts")

    def get_name_filter(self, response):
        # filters without output (no lookups) are not in filter_specs
        return next(
            (spec for spec in response.context["cl"].filter_specs if isinstance(spec, EventLogNameListFilter)), None
        )

    def test_hidden_without_category(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.get_name_filter(response))

    def test_import_category_lists_import_types(self):
        response = self.client.get(self.url, {"category__exact": EventLog.Category.IMPORT})

        self.assertEqual(self.get_name_filter(response).lookup_choices, ImportType.choices)

    def test_other_category_lists_its_distinct_names(self):
        response = self.client.get(self.url, {"category__exact": EventLog.Category.TASK})

        self.assertEqual(
            [value for value, _ in self.get_name_filter(response).lookup_choices],
            ["macantine.tasks.update_brevo_contacts", "macantine.tasks.update_user_data"],
        )

    def test_filters_by_name(self):
        response = self.client.get(
            self.url, {"category__exact": EventLog.Category.TASK, "name": "macantine.tasks.update_brevo_contacts"}
        )

        self.assertEqual(response.context["cl"].result_count, 2)
