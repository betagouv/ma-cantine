import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from data.fields import ChoiceArrayField
from .canteen import Canteen


class Diagnostic(models.Model):
    class Meta:
        verbose_name = "diagnostic"
        verbose_name_plural = "diagnostics"
        constraints = [
            models.UniqueConstraint(fields=["canteen", "year"], name="annual_diagnostic"),
        ]

    class MenuFrequency(models.TextChoices):
        LOW = "LOW", "Moins d'une fois par semaine"
        MID = "MID", "Une fois par semaine"
        HIGH = "HIGH", "Plus d'une fois par semaine"
        DAILY = "DAILY", "De façon quotidienne"

    class MenuType(models.TextChoices):
        UNIQUE = "UNIQUE", "Un menu végétarien en plat unique, sans choix"
        SEVERAL = "SEVERAL", "Un menu végétarien composé de plusieurs choix de plats végétariens"
        ALTERNATIVES = (
            "ALTERNATIVES",
            "Un menu végétarien au choix, en plus d'autres plats non végétariens",
        )

    class CommunicationType(models.TextChoices):
        EMAIL = "EMAIL", "Envoi d'e-mail aux convives ou à leurs représentants"
        DISPLAY = "DISPLAY", "Par affichage sur le lieu de restauration"
        WEBSITE = "WEBSITE", "Sur site internet ou intranet (mairie, cantine)"
        OTHER = "OTHER", "Autres moyens d'affichage et de communication électronique"
        DIGITAL = "DIGITAL", "Par voie électronique"

    class CommunicationFrequency(models.TextChoices):
        REGULARLY = "REGULARLY", "Régulièrement au cours de l’année"
        YEARLY = "YEARLY", "Une fois par an"
        LESS_THAN_YEARLY = "LESS_THAN_YEARLY", "Moins d'une fois par an"

    class WasteActions(models.TextChoices):
        INSCRIPTION = "INSCRIPTION", "Pré-inscription des convives obligatoire"
        AWARENESS = "AWARENESS", "Sensibilisation par affichage ou autre média"
        TRAINING = "TRAINING", "Formation / information du personnel de restauration"
        DISTRIBUTION = (
            "DISTRIBUTION",
            "Réorganisation de la distribution des composantes du repas",
        )
        PORTIONS = "PORTIONS", "Choix des portions (grande faim, petite faim)"
        REUSE = "REUSE", "Réutilisation des restes de préparation / surplus"

    class DiversificationPlanActions(models.TextChoices):
        PRODUCTS = (
            "PRODUCTS",
            "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
        )
        PRESENTATION = (
            "PRESENTATION",
            "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
        )
        MENU = (
            "MENU",
            "Agir sur la manière dont les menus sont conçus ces plats en soulignant leurs attributs positifs",
        )
        PROMOTION = (
            "PROMOTION",
            "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
        )
        TRAINING = (
            "TRAINING",
            "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
        )

    class VegetarianMenuBase(models.TextChoices):
        GRAIN = "GRAIN", "De céréales et/ou les légumes secs (hors soja)"
        SOY = "SOY", "De soja"
        CHEESE = "CHEESE", "De fromage"
        EGG = "EGG", "D’œufs"
        READYMADE = "READYMADE", "Plats prêts à l'emploi"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE)

    year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="année",
    )

    # Product origin
    value_bio_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Bio - Valeur annuelle HT",
    )
    value_fair_trade_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Commerce équitable - Valeur annuelle HT",
    )
    value_sustainable_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits durables (hors bio) - Valeur annuelle HT",
    )
    value_pat_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits dans le cadre de Projects Alimentaires Territoriaux - Valeur annuelle HT",
    )
    value_total_ht = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valeur totale annuelle HT",
    )

    value_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valeur label rouge",
    )
    value_label_aoc_igp = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valeur label AOC/AOP/IGP",
    )
    value_label_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valeur label HVE",
    )

    # Food waste
    has_waste_diagnostic = models.BooleanField(
        blank=True, null=True, verbose_name="diagnostic sur le gaspillage réalisé"
    )
    has_waste_plan = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="plan d'action contre le gaspillage en place",
    )
    waste_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=WasteActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions contre le gaspillage en place",
    )
    other_waste_action = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre action contre le gaspillage alimentaire",
    )
    has_donation_agreement = models.BooleanField(blank=True, null=True, verbose_name="propose des dons alimentaires")
    has_waste_measures = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="réalise des mesures de gaspillage alimentaire",
    )
    bread_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de pain kg/an",
    )
    served_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste plateau kg/an",
    )
    unserved_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste en production (non servi) kg/an",
    )
    side_leftovers = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="reste de composantes kg/an",
    )
    donation_frequency = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="fréquence de dons dons/an",
    )
    donation_quantity = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="quantité des denrées données kg/an",
    )
    donation_food_type = models.TextField(
        null=True,
        blank=True,
        verbose_name="type de denrées données",
    )
    other_waste_comments = models.TextField(
        null=True,
        blank=True,
        verbose_name="autres commentaires (gaspillage)",
    )

    # Vegetarian menus
    has_diversification_plan = models.BooleanField(
        blank=True, null=True, verbose_name="plan de diversification en place"
    )
    diversification_plan_actions = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=DiversificationPlanActions.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="actions inclus dans le plan de diversification des protéines",
    )
    vegetarian_weekly_recurrence = models.CharField(
        max_length=255,
        choices=MenuFrequency.choices,
        null=True,
        blank=True,
        verbose_name="Menus végétariens par semaine",
    )
    vegetarian_menu_type = models.CharField(
        max_length=255,
        choices=MenuType.choices,
        blank=True,
        null=True,
        verbose_name="Menu végétarien proposé",
    )
    vegetarian_menu_bases = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=VegetarianMenuBase.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="bases de menu végétarien",
    )

    # Plastic replacement
    cooking_plastic_substituted = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de cuisson en plastique remplacés",
    )
    serving_plastic_substituted = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="contenants de service en plastique remplacés",
    )
    plastic_bottles_substituted = models.BooleanField(
        blank=True, null=True, verbose_name="bouteilles en plastique remplacées"
    )
    plastic_tableware_substituted = models.BooleanField(
        blank=True, null=True, verbose_name="ustensils en plastique remplacés"
    )

    # Information and communication
    communication_supports = ChoiceArrayField(
        base_field=models.CharField(max_length=255, choices=CommunicationType.choices),
        blank=True,
        null=True,
        size=None,
        verbose_name="Communication utilisée",
    )
    other_communication_support = models.TextField(
        null=True,
        blank=True,
        verbose_name="autre communication utilisée",
    )
    communication_support_url = models.URLField(blank=True, null=True, verbose_name="Lien de communication")
    communicates_on_food_plan = models.BooleanField(
        blank=True, null=True, verbose_name="Communique sur le plan alimentaire"
    )
    communicates_on_food_quality = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Communique sur les démarches qualité/durables/équitables",
    )
    communication_frequency = models.CharField(
        max_length=255,
        choices=CommunicationFrequency.choices,
        blank=True,
        null=True,
        verbose_name="fréquence de communication",
    )

    # Campaign tracking
    creation_mtm_source = models.TextField(
        null=True, blank=True, verbose_name="mtm_source du lien tracké lors de la création"
    )
    creation_mtm_campaign = models.TextField(
        null=True, blank=True, verbose_name="mtm_campaign du lien tracké lors de la création"
    )
    creation_mtm_medium = models.TextField(
        null=True, blank=True, verbose_name="mtm_medium du lien tracké lors de la création"
    )

    # detailed values
    value_viandes_volailles_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Bio",
    )
    value_produits_de_la_mer_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Bio",
    )
    value_fruits_et_legumes_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Bio",
    )
    value_charcuterie_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Bio",
    )
    value_produits_laitiers_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio",
    )
    value_boulangerie_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Bio",
    )
    value_boissons_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Bio",
    )
    value_autres_bio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Bio",
    )
    value_viandes_volailles_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Label rouge",
    )
    value_produits_de_la_mer_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Label rouge",
    )
    value_fruits_et_legumes_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Label rouge",
    )
    value_charcuterie_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Label rouge",
    )
    value_produits_laitiers_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Label rouge",
    )
    value_boulangerie_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Label rouge",
    )
    value_boissons_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Label rouge",
    )
    value_autres_label_rouge = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Label rouge",
    )
    value_viandes_volailles_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, AOC / AOP / IGP / STG",
    )
    value_produits_de_la_mer_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, AOC / AOP / IGP / STG",
    )
    value_fruits_et_legumes_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, AOC / AOP / IGP / STG",
    )
    value_charcuterie_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, AOC / AOP / IGP / STG",
    )
    value_produits_laitiers_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), AOC / AOP / IGP / STG",
    )
    value_boulangerie_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, AOC / AOP / IGP / STG",
    )
    value_boissons_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, AOC / AOP / IGP / STG",
    )
    value_autres_aocaop_igp_stg = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, AOC / AOP / IGP / STG",
    )
    value_viandes_volailles_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Haute valeur environnementale",
    )
    value_produits_de_la_mer_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Haute valeur environnementale",
    )
    value_fruits_et_legumes_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Haute valeur environnementale",
    )
    value_charcuterie_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Haute valeur environnementale",
    )
    value_produits_laitiers_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Haute valeur environnementale",
    )
    value_boulangerie_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Haute valeur environnementale",
    )
    value_boissons_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Haute valeur environnementale",
    )
    value_autres_hve = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Haute valeur environnementale",
    )
    value_viandes_volailles_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Pêche durable",
    )
    value_produits_de_la_mer_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Pêche durable",
    )
    value_fruits_et_legumes_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Pêche durable",
    )
    value_charcuterie_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Pêche durable",
    )
    value_produits_laitiers_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Pêche durable",
    )
    value_boulangerie_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Pêche durable",
    )
    value_boissons_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Pêche durable",
    )
    value_autres_peche_durable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Pêche durable",
    )
    value_viandes_volailles_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Région ultrapériphérique",
    )
    value_produits_de_la_mer_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Région ultrapériphérique",
    )
    value_fruits_et_legumes_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Région ultrapériphérique",
    )
    value_charcuterie_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Région ultrapériphérique",
    )
    value_produits_laitiers_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Région ultrapériphérique",
    )
    value_boulangerie_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Région ultrapériphérique",
    )
    value_boissons_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Région ultrapériphérique",
    )
    value_autres_rup = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Région ultrapériphérique",
    )
    value_viandes_volailles_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Fermier",
    )
    value_produits_de_la_mer_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Fermier",
    )
    value_fruits_et_legumes_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Fermier",
    )
    value_charcuterie_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Fermier",
    )
    value_produits_laitiers_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Fermier",
    )
    value_boulangerie_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Fermier",
    )
    value_boissons_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Fermier",
    )
    value_autres_fermier = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Fermier",
    )
    value_viandes_volailles_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_produits_de_la_mer_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_fruits_et_legumes_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_charcuterie_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_produits_laitiers_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_boulangerie_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_boissons_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_autres_externalites = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    value_viandes_volailles_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Commerce équitable",
    )
    value_produits_de_la_mer_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Commerce équitable",
    )
    value_fruits_et_legumes_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Commerce équitable",
    )
    value_charcuterie_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Commerce équitable",
    )
    value_produits_laitiers_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Commerce équitable",
    )
    value_boulangerie_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Commerce équitable",
    )
    value_boissons_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Commerce équitable",
    )
    value_autres_commerce_equitable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Commerce équitable",
    )
    value_viandes_volailles_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_produits_de_la_mer_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_fruits_et_legumes_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_charcuterie_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_produits_laitiers_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_boulangerie_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_boissons_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_autres_performance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    value_viandes_volailles_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Provenance France",
    )
    value_produits_de_la_mer_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Provenance France",
    )
    value_fruits_et_legumes_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Provenance France",
    )
    value_charcuterie_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Provenance France",
    )
    value_produits_laitiers_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Provenance France",
    )
    value_boulangerie_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Provenance France",
    )
    value_boissons_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Provenance France",
    )
    value_autres_france = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Provenance France",
    )
    value_viandes_volailles_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Circuit-court",
    )
    value_produits_de_la_mer_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Circuit-court",
    )
    value_fruits_et_legumes_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Circuit-court",
    )
    value_charcuterie_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Circuit-court",
    )
    value_produits_laitiers_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Circuit-court",
    )
    value_boulangerie_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Circuit-court",
    )
    value_boissons_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Circuit-court",
    )
    value_autres_short_distribution = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Circuit-court",
    )
    value_viandes_volailles_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Viandes et volailles fraîches et surgelées, Produit local",
    )
    value_produits_de_la_mer_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Produits aquatiques frais et surgelés, Produit local",
    )
    value_fruits_et_legumes_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fruits et légumes frais et surgelés, Produit local",
    )
    value_charcuterie_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Charcuterie, Produit local",
    )
    value_produits_laitiers_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit local",
    )
    value_boulangerie_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boulangerie/Pâtisserie fraîches, Produit local",
    )
    value_boissons_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Boissons, Produit local",
    )
    value_autres_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres produits frais, surgelés et d’épicerie, Produit local",
    )

    @property
    def latest_teledeclaration(self):
        if self.teledeclaration_set.count() == 0:
            return None
        return self.teledeclaration_set.order_by("-creation_date").first()

    def clean(self):
        self.validate_year()
        self.validate_approvisionment_total()
        return super().clean()

    def validate_year(self):
        if self.year is None:
            return
        lower_limit_year = 2019
        upper_limit_year = datetime.datetime.now().date().year + 1
        if not isinstance(self.year, int) or self.year < lower_limit_year or self.year > upper_limit_year:
            raise ValidationError(
                {"year": f"L'année doit être comprise entre {lower_limit_year} et {upper_limit_year}."}
            )

    def validate_approvisionment_total(self):
        if self.value_total_ht is None or not isinstance(self.value_total_ht, Decimal):
            return
        value_sum = (self.value_bio_ht or 0) + (self.value_sustainable_ht or 0)
        if value_sum > self.value_total_ht:
            raise ValidationError(
                {
                    "value_total_ht": f"La somme des valeurs d'approvisionnement, {value_sum}, est plus que le total, {self.value_total_ht}"
                }
            )

    def __str__(self):
        return f"Diagnostic pour {self.canteen.name} ({self.year})"

    def label_sum(self, label):
        families = [
            "viandes_volailles",
            "produits_de_la_mer",
            "fruits_et_legumes",
            "charcuterie",
            "produits_laitiers",
            "boulangerie",
            "boissons",
            "autres",
        ]
        sum = 0
        for family in families:
            value = getattr(self, f"value_{family}_{label}")
            if value:
                sum = sum + value
        return sum

    def family_sum(self, family):
        labels = [
            "bio",
            "label_rouge",
            "aocaop_igp_stg",
            "hve",
            "peche_durable",
            "rup",
            "fermier",
            "externalites",
            "commerce_equitable",
            "performance",
            # TODO: should the following three be included if they're not EGAlim?
            "france",
            "short_distribution",
            "local",
        ]
        sum = 0
        for label in labels:
            value = getattr(self, f"value_{family}_{label}")
            if value:
                sum = sum + value
        return sum

    @property
    def total_label_bio(self):
        return self.label_sum("bio")

    @property
    def total_label_label_rouge(self):
        return self.label_sum("label_rouge")

    @property
    def total_label_aocaop_igp_stg(self):
        return self.label_sum("aocaop_igp_stg")

    @property
    def total_label_hve(self):
        return self.label_sum("hve")

    @property
    def total_label_peche_durable(self):
        return self.label_sum("peche_durable")

    @property
    def total_label_rup(self):
        return self.label_sum("rup")

    @property
    def total_label_fermier(self):
        return self.label_sum("fermier")

    @property
    def total_label_externalites(self):
        return self.label_sum("externalites")

    @property
    def total_label_commerce_equitable(self):
        return self.label_sum("commerce_equitable")

    @property
    def total_label_performance(self):
        return self.label_sum("performance")

    @property
    def total_label_france(self):
        return self.label_sum("france")

    @property
    def total_label_short_distribution(self):
        return self.label_sum("short_distribution")

    @property
    def total_label_local(self):
        return self.label_sum("local")

    @property
    def total_family_viandes_volailles(self):
        return self.family_sum("viandes_volailles")

    @property
    def total_family_produits_de_la_mer(self):
        return self.family_sum("produits_de_la_mer")

    @property
    def total_family_fruits_et_legumes(self):
        return self.family_sum("fruits_et_legumes")

    @property
    def total_family_charcuterie(self):
        return self.family_sum("charcuterie")

    @property
    def total_family_produits_laitiers(self):
        return self.family_sum("produits_laitiers")

    @property
    def total_family_boulangerie(self):
        return self.family_sum("boulangerie")

    @property
    def total_family_boissons(self):
        return self.family_sum("boissons")

    @property
    def total_family_autres(self):
        return self.family_sum("autres")
