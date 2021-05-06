# API

Pour lancer les tests: `npm run test`
Pour lancer l'api: `npm run start`

N'oubliez pas de `npm install` la première fois que vous installez ce projet.

## Variables d'environnements

```
SENDINBLUE_API_KEY=
SENDINBLUE_SENDER_EMAIL=
SENDINBLUE_CONTACT_EMAIL=
SENDINBLUE_LIST_ID=
DATABASE_URL=
TEST_DATABASE_URL=
JWT_SECRET_KEY=
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
TEST_DATABASE_URL=postgres://me:password@localhost:5432/test
```

#### Migrations

`npm run db:migrate`

Lisez plus:

 - https://github.com/sequelize/cli
 - https://sequelize.org/master/manual/migrations.html
