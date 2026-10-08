from datetime import timedelta

import factory
from django.utils import timezone
from oauth2_provider.models import get_access_token_model, get_application_model, get_refresh_token_model

from .user import UserFactory

Application = get_application_model()


class ApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Application

    name = factory.Sequence(lambda n: f"Logiciel {n}")
    user = factory.SubFactory(UserFactory)
    client_type = Application.CLIENT_CONFIDENTIAL
    authorization_grant_type = Application.GRANT_AUTHORIZATION_CODE
    redirect_uris = "https://example.com"


class AccessTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_access_token_model()

    user = factory.SubFactory(UserFactory)
    application = factory.SubFactory(ApplicationFactory)
    token = factory.Sequence(lambda n: f"access-token-{n}")
    expires = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=1))


class RefreshTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_refresh_token_model()

    user = factory.SubFactory(UserFactory)
    application = factory.SubFactory(ApplicationFactory)
    token = factory.Sequence(lambda n: f"refresh-token-{n}")
