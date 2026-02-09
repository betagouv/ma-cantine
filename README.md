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

### Outillage

- [Clever Cloud](https://www.clever-cloud.com) pour l'hébergement du serveur
- [Github](https://github.com) pour l'hébergement du code et l'intégration continue
- [Sentry](https://sentry.io) pour le reporting des erreurs
- [Brevo](https://www.brevo.com/fr) pour l'envoi d'e-mails
- [Crisp](https://crisp.chat/fr/) pour le support utilisateur
- [AlwaysData](https://www.alwaysdata.com/fr) pour la gestion des DNS
- [Metabase](https://www.metabase.com) pour l'analyse et la visualisation des données
- [Matomo](https://fr.matomo.org) pour l'analyse du traffic web
