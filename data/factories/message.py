import factory
from data.models import Message
from .canteen import CanteenFactory


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    destination_canteen = factory.SubFactory(CanteenFactory)
    sender_name = factory.Faker("name")
    sender_email = factory.Faker("email")
    body = factory.Faker("paragraph")
