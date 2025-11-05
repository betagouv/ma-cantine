# ma cantine

Accompagner au mieux les acteurs de la restauration collective dans leur offre aux consommateurs pour une alimentation de qualité, saine et durable.

* [https://ma-cantine.agriculture.gouv.fr](https://ma-cantine.agriculture.gouv.fr)
* [https://beta.gouv.fr/startups/ma-cantine-egalim.html](https://beta.gouv.fr/startups/ma-cantine-egalim.html)

## Aspects techniques

Si vous voulez installer l'environnement en local : [ONBOARDING.md](./docs/ONBOARDING.md)

### Architecture

On utilise [Python Django](https://www.djangoproject.com) pour le backend et l'API, et [Vue.js (v2)](https://v2.vuejs.org) pour le frontend. On est en train de migrer progressivement vers [Vue.js (v3)](https://fr.vuejs.org).

Le produit est découpé en applications. Les applications les plus modifiées :

- `frontend` & `2024-frontend` : le côté visible aux utilisateur.ice.s
- `data` : contient la plupart de nos modèles et l'interface admin
- `api` : fournit l'API
- `web` : l'application d'authentification du site et le source de quelques fichiers statiques

### Infrastructure

L’hébergement est fait chez [Clever Cloud](https://www.clever-cloud.com). Ceci concerne l'application, la base de données, les fichiers statiques, et l'instance [Metabase](https://www.metabase.com).

### Outillage

- [Github](https://github.com) pour l'hébergement du code et l'intégration continue
- [Sentry](https://sentry.io) pour le reporting des erreurs
- [Brevo](https://www.brevo.com/fr) pour l'envoi d'e-mails
- [Crisp](https://crisp.chat/fr/) pour le support utilisateur
- [AlwaysData](https://www.alwaysdata.com/fr) pour la gestion des DNS
- [Metabase](https://www.metabase.com) pour l'analyse et la visualisation des données : [nos statistiques publiques](https://ma-cantine-metabase.cleverapps.io/public/dashboard/f65ca7cc-c3bd-4cfb-a3dc-236f81864663)
- [Matomo](https://fr.matomo.org) pour l'analyse du traffic web : [nos statistiques publiques](https://stats.beta.gouv.fr/index.php?idSite=78) ([anciennes données](https://stats.data.gouv.fr/index.php?idSite=162))
