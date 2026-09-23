import filecmp
import functools
import json
import os
from datetime import timedelta

from django.utils import timezone

from common.api.validata import VALIDATA_PROD_API_URL
from data.factories import UserFactory
from data.models import ImportFailure

VALIDATA_RESPONSES_DIR = os.path.join(os.path.dirname(__file__), "files", "canteens", "validata_responses")


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_func(*args, **kwargs):
        authenticate.user = UserFactory()
        args[0].client.force_login(user=authenticate.user)
        return func(*args, **kwargs)

    return authenticate_and_func


def get_oauth2_token(scope):
    today = timezone.now()
    expiration = today + timedelta(hours=1)
    user = UserFactory()
    application = user.oauth2_provider_application.create(
        name="Test Application",
        redirect_uris="http://localhost",
        client_type="confidential",
        authorization_grant_type="password",
    )
    token = user.oauth2_provider_accesstoken.create(
        expires=expiration, token="token", scope=scope, application=application
    )
    return (user, token)


def assert_import_failure_created(self, user, type, file_path):
    self.assertTrue(ImportFailure.objects.count() >= 1)
    self.assertEqual(ImportFailure.objects.first().user, user)
    self.assertEqual(ImportFailure.objects.first().import_type, type)
    self.assertTrue(filecmp.cmp(file_path, ImportFailure.objects.last().file.path, shallow=False))


def mock_validata_response(mock, filename):
    """
    Mock the Validata API call for a given import fixture file, using a
    real response captured from the live API (see api/tests/files/canteens/validata_responses/).
    Avoids CI flakiness caused by depending on the live, third-party Validata service.
    """
    with open(os.path.join(VALIDATA_RESPONSES_DIR, f"{filename}.json")) as f:
        response_json = json.load(f)
    mock.post(VALIDATA_PROD_API_URL, json=response_json, status_code=200)


def assert_almost_equal(self, value, expected_value):
    # self.assertAlmostEqual(float(value), float(expected_value), places=2)
    # self.assertEqual(int(value), int(expected_value))  # avoid rounding errors
    self.assertAlmostEqual(float(value), float(expected_value), places=0)  # check that the difference is less than 1
