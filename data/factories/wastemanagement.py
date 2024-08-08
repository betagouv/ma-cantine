# import random
import factory
from data.models import WasteMeasurement
from .canteen import CanteenFactory


class WasteMeasurementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WasteMeasurement

    canteen = factory.SubFactory(CanteenFactory)
