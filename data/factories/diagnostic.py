import random
import factory
from factory import fuzzy
from data.models import Diagnostic
from .canteen import CanteenFactory


class DiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker("year")
    diagnostic_type = fuzzy.FuzzyChoice(list(Diagnostic.DiagnosticType))

    value_bio_ht = factory.Faker("random_int", min=0, max=2000)
    value_sustainable_ht = factory.Faker("random_int", min=0, max=2000)
    value_total_ht = factory.Faker("random_int", min=10000, max=20000)

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

    value_label_rouge_ht = factory.Faker("random_int", min=0, max=200)
    value_aocaop_igp_stg_ht = factory.Faker("random_int", min=0, max=200)
    value_hve_ht = factory.Faker("random_int", min=0, max=200)
    value_peche_durable_ht = factory.Faker("random_int", min=0, max=200)
    value_rup_ht = factory.Faker("random_int", min=0, max=200)
    value_fermier_ht = factory.Faker("random_int", min=0, max=200)
    value_externalites_ht = factory.Faker("random_int", min=0, max=200)
    value_commerce_equitable_ht = factory.Faker("random_int", min=0, max=200)
    value_performance_ht = factory.Faker("random_int", min=0, max=200)
    value_france_ht = factory.Faker("random_int", min=0, max=200)
    value_short_distribution_ht = factory.Faker("random_int", min=0, max=200)
    value_local_ht = factory.Faker("random_int", min=0, max=200)
