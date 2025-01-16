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
make build
make up
```

Voir le [Makefile](../Makefile) pour des commandes utiles.
