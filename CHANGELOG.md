# Journal des modifications

Ressources :
- [CHANGELOG recommendations](https://keepachangelog.com/)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [release-please](https://github.com/google-github-actions/release-please-action) (automated releases)
- [Semantic Versioning](https://semver.org/) & [Calendar Versioning](https://calver.org/)

## [2025.1.0](https://github.com/betagouv/ma-cantine/compare/v2025.0.3...v2025.1.0) (2025-01-14)


### Nouveautés

* définition et séparation du worker dans Docker ([#4774](https://github.com/betagouv/ma-cantine/issues/4774)) ([48c555b](https://github.com/betagouv/ma-cantine/commit/48c555bc8539460e962bdcd98ea0cdd0efa30120))


### Améliorations

* **Imports achats:** supprimer les fichiers d'exemples excel & odf ([#4894](https://github.com/betagouv/ma-cantine/issues/4894)) ([086cea0](https://github.com/betagouv/ma-cantine/commit/086cea00fa46ffd52e7fce9b7ebe5a425817b980))
* **Imports cantines/diagnostics:** supprimer les fichiers d'exemples excel & odf ([#4892](https://github.com/betagouv/ma-cantine/issues/4892)) ([6269098](https://github.com/betagouv/ma-cantine/commit/6269098a94d6bef4939933b6620254fcab3ed763))


### Corrections (bugs, typos...)

* **Télédéclarations:** fix de l'année de fin (typo 2024 au lieu de 2025) ([#4890](https://github.com/betagouv/ma-cantine/issues/4890)) ([474d641](https://github.com/betagouv/ma-cantine/commit/474d6418382316e61f11b83823d5f8593a8bde6b))


### Documentation

* **Onboarding:** mise à jour de la doc de déploiement suite à la mise en place de release-please ([#4873](https://github.com/betagouv/ma-cantine/issues/4873)) ([4b7735d](https://github.com/betagouv/ma-cantine/commit/4b7735db630c06c787f5880405d72361bb087a3f))


### Technique

* écrire EGalim partout (au lieu d'EGAlim ou Egalim ou EGALIM) ([#4883](https://github.com/betagouv/ma-cantine/issues/4883)) ([4d0b877](https://github.com/betagouv/ma-cantine/commit/4d0b877a90b03d140dab8027399c79b2d9dca652))
* **Télédéclaration:** Nouvelles versions disponibles pour les documents d'aide ([#4885](https://github.com/betagouv/ma-cantine/issues/4885)) ([196bb10](https://github.com/betagouv/ma-cantine/commit/196bb1064660b2ee653dfc7448bba5cc8ffdba09))

## [2025.0.3](https://github.com/betagouv/ma-cantine/compare/v2025.0.2...v2025.0.3) (2025-01-10)


### Corrections (bugs, typos...)

* **Imports de masse:** Cantines : ajoute les accents à modèle_économique. ref [#4856](https://github.com/betagouv/ma-cantine/issues/4856) ([1f39743](https://github.com/betagouv/ma-cantine/commit/1f397434e65587b6e944b37add4d0edcd9367570))

## [2025.0.2](https://github.com/betagouv/ma-cantine/compare/v2025.0.1...v2025.0.2) (2025-01-10)


### Améliorations

* **Import fichiers:** Ajout d'une modale pour informer l'utilisateur sur la validation de son import et qu'il lui reste à le télédéclarer ([#4860](https://github.com/betagouv/ma-cantine/issues/4860)) ([9648800](https://github.com/betagouv/ma-cantine/commit/964880080d592c0c88c8ad57aade9701f9b065b6))
* **Imports de masse:** utiliser le schema JSON des cantines & diagnostics pour l'affichage aux utilisateurs ([#4856](https://github.com/betagouv/ma-cantine/issues/4856)) ([e0a5ea3](https://github.com/betagouv/ma-cantine/commit/e0a5ea329279af236a288f2048d98bd3b1a163c8))


### Corrections (bugs, typos...)

* **Imports de masse:** fix des URL qui pointent vers les schemas cantines & diagnostics. ref [#4856](https://github.com/betagouv/ma-cantine/issues/4856) ([6d4b93b](https://github.com/betagouv/ma-cantine/commit/6d4b93bb867b30ab7c459ca5829c5ab9da7a71e6))


### Documentation

* **Imports de masse:** ajout d'une section dans le README listant les schémas ([#4865](https://github.com/betagouv/ma-cantine/issues/4865)) ([ebb2aa6](https://github.com/betagouv/ma-cantine/commit/ebb2aa6bc10c8243d8430edc3e47a7ecdd7f1631))


### Technique

* enlève Helen de la liste des auto-reviewers ([#4872](https://github.com/betagouv/ma-cantine/issues/4872)) ([3247cd0](https://github.com/betagouv/ma-cantine/commit/3247cd0294078ba7dee1d9bcf5393152ba9275f4))
* **Vue-cli:** Cache les logs de build du frontend (webpack) ([#4876](https://github.com/betagouv/ma-cantine/issues/4876)) ([a96c0f2](https://github.com/betagouv/ma-cantine/commit/a96c0f24b28b589241a467361f3c44aa250e1cb3))

## [2025.0.1](https://github.com/betagouv/ma-cantine/compare/v2025.0.0...v2025.0.1) (2025-01-09)


### Améliorations

* **Imports de masse:** Indiquer que le header est obligatoire & expliciter le nom des colonnes ([#4858](https://github.com/betagouv/ma-cantine/issues/4858)) ([765cf61](https://github.com/betagouv/ma-cantine/commit/765cf61f5c78a7a3764a083a99f7b8577a2d39de))


### Corrections (bugs, typos...)

* **Imports de masse:** Cantines : enlève annee_bilan du schema ([#4868](https://github.com/betagouv/ma-cantine/issues/4868)) ([e5e0eaf](https://github.com/betagouv/ma-cantine/commit/e5e0eaf7caf1246837fb71237901fb930862069f))
* **Imports de masse:** Diagnostics : corrige les position des champs siret & nom ([#4869](https://github.com/betagouv/ma-cantine/issues/4869)) ([5cabc7c](https://github.com/betagouv/ma-cantine/commit/5cabc7cd80fc0bb46a1d253f43ed56dac1734ca8))
* **Imports de masse:** Diagnostics : corrige une typo (boulangzrie) ([#4863](https://github.com/betagouv/ma-cantine/issues/4863)) ([4ffa49d](https://github.com/betagouv/ma-cantine/commit/4ffa49d80d3e8149f59fec383261faca22996311))
* **Imports de masse:** Diagnostics : généralise le nommage du champ nombre_satellites ([#4870](https://github.com/betagouv/ma-cantine/issues/4870)) ([95a1dd4](https://github.com/betagouv/ma-cantine/commit/95a1dd448c8ba444e5dae5483b19894205a7f9ff))
* **Imports de masse:** Diagnostics : généralise le nommage du champ siret_livreur_repas ([#4871](https://github.com/betagouv/ma-cantine/issues/4871)) ([07cecad](https://github.com/betagouv/ma-cantine/commit/07cecad6616bb962408365ad697f76829474e9bf))
* **Imports de masse:** ré-ajoute la ligne indiquant aux utilisateurs que l'ordre des champs est important. ref [#4804](https://github.com/betagouv/ma-cantine/issues/4804) ([81f3413](https://github.com/betagouv/ma-cantine/commit/81f3413e5e2d1a9d3645591ee933b2e51f00e459))
* **Logo:** Changement de Marianne ([#4866](https://github.com/betagouv/ma-cantine/issues/4866)) ([9eddea7](https://github.com/betagouv/ma-cantine/commit/9eddea7ee914f7bad2b8b4da0e90a9be9fdb2bad))


### Technique

* **Import de masse:** basculer la logique de documentation (schema -&gt; table) dans un composant dédié ([#4854](https://github.com/betagouv/ma-cantine/issues/4854)) ([7f65351](https://github.com/betagouv/ma-cantine/commit/7f65351b6085fccacd428d4b5ff7a6c2fea633a6))

## [2025.0.0](https://github.com/betagouv/ma-cantine/compare/v2024.14.0...v2025.0.0) (2025-01-07)


### Améliorations

* **Footer et Header:** Changement du nom du ministère ([#4849](https://github.com/betagouv/ma-cantine/issues/4849)) ([3543871](https://github.com/betagouv/ma-cantine/commit/3543871cb78feecb909b3188ef31ec82862591e4))
* **Import de masse:** utiliser le schema JSON des achats pour l'affichage du tableau aux utilisateurs ([#4832](https://github.com/betagouv/ma-cantine/issues/4832)) ([bfffc29](https://github.com/betagouv/ma-cantine/commit/bfffc2982984f9b9675911efa84151299a312de6))
* **Imports de masse:** Mise à jour des fichiers templates ([#4845](https://github.com/betagouv/ma-cantine/issues/4845)) ([faadb5a](https://github.com/betagouv/ma-cantine/commit/faadb5a13c713fefa5725bf2d5a066d1a3edb7fb))
* **Télédéclaration:** Amélioration des messages de modification d'une télédéclaration ([#4850](https://github.com/betagouv/ma-cantine/issues/4850)) ([9547a68](https://github.com/betagouv/ma-cantine/commit/9547a6843f8153df11f09523e372109391d13cac))


### Corrections (bugs, typos...)

* **Import de masse:** fix de l'URL qui pointe vers le schema. ref [#4832](https://github.com/betagouv/ma-cantine/issues/4832) ([ef262b0](https://github.com/betagouv/ma-cantine/commit/ef262b06e3d817963b480fe4a5f7b562f655f38e))
* **Nom du ministère:** Changement de nom ([#4852](https://github.com/betagouv/ma-cantine/issues/4852)) ([4d6689a](https://github.com/betagouv/ma-cantine/commit/4d6689a04b226225417fab6c442c83fc8222825c))


### Technique

* **deps:** bump django-modelcluster from 6.3 to 6.4 ([#4815](https://github.com/betagouv/ma-cantine/issues/4815)) ([422d3c4](https://github.com/betagouv/ma-cantine/commit/422d3c403bb249a68988196245ab87a1b8ca9822))
* **deps:** bump pypdf from 4.2.0 to 5.1.0 ([#4816](https://github.com/betagouv/ma-cantine/issues/4816)) ([2d1f02c](https://github.com/betagouv/ma-cantine/commit/2d1f02c5967e9df82ff01fa58e537ef1af8112bd))
* **deps:** bump sqlparse from 0.5.1 to 0.5.3 ([#4818](https://github.com/betagouv/ma-cantine/issues/4818)) ([0264871](https://github.com/betagouv/ma-cantine/commit/02648712a7a0a0cd165b7162d499f150a813330f))
* release 2025.0.0 ([e284e52](https://github.com/betagouv/ma-cantine/commit/e284e527f007d99154455d8f309ae6a998511d47))

## [2024.14.0](https://github.com/betagouv/ma-cantine/compare/v2024.13.1...v2024.14.0) (2025-01-06)


### Nouveautés

* **open-data:** Publication jeu données résultat de la campagne 2023 ([#4814](https://github.com/betagouv/ma-cantine/issues/4814)) ([eb53535](https://github.com/betagouv/ma-cantine/commit/eb5353588fb9ffa66b784065e76f2ccfa413a555))


### Améliorations

* **Imports de masse:** Rendre le header obligatoire pour les achats ([#4794](https://github.com/betagouv/ma-cantine/issues/4794)) ([cdc88ef](https://github.com/betagouv/ma-cantine/commit/cdc88ef18155a55b5296a33758ebd48d68a26507))
* **Imports de masse:** Rendre le header obligatoire pour les cantines/diagnostics ([#4804](https://github.com/betagouv/ma-cantine/issues/4804)) ([853da75](https://github.com/betagouv/ma-cantine/commit/853da7554f670c3251635314ccabac65ca2f4ddd))
* **Tableau de bord:** L'affichage du bandeau de communication est conditionné avec une variable d'env dédiée ([#4801](https://github.com/betagouv/ma-cantine/issues/4801)) ([7f7964c](https://github.com/betagouv/ma-cantine/commit/7f7964c9ac10dbc7830f5d0ca2a62a51d5a70487))
* **Teledeclaration:** Améliore la visibilité du statut et de la progression de la télédéclaration ([#4803](https://github.com/betagouv/ma-cantine/issues/4803)) ([a5b12de](https://github.com/betagouv/ma-cantine/commit/a5b12de6d4a72622d74f71203fee9c2ace8642db))


### Corrections (bugs, typos...)

* ajout des dates de la campagne de télédéclaration pour 2024 ([#4824](https://github.com/betagouv/ma-cantine/issues/4824)) ([3d083ae](https://github.com/betagouv/ma-cantine/commit/3d083ae787dbf220004bb08967d38380a3d33cb2))
* **Mentions légales:** renommer Clevercloud en Clever Cloud. ref [#4725](https://github.com/betagouv/ma-cantine/issues/4725) ([1283870](https://github.com/betagouv/ma-cantine/commit/1283870f7e50ab813e537d8e6a9db53ad09e1b96))
* **Page Contactez-nous:** Le style doit être contraint à la page uniquement ([#4826](https://github.com/betagouv/ma-cantine/issues/4826)) ([7b1ec18](https://github.com/betagouv/ma-cantine/commit/7b1ec18ba832a7b9a2cf0e34ceaa5214c84cf515))


### Documentation

* **Backup:** Comment restaurer un backup en locale et comment recuperer les IDs d'objets supprimées ([#4771](https://github.com/betagouv/ma-cantine/issues/4771)) ([73de9ba](https://github.com/betagouv/ma-cantine/commit/73de9ba1b6c6b9fe843a267053b2ca3f6f9a6090))


### Technique

* **CGU:** Migration de la page sur vue 3 ([#4828](https://github.com/betagouv/ma-cantine/issues/4828)) ([192e10f](https://github.com/betagouv/ma-cantine/commit/192e10f12fa53f1214eebc9b5e47959d8b290fb9))
* **Déclaration d'accessibilité:** Migration de la page sur vue 3 ([#4830](https://github.com/betagouv/ma-cantine/issues/4830)) ([71fbbd9](https://github.com/betagouv/ma-cantine/commit/71fbbd9c90cfd57a5e5541f64874c26f843dd8b8))
* **Dependabot:** change la fréquence de weekly à monthly 🤖 ([#4806](https://github.com/betagouv/ma-cantine/issues/4806)) ([9031773](https://github.com/betagouv/ma-cantine/commit/9031773fb4de132880f089d916dfee834cf49942))
* **deps-dev:** bump eslint from 9.15.0 to 9.17.0 in /2024-frontend ([12b334b](https://github.com/betagouv/ma-cantine/commit/12b334b478f82edfb22f05d964851227f912a277))
* **deps-dev:** bump prettier from 3.3.3 to 3.4.2 in /2024-frontend ([#4731](https://github.com/betagouv/ma-cantine/issues/4731)) ([85fa2da](https://github.com/betagouv/ma-cantine/commit/85fa2da97bc58b855aebd2b4cb00da94eb8a9317))
* **deps-dev:** bump sass from 1.81.0 to 1.83.0 in /frontend ([db60342](https://github.com/betagouv/ma-cantine/commit/db603426f7ed19c33df34ab10cbcee47efde5c9e))
* **deps-dev:** bump vite-plugin-vue-devtools in /2024-frontend ([5fda145](https://github.com/betagouv/ma-cantine/commit/5fda1459b2c8ce209d033f5f35742296d8a58ff0))
* **deps:** bump @vueuse/core from 11.3.0 to 12.0.0 in /2024-frontend ([a7bd3b6](https://github.com/betagouv/ma-cantine/commit/a7bd3b6a93a7dfe7cce23b51d726dac35fa88ea6))
* **deps:** bump astroid from 3.3.5 to 3.3.6 ([#4737](https://github.com/betagouv/ma-cantine/issues/4737)) ([140aabd](https://github.com/betagouv/ma-cantine/commit/140aabd3cd61c6c7d4decf782aba2ac71b4b81d8))
* **deps:** bump djlint from 1.34.1 to 1.36.3 ([#4740](https://github.com/betagouv/ma-cantine/issues/4740)) ([f8da40e](https://github.com/betagouv/ma-cantine/commit/f8da40e510a908d40bf0b26890db343fd78f56f5))
* **deps:** bump nanoid from 3.3.7 to 3.3.8 in /2024-frontend ([#4761](https://github.com/betagouv/ma-cantine/issues/4761)) ([58070ec](https://github.com/betagouv/ma-cantine/commit/58070ece1d1ef2adc18291ea0010425ffc92bf64))
* **deps:** bump pinia from 2.2.6 to 2.3.0 in /2024-frontend ([5faf279](https://github.com/betagouv/ma-cantine/commit/5faf2791899eaa02994e120fc85f0291ee586040))
* **deps:** bump tomli from 2.0.1 to 2.2.1 ([#4738](https://github.com/betagouv/ma-cantine/issues/4738)) ([4bc620e](https://github.com/betagouv/ma-cantine/commit/4bc620e5e7eb0a6478b1eb2467c36ee3d3019143))
* **deps:** bump vue-router from 4.4.5 to 4.5.0 in /2024-frontend ([49f576b](https://github.com/betagouv/ma-cantine/commit/49f576b271b3cf5a0c57aaa2a86a37ade167efcc))
* **deps:** bump wrapt from 1.16.0 to 1.17.0 ([#4736](https://github.com/betagouv/ma-cantine/issues/4736)) ([3bd2c93](https://github.com/betagouv/ma-cantine/commit/3bd2c934b807d808fbb3744d9e7f8627f89e4125))
* **Mentions légales:** enlève des classes inutiles ou inutilisées ([#4829](https://github.com/betagouv/ma-cantine/issues/4829)) ([9d88459](https://github.com/betagouv/ma-cantine/commit/9d88459c6d249becf347f2258f98e8f7849e0bcf))
* **Review apps:** ajout du lien vers l'environment github 'review-apps'. ref [#4825](https://github.com/betagouv/ma-cantine/issues/4825) ([11d23f2](https://github.com/betagouv/ma-cantine/commit/11d23f2060c8361180a8b9973926eea906e9cc83))
* **Review apps:** première configuration des review apps avec Clever Cloud ([#4825](https://github.com/betagouv/ma-cantine/issues/4825)) ([28b0d61](https://github.com/betagouv/ma-cantine/commit/28b0d61205b151f1e4f15403404db8423e027d66))
* **Review apps:** remplace la version par v1.1.1. ref [#4825](https://github.com/betagouv/ma-cantine/issues/4825) ([712aafc](https://github.com/betagouv/ma-cantine/commit/712aafcb533f3a55e2aec58b5a5d2f2ecdbdd163))

## [2024.13.1](https://github.com/betagouv/ma-cantine/compare/v2024.13.0...v2024.13.1) (2024-12-18)


### Améliorations

* **Achats:** Admin: Quelques améliorations dans la vue list (lien vers la cantine, colonne Suppr, date de création) ([#4791](https://github.com/betagouv/ma-cantine/issues/4791)) ([b406645](https://github.com/betagouv/ma-cantine/commit/b406645f3ca0afa63df69bc29885fbd81000a00b))
* **Cantine synthèse:** réorganise les champs suite aux modifications dans le formulaire ([#4793](https://github.com/betagouv/ma-cantine/issues/4793)) ([62611c0](https://github.com/betagouv/ma-cantine/commit/62611c073ef08602e640b4db080f446606a3e64a))
* **Contactez-Nous:** Migration de la page sur vue3 ([#4773](https://github.com/betagouv/ma-cantine/issues/4773)) ([f34f533](https://github.com/betagouv/ma-cantine/commit/f34f53386c21b1d7b23fe2305ff65f1db0d8bbec))
* **Diagnostique Approvisionnement:** Rendre l'antisèche des achats plus visible ([#4779](https://github.com/betagouv/ma-cantine/issues/4779)) ([998676d](https://github.com/betagouv/ma-cantine/commit/998676d0ac35558e559b700bf8532535b1eb4d58))
* **Formulaire cantine:** Affiche le champ 'Administration de tutelle' seulement pour les cantines publiques ([#4788](https://github.com/betagouv/ma-cantine/issues/4788)) ([b374d29](https://github.com/betagouv/ma-cantine/commit/b374d2923cb19aec2352d41a978aeae46595a41c))
* **Matomo:** Ajout du tracking sur notre frontend vue3 ([#4796](https://github.com/betagouv/ma-cantine/issues/4796)) ([c02b89a](https://github.com/betagouv/ma-cantine/commit/c02b89abc8f7224117a6ff304f86ac6301a25ce4))
* **Secteurs:** Admin: afficher la colonne "Ministère de tutelle" ([#4785](https://github.com/betagouv/ma-cantine/issues/4785)) ([e0222a0](https://github.com/betagouv/ma-cantine/commit/e0222a0b5ff75d636e43f567b4bd35ac45b00ac4))


### Corrections (bugs, typos...)

* **Contact Page:** l'image empêchait de build le frontend vu3 ([#4800](https://github.com/betagouv/ma-cantine/issues/4800)) ([cf6ed12](https://github.com/betagouv/ma-cantine/commit/cf6ed12dfe1c2b0f4c58330c061bfa5b36323dc1))
* **Tableau de bord:** Pour l'année en cours, afficher la graphe appro des achats si l'outil suivi achats est utilisé ([#4762](https://github.com/betagouv/ma-cantine/issues/4762)) ([f963e11](https://github.com/betagouv/ma-cantine/commit/f963e11fe785765af4af6c57f9adca5a7a14f805))


### Documentation

* **Onboarding:** Ajout section magic token ([#4776](https://github.com/betagouv/ma-cantine/issues/4776)) ([09f242a](https://github.com/betagouv/ma-cantine/commit/09f242add240b1c3951c055bae78fd6cfee608b4))


### Technique

* Ajoute une nouvelle section 'Documentation' dans nos release ([#4792](https://github.com/betagouv/ma-cantine/issues/4792)) ([5b5b19b](https://github.com/betagouv/ma-cantine/commit/5b5b19bc7f4232e2fd55aa3f9c0be5a6aa5d21fe))
* **deps-dev:** Bump numpy from 2.0.0 to 2.2.0 ([#4739](https://github.com/betagouv/ma-cantine/issues/4739)) ([e5eae34](https://github.com/betagouv/ma-cantine/commit/e5eae3482150095c660a19060cbd54fca412ac90))

## [2024.13.0](https://github.com/betagouv/ma-cantine/compare/v2024.12.0...v2024.13.0) (2024-12-12)


### Nouveautés

* **Diagnostique:** nouveau champ service_type pour stocker le type de service proposé par la cantine ([#4720](https://github.com/betagouv/ma-cantine/issues/4720)) ([0e57f40](https://github.com/betagouv/ma-cantine/commit/0e57f40248ab42eab95d05440e77fd078664a5fb))
* **Tunnel diagnostique:** Menu végé : nouvelle étape "options proposées aux convives" ([#4727](https://github.com/betagouv/ma-cantine/issues/4727)) ([c57a5cc](https://github.com/betagouv/ma-cantine/commit/c57a5cc02beabd085fde2915744e04562023e7f6))


### Améliorations

* **Formulaire cantine:** ajout de titre de sections, remonte 2 champs ([#4759](https://github.com/betagouv/ma-cantine/issues/4759)) ([fd8144d](https://github.com/betagouv/ma-cantine/commit/fd8144d78d2b700bf531d3bdc61b97370fcb9d0d))
* **Teledeclaration:** Changement des dates et des liens pour l'ouverture de campagne 2025 ([#4765](https://github.com/betagouv/ma-cantine/issues/4765)) ([11f7b15](https://github.com/betagouv/ma-cantine/commit/11f7b150cf9dd1f6e5b77b8ace723c9c2026a9fe))


### Corrections (bugs, typos...)

* **Diagnostic:** N'accepte pas les valeurs moins de 0 ([#4766](https://github.com/betagouv/ma-cantine/issues/4766)) ([8fc78ec](https://github.com/betagouv/ma-cantine/commit/8fc78ecaf9514017d16dbe39964b60ce2b183b00))
* **Import achats:** Améliorer le message d'erreur pour un fichier du mauvais format ([#4767](https://github.com/betagouv/ma-cantine/issues/4767)) ([3b6bdda](https://github.com/betagouv/ma-cantine/commit/3b6bdda193cbf158004517fd975d09eb7d84326b))
* **Import cantines:** reparer le cas où on veut ajouter des gestionnaires mais on n'a pas des colonnes vides en plus ([#4754](https://github.com/betagouv/ma-cantine/issues/4754)) ([9d25df1](https://github.com/betagouv/ma-cantine/commit/9d25df1e4e0c7a64898ad5014969807ec0e2fffc))


### Technique

* **api:** Suppression de la création d'une télédéclaration depuis l'API par une tierce application ([#4723](https://github.com/betagouv/ma-cantine/issues/4723)) ([eaeaa91](https://github.com/betagouv/ma-cantine/commit/eaeaa91bd1eaf20a1e6c0584040514fedf1159ee))

## 2024.12.0 (2024-12-11)


### Nouveautés

* **Accueil gestionnaire:** rendre le tableau actions plus trouvable (affichage liste) ([#4746](https://github.com/betagouv/ma-cantine/issues/4746)) ([164c074](https://github.com/betagouv/ma-cantine/commit/164c0748808bef25cd48a8f4791b32efd20eb821))
* **Cantines:** Renommage du label "Ministère de tutelle" ([#4719](https://github.com/betagouv/ma-cantine/issues/4719)) ([9ac31f2](https://github.com/betagouv/ma-cantine/commit/9ac31f2dd0200a5e54c3ee03279e679f36da0b3d))


### Améliorations

* **Mentions légales:** Migration de la page sur vue 3 ([#4725](https://github.com/betagouv/ma-cantine/issues/4725)) ([74ad0c2](https://github.com/betagouv/ma-cantine/commit/74ad0c2203b8575be8efa0547e9bc3e77aba290a))


### Technique

* Ajoute un nouveau type 'improve' dans la config release-please ([#4758](https://github.com/betagouv/ma-cantine/issues/4758)) ([db97d73](https://github.com/betagouv/ma-cantine/commit/db97d73118315feca91e88fdab83da56dcdb6692))
* **Diagnostique:** renomme les enum végé (MenuType & MenuFrequency) pour clarifier ([#4717](https://github.com/betagouv/ma-cantine/issues/4717)) ([b64642c](https://github.com/betagouv/ma-cantine/commit/b64642c53f3700770d213def830bd6dd382b6ef5))
* Github Action pour checker que le nom des PR respecte le format Conventional Commits ([#4700](https://github.com/betagouv/ma-cantine/issues/4700)) ([adbec3c](https://github.com/betagouv/ma-cantine/commit/adbec3cae0518426c853730148a27446b4108bd8))
* Github Action pour lancer release-please ([#4701](https://github.com/betagouv/ma-cantine/issues/4701)) ([2ab220b](https://github.com/betagouv/ma-cantine/commit/2ab220b5d01440f33d815396239de08565d754b6))
* Création d'un script pour corriger l'erreur Webpack ERR_OSSL_EVP_UNSUPPORTED au lancement de l'app en local


## [2024-12-09](https://github.com/betagouv/ma-cantine/compare/2024-11-29...2024-12-09)

### Outil suivi déchets alimentaires

- Tunnel gaspillage alimentaire : ajouter plus de contexte dans la synthèse évaluation déchets

### Tunnel bilan/TD

- Menu végé : changements cosmétiques sur l'étape 1, renommer le champ de l'étape 2
- Option pour ajouter des évaluations déchets alimentaires depuis le tunnel bilan gaspillage

- refactor(Page Ma Collectivité) : Maj des filtres des diagnostics afin d'avoir les mêmes données que le rapport

### Bug fix

- fix(Tunnel Diagnostique): Gaspillage: répare la fermeture de la modale XP réservation

### Téchnique

- CI : Homogénéisation des versions utilisées par pre-commit pour vue3
- MAJ dépendences

## New Contributors

- @Charline-L made their first contribution in https://github.com/betagouv/ma-cantine/pull/4728
