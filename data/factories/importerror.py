import factory
from data.models import ImportError
from .user import UserFactory


class ImportErrorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImportError

    details = factory.Faker("paragraph")
    user = factory.SubFactory(UserFactory)
