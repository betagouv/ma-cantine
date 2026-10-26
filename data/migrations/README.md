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
- 2026-10-26 : contenu des 2 fichiers **régénéré** depuis l'état final à `0250` (voir « Régénérer un squash » ci-dessous). Le `squashmigrations` initial laissait ~960 opérations (`AlterField`, `AddField`, `RenameField`… surtout sur `Diagnostic`), car l'optimiseur de Django ne fusionne qu'à l'intérieur d'une même migration : avec la coupure à `0151`, tout ce qui modifiait `Diagnostic` après sa création restait rejoué. Après régénération : 1 `CreateModel` par modèle avec ses champs finaux (~40 opérations). Noms, dépendances et `replaces` inchangés : rien à rejouer sur les bases existantes

## Comment squasher

Django fournit la commande `squashmigrations` :

```bash
uv run python manage.py squashmigrations <app> [<début>] <fin>
```

- sans `<début>`, part de la 1ère migration de l'app. Les préfixes (`0151`) suffisent s'ils sont uniques
- concatène les opérations des migrations, puis les optimise (fusion des `CreateModel` / `AddField` / `AlterField`… successifs), et écrit un nouveau fichier `<début>_squashed_<fin>.py` avec un attribut `replaces`
- options utiles : `--noinput` (pas de confirmation), `--squashed-name <nom>` (nom du fichier), `--no-optimize` (concaténer sans optimiser)

Commandes utilisées pour le squash de 2026-10-21 :

```bash
uv run python manage.py squashmigrations data 0151 --noinput
uv run python manage.py squashmigrations data 0152 0250 --noinput
```

Étapes autour de la commande :

1. **Avant**
   - `uv run python manage.py makemigrations --check --dry-run` : aucun changement de modèle en attente
   - aucune migration de la plage ne doit avoir de `replaces` (Django refuse de squasher un squash) : finaliser d'abord les squash précédents
   - marquer les `RunPython` / `RunSQL` de la plage avec `elidable=True`, pour qu'ils soient retirés du squash (sinon il faut recopier leurs fonctions à la main dans le fichier squashé)
2. **Après**
   - en cas de `CircularDependencyError` (ex. avec Wagtail) : couper en plusieurs squash, juste avant la 1ère migration qui dépend de l'autre app
   - vérifier sur une base vide (`migrate`) et sur une base existante (`migrate --plan` → rien à appliquer)
   - déplacer les migrations remplacées dans `archive/`, et faire pointer les migrations qui en dépendaient vers le squash
   - garder `replaces` tant que toutes les bases (staging, prod) n'ont pas été migrées avec le squash, puis le retirer dans une PR ultérieure

Pour ré-optimiser une seule migration existante : `uv run python manage.py optimizemigration <app> <migration>`.

⚠️ Vérifier le résultat : compter les opérations du fichier généré (`grep -c "migrations\.AlterField\|migrations\.RenameField" <fichier>`). S'il en reste beaucoup (surtout en cas de squash coupé en plusieurs fichiers), régénérer le squash (voir ci-dessous).

## Régénérer un squash (que des `CreateModel`)

Plutôt que de dépendre de l'optimiseur, on peut réécrire le contenu des squash depuis l'état final de la plage, comme le ferait `makemigrations` sur un projet neuf : l'autodetector de Django compare un état vide à l'état à la fin de la plage, et produit les `CreateModel` (+ quelques `AddField` / `AddIndex` / `AddConstraint` pour les FK circulaires entre nos modèles).

On garde les noms de fichiers, les `dependencies` et les `replaces` : les bases existantes ont déjà ces migrations d'enregistrées, et ne rejouent donc rien. Seules les bases neuves (CI, nouvel environnement) utilisent le nouveau contenu.

Script utilisé le 2026-10-26 (à lancer avec `uv run python manage.py shell < regen_squash.py`, en dehors de `data/migrations/` : tout fichier `.py` de ce dossier serait chargé comme une migration) :

<details>
<summary><code>regen_squash.py</code></summary>

```python
from pathlib import Path

import django.contrib.postgres.operations
from django.db import migrations
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.questioner import NonInteractiveMigrationQuestioner
from django.db.migrations.state import ProjectState
from django.db.migrations.writer import MigrationWriter

SQUASH_1 = "0001_squashed_0151_merge_20240906_1852"
SQUASH_2 = "0152_wasteaction_squashed_0250_alter_diagnostic_status_and_more"

loader = MigrationLoader(None, ignore_no_migrations=True)
to_state = loader.project_state(("data", SQUASH_2))  # état à la fin de la plage
autodetector = MigrationAutodetector(ProjectState(), to_state, NonInteractiveMigrationQuestioner())
operations = [op for migration in autodetector._detect_changes()["data"] for op in migration.operations]


def is_wagtail_fk(field):
    remote = getattr(field, "remote_field", None)
    if remote is None:
        return False
    label = remote.model if isinstance(remote.model, str) else remote.model._meta.label
    return label.lower().startswith("wagtail")


# fichier 1 : extension Postgres + tous les modèles, sans les FK vers Wagtail
# fichier 2 : les FK vers Wagtail (pour garder la coupure qui évite la dépendance circulaire)
ops_1 = [django.contrib.postgres.operations.UnaccentExtension()]
ops_2 = []
for op in operations:
    if isinstance(op, migrations.CreateModel):
        kept = []
        for name, field in op.fields:
            if is_wagtail_fk(field):
                ops_2.append(migrations.AddField(model_name=op.name.lower(), name=name, field=field))
            else:
                kept.append((name, field))
        op.fields = kept
        ops_1.append(op)
    elif isinstance(op, (migrations.AddField, migrations.AlterField)) and is_wagtail_fk(op.field):
        ops_2.append(op)
    else:
        ops_1.append(op)

for name, ops in [(SQUASH_1, ops_1), (SQUASH_2, ops_2)]:
    disk = loader.disk_migrations[("data", name)]
    migration = migrations.Migration(name, "data")
    migration.replaces = disk.replaces
    migration.dependencies = disk.dependencies
    migration.initial = name == SQUASH_1
    migration.operations = ops
    writer = MigrationWriter(migration)
    Path(writer.path).write_text(writer.as_string())
```

</details>

Les opérations hors modèles (ici `UnaccentExtension`) ne sont pas produites par l'autodetector : les reprendre à la main depuis l'ancien fichier.

Vérifier ensuite que le schéma d'une base neuve est identique à celui obtenu avec l'ancien contenu (colonnes, types, contraintes, index, extensions), puis `makemigrations --check` et les tests.

Documentation Django : https://docs.djangoproject.com/fr/5.2/topics/migrations/#migration-squashing

## Dossier `archive/`

Migrations d'origine remplacées par les squash (contenu identique à avant le squash), gardées pour référence uniquement : historique du schéma, migrations de données retirées des squash.

⚠️ Ces fichiers ne sont **pas** chargés par Django : `archive/` n'a volontairement pas de `__init__.py`, et Django ignore les sous-dossiers de `data/migrations/`. Ne pas y ajouter de nouvelles migrations, et ne pas les importer depuis le code.
