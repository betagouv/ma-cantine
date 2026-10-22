# Archive des migrations `data`

Migrations d'origine `0001` → `0250`, remplacées par les 2 squash :

- `data/migrations/0001_squashed_0151_merge_20240906_1852.py`
- `data/migrations/0152_wasteaction_squashed_0250_alter_diagnostic_status_and_more.py`

Gardées pour référence uniquement (historique du schéma, migrations de données `RunPython` / `RunSQL` qui ont été retirées des squash).

⚠️ Ces fichiers ne sont **pas** chargés par Django : ce dossier n'a volontairement pas de `__init__.py`, et Django ignore les sous-dossiers de `data/migrations/`. Ne pas y ajouter de nouvelles migrations, et ne pas les importer depuis le code.
