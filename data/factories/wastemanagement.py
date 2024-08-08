# import random
import factory
from data.models import WasteMeasurement
from .canteen import CanteenFactory
import zoneinfo


class WasteMeasurementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WasteMeasurement

    canteen = factory.SubFactory(CanteenFactory)
    period_start_date = factory.Faker("date_time", tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
    period_end_date = factory.Faker("date_time", tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
    meal_count = factory.Faker("random_int", min=0, max=2000)
