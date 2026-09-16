import random

import factory
from factory.fuzzy import FuzzyChoice

from data.models import Purchase

from .canteen import CanteenFactory


def _random_caracteristiques():
    """
    EUROPE and FRANCE cannot be selected at the same time (see validators/purchase.py),
    so one of them is excluded from the pool before sampling.
    """
    choices = list(Purchase.Characteristic.values)
    choices.remove(random.choice([Purchase.Characteristic.EUROPE, Purchase.Characteristic.FRANCE]))
    return random.sample(choices, random.randint(0, 3))


class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase

    canteen = factory.SubFactory(CanteenFactory)
    date = factory.Faker("date")
    description = factory.Faker("word")
    fournisseur = factory.Faker("company")
    famille_produits = FuzzyChoice(Purchase.Family.values)
    caracteristiques = factory.LazyFunction(_random_caracteristiques)
    prix_ht = factory.Faker("random_int", min=0, max=2000)
    definition_local = factory.LazyAttribute(
        lambda x: random.choice(Purchase.Local.values) if Purchase.Characteristic.LOCAL in x.caracteristiques else None
    )
