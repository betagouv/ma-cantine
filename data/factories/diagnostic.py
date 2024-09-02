import random
import factory
from factory import fuzzy
from data.models import Diagnostic
from data.utils import get_diagnostic_lower_limit_year, get_diagnostic_upper_limit_year
from .canteen import CanteenFactory


class DiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker(
        "random_int", min=get_diagnostic_lower_limit_year(), max=get_diagnostic_upper_limit_year()
    )  # "year"
    diagnostic_type = Diagnostic.DiagnosticType.SIMPLE


class CompleteDiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker(
        "random_int", min=get_diagnostic_lower_limit_year(), max=get_diagnostic_upper_limit_year()
    )  # "year"
    diagnostic_type = Diagnostic.DiagnosticType.COMPLETE

    value_total_ht = factory.Faker("random_int", min=6000, max=10000)
    value_viandes_volailles_bio = factory.Faker("random_int", min=0, max=20)
    value_boissons_bio = factory.Faker("random_int", min=0, max=20)

    value_egalim_others_ht = factory.Faker("random_int", min=0, max=20)
    value_meat_poultry_ht = factory.Faker("random_int", min=100, max=150)
    value_meat_poultry_egalim_ht = factory.Faker("random_int", min=0, max=20)
    value_meat_poultry_france_ht = factory.Faker("random_int", min=0, max=20)
    value_fish_ht = factory.Faker("random_int", min=50, max=100)
    value_fish_egalim_ht = factory.Faker("random_int", min=0, max=20)

    has_waste_diagnostic = factory.Faker("boolean")
    has_waste_plan = factory.Faker("boolean")
    waste_actions = factory.List(random.sample(list(Diagnostic.WasteActions), random.randint(0, 2)))
    has_donation_agreement = factory.Faker("boolean")

    has_diversification_plan = factory.Faker("boolean")
    vegetarian_weekly_recurrence = fuzzy.FuzzyChoice(list(Diagnostic.MenuFrequency))
    vegetarian_menu_type = fuzzy.FuzzyChoice(list(Diagnostic.MenuType))

    cooking_plastic_substituted = factory.Faker("boolean")
    serving_plastic_substituted = factory.Faker("boolean")
    plastic_bottles_substituted = factory.Faker("boolean")
    plastic_tableware_substituted = factory.Faker("boolean")

    communication_supports = factory.List(random.sample(list(Diagnostic.CommunicationType), random.randint(0, 2)))
    communication_support_url = factory.Faker("uri")
    communicates_on_food_plan = factory.Faker("boolean")
