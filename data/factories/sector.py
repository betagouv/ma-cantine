import factory

from data.models import SectorM2M


class SectorM2MFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectorM2M

    name = factory.Faker("text", max_nb_chars=20)
