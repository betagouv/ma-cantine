# Restaurer un backup de données

Clever cloud -> bdd add-on -> backups -> télécharger le backup (c'est format \*.dump)

Pour ne pas impacter mon setup local, je crée un nouveau DB, service, port. Faut MAJ les variables correspondants dans compose.yaml et .env.Docker (ou .env)

`docker compose up server`

Je choisit de travailler avec que `server` pour éviter le temps du build de front.

(optionnel) si t'as l'erreur que la BDD n'est pas créé, fait `docker compose down --volumes` et reessayer `up`

`docker compose run --user root --rm server bash`

si c'est une nouvelle BDD, faire les migrations python `python manage.py migrate`

```
apt-get install -y postgresql-client
pg_restore -v -x -d postgresql://<db user>:<db password>@<nom du db service dans compose>:<db port>/<db name> <path to .dump file>
```

(-v pour verbose; -x pour ignorer les droits; -d pour specifier la BDD)

pour voir les données dans l'admin, faut créer le superuser `python manage.py createsuperuser`

## Comment recuperer les identifiants des objets supprimés ?

On peut utiliser le modèle `LogEntry` : https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#logentry-objects

Hacky solution : connecte à l'application (grâce à [CleverCloud CLI](https://developers.clever-cloud.com/doc/cli/ssh-access/)) et avec django shell fait les queries sur LogEntry.

Tip : test en local et après en staging avant prod !

```
clever ssh --app <id de l'app>
cd app_<id, utiliser autocompletion>
python manage.py shell
```

maintenant si tu voulais trouver les objets supprimés par un utilisateur dans la dernière heure tu pourrais faire qqch comme :

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

les autres `action_flag`s et champs sont decrit dans la documentation django.

tu pourrais utiliser `content_type` pour trouver que les suppressions d'achats (par exemple):

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
