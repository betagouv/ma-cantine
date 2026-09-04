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

## Frontend Vue 3 (Vite + django-vite)

Le service `2024-frontend` monte uniquement le dossier de l'app Vue 3.
Django charge les assets via [`django-vite`](https://github.com/MrBin99/django-vite) (`DJANGO_VITE` dans `settings.py`) :
en développement, les balises pointent vers le serveur Vite (`localhost:5173`) ;
en production, elles lisent `build/manifest.json`.
