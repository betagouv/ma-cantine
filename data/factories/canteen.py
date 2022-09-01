import random
import factory
from data.models import Canteen
from .sector import SectorFactory
from .user import UserFactory


class CanteenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Canteen

    name = factory.Faker("text", max_nb_chars=20)
    city = factory.Faker("city")
    postal_code = factory.Faker("postcode")
    daily_meal_count = factory.Faker("pyint")

    @factory.post_generation
    def sectors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for sector in extracted:
                self.sectors.add(sector)
        else:
            for _ in range(random.randint(1, 4)):
                self.sectors.add(SectorFactory.create())

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for manager in extracted:
                self.managers.add(manager)
        else:
            for _ in range(random.randint(1, 2)):
                self.managers.add(UserFactory.create())
