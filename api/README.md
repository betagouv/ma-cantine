# API

Pour tester: `npm run test`
Pour démarré: `npm run start`

N'oubliez pas de `npm install` le premiere fois que vous installer ce projet.

## Setup

On doit avoir une fichier `.env` avec les variables:

```
SENDINBLUE_API_KEY=
SENDINBLUE_SENDER_EMAIL=
SENDINBLUE_CONTACT_EMAIL=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### BDD

On doit avoir une base de données (BDD) pour utiliser `api`. Pour démarrer un instance d'une BDD PostgreSQL sur OSX, ouvrez un Terminal et suivez:

```
brew install postgres
brew services start postgresql
psql postgres
CREATE ROLE me with LOGIN PASSWORD 'password';
ALTER ROLE me CREATEDB;
\q
psql -d postgres -U me
CREATE DATABASE test;
\c test
\conninfo
```

En utilisant l'information donnée par `\conninfo`, completez une fichier `.env` dans `ma-cantine/api` (ici) avec:

```
DB_NAME=test
DB_USERNAME=me
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=XXXX
```

Pour arretez postgres: `brew services stop postgres`.
