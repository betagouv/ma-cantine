import factory
from data.models import ReservationExpe
from .canteen import CanteenFactory


class ReservationExpeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReservationExpe

    canteen = factory.SubFactory(CanteenFactory)
    leader_email = factory.Faker("email")
    satisfaction_t0 = factory.Faker("random_int", min=0, max=5)
