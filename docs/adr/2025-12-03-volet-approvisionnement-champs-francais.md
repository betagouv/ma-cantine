# ADR : Volet approvisionnement : noms de champs en français

- Statut : acceptée
- Date : 03/12/2025 (merge sur `staging`, en prod le même jour avec la release 2025.41.1)
- PRs : #5951, #5953 (1/3), #5956 (2/3), #5959 (3/3), #5965

## Contexte

- Les champs du volet approvisionnement des bilans (`Diagnostic`) mélangeaient l'anglais et le français : `value_meat_poultry_ht` et `value_fish_ht` côté bilan simplifié, `value_viandes_volailles_bio` et `value_produits_de_la_mer_bio` côté bilan détaillé.
- Le suffixe `_ht` n'apportait rien : toutes les valeurs sont hors taxes.
- Les fichiers d'import utilisaient déjà le préfixe `valeur_`.
- Le renommage a été fait juste avant l'ouverture de la campagne 2026 (données 2025, ouverte le 12/01/2026), en même temps que l'ajout des champs « dont commerce équitable ».

## Décision

1. Les champs du volet approvisionnement sont renommés en français, en base (`diagnostic` & `historicaldiagnostic`) et dans l'API.
2. Règles appliquées :
   - le préfixe `value_` devient `valeur_` ;
   - le suffixe `_ht` est enlevé ;
   - `meat_poultry` devient `viandes_volailles`, `fish` devient `produits_de_la_mer` ;
   - les autres mots anglais sont traduits : `total` → `totale`, `sustainable` → `siqo`, `externality_performance` → `externalites_performance`, `egalim_others` → `egalim_autres` ;
   - `short_distribution` devient `circuit_court` (#5965).
3. `value_meat_poultry_france_ht` (bilan simplifié) est supprimé : le bilan simplifié utilise désormais `valeur_viandes_volailles_france`, le champ du bilan détaillé.
4. Ce volet n'a pas de champ à choix : seuls les noms de champs changent.

## Champs du bilan simplifié & champs agrégés (#5951, #5953, #5956, #5959)

| Ancien nom | Nouveau nom |
|-|-|
| `value_total_ht` | `valeur_totale` |
| `value_bio_ht` | `valeur_bio` |
| `value_bio_dont_commerce_equitable_ht` | `valeur_bio_dont_commerce_equitable` |
| `value_sustainable_ht` | `valeur_siqo` |
| `value_externality_performance_ht` | `valeur_externalites_performance` |
| `value_egalim_others_ht` | `valeur_egalim_autres` |
| `value_commerce_equitable_ht` | `valeur_egalim_autres_dont_commerce_equitable` |
| `value_meat_poultry_ht` | `valeur_viandes_volailles` |
| `value_meat_poultry_egalim_ht` | `valeur_viandes_volailles_egalim` |
| `value_meat_poultry_france_ht` | supprimé, remplacé par `valeur_viandes_volailles_france` |
| `value_fish_ht` | `valeur_produits_de_la_mer` |
| `value_fish_egalim_ht` | `valeur_produits_de_la_mer_egalim` |
| `value_bio_ht_agg` | `valeur_bio_agg` |
| `value_sustainable_ht_agg` | `valeur_siqo_agg` |
| `value_externality_performance_ht_agg` | `valeur_externalites_performance_agg` |
| `value_egalim_others_ht_agg` | `valeur_egalim_autres_agg` |
| `value_egalim_hors_bio_ht_agg` | `valeur_egalim_hors_bio_agg` |
| `value_egalim_ht_agg` | `valeur_egalim_agg` |

Les champs « dont commerce équitable » (`value_bio_dont_commerce_equitable_ht`, `value_commerce_equitable_ht`, et ceux du bilan détaillé) ont été créés le 28/11/2025 (#5907), quelques jours avant le renommage. Ils ne contiennent des données que sous leurs nouveaux noms, à partir de la campagne 2026 (données 2025).

Anciens champs, plus demandés depuis la version 9 des TD (données 2022), renommés eux aussi :

| Ancien nom | Nouveau nom |
|-|-|
| `value_label_rouge` | `valeur_label_rouge` |
| `value_label_aoc_igp` | `valeur_label_aoc_igp` |
| `value_label_hve` | `valeur_label_hve` |
| `value_fair_trade_ht` | `valeur_fair_trade` |
| `value_pat_ht` | `valeur_pat` |

## Champs du bilan détaillé (#5959, #5965)

Les champs du bilan détaillé (une famille de produits × un label ou une caractéristique) étaient déjà en français : seuls le préfixe (`value_` → `valeur_`) et `short_distribution` (→ `circuit_court`) changent. Tous les champs sont listés ci-dessous, famille par famille.

### Famille `viandes_volailles`

| Ancien nom | Nouveau nom |
|-|-|
| `value_viandes_volailles_aocaop_igp_stg` | `valeur_viandes_volailles_aocaop_igp_stg` |
| `value_viandes_volailles_bio` | `valeur_viandes_volailles_bio` |
| `value_viandes_volailles_bio_dont_commerce_equitable` | `valeur_viandes_volailles_bio_dont_commerce_equitable` |
| `value_viandes_volailles_commerce_equitable` | `valeur_viandes_volailles_commerce_equitable` |
| `value_viandes_volailles_externalites` | `valeur_viandes_volailles_externalites` |
| `value_viandes_volailles_fermier` | `valeur_viandes_volailles_fermier` |
| `value_viandes_volailles_france` | `valeur_viandes_volailles_france` |
| `value_viandes_volailles_hve` | `valeur_viandes_volailles_hve` |
| `value_viandes_volailles_label_rouge` | `valeur_viandes_volailles_label_rouge` |
| `value_viandes_volailles_local` | `valeur_viandes_volailles_local` |
| `value_viandes_volailles_non_egalim` | `valeur_viandes_volailles_non_egalim` |
| `value_viandes_volailles_peche_durable` | `valeur_viandes_volailles_peche_durable` |
| `value_viandes_volailles_performance` | `valeur_viandes_volailles_performance` |
| `value_viandes_volailles_rup` | `valeur_viandes_volailles_rup` |
| `value_viandes_volailles_short_distribution` | `valeur_viandes_volailles_circuit_court` |

### Famille `produits_de_la_mer`

| Ancien nom | Nouveau nom |
|-|-|
| `value_produits_de_la_mer_aocaop_igp_stg` | `valeur_produits_de_la_mer_aocaop_igp_stg` |
| `value_produits_de_la_mer_bio` | `valeur_produits_de_la_mer_bio` |
| `value_produits_de_la_mer_bio_dont_commerce_equitable` | `valeur_produits_de_la_mer_bio_dont_commerce_equitable` |
| `value_produits_de_la_mer_commerce_equitable` | `valeur_produits_de_la_mer_commerce_equitable` |
| `value_produits_de_la_mer_externalites` | `valeur_produits_de_la_mer_externalites` |
| `value_produits_de_la_mer_fermier` | `valeur_produits_de_la_mer_fermier` |
| `value_produits_de_la_mer_france` | `valeur_produits_de_la_mer_france` |
| `value_produits_de_la_mer_hve` | `valeur_produits_de_la_mer_hve` |
| `value_produits_de_la_mer_label_rouge` | `valeur_produits_de_la_mer_label_rouge` |
| `value_produits_de_la_mer_local` | `valeur_produits_de_la_mer_local` |
| `value_produits_de_la_mer_non_egalim` | `valeur_produits_de_la_mer_non_egalim` |
| `value_produits_de_la_mer_peche_durable` | `valeur_produits_de_la_mer_peche_durable` |
| `value_produits_de_la_mer_performance` | `valeur_produits_de_la_mer_performance` |
| `value_produits_de_la_mer_rup` | `valeur_produits_de_la_mer_rup` |
| `value_produits_de_la_mer_short_distribution` | `valeur_produits_de_la_mer_circuit_court` |

### Famille `fruits_et_legumes`

| Ancien nom | Nouveau nom |
|-|-|
| `value_fruits_et_legumes_aocaop_igp_stg` | `valeur_fruits_et_legumes_aocaop_igp_stg` |
| `value_fruits_et_legumes_bio` | `valeur_fruits_et_legumes_bio` |
| `value_fruits_et_legumes_bio_dont_commerce_equitable` | `valeur_fruits_et_legumes_bio_dont_commerce_equitable` |
| `value_fruits_et_legumes_commerce_equitable` | `valeur_fruits_et_legumes_commerce_equitable` |
| `value_fruits_et_legumes_externalites` | `valeur_fruits_et_legumes_externalites` |
| `value_fruits_et_legumes_fermier` | `valeur_fruits_et_legumes_fermier` |
| `value_fruits_et_legumes_france` | `valeur_fruits_et_legumes_france` |
| `value_fruits_et_legumes_hve` | `valeur_fruits_et_legumes_hve` |
| `value_fruits_et_legumes_label_rouge` | `valeur_fruits_et_legumes_label_rouge` |
| `value_fruits_et_legumes_local` | `valeur_fruits_et_legumes_local` |
| `value_fruits_et_legumes_non_egalim` | `valeur_fruits_et_legumes_non_egalim` |
| `value_fruits_et_legumes_peche_durable` | `valeur_fruits_et_legumes_peche_durable` |
| `value_fruits_et_legumes_performance` | `valeur_fruits_et_legumes_performance` |
| `value_fruits_et_legumes_rup` | `valeur_fruits_et_legumes_rup` |
| `value_fruits_et_legumes_short_distribution` | `valeur_fruits_et_legumes_circuit_court` |

### Famille `charcuterie`

| Ancien nom | Nouveau nom |
|-|-|
| `value_charcuterie_aocaop_igp_stg` | `valeur_charcuterie_aocaop_igp_stg` |
| `value_charcuterie_bio` | `valeur_charcuterie_bio` |
| `value_charcuterie_bio_dont_commerce_equitable` | `valeur_charcuterie_bio_dont_commerce_equitable` |
| `value_charcuterie_commerce_equitable` | `valeur_charcuterie_commerce_equitable` |
| `value_charcuterie_externalites` | `valeur_charcuterie_externalites` |
| `value_charcuterie_fermier` | `valeur_charcuterie_fermier` |
| `value_charcuterie_france` | `valeur_charcuterie_france` |
| `value_charcuterie_hve` | `valeur_charcuterie_hve` |
| `value_charcuterie_label_rouge` | `valeur_charcuterie_label_rouge` |
| `value_charcuterie_local` | `valeur_charcuterie_local` |
| `value_charcuterie_non_egalim` | `valeur_charcuterie_non_egalim` |
| `value_charcuterie_peche_durable` | `valeur_charcuterie_peche_durable` |
| `value_charcuterie_performance` | `valeur_charcuterie_performance` |
| `value_charcuterie_rup` | `valeur_charcuterie_rup` |
| `value_charcuterie_short_distribution` | `valeur_charcuterie_circuit_court` |

### Famille `produits_laitiers`

| Ancien nom | Nouveau nom |
|-|-|
| `value_produits_laitiers_aocaop_igp_stg` | `valeur_produits_laitiers_aocaop_igp_stg` |
| `value_produits_laitiers_bio` | `valeur_produits_laitiers_bio` |
| `value_produits_laitiers_bio_dont_commerce_equitable` | `valeur_produits_laitiers_bio_dont_commerce_equitable` |
| `value_produits_laitiers_commerce_equitable` | `valeur_produits_laitiers_commerce_equitable` |
| `value_produits_laitiers_externalites` | `valeur_produits_laitiers_externalites` |
| `value_produits_laitiers_fermier` | `valeur_produits_laitiers_fermier` |
| `value_produits_laitiers_france` | `valeur_produits_laitiers_france` |
| `value_produits_laitiers_hve` | `valeur_produits_laitiers_hve` |
| `value_produits_laitiers_label_rouge` | `valeur_produits_laitiers_label_rouge` |
| `value_produits_laitiers_local` | `valeur_produits_laitiers_local` |
| `value_produits_laitiers_non_egalim` | `valeur_produits_laitiers_non_egalim` |
| `value_produits_laitiers_peche_durable` | `valeur_produits_laitiers_peche_durable` |
| `value_produits_laitiers_performance` | `valeur_produits_laitiers_performance` |
| `value_produits_laitiers_rup` | `valeur_produits_laitiers_rup` |
| `value_produits_laitiers_short_distribution` | `valeur_produits_laitiers_circuit_court` |

### Famille `boulangerie`

| Ancien nom | Nouveau nom |
|-|-|
| `value_boulangerie_aocaop_igp_stg` | `valeur_boulangerie_aocaop_igp_stg` |
| `value_boulangerie_bio` | `valeur_boulangerie_bio` |
| `value_boulangerie_bio_dont_commerce_equitable` | `valeur_boulangerie_bio_dont_commerce_equitable` |
| `value_boulangerie_commerce_equitable` | `valeur_boulangerie_commerce_equitable` |
| `value_boulangerie_externalites` | `valeur_boulangerie_externalites` |
| `value_boulangerie_fermier` | `valeur_boulangerie_fermier` |
| `value_boulangerie_france` | `valeur_boulangerie_france` |
| `value_boulangerie_hve` | `valeur_boulangerie_hve` |
| `value_boulangerie_label_rouge` | `valeur_boulangerie_label_rouge` |
| `value_boulangerie_local` | `valeur_boulangerie_local` |
| `value_boulangerie_non_egalim` | `valeur_boulangerie_non_egalim` |
| `value_boulangerie_peche_durable` | `valeur_boulangerie_peche_durable` |
| `value_boulangerie_performance` | `valeur_boulangerie_performance` |
| `value_boulangerie_rup` | `valeur_boulangerie_rup` |
| `value_boulangerie_short_distribution` | `valeur_boulangerie_circuit_court` |

### Famille `boissons`

| Ancien nom | Nouveau nom |
|-|-|
| `value_boissons_aocaop_igp_stg` | `valeur_boissons_aocaop_igp_stg` |
| `value_boissons_bio` | `valeur_boissons_bio` |
| `value_boissons_bio_dont_commerce_equitable` | `valeur_boissons_bio_dont_commerce_equitable` |
| `value_boissons_commerce_equitable` | `valeur_boissons_commerce_equitable` |
| `value_boissons_externalites` | `valeur_boissons_externalites` |
| `value_boissons_fermier` | `valeur_boissons_fermier` |
| `value_boissons_france` | `valeur_boissons_france` |
| `value_boissons_hve` | `valeur_boissons_hve` |
| `value_boissons_label_rouge` | `valeur_boissons_label_rouge` |
| `value_boissons_local` | `valeur_boissons_local` |
| `value_boissons_non_egalim` | `valeur_boissons_non_egalim` |
| `value_boissons_peche_durable` | `valeur_boissons_peche_durable` |
| `value_boissons_performance` | `valeur_boissons_performance` |
| `value_boissons_rup` | `valeur_boissons_rup` |
| `value_boissons_short_distribution` | `valeur_boissons_circuit_court` |

### Famille `autres`

| Ancien nom | Nouveau nom |
|-|-|
| `value_autres_aocaop_igp_stg` | `valeur_autres_aocaop_igp_stg` |
| `value_autres_bio` | `valeur_autres_bio` |
| `value_autres_bio_dont_commerce_equitable` | `valeur_autres_bio_dont_commerce_equitable` |
| `value_autres_commerce_equitable` | `valeur_autres_commerce_equitable` |
| `value_autres_externalites` | `valeur_autres_externalites` |
| `value_autres_fermier` | `valeur_autres_fermier` |
| `value_autres_france` | `valeur_autres_france` |
| `value_autres_hve` | `valeur_autres_hve` |
| `value_autres_label_rouge` | `valeur_autres_label_rouge` |
| `value_autres_local` | `valeur_autres_local` |
| `value_autres_non_egalim` | `valeur_autres_non_egalim` |
| `value_autres_peche_durable` | `valeur_autres_peche_durable` |
| `value_autres_performance` | `valeur_autres_performance` |
| `value_autres_rup` | `valeur_autres_rup` |
| `value_autres_short_distribution` | `valeur_autres_circuit_court` |

## Conséquences

### Données

- **Réponses : inchangées.** Seuls les noms de colonnes changent (`RenameField`), sauf `value_meat_poultry_france_ht`, supprimé sans reprise de ses valeurs (migration `0224`).
- Les bilans simplifiés renseignent désormais `valeur_viandes_volailles_france`, comme les bilans détaillés.

### Entrepôt, dbt & Metabase

- dbt (créé en 09/2026) ne connaît que les nouveaux noms : `stg_diagnostics`, `stg_teledeclarations` et `mart_teledeclarations` lisent les colonnes `valeur_*`.
- Les anciennes tables et questions Metabase construites avant le 03/12/2025 utilisent les anciens noms (`value_*_ht`) : pour les relire, utiliser les tableaux ci-dessus.
- Les champs des achats ont été renommés en français le 02/06/2026, voir `2026-06-02-achats-champs-francais.md`. `short_distribution` → `circuit_court` change aussi une valeur de `Purchase.characteristics` (#5965).
