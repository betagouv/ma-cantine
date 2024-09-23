from datetime import datetime, timedelta

import factory

from data.models import WasteMeasurement

from .canteen import CanteenFactory


class WasteMeasurementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WasteMeasurement

    canteen = factory.SubFactory(CanteenFactory)
    period_start_date = factory.Faker("date", end_datetime=datetime.now() - timedelta(days=31))
    period_end_date = factory.Faker(
        "date_between_dates",
        date_start=datetime.now() - timedelta(days=30),
        date_end=datetime.now() - timedelta(days=1),
    )
    meal_count = factory.Faker("random_int", min=0, max=2000)
