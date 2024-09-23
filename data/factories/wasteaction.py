import random

import factory
from factory import fuzzy

from data.models import WasteAction


class WasteActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WasteAction

    title = factory.Faker("text", max_nb_chars=20)
    description = factory.Faker("text")
    effort = fuzzy.FuzzyChoice(list(WasteAction.Effort))
    waste_origins = factory.List(random.sample(list(WasteAction.WasteOrigin), random.randint(1, 3)))
