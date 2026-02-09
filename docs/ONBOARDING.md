# Onboarding tech

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Cloner le dépôt](#cloner-le-d%C3%A9p%C3%B4t)
- [Mise en place de l'environnement dev](#mise-en-place-de-lenvironnement-dev)
- [Lancer l'application en mode développement](#lancer-lapplication-en-mode-d%C3%A9veloppement)
- [Pre-commit](#pre-commit)
- [Lancer les tests](#lancer-les-tests)
- [Creation d'un superuser](#creation-dun-superuser)
- [Utilisation des magic token](#utilisation-des-magic-token)
- [Reception d'emails en local](#reception-demails-en-local)
- [Visual Studio Code](#visual-studio-code)
- [Git & Github](#git--github)
- [Déploiement](#d%C3%A9ploiement)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Cloner le dépôt

```
git clone git@github.com:betagouv/ma-cantine.git
```

### OSX

Si `git` dit que vous avez des nouveaux fichiers juste après cloner le dépôt, vérifier vos paramètres de `git`. Sur mon ordinateur, j'ai du faire :

- `git config core.precomposeunicode false`
- `git reset --hard origin/staging` (attention, vos changements en locale seront perdus)
- `git pull`

D'autres conseils que j'ai lu c'est de faire `git config core.precomposeunicode true` et/ou `git config core.quotepath false`. Vous pourriez vérifier vos config avec `git config -l`. Si ça ne marche pas, essayer de tirer des cartes de tarot ou faire une offrande à la lune (ou bien soumettre un issu). Bon courage.

## Mise en place de l'environnement dev

Vous pouvez installer en local ou utiliser l'environnement [Docker](./docker.md) pour démarrer.

### À installer localement

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Node et npm](https://nodejs.org/en/download/)
- [Postgres](https://www.postgresql.org/download/)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/)
- [pre-commit](https://pypi.org/project/pre-commit/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) (optionnel)

### Installer les dépendances du backend

Les dépendances du backend se trouvent dans `pyproject.toml`.

`uv` va installer les dépendances dans un environment virtuel : 

```
uv sync
```

Ensuite, pour lancer les commandes python du projet, 2 options :
* précéder chaque commande de `uv run` (e.g. `uv run python manage.py runserver`)
* activer l'environment virtuel : `source .venv/bin/activate`

### Installer les dépendances *des* frontends

On utilise les dernières versions LTS de `node` et `npm`.

/!\ Il y a actuellement 2 applications frontend côte à côte.

L'application frontend Vue2 se trouve sous `/frontend`. Pour installer les dépendances :

```
cd frontend
npm ci --ignore-scripts
```

L'application frontend Vue3 se trouve sous `/2024-frontend`. Pour installer les dépendances :

```
cd 2024-frontend
npm ci --ignore-scripts
```

### Créer la base de données

#### Rapide

Pour créer une base de données nommée `macantine_egalim` :

```
createdb macantine-egalim
```

#### Détaillée

Pour créer une base de données nommée `macantine_egalim` avec un utilisateur dédié `macantine_egalim_team`, et définir le mot de passe :

```
psql -c "CREATE USER macantine_egalim_team WITH PASSWORD 'password'"
psql -c "CREATE DATABASE macantine_egalim OWNER macantine_egalim_team"
psql -c "GRANT ALL PRIVILEGES ON DATABASE macantine_egalim to macantine_egalim_team"
psql -c "ALTER USER macantine_egalim_team CREATEROLE CREATEDB"
```

### Compléter les variables d'environnement

L'application utilise [python-dotenv](https://pypi.org/project/python-dotenv/), vous pouvez donc créer un fichier `.env` à la racine du projet avec les variables définies ci-dessous.

*Attention* : Certaines variables d'environnement sont utilisées uniquement dans les **tasks celery** (ex: mise à jours des contacts Brevo). Elles sont alors renseignées dans `celery.md`.
Pour tester ces tâches en local, vous pouvez renseigner ces variables d'environnement dans votre `.env`.

```
SECRET= Le secret pour Django (vous pouvez le [générer ici](https://djecrety.ir/))
DEBUG= `True` pour le développement local ou `False` autrement
DEBUG_FRONT= `True` pour le développement local du 2024-front ou `False` autrement
DEBUG_WEBPACK_PROGRESS= `True` pour afficher la progression lors du build de webpack pour le `frontend`
DB_USER= L'utilisateur de la base de données. Doit avoir les droits de creation de db pour les tests (par ex. 'macantine_egalim_team')
DB_PASSWORD= Le mot de passe pour accéder à la base de données
DB_HOST= Le host de la base de données (par ex. '127.0.0.1')
DB_PORT= Le port de la base de données (par ex. '3306')
DB_NAME= Le nom de la base de données (par ex. 'macantine_egalim')
HOSTNAME= Le hostname dans lequel l'application se trouve (par ex. 127.0.0.1:8000)
ALLOWED_HOSTS= Des noms de domaine/d’hôte que ce site peut servir (par ex. 'localhost, \*')
ENFORCE_HOST= Optionnel - Si présent, les requêtes seront redirigées à ce host
STATICFILES_STORAGE= Le système utilisé pour les fichiers statiques (par ex. 'django.contrib.staticfiles.storage.StaticFilesStorage' ou 'storages.backends.s3.S3Storage')
DEFAULT_FILE_STORAGE= Le système de stockage de fichiers (par ex 'django.core.files.storage.FileSystemStorage' ou 'storages.backends.s3.S3Storage')
FORCE_HTTPS= 'False' si on développe en local, 'True' autrement
SECURE= 'False' si on développe en local, 'True' autrement
EMAIL_BACKEND= par ex. 'django.core.mail.backends.console.EmailBackend'. Pour utiliser SendInBlue : 'anymail.backends.sendinblue.EmailBackend'
DEFAULT_FROM_EMAIL= par ex. 'ma-cantine@example.com'
CONTACT_EMAIL= par ex. 'contact@example.com'
NEWSLETTER_SENDINBLUE_LIST_ID= L'ID de la newsletter de SendInBlue
MATOMO_ID= 162 pour la prod (peut-être laissé vide)
CELLAR_HOST= Optionnel - le host du service S3
CELLAR_KEY= Optionnel - la clé du service S3
CELLAR_SECRET= Optionnel - le secret du service S3
CELLAR_BUCKET_NAME= Optionnel - le nom du bucket S3 à utiliser
DEBUG_PERFORMANCE= Optionnel - à utiliser avec "DEBUG" pour montrer la [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
ENVIRONMENT= Optionnel - si cette variable est remplie un badge sera visible dans l'application et l'admin changera. Les options sont : `dev` | `staging` | `demo` | `prod`
GIT_BRANCH= Optionnel - cette variable permet de préciser la branche à utiliser pour les urls des schemas d'imports
REDIS_URL= L'instance redis à utiliser pour les tâches asynchrones et le cache des clés API. Par exemple : 'redis://localhost:6379/0'
REDIS_PREPEND_KEY= Optionnel - Ajout ce string au début de chaque clé Redis. Utile pour partager la même DB Redis sur plusieurs environnements
OVERRIDE_TEST_SEED= Optionnel - `seed` utilisé par les tests pour les éléments aléatoires. Utile lors qu'un test échoue et qu'on veut reproduire exactement ce qu'il s'est passé.
MONCOMPTEPRO_CLIENT_ID= Optionnel - Client ID utilisé pour l'authentification via [MonComptePro](https://github.com/betagouv/moncomptepro).
MONCOMPTEPRO_SECRET= Optionnel - Secret utilisé pour l'authentification via [MonComptePro](https://github.com/betagouv/moncomptepro).
MONCOMPTEPRO_CONFIG= Optionnel - Url de configuration utilisé pour l'authentification via [MonComptePro](https://github.com/betagouv/moncomptepro). Par exemple : `https://app-test.moncomptepro.beta.gouv.fr/.well-known/openid-configuration`
MAX_DAYS_HISTORICAL_RECORDS= Optionnel - Flag pour indiquer le nombre de jours pendant lequels on garde l'historique des modèles. Utilisé lors d'une tâche Celery.
CSV_PURCHASE_CHUNK_LINES= Optionnel - Définit le nombre de lignes dans chaque chunk pour l'import des achats. Le choix par défaut est de 81920 ce qui représente en moyenne des chunks de 3Mb.
```

### Dates des campagnes

Elles sont définies dans le fichier `macantine.utils.CAMPAIGN_DATES`.

Il est possible de les overrider (pour l'année en cours) grâce aux variables d'environment suivantes :
```
TELEDECLARATION_START_DATE_OVERRIDE= Optionnel (exemple : `2025-01-07`)
TELEDECLARATION_END_DATE_OVERRIDE= Optionnel
CORRECTION_START_DATE_OVERRIDE= Optionnel
CORRECTION_END_DATE_OVERRIDE= Optionnel
```

### Activer les feature flags

```
ENABLE_XP_RESERVATION= Optionnel - `True` pour activer la feature de l'expérimentation des systèmes de réservation.
ENABLE_XP_VEGE= Optionnel - `True` pour activer la feature de l'expérimentation de l'offre quotidien de repas végétariens.
ENABLE_TELEDECLARATION= Optionnel - `True` pour permettre les utilisateurs de télédéclarer leur diagnostic.
ENABLE_DASHBOARD= Optionnel - `True` pour montrer la nouvelle page d'accueil des gestionnaires.
ENABLE_VUE3= Optionnel - `True` pour rendre les nouvelles vues disponibles.
ENABLE_WASTE_MEASUREMENTS= Optionnel - `True` pour rendre l'outil évaluation gaspillage alimentaire disponible
SHOW_BANNER= Optionnel - `True` pour afficher le bandeau d'information sous le menu
```

### Mise à jour des métadonnées sur data.gouv.fr

Nous gérons deux jeux de données sur data.gouv.fr, dont un jeu mis à jour régulièrement : le registre national des cantines.
Afin que l'outil **explore** de data.gouv.fr lise les dernière données, il faut mettre à jour de façon factice l'URL qui pointe vers la ressource.

```
DATAGOUV_API_KEY=<Clé d'API data.gouv.fr d'un compte ayant les droits sur les jeux>
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
NODE_OPTIONS=--openssl-legacy-provider npm run serve
```

> Un bug connu de code legacy avec Webpack sur les versions récentes entraine l'erreur suivante `code: 'ERR_OSSL_EVP_UNSUPPORTED'`. Pour éviter d'avoir à configurer une variable d'environnement en local on peut utiliser le script `npm run serve:ssl-legacy` qui intègre la configuration.

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

## Lancer les tests

### Django

La commande pour lancer les tests Django est :

```
python manage.py test
```

Sur VSCode, ces tests peuvent être debuggés avec la configuration "Python: Tests", présente sur le menu "Run".

Tips :
- lancer les tests plus rapidement : `python manage.py test --keepdb`
- lancer les tests qui ne nécessitent pas internet : `SKIP_TESTS_THAT_REQUIRE_INTERNET=True python manage.py test`

### Vue2

Il faut d'abord se placer sur `/frontend`, ensuite la commande pour lancer les tests VueJS est :

```
cd frontend
npm run test
```

## Creation d'un superuser

Afin de pouvoir s'identifier dans le backoffice (sous `/admin`), il est nécessaire de créer un utilisateur admin avec tous les droits. Pour ce faire, vous pouvez lancer :

```
python manage.py createsuperuser
```

## Utilisation des magic token

Les `magic token` permettent de se connecter à la place d'un utilisateur à des fins de support. Voici comment les utiliser :
* Générer un token depuis l'interface admin de Django
* Déconnecter-vous ou utiliser une navigation privée (recommandé)
* Saisir l'adresse sur le navigateur: `<URL MA CANTINE>/code/<MAGIC TOKEN>`
* Se déconnecter après usage


## Reception d'emails en local

Il y a deux options pour recevoir les emails envoyés depuis l'application en local :

### 1- Les imprimer dans la console

Django permet d'imprimer en console les emails envoyés avec le `django.core.mail.backends.console.EmailBackend`. Pour l'utiliser il suffit de mettre la variable d'environnement `EMAIL_BACKEND` à cette valeur. Cette option est rapide à mettre en place et ne nécessite pas d'autres outils.

Il faut néanmoins tenir en compte que la mise en page ne sera pas visible et que certaines configurations qui marchent avec la console ne marchent pas avec d'autres services email. Nous conseillons plutôt d'utiliser la solution suivante :

### 2- Utiliser Maildev

[Maildev](https://maildev.github.io/maildev/) est un outil ouvert qui exécute un serveur SMTP en local et qui permet de visualiser tous les emails traités. En l'installant de façon globale on peut mettre `django.core.mail.backends.smtp.EmailBackend` comme variable d'environnement `EMAIL_BACKEND` pour l'utiliser.

## Visual Studio Code

Des extensions utiles :

- Django
- EJS Beautify
- EJS langauge support
- ESLint
- Prettier - Code formatter
- Vue Language Features
- Vetur
- vuetify-vscode
- Spell Right

## Git & Github

### Branches

- chaque branche doit partir de `staging`
- `main` sert uniquement pour les déploiements

### Commits

Pas de convention particulière à respecter !
- anglais ou français
- pas besoin de respecter les Conventional Commits (voir ci-dessous)

### PR

- le nommage des PR doit respecter les [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
    - pour pouvoir être bien interprété par `release-please`
- au moins 1 review est nécessaire avant de pouvoir merger
- les PR sont **squashées** avant d'être mergées (option "Squash & Merge" sur Github)
    - pour avoir un historique simple et clair
    - et ainsi plus facilement retrouver la PR qui a effectué un changement donné

### CI

Lorsqu'une PR est ouverte, plusieurs Github Actions vont tourner (tests, sécurité, reviewers...). Elles sont configurées dans le dossier `.github/workflows`.

### Open source

L'ensemble de notre code est ouvert, ne pushez pas de secrets :)

## Déploiement

### Rappels

- sur Clever Cloud, notre app de staging est branchée sur la branche `staging`
- sur Clever Cloud, nos apps de demo et de prod sont branchées sur la branche `main`
- nous utilisons `release-please` (voir #4379) pour automatiser une partie nos déploiements (en particulier le versionnage & la documentation des releases)

### Test déploiement en locale

```
// .env
DEBUG=False
DEBUG_FRONT=False
```

Dans le dossier principal, lancez

```bash
bash ./clevercloud/test-build-with-vue3.sh
python manage.py runserver --insecure
```

Créer des données initiales grâce aux fixtures : `python manage.py loaddata initial_data.json`

### Lancer un déploiement

Pour le déploiement en prod il faut ajouter ces variables d'env :

```
CC_PRE_BUILD_HOOK=./clevercloud/pre-build-hook.sh
CC_PYTHON_MANAGE_TASKS=buildnpm, buildnpmvue3, collectstatic --noinput, migrate --noinput, compilemessages
```

#### Vérification pre-déploiment

- est-ce que les tests passent sur staging ?
- est-ce que tout va bien côté Clever Cloud ?
- est-ce qu'il y a des cherry-picks sur main qui n'existent pas sur staging ?

#### Etapes à suivre

1. grâce à `release-please`, une PR nommée `chore(staging): release YYYY.X.Z` est ouverte, et liste les PR mergées sur `staging` depuis la dernière release
2. il faut merger cette PR. Il se passera alors 2 choses :
    - une nouvelle release va être automatiquement crée : voir [la liste des releases](https://github.com/betagouv/ma-cantine/releases)
        - optionnel : supprimer toutes les lignes dependabot et les remplacer avec une ligne "MAJ dépendances"
    - le CHANGELOG.md sera mis à jour sur `staging`
3. il reste maintenant à déployer (manuellement) en mettant à jour la branche `main`
    - si il y a des variables d'environnement à ajouter, ajoutez-les sur prod et demo côté Clever Cloud
    - en local, preparer la branche `main` : `git checkout staging && git pull && git checkout main && git rebase staging`
    - puis publier les changements : `git push` (peut-être `git push -f`)
4. le déploiement va commencer automatiquement. Ça prend un moment pour déployer côté Clever Cloud... suivez la progression là-bas.
5. une fois le déploiement terminé, envoyer un message sur mattermost (canal produit) pour tenir l'équipe au courant ! (en copiant-collant le contenu de la dernière release)

> Si jamais vous doutez/si il y a un problème, parlez avec un.e autre dév.

### Release notes

Vous pourrez modifier les notes dans un éditeur pour être plus rapide.

- supprimer toutes les lignes dependabot et les remplacer avec une ligne "MAJ dépendances"
- supprimer la partie "by @username in https://..."
- faire n'importe quel autre changement pour rendre la liste facilement comprensible par tout le monde
