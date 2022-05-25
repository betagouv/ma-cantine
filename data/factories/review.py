import factory
import random
from data.models import Review
from .user import UserFactory


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    rating = random.randint(0, 5)
    suggestion = factory.Faker("sentence")
    page = factory.Faker("word")
    hasCanteen = factory.Faker("boolean")
    hasDiagnostic = factory.Faker("boolean")
