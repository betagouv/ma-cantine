# Onboarding tech

## Cloner le dépôt

### OSX

Si `git` dit que vous avez des nouveaux fichiers juste après cloner le dépôt, vérifier vos paramètres de `git`. Sur mon ordinateur, j'ai du faire :

- `git config core.precomposeunicode false`
- `git reset --hard origin/staging` (attention, vos changements en locale seront perdus)
- `git pull`

D'autres conseils que j'ai lu c'est de faire `git config core.precomposeunicode true` et/ou `git config core.quotepath false`. Vous pourriez vérifier vos config avec `git config -l`. Si ça ne marche pas, essayer de tirer des cartes de tarot ou faire une offrande à la lune (ou bien soumettre un issu). Bon courage.

## Mise en place de l'environnement dev

Please note that the `staging` and `main` branches are protected and all commits must come through a pull request.

### À installer localement

- [Python3](https://www.python.org/downloads/) (de préference 3.11)
- [pip](https://pip.pypa.io/en/stable/installing/) (souvent installé avec Python)
- [vitrualenv](https://virtualenv.pypa.io/en/stable/installation.html)
- [Node et npm](https://nodejs.org/en/download/)
- [Postgres](https://www.postgresql.org/download/)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)
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

On utilise les dernires versions LTS de `node` et `npm`.

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
DEBUG_FRONT= `True` pour le développement local du 2024-front ou `False` autrement
DB_USER= L'utilisateur de la base de données. Doit avoir les droits de creation de db pour les tests.
DB_PASSWORD= Le mot de passe pour accéder à la base de données
DB_HOST= Le host de la base de données (par ex. '127.0.0.1')
DB_PORT= Le port de la base de données (par ex. '3306')
DB_NAME= Le nom de la base de données (par ex. 'macantine-egalim'
HOSTNAME= Le hostname dans lequel l'application se trouve (par ex. 127.0.0.1:8000)
ALLOWED_HOSTS= Des noms de domaine/d’hôte que ce site peut servir (par ex. 'localhost, \*')
ENFORCE_HOST= Optionnel - Si présent, les requêtes seront redirigées à ce host
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
DATA_WARE_HOUSE_USER= Optionnel - l'utilisateur de la base postgres utilisée pour les analsyes stats
DATA_WARE_HOUSE_PASSWORD= Optionnel - le mot de passe de la base de postgres utilisée pour les analsyes stats
DATA_WARE_HOUSE_HOST=Optionnel - le host de la base postgres utilisée pour les analsyes stats
DATA_WARE_HOUSE_PORT= Optionnel - le port de la base postgres utilisée pour les analsyes stats
DATA_WARE_HOUSE_DB= Optionnel - le nom de la db de la base postgres utilisée pour les analsyes stats
DEBUG_PERFORMANCE= Optionnel - à utiliser avec "DEBUG" pour montrer la [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
ENVIRONMENT= Optionnel - si cette variable est remplie un badge sera visible dans l'application et l'admin changera. Les options sont : `dev` | `staging` | `demo` | `prod`
REDIS_URL= L'instance redis à utiliser pour les tâches asynchrones et le cache des clés API. Par exemple : 'redis://localhost:6379/0'
REDIS_PREPEND_KEY= Optionnel - Ajout ce string au début de chaque clé Redis. Utile pour partager la même DB Redis sur plusieurs environnements
OVERRIDE_TEST_SEED= Optionnel - `seed` utilisé par les tests pour les éléments aléatoires. Utile lors qu'un test échoue et qu'on veut reproduire exactement ce qu'il s'est passé.
SIRET_API_KEY= Optionnel - pour utiliser l'API INSEE Sirene. Pour générer : accèder votre compte https://api.insee.fr/catalogue/ > My applications > Add application
SIRET_API_SECRET= Optionnel - pour utiliser l'API INSEE Sirene
MONCOMPTEPRO_CLIENT_ID= Optionnel - Client ID utilisé pour l'authentification via [MonComptePro](https://github.com/betagouv/moncomptepro).
MONCOMPTEPRO_SECRET= Optionnel - Secret utilisé pour l'authentification via [MonComptePro](https://github.com/betagouv/moncomptepro).
MONCOMPTEPRO_CONFIG= Optionnel - Url de configuration utilisé pour l'authentification via [MonComptePro](https://github.com/betagouv/moncomptepro). Par exemple : `https://app-test.moncomptepro.beta.gouv.fr/.well-known/openid-configuration`
MAX_DAYS_HISTORICAL_RECORDS= Optionnel - Flag pour indiquer le nombre de jours pendant lequels on garde l'historique des modèles. Utilisé lors d'une tâche Celery.
CSV_PURCHASE_CHUNK_LINES= Optionnel - Définit le nombre de lignes dans chaque chunk pour l'import des achats. Le choix par défaut est de 81920 ce qui représente en moyenne des chunks de 3Mb.
```

### Activer les feature flags

```
ENABLE_XP_RESERVATION= Optionnel - `True` pour activer la feature de l'expérimentation des systèmes de réservation.
ENABLE_XP_VEGE= Optionnel - `True` pour activer la feature de l'expérimentation de l'offre quotidien de repas végétariens.
ENABLE_TELEDECLARATION= Optionnel - `True` pour permettre les utilisateurs de télédéclarer leur diagnostic.
TELEDECLARATION_CORRECTION_CAMPAIGN= Optionnel - `True` pour pour distinguer la campagne de TD de la campagne de corrections. Ça fait pas grande chose sans ENABLE_TELEDECLARATION.
TELEDECLARATION_END_DATE= Optionnel - Celle-ci n'est pas exactement une feature flag mais fonctionne avec le flag précedent. Il faut indiquer une date pour la fin de la campagne de la télédéclaration (par exemple, `2024-03-15`)
ENABLE_DASHBOARD= Optionnel - `True` pour montrer la nouvelle page d'accueil des gestionnaires.
PUBLISH_BY_DEFAULT= Optionnel - `True` pour publier les cantines sauf celles qui sont identifiées autrement.
ENABLE_VUE3= Optionnel - `True` pour rendre les nouvelles vues disponibles.
ENABLE_WASTE_MEASUREMENTS= Optionnel - `True` pour rendre l'outil évaluation gaspillage alimentaire disponible
```

### Relances automatiques par email

```
TEMPLATE_ID_NO_CANTEEN_FIRST= Optionnel - ID du template SendInBlue pour le premier email envoyé aux utilisateurs n'ayant pas encore créé une cantine. En cas d'absence la relance n'aura pas lieu.
TEMPLATE_ID_NO_CANTEEN_SECOND= Optionnel - ID du template SendInBlue pour le deuzième email envoyé aux utilisateurs n'ayant pas encore créé une cantine. En cas d'absence la relance n'aura pas lieu.
TEMPLATE_ID_NO_DIAGNOSTIC_FIRST= Optionnel - ID du template SendInBlue pour le premier email envoyé aux utilisateurs ayant une cantine mais pas un diagnostic. En cas d'absence la relance n'aura pas lieu.
```

### Création des tables / Migration de la base de données

Pour créer les tables nécessaires :

```
python manage.py migrate
```

Notez que cette commande est à effectuer à chaque changement de schema de la base de données.

### Génération des fichiers de i18n

Pour créer les fichiers compilés de traduction :

```
python manage.py compilemessages
```

Notez que cette commande est à effectuer à chaque changement de fichier de traduction \*po.

## Lancer l'application en mode développement

Certaines fonctionnalités ont besoin de fichiers statics. La première fois que vous lancez le projet, d'abord lancez `python manage.py collectstatic`.

Deux options :

1. Le script `./local-build.sh` lance les trois commandes en parallel (Django, Vue2, Vue3). Faut pas avoir besoin de faire des migrations pour utiliser ça.

2. Ouvrir trois terminales : une pour l'application Django, une pour l'application Vue2, et une pour l'application Vue3.

### Terminal Django

Il suffit de lancer la commande Django "runserver" à la racine du projet pour avoir le serveur de développement (avec hot-reload) :

```
python manage.py runserver
```

### Terminal Vue2

Pour faire l'équivalent côté frontend, allez sur `./frontend` et lancez le serveur npm :

```
cd frontend
npm run serve
```

### Terminal Vue3

```
cd 2024-frontend
npm run dev
```

Une fois la compilation finie des trois côtés, l'application se trouvera sous [127.0.0.1:8000](127.0.0.1:8000) (le port Django, non pas celui de npm).

## Pre-commit

On utilise l'outil [`pre-commit`](https://pre-commit.com/) pour effectuer des vérifications automatiques
avant chaque commit. Cela permet par exemple de linter les code Python, Javascript et HTML.

Pour pouvoir l'utiliser, il faut installer `pre-commit` (en général plutôt de manière globable que dans
l'environnement virtuel) : `pip install pre-commit`.

Puis l'activer : `pre-commit install`.

Note : commande pour lancer les règles du pre-commit sur tous les fichiers : `pre-commit run --all-files`

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

## Lancer les tests pour l'application Vue2

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

## Celery

Celery est un gestionnaire de tâches asynchrone utilisé par exemple pour l'envoi périodique de courriels de rappel et pour le remplissage des donn

Pour staging/demo/prod, le chemin du fichier d'instantiation de Celery doit être spéficié dans la console CleverCloud sous la variable `CC_PYTHON_CELERY_MODULE=macantine.celery`. La fonctionnalité Celery Beat doit aussi être activée : `CC_PYTHON_CELERY_USE_BEAT=true`, ainsi que le timezone souhaité : `CELERY_TIMEZONE:'Europe/Paris'`

## Visual Studio Code

Des extensions qu'on trouve utile :

- Django
- EJS Beautify
- EJS langauge support
- ESLint
- Prettier - Code formatter
- Vue Language Features
- Vetur
- vuetify-vscode
- Spell Right

## Test déploiement en locale

Les commandes lancées sur CleverCloud sont listées dans `clevercloud/python.json`.

.env :

```
DEBUG=False
DEBUG_FRONT=False
```

Dans le dossier principal, lancez :
`bash ./clevercloud/test-build-with-vue3.sh`
`python manage.py runserver --insecure`

En prod, faut ajouter `CC_PRE_BUILD_HOOK=./clevercloud/pre-build-hook.sh`

## Déploiement

Vérification pre-déploiment

- est-ce que les tests passent sur staging ?
- est-ce que tout va bien côté Clever Cloud ?
- est-ce qu'il y a des cherry-picks sur main qui n'existent pas sur staging ?

Étapes :

- https://github.com/betagouv/ma-cantine/releases > "Draft a new release"
- "Choose a tag" > taper la date d'aujourd'hui en format YYYY-MM-DD > "Create a new tag on publish"
- "Generate release notes"
- Modifier les notes générés (indications ci-dessous)
- "Publish release"
- Si il y a des variables d'environnement à ajouter, ajoutez-les sur prod et demo côté Clever Cloud
- avec staging : `git pull`
- preparer la branche main en locale : `git checkout main` `git rebase staging`
- `git push` (peut-être `git push -f`)
- Le déploiement va commencer automatiquement. Ça prend un moment pour déployer côté Clever Cloud, suivez la progression là-bas.
- Une fois que le déploiement est fait, envoyer un message sur mattermost canal produit pour tenir l'équipe au courant.

### Release notes

Vous pourrez modifier les notes dans un éditeur pour être plus rapide.

- supprimer toutes les lignes dependabot et les remplacer avec une ligne "MAJ dépendances"
- supprimer la partie "by @username in https://..."
- faire n'importe quel autre changement pour rendre la liste facilement comprensible par tout le monde

### Debugging

Si jamais vous doutez/si il y a un problème, parlez avec un.e autre dév.
