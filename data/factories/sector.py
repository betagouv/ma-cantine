import factory

from data.models import SectorM2M, Sector


class SectorM2MFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectorM2M

    name = factory.Iterator([label for value, label in Sector.choices])
