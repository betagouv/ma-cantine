# Application `imports`

## Objectif

Cette application regroupe la logique des imports en masse de fichiers CSV/TSV exposés par l'API
(création/modification de cantines, gestionnaires, bilans diagnostics, achats).

## URLs publiques

Endpoints publics :

- `/api/v1/importCanteens/create/`
- `/api/v1/importCanteens/update/`
- `/api/v1/importCanteensManagers/`
- `/api/v1/importDiagnostics/simple/`
- `/api/v1/importDiagnostics/complete/`
- `/api/v1/importPurchases/`

Le routage est délégué par `api/urls.py` vers `backend/imports/urls.py`.

## Structure

- `base.py` : classe abstraite `BaseImportView` qui factorise la lecture/validation des fichiers
- `canteen_create.py`, `canteen_update.py`, `canteen_managers.py` : imports liés aux cantines
- `diagnostic.py` : imports des bilans diagnostics (simple et détaillé)
- `purchase.py` : import des achats
- `urls.py` : routage des endpoints d'import
- `schemas/` : schémas Frictionless (JSON) utilisés par Validata pour valider les fichiers importés
- `tests/` : tests automatisés
