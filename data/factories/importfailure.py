import factory

from data.models import ImportFailure

from .user import UserFactory


class ImportFailureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImportFailure

    details = factory.Faker("paragraph")
    user = factory.SubFactory(UserFactory)
