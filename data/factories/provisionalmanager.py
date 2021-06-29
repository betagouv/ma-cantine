import factory
from data.models import ProvisionalManager
from .canteen import CanteenFactory


class ProvisionalManagerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProvisionalManager

    canteen = factory.SubFactory(CanteenFactory)
    email = factory.Faker("email")
