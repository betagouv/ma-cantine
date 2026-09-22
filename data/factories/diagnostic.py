import random
import datetime

import factory
from factory import fuzzy

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import TELEDECLARATION_FIELDS, get_teledeclaration_fields_required

from .canteen import CanteenFactory


def _fill_required_fields(obj):
    """
    Fill any required (appro & canteen) field left at None with 0, so full_clean() doesn't reject the diagnostic.
    NOTE: valeur_totale must be > 0 (see validate_valeur_totale), so it's left as is.
    """
    if not (obj.year and obj.diagnostic_type):
        return
    try:
        required_fields = get_teledeclaration_fields_required(obj.year, obj.diagnostic_type)
    except ValueError:
        return
    if int(obj.year) >= 2026:
        required_fields = list(required_fields) + Diagnostic.CANTEEN_FIELDS
    for field_name in required_fields:
        if field_name != "valeur_totale" and getattr(obj, field_name) is None:
            setattr(obj, field_name, 0)


class DiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic
        # cannot be used because we want to save after fill_complete_fields is run
        # skip_postgeneration_save = True

    canteen = factory.SubFactory(CanteenFactory)
    year = datetime.date.today().year - 1
    diagnostic_type = fuzzy.FuzzyChoice(list(Diagnostic.DiagnosticType))

    valeur_totale = factory.Faker("random_int", min=6000, max=10000)
    valeur_bio = factory.Faker("random_int", min=0, max=2000)
    valeur_siqo = factory.Faker("random_int", min=0, max=2000)
    valeur_egalim_autres = factory.Faker("random_int", min=0, max=20)
    valeur_viandes_volailles = factory.Faker("random_int", min=0, max=20)
    # the egalim part cannot be more than the family total
    valeur_viandes_volailles_egalim = factory.LazyAttribute(
        lambda o: random.randint(0, o.valeur_viandes_volailles or 0)
    )

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

    @factory.post_generation
    def fill_required_fields(obj, create, extracted, **kwargs):
        _fill_required_fields(obj)


class CompleteDiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = fuzzy.FuzzyChoice(TELEDECLARATION_FIELDS.keys())
    diagnostic_type = Diagnostic.DiagnosticType.COMPLETE

    valeur_totale = factory.Faker("random_int", min=6000, max=10000)
    valeur_viandes_volailles_bio = factory.Faker("random_int", min=0, max=20)
    # valeur_boissons (family total) isn't otherwise set, so it must be >= valeur_boissons_bio (see validate_valeur_famille)
    valeur_boissons = factory.Faker("random_int", min=0, max=20)
    valeur_boissons_bio = factory.LazyAttribute(lambda o: random.randint(0, o.valeur_boissons or 0))

    valeur_egalim_autres = factory.Faker("random_int", min=0, max=20)
    # the family totals must be >= each of their label values (bio & france are up to 20 each), and their egalim part
    valeur_viandes_volailles = factory.Faker("random_int", min=40, max=60)
    valeur_viandes_volailles_egalim = factory.LazyAttribute(
        lambda o: random.randint(0, o.valeur_viandes_volailles or 0)
    )
    valeur_viandes_volailles_france = factory.Faker("random_int", min=0, max=20)
    valeur_produits_de_la_mer = factory.Faker("random_int", min=0, max=20)
    valeur_produits_de_la_mer_egalim = factory.LazyAttribute(
        lambda o: random.randint(0, o.valeur_produits_de_la_mer or 0)
    )

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

    @factory.post_generation
    def fill_required_fields(obj, create, extracted, **kwargs):
        _fill_required_fields(obj)
