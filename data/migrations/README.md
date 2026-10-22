# Migrations `data`

## Historique des squash

| Date du squash | Fichier(s) squashé(s) | Migrations remplacées |
|---|---|---|
| 2021-05-28 | `0001_squashed_0006_blogpost_tagline.py` | `0001_initial` → `0006_blogpost_tagline` (migrations du 1er jour, jamais commitées sauf `0001_initial`) |
| 2026-10-21 | `0001_squashed_0151_merge_20240906_1852.py` | `0001_squashed_0006_blogpost_tagline` → `0151_merge_20240906_1852` (2021-05-28 → 2024-09-06) |
| 2026-10-21 | `0152_wasteaction_squashed_0250_alter_diagnostic_status_and_more.py` | `0152_wasteaction` → `0250_alter_diagnostic_status_and_more` (2024-09-09 → 2026-04-02) |

Notes sur le squash de 2026-10-21 :

- coupé en 2 pour éviter une dépendance circulaire avec Wagtail : `wagtailcore` dépend de notre modèle `User` (`AUTH_USER_MODEL`), et nos migrations dépendent de `wagtailcore` / `wagtailimages` à partir de `0152_wasteaction`
- les `RunPython` / `RunSQL` (migrations de données uniquement) ont été retirés des squash : sans effet sur une base vide, et déjà appliqués sur les bases existantes
- les migrations suivantes (`0251_…`, 2026-05-04 →) restent des migrations normales

## Dossier `archive/`

Migrations d'origine remplacées par les squash (contenu identique à avant le squash), gardées pour référence uniquement : historique du schéma, migrations de données retirées des squash.

⚠️ Ces fichiers ne sont **pas** chargés par Django : `archive/` n'a volontairement pas de `__init__.py`, et Django ignore les sous-dossiers de `data/migrations/`. Ne pas y ajouter de nouvelles migrations, et ne pas les importer depuis le code.
