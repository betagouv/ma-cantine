import random
import factory
from factory import fuzzy
from data.models import Diagnostic
from .canteen import CanteenFactory
import datetime

YEAR = datetime.date.today().year
MIN_YEAR = YEAR - 2
MAX_YEAR = YEAR + 1


class DiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker("random_int", min=MIN_YEAR, max=MAX_YEAR)
    diagnostic_type = fuzzy.FuzzyChoice(list(Diagnostic.DiagnosticType))

    value_bio_ht = factory.Faker("random_int", min=0, max=2000)
    value_sustainable_ht = factory.Faker("random_int", min=0, max=2000)
    value_total_ht = factory.Faker("random_int", min=6000, max=10000)

    value_externality_performance_ht = factory.Faker("random_int", min=0, max=20)
    value_egalim_others_ht = factory.Faker("random_int", min=0, max=20)
    value_meat_poultry_ht = factory.Faker("random_int", min=0, max=20)
    value_meat_poultry_egalim_ht = factory.Faker("random_int", min=0, max=20)
    value_meat_poultry_france_ht = factory.Faker("random_int", min=0, max=20)
    value_fish_ht = factory.Faker("random_int", min=0, max=20)
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


def random_int(min, max):
    return factory.Faker("random_int", min=min, max=max)


class CompleteDiagnosticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnostic

    canteen = factory.SubFactory(CanteenFactory)
    year = factory.Faker("random_int", min=MIN_YEAR, max=MAX_YEAR)
    diagnostic_type = Diagnostic.DiagnosticType.COMPLETE

    # there are 112 complete fields. The sum of a subset, containing 88 fields, cannot exceed the total sum.
    # this check happens in the diagnostic's clean method.
    value_total_ht = random_int(8800, 10000)
    value_meat_poultry_ht = random_int(1100, 4400)
    value_fish_ht = random_int(1100, 4400)

    # you'll need to call diagnostic.full_clean() in your test to get the simple values

    # meat_poultry fields
    value_viandes_volailles_bio = random_int(0, 100)
    value_viandes_volailles_label_rouge = random_int(0, 100)
    value_viandes_volailles_aocaop_igp_stg = random_int(0, 100)
    value_viandes_volailles_hve = random_int(0, 100)
    value_viandes_volailles_peche_durable = random_int(0, 100)
    value_viandes_volailles_rup = random_int(0, 100)
    value_viandes_volailles_commerce_equitable = random_int(0, 100)
    value_viandes_volailles_fermier = random_int(0, 100)
    value_viandes_volailles_performance = random_int(0, 100)
    value_viandes_volailles_externalites = random_int(0, 100)
    value_viandes_volailles_non_egalim = random_int(0, 100)

    # fish fields
    value_produits_de_la_mer_bio = random_int(0, 100)
    value_produits_de_la_mer_label_rouge = random_int(0, 100)
    value_produits_de_la_mer_aocaop_igp_stg = random_int(0, 100)
    value_produits_de_la_mer_hve = random_int(0, 100)
    value_produits_de_la_mer_peche_durable = random_int(0, 100)
    value_produits_de_la_mer_rup = random_int(0, 100)
    value_produits_de_la_mer_commerce_equitable = random_int(0, 100)
    value_produits_de_la_mer_fermier = random_int(0, 100)
    value_produits_de_la_mer_externalites = random_int(0, 100)
    value_produits_de_la_mer_performance = random_int(0, 100)
    value_produits_de_la_mer_non_egalim = random_int(0, 100)

    # remaining fields where a product can only be counted one time
    value_fruits_et_legumes_bio = random_int(0, 100)
    value_charcuterie_bio = random_int(0, 100)
    value_produits_laitiers_bio = random_int(0, 100)
    value_boulangerie_bio = random_int(0, 100)
    value_boissons_bio = random_int(0, 100)
    value_autres_bio = random_int(0, 100)
    value_fruits_et_legumes_label_rouge = random_int(0, 100)
    value_charcuterie_label_rouge = random_int(0, 100)
    value_produits_laitiers_label_rouge = random_int(0, 100)
    value_boulangerie_label_rouge = random_int(0, 100)
    value_boissons_label_rouge = random_int(0, 100)
    value_autres_label_rouge = random_int(0, 100)
    value_fruits_et_legumes_aocaop_igp_stg = random_int(0, 100)
    value_charcuterie_aocaop_igp_stg = random_int(0, 100)
    value_produits_laitiers_aocaop_igp_stg = random_int(0, 100)
    value_boulangerie_aocaop_igp_stg = random_int(0, 100)
    value_boissons_aocaop_igp_stg = random_int(0, 100)
    value_autres_aocaop_igp_stg = random_int(0, 100)
    value_fruits_et_legumes_hve = random_int(0, 100)
    value_charcuterie_hve = random_int(0, 100)
    value_produits_laitiers_hve = random_int(0, 100)
    value_boulangerie_hve = random_int(0, 100)
    value_boissons_hve = random_int(0, 100)
    value_autres_hve = random_int(0, 100)
    value_fruits_et_legumes_peche_durable = random_int(0, 100)
    value_charcuterie_peche_durable = random_int(0, 100)
    value_produits_laitiers_peche_durable = random_int(0, 100)
    value_boulangerie_peche_durable = random_int(0, 100)
    value_boissons_peche_durable = random_int(0, 100)
    value_autres_peche_durable = random_int(0, 100)
    value_fruits_et_legumes_rup = random_int(0, 100)
    value_charcuterie_rup = random_int(0, 100)
    value_produits_laitiers_rup = random_int(0, 100)
    value_boulangerie_rup = random_int(0, 100)
    value_boissons_rup = random_int(0, 100)
    value_autres_rup = random_int(0, 100)
    value_fruits_et_legumes_commerce_equitable = random_int(0, 100)
    value_charcuterie_commerce_equitable = random_int(0, 100)
    value_produits_laitiers_commerce_equitable = random_int(0, 100)
    value_boulangerie_commerce_equitable = random_int(0, 100)
    value_boissons_commerce_equitable = random_int(0, 100)
    value_autres_commerce_equitable = random_int(0, 100)
    value_fruits_et_legumes_fermier = random_int(0, 100)
    value_charcuterie_fermier = random_int(0, 100)
    value_produits_laitiers_fermier = random_int(0, 100)
    value_boulangerie_fermier = random_int(0, 100)
    value_boissons_fermier = random_int(0, 100)
    value_autres_fermier = random_int(0, 100)
    value_fruits_et_legumes_externalites = random_int(0, 100)
    value_charcuterie_externalites = random_int(0, 100)
    value_produits_laitiers_externalites = random_int(0, 100)
    value_boulangerie_externalites = random_int(0, 100)
    value_boissons_externalites = random_int(0, 100)
    value_autres_externalites = random_int(0, 100)
    value_fruits_et_legumes_performance = random_int(0, 100)
    value_charcuterie_performance = random_int(0, 100)
    value_produits_laitiers_performance = random_int(0, 100)
    value_boulangerie_performance = random_int(0, 100)
    value_boissons_performance = random_int(0, 100)
    value_autres_performance = random_int(0, 100)
    value_fruits_et_legumes_non_egalim = random_int(0, 100)
    value_charcuterie_non_egalim = random_int(0, 100)
    value_produits_laitiers_non_egalim = random_int(0, 100)
    value_boulangerie_non_egalim = random_int(0, 100)
    value_boissons_non_egalim = random_int(0, 100)
    value_autres_non_egalim = random_int(0, 100)

    # fields that can contain items counted twice
    value_viandes_volailles_france = random_int(0, 100)
    value_produits_de_la_mer_france = random_int(0, 100)
    value_fruits_et_legumes_france = random_int(0, 100)
    value_charcuterie_france = random_int(0, 100)
    value_produits_laitiers_france = random_int(0, 100)
    value_boulangerie_france = random_int(0, 100)
    value_boissons_france = random_int(0, 100)
    value_autres_france = random_int(0, 100)
    value_viandes_volailles_short_distribution = random_int(0, 100)
    value_produits_de_la_mer_short_distribution = random_int(0, 100)
    value_fruits_et_legumes_short_distribution = random_int(0, 100)
    value_charcuterie_short_distribution = random_int(0, 100)
    value_produits_laitiers_short_distribution = random_int(0, 100)
    value_boulangerie_short_distribution = random_int(0, 100)
    value_boissons_short_distribution = random_int(0, 100)
    value_autres_short_distribution = random_int(0, 100)
    value_viandes_volailles_local = random_int(0, 100)
    value_produits_de_la_mer_local = random_int(0, 100)
    value_fruits_et_legumes_local = random_int(0, 100)
    value_charcuterie_local = random_int(0, 100)
    value_produits_laitiers_local = random_int(0, 100)
    value_boulangerie_local = random_int(0, 100)
    value_boissons_local = random_int(0, 100)
    value_autres_local = random_int(0, 100)

    # diagnostics of type COMPLETE do contain the other measure values, but this factory doesn't care about them
