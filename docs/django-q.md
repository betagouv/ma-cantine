# Tâches asynchrones (django-q2)

[django-q2](https://django-q2.readthedocs.io/) est le gestionnaire de tâches asynchrones utilisé pour les tâches régulières (export des données, mise à jour des contacts Brevo, dbt...).

Il utilise la base de données Django (Postgres) à la fois comme file d'attente (broker), pour stocker les tâches planifiées et pour stocker les résultats. Pas besoin de Redis.

- la configuration est dans `Q_CLUSTER` dans [macantine/settings.py](../macantine/settings.py)
- les tâches sont des fonctions dans [macantine/tasks.py](../macantine/tasks.py)
- les tâches régulières (et leur fréquence) sont définies dans [macantine/schedules.py](../macantine/schedules.py)
  - elles sont synchronisées en base (modèle `Schedule`) après chaque `migrate`, donc à chaque déploiement
  - certaines tâches ne tournent qu'en prod (`"prod_only": True`)
- les tâches planifiées, réussies, échouées et en attente sont visibles dans l'admin Django (section "Django Q")

## En local

1. Lancer `python manage.py migrate` (crée les tables de django-q2 et les tâches planifiées)
1. Démarrer le cluster (workers + scheduler) : `python manage.py qcluster`
1. Voir l'état du cluster : `python manage.py qinfo` (ou `python manage.py qmonitor`)

## En production

Le cluster est déployé sur un autre serveur que l'application web pour des questions de robustesse (les exports consomment beaucoup de mémoire).
Sur ce serveur (historiquement appelé "celery" sur Clever Cloud), renseigner les mêmes variables d'environnement que le serveur web, plus :

### Variables d'environnement

1. Fonctionnement de django-q2 :
    1. `CC_WORKER_COMMAND=python manage.py qcluster` (Clever Cloud lance et supervise cette commande à côté de l'application)
    1. `Q_CLUSTER_WORKERS=` Optionnel - nombre de workers (par défaut : 2)
    1. `CONN_MAX_AGE=0`
1. Export des données via la task `export_datasets()`:
    1. `DATA_WARE_HOUSE_USER= Optionnel - l'utilisateur de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_PASSWORD= Optionnel - le mot de passe de la base de postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_HOST=Optionnel - le host de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_PORT= Optionnel - le port de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_DB= Optionnel - le nom de la db de la base postgres utilisée pour les analsyes stats`
1. Mise à jour des contacts Brevo
    1. `SENDINBLUE_API_KEY= La clé API de SendInBlue`

Ne garder qu'une seule instance de ce serveur : chaque instance lance son propre cluster.

### Points d'attention

- une tâche qui dépasse `timeout` (4h) est arrêtée et notée en échec
- une tâche en échec ou interrompue (worker tué, redéploiement) n'est pas relancée automatiquement (`max_attempts: 1`) : il faut la relancer à la main
- après une interruption du cluster, les occurrences manquées ne sont pas rattrapées (`catch_up: False`)

## Lancer une tâche manuellement

1. Se connecter au serveur via ssh `ssh ssh@sshgateway-clevercloud-customers.services.clever-cloud.com`
2. Se déplacer dans le dossier de l'app `cd app_XXXX`
3. Lancer la commande souhaitée `python manage.py <MANAGEMENT_COMMANDE>`

ou, si la tâche n'est pas implémentée dans une commande de management :

- l'envoyer au cluster (le résultat sera visible dans l'admin) :
    ```
    python manage.py shell -c "from django_q.tasks import async_task; async_task('macantine.tasks.<MA_TACHE>')"
    ```
- ou l'exécuter directement dans le terminal :
    ```
    python manage.py shell -c "from macantine.tasks import <MA_TACHE>; <MA_TACHE>()"
    ```

Depuis l'admin, une tâche en échec peut être relancée avec l'action "Resubmit selected tasks to queue" (section "Django Q" > "Failed tasks").
