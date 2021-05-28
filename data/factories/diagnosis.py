import random
import factory
from factory import fuzzy
from data.models import Diagnosis
from .canteen import CanteenFactory


class DiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnosis

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker("year")

    value_bio_ht = factory.Faker("random_int", min=0, max=10000)
    value_fair_trade_ht = factory.Faker("random_int", min=0, max=2000)
    value_sustainable_ht = factory.Faker("random_int", min=0, max=2000)
    value_total_ht = factory.Faker("random_int", min=0, max=2000)

    has_waste_diagnostic = factory.Faker("boolean")
    has_waste_plan = factory.Faker("boolean")
    waste_actions = factory.List(
        random.sample(list(Diagnosis.WasteActions), random.randint(0, 2))
    )
    has_donation_agreement = factory.Faker("boolean")

    has_diversification_plan = factory.Faker("boolean")
    vegetarian_weekly_recurrence = fuzzy.FuzzyChoice(list(Diagnosis.MenuFrequency))
    vegetarian_menu_type = fuzzy.FuzzyChoice(list(Diagnosis.MenuType))

    cooking_plastic_substituted = factory.Faker("boolean")
    serving_plastic_substituted = factory.Faker("boolean")
    plastic_bottles_substituted = factory.Faker("boolean")
    plastic_tableware_substituted = factory.Faker("boolean")

    communication_supports = factory.List(
        random.sample(list(Diagnosis.CommunicationType), random.randint(0, 2))
    )
    communication_support_url = factory.Faker("uri")
    comunicates_on_food_plan = factory.Faker("boolean")
