import factory
from data.models import PartnerType


class PartnerTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartnerType

    name = factory.Faker("text", max_nb_chars=20)
