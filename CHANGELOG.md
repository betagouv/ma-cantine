# Journal des modifications

Ressources :
- [CHANGELOG recommendations](https://keepachangelog.com/)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [release-please](https://github.com/google-github-actions/release-please-action) (automated releases)
- [Semantic Versioning](https://semver.org/) & [Calendar Versioning](https://calver.org/)

## [2025.10.0](https://github.com/betagouv/ma-cantine/compare/v2025.9.0...v2025.10.0) (2025-03-17)


### Nouveautés

* **Ajouter une cantine:** ajout de la fonctionnalité de recherche et de rattachement à une unité légale ([#5127](https://github.com/betagouv/ma-cantine/issues/5127)) ([a3bd143](https://github.com/betagouv/ma-cantine/commit/a3bd1436cc7e6d895641276d443885a5b53cebb5))
* **Ajouter une cantine:** remplace l'ancienne url par la nouvelle dans l'application ([#5129](https://github.com/betagouv/ma-cantine/issues/5129)) ([67308c8](https://github.com/betagouv/ma-cantine/commit/67308c8c48e89ddfd6911ae6a4d57c803f674281))


### Améliorations

* **Ajouter une cantine:** divers correctifs et améliorations de wordings ([#5128](https://github.com/betagouv/ma-cantine/issues/5128)) ([cfd95d7](https://github.com/betagouv/ma-cantine/commit/cfd95d70e30e51ae7b75495d1e6f980c1d04a427))
* **Cantines:** afficher l'info du SIREN de l'unité légale dans l'application ([#5123](https://github.com/betagouv/ma-cantine/issues/5123)) ([6a04707](https://github.com/betagouv/ma-cantine/commit/6a04707106fbcad41ccc9b0d3111c1e7d3bdadc9))
* **Cantines:** gérer le nouveau champ siren_unite_legale dans les TD (juste le nouveau champ) ([#5082](https://github.com/betagouv/ma-cantine/issues/5082)) ([905d992](https://github.com/betagouv/ma-cantine/commit/905d992f3d40eee7b528a5288625deb19c6ed503))
* **Cantines:** permettre aux cantines sans SIRET (mais avec un siren_unite_legale) de TD ([#5122](https://github.com/betagouv/ma-cantine/issues/5122)) ([fd17a05](https://github.com/betagouv/ma-cantine/commit/fd17a05930a64c992062b1fabf049b67b02fa207))


### Corrections (bugs, typos...)

* **Ajouter une cantine:** corrige le comportement des secteurs en ayant un seul sélecteur ([#5121](https://github.com/betagouv/ma-cantine/issues/5121)) ([633613a](https://github.com/betagouv/ma-cantine/commit/633613ae6a422c3d11cae455d3840335aa851aeb))
* **Ajouter une cantine:** l'affichage du ministère de tutelle était calculé sur tous les secteurs et non juste ceux sélectionnés ([#5126](https://github.com/betagouv/ma-cantine/issues/5126)) ([e6ba6d9](https://github.com/betagouv/ma-cantine/commit/e6ba6d9ba08beb9db408b172f27b09526b370c02))

## [2025.9.0](https://github.com/betagouv/ma-cantine/compare/v2025.8.1...v2025.9.0) (2025-03-13)


### Nouveautés

* **Cantines:** nouvel endpoint API pour récupérer les status des cantines par siren (utile pour l'ajout sans SIRET) ([#5108](https://github.com/betagouv/ma-cantine/issues/5108)) ([8f0fb19](https://github.com/betagouv/ma-cantine/commit/8f0fb192257a2d91b0bb3aa60f7fd144de1cda78))


### Améliorations

* **Cantines:** affiche le nouveau champ siren_unite_legale dans l'admin ([#5119](https://github.com/betagouv/ma-cantine/issues/5119)) ([aa452de](https://github.com/betagouv/ma-cantine/commit/aa452def3965a81e8e1a2994222c25f1a94a3906))
* **Cantines:** gérer le nouveau champ siren_unite_legale dans les exports Metabase ([#5083](https://github.com/betagouv/ma-cantine/issues/5083)) ([f1bd2ea](https://github.com/betagouv/ma-cantine/commit/f1bd2eac695a19fab4e78de3029c5596c3de78e7))


### Corrections (bugs, typos...)

* **Ajouter une cantine:** corrige le ministère de tutelle qui ne s'enregistrait pas et homogénéise les variables en lien avec ce champ ([#5113](https://github.com/betagouv/ma-cantine/issues/5113)) ([ed7c285](https://github.com/betagouv/ma-cantine/commit/ed7c285434f93c121412e15fcb109a47f8cd453c))
* **Ajouter une cantine:** début de la gestion des cantines sans SIRET (formulaire de création personnalisé) ([#5117](https://github.com/betagouv/ma-cantine/issues/5117)) ([dc6fb50](https://github.com/betagouv/ma-cantine/commit/dc6fb50834b7317a3814f355a0ba7b071119ddf2))
* **Imports:** Sépare les catégories IME & ESAT (typo) ([#5118](https://github.com/betagouv/ma-cantine/issues/5118)) ([9030138](https://github.com/betagouv/ma-cantine/commit/9030138a56453a6af869ca0dca7b5ca4af1cff3d))

## [2025.8.1](https://github.com/betagouv/ma-cantine/compare/v2025.8.0...v2025.8.1) (2025-03-12)


### Corrections (bugs, typos...)

* **Cantines:** Répare les règles concernant le champ 'Administration de tutelle' au moment de la TD ([#5112](https://github.com/betagouv/ma-cantine/issues/5112)) ([8eab91a](https://github.com/betagouv/ma-cantine/commit/8eab91a3ab453db3a472861e4253471839bb69b8))

## [2025.8.0](https://github.com/betagouv/ma-cantine/compare/v2025.7.1...v2025.8.0) (2025-03-11)


### Nouveautés

* **Cantines:** nouveau champ siren_unite_legale pour commencer à gérer les cantines sans SIRET propre ([#5081](https://github.com/betagouv/ma-cantine/issues/5081)) ([b5c04b4](https://github.com/betagouv/ma-cantine/commit/b5c04b44ee5d6e8d04591a9b3dabb2f755d397df))


### Améliorations

* **Ajouter une cantine:** ajoute des cases à cocher pour confirmer certaines valeurs renseignées ([#5096](https://github.com/betagouv/ma-cantine/issues/5096)) ([331f55a](https://github.com/betagouv/ma-cantine/commit/331f55a956209152822f92a2e78b36bf6ea443a0))
* **Ajouter une cantine:** améliore l'accessibilité, le responsive et quelques correctifs de stylisation ([#5097](https://github.com/betagouv/ma-cantine/issues/5097)) ([d1e98e8](https://github.com/betagouv/ma-cantine/commit/d1e98e8253a9c33b4b11d9fce6bf09d72e4c327f))
* **Ajouter une cantine:** rechercher un SIRET ([#5094](https://github.com/betagouv/ma-cantine/issues/5094)) ([d7e807e](https://github.com/betagouv/ma-cantine/commit/d7e807ead1622cb71c757ee49bba96fb587ab5a8))


### Corrections (bugs, typos...)

* **Ajouter une cantine:** le message d'erreur du SIRET manquant ne s'affichait pas ([#5105](https://github.com/betagouv/ma-cantine/issues/5105)) ([599bbb1](https://github.com/betagouv/ma-cantine/commit/599bbb1704d52eb76176782f91f9cff93e435f21))
* **Ajouter une cantine:** multiples correctifs suite aux tests manuels de la fonctionnalité ([#5102](https://github.com/betagouv/ma-cantine/issues/5102)) ([3a04877](https://github.com/betagouv/ma-cantine/commit/3a04877acc10c09c224e97d602ec24ab4c8323d2))
* **Imports:** Deuxième partie de correction des regex pour rendre les apostrophes plus permissives ([#5103](https://github.com/betagouv/ma-cantine/issues/5103)) ([e9b2d20](https://github.com/betagouv/ma-cantine/commit/e9b2d206be578b8fb584641c4087d15f9bb307e1))
* **Imports:** Rendre la regex plus permissive pour accepter tous les secteurs avec les apostrophes ([#5100](https://github.com/betagouv/ma-cantine/issues/5100)) ([9dcdd97](https://github.com/betagouv/ma-cantine/commit/9dcdd97f007362f2cb2985a0ea2f3514aaa9a31d))
* **Imports:** Troisième partie de correction des regex pour rendre les apostrophes plus permissives ([#5104](https://github.com/betagouv/ma-cantine/issues/5104)) ([6f790b3](https://github.com/betagouv/ma-cantine/commit/6f790b3a73fa59247caa2034f10032b1e4381be0))


### Technique

* **deps:** bump django from 5.0.11 to 5.0.13 ([#5098](https://github.com/betagouv/ma-cantine/issues/5098)) ([352d78c](https://github.com/betagouv/ma-cantine/commit/352d78c4d6e9fcfbab7b61ba295151917629a7b2))
* **Import:** Vérifier que les imports uniformisent les apostrophes ([#5106](https://github.com/betagouv/ma-cantine/issues/5106)) ([31c04b4](https://github.com/betagouv/ma-cantine/commit/31c04b471b3cbc2bd60f52263ccf53b0a9ea200e))
* **Page Développeur:** Migration de la page en Vue 3 ([#5101](https://github.com/betagouv/ma-cantine/issues/5101)) ([a6485e2](https://github.com/betagouv/ma-cantine/commit/a6485e2dc5517b242262549f6ffff86ff6f1b314))
* **TD:** bouger les queryset de stats dans les modèles ([#5095](https://github.com/betagouv/ma-cantine/issues/5095)) ([127867c](https://github.com/betagouv/ma-cantine/commit/127867c9a331ab93023243010692b47c26f7a2b0))

## [2025.7.1](https://github.com/betagouv/ma-cantine/compare/v2025.7.0...v2025.7.1) (2025-03-05)


### Améliorations

* **Ajouter un cantine:** enregistrement de la nouvelle cantine ([#5090](https://github.com/betagouv/ma-cantine/issues/5090)) ([04ed0c2](https://github.com/betagouv/ma-cantine/commit/04ed0c2c927b6c1a14bbb030c1163e3214a12b6e))
* **Ajouter une cantine:** création de la nouvelle page en vue3 ([#5085](https://github.com/betagouv/ma-cantine/issues/5085)) ([1a5afa7](https://github.com/betagouv/ma-cantine/commit/1a5afa774fc569679590529d1427980045ab33c3))
* **Ajouter une cantine:** vérification des champs avant l'envoi du formulaire de création [#5086](https://github.com/betagouv/ma-cantine/issues/5086)  ([#5087](https://github.com/betagouv/ma-cantine/issues/5087)) ([523e104](https://github.com/betagouv/ma-cantine/commit/523e1049b06a6bccf79c3f0eb09bd784bf66f935))
* **Imports:** Cantines: mieux documenter les champs admin (les lister dans le tableau) ([#5064](https://github.com/betagouv/ma-cantine/issues/5064)) ([efec9bb](https://github.com/betagouv/ma-cantine/commit/efec9bba26440d7378c7d81c44b4dfa08313ff0b))


### Corrections (bugs, typos...)

* **Cantines données géo:** Ajout condition supplémentaire en cas d enseignes vides ([#5066](https://github.com/betagouv/ma-cantine/issues/5066)) ([ff052d9](https://github.com/betagouv/ma-cantine/commit/ff052d9d6626970b023cca5f43613939bbc73561))


### Documentation

* **API Stats:** Ajout des filtres dans la documentation ([#5091](https://github.com/betagouv/ma-cantine/issues/5091)) ([bc95447](https://github.com/betagouv/ma-cantine/commit/bc95447cb6d1889d4390bb9837829786636c3478))


### Technique

* **API Stats:** Créer une classe serializer pour l'API stats ([#5084](https://github.com/betagouv/ma-cantine/issues/5084)) ([110a2ad](https://github.com/betagouv/ma-cantine/commit/110a2adf132219cedf7c2120d44d5aad0c4dee25))
* **Cantines:** meilleure gestion des SIRET ([#5080](https://github.com/betagouv/ma-cantine/issues/5080)) ([1fe5fc2](https://github.com/betagouv/ma-cantine/commit/1fe5fc2bb80d2e677bba70f7e720a15b334bbd54))
* **deps-dev:** bump @rushstack/eslint-patch from 1.10.4 to 1.10.5 in /2024-frontend ([#4990](https://github.com/betagouv/ma-cantine/issues/4990)) ([f8c4e19](https://github.com/betagouv/ma-cantine/commit/f8c4e19ba3d8fccb1080dc7066850446776f3b87))
* **deps-dev:** bump eslint from 9.17.0 to 9.21.0 in /2024-frontend ([7f01840](https://github.com/betagouv/ma-cantine/commit/7f018402c88876a79cc3e16cc9c41045f5614f7a))
* **deps:** bump @vueuse/core from 12.0.0 to 12.7.0 in /2024-frontend ([b3928ac](https://github.com/betagouv/ma-cantine/commit/b3928accb472a8078b9cb0757aee720d79c83d78))

## [2025.7.0](https://github.com/betagouv/ma-cantine/compare/v2025.6.2...v2025.7.0) (2025-02-27)


### Nouveautés

* **Cantine données géo:** Remplacer API Insee vers Recherche Entreprises  ([#5048](https://github.com/betagouv/ma-cantine/issues/5048)) ([b59303e](https://github.com/betagouv/ma-cantine/commit/b59303e5de31c0822a2a1c1d9c3e79f0f9038045))

## [2025.6.2](https://github.com/betagouv/ma-cantine/compare/v2025.6.1...v2025.6.2) (2025-02-27)


### Améliorations

* **Affiche en ligne:** affiche par défaut les % des viandes et produits de la mer ([#5056](https://github.com/betagouv/ma-cantine/issues/5056)) ([b6066f8](https://github.com/betagouv/ma-cantine/commit/b6066f8522cd7ede45bf465a0e58d103b43863b6))
* **Badge qualité des produits:** supprime l'objectif sur les viandes et volailles de France qui ne fait pas parti de loi ([#5053](https://github.com/betagouv/ma-cantine/issues/5053)) ([44b0958](https://github.com/betagouv/ma-cantine/commit/44b0958bbe6bb3026cf5e392d395463dafb89af3))
* **Cantines:** Imports: autoriser les admin à modifier des cantines dont ils ne sont pas gestionnaires ([#5052](https://github.com/betagouv/ma-cantine/issues/5052)) ([75aea3e](https://github.com/betagouv/ma-cantine/commit/75aea3e9a6f440dcc6492d6e1545d2179b5ded78))
* **Import de masse:** affiche en rouge les cellules ordre et colonne au clic "voir le format attendu" ([#5061](https://github.com/betagouv/ma-cantine/issues/5061)) ([c2805c2](https://github.com/betagouv/ma-cantine/commit/c2805c22dffcca1c288dbcdc915d9b7827e557d6))
* **Import de masse:** précise le message d'erreur de l'en-tête non conforme ([#5060](https://github.com/betagouv/ma-cantine/issues/5060)) ([63182ff](https://github.com/betagouv/ma-cantine/commit/63182ffe75af8a692ffa90505bfa986d4217ab35))
* **Imports:** Cantines: ajout du champ ministère_tutelle (seulement pour les admins) ([#5050](https://github.com/betagouv/ma-cantine/issues/5050)) ([f3dac84](https://github.com/betagouv/ma-cantine/commit/f3dac849270b6f7bfbb67b610bc01b1d1a5a2336))
* **Imports:** Cantines: mieux gérer les imports admin (schéma dédié, erreurs, tests) ([#5049](https://github.com/betagouv/ma-cantine/issues/5049)) ([6a2dd2d](https://github.com/betagouv/ma-cantine/commit/6a2dd2d064145328c2143d529d64afe7c49a87ca))
* **Imports:** Cantines: suite de l'ajout du champ admin_ministère_tutelle (affichage dans l'interface) ([#5059](https://github.com/betagouv/ma-cantine/issues/5059)) ([1a70140](https://github.com/betagouv/ma-cantine/commit/1a70140651df7fcdd26a9b640fa0398df9b75ee1))


### Corrections (bugs, typos...)

* **Imports:** Cantines: répare le fichier d'exemple admin ([#5062](https://github.com/betagouv/ma-cantine/issues/5062)) ([70ecb5a](https://github.com/betagouv/ma-cantine/commit/70ecb5a77f508f547f31881a08347a6e21acdfad))
* **Tableau de bord:** renomme la section "Ma progression" pour "Mon bilan annuel" ([#5051](https://github.com/betagouv/ma-cantine/issues/5051)) ([bfe4f2f](https://github.com/betagouv/ma-cantine/commit/bfe4f2fab924851514b3d5b6f9a95b8c7ea04376))


### Technique

* **Imports:** simplifier un peu le code de récupération des headers à partir des schémas (achats, cantines, bilans) ([#5054](https://github.com/betagouv/ma-cantine/issues/5054)) ([e25a7fb](https://github.com/betagouv/ma-cantine/commit/e25a7fb05a50509cade7a0ea59defec754881e25))
* **Review apps:** Les désactiver en attendant qu'on prenne le temps de les faire fonctionner ([#5057](https://github.com/betagouv/ma-cantine/issues/5057)) ([b09965d](https://github.com/betagouv/ma-cantine/commit/b09965d3158cfd892b4e76463cdbab0ae2db996d))

## [2025.6.1](https://github.com/betagouv/ma-cantine/compare/v2025.6.0...v2025.6.1) (2025-02-25)


### Améliorations

* **Imports:** Cantines: rajoute une contrainte d'unicité sur le champ SIRET ([#5039](https://github.com/betagouv/ma-cantine/issues/5039)) ([0cc9efd](https://github.com/betagouv/ma-cantine/commit/0cc9efd564c63aea3dae9685de1320cdbb05ed96))
* **Validata:** Change l'url pour celle de prod ([#5036](https://github.com/betagouv/ma-cantine/issues/5036)) ([697eda9](https://github.com/betagouv/ma-cantine/commit/697eda93c0188ec97be7b57f69908d19654b6dbb))
* **Validata:** Message d'erreur spécifique pour indiquer que le fichier contient des lignes vides ([#5042](https://github.com/betagouv/ma-cantine/issues/5042)) ([5083b6c](https://github.com/betagouv/ma-cantine/commit/5083b6cdb723a3e9cb8c1533bef7aa3b61d631ea))


### Corrections (bugs, typos...)

* **Imports:** Cantines: corrige le lien vers le schéma ([#5043](https://github.com/betagouv/ma-cantine/issues/5043)) ([98ee42e](https://github.com/betagouv/ma-cantine/commit/98ee42e6621f25822ac38e8c1029e7e41137b894))
* **Imports:** Cantines: quelques corrections sur l'encart admin ([#5045](https://github.com/betagouv/ma-cantine/issues/5045)) ([f62dc68](https://github.com/betagouv/ma-cantine/commit/f62dc684b936b67cd1825132c88d84c3bc019bbe))
* **Imports:** Cantines: répare les tests suite à la correction du lien vers le schéma ([#5044](https://github.com/betagouv/ma-cantine/issues/5044)) ([18689c1](https://github.com/betagouv/ma-cantine/commit/18689c15e2c17b1560f430a3e77097795acb0b12))


### Technique

* **Imports:** Achats: améliore les tests ([#5037](https://github.com/betagouv/ma-cantine/issues/5037)) ([fbfd3c1](https://github.com/betagouv/ma-cantine/commit/fbfd3c1dc023171e9675e6adc2b9bd484bfe52ad))
* **Imports:** Cantines: améliorer les tests ([#5038](https://github.com/betagouv/ma-cantine/issues/5038)) ([fe15321](https://github.com/betagouv/ma-cantine/commit/fe15321b35c4d633d386493565ab1fcdc475ed57))
* **Imports:** Regroupe tous les tests dans les mêmes fichiers ([#5046](https://github.com/betagouv/ma-cantine/issues/5046)) ([604a890](https://github.com/betagouv/ma-cantine/commit/604a8901bbbaf41e7449abbc392ebd77f9b3f28c))

## [2025.6.0](https://github.com/betagouv/ma-cantine/compare/v2025.5.0...v2025.6.0) (2025-02-17)


### Nouveautés

* **Import de masse:** Cantines: remplace l'ancienne page pour la nouvelle ([#5028](https://github.com/betagouv/ma-cantine/issues/5028)) ([ef1eef8](https://github.com/betagouv/ma-cantine/commit/ef1eef87ddb488b19cbc03b9dbe1436f24f3b508))
* **Imports:** Cantines: ajout d'appels à Validata et renvoyer les erreurs ([#5034](https://github.com/betagouv/ma-cantine/issues/5034)) ([e4d70cf](https://github.com/betagouv/ma-cantine/commit/e4d70cf6b6356f25e662f1bb5837fa0b36152f5f))
* **Tableau de bord:** Rend le numéro SIRET de la cantine plus visible  ([#5032](https://github.com/betagouv/ma-cantine/issues/5032)) ([5fa7574](https://github.com/betagouv/ma-cantine/commit/5fa7574ec862219420713a40727b9902dd5d82c9))
* **Validata:** Cantines : Rendre le schéma de données compatible TableSchema ([#5016](https://github.com/betagouv/ma-cantine/issues/5016)) ([d54ea41](https://github.com/betagouv/ma-cantine/commit/d54ea4164224888dee73b363ea362e37670d334c))


### Améliorations

* **Imports:** Cantines: remonte le check du header plus haut (comme les achats) ([#5033](https://github.com/betagouv/ma-cantine/issues/5033)) ([5555010](https://github.com/betagouv/ma-cantine/commit/555501069d88912bf3a4fd3260e7ded765753958))
* **Imports:** Cantines: séparer dans le backend les imports cantines des imports diagnostics ([#5031](https://github.com/betagouv/ma-cantine/issues/5031)) ([7b463c6](https://github.com/betagouv/ma-cantine/commit/7b463c65f336f75cd654e2cfc9248e6e1f3e3b89))
* **Validata:** Montée de version de l'API v0.12. Correction des changements cassant. ([#5035](https://github.com/betagouv/ma-cantine/issues/5035)) ([2b0ba9f](https://github.com/betagouv/ma-cantine/commit/2b0ba9f2b78052dff3c95c72a9ca3b5adc26a0b8))


### Corrections (bugs, typos...)

* **Imports:** Changement de l'url du schema import cantine ([#5030](https://github.com/betagouv/ma-cantine/issues/5030)) ([982e3d2](https://github.com/betagouv/ma-cantine/commit/982e3d26611b284f484d50f5a00bf660d2510519))

## [2025.5.0](https://github.com/betagouv/ma-cantine/compare/v2025.4.1...v2025.5.0) (2025-02-12)


### Nouveautés

* **Validata:** Import achats: ajout d'appels à Validata et renvoyer les erreurs ([#4949](https://github.com/betagouv/ma-cantine/issues/4949)) ([2c58007](https://github.com/betagouv/ma-cantine/commit/2c5800782f7eb47e4c25f2ac4c239755aa4817ed))


### Améliorations

* **Imports:** Ajoute une colonne Ordre (A, B...) dans la doc du schéma ([#5025](https://github.com/betagouv/ma-cantine/issues/5025)) ([0b25f03](https://github.com/betagouv/ma-cantine/commit/0b25f037d2b0b4146b46b9ae9db38ded5806a94e))


### Technique

* **Imports achats:** ajouter un lien vers la doc au-dessus ([#5021](https://github.com/betagouv/ma-cantine/issues/5021)) ([b52d79a](https://github.com/betagouv/ma-cantine/commit/b52d79ad6502221aedda3027933bbaf46a45d9ba))
* **Imports achats:** regrouper les erreurs par colonne ([#5020](https://github.com/betagouv/ma-cantine/issues/5020)) ([c10930b](https://github.com/betagouv/ma-cantine/commit/c10930be5d4aa9c3b782b6059a468cd2d7caf1a5))
* **Imports de masse:** Achats: renvoyer toutes les erreurs (c'était limité au 30 premières) ([#5018](https://github.com/betagouv/ma-cantine/issues/5018)) ([3051548](https://github.com/betagouv/ma-cantine/commit/30515482793f74f01b21bbc99d6fe61ebe1a8f37))
* **Imports:** clarifie le message d'erreur venant du header ([#5024](https://github.com/betagouv/ma-cantine/issues/5024)) ([c67888f](https://github.com/betagouv/ma-cantine/commit/c67888fae5f879999d402ff6dc5561084d1b9b5c))
* **Pre commit:** mise à jour de la version utilisée par flake8 et correction de quelques fichiers ([#5022](https://github.com/betagouv/ma-cantine/issues/5022)) ([3623fd9](https://github.com/betagouv/ma-cantine/commit/3623fd9422994179e0ee3b138bfe16e8cfcd20db))
* **Validata:** Imports achats: petits ajustements pour commencer à afficher les erreurs renvoyées par Validata ([#5009](https://github.com/betagouv/ma-cantine/issues/5009)) ([a15fe17](https://github.com/betagouv/ma-cantine/commit/a15fe17a6a4ebc6e236efd87932a2d90358fb8a1))

## [2025.4.1](https://github.com/betagouv/ma-cantine/compare/v2025.4.0...v2025.4.1) (2025-02-11)


### Corrections (bugs, typos...)

* **Import de masse:** autorise le format de fichier utilisé par window pour les fichier csv ([#5012](https://github.com/betagouv/ma-cantine/issues/5012)) ([d75e6bc](https://github.com/betagouv/ma-cantine/commit/d75e6bc0b704ce4ceb5e476e7d91dc807734cd2d))
* **Import de masse:** restreint l'import aux fichiers .csv et .tsv uniquement ([#5011](https://github.com/betagouv/ma-cantine/issues/5011)) ([fd616e2](https://github.com/betagouv/ma-cantine/commit/fd616e20a221fa81aa12c7a363e0fdf04adefa85))
* **Télédéclaration:** afficher le bouton de remplissage rapide de l'approvisionnement seulement si le total des achats est supérieur à zéro ([#5008](https://github.com/betagouv/ma-cantine/issues/5008)) ([c8be596](https://github.com/betagouv/ma-cantine/commit/c8be59644bbae6f1eb2aaa87525a7b75f2150e64))


### Technique

* **Open data:** lancer les exports plus tôt (à 3AM au lieu de 10AM) ([#5014](https://github.com/betagouv/ma-cantine/issues/5014)) ([53b285b](https://github.com/betagouv/ma-cantine/commit/53b285b0a79240cb0bd0c8769c23a779cfcd80e3))

## [2025.4.0](https://github.com/betagouv/ma-cantine/compare/v2025.3.2...v2025.4.0) (2025-02-10)


### Nouveautés

* **Import de masse:** Cantines: Migration vue3 et redesign de la page ([#4975](https://github.com/betagouv/ma-cantine/issues/4975)) ([91d6110](https://github.com/betagouv/ma-cantine/commit/91d61102b1ecd17956f7d60d8fe01e04b937bc5c))
* **Open-Data:** Ajout colonne participation campagne TD 2024 en cours sur le registre des cantines ([#5006](https://github.com/betagouv/ma-cantine/issues/5006)) ([da4ac60](https://github.com/betagouv/ma-cantine/commit/da4ac601f184fc5face58abda0b6130ff5a0f4cd))


### Améliorations

* **Import de masse:** Cantines: Renomme les fichiers d'exemple ([#5007](https://github.com/betagouv/ma-cantine/issues/5007)) ([52565b6](https://github.com/betagouv/ma-cantine/commit/52565b6f43f5fa9d958026e6cda26b212d8d37b0))


### Corrections (bugs, typos...)

* **Import de masse:** les schémas ne s'affichent pas ([#5005](https://github.com/betagouv/ma-cantine/issues/5005)) ([3f3c463](https://github.com/betagouv/ma-cantine/commit/3f3c46370b468f6ccf38d7d8b07fd4b94e652a01))
* **Imports:** Remplacer ancien secteur "Secondaire lycée agricole" par "Etablissements d’enseignement agricole" ([#4999](https://github.com/betagouv/ma-cantine/issues/4999)) ([37c4a0c](https://github.com/betagouv/ma-cantine/commit/37c4a0c7f6c0932552bbc71a5e108a62e87a6ffc))
* **Tunnel gaspillage:** Les erreurs ne s'effaçaient pas ([#4998](https://github.com/betagouv/ma-cantine/issues/4998)) ([5c6e8c3](https://github.com/betagouv/ma-cantine/commit/5c6e8c315d7c5985e58b8bb612107fe031d47950))


### Documentation

* **Celery:** Documenter séparation celery et app web ([#4993](https://github.com/betagouv/ma-cantine/issues/4993)) ([0225e7e](https://github.com/betagouv/ma-cantine/commit/0225e7e9add7c7c136672b90e6559e851b58a3ff))


### Technique

* **API:** Imports: Achats: séparer le check sur la présence du header ([#4997](https://github.com/betagouv/ma-cantine/issues/4997)) ([a782b1a](https://github.com/betagouv/ma-cantine/commit/a782b1a8ac915983ff5caf161e746df0512130cb))
* **CleverCloud:** ajoute le mode verbose pour debugger ([#5002](https://github.com/betagouv/ma-cantine/issues/5002)) ([957ba8f](https://github.com/betagouv/ma-cantine/commit/957ba8fa17f319812d19218497c8e8fd0aeb6577))
* **CleverCloud:** Efface fichier le déploiement pour le remplacer par des variables d'env ([#4978](https://github.com/betagouv/ma-cantine/issues/4978)) ([782bebf](https://github.com/betagouv/ma-cantine/commit/782bebf8062284e87fab2f4d8afa711a711d8358))
* **deps:** bump jsonschema-specifications from 2023.12.1 to 2024.10.1 ([#4984](https://github.com/betagouv/ma-cantine/issues/4984)) ([4cc007f](https://github.com/betagouv/ma-cantine/commit/4cc007fa218c3be51435fcc96a1d97144c46b40f))
* **Validata:** Achats: Modifie le schéma pour accepter des decimal avec virgule ([#5001](https://github.com/betagouv/ma-cantine/issues/5001)) ([db77dc9](https://github.com/betagouv/ma-cantine/commit/db77dc95ed987aaf1bd51d1f267dd247085ac2b6))
* **Validata:** Achats: Modifie le schéma pour accepter des espaces dans les champs enum ([#4973](https://github.com/betagouv/ma-cantine/issues/4973)) ([5ac8e3c](https://github.com/betagouv/ma-cantine/commit/5ac8e3c39aad64bab63b408211e263bd626c37c3))
* **Validata:** Achats: Re-modifie le schéma pour accepter des decimal avec virgule (et sans limites de chiffres après la virgule) ([#5004](https://github.com/betagouv/ma-cantine/issues/5004)) ([b83e207](https://github.com/betagouv/ma-cantine/commit/b83e2070f1bd5c10d37b5a8fbdab8411cda4bd61))
* **Vue3:** Change l'organisation du code des views et du router ([#5003](https://github.com/betagouv/ma-cantine/issues/5003)) ([ecf1eb5](https://github.com/betagouv/ma-cantine/commit/ecf1eb5b73bdfdf2405823d41c53a5a34916be52))

## [2025.3.2](https://github.com/betagouv/ma-cantine/compare/v2025.3.1...v2025.3.2) (2025-01-29)


### Améliorations

* **Statistiques territoire:** Indiquer l'année de télédéclaration ([#4966](https://github.com/betagouv/ma-cantine/issues/4966)) ([436b7ba](https://github.com/betagouv/ma-cantine/commit/436b7bab36bc6c8b4af91b4a5e24643a4c8677ca))
* **Statistiques territoire:** Mettre un message pour l'année en cours (2024) et cacher certains chiffres ([#4968](https://github.com/betagouv/ma-cantine/issues/4968)) ([8b172e0](https://github.com/betagouv/ma-cantine/commit/8b172e0bf61f3a897487b99c5737769d13ba5ab6))


### Corrections (bugs, typos...)

* **Télédéclaration:** Gaspillage alimentaire: affiche les mesures du nouveau tunnel dans la télédéclaration ([#4965](https://github.com/betagouv/ma-cantine/issues/4965)) ([0097bd4](https://github.com/betagouv/ma-cantine/commit/0097bd4e2b5ce2a54908fc103a2d5c9b49914145))
* **Télédéclaration:** Gaspillage alimentaire: désactive temporairement le remplissage automatique ([#4967](https://github.com/betagouv/ma-cantine/issues/4967)) ([de15b94](https://github.com/betagouv/ma-cantine/commit/de15b942bcac2161ed96b66814ece9e286813f9e))


### Technique

* **API:** Imports: nouvelle librairie de gestion des imports (qui check le format, la taille max, et si déjà uploadé) ([#4936](https://github.com/betagouv/ma-cantine/issues/4936)) ([7fa3b00](https://github.com/betagouv/ma-cantine/commit/7fa3b00d75c4877a2b98dbdb58704974fc9caad9))
* **common:** centraliser la logique API Adresse dans un nouveau fichier api/adresse.py ([#4963](https://github.com/betagouv/ma-cantine/issues/4963)) ([dc04f52](https://github.com/betagouv/ma-cantine/commit/dc04f5272579d8c82b5574a943f61a045788e9af))
* **common:** centraliser la logique API Insee dans un nouveau fichier api/insee.py ([#4962](https://github.com/betagouv/ma-cantine/issues/4962)) ([aab167f](https://github.com/betagouv/ma-cantine/commit/aab167f3043221fd425115305276aa69ec75e291))
* **common:** nouveau fichier utils/siret.py ([#4961](https://github.com/betagouv/ma-cantine/issues/4961)) ([387a8cc](https://github.com/betagouv/ma-cantine/commit/387a8cc68a65274f9324cec53c4faf54a6cbe6d8))
* **deps-dev:** bump vite from 5.4.11 to 5.4.14 in /2024-frontend ([#4938](https://github.com/betagouv/ma-cantine/issues/4938)) ([c4af8cc](https://github.com/betagouv/ma-cantine/commit/c4af8cc4bcf73801dac46ca890a52b232905d3fe))

## [2025.3.1](https://github.com/betagouv/ma-cantine/compare/v2025.3.0...v2025.3.1) (2025-01-28)


### Améliorations

* **Statistiques territoire:** cacher les chiffres en bas en attendant d'améliorer les requêtes backend ([#4957](https://github.com/betagouv/ma-cantine/issues/4957)) ([40f9f5d](https://github.com/betagouv/ma-cantine/commit/40f9f5d5beb4c129e928c0fe17e2d200e496c73e))
* **Statistiques territoire:** étoffer les stats dans la section EGalim. clean du CSS ([#4958](https://github.com/betagouv/ma-cantine/issues/4958)) ([ff0e298](https://github.com/betagouv/ma-cantine/commit/ff0e298bf0f2b9a0cc32345e74df9ce5658cabec))
* **Statistiques territoire:** modification du titre de la page et du breadcrumb ([#4954](https://github.com/betagouv/ma-cantine/issues/4954)) ([d56c319](https://github.com/betagouv/ma-cantine/commit/d56c319bd8f8fdde0990d1943dada9e135855735))
* **Statistiques territoire:** réorganisation du contenu (renommage de sous-titre, nouvelle card, clarifications) ([#4955](https://github.com/betagouv/ma-cantine/issues/4955)) ([1cc0e3f](https://github.com/betagouv/ma-cantine/commit/1cc0e3fb4b612024cb39a98dd92b3863997f6d99))


### Corrections (bugs, typos...)

* **Imports de masse:** Renomme un secteur ([#4951](https://github.com/betagouv/ma-cantine/issues/4951)) ([d96408e](https://github.com/betagouv/ma-cantine/commit/d96408e0b31075df09e61fd9caa61fc78c18f4ea))
* **Télédéclaration:** supprime la pré-sélection du mode de saisie de la télédéclaration qui ne s'enregistrait pas ([#4952](https://github.com/betagouv/ma-cantine/issues/4952)) ([a8d8a08](https://github.com/betagouv/ma-cantine/commit/a8d8a08d50339e3964ca9f7de8f8e2c3de339f1f))


### Technique

* **API:** Filters: basculer dans un fichier utils.py dédié ([#4934](https://github.com/betagouv/ma-cantine/issues/4934)) ([3cc558e](https://github.com/betagouv/ma-cantine/commit/3cc558e245e0e64e7b3d97e6f861d90bad09192f))
* **deps:** bump @gouvfr/dsfr from 1.12.1 to 1.13.0 in /2024-frontend ([#4821](https://github.com/betagouv/ma-cantine/issues/4821)) ([d94c498](https://github.com/betagouv/ma-cantine/commit/d94c49825e2c7342c0a79b569e1ceb0a0282dbdb))
* **deps:** bump @gouvminint/vue-dsfr from 7.1.0 to 7.2.0 in /2024-frontend ([#4820](https://github.com/betagouv/ma-cantine/issues/4820)) ([92947ae](https://github.com/betagouv/ma-cantine/commit/92947aed3b3956c2dd7279a28c644d54bde0e88a))
* **deps:** bump nanoid from 3.3.7 to 3.3.8 in /frontend ([#4920](https://github.com/betagouv/ma-cantine/issues/4920)) ([92bb06d](https://github.com/betagouv/ma-cantine/commit/92bb06d06f42fd84db31d4d756d17c7f1a551b78))
* **deps:** bump vue-i18n from 10.0.5 to 11.0.1 in /2024-frontend ([#4822](https://github.com/betagouv/ma-cantine/issues/4822)) ([30b1879](https://github.com/betagouv/ma-cantine/commit/30b187940d8e540932c9a858f3135060591a4a09))

## [2025.3.0](https://github.com/betagouv/ma-cantine/compare/v2025.2.0...v2025.3.0) (2025-01-24)


### Nouveautés

* **Import de masse:** Achats: Migration vue3 et redesign de la page ([#4923](https://github.com/betagouv/ma-cantine/issues/4923)) ([cfaaa71](https://github.com/betagouv/ma-cantine/commit/cfaaa71e5fee5eb72779f9504e94a2ce56017f91))
* **Imports de masse:** Achats: remplace l'ancienne page pour la nouvelle ([#4946](https://github.com/betagouv/ma-cantine/issues/4946)) ([d088735](https://github.com/betagouv/ma-cantine/commit/d08873570f36d4fded815fc8d5a7d8abaa8cdfdb))
* **Validata:** Achats: Rendre le schéma de données compatible TableSchema ([#4889](https://github.com/betagouv/ma-cantine/issues/4889)) ([5a8a134](https://github.com/betagouv/ma-cantine/commit/5a8a1347634ac057ce9d22beac1a5bc7e2cb4a2f))


### Améliorations

* **Imports de masse:** Achats: utiliser le nouveau schema amélioré pour l'affichage de la doc aux utilisateurs ([#4926](https://github.com/betagouv/ma-cantine/issues/4926)) ([4ea7b28](https://github.com/betagouv/ma-cantine/commit/4ea7b2811c9b462671304ae1f26101b487526deb))


### Corrections (bugs, typos...)

* **ETL:** Corriger l'appel à la tâche Celery d'export + modifie la fréquence à journalier (sauf weekend) ([#4929](https://github.com/betagouv/ma-cantine/issues/4929)) ([3b01a3f](https://github.com/betagouv/ma-cantine/commit/3b01a3fa932f92f2fa58a62c703cb7d93791b823))
* **ETL:** Les départements et régions vides sont mal gérés ([#4935](https://github.com/betagouv/ma-cantine/issues/4935)) ([fe3793c](https://github.com/betagouv/ma-cantine/commit/fe3793cc61adb9fe78d2a342570d6a0224e6b31c))
* **Import de Masse:** Achats: différents correctifs suite au test de la nouvelle page ([#4942](https://github.com/betagouv/ma-cantine/issues/4942)) ([69b3ced](https://github.com/betagouv/ma-cantine/commit/69b3ced007350c1964f8abf410fe73b9a319dfc2))
* **Imports de masse:** Achats: enlève temporairement le picto svg (souci de build vue 3) ([#4930](https://github.com/betagouv/ma-cantine/issues/4930)) ([4002a33](https://github.com/betagouv/ma-cantine/commit/4002a33d9675ac39cf0163ec963c94242ab14776))


### Technique

* **deps:** bump virtualenv from 20.26.5 to 20.26.6 ([#4919](https://github.com/betagouv/ma-cantine/issues/4919)) ([2279c43](https://github.com/betagouv/ma-cantine/commit/2279c436fbef423f969792253d6a67d6f9679090))
* **ETL:** Précharger les champs Many To Many [#4931](https://github.com/betagouv/ma-cantine/issues/4931) ([#4932](https://github.com/betagouv/ma-cantine/issues/4932)) ([eec3c62](https://github.com/betagouv/ma-cantine/commit/eec3c6283d8aab9ebae98ff1d122e3eb0e8bc064))
* **Review apps:** création d'un hook dédié pour le prebuild ([#4945](https://github.com/betagouv/ma-cantine/issues/4945)) ([45b2c5d](https://github.com/betagouv/ma-cantine/commit/45b2c5dd49059df5b43f6320a768edaf4d4cc9ce))
* **Review apps:** spécifie la version de python ([#4950](https://github.com/betagouv/ma-cantine/issues/4950)) ([526be60](https://github.com/betagouv/ma-cantine/commit/526be60f9faefb3829ab0c4df428c98ae4ceb19b))
* **Tunnel gaspillage:** Simplification et homogénéisation des règles sur le début et la fin ([#4941](https://github.com/betagouv/ma-cantine/issues/4941)) ([9da5256](https://github.com/betagouv/ma-cantine/commit/9da52562c4456ccb4aa92b9e740dc452e80ab3e4))

## [2025.2.0](https://github.com/betagouv/ma-cantine/compare/v2025.1.0...v2025.2.0) (2025-01-17)


### Nouveautés

* **Metabase:** Ajout champ email ([#4925](https://github.com/betagouv/ma-cantine/issues/4925)) ([36ba9f7](https://github.com/betagouv/ma-cantine/commit/36ba9f7792fd3feae7752ba1b9597170eae44b55))
* **Metabase:** Ajout du champ code commune INSEE dans le modèle TD ([#4880](https://github.com/betagouv/ma-cantine/issues/4880)) ([4469e74](https://github.com/betagouv/ma-cantine/commit/4469e7438d853cbbbae0780e6b81bca01657f4fc))


### Améliorations

* **Cantines:** Card : afficher le badge 'Non-télédéclarée' en rouge ([#4902](https://github.com/betagouv/ma-cantine/issues/4902)) ([ee09a82](https://github.com/betagouv/ma-cantine/commit/ee09a82063552280051c0d8b29232924a01e6ca6))
* **Cantines:** Card : cacher le badge 'Publiée' ([#4901](https://github.com/betagouv/ma-cantine/issues/4901)) ([7c75af9](https://github.com/betagouv/ma-cantine/commit/7c75af92c57bf8e721eb81dd03807bd44171bed0))


### Documentation

* **Docker:** Création d'une doc dédiée ([#4922](https://github.com/betagouv/ma-cantine/issues/4922)) ([8c02d0d](https://github.com/betagouv/ma-cantine/commit/8c02d0dd9264762ad9e71fb2f8775879647a58e3))


### Technique

* **Cantines:** Serializer : remplace PublicationStatusMixin par une property sur le modèle ([#4900](https://github.com/betagouv/ma-cantine/issues/4900)) ([3050dcf](https://github.com/betagouv/ma-cantine/commit/3050dcf24e96f7e711c7bc5487ebfda87c10c1d1))
* **deps:** bump django from 5.0.8 to 5.0.11 ([#4904](https://github.com/betagouv/ma-cantine/issues/4904)) ([98cc4d8](https://github.com/betagouv/ma-cantine/commit/98cc4d8e39d98ddf6a781fca92c3b20a33cd0eda))
* **ETL:** Déplacer et renommer les schémas pour les exports ([#4913](https://github.com/betagouv/ma-cantine/issues/4913)) ([7436ee5](https://github.com/betagouv/ma-cantine/commit/7436ee54b02e684df29304d52e43790e200bbed8))
* **ETL:** Utilser QuerySet et Serializer pour publier les cantines dans Metabase ([#4884](https://github.com/betagouv/ma-cantine/issues/4884)) ([fe674ff](https://github.com/betagouv/ma-cantine/commit/fe674ff8df71992a619a020c7e34e28757a398d8))
* **Imports de masse:** Achats: renomme les fichiers de tests ([#4914](https://github.com/betagouv/ma-cantine/issues/4914)) ([3e42f1e](https://github.com/betagouv/ma-cantine/commit/3e42f1e986d3db9f06a18d69b316328b08d34397))
* **Imports de masse:** Cantines: renomme les fichiers de tests ([#4918](https://github.com/betagouv/ma-cantine/issues/4918)) ([bcab6d3](https://github.com/betagouv/ma-cantine/commit/bcab6d37ac59f46e0b54d3ae2e0b8f3c2c66f94e))
* **Imports de masse:** Diagnostics: renomme les fichiers de tests ([#4916](https://github.com/betagouv/ma-cantine/issues/4916)) ([4ab3cff](https://github.com/betagouv/ma-cantine/commit/4ab3cff30681095218ce0a0ea9c178340bee4929))

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
