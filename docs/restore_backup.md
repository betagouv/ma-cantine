# Restaurer un backup de données

**Attention : La restauration de la base de donnée va supprimer vos donénes actuelles**

1. Exporter un backup : Clever cloud -> bdd add-on -> backups -> télécharger le backup (au format `.dump`, extrait via une commande `pg_dump`)
2. Lancer la restauration :
```
pg_restore --verbose --clean --no-privileges -d postgresql://<db user>:<db password>@<nom du db service dans compose>:<db port>/<db name> <path to .dump file>
```

## Comment recuperer les identifiants des objets supprimés ?

Il est possible d'utiliser le modèle [LogEntry](https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#logentry-objects)

Hacky solution : Se connecter à l'application (grâce à [CleverCloud CLI](https://developers.clever-cloud.com/doc/cli/ssh-access/)) et avec django shell fait les queries sur LogEntry.

*Tip : test en local et après en staging avant prod !*

```
clever ssh --app <id de l'app>
cd app_<id, utiliser autocompletion>
python manage.py shell
```

Pour trouver les objets supprimés par un utilisateur dans la dernière heure il est possible de :

```
from data.models import User

user = User.objects.filter(email=<email de l'utilisateur>).first()
print(user) # check if right user

from django.contrib.admin.models import LogEntry, DELETION
from django.utils import timezone
from datetime import timedelta

threshold = timezone.now() - timedelta(hours=1)
recent_deletions = LogEntry.objects.filter(action_time__gte=threshold, user=user, action_flag=DELETION).order_by("-action_time")
print(recent_deletions.count())
```

Les autres `action_flags` et champs sont decrit dans la documentation django.

Il est possible d'utiliser `content_type` pour trouver que les suppressions d'achats (par exemple):

```
recent_deletions.first().content_type
recent_purchase_deletions = LogEntry.objects.filter(action_time__gte=threshold, user=user, action_flag=DELETION, content_type=purchase_type).order_by("-action_time")
print(recent_purchase_deletions.count())
```

et pour recuperer les ids:

```
ids = recent_purchase_deletions.values_list("object_id", flat=True)
print(list(ids))
```

Deconnecter du shell et après l'appli avec ctrl-D chaque fois.
