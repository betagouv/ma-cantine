import zoneinfo

import factory

from data.models import CommunityEvent


class CommunityEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommunityEvent

    title = factory.Faker("catch_phrase")
    tagline = factory.Faker("paragraph")
    start_date = factory.Faker("future_datetime", tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
    end_date = factory.Faker("future_datetime", tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))
    link = factory.Faker("uri")
