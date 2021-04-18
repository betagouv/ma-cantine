# API

Pour lancer les tests: `npm run test`
Pour lancer l'api: `npm run start`

N'oubliez pas de `npm install` la première fois que vous installez ce projet.

## Variables d'environnements

```
SENDINBLUE_API_KEY=
SENDINBLUE_SENDER_EMAIL=
SENDINBLUE_CONTACT_EMAIL=
DB_NAME=
TEST_DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

## BDD

### Pour installer PostgreSQL :

#### OSX
```
brew install postgres
brew services start postgresql

```

#### Linux
```
sudo apt-get install postgresql
sudo -i -u postgres
```

### Pour configurer PostgreSQL :

```
psql postgres
CREATE ROLE me with LOGIN PASSWORD 'password';
ALTER ROLE me CREATEDB;
\q
psql -d postgres -U me
CREATE DATABASE test;
\c test
\conninfo
```

Récupérer l'information du port en utilisant l'information donnée par `\conninfo`, completez une fichier `.env` dans `ma-cantine/api` (ici) avec:

```
TEST_DB_NAME=test
DB_USERNAME=me
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=XXXX
```
