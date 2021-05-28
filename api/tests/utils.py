import functools

from data.factories import (
    UserFactory,
)


def authenticate(func):
    @functools.wraps(func)
    def authenticate_and_func(*args, **kwargs):
        authenticate.user = UserFactory.create()
        args[0].client.force_login(user=authenticate.user)
        return func(*args, **kwargs)

    return authenticate_and_func
