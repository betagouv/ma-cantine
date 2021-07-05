import factory
from data.models import ManagerInvitation
from .canteen import CanteenFactory


class ManagerInvitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ManagerInvitation

    canteen = factory.SubFactory(CanteenFactory)
    email = factory.Faker("email")
