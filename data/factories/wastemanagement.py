# import random
import factory
from data.models import WasteMeasurement
from .canteen import CanteenFactory


class WasteMeasurementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WasteMeasurement

    canteen = factory.SubFactory(CanteenFactory)
    period_start_date = factory.Faker("date")
    period_end_date = factory.Faker("date")
    meal_count = factory.Faker("random_int", min=0, max=2000)