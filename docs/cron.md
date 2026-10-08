# Tâches régulières (crons)

Les tâches régulières (export des données, mise à jour des contacts Brevo, dbt...) sont lancées par les [crons de Clever Cloud](https://www.clever.cloud/developers/doc/develop/cron/).

- les tâches sont des fonctions dans [macantine/tasks.py](../macantine/tasks.py)
- leur fréquence est définie dans [clevercloud/cron.json](../clevercloud/cron.json)
- chaque cron appelle [clevercloud/cron.sh](../clevercloud/cron.sh), qui lance la commande `python manage.py run_task <nom_de_la_tache>`
  - chaque exécution est enregistrée dans les "Command logs" (visibles dans l'admin Django) : début, fin, logs, succès ou échec
  - en cas d'erreur, l'exception est envoyée à Sentry (avec le tag `task`)
  - les tâches avec l'option `--prod-only` ne font rien si `ENVIRONMENT` n'est pas `prod`

## Planning

⚠️ Les serveurs Clever Cloud sont en UTC : les horaires de `cron.json` sont en UTC. Ils ont été choisis pour correspondre à l'heure de Paris en été (UTC+2) : en hiver (UTC+1), les tâches tournent donc 1h plus tôt (l'ordre des tâches est conservé).

| Tâche | UTC (`cron.json`) | Paris (été) | Paris (hiver) | Prod uniquement | Remarque |
|---|---|---|---|---|---|
| `canteen_fill_declaration_donnees_year_field` | toutes les 6h à :10 (4h, 10h, 16h, 22h) | 0h10, 6h10, 12h10, 18h10 | 23h10, 5h10, 11h10, 17h10 | | Liée à la campagne. Nécessaire pour `update_user_data` |
| `update_user_data` | 22h20 | 0h20 | 23h20 | | Nécessaire pour `update_brevo_contacts` |
| `update_brevo_contacts` | 22h30 | 0h30 | 23h30 | ✅ | |
| `export_dataset_raw_analysis` | 23h00 | 1h00 | 0h00 | ✅ | Nécessaire pour `dbt_run` |
| `dbt_run` | 23h30 | 1h30 | 0h30 | ✅ | |
| `export_dataset_canteen_analysis` | 0h00 | 2h00 | 1h00 | ✅ | Toutes les 6h pendant la campagne |
| `export_dataset_canteen_opendata` | 0h00 | 2h00 | 1h00 | ✅ | Toutes les 6h pendant la campagne |
| `delete_old_historical_records` | 1h00 | 3h00 | 2h00 | | |

Pendant la campagne de télédéclaration, on peut aussi ajouter `export_dataset_td_analysis` (par exemple toutes les 6h : `"0 */6 * * * $ROOT/clevercloud/cron.sh export_dataset_td_analysis --prod-only"`).

## En local

Les crons ne tournent pas en local (ni dans Docker). Pour lancer une tâche : `python manage.py run_task <nom_de_la_tache>`

## En production

Le fichier `cron.json` est déployé sur toutes les applications Clever Cloud qui utilisent ce dépôt (web, staging, demo...). Les crons ne tournent que sur l'application où `CRON_ENABLED=true`.
On les fait tourner sur une application à part (historiquement appelée "celery"), pour que les tâches (qui consomment beaucoup de mémoire) ne ralentissent pas l'application web.

Sur cette application, renseigner les mêmes variables d'environnement que le serveur web, plus :

### Variables d'environnement

1. Fonctionnement des crons :
    1. `CRON_ENABLED=true`
1. Export des données via la task `export_datasets()`:
    1. `DATA_WARE_HOUSE_USER= Optionnel - l'utilisateur de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_PASSWORD= Optionnel - le mot de passe de la base de postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_HOST=Optionnel - le host de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_PORT= Optionnel - le port de la base postgres utilisée pour les analsyes stats`
    1. `DATA_WARE_HOUSE_DB= Optionnel - le nom de la db de la base postgres utilisée pour les analsyes stats`
1. Mise à jour des contacts Brevo
    1. `SENDINBLUE_API_KEY= La clé API de SendInBlue`

### Points d'attention

- les crons sont installés sur chaque instance de l'application : `cron.sh` ne les lance que sur la première (`INSTANCE_NUMBER=0`)
- si le "zero downtime deployment" est activé, les crons de l'ancienne et de la nouvelle instance peuvent se chevaucher pendant quelques minutes
- une tâche en cours lors d'un redéploiement est interrompue : elle n'est pas relancée (et n'apparaît pas dans les "Command logs"), il faut la relancer à la main
- rien n'empêche 2 exécutions de la même tâche de se chevaucher (si une tâche dure plus longtemps que l'intervalle entre 2 exécutions)
- les logs des crons sont visibles dans les logs de l'application Clever Cloud

## Lancer une tâche manuellement

1. Se connecter au serveur via ssh `ssh ssh@sshgateway-clevercloud-customers.services.clever-cloud.com`
2. Se déplacer dans le dossier de l'app `cd app_XXXX`
3. Lancer la tâche : `python manage.py run_task <nom_de_la_tache>` (ou une autre commande de management `python manage.py <MANAGEMENT_COMMANDE>`)
