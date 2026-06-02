import random

import factory
from factory.fuzzy import FuzzyChoice

from data.models import Purchase

from .canteen import CanteenFactory


class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase

    canteen = factory.SubFactory(CanteenFactory)
    date = factory.Faker("date")
    description = factory.Faker("word")
    fournisseur = factory.Faker("company")
    famille_produits = FuzzyChoice(Purchase.Family.values)
    caracteristiques = factory.List(random.sample(list(Purchase.Characteristic.values), random.randint(0, 3)))
    prix_ht = factory.Faker("random_int", min=0, max=2000)
    definition_local = factory.LazyAttribute(
        lambda x: random.choice(Purchase.Local.values) if Purchase.Characteristic.LOCAL in x.caracteristiques else None
    )
