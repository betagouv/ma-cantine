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

    valeur_totale = factory.Faker("random_int", min=6000, max=10000)
    valeur_bio = factory.Faker("random_int", min=0, max=2000)
    valeur_siqo = factory.Faker("random_int", min=0, max=2000)
    valeur_externalites_performance = factory.Faker("random_int", min=0, max=20)
    valeur_egalim_autres = factory.Faker("random_int", min=0, max=20)

    valeur_viandes_volailles = factory.Faker("random_int", min=0, max=20)
    valeur_viandes_volailles_egalim = factory.Faker("random_int", min=0, max=20)
    valeur_viandes_volailles_france = factory.Faker("random_int", min=0, max=20)
    valeur_produits_de_la_mer = factory.Faker("random_int", min=0, max=20)
    valeur_produits_de_la_mer_egalim = factory.Faker("random_int", min=0, max=20)

    has_waste_diagnostic = factory.Faker("boolean")
    has_waste_plan = factory.Faker("boolean")
    waste_actions = factory.List(random.sample(list(Diagnostic.WasteActions), random.randint(0, 2)))
    has_donation_agreement = factory.Faker("boolean")

    has_diversification_plan = factory.Faker("boolean")
    vegetarian_weekly_recurrence = fuzzy.FuzzyChoice(list(Diagnostic.VegetarianMenuFrequency))
    vegetarian_menu_type = fuzzy.FuzzyChoice(list(Diagnostic.VegetarianMenuType))

    cooking_plastic_substituted = factory.Faker("boolean")
    serving_plastic_substituted = factory.Faker("boolean")
    plastic_bottles_substituted = factory.Faker("boolean")
    plastic_tableware_substituted = factory.Faker("boolean")

    communication_supports = factory.List(random.sample(list(Diagnostic.CommunicationType), random.randint(0, 2)))
    communication_support_url = factory.Faker("uri")
    communicates_on_food_plan = factory.Faker("boolean")


class CompleteDiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker("year")
    diagnostic_type = Diagnostic.DiagnosticType.COMPLETE

    valeur_totale = factory.Faker("random_int", min=6000, max=10000)
    valeur_viandes_volailles_bio = factory.Faker("random_int", min=0, max=20)
    valeur_boissons_bio = factory.Faker("random_int", min=0, max=20)

    valeur_egalim_autres = factory.Faker("random_int", min=0, max=20)
    valeur_viandes_volailles = factory.Faker("random_int", min=0, max=20)
    valeur_viandes_volailles_egalim = factory.Faker("random_int", min=0, max=20)
    valeur_viandes_volailles_france = factory.Faker("random_int", min=0, max=20)
    valeur_produits_de_la_mer = factory.Faker("random_int", min=0, max=20)
    valeur_produits_de_la_mer_egalim = factory.Faker("random_int", min=0, max=20)

    has_waste_diagnostic = factory.Faker("boolean")
    has_waste_plan = factory.Faker("boolean")
    waste_actions = factory.List(random.sample(list(Diagnostic.WasteActions), random.randint(0, 2)))
    has_donation_agreement = factory.Faker("boolean")

    has_diversification_plan = factory.Faker("boolean")
    vegetarian_weekly_recurrence = fuzzy.FuzzyChoice(list(Diagnostic.VegetarianMenuFrequency))
    vegetarian_menu_type = fuzzy.FuzzyChoice(list(Diagnostic.VegetarianMenuType))

    cooking_plastic_substituted = factory.Faker("boolean")
    serving_plastic_substituted = factory.Faker("boolean")
    plastic_bottles_substituted = factory.Faker("boolean")
    plastic_tableware_substituted = factory.Faker("boolean")

    communication_supports = factory.List(random.sample(list(Diagnostic.CommunicationType), random.randint(0, 2)))
    communication_support_url = factory.Faker("uri")
    communicates_on_food_plan = factory.Faker("boolean")
