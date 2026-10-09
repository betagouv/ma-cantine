import logging
import sys

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from macantine.sentry import before_send


def get_exc_info(exception):
    try:
        raise exception
    except Exception:
        return sys.exc_info()


def get_log_record(module):
    return logging.LogRecord("name", logging.ERROR, f"/path/{module}.py", 1, "message", None, None)


class SentryBeforeSendTest(SimpleTestCase):
    event = {"event_id": "123"}

    def test_logged_exception_from_import_is_filtered_out(self):
        hint = {"exc_info": get_exc_info(ValidationError("x")), "log_record": get_log_record("diagnostic_import")}
        self.assertIsNone(before_send(self.event, hint))

    def test_logged_exception_from_other_module_is_kept(self):
        hint = {"exc_info": get_exc_info(ValidationError("x")), "log_record": get_log_record("other_module")}
        self.assertEqual(before_send(self.event, hint), self.event)

    def test_captured_exception_without_log_record_is_kept(self):
        # e.g. unhandled exception in a view (DjangoIntegration), failed Celery task (CeleryIntegration)
        hint = {"exc_info": get_exc_info(RuntimeError("boom"))}
        self.assertEqual(before_send(self.event, hint), self.event)

    def test_event_without_exception_is_kept(self):
        # e.g. logger.error("...") without exc_info
        hint = {"log_record": get_log_record("other_module")}
        self.assertEqual(before_send(self.event, hint), self.event)
