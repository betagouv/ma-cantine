from django.core.validators import MinValueValidator
from django.db import models

from data.models.definitionlocal import DefinitionLocal
from data.models.diagnostic_teledeclaration_fields import get_teledeclaration_fields_all_years
from data.utils import (
    make_optional_positive_decimal_field,
    make_optional_positive_integer_field,
    make_optional_positive_percentage_decimal_field,
)


class DiagnosticVoletApprovisionnementMixin(models.Model):
    """
    Volet "Approvisionnements"
    + the computed fields: *_agg & pourcentage_*
    """

    SIMPLE_APPRO_FIELDS = [
        "valeur_totale",
        "valeur_bio",
        "valeur_bio_dont_commerce_equitable",
        "valeur_siqo",
        "valeur_externalites_performance",
        "valeur_egalim_autres",
        "valeur_egalim_autres_dont_commerce_equitable",
        "valeur_europe",
        "valeur_france",
        "valeur_circuit_court",
        "valeur_local",
        "valeur_viandes_volailles",
        "valeur_viandes_volailles_egalim",
        "valeur_viandes_volailles_france",
        "valeur_produits_de_la_mer",
        "valeur_produits_de_la_mer_egalim",
        "valeur_produits_de_la_mer_france",
        "valeur_fruits_et_legumes_france",
        "valeur_charcuterie_france",
        "valeur_produits_laitiers_france",
        "valeur_boulangerie_france",
        "valeur_boissons_france",
        "valeur_autres_france",
    ]

    APPRO_AGGREGATED_FIELDS = [
        "valeur_bio_agg",
        "valeur_siqo_agg",
        "valeur_externalites_performance_agg",
        "valeur_egalim_autres_agg",
        "valeur_egalim_hors_bio_agg",
        "valeur_egalim_agg",
    ]

    SIMPLIFIED_DIAGNOSTIC_FIELDS = [
        "valeur_bio",
        "valeur_bio_dont_commerce_equitable",
        "valeur_siqo",
        "valeur_externalites_performance",
        "valeur_egalim_autres",
        "valeur_egalim_autres_dont_commerce_equitable",
        "valeur_viandes_volailles_egalim",
        "valeur_produits_de_la_mer_egalim",
    ]

    APPRO_FAMILY_FIELDS = [
        "valeur_viandes_volailles",
        "valeur_produits_de_la_mer",
        "valeur_fruits_et_legumes",
        "valeur_charcuterie",
        "valeur_produits_laitiers",
        "valeur_boulangerie",
        "valeur_boissons",
        "valeur_autres",
    ]

    APPRO_LABEL_FIELDS = [
        "valeur_bio",
        "valeur_bio_dont_commerce_equitable",
        "valeur_europe",
        "valeur_france",
        "valeur_circuit_court",
        "valeur_local",
    ]

    # valeur_local (simple) + valeur_<famille>_local (complete), see validate_definition_local
    APPRO_LOCAL_FIELDS = ["valeur_local"] + [f"{family_field}_local" for family_field in APPRO_FAMILY_FIELDS]

    # kept out of APPRO_FIELDS/SIMPLE_APPRO_FIELDS/COMPLETE_APPRO_FIELDS since those are also used
    # as numeric value fields (see validate_valeur_totale, macantine.utils.get_appro_fields_satellite)
    APPRO_LOCAL_DEFINITION_FIELDS = ["definition_local", "definition_local_km"]

    APPRO_LABEL_GROUPE_FIELDS = [
        "valeur_bio",
        "valeur_siqo",
        "valeur_externalites_performance",
        "valeur_egalim_autres",
    ]

    # all the appro amounts (all years & diagnostic_types, see diagnostic_teledeclaration_fields.py)
    # only the valeur_* fields: APPRO_FIELDS is also used as the list of numeric value fields
    # (nombre_repas_an & definition_local/definition_local_km are in the registry but not amounts)
    APPRO_FIELDS = [
        field_name
        for field_name in get_teledeclaration_fields_all_years("APPROVISIONNEMENT")
        if field_name.startswith("valeur_")
    ]
    # TODO: clean up when updating the imports
    APPRO_FIELDS_FOR_IMPORT = [
        field_name for field_name in APPRO_FIELDS if "bio_dont_commerce_equitable" not in field_name
    ]

    APPRO_FIELDS_NON_APPLICABLE = [
        "valeur_boissons_label_rouge",
        "valeur_viandes_volailles_peche_durable",
        "valeur_fruits_et_legumes_peche_durable",
        "valeur_charcuterie_peche_durable",
        "valeur_produits_laitiers_peche_durable",
        "valeur_boulangerie_peche_durable",
        "valeur_boissons_peche_durable",
        "valeur_autres_peche_durable",
    ]

    # legacy amounts from before the teledeclaration registry (not in diagnostic_teledeclaration_fields.py)
    APPRO_FIELDS_LEGACY = [
        "valeur_label_rouge",
        "valeur_label_aoc_igp",
        "valeur_label_hve",
        "valeur_fair_trade",
        "valeur_pat",
    ]

    COMPLETE_APPRO_FIELDS = ["valeur_totale"] + APPRO_FAMILY_FIELDS + APPRO_FIELDS
    # COMPLETE_APPRO_FIELDS = ["valeur_totale"] + APPRO_FAMILY_FIELDS + APPRO_FIELDS  # TODO when updating the imports

    APPRO_STATS_FIELDS = [
        "pourcentage_bio",
        "pourcentage_siqo",
        "pourcentage_externalites_performance",
        "pourcentage_egalim_autres",
        "pourcentage_egalim_hors_bio",
        "pourcentage_egalim",
        "pourcentage_viandes_volailles_egalim",
        "pourcentage_produits_de_la_mer_egalim",
        "pourcentage_viandes_volailles_produits_de_la_mer_egalim",
        "pourcentage_europe",
        "pourcentage_france",
        "pourcentage_circuit_court",
        "pourcentage_local",
        "pourcentage_viandes_volailles_europe",
        "pourcentage_produits_de_la_mer_europe",
        "pourcentage_fruits_et_legumes_europe",
        "pourcentage_charcuterie_europe",
        "pourcentage_produits_laitiers_europe",
        "pourcentage_boulangerie_europe",
        "pourcentage_boissons_europe",
        "pourcentage_autres_europe",
        "pourcentage_viandes_volailles_france",
        "pourcentage_produits_de_la_mer_france",
        "pourcentage_fruits_et_legumes_france",
        "pourcentage_charcuterie_france",
        "pourcentage_produits_laitiers_france",
        "pourcentage_boulangerie_france",
        "pourcentage_boissons_france",
        "pourcentage_autres_france",
        "pourcentage_viandes_volailles_circuit_court",
        "pourcentage_produits_de_la_mer_circuit_court",
        "pourcentage_fruits_et_legumes_circuit_court",
        "pourcentage_charcuterie_circuit_court",
        "pourcentage_produits_laitiers_circuit_court",
        "pourcentage_boulangerie_circuit_court",
        "pourcentage_boissons_circuit_court",
        "pourcentage_autres_circuit_court",
        "pourcentage_viandes_volailles_local",
        "pourcentage_produits_de_la_mer_local",
        "pourcentage_fruits_et_legumes_local",
        "pourcentage_charcuterie_local",
        "pourcentage_produits_laitiers_local",
        "pourcentage_boulangerie_local",
        "pourcentage_boissons_local",
        "pourcentage_autres_local",
        "objectifs_egalim_atteints",
    ]

    # Canteen info
    nombre_repas_an = make_optional_positive_integer_field(verbose_name="Nombre de repas par an")

    # Product origin
    valeur_totale = make_optional_positive_decimal_field(
        verbose_name="Valeur totale annuelle HT",
    )

    # per family
    valeur_viandes_volailles = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées",
    )
    valeur_produits_de_la_mer = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) poissons et produits aquatiques",
    )
    valeur_fruits_et_legumes = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) fruits et légumes frais ou surgelés",
    )
    valeur_charcuterie = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) charcuterie",
    )
    valeur_produits_laitiers = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) BOF (Produits laitiers, beurre et œufs)",
    )
    valeur_boulangerie = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) boulangerie / pâtisserie fraîches",
    )
    valeur_boissons = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) boissons",
    )
    valeur_autres = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) autres produits frais, surgelés et d'épicerie",
    )

    # per label
    valeur_bio = make_optional_positive_decimal_field(
        verbose_name="Bio - Valeur annuelle HT",
    )
    # TODO: label_rouge, aocaop, igp, stg, hve, peche_durable, rup, commerce_equitable, fermier, externalites, performance ?
    valeur_europe = make_optional_positive_decimal_field(
        verbose_name="Origine UE (hors France) - Valeur annuelle HT",
    )
    valeur_france = make_optional_positive_decimal_field(
        verbose_name="Origine France - Valeur annuelle HT",
    )
    valeur_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Circuit court - Valeur annuelle HT",
    )
    valeur_local = make_optional_positive_decimal_field(
        verbose_name="Local - Valeur annuelle HT",
    )
    definition_local = models.CharField(
        max_length=255, choices=DefinitionLocal.choices, null=True, blank=True, verbose_name="définition de local"
    )
    definition_local_km = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="définition de local (distance en km)", validators=[MinValueValidator(0)]
    )

    # per label group
    # valeur_bio: voir au-dessus
    valeur_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Bio dont commerce équitable - Valeur annuelle HT",
    )
    valeur_siqo = make_optional_positive_decimal_field(
        verbose_name="Produits SIQO (hors bio) - Valeur annuelle HT",
    )
    valeur_externalites_performance = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) prenant en compte les coûts imputés aux externalités environnementales ou leurs performances en matière environnementale",
    )
    valeur_egalim_autres = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) des autres achats EGalim",
    )
    valeur_egalim_autres_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) des achats commerce équitable (hors bio)",
    )

    # other
    valeur_viandes_volailles_egalim = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) viandes et volailles fraiches ou surgelées, EGalim",
    )
    valeur_produits_de_la_mer_egalim = make_optional_positive_decimal_field(
        verbose_name="Valeur totale (HT) poissons et produits aquatiques, EGalim",
    )

    # detailed values
    valeur_viandes_volailles_bio = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Bio",
    )
    valeur_viandes_volailles_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Bio dont commerce équitable",
    )
    valeur_produits_de_la_mer_bio = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Bio",
    )
    valeur_produits_de_la_mer_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Produits aquatiques frais et surgelés, Bio dont commerce équitable",
    )
    valeur_fruits_et_legumes_bio = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Bio",
    )
    valeur_fruits_et_legumes_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Bio dont commerce équitable",
    )
    valeur_charcuterie_bio = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Bio",
    )
    valeur_charcuterie_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Bio dont commerce équitable",
    )
    valeur_produits_laitiers_bio = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio",
    )
    valeur_produits_laitiers_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Bio dont commerce équitable",
    )
    valeur_boulangerie_bio = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Bio",
    )
    valeur_boulangerie_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Bio dont commerce équitable",
    )
    valeur_boissons_bio = make_optional_positive_decimal_field(
        verbose_name="Boissons, Bio",
    )
    valeur_boissons_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Bio dont commerce équitable",
    )
    valeur_autres_bio = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Bio",
    )
    valeur_autres_bio_dont_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Bio dont commerce équitable",
    )
    valeur_viandes_volailles_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Label rouge",
    )
    valeur_produits_de_la_mer_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Label rouge",
    )
    valeur_fruits_et_legumes_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Label rouge",
    )
    valeur_charcuterie_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Label rouge",
    )
    valeur_produits_laitiers_label_rouge = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Label rouge",
    )
    valeur_boulangerie_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Label rouge",
    )
    valeur_autres_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Label rouge",
    )
    valeur_viandes_volailles_aocaop = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, AOC / AOP",
    )
    valeur_produits_de_la_mer_aocaop = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, AOC / AOP",
    )
    valeur_fruits_et_legumes_aocaop = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, AOC / AOP",
    )
    valeur_charcuterie_aocaop = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, AOC / AOP",
    )
    valeur_produits_laitiers_aocaop = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), AOC / AOP",
    )
    valeur_boulangerie_aocaop = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, AOC / AOP",
    )
    valeur_boissons_aocaop = make_optional_positive_decimal_field(
        verbose_name="Boissons, AOC / AOP",
    )
    valeur_autres_aocaop = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, AOC / AOP",
    )
    valeur_viandes_volailles_igp = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, IGP",
    )
    valeur_produits_de_la_mer_igp = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, IGP",
    )
    valeur_fruits_et_legumes_igp = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, IGP",
    )
    valeur_charcuterie_igp = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, IGP",
    )
    valeur_produits_laitiers_igp = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), IGP",
    )
    valeur_boulangerie_igp = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, IGP",
    )
    valeur_boissons_igp = make_optional_positive_decimal_field(
        verbose_name="Boissons, IGP",
    )
    valeur_autres_igp = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, IGP",
    )
    valeur_viandes_volailles_stg = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, STG",
    )
    valeur_produits_de_la_mer_stg = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, STG",
    )
    valeur_fruits_et_legumes_stg = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, STG",
    )
    valeur_charcuterie_stg = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, STG",
    )
    valeur_produits_laitiers_stg = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), STG",
    )
    valeur_boulangerie_stg = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, STG",
    )
    valeur_boissons_stg = make_optional_positive_decimal_field(
        verbose_name="Boissons, STG",
    )
    valeur_autres_stg = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, STG",
    )
    valeur_viandes_volailles_hve = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Haute valeur environnementale",
    )
    valeur_produits_de_la_mer_hve = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Haute valeur environnementale",
    )
    valeur_fruits_et_legumes_hve = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Haute valeur environnementale",
    )
    valeur_charcuterie_hve = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Haute valeur environnementale",
    )
    valeur_produits_laitiers_hve = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Haute valeur environnementale",
    )
    valeur_boulangerie_hve = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Haute valeur environnementale",
    )
    valeur_boissons_hve = make_optional_positive_decimal_field(
        verbose_name="Boissons, Haute valeur environnementale",
    )
    valeur_autres_hve = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Haute valeur environnementale",
    )
    valeur_produits_de_la_mer_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Pêche durable",
    )
    valeur_viandes_volailles_rup = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Région ultrapériphérique",
    )
    valeur_produits_de_la_mer_rup = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Région ultrapériphérique",
    )
    valeur_fruits_et_legumes_rup = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Région ultrapériphérique",
    )
    valeur_charcuterie_rup = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Région ultrapériphérique",
    )
    valeur_produits_laitiers_rup = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Région ultrapériphérique",
    )
    valeur_boulangerie_rup = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Région ultrapériphérique",
    )
    valeur_boissons_rup = make_optional_positive_decimal_field(
        verbose_name="Boissons, Région ultrapériphérique",
    )
    valeur_autres_rup = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Région ultrapériphérique",
    )
    valeur_viandes_volailles_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Commerce équitable",
    )
    valeur_produits_de_la_mer_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Commerce équitable",
    )
    valeur_fruits_et_legumes_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Commerce équitable",
    )
    valeur_charcuterie_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Commerce équitable",
    )
    valeur_produits_laitiers_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Commerce équitable",
    )
    valeur_boulangerie_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Commerce équitable",
    )
    valeur_boissons_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Commerce équitable",
    )
    valeur_autres_commerce_equitable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Commerce équitable",
    )
    valeur_viandes_volailles_fermier = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Fermier",
    )
    valeur_produits_de_la_mer_fermier = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Fermier",
    )
    valeur_fruits_et_legumes_fermier = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Fermier",
    )
    valeur_charcuterie_fermier = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Fermier",
    )
    valeur_produits_laitiers_fermier = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Fermier",
    )
    valeur_boulangerie_fermier = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Fermier",
    )
    valeur_boissons_fermier = make_optional_positive_decimal_field(
        verbose_name="Boissons, Fermier",
    )
    valeur_autres_fermier = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Fermier",
    )
    valeur_viandes_volailles_externalites = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_produits_de_la_mer_externalites = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_fruits_et_legumes_externalites = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_charcuterie_externalites = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_produits_laitiers_externalites = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_boulangerie_externalites = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_boissons_externalites = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_autres_externalites = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    )
    valeur_viandes_volailles_performance = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_produits_de_la_mer_performance = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_fruits_et_legumes_performance = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_charcuterie_performance = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_produits_laitiers_performance = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_boulangerie_performance = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_boissons_performance = make_optional_positive_decimal_field(
        verbose_name="Boissons, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_autres_performance = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Produits acquis sur la base de leurs performances en matière environnementale",
    )
    valeur_viandes_volailles_europe = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Origine UE (hors France)",
    )
    valeur_produits_de_la_mer_europe = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Origine UE (hors France)",
    )
    valeur_fruits_et_legumes_europe = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Origine UE (hors France)",
    )
    valeur_charcuterie_europe = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Origine UE (hors France)",
    )
    valeur_produits_laitiers_europe = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Origine UE (hors France)",
    )
    valeur_boulangerie_europe = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Origine UE (hors France)",
    )
    valeur_boissons_europe = make_optional_positive_decimal_field(
        verbose_name="Boissons, Origine UE (hors France)",
    )
    valeur_autres_europe = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Origine UE (hors France)",
    )
    valeur_viandes_volailles_france = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Origine France",
    )
    valeur_produits_de_la_mer_france = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Origine France",
    )
    valeur_fruits_et_legumes_france = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Origine France",
    )
    valeur_charcuterie_france = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Origine France",
    )
    valeur_produits_laitiers_france = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Origine France",
    )
    valeur_boulangerie_france = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Origine France",
    )
    valeur_boissons_france = make_optional_positive_decimal_field(
        verbose_name="Boissons, Origine France",
    )
    valeur_autres_france = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Origine France",
    )
    valeur_viandes_volailles_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Origine France (dont circuit-court)",
    )
    valeur_produits_de_la_mer_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Origine France (dont circuit-court)",
    )
    valeur_fruits_et_legumes_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Origine France (dont circuit-court)",
    )
    valeur_charcuterie_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Origine France (dont circuit-court)",
    )
    valeur_produits_laitiers_circuit_court = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Origine France (dont circuit-court)",
    )
    valeur_boulangerie_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Origine France (dont circuit-court)",
    )
    valeur_boissons_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Boissons, Origine France (dont circuit-court)",
    )
    valeur_autres_circuit_court = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Origine France (dont circuit-court)",
    )
    valeur_viandes_volailles_local = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Origine France (dont local)",
    )
    valeur_produits_de_la_mer_local = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, Origine France (dont local)",
    )
    valeur_fruits_et_legumes_local = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Origine France (dont local)",
    )
    valeur_charcuterie_local = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Origine France (dont local)",
    )
    valeur_produits_laitiers_local = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Origine France (dont local)",
    )
    valeur_boulangerie_local = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Origine France (dont local)",
    )
    valeur_boissons_local = make_optional_positive_decimal_field(
        verbose_name="Boissons, Origine France (dont local)",
    )
    valeur_autres_local = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Origine France (dont local)",
    )

    # non applicable
    valeur_boissons_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Boissons, Label rouge (non applicable)",
    )
    valeur_viandes_volailles_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, Pêche durable (non applicable)",
    )
    valeur_fruits_et_legumes_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, Pêche durable (non applicable)",
    )
    valeur_charcuterie_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, Pêche durable (non applicable)",
    )
    valeur_produits_laitiers_peche_durable = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), Pêche durable (non applicable)",
    )
    valeur_boulangerie_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, Pêche durable (non applicable)",
    )
    valeur_boissons_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Boissons, Pêche durable (non applicable)",
    )
    valeur_autres_peche_durable = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, Pêche durable (non applicable)",
    )

    # legacy
    valeur_label_rouge = make_optional_positive_decimal_field(
        verbose_name="Valeur label rouge",
    )
    valeur_label_aoc_igp = make_optional_positive_decimal_field(
        verbose_name="Valeur label AOC/AOP/IGP",
    )
    valeur_label_hve = make_optional_positive_decimal_field(
        verbose_name="Valeur label HVE",
    )
    valeur_fair_trade = make_optional_positive_decimal_field(
        verbose_name="Commerce équitable - Valeur annuelle HT",
    )
    valeur_pat = make_optional_positive_decimal_field(
        verbose_name="Produits dans le cadre de Projects Alimentaires Territoriaux - Valeur annuelle HT",
    )
    valeur_viandes_volailles_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, AOC / AOP / IGP / STG",
    )
    valeur_produits_de_la_mer_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, AOC / AOP / IGP / STG",
    )
    valeur_fruits_et_legumes_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, AOC / AOP / IGP / STG",
    )
    valeur_charcuterie_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, AOC / AOP / IGP / STG",
    )
    valeur_produits_laitiers_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), AOC / AOP / IGP / STG",
    )
    valeur_boulangerie_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, AOC / AOP / IGP / STG",
    )
    valeur_boissons_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Boissons, AOC / AOP / IGP / STG",
    )
    valeur_autres_aocaop_igp_stg = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, AOC / AOP / IGP / STG",
    )
    valeur_viandes_volailles_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Viandes et volailles fraîches et surgelées, non-EGalim",
    )
    valeur_produits_de_la_mer_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Poissons, produits de la mer et de l'aquaculture, non-EGalim",
    )
    valeur_fruits_et_legumes_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Fruits et légumes frais et surgelés, non-EGalim",
    )
    valeur_charcuterie_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Charcuterie, non-EGalim",
    )
    valeur_produits_laitiers_non_egalim = make_optional_positive_decimal_field(
        verbose_name="BOF (Produits laitiers, beurre et œufs), non-EGalim",
    )
    valeur_boulangerie_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Boulangerie / Pâtisserie fraîches, non-EGalim",
    )
    valeur_boissons_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Boissons, non-EGalim",
    )
    valeur_autres_non_egalim = make_optional_positive_decimal_field(
        verbose_name="Autres produits frais, surgelés et d'épicerie, non-EGalim",
    )

    # computed: aggregated values
    valeur_bio_agg = make_optional_positive_decimal_field(
        verbose_name="Bio - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_siqo_agg = make_optional_positive_decimal_field(
        verbose_name="Produits SIQO (hors bio) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_externalites_performance_agg = make_optional_positive_decimal_field(
        verbose_name="Externalité/performance - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)",
    )
    valeur_egalim_autres_agg = make_optional_positive_decimal_field(
        verbose_name="Autres achats EGalim - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_egalim_hors_bio_agg = make_optional_positive_decimal_field(
        verbose_name="EGalim (Produits SIQO (hors bio) + Externalité/performance + Autres achats EGalim) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )
    valeur_egalim_agg = make_optional_positive_decimal_field(
        verbose_name="EGalim (Bio + Produits SIQO (hors bio) + Externalité/performance + Autres achats EGalim) - Valeur annuelle HT (en cas de TD détaillée, ce champ est aggrégé)"
    )

    # computed: EGalim
    pourcentage_bio = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage bio (champ calculé)",
    )
    pourcentage_siqo = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage SIQO (champ calculé)",
    )
    pourcentage_externalites_performance = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage externalités/performance (champ calculé)",
    )
    pourcentage_egalim_autres = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage autres EGalim (champ calculé)",
    )
    pourcentage_egalim_hors_bio = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage EGalim hors bio (champ calculé)",
    )
    pourcentage_egalim = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage EGalim (champ calculé)",
    )
    pourcentage_viandes_volailles_egalim = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage viandes et volailles EGalim (champ calculé)",
        help_text="par rapport à la valeur totale viandes et volailles",
    )
    pourcentage_produits_de_la_mer_egalim = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits de la mer EGalim (champ calculé)",
        help_text="par rapport à la valeur totale produits de la mer",
    )
    pourcentage_viandes_volailles_produits_de_la_mer_egalim = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage viandes, volailles et produits de la mer EGalim (champ calculé)",
        help_text="par rapport à la somme de valeur totale viandes et volailles + valeur totale produits de la mer",
    )
    pourcentage_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage origine UE (hors France) (champ calculé)",
    )
    pourcentage_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage origine France (champ calculé)",
    )
    pourcentage_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage circuit court (champ calculé)",
    )
    pourcentage_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage local (champ calculé)",
    )
    pourcentage_viandes_volailles_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage viandes et volailles origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale viandes et volailles",
    )
    pourcentage_produits_de_la_mer_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits de la mer origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale produits de la mer",
    )
    pourcentage_fruits_et_legumes_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage fruits et légumes origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale fruits et légumes",
    )
    pourcentage_charcuterie_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage charcuterie origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale charcuterie",
    )
    pourcentage_produits_laitiers_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits laitiers (BOF) origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale produits laitiers (BOF)",
    )
    pourcentage_boulangerie_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boulangerie / pâtisserie origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale boulangerie / pâtisserie",
    )
    pourcentage_boissons_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boissons origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale boissons",
    )
    pourcentage_autres_europe = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage autres produits origine UE (hors France) (champ calculé)",
        help_text="par rapport à la valeur totale autres produits",
    )
    pourcentage_viandes_volailles_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage viandes et volailles origine France (champ calculé)",
        help_text="par rapport à la valeur totale viandes et volailles",
    )
    pourcentage_produits_de_la_mer_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits de la mer origine France (champ calculé)",
        help_text="par rapport à la valeur totale produits de la mer",
    )
    pourcentage_fruits_et_legumes_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage fruits et légumes origine France (champ calculé)",
        help_text="par rapport à la valeur totale fruits et légumes",
    )
    pourcentage_charcuterie_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage charcuterie origine France (champ calculé)",
        help_text="par rapport à la valeur totale charcuterie",
    )
    pourcentage_produits_laitiers_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits laitiers (BOF) origine France (champ calculé)",
        help_text="par rapport à la valeur totale produits laitiers (BOF)",
    )
    pourcentage_boulangerie_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boulangerie / pâtisserie origine France (champ calculé)",
        help_text="par rapport à la valeur totale boulangerie / pâtisserie",
    )
    pourcentage_boissons_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boissons origine France (champ calculé)",
        help_text="par rapport à la valeur totale boissons",
    )
    pourcentage_autres_france = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage autres produits origine France (champ calculé)",
        help_text="par rapport à la valeur totale autres produits",
    )
    pourcentage_viandes_volailles_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage viandes et volailles circuit court (champ calculé)",
        help_text="par rapport à la valeur totale viandes et volailles",
    )
    pourcentage_produits_de_la_mer_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits de la mer circuit court (champ calculé)",
        help_text="par rapport à la valeur totale produits de la mer",
    )
    pourcentage_fruits_et_legumes_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage fruits et légumes circuit court (champ calculé)",
        help_text="par rapport à la valeur totale fruits et légumes",
    )
    pourcentage_charcuterie_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage charcuterie circuit court (champ calculé)",
        help_text="par rapport à la valeur totale charcuterie",
    )
    pourcentage_produits_laitiers_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits laitiers (BOF) circuit court (champ calculé)",
        help_text="par rapport à la valeur totale produits laitiers (BOF)",
    )
    pourcentage_boulangerie_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boulangerie / pâtisserie circuit court (champ calculé)",
        help_text="par rapport à la valeur totale boulangerie / pâtisserie",
    )
    pourcentage_boissons_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boissons circuit court (champ calculé)",
        help_text="par rapport à la valeur totale boissons",
    )
    pourcentage_autres_circuit_court = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage autres produits circuit court (champ calculé)",
        help_text="par rapport à la valeur totale autres produits",
    )
    pourcentage_viandes_volailles_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage viandes et volailles local (champ calculé)",
        help_text="par rapport à la valeur totale viandes et volailles",
    )
    pourcentage_produits_de_la_mer_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits de la mer local (champ calculé)",
        help_text="par rapport à la valeur totale produits de la mer",
    )
    pourcentage_fruits_et_legumes_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage fruits et légumes local (champ calculé)",
        help_text="par rapport à la valeur totale fruits et légumes",
    )
    pourcentage_charcuterie_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage charcuterie local (champ calculé)",
        help_text="par rapport à la valeur totale charcuterie",
    )
    pourcentage_produits_laitiers_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage produits laitiers (BOF) local (champ calculé)",
        help_text="par rapport à la valeur totale produits laitiers (BOF)",
    )
    pourcentage_boulangerie_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boulangerie / pâtisserie local (champ calculé)",
        help_text="par rapport à la valeur totale boulangerie / pâtisserie",
    )
    pourcentage_boissons_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage boissons local (champ calculé)",
        help_text="par rapport à la valeur totale boissons",
    )
    pourcentage_autres_local = make_optional_positive_percentage_decimal_field(
        verbose_name="pourcentage autres produits local (champ calculé)",
        help_text="par rapport à la valeur totale autres produits",
    )
    objectifs_egalim_atteints = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="objectifs EGalim atteints (champ calculé)",
    )

    class Meta:
        abstract = True
