# Redis

Redis est utilisé comme broker de messages pour [Celery](celery.md) et comme stockage clé/valeur rapide pour certains usages applicatifs.

## En local

à compléter ?

## En production

L'application web et Celery doivent pointer vers la même instance Redis via `REDIS_URL`.

### Variables d'environnement

1. `REDIS_URL=...` URL de connexion Redis
1. `REDIS_PREPEND_KEY=...` préfixe optionnel pour isoler les clés par environnement

## Commandes utiles

1. Lister les clés (debug) : `redis-cli --scan`
1. Lire une clé : `redis-cli GET <cle>`
1. Supprimer une clé : `redis-cli DEL <cle>`

## Notes

1. Redis est une dépendance de Celery : si Redis est indisponible, les tâches asynchrones ne seront plus consommées.
1. Éviter les commandes destructives globales en production (`FLUSHALL`, `FLUSHDB`).
