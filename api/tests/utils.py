import filecmp
import functools
from data.factories import AccessTokenFactory, UserFactory
from data.models import EventLog, ImportFailure


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_func(*args, **kwargs):
        authenticate.user = UserFactory()
        args[0].client.force_login(user=authenticate.user)
        return func(*args, **kwargs)

    return authenticate_and_func


def get_oauth2_token(scope):
    user = UserFactory()
    access_token = AccessTokenFactory(user=user, application__user=user, scope=scope)
    return (user, access_token)


def assert_import_failure_created(self, user, type, file_path):
    self.assertTrue(ImportFailure.objects.count() >= 1)
    self.assertEqual(ImportFailure.objects.first().user, user)
    self.assertEqual(ImportFailure.objects.first().import_type, type)
    self.assertTrue(filecmp.cmp(file_path, ImportFailure.objects.last().file.path, shallow=False))
    # EventLog
    event_log = EventLog.objects.filter(category=EventLog.Category.IMPORT, status=EventLog.Status.FAILURE).first()
    self.assertIsNotNone(event_log)
    self.assertEqual(event_log.user, user)
    self.assertEqual(event_log.name, type)
    self.assertEqual(set(event_log.data.keys()), {"message", "count", "seconds"})
    self.assertTrue(event_log.data["message"])
    self.assertIsNone(event_log.data["count"])


def assert_import_success_created(self, user, type, count=None):
    """Checks the latest import (some tests run several imports)"""
    self.assertFalse(ImportFailure.objects.exists())
    event_log = EventLog.objects.filter(category=EventLog.Category.IMPORT).order_by("creation_date", "id").last()
    self.assertIsNotNone(event_log)
    self.assertEqual(event_log.status, EventLog.Status.SUCCESS)
    self.assertEqual(event_log.user, user)
    self.assertEqual(event_log.name, type)
    self.assertEqual(set(event_log.data.keys()), {"message", "count", "seconds"})
    self.assertIsNone(event_log.data["message"])
    if count is not None:
        self.assertEqual(event_log.data["count"], count)


def assert_almost_equal(self, value, expected_value):
    # self.assertAlmostEqual(float(value), float(expected_value), places=2)
    # self.assertEqual(int(value), int(expected_value))  # avoid rounding errors
    self.assertAlmostEqual(float(value), float(expected_value), places=0)  # check that the difference is less than 1
