# ma cantine

Accompagner au mieux les acteurs de la restauration collective dans leur offre aux consommateurs pour une alimentation de qualité, saine et durable.

[Le site](https://ma-cantine.agriculture.gouv.fr)

[En savoir plus](https://beta.gouv.fr/startups/ma-cantine-egalim.html)

## Aspects techniques

Si vous voulez installer l'environnement en local : [ONBOARDING.md](./ONBOARDING.md)

### Architecture

On utilise [Django](https://www.djangoproject.com/) au back-end et [Vue.js (V2)](https://v2.vuejs.org/) au front.

Le produit est découpé en applications. Les applications les plus modifiées :

- `frontend` : le côté visible aux utilisateur.ice.s
- `data` : contenant la plupart de notre modèles et vue admin
- `api` : fournit l'API du backend
- `web` : l'application d'authentification du site et le source de quelques fichiers statiques

### Infrastructure

L’hébergement est fait chez [Clever Cloud](https://www.clever-cloud.com/). Ceci concerne l'application, la base de données, les fichiers statiques, et l'instance Metabase.

### Outillage

- [Github](https://github.com/) pour l'hébergement du code et l'intégration continue
- [Sentry](https://sentry.io) pour le reporting des erreurs
- [SendInBlue](https://fr.sendinblue.com/) pour l'envoi d'emails
- [AlwaysData](https://www.alwaysdata.com/fr/) pour la gestion des DNS
- [Metabase](https://ma-cantine-metabase.cleverapps.io/public/dashboard/f65ca7cc-c3bd-4cfb-a3dc-236f81864663) pour l'analyse et la visualisation des données
- [Matomo](https://stats.data.gouv.fr/index.php?module=CoreHome&action=index&idSite=162&period=range&date=previous30&updated=1) pour l'analyse du traffic web
- [ELK](http://kibana-bxrbvv38clpvd6tvzpkz-elasticsearch.services.clever-cloud.com/) afin de gérer les logs nous utilisons une base de données ElasticSearch avec un frontend Kibana. Les logs applicatifs sont gardés pendant trois mois.
