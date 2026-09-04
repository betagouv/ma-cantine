# Avec Docker

## Installation

Un environnement Docker / Docker Compose est fourni.

```sh
docker compose build
docker compose up
```

Dans un nouveau terminal, accèder au container du back pour migrer la BDD et créer la première utilisatrice.

```sh
docker compose run server bash
python manage.py migrate
python manage.py createsuperuser
```

> À la première installation il est possible d'avoir l'erreur "image iconnue ma-cantine-server" : pour corriger cela il faudra juste construire l'image de notre server en premier

## Makefile

Pour faciliter l'utilisation quotidienne avec docker, un fichier makefile regroupe les raccourcis :

```sh
make docker-build
make docker-up
```

Voir le [Makefile](../Makefile) pour des commandes utiles.

## Frontends Vite + django-vite

Les deux apps frontend utilisent Vite et sont branchées sur Django via [`django-vite`](https://github.com/MrBin99/django-vite) (`DJANGO_VITE` dans `settings.py`) :

| App | Dossier | Port Vite | Clé django-vite |
|---|---|---|---|
| Vue 3 | `frontend-vue3` | 5173 | `default` |
| Vue 2 | `frontend-vue2` | 8080 | `vue2` |

En développement, les balises pointent vers le serveur Vite correspondant ;
en production, elles lisent le `manifest.json` de chaque build (`build/` et `frontend-vue2/dist/`).
