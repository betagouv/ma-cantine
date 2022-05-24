import functools
from datetime import timedelta
from django.utils import timezone

from data.factories import UserFactory


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_func(*args, **kwargs):
        authenticate.user = UserFactory.create()
        args[0].client.force_login(user=authenticate.user)
        return func(*args, **kwargs)

    return authenticate_and_func


def get_oauth2_token(scope):
    today = timezone.now()
    expiration = today + timedelta(hours=1)
    user = UserFactory.create()
    token = user.oauth2_provider_accesstoken.create(expires=expiration, token="token", scope=scope)
    return (user, token)
