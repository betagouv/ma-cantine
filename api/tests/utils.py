import filecmp
import functools
from datetime import timedelta

from django.utils import timezone

from data.factories import UserFactory
from data.models import ImportFailure


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
    token = user.oauth2_provider_accesstoken.create(expires=expiration, token="token", scope=scope)
    return (user, token)


def assert_import_failure_created(self, user, type, file_path):
    self.assertTrue(ImportFailure.objects.count() >= 1)
    self.assertEqual(ImportFailure.objects.first().user, user)
    self.assertEqual(ImportFailure.objects.first().import_type, type)
    self.assertTrue(filecmp.cmp(file_path, ImportFailure.objects.last().file.path, shallow=False))
