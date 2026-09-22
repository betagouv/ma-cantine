import random
import datetime

import factory
from factory import fuzzy

from data.models import Diagnostic
from data.models.diagnostic_teledeclaration_fields import TELEDECLARATION_FIELDS

from .canteen import CanteenFactory


def _fill_required_fields(obj):
    """
    Ensure the generated Diagnostic passes full_clean(): fill required appro fields via the model's own
    logic, plus, since 2026, canteen fields too (nombre_repas_an) -- the model intentionally doesn't
    default that one on its own (see Diagnostic2026ModelSaveTest), so it's a factory-only concern here.
    """
    try:
        obj.populate_required_fields_with_zero()
    except ValueError:
        pass
    if obj.year and obj.diagnostic_type and int(obj.year) >= 2026:
        for field_name in Diagnostic.CANTEEN_FIELDS:
            if getattr(obj, field_name) is None:
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
    # bio/siqo/egalim_autres are derived from valeur_totale (not independently random), so that overriding
    # valeur_totale in a test (e.g. to a small round number) can't make their sum exceed it (see validate_valeur_totale)
    valeur_bio = factory.LazyAttribute(
        lambda o: random.randint(0, min(2000, int(o.valeur_totale) // 4)) if o.valeur_totale else 0
    )
    valeur_siqo = factory.LazyAttribute(
        lambda o: random.randint(0, min(2000, int(o.valeur_totale) // 4)) if o.valeur_totale else 0
    )
    valeur_egalim_autres = factory.LazyAttribute(
        lambda o: random.randint(0, min(20, int(o.valeur_totale) // 20)) if o.valeur_totale else 0
    )
    # also derived from valeur_totale, for the same reason as bio/siqo/egalim_autres above
    valeur_viandes_volailles = factory.LazyAttribute(
        lambda o: random.randint(0, min(20, int(o.valeur_totale) // 20)) if o.valeur_totale else 0
    )
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

    # NOTE: here because we want to ensure valid Diagnostic are created (regarding full_clean)
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

    # NOTE: here because we want to ensure valid Diagnostic are created (regarding full_clean)
    @factory.post_generation
    def fill_required_fields(obj, create, extracted, **kwargs):
        _fill_required_fields(obj)
