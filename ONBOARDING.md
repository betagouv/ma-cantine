# Onboarding tech

## Mise en place de l'environnement dev

### À installer localement

- [Python3](https://www.python.org/downloads/) (de préference 3.8)
- [pip](https://pip.pypa.io/en/stable/installing/) (souvent installé avec Python)
- [vitrualenv](https://virtualenv.pypa.io/en/stable/installation.html)
- [Node et npm](https://nodejs.org/en/download/)
- [Postgres](https://www.postgresql.org/download/)
- [pre-commit](https://pypi.org/project/pre-commit/)

### Création d'un environnement Python3 virtualenv

Pour commencer, c'est recommandé de créer un environnement virtuel avec Python3.

```
virtualenv -p python3 venv
source ./venv/bin/activate
```

### Installer les dépendances du backend

Les dépendances du backend se trouvent dans `requirements.txt`. Pour les installer :

```
pip install -r requirements.txt
```

### Installer les dépendances du frontend

On utilise `node` version 14 et npm version 6.

L'application frontend se trouve sous `/frontend`. Pour installer les dépendances :

```
cd frontend
npm install
```

### Créer la base de données

Par exemple, pour utiliser une base de données nommée _macantine_egalim_ :

```
createdb macantine-egalim
```

### Compléter les variables d'environnement

L'application utilise [python-dotenv](https://pypi.org/project/python-dotenv/), vous pouvez donc créer un fichier `.env` à la racine du projet avec ces variables définies :

```
SECRET= Le secret pour Django (vous pouvez le [générer ici](https://djecrety.ir/))
DEBUG= `True` pour le développement local ou `False` autrement
DB_USER= L'utilisateur de la base de données
DB_PASSWORD= Le mot de passe pour accéder à la base de données
DB_HOST= Le host de la base de données (par ex. '127.0.0.1')
DB_PORT= Le port de la base de données (par ex. '3306')
DB_NAME= Le nom de la base de données (par ex. 'macantine-egalim'
HOSTNAME= Le hostname dans lequel l'application se trouve (par ex. 127.0.0.1:8000)
ALLOWED_HOSTS= Des noms de domaine/d’hôte que ce site peut servir (par ex. 'localhost, \*')
STATICFILES_STORAGE= Le système utilisé pour les fichiers statiques (par ex. 'django.contrib.staticfiles.storage.StaticFilesStorage')
DEFAULT_FILE_STORAGE= Le système de stockage de fichiers (par ex 'django.core.files.storage.FileSystemStorage')
FORCE_HTTPS= 'False' si on développe en local, 'True' autrement
SECURE= 'False' si on développe en local, 'True' autrement
EMAIL_BACKEND= par ex. 'django.core.mail.backends.console.EmailBackend'. Pour utiliser SendInBlue : 'anymail.backends.sendinblue.EmailBackend'
DEFAULT_FROM_EMAIL= par ex. 'ma-cantine@example.com'
CONTACT_EMAIL= par ex. 'contact@example.com'
SENDINBLUE_API_KEY= La clé API de SendInBlue
NEWSLETTER_SENDINBLUE_LIST_ID= L'ID de la newsletter de SendInBlue
MATOMO_ID= 162 pour la prod (peut-être laissé vide)
CELLAR_HOST= Optionnel - le host du service S3
CELLAR_KEY= Optionnel - la clé du service S3
CELLAR_SECRET= Optionnel - le secret du service S3
CELLAR_BUCKET_NAME= Optionnel - le nom du bucket S3 à utiliser
DEBUG_PERFORMANCE= Optionnel - à utiliser avec "DEBUG" pour montrer la [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
ENVIRONMENT= Optionnel - si cette variable est remplie un badge sera visible dans l'application et l'admin changera. Les options sont : `dev` | `staging` | `demo` | `prod`
TRELLO_API_KEY= Optionnel - Permet la création de cartes Trello suite à une demande de contact de la part de l'utilisateur. Conseils en-dessous pour l'obtenir.
TRELLO_API_TOKEN= Optionnel - Permet la création de cartes Trello suite à une demande de contact de la part de l'utilisateur. Conseils en-dessous pour l'obtenir.
TRELLO_LIST_ID_CONTACT= Optionnel - ID de la liste où l'application mettra des cartes suite à une demande de contact de la part de l'utilistauer. Conseils en-dessous pour l'obtenir.
TRELLO_LIST_ID_PUBLICATION= Optionnel - ID de la liste où l'application mettra des cartes suite à une demande de publication de la part de l'utilistauer. Conseils en-dessous pour l'obtenir.
REDIS_URL= Optionnel - L'instance redis à utiliser pour les tâches asynchrones. Cette fonctionnalité n'est pas encore utilisée. Par exemple : 'redis://localhost:6379/0'
OVERRIDE_TEST_SEED= Optionnel - `seed` utilisé par les tests pour les éléments aléatoires. Utile lors qu'un test échoue et qu'on veut reproduire exactement ce qu'il s'est passé.
```

### Activer les feature flags

```
ENABLE_XP_RESERVATION= Optionnel - `True` pour activer la feature de l'expérimentation des systèmes de réservation.
ENABLE_XP_VEGE= Optionnel - `True` pour activer la feature de l'expérimentation de l'offre quotidien de repas végétariens.
ENABLE_PARTNERS= Optionnel - `True` pour afficher nos partenaires sur la page d'accueil.
```

### Relances automatiques par email

```
TEMPLATE_ID_NO_CANTEEN_FIRST= Optionnel - ID du template SendInBlue pour le premier email envoyé aux utilisateurs n'ayant pas encore créé une cantine. En cas d'absence la relance n'aura pas lieu.
TEMPLATE_ID_NO_CANTEEN_SECOND= Optionnel - ID du template SendInBlue pour le deuzième email envoyé aux utilisateurs n'ayant pas encore créé une cantine. En cas d'absence la relance n'aura pas lieu.
TEMPLATE_ID_NO_DIAGNOSTIC_FIRST= Optionnel - ID du template SendInBlue pour le premier email envoyé aux utilisateurs ayant une cantine mais pas un diagnostic. En cas d'absence la relance n'aura pas lieu.
```


#### Trello

Si vous ne connaissez pas les variables trello, suivez [ce guide](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/) pour identifier votre clé et token.

Après, pour trouver l'ID de la liste pour laquelle vous voulez ajouter des cartes :

`curl 'https://api.trello.com/1/boards/{idBoard}/lists?key={yourKey}&token={yourToken}'`

### Création des tables / Migration de la base de données

Pour créer les tables nécessaires :

```
python manage.py migrate
```

Notez que cette commande est à effectuer à chaque changement de schema de la base de données.

## Lancer l'application en mode développement

Pour le développement il faudra avoir deux terminales ouvertes : une pour l'application Django, et une autre pour l'application VueJS.

### Terminal Django

Il suffit de lancer la commande Django "runserver" à la racine du projet pour avoir le serveur de développement (avec hot-reload) :

```
python manage.py runserver
```

### Terminal VueJS

Pour faire l'équivalent côté frontend, allez sur `./frontend` et lancez le serveur npm :

```
cd frontend
npm run serve
```

Une fois la compilation finie des deux côtés, l'application se trouvera sous [127.0.0.1:8000](127.0.0.1:8000) (le port Django, non pas celui de npm).

### Pre-commit

On utilise l'outil [`pre-commit`](https://pre-commit.com/) pour effectuer des vérifications automatiques
avant chaque commit. Cela permet par exemple de linter les code Python, Javascript et HTML.

Pour pouvoir l'utiliser, il faut installer `pre-commit` (en général plutôt de manière globable que dans
l'environnement virtuel) : `pip install pre-commit`.

Puis l'activer : `pre-commit install`.

Les vérifications seront ensuite effectuées avant chaque commit. Attention, lorsqu'une vérification `fail`,
le commit est annulé. Il faut donc que toutes les vérifications passent pour que le commit soit pris en
compte. Si exceptionnellement vous voulez commiter malgré qu'une vérification ne passe pas, c'est possible
avec `git commit -m 'my message' --no-verify`.

## Lancer les tests pour l'application Django

La commande pour lancer les tests Django est :

```
python manage.py test
```

Sur VSCode, ces tests peuvent être debuggés avec la configuration "Python: Tests", présente sur le menu "Run".

## Lancer les tests pour l'application VueJS

Il faut d'abord se placer sur "/frontend", ensuite la commande pour lancer les tests VueJS est :

```
cd frontend
npm run test
```

## Creation d'un superuser

Afin de pouvoir s'identifier dans le backoffice (sous /admin), il est nécessaire de créer un utilisateur admin avec tous les droits. Pour ce faire, vous pouvez en console lancer :

```
python manage.py createsuperuser
```

## Reception d'emails en local

Il y a deux options pour recevoir les emails envoyés depuis l'application en local:

### 1- Les imprimer dans la console

Django permet d'imprimer en console les emails envoyés avec le 'django.core.mail.backends.console.EmailBackend'. Pour l'utiliser il suffit de mettre la variable d'environnement `EMAIL_BACKEND` à cette valeur. Cette option est rapide à mettre en place et ne nécessite pas d'autres outils.

Il faut néanmoins tenir en compte que la mise en page ne sera pas visible et que certaines configurations qui marchent avec la console ne marchent pas avec d'autres services email. Nous conseillons plutôt d'utiliser la solution suivante :

### 2- Utiliser Maildev

[Maildev](https://maildev.github.io/maildev/) est un outil ouvert qui exécute un serveur SMTP en local et qui permet de visualiser tous les emails traités. En l'installant de façon globale on peut mettre 'django.core.mail.backends.smtp.EmailBackend' comme variable d'environnement `EMAIL_BACKEND` pour l'utiliser.

### Celery

Celery est un gestionnaire de tâches asynchrone. À l'heure actuelle il n'est pas utilisé, mais le roadmap prévoit la mise en place de tâches récurrentes. Pour l'utiliser, un serveur redis est nécessaire.

Pour staging/demo/prod, le chemin du fichier d'instantiation de Celery doit être spéficié dans la console CleverCloud sous la variable `CC_PYTHON_CELERY_MODULE=macantine.celery`. La fonctionnalité Celery Beat doit aussi être activée : `CC_PYTHON_CELERY_USE_BEAT=true`, ainsi que le timezone souhaité : `CELERY_TIMEZONE:'Europe/Paris'`
