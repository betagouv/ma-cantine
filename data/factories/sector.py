import factory
from data.models import Sector


class SectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sector

    name = factory.Faker("text", max_nb_chars=20)
    category = factory.Faker("text", max_nb_chars=20)
