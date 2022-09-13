import factory
from data.models import Partner


class PartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Partner

    name = factory.Faker("text", max_nb_chars=20)
    short_description = factory.Faker("catch_phrase")
    long_description = factory.Faker("paragraph")
