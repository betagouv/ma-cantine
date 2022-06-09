import factory
from data.models import CommunityEvent
import pytz


class CommunityEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommunityEvent

    title = factory.Faker("catch_phrase")
    tagline = factory.Faker("paragraph")
    start_date = factory.Faker("future_datetime", tzinfo=pytz.timezone("Europe/Paris"))
    end_date = factory.Faker("future_datetime", tzinfo=pytz.timezone("Europe/Paris"))
    link = factory.Faker("uri")
