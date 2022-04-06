import factory
from data.models import VegetarianExpe
from .canteen import CanteenFactory


class VegetarianExpeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VegetarianExpe

    canteen = factory.SubFactory(CanteenFactory)
    satisfaction_guests_t0 = factory.Faker("random_int", min=0, max=5)
    satisfaction_staff_t0 = factory.Faker("random_int", min=0, max=5)
