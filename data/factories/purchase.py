import random

import factory
from factory.fuzzy import FuzzyChoice

from data.models import Purchase
from data.models.definitionlocal import DefinitionLocal

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
        lambda x: random.choice(DefinitionLocal.values)
        if Purchase.Characteristic.LOCAL in x.caracteristiques
        else None
    )
    definition_local_km = factory.LazyAttribute(
        lambda x: random.randint(0, 1000) if x.definition_local == DefinitionLocal.KM else None
    )

    @classmethod
    def _create(cls, model_class, *args, skip_validations=False, **kwargs):
        """
        skip_validations=True: to create a purchase that doesn't pass the validations (e.g. missing or invalid data)
        Usage: PurchaseFactory(prix_ht=None, skip_validations=True)
        """
        obj = model_class(*args, **kwargs)
        obj.save(skip_validations=skip_validations)
        return obj
