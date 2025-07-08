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

## .hotfile et DjangoVite

Dans notre `compose.yaml` pour le volume du service `2024-frontend`, c'est l'app entière qui doit être mappée `"./:/app"` et non juste `"./2024-frontend:/app/2024-frontend"`, notre frontend vue3 utilise le plugin "django-vite" qui demande la création d'un fichier '.hotfile' partagé entre notre front et notre serveur.

[Voir commit](https://github.com/betagouv/ma-cantine/pull/4774/commits/31f94517df989a8ad7e74ba9395d3e93bef4b188)

> Si nous décidons de ne plus utiliser ce plugin, nous pourrons simplifier la configuration
