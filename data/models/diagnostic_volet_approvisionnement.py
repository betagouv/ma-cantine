from django.core.validators import MinValueValidator
from django.db import models

from data.models.definitionlocal import DefinitionLocal
from data.utils import make_optional_positive_decimal_field, make_optional_positive_integer_field


class DiagnosticVoletApprovisionnementMixin(models.Model):
    """
    Volet approvisionnement (computed fields like *_agg & pourcentage_* stay in Diagnostic)
    """

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

    class Meta:
        abstract = True
