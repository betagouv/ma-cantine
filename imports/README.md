# Application `imports`

## Objectif

Cette application regroupe les imports de masse de fichiers CSV / Excel : cantines, bilans & achats.

## URLs

Endpoints (authentifiés) :

- `/api/v1/importCanteens/create/` & `/api/v1/importCanteens/update/`
- `/api/v1/importCanteensManagers/`
- `/api/v1/importDiagnostics/simple/` & `/api/v1/importDiagnostics/complete/`
- `/api/v1/importPurchases/` & `/api/v1/importPurchasesOld/`

Le routage est délégué par `api/urls.py` vers `imports/urls.py`.

## Fonctionnement

Toutes les vues héritent de `BaseImportView` (`imports/views/base.py`) :

1. validation de la taille du fichier
2. validation du fichier via l'API [Validata](https://validata.fr) :
   - en-tête : détection du schéma utilisé par le fichier, parmi les schémas acceptés par l'import (`_get_schemas()`)
   - lignes : contre le schéma détecté
3. traitement des lignes (permissions, création / mise à jour) dans une transaction
4. log du résultat (`ImportFailure` en cas d'échec)

## Schémas

Chaque import déclare la liste des schémas qu'il accepte (`ImportSchema`, dans `imports/schemas.py`) :

- le schéma utilisé est celui dont l'en-tête correspond **exactement** à l'en-tête du fichier
- si aucun ne correspond, les erreurs d'en-tête sont calculées par rapport au premier schéma de la liste (celui par défaut)

Ajouter un schéma :

1. ajouter le fichier dans `data/schemas/imports/`
2. l'ajouter dans la liste des schémas acceptés par l'import (`_get_schemas()`)

## Ce qui reste ailleurs

- schémas : `data/schemas/imports/` (Validata les lit depuis GitHub, sur la branche `GIT_BRANCH`)
- génération des schémas de bilans : `macantine/management/commands/generate_import_schema.py`
- `ImportType` & `ImportFailure` : `data/models/importtype.py` & `data/models/importfailure.py`
- utilitaires : `common/utils/file_import.py` & `common/api/validata.py` (aussi utilisés hors imports)

## À faire

- déplacer `ImportType` & `ImportFailure` dans `imports/models/` (migration `SeparateDatabaseAndState` en gardant la table `data_importfailure`, renommer le content type, adapter le test de la migration 0287). À moins de supprimer `ImportFailure` au profit d'`EventLog`
