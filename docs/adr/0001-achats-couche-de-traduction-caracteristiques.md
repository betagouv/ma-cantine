# ADR-0001 : Achats : couche de traduction entre l'ancien et le nouveau format des caractéristiques

- **Statut** : Acceptée
- **Date** : juin 2026 (implémentation : #6807, #6755, #6810, #6841)
- **Auteurs** : équipe ma-cantine

## Contexte

Un achat (`Purchase`) stocke ses labels et ses informations d'origine dans **un seul champ tableau**, `caracteristiques` (`ChoiceArrayField`). On y retrouve des valeurs de natures différentes :

- les catégories EGalim (`BIO`, `LABEL_ROUGE`, `HVE`, `AOCAOP`…), plusieurs valeurs possibles ;
- l'origine (`FRANCE` ou `EUROPE`), une seule valeur possible ;
- `CIRCUIT_COURT`, qui est en réalité un booléen ;
- `LOCAL`, qui est en réalité un booléen, et dont dépendent `definition_local` et `definition_local_km`.

Ce format « liste à plat » pose problème aux utilisateurs qui saisissent ou envoient des achats (imports CSV, éditeurs de logiciels via l'API) :

- il ne dit pas quelles combinaisons sont valides (`FRANCE` + `EUROPE` est interdit, mais rien ne le signale dans le format) ;
- il mélange des notions métier distinctes, ce qui rend les fichiers d'import et la documentation de l'API difficiles à comprendre.

Nous voulions donc exposer un format plus explicite, avec 4 champs : `categories_egalim`, `origine`, `est_circuit_court` et `est_local`.

En parallèle, beaucoup de code s'appuie sur `caracteristiques` tel qu'il est stocké :

- les agrégations utilisées pour les bilans et la télédéclaration (requêtes `caracteristiques__overlap`, `PurchaseSummarySerializer`, remplissage automatique des diagnostics) ;
- les validateurs du modèle (`data/validators/purchase.py`) ;
- l'admin, l'export dbt, les exports Excel ;
- le frontend Vue 2 (`frontend/`) et les endpoints `purchases/` qu'il utilise ;
- les fichiers d'import déjà diffusés aux utilisateurs (ancien format), qu'il faut continuer d'accepter pendant la transition.

## Décision

**Nous gardons le schéma du modèle `Purchase` inchangé** (`caracteristiques` reste la source de vérité en base) et nous ajoutons **une couche de traduction** aux points d'entrée et de sortie, qui convertit le nouveau format en 4 champs vers le format stocké, et inversement.

Concrètement :

| Point d'entrée                                        | Format     | Où se fait la traduction                                                                          |
| ----------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| API `canteens/<id>/purchases/` (éditeurs, nouveau)    | nouveau    | `PurchaseSerializer.to_internal_value()` / `to_representation()` (`api/serializers/purchase.py`) |
| Import CSV (`importPurchases/`, schémas `achats_*.json`) | nouveau | `PurchasesImportView._get_caracteristiques()` (`api/views/purchase_import.py`)                     |
| Import CSV (`importPurchasesOld/`, schémas `achats_*_old.json`) | ancien | `PurchasesImportOldView` (`api/views/purchase_import_old.py`) : passe-plat + conversion des anciennes valeurs de `definition_local` |
| API `purchases/` (frontend Vue 2)                     | ancien     | `PurchaseOldSerializer` : pas de traduction                                                       |

Les imports partagent leur logique dans `BasePurchasesImportView` (`api/views/purchase_import_base.py`). Chaque format ne surcharge que l'extraction des champs (`_get_schema_config`, `_get_caracteristiques`, `_get_definition_local`, `_get_definition_local_km`).

Côté modèle, des propriétés en lecture seule (`categories_egalim`, `origine`, `est_circuit_court`, `est_local`) exposent la vue « 4 champs » à partir de `caracteristiques`, pour le code Python qui en a besoin.

La validation métier reste **dans le modèle** (`Purchase.clean()`, appelée par `save()`). Elle s'applique donc de la même façon quel que soit le point d'entrée.

## Alternatives considérées

### 1. Migrer le schéma : 4 colonnes en base

Remplacer `caracteristiques` par `categories_egalim` (tableau), `origine` (choix), `est_circuit_court` et `est_local` (booléens).

- ✅ Modèle plus explicite, contraintes exprimables en base.
- ❌ Migration de données sur tous les achats existants.
- ❌ Il faut réécrire toutes les agrégations (bilans, télédéclaration, remplissage automatique), l'admin, les exports et l'export dbt, **en même temps**.
- ❌ Il faut quand même une traduction pour l'ancien format (Vue 2, anciens imports) : on déplace la couche de traduction au lieu de la supprimer.
- ❌ Risque élevé pendant une campagne de télédéclaration.

### 2. Stocker les deux formats en base (dénormalisation)

Ajouter les 4 colonnes tout en gardant `caracteristiques`, et les synchroniser.

- ❌ Deux sources de vérité, risque de désynchronisation.
- ❌ Migration nécessaire quand même, sans retirer aucune complexité.

### 3. Remplacer directement l'ancien format partout

- ❌ Casse les fichiers d'import déjà utilisés par les gestionnaires et le frontend Vue 2, sans période de transition.

## Conséquences

### Positives

- Aucune migration de données, aucun changement sur les agrégations, la télédéclaration, l'admin ou les exports.
- Les éditeurs (API) et les nouveaux imports utilisent un format explicite et documenté (OpenAPI via drf-spectacular, schémas TableSchema).
- L'ancien et le nouveau format coexistent : la transition peut être progressive.
- Toute la validation reste dans le modèle, donc cohérente entre l'API, les imports et l'admin.

### Négatives / points de vigilance

- **Deux représentations du même concept** : il faut connaître le mapping pour passer de l'API à la base (et inversement), par exemple pendant le débogage ou l'analyse de données.
- **Logique de traduction dupliquée** à plusieurs endroits (serializer, vue d'import, propriétés du modèle). Si on ajoute une caractéristique, il faut mettre à jour `CHARACTERISTIC_LABELS_EGALIM` / `CHARACTERISTIC_LABELS_ORIGINE`, puis vérifier chaque point de traduction.
- **Mises à jour partielles (PATCH)** : `caracteristiques` est reconstruit à partir des 4 champs. Pour ne pas écraser les champs absents de la requête, le serializer complète les champs manquants avec les valeurs déjà stockées (et ne touche pas à `caracteristiques` si aucun des 4 champs n'est envoyé).
- Les messages d'erreur de validation du modèle portent sur `caracteristiques`, alors que l'utilisateur du nouveau format a envoyé `origine`, `est_local`, etc.
- Le code « Old » (`PurchaseOldSerializer`, `PurchasesImportOldView`, schémas `achats_*_old.json`, pages `*Old.vue`) devient de la dette, à supprimer explicitement.

## Suite

Cette couche de traduction est une **étape de transition**. Conditions pour la simplifier :

1. Le frontend Vue 2 n'utilise plus les endpoints `purchases/`. On peut alors supprimer `PurchaseOldSerializer`.
2. L'ancien format d'import n'est plus utilisé (à suivre via `import_source` / les statistiques d'import). On peut alors supprimer `PurchasesImportOldView` et les schémas `*_old.json`.
3. Une fois ces deux étapes faites, il ne reste plus que le nouveau format en entrée. On pourra alors réévaluer l'alternative 1 (4 colonnes en base) dans un nouvel ADR.
