# ADR : Volets thématiques : noms de champs & valeurs de choix en français

- Statut : acceptée
- Date : 04/11/2026 (merge sur `staging`)
- PRs : #7447 (diversification), #7449 (gaspillage), #7513 (information), #7514 (plastique)

## Contexte

- Les champs du volet approvisionnement sont déjà en français (version 16 des TD, `valeur_*`). Les 4 autres volets (diversification, gaspillage, information, plastique) avaient encore des noms et des valeurs de choix en anglais.
- L'API v2 des bilans (#7435) expose un endpoint par volet. Elle sera ouverte aux partenaires : les noms doivent être fixés avant, pour ne pas la casser ensuite.

## Décision

1. Les champs des 4 volets sont renommés en français, en base (`diagnostic` & `historicaldiagnostic`) et dans l'API v2.
2. Les valeurs de choix sont traduites en français et **réécrites en base pour toutes les années** (migrations `0297` à `0300`, réversibles).
3. L'API v1 garde les noms et les valeurs en anglais (tunnel Vue 2), par une traduction à l'entrée et à la sortie de l'API.

## Champs, volet par volet

### Diversification (#7447)

| Ancien nom | Nouveau nom |
|-|-|
| `has_diversification_plan` | `plan_diversification_en_place` |
| `diversification_plan_actions` | `plan_diversification_actions` |
| `service_type` | `service_type` (inchangé) |
| `vegetarian_weekly_recurrence` | `menu_vegetarien_frequence` |
| `vegetarian_menu_type` | `menu_vegetarien_type` |
| `vegetarian_menu_bases` | `menu_vegetarien_bases` |

| Champ | Ancienne valeur | Nouvelle valeur |
|-|-|-|
| `service_type` | `UNIQUE` | `MENU_UNIQUE` |
| `service_type` | `MULTIPLE_SELF` | `CHOIX_MULTIPLE_LIBRE_SERVICE` |
| `service_type` | `MULTIPLE_RESERVATION` | `CHOIX_MULTIPLE_RESERVATION` |
| `menu_vegetarien_frequence` | `NEVER` | `JAMAIS` |
| `menu_vegetarien_frequence` | `LOW` | `MOINS_HEBDO` |
| `menu_vegetarien_frequence` | `MID` | `HEBDO` |
| `menu_vegetarien_frequence` | `HIGH` | `PLUS_HEBDO` |
| `menu_vegetarien_frequence` | `DAILY` | `QUOTIDIEN` |
| `plan_diversification_actions` | `PRODUCTS` | `PLATS_PRODUITS` |
| `plan_diversification_actions` | `TRAINING` | `FORMATION` |
| `menu_vegetarien_bases` | `GRAIN` | `CEREALES_LEGUMINEUSES` |
| `menu_vegetarien_bases` | `SOY` | `SOJA` |
| `menu_vegetarien_bases` | `CHEESE` | `FROMAGE` |
| `menu_vegetarien_bases` | `EGG` | `OEUFS` |
| `menu_vegetarien_bases` | `READYMADE` | `PLATS_PRETS_A_L_EMPLOI` |

Valeurs inchangées : `PRESENTATION`, `MENU`, `PROMOTION` (`plan_diversification_actions`), toutes celles de `menu_vegetarien_type`.

### Gaspillage (#7449)

| Ancien nom | Nouveau nom |
|-|-|
| `has_waste_diagnostic` | `diagnostic_gaspillage_realise` |
| `has_waste_plan` | `plan_gaspillage_en_place` |
| `has_waste_measures` | `mesures_gaspillage_realisees` |
| `waste_actions` | `actions_gaspillage_realisees` |
| `other_waste_action` | `actions_gaspillage_autre` |
| `has_donation_agreement` | `dons_convention` |
| `donation_frequency` | `dons_frequence` |
| `donation_quantity` | `dons_quantite` |
| `donation_food_type` | `dons_type_denrees` |
| `other_waste_comments` | `commentaires_gaspillage_autre` |
| `total_leftovers` | `dechets_total` |
| `duration_leftovers_measurement` | `dechets_mesure_duree` |
| `bread_leftovers` | `dechets_pain` |
| `served_leftovers` | `dechets_plateau` |
| `unserved_leftovers` | `dechets_non_servis` |
| `side_leftovers` | `dechets_composantes` |

| Champ | Ancienne valeur | Nouvelle valeur |
|-|-|-|
| `actions_gaspillage_realisees` | `AWARENESS` | `SENSIBILISATION` |
| `actions_gaspillage_realisees` | `TRAINING` | `FORMATION` |
| `actions_gaspillage_realisees` | `REUSE` | `REUTILISATION` |

Valeurs inchangées : `INSCRIPTION`, `DISTRIBUTION`, `PORTIONS`.

### Information des convives (#7513)

| Ancien nom | Nouveau nom |
|-|-|
| `communication_supports` | `information_supports` |
| `other_communication_support` | `information_supports_autre` |
| `communication_support_url` | `information_support_url` |
| `communicates_on_food_plan` | `information_qualite_nutritionnelle` |
| `communicates_on_food_quality` | `information_qualite_durable` |
| `communication_frequency` | `information_frequence` |

| Champ | Ancienne valeur | Nouvelle valeur |
|-|-|-|
| `information_supports` | `DISPLAY` | `AFFICHAGE` |
| `information_supports` | `WEBSITE` | `SITE_INTERNET` |
| `information_supports` | `OTHER` | `AUTRE` |
| `information_supports` | `DIGITAL` | `ELECTRONIQUE` |
| `information_frequence` | `REGULARLY` | `REGULIEREMENT` |
| `information_frequence` | `YEARLY` | `ANNUELLE` |
| `information_frequence` | `LESS_THAN_YEARLY` | `MOINS_QUE_ANNUELLE` |

Valeur inchangée : `EMAIL` (`information_supports`).

### Substitution des plastiques (#7514)

| Ancien nom | Nouveau nom |
|-|-|
| `cooking_plastic_substituted` | `plastique_contenant_cuisson_remplace` |
| `serving_plastic_substituted` | `plastique_contenant_service_remplace` |
| `plastic_bottles_substituted` | `plastique_bouteille_remplace` |
| `plastic_tableware_substituted` | `plastique_ustensile_remplace` |

Pas de choix sur ce volet (que des booléens).

## Conséquences

### Données

- **Valeurs de choix : réécrites en base pour toutes les années.** Il n'y a pas de mélange de valeurs anglaises et françaises : les comparaisons d'une année à l'autre restent cohérentes.
- **Réponses : inchangées.** Seuls les noms de colonnes et les codes de valeurs changent.
- L'API v1 (et donc les payloads des requêtes v1 journalisées dans EventLog) garde les noms et les valeurs en anglais.

### Entrepôt & dbt

- `diagnostics_raw` : les colonnes changent de nom, donc l'ETL recrée la table (`DROP TABLE … CASCADE`). Les vues créées à la main sur cette table sont supprimées. dbt doit tourner après l'ETL (ordre déjà en place la nuit).
- `stg_diagnostics` : les colonnes des 4 volets prennent les nouveaux noms. En prod, les modèles staging & intermediate sont `ephemeral` : ils n'existent pas comme tables.
- `mart_teledeclarations` : **noms de colonnes inchangés**, mais 4 colonnes contiennent les valeurs en français : `type_service`, `recurrence_vege`, `bases_menu_vege`, `actions_plan_diversification`. Les colonnes dérivées (`choix_multiple`, `atteint_vege_quotidien`, `action_gaspi_inscription`, `action_gaspi_sensibilisation`, `action_gaspi_formation`, `action_gaspi_distribution`, `action_gaspi_portions`, `action_gaspi_reutilisation`) sont déjà adaptées.
- Open data (data.gouv) : pas d'impact (seuls les champs cantine & appro sont exportés).

### Metabase

- Les questions sur `diagnostics_raw` qui utilisent les anciens noms de colonnes cassent, en SQL comme dans l'éditeur graphique. Après la synchronisation, les anciennes colonnes disparaissent et les nouvelles arrivent sans leurs métadonnées (nom d'affichage, type sémantique).
- Les filtres sur les anciennes valeurs (`'UNIQUE'`, `'DAILY'`, `'AWARENESS'`, `'DISPLAY'`…) ne renvoient plus rien, sans erreur.
- Pour les trouver : chercher les anciens noms et valeurs ci-dessus dans le SQL des questions, ou interroger la base applicative de Metabase (`report_card`).
