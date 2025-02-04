# Celery

Celery est un gestionnaire de tâches asynchrone utilisé par exemple pour l'envoi périodique de courriels de rappel et pour le remplissage des données.

Pour staging/demo/prod, le chemin du fichier d'instantiation de Celery doit être spéficié dans la console CleverCloud. La fonctionnalité Celery Beat, qui gère le cron, doit aussi être activée, ainsi que le timezone souhaité.

## En local

1. Démarrer le beat (gère les tâches régulières) celery `celery -A macantine beat --loglevel=INFO`
1. Démarrer le worker celery `celery -A macantine worker --loglevel=INFO`.

## En production

Le scheduler et les workers Celery sont déployés sur un autre serveur que l'application web pour des questions de robustesse.
Sur le serveur dit "celery", renseigner les mêmes variables d'environnement que le serveur web, plus :

### Variables d'environnement

1. Fonctionnement de celery :
    1. `CC_PYTHON_CELERY_USE_BEAT=true`
    1. `CC_PYTHON_CELERY_MODULE=macantine.celery`
    1. `CELERY_TIMEZONE='Europe/Paris'`
1. Export des données via la task `export_datasets()`:
    1. `DATA_WARE_HOUSE_USER= Optionnel - l'utilisateur de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_PASSWORD= Optionnel - le mot de passe de la base de postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_HOST=Optionnel - le host de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_PORT= Optionnel - le port de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_DB= Optionnel - le nom de la db de la base postgres utilisée pour les analsyes stats`
1. Relances automatiques par email
    1. `TEMPLATE_ID_NO_CANTEEN_FIRST= Optionnel - ID du template SendInBlue pour le premier email envoyé aux utilisateurs n'ayant pas encore créé une cantine. En cas d'absence la relance n'aura pas lieu.`
    1. `TEMPLATE_ID_NO_CANTEEN_SECOND= Optionnel - ID du template SendInBlue pour le deuzième email envoyé aux utilisateurs n'ayant pas encore créé une cantine. En cas d'absence la relance n'aura pas lieu.`
    1. `TEMPLATE_ID_NO_DIAGNOSTIC_FIRST= Optionnel - ID du template SendInBlue pour le premier email envoyé aux utilisateurs ayant une cantine mais pas un diagnostic. En cas d'absence la relance n'aura pas lieu.`
1. Mise à jour des contacts Brevo
    1. `SENDINBLUE_API_KEY= La clé API de SendInBlue`

### Dépendances

L'application Celery (Worker & Orchestrateur) doit être lié à un message broker. Dans notre cas, c'est redis
