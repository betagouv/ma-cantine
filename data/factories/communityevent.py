import factory
from data.models import CommunityEvent


class CommunityEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommunityEvent

    title = factory.Faker("catch_phrase")
    description = factory.Faker("paragraph")
    date = factory.Faker("future_date")
    link = factory.Faker("uri")
