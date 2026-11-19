# ADR : Achats : noms de champs en français

- Statut : acceptée
- Date : 02/06/2026 (merge sur `staging`, en prod le 08/06/2026 avec la release 2026.37.0)
- PRs : #6765, #6755 & #6810 (nouvelle API), #6809 (ancienne API)

## Contexte

- Les champs des bilans sont en français depuis le 03/12/2025 (`valeur_*`, voir l'ADR du volet approvisionnement). Les champs des achats (`Purchase`) étaient encore en anglais.
- Les fichiers d'import d'achats utilisaient déjà les noms français (`fournisseur`, `prix_ht`, `famille_produits`, `caracteristiques`, `definition_local`) : le nommage part de là.
- Une nouvelle API des achats (#6755) allait diviser `caracteristiques` en 4 champs : autant la faire directement en français.
- Les valeurs de choix étaient déjà en français (`VIANDES_VOLAILLES`, `BIO`, `CIRCUIT_COURT`…).

## Décision

1. Les champs du modèle `Purchase` sont renommés en français, en base (`data_purchase`, migration `0261`).
2. La nouvelle API (`canteens/<id>/purchases/`, #6755 & #6810) utilise les noms français.
3. L'ancienne API (`purchases/`, `PurchaseOldSerializer`, #6809) garde les noms anglais (ancien frontend Vue 2), par une traduction dans le serializer.
4. Les valeurs de choix ne changent pas avec ce renommage.

## Champs (#6765)

| Ancien nom | Nouveau nom |
|-|-|
| `provider` | `fournisseur` |
| `family` | `famille_produits` |
| `characteristics` | `caracteristiques` |
| `price_ht` | `prix_ht` |
| `invoice_file` | `facture` |
| `local_definition` | `definition_local` |

Champs inchangés : `canteen`, `date`, `description`, `category` (plus utilisé), `import_source`, `creation_source`…

Propriétés renommées (utilisées par l'export Excel) : `readable_family` → `famille_produits_display`, `readable_characteristics` → `caracteristiques_display`.

## Valeurs de choix renommées avant

Deux valeurs avaient déjà été traduites, avec réécriture en base :

| Champ | Ancienne valeur | Nouvelle valeur | PR & migration |
|-|-|-|-|
| `characteristics` | `SHORT_DISTRIBUTION` | `CIRCUIT_COURT` | #5965 (03/12/2025), `0227` |
| `local_definition` | `DEPARTMENT` | `DEPARTEMENT` | #6042 (17/12/2025), `0229` |

## Conséquences

### Données

- **Réponses : inchangées.** Seuls les noms de colonnes changent (`RenameField`).

### API

- Nouvelle API (`canteens/<id>/purchases/`) : noms français, et `caracteristiques` divisé en 4 champs (`categories_egalim`, `origine`, `est_circuit_court`, `est_local`).
- Ancienne API (`purchases/`) : noms anglais (`provider`, `family`, `characteristics`, `price_ht`, `invoice_file`, `local_definition`), y compris pour les filtres (`?family=`, `?characteristics=`).

### Entrepôt & Metabase

- `purchases_raw` (exportée depuis le 17/03/2026) : les colonnes changent de nom à partir du 08/06/2026. Les questions Metabase qui utilisent les anciens noms (`price_ht`, `family`, `characteristics`…) cassent : utiliser le tableau ci-dessus.
- dbt (créé en 09/2026) n'utilise pas les colonnes de `purchases_raw`.
