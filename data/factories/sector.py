import factory

from data.models import Sector, SectorM2M


class SectorM2MFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SectorM2M

    name = factory.Iterator([label for value, label in Sector.choices])
