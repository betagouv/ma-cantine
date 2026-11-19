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
2. validation du fichier contre son schéma via l'API [Validata](https://validata.fr) (en-tête puis lignes)
3. traitement des lignes (permissions, création / mise à jour) dans une transaction
4. log du résultat (`ImportFailure` en cas d'échec)

## Schémas

Chaque import déclare le schéma contre lequel valider le fichier (`_get_schema()`, qui renvoie un `ImportSchema`, dans `imports/models/importschema.py`). Le fichier du schéma est dans `data/schemas/imports/`.

Les valeurs d'une ligne sont lues par nom de colonne (`_get_row_dict()`, avec les colonnes du schéma), et non par position.

Bilans : les imports ne sont possibles que pendant la campagne (télédéclaration ou correction), par exemple au début de 2027 pour les bilans 2026 : hors campagne, le fichier entier est refusé (`_process_file()`). Format 2026 : pas de colonne `année_bilan`, les bilans sont ceux de l'année de la campagne en cours (`get_current_campaign_year()`). Format 2025 : l'année de chaque ligne (`année_bilan`) est vérifiée par la validation du modèle (`CAMPAIGN_DATES`, avec les settings `TELEDECLARATION_*_OVERRIDE` pour tester dans les environnements non-prod).

Bilans : les erreurs de validation sur les champs absents du fichier sont ignorées (`_full_clean()`). Par exemple, le format 2025 n'a pas de colonne `nombre_repas_an`, obligatoire pour les bilans 2026 : il sera à compléter dans l'interface avant la télédéclaration.

Bilans : dans les messages d'erreur, le nom des champs est celui de `teledeclaration/<année>/champs.json` (année du format du fichier, `schema_version`), comme les titres des colonnes du schéma (`_get_verbose_field_name()`). Les champs hors `champs.json` (`year`, `canteen`…) gardent le `verbose_name` du modèle.

## Tests

Les tests des imports n'appellent pas l'API Validata : ils rejouent ses réponses, enregistrées dans `imports/tests/files/validata_responses/<schéma>/<fichier>.json` (`ValidataReplayMixin`, dans `imports/tests/validata_replay.py`). Chaque réponse garde le hash du schéma et du fichier : s'il change (ou si la réponse n'existe pas), le test échoue.

Pour enregistrer les réponses manquantes ou obsolètes (appelle l'API Validata) :

```bash
VALIDATA_RECORD=1 python manage.py test imports
```

Si un schéma change : Validata le lit depuis GitHub, il faut donc d'abord pousser la branche, puis enregistrer avec `GIT_BRANCH=<branche>` (l'enregistrement échoue si le schéma sur GitHub est différent du schéma local).

## Ce qui reste ailleurs

- schémas : `data/schemas/imports/` (Validata les lit depuis GitHub, sur la branche `GIT_BRANCH`)
- génération des schémas de bilans : `macantine/management/commands/generate_import_schema.py`
- `ImportFailure` : `data/models/importfailure.py` (`ImportType` est dans `imports/models/importtype.py`)
- utilitaires : `common/utils/file_import.py` & `common/api/validata.py` (aussi utilisés hors imports)

## À faire

- déplacer `ImportFailure` dans `imports/models/` (migration `SeparateDatabaseAndState` en gardant la table `data_importfailure`, renommer le content type, adapter le test de la migration 0287). À moins de supprimer `ImportFailure` au profit d'`EventLog`
