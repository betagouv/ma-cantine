# Journal des modifications

Ressources :
- [CHANGELOG recommendations](https://keepachangelog.com/)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [release-please](https://github.com/google-github-actions/release-please-action) (automated releases)
- [Semantic Versioning](https://semver.org/) & [Calendar Versioning](https://calver.org/)

## [2026.10.0](https://github.com/betagouv/ma-cantine/compare/v2026.9.0...v2026.10.0) (2026-02-03)


### Nouveautés

* **Ressource:** mise à jour antisèche et kit du télédéclarant ([#6346](https://github.com/betagouv/ma-cantine/issues/6346)) ([852ec2a](https://github.com/betagouv/ma-cantine/commit/852ec2a46977b5431f760f4ad095f9ad2e4301a0))

## [2026.9.0](https://github.com/betagouv/ma-cantine/compare/v2026.8.0...v2026.9.0) (2026-02-02)


### Nouveautés

* **Cantines:** ajoute une règle métier sur le ministère de tutelle ([#6319](https://github.com/betagouv/ma-cantine/issues/6319)) ([40e1514](https://github.com/betagouv/ma-cantine/commit/40e151426df61eef20439f56f65328cbd94598e5))
* **Imports:** Cantines: déplace la colonne "Administration de tutelle" dans l'import commun ([#6318](https://github.com/betagouv/ma-cantine/issues/6318)) ([756b73b](https://github.com/betagouv/ma-cantine/commit/756b73b5b504f2d11b5f21cfc661abe7c9373195))
* **Imports:** remplace les fichiers d'exemples CSV par les Excel ([#6323](https://github.com/betagouv/ma-cantine/issues/6323)) ([d418998](https://github.com/betagouv/ma-cantine/commit/d4189986c812a22fd2826bd940ec2c183a4c8cc5))


### Améliorations

* **Achats:** Caractéristiques: améliorer le wording pour 'performance' & 'externalités' ([#6342](https://github.com/betagouv/ma-cantine/issues/6342)) ([7d9b78c](https://github.com/betagouv/ma-cantine/commit/7d9b78c6cdf35d53136248627e588720f9c2accc))
* **Metabase:** Télédéclarations: exporter aussi la version de la TD ([#6317](https://github.com/betagouv/ma-cantine/issues/6317)) ([eb2eab0](https://github.com/betagouv/ma-cantine/commit/eb2eab04b0f5c1f656c01ae9b25fdc7bae4a2395))
* **Metabase:** Télédéclarations: ordonner par teledeclaration_date ([#6315](https://github.com/betagouv/ma-cantine/issues/6315)) ([2b2ed41](https://github.com/betagouv/ma-cantine/commit/2b2ed41d05f549b3ec94f5a42a4082803ce027cd))
* **Metabase:** Télédéclarations: utiliser les city_insee_code, department & region du satellite [1TD1Site] ([#6325](https://github.com/betagouv/ma-cantine/issues/6325)) ([8e76975](https://github.com/betagouv/ma-cantine/commit/8e769756ddffe2cd74f661cf84a0140a785f7018))
* **Metabase:** Télédéclarations: utiliser les sector_list du satellite [1TD1Site] ([#6324](https://github.com/betagouv/ma-cantine/issues/6324)) ([1175eba](https://github.com/betagouv/ma-cantine/commit/1175eba58a9dc7c4f799aadf4f7e329abee6f972))
* **Open Data:** Télédéclaration: avoir une seule colonne id (enlever le doublon teledeclaration_id) ([#6316](https://github.com/betagouv/ma-cantine/issues/6316)) ([49658e6](https://github.com/betagouv/ma-cantine/commit/49658e60dbaeab8f972f6537701f0753fccd42bb))


### Corrections (bugs, typos...)

* **ETL:** Simplifie les exports secteur & catégorie (et répare l'export Metabase) ([#6321](https://github.com/betagouv/ma-cantine/issues/6321)) ([7be0526](https://github.com/betagouv/ma-cantine/commit/7be052601e808df049e9881e0eaa490bb08514f7))


### Technique

* **Cantines:** nouvelle property has_missing_geo_data pour détecter si elle a des champs géo manquants ([#6303](https://github.com/betagouv/ma-cantine/issues/6303)) ([77ead7e](https://github.com/betagouv/ma-cantine/commit/77ead7e9a01a0ab22ed546a9ce4227f215ddd497))
* **Données Géo:** améliorer les mocks pour les tests ([#6304](https://github.com/betagouv/ma-cantine/issues/6304)) ([4616a01](https://github.com/betagouv/ma-cantine/commit/4616a01399642cd3b063f1142b9df55ef532b323))
* **ETL:** Télédéclaration: bouge les views dédié aux exports dans le fichier séparé ([#6314](https://github.com/betagouv/ma-cantine/issues/6314)) ([558fee9](https://github.com/betagouv/ma-cantine/commit/558fee9e47a0151e40ce658c6325e504d18707da))
* **ETL:** Télédéclarations: homogénéiser les tests entre Metabase et Open Data ([#6308](https://github.com/betagouv/ma-cantine/issues/6308)) ([ef99178](https://github.com/betagouv/ma-cantine/commit/ef9917854f05f6e26ca1c32c232ff7e8b0c67e4c))
* **Secteurs:** utils pour mieux jongler avec les verbose_name et les lib ([#6320](https://github.com/betagouv/ma-cantine/issues/6320)) ([c28fec8](https://github.com/betagouv/ma-cantine/commit/c28fec8862d2a2d960cc11d92a40c700a00ae7d8))

## [2026.8.0](https://github.com/betagouv/ma-cantine/compare/v2026.7.0...v2026.8.0) (2026-01-29)


### Nouveautés

* **Bandeau:** Ajoute le bandeau d'alerte pour le rappel des laits infantiles ([#6312](https://github.com/betagouv/ma-cantine/issues/6312)) ([e5748aa](https://github.com/betagouv/ma-cantine/commit/e5748aae3b73524ae94a315bf59278af787716e8))
* **Cantines:** supprime le champ déclaratif "satellite_canteens_count" ([#6299](https://github.com/betagouv/ma-cantine/issues/6299)) ([5b9f026](https://github.com/betagouv/ma-cantine/commit/5b9f026742b02454ab9fe0908b7dc99f07ece721))
* **Imports:** Achats: ajoute une ressource pour retrouver l'ID de sa cantine ([#6300](https://github.com/betagouv/ma-cantine/issues/6300)) ([61707c8](https://github.com/betagouv/ma-cantine/commit/61707c8a9d5f101293b9357c170afe538301f520))
* **Ressources:** ajout du kit du teledeclarant ([#6309](https://github.com/betagouv/ma-cantine/issues/6309)) ([4fa5167](https://github.com/betagouv/ma-cantine/commit/4fa5167c5e5bf05d1dc547fe75c4df88aeedf453))


### Améliorations

* **Metabase:** Cantines: ajouter le champ 'groupe_id' dans les exports ([#6306](https://github.com/betagouv/ma-cantine/issues/6306)) ([fe930bb](https://github.com/betagouv/ma-cantine/commit/fe930bbdf762e0e43142441a065d20dfe642776a))
* **Open Data:** Cantines: lors de l'export, ne plus aller chercher les données géo, on les a déjà en DB ([#6307](https://github.com/betagouv/ma-cantine/issues/6307)) ([6d61ae1](https://github.com/betagouv/ma-cantine/commit/6d61ae1da64db37dd0d18cf8ae645930c95683be))


### Technique

* **ETL:** Cantines: homogénéiser les tests entre Metabase et Open Data ([#6305](https://github.com/betagouv/ma-cantine/issues/6305)) ([8e2b4c5](https://github.com/betagouv/ma-cantine/commit/8e2b4c519837a19f5e9e808e057205e1f2399274))

## [2026.7.0](https://github.com/betagouv/ma-cantine/compare/v2026.6.0...v2026.7.0) (2026-01-28)


### Nouveautés

* **Cantines:** récupérer les données géo en temps réel (au lieu d'attendre 1h puis le lendemain) ([#6266](https://github.com/betagouv/ma-cantine/issues/6266)) ([c36e4e9](https://github.com/betagouv/ma-cantine/commit/c36e4e9e902321eb375b66c621c203a7d14ebb5f))
* **Imports:** Achats: permettre d'importer des achats via le numéro ID de la cantine ([#6293](https://github.com/betagouv/ma-cantine/issues/6293)) ([303de4f](https://github.com/betagouv/ma-cantine/commit/303de4f0d0bb7536478786576aa6ade1df913879))
* **Imports:** améliore la page tampon avant d'ajouter les nouveaux imports via ID ([#6287](https://github.com/betagouv/ma-cantine/issues/6287)) ([b5305ae](https://github.com/betagouv/ma-cantine/commit/b5305ae353ac594551d27db320dd9ef11f7a9ce5))
* **Imports:** Cantines et Bilans: améliorations du message d'erreur pour une en-tête de fichier incorrecte ([#6289](https://github.com/betagouv/ma-cantine/issues/6289)) ([3315f77](https://github.com/betagouv/ma-cantine/commit/3315f7798e090a97fe3dc3fac34acb8f889d771f))
* **Imports:** Cantines: ajoute le colonne "groupe_id" ([#6273](https://github.com/betagouv/ma-cantine/issues/6273)) ([081283f](https://github.com/betagouv/ma-cantine/commit/081283f08dec3bbf5cf076f4addb14b6de548c66))
* **Ressources:** ajout des supports de webinaire sur les cuisines centrales et satellites ([#6302](https://github.com/betagouv/ma-cantine/issues/6302)) ([f6b75bc](https://github.com/betagouv/ma-cantine/commit/f6b75bc089049b81ee8e3adba08fa4035e56d043))


### Améliorations

* **Admin:** Cantines: mettre les champs ville & code postal en lecture-seule (le code INSEE est le pivot) ([#6291](https://github.com/betagouv/ma-cantine/issues/6291)) ([e07b569](https://github.com/betagouv/ma-cantine/commit/e07b569a7e26c0f239e46e7d107768ae638b6ef9))
* **Admin:** Cantines: ré-organiser les champs en groupes (fieldsets) ([#6294](https://github.com/betagouv/ma-cantine/issues/6294)) ([046feb3](https://github.com/betagouv/ma-cantine/commit/046feb3759142c2e0ad0cd589b2512403288b496))
* **Admin:** donner une plus grande largeur aux checkbox ([#6292](https://github.com/betagouv/ma-cantine/issues/6292)) ([6c71d90](https://github.com/betagouv/ma-cantine/commit/6c71d909949ff01d2d408151b345e072a9094da5))


### Corrections (bugs, typos...)

* **Ressources:** mise à jour de la convention de délégation ([#6301](https://github.com/betagouv/ma-cantine/issues/6301)) ([ee1243d](https://github.com/betagouv/ma-cantine/commit/ee1243ddaeb22e0dfa1e3b9ee6d5abce223553dc))


### Technique

* **Cantines:** désactiver le géo bot "temps réel" quand on utilise la factory (tests) ([#6298](https://github.com/betagouv/ma-cantine/issues/6298)) ([2c65cf3](https://github.com/betagouv/ma-cantine/commit/2c65cf364ceec1d5619c271f772d756763432421))
* **Historisations:** ajout de tests pour expliciter le fonctionnement actuel ([#6295](https://github.com/betagouv/ma-cantine/issues/6295)) ([c6371bf](https://github.com/betagouv/ma-cantine/commit/c6371bf355db74ead6522f2d8685a9873284671c))
* **Import:** créer une classe "base" commune qui supprime le code dupliqué ([#6279](https://github.com/betagouv/ma-cantine/issues/6279)) ([5ff87f0](https://github.com/betagouv/ma-cantine/commit/5ff87f0ea3e5d0a990db321d18a5ae7bcabc02e5))
* **Tests:** Cantines: utiliser skip_postgeneration_save pour éviter d'appeler 2x save dans la factory (qui utilise post_generation) ([#6297](https://github.com/betagouv/ma-cantine/issues/6297)) ([a24edb2](https://github.com/betagouv/ma-cantine/commit/a24edb2c5ac21f10ed1a3dc1d79ac4ab40a1098d))

## [2026.6.0](https://github.com/betagouv/ma-cantine/compare/v2026.5.0...v2026.6.0) (2026-01-26)


### Nouveautés

* **Admin:** configurer l'affichage des groupes pour pouvoir sélectionner des utilisateurs ([#6267](https://github.com/betagouv/ma-cantine/issues/6267)) ([18f9e1f](https://github.com/betagouv/ma-cantine/commit/18f9e1f673674d176894816c2637a0456baa5a37))


### Améliorations

* **API Data Gouv:** PATs: utiliser le cache pour appeler l'API qu'1 seule fois par semaine ([#6263](https://github.com/betagouv/ma-cantine/issues/6263)) ([24a65d0](https://github.com/betagouv/ma-cantine/commit/24a65d00881d912f2dc766d433a3a3ed222fe29b))
* **Brevo:** enlever de Django les emails de rappels 'pas de cantines' (les basculer sur Brevo) ([#6283](https://github.com/betagouv/ma-cantine/issues/6283)) ([0305b5b](https://github.com/betagouv/ma-cantine/commit/0305b5b0dcae9cd518abedf66424c311c6f6a311))
* **Open Data:** Cantines: ajouter la colonne groupe_id ([#6285](https://github.com/betagouv/ma-cantine/issues/6285)) ([8f81292](https://github.com/betagouv/ma-cantine/commit/8f81292677cb04d4dbfe3b169a6dd9e3952a4313))


### Technique

* **API Decoupage Administratif:** mieux mocker les appels API dans les tests ([#6284](https://github.com/betagouv/ma-cantine/issues/6284)) ([feb5a49](https://github.com/betagouv/ma-cantine/commit/feb5a49e038bf8b8bfcb519af211bae4010369c7))
* **API Recherche Entreprises:** mieux mocker les appels API dans les tests ([#6286](https://github.com/betagouv/ma-cantine/issues/6286)) ([7943f33](https://github.com/betagouv/ma-cantine/commit/7943f33b7fc0b168c048032502e29b03f686cde3))
* **Tests:** màj des fixtures (et enlever les SectorM2M) ([#6281](https://github.com/betagouv/ma-cantine/issues/6281)) ([9d0f1bf](https://github.com/betagouv/ma-cantine/commit/9d0f1bf6bad085c8a1b52d4c9c6473d0c623c1db))

## [2026.5.0](https://github.com/betagouv/ma-cantine/compare/v2026.4.0...v2026.5.0) (2026-01-23)


### Nouveautés

* **Imports:** Cantines: renommer "siret_livreur_repas" pour "siret_cuisine_centrale" ([#6261](https://github.com/betagouv/ma-cantine/issues/6261)) ([ad7729a](https://github.com/betagouv/ma-cantine/commit/ad7729a3414e820acb38315d76bb1a45d4c8d3ef))


### Améliorations

* **Admin:** cacher les Télédéclarations (ont été remplacés par les Diagnostics) ([#6269](https://github.com/betagouv/ma-cantine/issues/6269)) ([ab7878c](https://github.com/betagouv/ma-cantine/commit/ab7878cbf3ec04a94bec8d7a6c892a1f15f0fb2f))
* **Admin:** Cantines: améliorer l'affichage du filtre par secteurs ([#6268](https://github.com/betagouv/ma-cantine/issues/6268)) ([2f48ea3](https://github.com/betagouv/ma-cantine/commit/2f48ea3c205ff739c7066d2ab26e87bea1ccbc5f))
* **API Découpage Administratif:** utiliser le cache pour appeler l'API qu'1 seule fois par semaine ([#6262](https://github.com/betagouv/ma-cantine/issues/6262)) ([e202bbc](https://github.com/betagouv/ma-cantine/commit/e202bbcc4df6591d31ca9ed236b559821abffd83))
* **Cantines:** connaitre facilement la valeur précédente des champs qui sont modifiés, grâce à django-dirtyfields ([#6260](https://github.com/betagouv/ma-cantine/issues/6260)) ([2d9fa4a](https://github.com/betagouv/ma-cantine/commit/2d9fa4a23615d96730765ae04658a97bf2b75ed7))
* **Cantines:** lorsque le SIRET est modifié, réinitialiser tous les champs géo ([#6259](https://github.com/betagouv/ma-cantine/issues/6259)) ([73f2d35](https://github.com/betagouv/ma-cantine/commit/73f2d35cb12df111e0408afbd8b9195e96114aa5))
* **Ressource:** mise à jour des annexes du protocole de pesées ([#6272](https://github.com/betagouv/ma-cantine/issues/6272)) ([a52b8b3](https://github.com/betagouv/ma-cantine/commit/a52b8b304f87138e97ea0c1de68096735dcdaf83))


### Corrections (bugs, typos...)

* **Gaspillage alimentaire:** corrige le non affichage de l'input ([#6277](https://github.com/betagouv/ma-cantine/issues/6277)) ([5875e88](https://github.com/betagouv/ma-cantine/commit/5875e886b7382a448f3207c83272fbcac16109a3))
* **Groupes:** empêcher toute modification de cantines vers central ou central_serving ([#6265](https://github.com/betagouv/ma-cantine/issues/6265)) ([bb0a97f](https://github.com/betagouv/ma-cantine/commit/bb0a97f1a158831b99630cbdf0400af5a8f7f615))
* **Inscription:** corrige la redirection vers le tableau de bord après la création de compte ([#6276](https://github.com/betagouv/ma-cantine/issues/6276)) ([b60d39d](https://github.com/betagouv/ma-cantine/commit/b60d39d724c1064d9fe8fb87c5473649aa777cca))
* **Télédéclaration:** corrige la vérification des totaux viandes et poissons concaténée ([#6278](https://github.com/betagouv/ma-cantine/issues/6278)) ([dea4853](https://github.com/betagouv/ma-cantine/commit/dea485340a784d21ab1cee2064810cc3ac054606))

## [2026.4.0](https://github.com/betagouv/ma-cantine/compare/v2026.3.0...v2026.4.0) (2026-01-20)


### Nouveautés

* **Groupe:** ajouter le garde-fou au moment de télédéclarer pour un groupe avec des SAT déjà télédéclarés ([#6248](https://github.com/betagouv/ma-cantine/issues/6248)) ([763b0f1](https://github.com/betagouv/ma-cantine/commit/763b0f1d23606a4e1094f97ef400151da15f2e7b))
* **Ressources:** ajout du lien vers l'article "Bien calculer son nombre de couverts" ([#6257](https://github.com/betagouv/ma-cantine/issues/6257)) ([ad1b409](https://github.com/betagouv/ma-cantine/commit/ad1b409d55143878a3760ac8885d89ad468ae057))


### Améliorations

* **Cantines:** Actions: si le groupe a au moins 1 satellite avec des données manquantes, renvoyer FILL_SATELLITE_CANTEEN_DATA ([#6247](https://github.com/betagouv/ma-cantine/issues/6247)) ([1e84d64](https://github.com/betagouv/ma-cantine/commit/1e84d64b83c3a237655c037f93772d9fa31aebe7))


### Corrections (bugs, typos...)

* **Imports:** Cantine admin: corrige le fichier d'exemple ([#6254](https://github.com/betagouv/ma-cantine/issues/6254)) ([2c5dffa](https://github.com/betagouv/ma-cantine/commit/2c5dffa62879f0366858b84344d54098121f1092))
* **Logo:** corrige l'affichage du logo ma-cantine sur les pages mobile de l'ancien frontend ([#6253](https://github.com/betagouv/ma-cantine/issues/6253)) ([0cfcc39](https://github.com/betagouv/ma-cantine/commit/0cfcc3968c33046ed0df734a4ad81726c1db13fd))
* **Page cantine:** supprimer le lien "Contactez-nous" ([#6252](https://github.com/betagouv/ma-cantine/issues/6252)) ([4c8e638](https://github.com/betagouv/ma-cantine/commit/4c8e63801b5154fa6688c71e4fde6e8b920459ac))
* **Télédéclaration:** supprime la vérification inexactes de la sommes de totaux EGalim + France ([#6251](https://github.com/betagouv/ma-cantine/issues/6251)) ([09653ce](https://github.com/betagouv/ma-cantine/commit/09653ce53189ffcccc25e3d124441f861959c9a1))


### Technique

* **Cantines:** améliorations mineures sur la gestion des champs géo ([#6255](https://github.com/betagouv/ma-cantine/issues/6255)) ([e266bca](https://github.com/betagouv/ma-cantine/commit/e266bca9c1cf7441c235fd7b642881442d0f55a1))
* **Cantines:** améliorer les tests sur l'API de modification ([#6258](https://github.com/betagouv/ma-cantine/issues/6258)) ([c86f27a](https://github.com/betagouv/ma-cantine/commit/c86f27ac3dec8f7154152c6c67ece85efc0aa35d))
* **Cantines:** faire le ménage des is_central_cuisine plus utilisés ([#6245](https://github.com/betagouv/ma-cantine/issues/6245)) ([1f09c73](https://github.com/betagouv/ma-cantine/commit/1f09c738cfe46da5d56b69496da516c17722cf3f))
* **Liens documentation:** stocker les urls vers les ressources dans un fichier dédié  ([#6256](https://github.com/betagouv/ma-cantine/issues/6256)) ([0a8594c](https://github.com/betagouv/ma-cantine/commit/0a8594c122628931e6f178c916dbae8f4fd3f2b3))
* **Open Data:** enlever les exports parquet (gérés automatiquement par data.gouv) ([#6243](https://github.com/betagouv/ma-cantine/issues/6243)) ([e97f01a](https://github.com/betagouv/ma-cantine/commit/e97f01a1c4445cf31e8759b7c5fb604f4d328da5))

## [2026.3.0](https://github.com/betagouv/ma-cantine/compare/v2026.2.0...v2026.3.0) (2026-01-19)


### Nouveautés

* **Gérer mes satellites:** afficher la commune et le code postal dans le tableau ([#6236](https://github.com/betagouv/ma-cantine/issues/6236)) ([c646b65](https://github.com/betagouv/ma-cantine/commit/c646b653400f6bf4989f75a2bea3b3d0584ce207))
* **Gérer mes satellites:** ajoute une barre de recherche ([#6239](https://github.com/betagouv/ma-cantine/issues/6239)) ([5004fe2](https://github.com/betagouv/ma-cantine/commit/5004fe278352a52a04e6a3e165571843bb83f444))
* **Gérer mes satellites:** remplace les multiples actions en menu déroulant  ([#6234](https://github.com/betagouv/ma-cantine/issues/6234)) ([a3609e0](https://github.com/betagouv/ma-cantine/commit/a3609e077f178aef36356e3f208165c0dffe5073))
* **Imports:** Achats: améliorations du message d'erreur pour une en-tête de fichier incorrecte ([#6242](https://github.com/betagouv/ma-cantine/issues/6242)) ([74f3fe3](https://github.com/betagouv/ma-cantine/commit/74f3fe30508b6cdd4f33965bc70bda13e9c7a18a))


### Corrections (bugs, typos...)

* **Imports:** diverses corrections ([#6237](https://github.com/betagouv/ma-cantine/issues/6237)) ([226fd6c](https://github.com/betagouv/ma-cantine/commit/226fd6c02663f6d1dba8e6609eab5a876eacbe23))
* **Ressources:** supprime les espaces des noms de fichiers ([#6235](https://github.com/betagouv/ma-cantine/issues/6235)) ([67ef8e1](https://github.com/betagouv/ma-cantine/commit/67ef8e1e7884f5b4f99480fa4d054d2c37557dd1))


### Technique

* **Admin:** Echec d'import: améliorations (rendre l'utilisateur cliquable, afficher le message d'erreur) ([#6223](https://github.com/betagouv/ma-cantine/issues/6223)) ([ee590e7](https://github.com/betagouv/ma-cantine/commit/ee590e76e055e1614489f5c22ae2403062f33643))
* **Admin:** ordonner les config par groupes (list/fields/add) ([#6222](https://github.com/betagouv/ma-cantine/issues/6222)) ([ded4809](https://github.com/betagouv/ma-cantine/commit/ded4809d0367225980c75e0840396ac0ebbfd0b2))
* **Cantines:** API: utiliser un annotate pour is_managed_by_user (liste des satellites, page d'une cantine...) ([#6230](https://github.com/betagouv/ma-cantine/issues/6230)) ([a358990](https://github.com/betagouv/ma-cantine/commit/a35899092baf2312d78cd0108fa0097366b8b2f0))
* **Composants:** renomme des composants pour les organiser dans le dossier ([#6217](https://github.com/betagouv/ma-cantine/issues/6217)) ([85c66c7](https://github.com/betagouv/ma-cantine/commit/85c66c70d070819cc3283537cb4408d892df2eee))
* **Cuisines centrales:** supprime les références à ces anciens type de production dans le code vue3 ([#6241](https://github.com/betagouv/ma-cantine/issues/6241)) ([a1fb8f1](https://github.com/betagouv/ma-cantine/commit/a1fb8f13b502065bfb68fb48b2c30b091a3206d6))
* **Groupe:** créer un composant dédié pour l'affichage du tableau des satellites ([#6232](https://github.com/betagouv/ma-cantine/issues/6232)) ([43b8785](https://github.com/betagouv/ma-cantine/commit/43b87856ccc4ca673581c75816fae1250682614e))
* **Supprimer une cantine:** migration de la page en vue 3 ([#6240](https://github.com/betagouv/ma-cantine/issues/6240)) ([4813f7d](https://github.com/betagouv/ma-cantine/commit/4813f7d6dbb9b82f17088473b61c456c058bf8ff))

## [2026.2.0](https://github.com/betagouv/ma-cantine/compare/v2026.1.0...v2026.2.0) (2026-01-15)


### Nouveautés

* **Ressources:** ajout des supports webinaire 14/01/26 ([#6233](https://github.com/betagouv/ma-cantine/issues/6233)) ([83867db](https://github.com/betagouv/ma-cantine/commit/83867db296c77321b0c7e3be5b7055cf96b0ef2f))


### Améliorations

* **Ressources:** ajout de l'antiseche ([#6221](https://github.com/betagouv/ma-cantine/issues/6221)) ([f9ac776](https://github.com/betagouv/ma-cantine/commit/f9ac77629326428885ef44effe7307d66e1beeb8))


### Corrections (bugs, typos...)

* **Cantines:** Données géographiques: pouvoir enregistrer les modifications même si la cantine a des données manquantes par ailleurs ([#6229](https://github.com/betagouv/ma-cantine/issues/6229)) ([afea7d6](https://github.com/betagouv/ma-cantine/commit/afea7d66b62f521a1779eeb64136b2d6a7a233bb))
* **Graphique synthèse des achats:** corrige la différence entre le pourcentage renvoyé depuis le bilan et celui de la page publique de la cantine ([#6231](https://github.com/betagouv/ma-cantine/issues/6231)) ([7e2729f](https://github.com/betagouv/ma-cantine/commit/7e2729fd71e30cea6334847713880b2127442a7e))

## [2026.1.0](https://github.com/betagouv/ma-cantine/compare/v2026.0.3...v2026.1.0) (2026-01-14)


### Nouveautés

* **Tableau de bord:** cache les restaurants satellites des groupes et ajoute un lien vers la page de gestion ([#6214](https://github.com/betagouv/ma-cantine/issues/6214)) ([3a2fc82](https://github.com/betagouv/ma-cantine/commit/3a2fc8219ac5aa528caad46954de37690a919151))


### Améliorations

* **Gérer mes satellites:** petites améliorations d'interfaces (ordonner par nom, largeur colonnes..) ([#6216](https://github.com/betagouv/ma-cantine/issues/6216)) ([0b333b2](https://github.com/betagouv/ma-cantine/commit/0b333b2d0fd5d61e67d4d56e6d298db6de99c470))
* **Télédéclaration:** ajouter des champs supplémentaires (géo en particulier) dans les snapshots cantines & satellites ([#6202](https://github.com/betagouv/ma-cantine/issues/6202)) ([61a766c](https://github.com/betagouv/ma-cantine/commit/61a766ccff26fecb7849f2d7030c96b922b5680b))


### Corrections (bugs, typos...)

* **Cantine:** corrige le message d'erreur satellite manquant affiché sur des cantines non groupe ([#6215](https://github.com/betagouv/ma-cantine/issues/6215)) ([783e4f6](https://github.com/betagouv/ma-cantine/commit/783e4f6a012a8df36f6da4627d7ce30ff35ef98d))

## [2026.0.3](https://github.com/betagouv/ma-cantine/compare/v2026.0.2...v2026.0.3) (2026-01-13)


### Améliorations

* **Admin:** Cantines: accélérer la page 'détail d'une cantine' ([#6212](https://github.com/betagouv/ma-cantine/issues/6212)) ([22fe5f9](https://github.com/betagouv/ma-cantine/commit/22fe5f989f1e18821ebb6de00277081a8b2c73f5))
* **Admin:** Cantines: accélérer la page 'liste des cantines' ([#6211](https://github.com/betagouv/ma-cantine/issues/6211)) ([066396d](https://github.com/betagouv/ma-cantine/commit/066396dc4f8065b05a1903e91cccb2a58dbd01dc))
* **Cantines:** API: permettre de supprimer une cantine qui aurait des données manquantes ([#6198](https://github.com/betagouv/ma-cantine/issues/6198)) ([89447d8](https://github.com/betagouv/ma-cantine/commit/89447d83fdb31c7b6ff5a8e9686507a43b1e4e76))
* **Groupe:** utiliser le message d'erreur du serveur pour l'ajout ou le retrait d'un SAT avec un bilan télédéclaré ([#6210](https://github.com/betagouv/ma-cantine/issues/6210)) ([1ca1525](https://github.com/betagouv/ma-cantine/commit/1ca152515daefb9f1bfd08555a6c707a06ae395e))

## [2026.0.2](https://github.com/betagouv/ma-cantine/compare/v2026.0.1...v2026.0.2) (2026-01-13)


### Améliorations

* **Open Data:** Télédéclaration: améliorer la gestion des secteurs ([#6209](https://github.com/betagouv/ma-cantine/issues/6209)) ([41becd5](https://github.com/betagouv/ma-cantine/commit/41becd5e65bcc977f7cc2a206e184ad424cbd121))


### Corrections (bugs, typos...)

* **Groupe:** corrige l'affichage du bloc 'Restaurants Satellites non renseigné' ([#6207](https://github.com/betagouv/ma-cantine/issues/6207)) ([b7e1b91](https://github.com/betagouv/ma-cantine/commit/b7e1b91ef9ac1c45d6fc5f66f60709dfe2795a2f))
* **Télédéclaration:** corrige les vérifications sur les totaux des familles de la version simplifiée ([#6205](https://github.com/betagouv/ma-cantine/issues/6205)) ([92e1750](https://github.com/betagouv/ma-cantine/commit/92e175050a7b407302af4c379e20c88d3abec212))
* **Télédéclaration:** remplir le teledeclaration_id avec celle du bilan ([#6200](https://github.com/betagouv/ma-cantine/issues/6200)) ([c2938ac](https://github.com/betagouv/ma-cantine/commit/c2938ac1537ec23a431af71eae1f453462c8d596))


### Technique

* **API:** nouvelle organisation pour la gestion des erreurs renvoyées par l'API  ([#6199](https://github.com/betagouv/ma-cantine/issues/6199)) ([fa225af](https://github.com/betagouv/ma-cantine/commit/fa225af7837d1db7fda891fb4793e9f0565f9b87))
* **Diagnostics:** Tests: bouger les tests lié à la télédéclaration dans un fichier dédié ([#6203](https://github.com/betagouv/ma-cantine/issues/6203)) ([dd79f63](https://github.com/betagouv/ma-cantine/commit/dd79f632fb65d92d065b6ffab58f7dc6f411a7bd))
* **Open Data:** Cantines: retirer toute mention à sector_m2m (ancienne relation) ([#6204](https://github.com/betagouv/ma-cantine/issues/6204)) ([e26dd01](https://github.com/betagouv/ma-cantine/commit/e26dd0151b6fe39ba939d5db756283650a41aaa0))

## [2026.0.1](https://github.com/betagouv/ma-cantine/compare/v2026.0.0...v2026.0.1) (2026-01-12)


### Améliorations

* **TD:** Cantines: remplir le champ declaration_donnees_2025 toutes les nuits (pour Open Data & Metabase) ([#6163](https://github.com/betagouv/ma-cantine/issues/6163)) ([685d4af](https://github.com/betagouv/ma-cantine/commit/685d4af4039b6990ab7d5aa923328c95dcb5d8d5))


### Corrections (bugs, typos...)

* **Utilisateurs:** Brevo: nouveau champ pour indiquer si l'utilisateur a été supprimé de Brevo (et éviter les erreurs de synchro) ([#6177](https://github.com/betagouv/ma-cantine/issues/6177)) ([0861201](https://github.com/betagouv/ma-cantine/commit/08612014f40b68e05fba3ab3a737c5a3196414ac))

## [2026.0.0](https://github.com/betagouv/ma-cantine/compare/v2025.50.0...v2026.0.0) (2026-01-12)


### Nouveautés

* **Groupe:** afficher le badge "à compléter" pour les satellites peut importe le type de déclaration du groupe ([#6187](https://github.com/betagouv/ma-cantine/issues/6187)) ([fd61c4c](https://github.com/betagouv/ma-cantine/commit/fd61c4c590de8a435a53231481483016814a6d71))


### Améliorations

* **Metabase:** exporter les TD avec le même nom de table (désactiver le versionnage) ([#6195](https://github.com/betagouv/ma-cantine/issues/6195)) ([f1d5d03](https://github.com/betagouv/ma-cantine/commit/f1d5d037d0e2f79aad353d6d622945dd17e8f515))
* **Metabase:** exporter les TD toutes les 6h ([#6194](https://github.com/betagouv/ma-cantine/issues/6194)) ([bcc1839](https://github.com/betagouv/ma-cantine/commit/bcc18396135d14c13c8b8f7ec68432405dfb9fb1))
* **Metabase:** Groupes: ajuster les exports TD ([#6193](https://github.com/betagouv/ma-cantine/issues/6193)) ([438e056](https://github.com/betagouv/ma-cantine/commit/438e056367aa85615949b6e2c44bfd15dafe6498))


### Technique

* **Cantines:** renommer le flag run_validations en skip_validations ([#6191](https://github.com/betagouv/ma-cantine/issues/6191)) ([b6f0024](https://github.com/betagouv/ma-cantine/commit/b6f00244f41c737be23e1d70000d62e7ff974c8d))
* **Cantines:** stocker le champ is_filled + le mettre à jour à chaque save ([#6190](https://github.com/betagouv/ma-cantine/issues/6190)) ([79db688](https://github.com/betagouv/ma-cantine/commit/79db68812f20be19b488c651a2b006c6c7745da7))
* **Cantines:** utiliser save(skip_validations=True) au lieu de .filter().update() ([#6192](https://github.com/betagouv/ma-cantine/issues/6192)) ([450b973](https://github.com/betagouv/ma-cantine/commit/450b97336288b9e5e808c36238e794775b5b1fa7))
* **Groupes:** désactiver le test sur la migration maintenant qu'elle est derrière nous ([#6196](https://github.com/betagouv/ma-cantine/issues/6196)) ([5084396](https://github.com/betagouv/ma-cantine/commit/5084396713936da13ce5da2ec15db4003f6b6148))
* release 2026.0.0 ([bb3e085](https://github.com/betagouv/ma-cantine/commit/bb3e08564cdb5e59645216f496d3ba90bbc77c48))

## [2025.50.0](https://github.com/betagouv/ma-cantine/compare/v2025.49.0...v2025.50.0) (2026-01-11)


### Nouveautés

* **Cantine:** afficher l'id de l'établissement dans la page "Gérer mon établissement" ([#6135](https://github.com/betagouv/ma-cantine/issues/6135)) ([09aee98](https://github.com/betagouv/ma-cantine/commit/09aee981628ef0d99d85a9daec1813f2472ee743))
* **Cantines:** nouveau champ 'groupe' pour lier les cantines entre elles ([#6133](https://github.com/betagouv/ma-cantine/issues/6133)) ([fc297a8](https://github.com/betagouv/ma-cantine/commit/fc297a84ea92b6f09d998380fb08941c18777e1c))
* **Cantines:** nouveau type de production 'groupe' ([#6125](https://github.com/betagouv/ma-cantine/issues/6125)) ([994dcd7](https://github.com/betagouv/ma-cantine/commit/994dcd718e8f74a2b72854985bdbe67aef32da92))
* **Cantine:** supprime central et central serving du formulaire d'ajout et de modification de cantine ([#6147](https://github.com/betagouv/ma-cantine/issues/6147)) ([040756b](https://github.com/betagouv/ma-cantine/commit/040756b832a2ec7de3035b0a185a75b6784e5e7c))
* **Gérer mes satellites:** petites corrections sur la page et affichage du badge des satellites ([#6146](https://github.com/betagouv/ma-cantine/issues/6146)) ([cac25fd](https://github.com/betagouv/ma-cantine/commit/cac25fda25782b4a1ff24deeca7756b87ec0afad))
* **Groupe:** affiche la page de création de groupe ([#6144](https://github.com/betagouv/ma-cantine/issues/6144)) ([731c030](https://github.com/betagouv/ma-cantine/commit/731c030242d46cbd416b2edaf9b5c6a7140d378f))
* **Groupe:** affiche le nombre de satellites liés depuis le tableau de bord ([#6145](https://github.com/betagouv/ma-cantine/issues/6145)) ([7553ab0](https://github.com/betagouv/ma-cantine/commit/7553ab0fb3d90b93349ea9fe03c9b614d6e88945))
* **Groupe:** affiche les informations du nouveau type dans la page "Tableau de bord" ([#6132](https://github.com/betagouv/ma-cantine/issues/6132)) ([e426c4d](https://github.com/betagouv/ma-cantine/commit/e426c4ddc0cf98a2d3821e2c2a56221668eb5d67))
* **Groupe:** afficher le badge "A compléter" si un SAT du groupe a des données incomplètes ([#6185](https://github.com/betagouv/ma-cantine/issues/6185)) ([40689b8](https://github.com/betagouv/ma-cantine/commit/40689b8a3e5523d46bf8ebbebf03a04d533e7058))
* **Groupe:** afficher les informations du groupe pour un restaurant satellite ([#6143](https://github.com/betagouv/ma-cantine/issues/6143)) ([eb32b8b](https://github.com/betagouv/ma-cantine/commit/eb32b8befffc7eec8a9ad977208a5432e6292a9c))
* **Groupe:** afficher les ressources Crisp ([#6157](https://github.com/betagouv/ma-cantine/issues/6157)) ([3d0c62d](https://github.com/betagouv/ma-cantine/commit/3d0c62d21ace471625218d139f6e8a380f66011d))
* **Groupe:** ajout de la page de création avec les informations en statique ([#6126](https://github.com/betagouv/ma-cantine/issues/6126)) ([f011129](https://github.com/betagouv/ma-cantine/commit/f011129a4896145b4210b45e18ad4872f7373a8b))
* **Groupe:** ajouter un satellite à son groupe depuis la page "Gérer mes satellites" ([#6149](https://github.com/betagouv/ma-cantine/issues/6149)) ([cb25bb4](https://github.com/betagouv/ma-cantine/commit/cb25bb476a65a1fb7e97568848c1af4a6a9d02e6))
* **Groupe:** connecte les pages de création et modification de groupe à l'api ([#6130](https://github.com/betagouv/ma-cantine/issues/6130)) ([9fb6157](https://github.com/betagouv/ma-cantine/commit/9fb6157ec7e886e3b2d8c369961cbf4c5909adf4))
* **Groupe:** migrer les 'central' & 'central_serving' en 'groupe' ([#6152](https://github.com/betagouv/ma-cantine/issues/6152)) ([287f18f](https://github.com/betagouv/ma-cantine/commit/287f18ffda2bf5c8a06876b75df0cc5c42939750))
* **Groupe:** mise à jour de la page "Gérer mon établissement" ([#6134](https://github.com/betagouv/ma-cantine/issues/6134)) ([8d02074](https://github.com/betagouv/ma-cantine/commit/8d02074a5dccea398a42cafa3e7d025b5be9b191))
* **Groupe:** mise à jour du parcours de création de bilan et télédéclaration ([#6164](https://github.com/betagouv/ma-cantine/issues/6164)) ([7cdaefa](https://github.com/betagouv/ma-cantine/commit/7cdaefa4354c3b8cca5e7fa2a1719de74b04c688))
* **Groupe:** Refonte des checks "données manquantes" ([#6155](https://github.com/betagouv/ma-cantine/issues/6155)) ([daa3ec2](https://github.com/betagouv/ma-cantine/commit/daa3ec27d1725b1a872a242b4e93a3a0cd02820e))
* **Groupe:** remplace "SIREN de l'unité légale" par "SIREN" ([#6131](https://github.com/betagouv/ma-cantine/issues/6131)) ([6818a02](https://github.com/betagouv/ma-cantine/commit/6818a02017df7c88f0573902e7e2710ed66781f3))
* **Groupe:** supprime l'ancienne page de création des cantines satellites reliées à une cuisine centrale ([#6128](https://github.com/betagouv/ma-cantine/issues/6128)) ([3c9a7a9](https://github.com/betagouv/ma-cantine/commit/3c9a7a94cb7115cde65195b599409bdf01c22a98))
* **Groupe:** Télédéclaration: bloquer si les données de la cantine ne sont pas complètes ([#6165](https://github.com/betagouv/ma-cantine/issues/6165)) ([34b8b0a](https://github.com/betagouv/ma-cantine/commit/34b8b0a0de20689163ccc1f02da3728a09ab4e7b))
* **Import:** Cantines: supprime le type de production "central" et met à jour les champs liés ([#6172](https://github.com/betagouv/ma-cantine/issues/6172)) ([3577dba](https://github.com/betagouv/ma-cantine/commit/3577dba87889823fb41b0d93f1ad17585b55b890))
* **Restaurants Satellites:** parcours lors qu'un SAT est rattaché à un groupe ([#6180](https://github.com/betagouv/ma-cantine/issues/6180)) ([1442edc](https://github.com/betagouv/ma-cantine/commit/1442edc9e1f830804ba5e37f2a2a428813741634))


### Améliorations

* **Cantine:** renomme les fichiers pour distinguer les groupes des autres établissements ([#6127](https://github.com/betagouv/ma-cantine/issues/6127)) ([0b5d278](https://github.com/betagouv/ma-cantine/commit/0b5d27870f875c3aeef5090c650da5ecb88c48af))
* **Cantines:** API: ne plus autoriser la création de cantines central & central_serving ([#6188](https://github.com/betagouv/ma-cantine/issues/6188)) ([7d72910](https://github.com/betagouv/ma-cantine/commit/7d729105904e8fe714bff85f2c05afb9a4954f8c))
* **Cantines:** cacher les groupes de 'Trouver une cantine' & de l'Open Data ([#6129](https://github.com/betagouv/ma-cantine/issues/6129)) ([94faf9d](https://github.com/betagouv/ma-cantine/commit/94faf9d09a45476b2082305d588f2c212031d49a))
* **Gérer mes satellites:** petits correctifs et améliorations de la page ([#6138](https://github.com/betagouv/ma-cantine/issues/6138)) ([a324ecd](https://github.com/betagouv/ma-cantine/commit/a324ecd9469887d71db683ad582713eba3b336da))
* **Groupe:** affiche le badge "À compléter" si un groupe a des satellites incomplets ([#6184](https://github.com/betagouv/ma-cantine/issues/6184)) ([ba9dae8](https://github.com/betagouv/ma-cantine/commit/ba9dae8c038665d757b4e14684209aaf2e1e60f0))
* **Groupe:** empecher de rattacher (ou enlever) un satellite si le groupe a une TD ([#6186](https://github.com/betagouv/ma-cantine/issues/6186)) ([1966568](https://github.com/betagouv/ma-cantine/commit/1966568896e2c456a7528f41c24ec6e0f86a16a3))
* **Groupes:** API: endpoint pour ajouter (et enlever) des satellites ([#6137](https://github.com/betagouv/ma-cantine/issues/6137)) ([1bd47ad](https://github.com/betagouv/ma-cantine/commit/1bd47ad82b4054ee0a1788f34c6aee28bd8e88d5))
* **Groupes:** API: endpoint pour récupérer la liste des cantines rattachées ([#6136](https://github.com/betagouv/ma-cantine/issues/6136)) ([d7f7eca](https://github.com/betagouv/ma-cantine/commit/d7f7eca78be059c85a7f3008cda0fd8219026f47))
* **Groupes:** API: renvoyer l'action à effectuer pour chacun des satellites ([#6141](https://github.com/betagouv/ma-cantine/issues/6141)) ([a0f6f5f](https://github.com/betagouv/ma-cantine/commit/a0f6f5f5009a78ace126d24a0f5265f0cb74d898))
* **Groupes:** API: renvoyer les infos du groupe dans l'endpoint 'single_canteen' ([#6139](https://github.com/betagouv/ma-cantine/issues/6139)) ([5af4add](https://github.com/betagouv/ma-cantine/commit/5af4add2a286dc27c539af0f2b408b189d184429))
* **Groupes:** API: renvoyer les infos du nombre de satellites dans l'endpoint 'single_canteen' ([#6140](https://github.com/betagouv/ma-cantine/issues/6140)) ([0bd9f35](https://github.com/betagouv/ma-cantine/commit/0bd9f35a7406bd9e7b32e92c68c237baabd94725))
* **Groupes:** Bilans: renvoyer les bilans du groupe si satellite ([#6175](https://github.com/betagouv/ma-cantine/issues/6175)) ([ea09242](https://github.com/betagouv/ma-cantine/commit/ea092429065a1ca3bd65bf52d6c3834c2acc1c40))
* **Groupes:** permettre leur suppression seulement si aucun satellite rattaché ([#6162](https://github.com/betagouv/ma-cantine/issues/6162)) ([37afd53](https://github.com/betagouv/ma-cantine/commit/37afd53c9daaa5f44fd0911ea49f58692d5b399f))
* **Groupes:** Télédéclaration: faire aussi un snapshot de leur satellites + remplir correctement teledeclaration_mode ([#6158](https://github.com/betagouv/ma-cantine/issues/6158)) ([5d49ceb](https://github.com/betagouv/ma-cantine/commit/5d49ceba578214ff0b7136136e8e0ef4fa669492))
* **Groupe:** Télédéclaration: empêcher la TD si un des satellites a des données manquantes ([#6182](https://github.com/betagouv/ma-cantine/issues/6182)) ([c7f1e86](https://github.com/betagouv/ma-cantine/commit/c7f1e868860343dd4759c979edfafff82ce7624a))


### Corrections (bugs, typos...)

* **Cantines:** Règles métiers: les ministères de tutelle sont uniquement obligatoires pour les établissements public ([#6179](https://github.com/betagouv/ma-cantine/issues/6179)) ([c226bf6](https://github.com/betagouv/ma-cantine/commit/c226bf657e08e8b67182c76e6b012eee563c249b))
* **Groupe:** API: pouvoir ajouter (et enlever) des satellites qui ont des infos manquantes ([#6167](https://github.com/betagouv/ma-cantine/issues/6167)) ([d04f547](https://github.com/betagouv/ma-cantine/commit/d04f547d77f8e7272c8c5cde0fa9127ab2d23335))
* **Groupe:** corrections suite au recettage ([#6166](https://github.com/betagouv/ma-cantine/issues/6166)) ([a57bb1c](https://github.com/betagouv/ma-cantine/commit/a57bb1cb29c10f5a92c5dd7fdd37af8b6a5b7c23))
* **Groupe:** diverses améliorations pour la page "Gérer mes satellites" ([#6170](https://github.com/betagouv/ma-cantine/issues/6170)) ([5850e91](https://github.com/betagouv/ma-cantine/commit/5850e91f6a40874f8ce45a7a9170a537ccf3bcc0))
* **Groupe:** diverses corrections frontend ([#6148](https://github.com/betagouv/ma-cantine/issues/6148)) ([1db838e](https://github.com/betagouv/ma-cantine/commit/1db838e1231014242146f5c041de090cbbfa825f))
* **Groupe:** diverses corrections frontend ([#6159](https://github.com/betagouv/ma-cantine/issues/6159)) ([7a67566](https://github.com/betagouv/ma-cantine/commit/7a675664ab21614710e4b6cf47758fbbea57da73))
* **Groupe:** le champ central_producer_siret d'un satellite n'est plus obligatoire ([#6178](https://github.com/betagouv/ma-cantine/issues/6178)) ([c7a271e](https://github.com/betagouv/ma-cantine/commit/c7a271ea1275fdc1a3688978f00f828eb4768bbc))
* **Groupe:** permettre aux satellites avec des groupes en "APPRO" de télédéclarer les autres volets ([#6183](https://github.com/betagouv/ma-cantine/issues/6183)) ([2a29655](https://github.com/betagouv/ma-cantine/commit/2a296551705509333c995dec6cc68219553d4690))
* **Télédéclaration détaillée:** corrige le message d'erreur des totaux suite à un problème d'arrondis ([#6173](https://github.com/betagouv/ma-cantine/issues/6173)) ([951fad9](https://github.com/betagouv/ma-cantine/commit/951fad9d6a6a5c2979d6637f64afebb0f42cdcc0))


### Technique

* **Cantines:** ajoute une property is_deleted pour les cantines soft-deleted ([#6161](https://github.com/betagouv/ma-cantine/issues/6161)) ([da5bcfe](https://github.com/betagouv/ma-cantine/commit/da5bcfe619d26f802d162aa247687b6a827f32b0))
* **Cantines:** API: enlever les anciens endpoints CC-CSAT ([#6153](https://github.com/betagouv/ma-cantine/issues/6153)) ([526899f](https://github.com/betagouv/ma-cantine/commit/526899fc00e4b68c593d57886f2b087666e8e160))
* **Cantines:** enlève le signal post-modification de central (plus besoin) ([#6160](https://github.com/betagouv/ma-cantine/issues/6160)) ([6190e44](https://github.com/betagouv/ma-cantine/commit/6190e44e35cacbfe53b17c39871b640076a41a6c))
* **Cantines:** permettre d'ignorer les règles métiers grâce à run_validations=False ([#6156](https://github.com/betagouv/ma-cantine/issues/6156)) ([cd7edf7](https://github.com/betagouv/ma-cantine/commit/cd7edf7bbe1e09a39167385e28fab2178ce1ee35))
* **Groupe:** API: ajout de tests supplémentaires sur les nouveaux endpoints ([#6142](https://github.com/betagouv/ma-cantine/issues/6142)) ([4579dcd](https://github.com/betagouv/ma-cantine/commit/4579dcdba1b9004e6ec5ea7ff2364c8f1c8f805f))
* **Groupe:** nouvelle property satellites_missing_data_count pour connaitre le nombre de satellites avec des données manquantes ([#6181](https://github.com/betagouv/ma-cantine/issues/6181)) ([cf11577](https://github.com/betagouv/ma-cantine/commit/cf115776b1b79640b85d845ea2014cac4b5f4048))
* **Groupes:** Brevo: corrige le nb_cantines_groupe ([#6176](https://github.com/betagouv/ma-cantine/issues/6176)) ([be900f8](https://github.com/betagouv/ma-cantine/commit/be900f81fcbf77eb5520246527efcfa69f57ee8a))

## [2025.49.0](https://github.com/betagouv/ma-cantine/compare/v2025.48.0...v2025.49.0) (2026-01-06)


### Nouveautés

* **Imports:** Bilans simples: rend la nouvelle page visible à nos utilisateurs ([#6082](https://github.com/betagouv/ma-cantine/issues/6082)) ([5a574bf](https://github.com/betagouv/ma-cantine/commit/5a574bf9155deca79a49caad3c55775ab63d73f2))


### Améliorations

* **Bilans:** ajouter de nouvelles règles métiers au niveau du modèle (valeur totale) (2/2) ([#6120](https://github.com/betagouv/ma-cantine/issues/6120)) ([cfc87f7](https://github.com/betagouv/ma-cantine/commit/cfc87f753e720570a85465607eb0910ba8f4138a))
* **Bilans:** ajouter de nouvelles règles métiers au niveau du modèle (valeur totale) (bilans simples) ([#6119](https://github.com/betagouv/ma-cantine/issues/6119)) ([c531d40](https://github.com/betagouv/ma-cantine/commit/c531d404139b1227731a699c2a91836c86a19333))


### Corrections (bugs, typos...)

* **Cantines:** API: répare l'endpoint recherche par siren ([#6123](https://github.com/betagouv/ma-cantine/issues/6123)) ([8876a65](https://github.com/betagouv/ma-cantine/commit/8876a65403ef141ca3623dfed803c7960ce712c1))
* **Cantines:** API: répare l'endpoint recherche par siren (ajout de tests) ([#6124](https://github.com/betagouv/ma-cantine/issues/6124)) ([aa4c44f](https://github.com/betagouv/ma-cantine/commit/aa4c44fb3e2021f656f01e5d133119f2a06e915f))


### Technique

* **Achats:** éviter une requête N+1 sur l'endpoint /api/v1/purchases ([#6122](https://github.com/betagouv/ma-cantine/issues/6122)) ([d7ed2e8](https://github.com/betagouv/ma-cantine/commit/d7ed2e8458fe47d28ef97262947f0a0e69618563))

## [2025.48.0](https://github.com/betagouv/ma-cantine/compare/v2025.47.0...v2025.48.0) (2026-01-05)


### Nouveautés

* **Bilans:** autoriser la création de bilans uniquement pour l'année précédente et l'année suivante ([#6116](https://github.com/betagouv/ma-cantine/issues/6116)) ([927cb2f](https://github.com/betagouv/ma-cantine/commit/927cb2f6083985efa13bf0c87002201668274523))
* **Bilans:** Imports: création de la page avec les données statiques (bilans simples) ([#6075](https://github.com/betagouv/ma-cantine/issues/6075)) ([2b01d1a](https://github.com/betagouv/ma-cantine/commit/2b01d1aaec390cca6bec2ef5acd3fce5a27d4456))
* **Bilans:** Imports: mise en place de l'import avec Validata et le nouveau schéma (bilans simples) ([#6078](https://github.com/betagouv/ma-cantine/issues/6078)) ([2c1eb45](https://github.com/betagouv/ma-cantine/commit/2c1eb450a8b499f4af39d9f53ebdff71b2e22856))
* **Bilans:** Imports: v1 du schéma pour le bilan simplifié (compatible Validata) ([#6053](https://github.com/betagouv/ma-cantine/issues/6053)) ([c752172](https://github.com/betagouv/ma-cantine/commit/c7521729c3c5c254e4e85fa922b61c23d7dddd5b))
* **Ressources:** ajout du guide pratique "plus de bio" ([#6107](https://github.com/betagouv/ma-cantine/issues/6107)) ([3b6fe23](https://github.com/betagouv/ma-cantine/commit/3b6fe23edf1efda55b39b42724fcb83ff74eacf7))
* **Télédéclaration:** nouvelle campagne pour l'année 2025 ([#6103](https://github.com/betagouv/ma-cantine/issues/6103)) ([19a050f](https://github.com/betagouv/ma-cantine/commit/19a050f0f4e032972c0165448ba53fff98bcbaf5))


### Améliorations

* **Bilans:** Admin: lancer les validation à la création & modification ([#6117](https://github.com/betagouv/ma-cantine/issues/6117)) ([13c6cee](https://github.com/betagouv/ma-cantine/commit/13c6cee44629b6ef74e427e902accf58f9c4b6b7))
* **Bilans:** ajouter de nouvelles règles métiers au niveau du modèle (bilans simples) ([#6086](https://github.com/betagouv/ma-cantine/issues/6086)) ([6280698](https://github.com/betagouv/ma-cantine/commit/62806981b64d719848838ce65a754d250686d630))
* **Imports:** améliore le message d'erreur pour les lignes vides ([#6104](https://github.com/betagouv/ma-cantine/issues/6104)) ([f21a36a](https://github.com/betagouv/ma-cantine/commit/f21a36a7327649188b9eb6f86bdb61b7f9aaee91))


### Corrections (bugs, typos...)

* **Badges:** le badge télédéclaré est prioritaire par rapport aux informations manquantes ([#6118](https://github.com/betagouv/ma-cantine/issues/6118)) ([e75fe74](https://github.com/betagouv/ma-cantine/commit/e75fe740540ac50a3e2d60f21ef2c762da0c7b1f))
* **Brevo:** ne pas tenter de synchroniser le champ email vu qu'il est déjà connu par Brevo ([#6085](https://github.com/betagouv/ma-cantine/issues/6085)) ([3f0c8db](https://github.com/betagouv/ma-cantine/commit/3f0c8db12ddf75f51483fc7f84ce1ddf44ac7d55))
* **Imports:** Bilans: autorise les formats texte et nombre pour le champ "année_bilan" ([#6115](https://github.com/betagouv/ma-cantine/issues/6115)) ([1d709cd](https://github.com/betagouv/ma-cantine/commit/1d709cdb874b5224b946f7e4b3bfa02b20eeca72))
* **Imports:** Bilans: remplace provenance France par origine France ([#6106](https://github.com/betagouv/ma-cantine/issues/6106)) ([1cc73f8](https://github.com/betagouv/ma-cantine/commit/1cc73f8aba0cd06d9a61c94161f1f7c2ffc7e711))
* **Télédéclaration:** justificatif de la télédéclaration détaillée n'affiche pas tous les champs ([#6105](https://github.com/betagouv/ma-cantine/issues/6105)) ([d0bba30](https://github.com/betagouv/ma-cantine/commit/d0bba303dad7cb276544bff13cb89b4ff448a8d6))
* **Télédéclaration:** le sous-badge "à compléter" s'affichait pour une cuisine centrale sans secteurs ([#6108](https://github.com/betagouv/ma-cantine/issues/6108)) ([daeb7dc](https://github.com/betagouv/ma-cantine/commit/daeb7dc83442579cc5c178d0945e069a33bdbda3))
* **Trouver une cantine:** corrige l'affichage répétitif des villes ([#6109](https://github.com/betagouv/ma-cantine/issues/6109)) ([f82707e](https://github.com/betagouv/ma-cantine/commit/f82707e3cee405d2a58fe0da9ac427ba87abff6e))


### Technique

* **Bilans:** Imports: commente l'ancien code en attendant de finir l'intégration des nouveaux imports bilans ([#6080](https://github.com/betagouv/ma-cantine/issues/6080)) ([264d06f](https://github.com/betagouv/ma-cantine/commit/264d06ff5f0b7da118279e94ebba96630ba0726f))
* **Brevo:** fait le ménage dans la logique pour filtrer les utilisateurs ([#6084](https://github.com/betagouv/ma-cantine/issues/6084)) ([fc26cb5](https://github.com/betagouv/ma-cantine/commit/fc26cb50130c5bda251c501f2ed62b6c87328291))
* **Brevo:** rajoute un champ avec le nombre de groupe (CC) ([#6111](https://github.com/betagouv/ma-cantine/issues/6111)) ([c24c59a](https://github.com/betagouv/ma-cantine/commit/c24c59aae607a3baf1615027ed93389c2d14981c))
* **Brevo:** renomme 1 champ. supprime un autre non utilisé ([#6110](https://github.com/betagouv/ma-cantine/issues/6110)) ([d1ad10c](https://github.com/betagouv/ma-cantine/commit/d1ad10c9f7d6f4d8f088a56fe8caa9cb0f2826d0))
* **Diagnostics:** ajouter un related_name sur la FK canteen ([#6113](https://github.com/betagouv/ma-cantine/issues/6113)) ([b5eacdf](https://github.com/betagouv/ma-cantine/commit/b5eacdfc9d209a58be187c11aa13b53096e4ae62))
* **Imports:** ménage pour homogénéiser entre cantines, achats & bilans ([#6083](https://github.com/betagouv/ma-cantine/issues/6083)) ([8999ec6](https://github.com/betagouv/ma-cantine/commit/8999ec6bba23597b861a3ba9fb7e3f845c483b54))


### Documentation

* **Open Data:** mettre les constants dans datagouv.py & documenter l'ajout de nouveaux fichiers ([#6079](https://github.com/betagouv/ma-cantine/issues/6079)) ([9f10193](https://github.com/betagouv/ma-cantine/commit/9f101932481bba713d3397bc799f0f2991b9f157))

## [2025.47.0](https://github.com/betagouv/ma-cantine/compare/v2025.46.0...v2025.47.0) (2025-12-23)


### Nouveautés

* **Observatoire:** rend les statistiques de la campagne de télédéclaration 2025 publiques ([#6068](https://github.com/betagouv/ma-cantine/issues/6068)) ([2e79822](https://github.com/betagouv/ma-cantine/commit/2e798229945eca17e417b888bd169ee31e8f7e75))
* **Open Data:** exporte les données de la campagne de télédéclaration 2025 ([#6073](https://github.com/betagouv/ma-cantine/issues/6073)) ([51ed5cf](https://github.com/betagouv/ma-cantine/commit/51ed5cf1f907d9562550148de9cfa230a20f18e5))
* **Utilisateurs:** Brevo: utiliser les données stockées dans le nouveau champ 'data' ([#6072](https://github.com/betagouv/ma-cantine/issues/6072)) ([c1aea24](https://github.com/betagouv/ma-cantine/commit/c1aea246b281455e40d299e29d6de559547220a5))
* **Utilisateurs:** stocker toutes les nuits des données en lien avec les cantines gérées ([#6069](https://github.com/betagouv/ma-cantine/issues/6069)) ([48775c5](https://github.com/betagouv/ma-cantine/commit/48775c5af4e32e226ac60f64192de7c89e5ac7ae))


### Améliorations

* **Open Data:** mieux exporter les secteurs des cantines ([#6076](https://github.com/betagouv/ma-cantine/issues/6076)) ([54d75c1](https://github.com/betagouv/ma-cantine/commit/54d75c15a56f08fe8acda919fd59686201160623))


### Corrections (bugs, typos...)

* **Observatoire:** cache temporairement le graphique "Viandes origine France" ([#6077](https://github.com/betagouv/ma-cantine/issues/6077)) ([b5a02db](https://github.com/betagouv/ma-cantine/commit/b5a02db2972ddbe61c2a3e4797fa5abdb5bb7af5))


### Technique

* **Cantines:** évite d'avoir à dupliquer les QuerySet dans Manager ([#6071](https://github.com/betagouv/ma-cantine/issues/6071)) ([4e3fe60](https://github.com/betagouv/ma-cantine/commit/4e3fe60338b5ee0f80946aba89c626ad969c39cc))

## [2025.46.0](https://github.com/betagouv/ma-cantine/compare/v2025.45.1...v2025.46.0) (2025-12-22)


### Nouveautés

* **Badge:** valide le badge végétarien pour les cantines d'au minimum 200 couverts journaliers et un plan de diversification alimentaire ([#6051](https://github.com/betagouv/ma-cantine/issues/6051)) ([268b9aa](https://github.com/betagouv/ma-cantine/commit/268b9aa88d918f9331b6662ec8fdcef41cf75d0b))
* **Cantines:** affiche le numéro ID de la cantine ([#6066](https://github.com/betagouv/ma-cantine/issues/6066)) ([21c0b38](https://github.com/betagouv/ma-cantine/commit/21c0b38bb159cf57a0947e2b784fc0fe826118ec))
* **Imports:** Achats: utilise Validata pour vérifier le fichier importé et autorise Excel ([#6057](https://github.com/betagouv/ma-cantine/issues/6057)) ([e4d99ec](https://github.com/betagouv/ma-cantine/commit/e4d99ecd867409e370ea3bf1e21651ec687a63bc))
* **Ressources:** ajoute le bilan 2025 ([#6067](https://github.com/betagouv/ma-cantine/issues/6067)) ([c3cb4e2](https://github.com/betagouv/ma-cantine/commit/c3cb4e2b6c6c9793cf0d3ffeeba873281938c9b0))
* **Télédéclaration:** mise à jour des questions du volet "Menu végétarien" ([#6049](https://github.com/betagouv/ma-cantine/issues/6049)) ([808fc7a](https://github.com/betagouv/ma-cantine/commit/808fc7a44f9a3a9c493c0797163f5688ae68cb6f))
* **Télédéclaration:** Végétarien: déplace le bouton de remplissage automatique à la première question ([#6061](https://github.com/betagouv/ma-cantine/issues/6061)) ([9227c28](https://github.com/betagouv/ma-cantine/commit/9227c2810f8d46cda53da301d33f7aa12b2ae0e1))


### Améliorations

* **Brevo:** ajout des champs de bases utilisateurs (nom, prénom, email, dernière connexion) ([#6062](https://github.com/betagouv/ma-cantine/issues/6062)) ([43f4dfe](https://github.com/betagouv/ma-cantine/commit/43f4dfe050e4caa1b85d8e8b137b1821d3173d86))
* **Ressources:** homogénéise les noms des fichiers des rapports statistiques EGalim ([#6070](https://github.com/betagouv/ma-cantine/issues/6070)) ([bf0773b](https://github.com/betagouv/ma-cantine/commit/bf0773b26b223ec1b234e809e873a358e52e47b5))
* **Utilisateurs:** nouveau champ 'data' (JSONField) pour stocker des données calculées ([#6064](https://github.com/betagouv/ma-cantine/issues/6064)) ([bb48c5a](https://github.com/betagouv/ma-cantine/commit/bb48c5a3c23d918984a6f9996d83b1c36d58b22b))


### Corrections (bugs, typos...)

* **Imports:** Achats: remet un test de valeur non valide du regex ([#6059](https://github.com/betagouv/ma-cantine/issues/6059)) ([d735595](https://github.com/betagouv/ma-cantine/commit/d73559552457d6bc95b684cd82e82c55eb0205a9))
* **Imports:** affiche le format "excel" pour tous les imports ([#6063](https://github.com/betagouv/ma-cantine/issues/6063)) ([e16e155](https://github.com/betagouv/ma-cantine/commit/e16e1551d1193221c5e3e527cef160942eb3acbc))
* **Imports:** corrige des erreurs de formats des cellules d'Excel et autorise les majuscule dans le nom de colonnes ([#6065](https://github.com/betagouv/ma-cantine/issues/6065)) ([bcb7296](https://github.com/betagouv/ma-cantine/commit/bcb72961129eaebae7509bfa43941f89536bfc6d))
* **Télédéclaration:** Affiche le champ "Service proposé" ([#6060](https://github.com/betagouv/ma-cantine/issues/6060)) ([46135ee](https://github.com/betagouv/ma-cantine/commit/46135ee82a4b9d9a13a61c58fbe975b13c7a5ebb))


### Technique

* **Imports:** homogénéiser le nommage des views & tests ([#6052](https://github.com/betagouv/ma-cantine/issues/6052)) ([e7c858a](https://github.com/betagouv/ma-cantine/commit/e7c858a193c7f4ed0815d7ae1d736392e906f0a0))
* **Validata:** faire un peu le ménage dans les erreurs remontées ([#6050](https://github.com/betagouv/ma-cantine/issues/6050)) ([1a3f4a9](https://github.com/betagouv/ma-cantine/commit/1a3f4a9e25c95f6d8ac37fc37252524745d02df2))


### Documentation

* **Télédéclaration:** ajout d'un serializer pour l'endpoint campaign dates ([#6026](https://github.com/betagouv/ma-cantine/issues/6026)) ([efeb9b8](https://github.com/betagouv/ma-cantine/commit/efeb9b8c8d0d4de4107788dbf4c176d30bbef9a0))

## [2025.45.1](https://github.com/betagouv/ma-cantine/compare/v2025.45.0...v2025.45.1) (2025-12-19)


### Corrections (bugs, typos...)

* **Achats:** rend le champ caractéristique optionnel ([#6055](https://github.com/betagouv/ma-cantine/issues/6055)) ([029016a](https://github.com/betagouv/ma-cantine/commit/029016a8b82d7524fb2f3d9f085e14cbdf75aaa2))

## [2025.45.0](https://github.com/betagouv/ma-cantine/compare/v2025.44.0...v2025.45.0) (2025-12-17)


### Nouveautés

* **Achats:** Formulaire: rend les champs familles et caractéristiques obligatoires ([#6048](https://github.com/betagouv/ma-cantine/issues/6048)) ([d89fb3a](https://github.com/betagouv/ma-cantine/commit/d89fb3a53bb93bc5061cbcacab2542169a9af828))
* **Imports:** ajouter une prévisualisation de fichiers d'exemples valide et non-valide ([#6040](https://github.com/betagouv/ma-cantine/issues/6040)) ([51a5f31](https://github.com/betagouv/ma-cantine/commit/51a5f31aead62180c0fd4fdeb54ca809dd4ee4af))


### Améliorations

* **Achats:** renomme 'DEPARTMENT' en 'DEPARTEMENT' ([#6042](https://github.com/betagouv/ma-cantine/issues/6042)) ([cd76d2f](https://github.com/betagouv/ma-cantine/commit/cd76d2ff3281a322a1cf5f7445ad4aa3d466c67b))
* **Gaspillage alimentaire:** champ nombre de repas devient un champ libre ([#6044](https://github.com/betagouv/ma-cantine/issues/6044)) ([11fa0e7](https://github.com/betagouv/ma-cantine/commit/11fa0e734cd54e46881b434336bf3c910bdff4c7))
* **Imports:** Achats: rendre le champ caracteristiques obligatoire ([#6039](https://github.com/betagouv/ma-cantine/issues/6039)) ([c6c999e](https://github.com/betagouv/ma-cantine/commit/c6c999e42088b03da319981bcc8f7babe0fabdf8))
* **Tableur excel:** supprime le tableur obsolète ([#6047](https://github.com/betagouv/ma-cantine/issues/6047)) ([7c6eb2f](https://github.com/betagouv/ma-cantine/commit/7c6eb2f98a695e6eaa1a14cab986384ebab0c386))


### Corrections (bugs, typos...)

* **Télédéclaration:** ré-organise les icones EGalim et commerce équitable ([#6041](https://github.com/betagouv/ma-cantine/issues/6041)) ([f9bb794](https://github.com/betagouv/ma-cantine/commit/f9bb794680cf4151cf17f412891b4105edb7b741))


### Technique

* évite d'avoir en parallèle plusieurs Github Actions de test pour la même PR ([#6043](https://github.com/betagouv/ma-cantine/issues/6043)) ([f9fea13](https://github.com/betagouv/ma-cantine/commit/f9fea13d11c6f12de98b57b45c71b8c3eb373ef2))


### Documentation

* améliore la lisibilité des settings. documente la facon actuelle de lancer nos tests ([#6037](https://github.com/betagouv/ma-cantine/issues/6037)) ([846434c](https://github.com/betagouv/ma-cantine/commit/846434cfdb7deb332360eb312f06d86dbb724dc3))

## [2025.44.0](https://github.com/betagouv/ma-cantine/compare/v2025.43.0...v2025.44.0) (2025-12-16)


### Nouveautés

* **Import:** Cantines: remplacer les valeurs anglaises par leur version "verbeuse" française ([#6012](https://github.com/betagouv/ma-cantine/issues/6012)) ([dbe634f](https://github.com/betagouv/ma-cantine/commit/dbe634f975ea57ae9adf14cc5e570c509ecd42a3))
* **Imports:** Cantines: autorise les valeurs en anglais à l'import sans les afficher aux utilisateurs ([#6016](https://github.com/betagouv/ma-cantine/issues/6016)) ([793e9ce](https://github.com/betagouv/ma-cantine/commit/793e9ce0f63e2e71c6a7a98e0f3ca4cf1304a7c7))
* **Imports:** Cantines: supprime le type "Cuisine centrale et site" ([#6019](https://github.com/betagouv/ma-cantine/issues/6019)) ([a895264](https://github.com/betagouv/ma-cantine/commit/a895264ea5ba41580e70cdc6cf124eb9eb778831))


### Améliorations

* **Imports:** Achats: rendre le champ "famille_produits" obligatoire ([#5985](https://github.com/betagouv/ma-cantine/issues/5985)) ([c8c7c6a](https://github.com/betagouv/ma-cantine/commit/c8c7c6ad43bf8ff87f3c54e3dc70a359f6aba847))
* **Imports:** Cantines: amélioration des terminologies du schéma ([#5998](https://github.com/betagouv/ma-cantine/issues/5998)) ([28ee396](https://github.com/betagouv/ma-cantine/commit/28ee396bcdbac39ca58e67adb56918a94373ae7e))
* **Imports:** Schémas: rendre dynamique l'URL en fonction de la branche git ([#6033](https://github.com/betagouv/ma-cantine/issues/6033)) ([eb71955](https://github.com/betagouv/ma-cantine/commit/eb719555faacfdfa2968e4ce9753b3eafacbb173))


### Corrections (bugs, typos...)

* **CI:** lancer la suite de tests seulement à l'ouverture de la PR (fix 'on') ([#6032](https://github.com/betagouv/ma-cantine/issues/6032)) ([64dd905](https://github.com/betagouv/ma-cantine/commit/64dd905613a26a8b1b1c796ce8806f8a92daa897))
* **Imports:** Cantines: met à jour le fichier démo ([#6021](https://github.com/betagouv/ma-cantine/issues/6021)) ([0c82ac8](https://github.com/betagouv/ma-cantine/commit/0c82ac8a7315446cd1cf4d230c9f9e593ed54133))
* **Imports:** Cantines: supprime du fichier d'exemple le SIRET commençant par un zéro ([#6035](https://github.com/betagouv/ma-cantine/issues/6035)) ([fd7b312](https://github.com/betagouv/ma-cantine/commit/fd7b312cf8046a321f8119324fa75c7332e3976a))
* **Télédéclaration:** répare un test suite au bump de la version de la TD à 16 ([#6030](https://github.com/betagouv/ma-cantine/issues/6030)) ([429ec03](https://github.com/betagouv/ma-cantine/commit/429ec03921754bfb872b774c733c803abc787c25))


### Technique

* **CI:** permet à la variable "GIT_BRANCH" d'être une config d'environnement ([#6038](https://github.com/betagouv/ma-cantine/issues/6038)) ([de1dea9](https://github.com/betagouv/ma-cantine/commit/de1dea9f83a0c58e987aac190befe4bd39e23d35))


### Documentation

* **Télédéclaration:** bump à la version 16. Lister les changements ([#6005](https://github.com/betagouv/ma-cantine/issues/6005)) ([1e2eb17](https://github.com/betagouv/ma-cantine/commit/1e2eb1792f2d6c7812d34720ef264ff0521d8f98))

## [2025.43.0](https://github.com/betagouv/ma-cantine/compare/v2025.42.1...v2025.43.0) (2025-12-12)


### Nouveautés

* **Ressources:** ajout du support webinaire ([#6014](https://github.com/betagouv/ma-cantine/issues/6014)) ([562c413](https://github.com/betagouv/ma-cantine/commit/562c413ad692f70c57cbb4d9d048ffbc0b2b6f27))


### Améliorations

* **Achats:** Admin: accélérer le chargement ([#5983](https://github.com/betagouv/ma-cantine/issues/5983)) ([de1e87e](https://github.com/betagouv/ma-cantine/commit/de1e87e43e956aff11851c27fe99b03f0fadc1d7))
* **Achats:** Règles métiers: au moment du save, vérifier les règles de bases ([#5984](https://github.com/betagouv/ma-cantine/issues/5984)) ([81f209a](https://github.com/betagouv/ma-cantine/commit/81f209a3f4dc0de564ddafc8a8cc3d57cbe676f6))


### Corrections (bugs, typos...)

* **Cantines:** Affiche: répare l'affichage des données dans le cas de satellites qui ont TD mais pas leur centrale ([#6022](https://github.com/betagouv/ma-cantine/issues/6022)) ([6ece192](https://github.com/betagouv/ma-cantine/commit/6ece192c3247a70a009ff80fbbc806db026d62d1))
* **Trouver une cantine:** corrige les graphiques "taux télédéclaration" qui ne s'affichaient  ([#6018](https://github.com/betagouv/ma-cantine/issues/6018)) ([7520269](https://github.com/betagouv/ma-cantine/commit/7520269a4d07d3bad714dd768fdbe20624476e0f))


### Technique

* **Télédéclaration:** bouge la logique TD des Diagnostic dans un fichier séparé ([#6003](https://github.com/betagouv/ma-cantine/issues/6003)) ([d66f81e](https://github.com/betagouv/ma-cantine/commit/d66f81eb5c57ce8f0d76f434a26be6c51ca42146))

## [2025.42.1](https://github.com/betagouv/ma-cantine/compare/v2025.42.0...v2025.42.1) (2025-12-10)


### Améliorations

* **Cantines:** enlever le formulaire de contact sur la page vitrine de chaque cantine ([#5914](https://github.com/betagouv/ma-cantine/issues/5914)) ([b95a1d6](https://github.com/betagouv/ma-cantine/commit/b95a1d6c025e10acae0d1d7592a215143d1adfe3))


### Corrections (bugs, typos...)

* **CI:** corrige les tests en erreur de l'import diagnostic ([#6010](https://github.com/betagouv/ma-cantine/issues/6010)) ([e477ceb](https://github.com/betagouv/ma-cantine/commit/e477ceb673e1bb4880d2dcad560dff2989d20136))
* **Crisp:** supprime et remplace les références à l'ancienne url de documentation de Gitbook ([#6002](https://github.com/betagouv/ma-cantine/issues/6002)) ([81ba35a](https://github.com/betagouv/ma-cantine/commit/81ba35a271e1240ba244fb5466d8fe7321ee2c95))
* **Foire aux questions:** supprime la page ([#6007](https://github.com/betagouv/ma-cantine/issues/6007)) ([a52a4cd](https://github.com/betagouv/ma-cantine/commit/a52a4cdac9482c40fd6e1f010e8bba8c99158156))
* **Imports:** ouvre le centre de ressources dans un nouvel onglet ([#6000](https://github.com/betagouv/ma-cantine/issues/6000)) ([344ce52](https://github.com/betagouv/ma-cantine/commit/344ce524c78b255ffa7f9372d4d3ede2e84163a7))
* **Menu:** supprime le lien vers la page d'import des fichiers du sous-menu "Aide" ([#6008](https://github.com/betagouv/ma-cantine/issues/6008)) ([a2afeb6](https://github.com/betagouv/ma-cantine/commit/a2afeb6b70471410dc126a09fc2d0e60f20278c6))
* **Tableau de bord:** met à jour les tuiles de bas de page ([#6006](https://github.com/betagouv/ma-cantine/issues/6006)) ([caa6b02](https://github.com/betagouv/ma-cantine/commit/caa6b02944779fa86c407bd9cf05e588090bc28c))
* **Télédéclaration:** Justificatif: répare l'affichage des secteurs de la cantine ([#6009](https://github.com/betagouv/ma-cantine/issues/6009)) ([7fae2d5](https://github.com/betagouv/ma-cantine/commit/7fae2d58c5d0c782700d35ad62a746a249b319f8))
* **Webinaires:** mise à jour de la page ([#6004](https://github.com/betagouv/ma-cantine/issues/6004)) ([a83d3e8](https://github.com/betagouv/ma-cantine/commit/a83d3e8eec480a7a7e11cd9b750a60641cc0a543))

## [2025.42.0](https://github.com/betagouv/ma-cantine/compare/v2025.41.1...v2025.42.0) (2025-12-09)


### Nouveautés

* **Ressources:** ajout de l'infographie de l'ademe sur le gaspillage ([#5970](https://github.com/betagouv/ma-cantine/issues/5970)) ([53aac73](https://github.com/betagouv/ma-cantine/commit/53aac732809526764e9730896d8d8c8127458540))
* **Télédéclaration:** affiche le coût des denrées dans le tunnel "Appro" ([#5991](https://github.com/betagouv/ma-cantine/issues/5991)) ([3cf8cc7](https://github.com/betagouv/ma-cantine/commit/3cf8cc743ff809f3f5d5236a63d09b3b59f1fb64))
* **Télédéclaration:** afficher les nouveaux champs de la TD détaillée hors-tunnel ([#5973](https://github.com/betagouv/ma-cantine/issues/5973)) ([6018b0c](https://github.com/betagouv/ma-cantine/commit/6018b0c3ba68e20fdb583db49c7b00fc61db2e9d))
* **Télédéclaration:** ajoute le remplissage automatique à partir des achats pour les catégories bio + commerce équitable ([#5980](https://github.com/betagouv/ma-cantine/issues/5980)) ([46f6e01](https://github.com/betagouv/ma-cantine/commit/46f6e01a39927d6de60c9c53ee025c4994d4c19f))
* **Télédéclaration:** ajoute les champs du commerce équitable dans l'étape bio ([#5972](https://github.com/betagouv/ma-cantine/issues/5972)) ([3537161](https://github.com/betagouv/ma-cantine/commit/353716120e604bff3f6e24b70fc35cddc4d020af))
* **Télédéclaration:** branche la correction d'un bilan et l'affichage dynamique une fois le bilan télédéclaré ([#5992](https://github.com/betagouv/ma-cantine/issues/5992)) ([4c6a632](https://github.com/betagouv/ma-cantine/commit/4c6a632aa1ef5aaa31204b59c546d58c5e74a268))
* **Télédéclaration:** rend obligatoire des champs de la TD détaillée ([#5969](https://github.com/betagouv/ma-cantine/issues/5969)) ([de76751](https://github.com/betagouv/ma-cantine/commit/de7675167eb85ca18b7fff793ba943eacbba2459))


### Améliorations

* **Admin:** ré-afficher la gestion des groupes d'utilisateurs ([#5967](https://github.com/betagouv/ma-cantine/issues/5967)) ([9dc4a26](https://github.com/betagouv/ma-cantine/commit/9dc4a26bb823dc28dc79207537a277101d591631))
* **Télédéclaration:** améliore le parcours entre les pages "Bilan" et "Modifier ma cantine" ([#5993](https://github.com/betagouv/ma-cantine/issues/5993)) ([0ebd29d](https://github.com/betagouv/ma-cantine/commit/0ebd29dfa2ff65b5dcae903047006d68af9c7e5f))
* **Télédéclaration:** améliore les catégories "dont origine France" de la TD détaillée ([#5987](https://github.com/betagouv/ma-cantine/issues/5987)) ([8f5d940](https://github.com/betagouv/ma-cantine/commit/8f5d94089af067a5a08d621efbca5b1868c677fc))
* **Télédéclaration:** au remplissage automatique depuis les achats autorise les valeurs vides pour les champs non obligatoires ([#5975](https://github.com/betagouv/ma-cantine/issues/5975)) ([0c5f718](https://github.com/betagouv/ma-cantine/commit/0c5f71812edc95e2b9c71908b88223ca4f49a4a7))
* **Télédéclaration:** mise à jour des terminologies ([#5974](https://github.com/betagouv/ma-cantine/issues/5974)) ([71321f0](https://github.com/betagouv/ma-cantine/commit/71321f098102eb15341b30e010c882c0d04f9723))
* **Télédéclaration:** nouvel endpoint coté Diagnostic pour annuler une télédéclaration ([#5989](https://github.com/betagouv/ma-cantine/issues/5989)) ([e1b7044](https://github.com/betagouv/ma-cantine/commit/e1b704424f5acc4ae7fbf2e68bcf2ddf4a720f94))
* **Télédéclaration:** nouvel endpoint coté Diagnostic pour télédéclarer ([#5981](https://github.com/betagouv/ma-cantine/issues/5981)) ([d451100](https://github.com/betagouv/ma-cantine/commit/d4511005e81a37ef9a4f492bca7f5d2667eb9843))


### Corrections (bugs, typos...)

* **Télédéclaration:** ajoute les nouveaux champs dans les totaux provenant des achats ([#5976](https://github.com/betagouv/ma-cantine/issues/5976)) ([3866fdd](https://github.com/betagouv/ma-cantine/commit/3866fddc84feccfca9d5dedadd69e9f8f0151bc2))
* **Télédéclaration:** branche le bouton "Télédéclarer" sur la nouvelle route api ([#5986](https://github.com/betagouv/ma-cantine/issues/5986)) ([2ed5e90](https://github.com/betagouv/ma-cantine/commit/2ed5e9008f201d290cbf7e9f88b4f9a0c17edd68))
* **Télédéclaration:** calculer les actions 'Télédéclaré' sur la table Diagnostic ([#5988](https://github.com/betagouv/ma-cantine/issues/5988)) ([f86eb39](https://github.com/betagouv/ma-cantine/commit/f86eb39001871db5ce4d3459d1cd6ee58b8cfe1e))
* **Télédéclaration:** corrige l'erreur de variable inconnue ([#5968](https://github.com/betagouv/ma-cantine/issues/5968)) ([d20adf5](https://github.com/betagouv/ma-cantine/commit/d20adf595d918a1cfdb672ea37b18571b42166f3))
* **Télédéclaration:** recettage (plusieurs corrections) ([#5994](https://github.com/betagouv/ma-cantine/issues/5994)) ([ec1d2cc](https://github.com/betagouv/ma-cantine/commit/ec1d2cc0e2491860b0bb94ef0d06802546996f56))
* **Télédéclaration:** rend obligatoire l'étape 'choix du mode de saisie' (simplifiée ou détaillée) ([#5978](https://github.com/betagouv/ma-cantine/issues/5978)) ([4bbcb98](https://github.com/betagouv/ma-cantine/commit/4bbcb989f7de77ab34ef705f1bd1e3bab02737ea))


### Technique

* **Achats:** réorganise les tests (list / get / create / update / delete) ([#5977](https://github.com/betagouv/ma-cantine/issues/5977)) ([79215b7](https://github.com/betagouv/ma-cantine/commit/79215b7b14cb45aa6fdfea889c0548a986adb3ba))
* **API:** enlever les camelize et JSONResponse inutiles ([#5909](https://github.com/betagouv/ma-cantine/issues/5909)) ([d4f79d1](https://github.com/betagouv/ma-cantine/commit/d4f79d14c6b22f37c4a436709e76279a7f698df7))
* **API:** généraliser l'usage de PATCH (au lieu de PUT) pour la modification ([#5966](https://github.com/betagouv/ma-cantine/issues/5966)) ([9eefdca](https://github.com/betagouv/ma-cantine/commit/9eefdca59a370dcda304725150c36bc9eaa694c9))
* **Diagnostics:** réorgnise les tests (create / update) ([#5979](https://github.com/betagouv/ma-cantine/issues/5979)) ([ccd8451](https://github.com/betagouv/ma-cantine/commit/ccd8451bf489cad1dea2be431177db732f208c1f))
* **Télédéclaration:** ajoute les règles métiers "remplie" sur les TD simplifiée et détaillée (et sépare avant/après 2025) ([#5960](https://github.com/betagouv/ma-cantine/issues/5960)) ([8c82094](https://github.com/betagouv/ma-cantine/commit/8c82094728a85f84469e77dc6c91b3a5d8e086b8))
* **Télédéclaration:** renomme le nouvel endpoint de création de TD en '/teledeclaration/create' ([#5990](https://github.com/betagouv/ma-cantine/issues/5990)) ([ab35213](https://github.com/betagouv/ma-cantine/commit/ab352130348bff8651950078ea80e32e27c1f60b))
* **Télédéclaration:** supprime les anciennes URL de création et annulation de TD ([#5996](https://github.com/betagouv/ma-cantine/issues/5996)) ([d2952a8](https://github.com/betagouv/ma-cantine/commit/d2952a820804a4d38b6d89a9f7c3ac74d10b8265))

## [2025.41.1](https://github.com/betagouv/ma-cantine/compare/v2025.41.0...v2025.41.1) (2025-12-03)


### Améliorations

* **Evaluation Gaspillage:** API: les rendre visible dans le swagger et permettre aux éditeurs de les créer & modifier ([#5962](https://github.com/betagouv/ma-cantine/issues/5962)) ([0fdb8ae](https://github.com/betagouv/ma-cantine/commit/0fdb8ae202ce100c24221361185eb502c380536b))


### Technique

* **deps:** bump django from 5.1.14 to 5.1.15 ([#5964](https://github.com/betagouv/ma-cantine/issues/5964)) ([73f3b2a](https://github.com/betagouv/ma-cantine/commit/73f3b2a9bebd9c8572859b85db00ea589a2a7aed))
* **Télédéclaration:** renomme 'short_distribution' en 'circuit_court' ([#5965](https://github.com/betagouv/ma-cantine/issues/5965)) ([b787b2a](https://github.com/betagouv/ma-cantine/commit/b787b2adabdbd8354e51035ba46779bfe610fbdf))

## [2025.41.0](https://github.com/betagouv/ma-cantine/compare/v2025.40.0...v2025.41.0) (2025-12-03)


### Nouveautés

* **Bandeau information:** ajout d'un bandeau d'information pour communiquer globalement sur le site ([#5791](https://github.com/betagouv/ma-cantine/issues/5791)) ([51daa3b](https://github.com/betagouv/ma-cantine/commit/51daa3b0d8fe759a7e3128d631ffcead98d4c1e1))
* **Télédéclaration:** affiche les nouveaux champs dans les informations du bilan à télédéclarer ([#5922](https://github.com/betagouv/ma-cantine/issues/5922)) ([ae1a865](https://github.com/betagouv/ma-cantine/commit/ae1a86537a0c1bd876ad3849ea0cfdade16277e8))
* **Télédéclaration:** ajout de l'étape "origine France" dans le tunnel ([#5898](https://github.com/betagouv/ma-cantine/issues/5898)) ([6fd56ef](https://github.com/betagouv/ma-cantine/commit/6fd56ef724504d84dfc383474aa6d84d99da4113))
* **Télédéclaration:** ajout des champs "Dont commerce équitable" (tunnel simplifiée) ([#5921](https://github.com/betagouv/ma-cantine/issues/5921)) ([b0da757](https://github.com/betagouv/ma-cantine/commit/b0da7570cc72210d77802c0d4bdf32d9fb5fad13))
* **Télédéclaration:** ajout du champ "produits de la mer et de l’aquaculture origine France" ([#5919](https://github.com/betagouv/ma-cantine/issues/5919)) ([be4caae](https://github.com/betagouv/ma-cantine/commit/be4caae317bb990ce0f4c2a9bd2a334b422d6b88))
* **Télédéclaration:** des champs deviennent obligatoires ([#5897](https://github.com/betagouv/ma-cantine/issues/5897)) ([68a1a4e](https://github.com/betagouv/ma-cantine/commit/68a1a4e45856800b7fc57525d9836d871fc83144))


### Améliorations

* **Diagnostic:** créer les nouveaux champs 'dont commerce équitable' (bilans simplifiés et détaillés) ([#5907](https://github.com/betagouv/ma-cantine/issues/5907)) ([039321b](https://github.com/betagouv/ma-cantine/commit/039321b07ac130ab1dd7701c91eff3119eb579c8))
* **Télédéclaration:** ajouter les dates de campagne 2026 dans le code ([#5913](https://github.com/betagouv/ma-cantine/issues/5913)) ([9e5eb15](https://github.com/betagouv/ma-cantine/commit/9e5eb157a8b9dbac4444eb8e730b6dd884c3d205))
* **Télédéclaration:** homogénéisation du vocabulaire (origine France et Produits de la mer) ([#5920](https://github.com/betagouv/ma-cantine/issues/5920)) ([2185f38](https://github.com/betagouv/ma-cantine/commit/2185f38bbfc3cf40f8348f67f4f37ccdc859bfa7))
* **Télédéclaration:** met à jour les descriptions des champs (origine france, qq descriptions) ([#5900](https://github.com/betagouv/ma-cantine/issues/5900)) ([5580e21](https://github.com/betagouv/ma-cantine/commit/5580e21f833c84a9fb6670b2cf27d17c528d013d))


### Corrections (bugs, typos...)

* **Télédéclaration:** maj des actions suite aux changements sur les champs obligatoires ([#5952](https://github.com/betagouv/ma-cantine/issues/5952)) ([528f8b7](https://github.com/betagouv/ma-cantine/commit/528f8b7014c7c0cc6e0938fe02b8b64dd3f72cfa))
* **Télédéclaration:** mise à jour des terminologies suite au recettage de la télédéclaration simplifiée ([#5957](https://github.com/betagouv/ma-cantine/issues/5957)) ([37a8ea4](https://github.com/betagouv/ma-cantine/commit/37a8ea4551cb0ac03daf1cf5d7e6f337efa50891))
* **Télédéclaration:** renommer le champ value_egalim_others_dont_commerce_equitable_ht ([#5951](https://github.com/betagouv/ma-cantine/issues/5951)) ([e96e396](https://github.com/betagouv/ma-cantine/commit/e96e39624feb2ae9f464cf69d57c5d10122bbca4))
* **Télédéclaration:** répare un test suite au changement vers 'provenance France' ([#5955](https://github.com/betagouv/ma-cantine/issues/5955)) ([1a46800](https://github.com/betagouv/ma-cantine/commit/1a468009a88593b91cbfb15c35d86709770611c6))
* **Télédéclarations:** réparer les tests avant MEP ([#5961](https://github.com/betagouv/ma-cantine/issues/5961)) ([8812bd0](https://github.com/betagouv/ma-cantine/commit/8812bd01e514c90bcd05923255414683da55b0fc))
* **Télédéclarations:** Tunnel simplifié: répare le pré-remplissage à partir des achats ([#5950](https://github.com/betagouv/ma-cantine/issues/5950)) ([ee40c81](https://github.com/betagouv/ma-cantine/commit/ee40c81d52a6e9f9f6189f94d21d408c7cdc522d))
* **Télédéclaration:** Tunnel simplifié: corrige la sauvegarde des nouvelles valeurs ([#5949](https://github.com/betagouv/ma-cantine/issues/5949)) ([b70787d](https://github.com/betagouv/ma-cantine/commit/b70787d82fc0443c3774a1c66fb14374ade1d909))


### Technique

* **Diagnostic:** clean du modèle avant d'ajouter les nouveaux champs ([#5906](https://github.com/betagouv/ma-cantine/issues/5906)) ([865da2e](https://github.com/betagouv/ma-cantine/commit/865da2e268bfb6f6b69f89e2c43b5cd5369d0f5f))
* **Télédéclaration:** API: supprime les serializers plus utilisés ([#5958](https://github.com/betagouv/ma-cantine/issues/5958)) ([09ffda7](https://github.com/betagouv/ma-cantine/commit/09ffda7a4971ffaf7fdeb16379ec5af125c0f80a))
* **Télédéclaration:** clarifier les champs (1/3): meat & fish deviennent viandes_volailles et produits_de_la_mer. Enlever _ht ([#5953](https://github.com/betagouv/ma-cantine/issues/5953)) ([329f56c](https://github.com/betagouv/ma-cantine/commit/329f56c6a2a48e849bc71b82f7e21a468d20e5c3))
* **Télédéclaration:** clarifier les champs (2/3): renommer les autres champs en français. Enlever _ht ([#5956](https://github.com/betagouv/ma-cantine/issues/5956)) ([62f15b6](https://github.com/betagouv/ma-cantine/commit/62f15b67e5bd3ca7a33bac09fd07a5daec198a06))
* **Télédéclaration:** clarifier les champs (3/3): renommer 'value' en 'valeur' ([#5959](https://github.com/betagouv/ma-cantine/issues/5959)) ([49f7558](https://github.com/betagouv/ma-cantine/commit/49f755829990de4ee239475b32e9d09e9b5eaf3c))
* **Tests:** enlever les warning min_value ou max_value 'should be a Decimal instance' ([#5917](https://github.com/betagouv/ma-cantine/issues/5917)) ([2421667](https://github.com/betagouv/ma-cantine/commit/2421667df1d02df3434d33db319cf22c0f1a2f61))

## [2025.40.0](https://github.com/betagouv/ma-cantine/compare/v2025.39.1...v2025.40.0) (2025-12-01)


### Nouveautés

* **Secteurs:** utilise le nouveau champ secteur dans le frontend ([#5915](https://github.com/betagouv/ma-cantine/issues/5915)) ([ce9255c](https://github.com/betagouv/ma-cantine/commit/ce9255c9155681a1b767c7acf4e5a025112038ec))


### Améliorations

* **Cantines:** migrer le champ 'secteurs' d'une relation (M2M) vers un champ liste (ArrayField) [1/2] ([#5886](https://github.com/betagouv/ma-cantine/issues/5886)) ([f88bdf4](https://github.com/betagouv/ma-cantine/commit/f88bdf4c20b95782e64f8a17475f0d6992c9a8d6))
* **Cantines:** Règles métiers: ajouter les contraintes sur les secteurs ([#5895](https://github.com/betagouv/ma-cantine/issues/5895)) ([f6f7a46](https://github.com/betagouv/ma-cantine/commit/f6f7a46a83fddd7abb961cd379cb44b6b4138452))
* **Ressources:** ajoute 4 documents ([#5923](https://github.com/betagouv/ma-cantine/issues/5923)) ([3888d0d](https://github.com/betagouv/ma-cantine/commit/3888d0dfac95190833bb86019009d540454b5db3))


### Corrections (bugs, typos...)

* **API Stats:** corrige les stats 'inconnu' suite aux changements sur les secteurs ([#5908](https://github.com/betagouv/ma-cantine/issues/5908)) ([ef0daf4](https://github.com/betagouv/ma-cantine/commit/ef0daf488d651b7369118f9da7de0cf5d11c9452))
* **CI:** remplacer 'npm install' par 'npm ci' pour les instances déployées ([#5911](https://github.com/betagouv/ma-cantine/issues/5911)) ([3f8d4b1](https://github.com/betagouv/ma-cantine/commit/3f8d4b14eee5d2214511eb730edf1ad07576a3ed))
* **Tests:** répare un test sur les exports open_data qui échoue régulièrement ([#5905](https://github.com/betagouv/ma-cantine/issues/5905)) ([c93747a](https://github.com/betagouv/ma-cantine/commit/c93747ac2a586814ed88fdac9764def6cf6a4f37))
* **Tests:** s'assurer qu'il n'y a pas d'emails générés en double ([#5901](https://github.com/betagouv/ma-cantine/issues/5901)) ([ae0ddaf](https://github.com/betagouv/ma-cantine/commit/ae0ddaf81106fda3225af5d06ba5e63b03bb1138))


### Technique

* **API:** enlever l'endpoint 'canteenLocations' qui n'est pas utilisé ([#5910](https://github.com/betagouv/ma-cantine/issues/5910)) ([ad39192](https://github.com/betagouv/ma-cantine/commit/ad391924c4d9f0d16df42e70d550282bc0a3d1ad))
* **API:** Ministères de tutelle: améliorer la documentation ([#5903](https://github.com/betagouv/ma-cantine/issues/5903)) ([4c7f804](https://github.com/betagouv/ma-cantine/commit/4c7f804a3793d5f31fdcfda18fbbfd55ee16861e))
* **API:** Secteurs: renvoyer la liste à partir des enum (et non du M2M) ([#5902](https://github.com/betagouv/ma-cantine/issues/5902)) ([12733a8](https://github.com/betagouv/ma-cantine/commit/12733a81588f82ab2e1c9272964cf7fab333708e))
* **Securité:** dependabot: rajouter un cooldown de 7 jours ([#5925](https://github.com/betagouv/ma-cantine/issues/5925)) ([509cdff](https://github.com/betagouv/ma-cantine/commit/509cdffdcab8ae36e9bc9a1ea0a5701a557f4754))
* **Sécurité:** npm: utiliser le flag ignore-scripts (protection Shai-Hulud) ([#5924](https://github.com/betagouv/ma-cantine/issues/5924)) ([94c6dd1](https://github.com/betagouv/ma-cantine/commit/94c6dd1fc5e1ae90925e3751426775ab08b89ad3))
* **Tests:** remplacer Factory.create() par Factory() ([#5916](https://github.com/betagouv/ma-cantine/issues/5916)) ([cc6968c](https://github.com/betagouv/ma-cantine/commit/cc6968c61f858f461eae48c7b6800cb964543136))

## [2025.39.1](https://github.com/betagouv/ma-cantine/compare/v2025.39.0...v2025.39.1) (2025-11-18)


### Améliorations

* **Cantines:** Règles métiers: enlever les contraintes sur le siret de la CC ([#5884](https://github.com/betagouv/ma-cantine/issues/5884)) ([b457b36](https://github.com/betagouv/ma-cantine/commit/b457b363220c1e722bba82ae22e91ee4892392ac))
* **Cantines:** supprime le sélecteur de cuisine centrale ([#5891](https://github.com/betagouv/ma-cantine/issues/5891)) ([46227aa](https://github.com/betagouv/ma-cantine/commit/46227aa86c11c4bd6ad9fca5d0f0ec2bbb133c72))
* **Tableau de bord:** multiples améliorations ([#5888](https://github.com/betagouv/ma-cantine/issues/5888)) ([1267809](https://github.com/betagouv/ma-cantine/commit/12678094e042059375ededb24328154e3081d8cd))


### Corrections (bugs, typos...)

* **Données personnelles:** homogénéise le nom de la plateforme ([#5889](https://github.com/betagouv/ma-cantine/issues/5889)) ([fce131a](https://github.com/betagouv/ma-cantine/commit/fce131ac7f3fe37eede7f09814d62a1527e3ab0e))
* **Observatoire:** répare la stat 'viande & aquaculture EGalim' ([#5893](https://github.com/betagouv/ma-cantine/issues/5893)) ([fcb8fae](https://github.com/betagouv/ma-cantine/commit/fcb8faea41e1b013fbced3ebe0adbd86110dda7d))
* **Secteurs:** API: répare un bug sur le swagger suite au récent renommage ([#5892](https://github.com/betagouv/ma-cantine/issues/5892)) ([a828b51](https://github.com/betagouv/ma-cantine/commit/a828b518d5d27b54be97d8988d567f3cac9f3218))


### Technique

* **Secteurs:** créer les enum dans le code à partir des données présentes en DB ([#5878](https://github.com/betagouv/ma-cantine/issues/5878)) ([0069f23](https://github.com/betagouv/ma-cantine/commit/0069f2347d35b8fbd7d1e588f3ae21b5143f4f7b))

## [2025.39.0](https://github.com/betagouv/ma-cantine/compare/v2025.38.0...v2025.39.0) (2025-11-14)


### Nouveautés

* **Badge:** ajoute le nouvel affichage du badge en vue2 ([#5883](https://github.com/betagouv/ma-cantine/issues/5883)) ([5acddcd](https://github.com/betagouv/ma-cantine/commit/5acddcd96e83ec543f9074727dd67ce342956c58))
* **Comprendre mes obligation:** remplace la page par le contenu récupéré depuis Crisp ([#5505](https://github.com/betagouv/ma-cantine/issues/5505)) ([87ec4cc](https://github.com/betagouv/ma-cantine/commit/87ec4cc0c0577512723184b1c67e703e3577b77b))
* **Tableu de bord:** ajout du bouton "Je donne mon avis" ([#5874](https://github.com/betagouv/ma-cantine/issues/5874)) ([a7ca3cd](https://github.com/betagouv/ma-cantine/commit/a7ca3cdfd1e821b37086fa8009115e51510cd85c))


### Améliorations

* **Imports bilan:** suppression des pages en attendant leur mise à jour  ([#5873](https://github.com/betagouv/ma-cantine/issues/5873)) ([fb2799b](https://github.com/betagouv/ma-cantine/commit/fb2799b3a9cfe016c7ac6be9c220712a47259967))
* **Imports:** simplification de la page tampon ([#5870](https://github.com/betagouv/ma-cantine/issues/5870)) ([fd6ac98](https://github.com/betagouv/ma-cantine/commit/fd6ac985df6eff65d0a88c58db071c3b1ab7fc10))
* **Tableau de bord:** mise en avant des tuiles ([#5882](https://github.com/betagouv/ma-cantine/issues/5882)) ([132d0aa](https://github.com/betagouv/ma-cantine/commit/132d0aaccddaf4d05cd433d27ebf0822a338370b))
* **Tableau de bord:** ré-organisation des colonnes "Statut" et "Actions" pour regrouper dans "Télédéclaration" ([#5877](https://github.com/betagouv/ma-cantine/issues/5877)) ([8895310](https://github.com/betagouv/ma-cantine/commit/88953102d04c1f4e33eafca12b74866606865be2))
* **Tableau de bord:** simplification du badge ([#5881](https://github.com/betagouv/ma-cantine/issues/5881)) ([062eb3a](https://github.com/betagouv/ma-cantine/commit/062eb3af59b8efefa4b18079f715158d125b09e9))


### Corrections (bugs, typos...)

* **Tableau de bord:** renommer 'Créer une cantine' en 'Ajouter une cantine' pour homogénéiser ([#5885](https://github.com/betagouv/ma-cantine/issues/5885)) ([2b34a4d](https://github.com/betagouv/ma-cantine/commit/2b34a4d293ea677cbbffccb19bd60512ba588516))


### Technique

* **Admin:** basculer la liste des secteurs en lecture-seule ([#5875](https://github.com/betagouv/ma-cantine/issues/5875)) ([bcb09d6](https://github.com/betagouv/ma-cantine/commit/bcb09d69f849e8679c95cd0afd3c58098212fda4))
* bouge les CreationSource dans un fichier dédié ([#5880](https://github.com/betagouv/ma-cantine/issues/5880)) ([53939ff](https://github.com/betagouv/ma-cantine/commit/53939ffaba475c267184158943219c1be0e9e35f))
* Checker le linting de l'app Vue 3 + noms de tâches plus claires ([#5871](https://github.com/betagouv/ma-cantine/issues/5871)) ([e0978b7](https://github.com/betagouv/ma-cantine/commit/e0978b7be37f874a1fb233a37d9b8af4792aa65a))
* **Geo:** bouger les départements & les régions dans le même fichier ([#5879](https://github.com/betagouv/ma-cantine/issues/5879)) ([63ab776](https://github.com/betagouv/ma-cantine/commit/63ab7761a0f142a0aa834704bc9cf95bb48ac15b))
* **Secteurs:** renommer 'sectors' en 'sectors_m2m' ([#5876](https://github.com/betagouv/ma-cantine/issues/5876)) ([1ab566d](https://github.com/betagouv/ma-cantine/commit/1ab566dfd42e80b8c2a73108368d551ba0c4a400))

## [2025.38.0](https://github.com/betagouv/ma-cantine/compare/v2025.37.0...v2025.38.0) (2025-11-10)


### Nouveautés

* **Tableau de bord:** ajout du bouton d'action rapide ([#5862](https://github.com/betagouv/ma-cantine/issues/5862)) ([de67620](https://github.com/betagouv/ma-cantine/commit/de676207387eb7bbdfba71f6e9c21f051b8d6360))
* **Tableau de bord:** ajoute la barre de recherche ([#5863](https://github.com/betagouv/ma-cantine/issues/5863)) ([f6e1165](https://github.com/betagouv/ma-cantine/commit/f6e1165c589c1976555cc9180702eaf04eb59124))
* **Tableau de bord:** remplace l'ancienne page par la nouvelle ([#5866](https://github.com/betagouv/ma-cantine/issues/5866)) ([5c392ea](https://github.com/betagouv/ma-cantine/commit/5c392eaa673c9f99adfe281a3b2684f415e546bb))


### Améliorations

* **Accessibilité:** ajout du plugin 'eslint-plugin-vuejs-accessibility' pour détecter quelques erreurs de bases ([#5868](https://github.com/betagouv/ma-cantine/issues/5868)) ([c086e87](https://github.com/betagouv/ma-cantine/commit/c086e879f467de617cb3c52ba0fa24d1392a41d8))
* **Tableau de bord:** améliore le responsive, l'accessibilité et petite simplification de code ([#5864](https://github.com/betagouv/ma-cantine/issues/5864)) ([171942d](https://github.com/betagouv/ma-cantine/commit/171942dbe9fe8f2bc98c226220f879e1cb6e4e78))


### Corrections (bugs, typos...)

* **Tableau de bord:** corrige l'url du lien "Modifier la cantine" ([#5869](https://github.com/betagouv/ma-cantine/issues/5869)) ([55da84f](https://github.com/betagouv/ma-cantine/commit/55da84f4eefb6a77bdd577b198371c8a4598c9a0))
* **Tableau de bord:** multiples corrections suite au recettage ([#5867](https://github.com/betagouv/ma-cantine/issues/5867)) ([14a71a4](https://github.com/betagouv/ma-cantine/commit/14a71a4c485e4c7f3a54f33f824f72153cf1c791))

## [2025.37.0](https://github.com/betagouv/ma-cantine/compare/v2025.36.1...v2025.37.0) (2025-11-06)


### Nouveautés

* **Ressources:** ajout des documents de notre ancien support gitbook ([#5848](https://github.com/betagouv/ma-cantine/issues/5848)) ([691b199](https://github.com/betagouv/ma-cantine/commit/691b199191f7ea5ce0dd36c03ae5d41580529a57))
* **Tableau de bord:** ajout du bouton "Gérer mes cantines" ([#5853](https://github.com/betagouv/ma-cantine/issues/5853)) ([b49a39c](https://github.com/betagouv/ma-cantine/commit/b49a39c72d55d5ecd372467be435aa41434b1d9d))
* **Tableau de bord:** ajoute la pagination ([#5852](https://github.com/betagouv/ma-cantine/issues/5852)) ([f3cf800](https://github.com/betagouv/ma-cantine/commit/f3cf8000aa96c2d08b99e0d6e69d35ae2f5e8df0))


### Améliorations

* **Cantines:** Règles métiers: ajout des min sur daily_meal_count (3) & yearly_meal_count (420) ([#5847](https://github.com/betagouv/ma-cantine/issues/5847)) ([3175065](https://github.com/betagouv/ma-cantine/commit/31750657fbd78fd03f666de9423e2d01d2663514))
* **Cantines:** Règles métiers: rendre le champ siret unique (sur les cantines ouvertes) ([#5849](https://github.com/betagouv/ma-cantine/issues/5849)) ([2675442](https://github.com/betagouv/ma-cantine/commit/26754429bd1e98cde475685bc54694fce9ca5a93))
* **Création de cantines:** intégrer la vérification du nombre minimum de repas jours et annuels côté frontend  ([#5857](https://github.com/betagouv/ma-cantine/issues/5857)) ([3bfe964](https://github.com/betagouv/ma-cantine/commit/3bfe9645f545c74320f6afd2e9913ca415dc94cc))
* **Footer:** ajout d'un lien vers le code source ([#5861](https://github.com/betagouv/ma-cantine/issues/5861)) ([a531a66](https://github.com/betagouv/ma-cantine/commit/a531a66e7dc9faebc23c2ed4af81e4b18131308f))


### Corrections (bugs, typos...)

* **Ajouter une cantine:** modification du texte d'introduction ([#5854](https://github.com/betagouv/ma-cantine/issues/5854)) ([1fa3595](https://github.com/betagouv/ma-cantine/commit/1fa359567ab427de04fa38f22c5dc251ae744f4a))
* **Cantines:** Règles métiers: répare un test suite aux nouvelles contraintes sur le min des meal_count. ref [#5847](https://github.com/betagouv/ma-cantine/issues/5847) ([#5855](https://github.com/betagouv/ma-cantine/issues/5855)) ([c31becd](https://github.com/betagouv/ma-cantine/commit/c31becdf6a6476fccecdead52d2d928c7eddac60))
* **Formulaire de contact:** envoyer les emails au format text/html ([#5856](https://github.com/betagouv/ma-cantine/issues/5856)) ([e46cd39](https://github.com/betagouv/ma-cantine/commit/e46cd39bdfc2f27aebcf469de7e28b57da500aad))


### Technique

* **deps:** bump django from 5.1.13 to 5.1.14 ([#5860](https://github.com/betagouv/ma-cantine/issues/5860)) ([a63a92f](https://github.com/betagouv/ma-cantine/commit/a63a92fb7bfc4b68a5aaed3e4f031e48ce4e7b92))
* **Tests:** Cantines: réorganise les fichiers de tests pour en avoir 1 par endpoint ([#5845](https://github.com/betagouv/ma-cantine/issues/5845)) ([7d40390](https://github.com/betagouv/ma-cantine/commit/7d403908850cbf961e2a98e1135c16d3ef9175c2))
* **Tests:** Imports cantines: clean & ajout de tests 'model' (post-Validata) ([#5850](https://github.com/betagouv/ma-cantine/issues/5850)) ([6c1b433](https://github.com/betagouv/ma-cantine/commit/6c1b433d22941bf11dabdfae62410a8490785815))


### Documentation

* **README:** ajout de Crisp dans les outils ([#5859](https://github.com/betagouv/ma-cantine/issues/5859)) ([9f1173a](https://github.com/betagouv/ma-cantine/commit/9f1173a0003a9c7d4a47cf0687cd823ecdeac924))
* **README:** on ne se sert plus d'ELK (Elastic & Kibana) ([#5858](https://github.com/betagouv/ma-cantine/issues/5858)) ([ac001ac](https://github.com/betagouv/ma-cantine/commit/ac001ac5eef99b61ba1487b8bf7f6e55a0e57810))

## [2025.36.1](https://github.com/betagouv/ma-cantine/compare/v2025.36.0...v2025.36.1) (2025-11-03)


### Améliorations

* **Imports:** Cantines: enlève les champs city_insee_code & postal_code ([#5833](https://github.com/betagouv/ma-cantine/issues/5833)) ([008db4c](https://github.com/betagouv/ma-cantine/commit/008db4ce6fb16a58290b24e08d4435854273787f))


### Technique

* **Admin:** ne plus faire d'imports relatifs (utils, softdeletionadmin) ([#5836](https://github.com/betagouv/ma-cantine/issues/5836)) ([ca7ee60](https://github.com/betagouv/ma-cantine/commit/ca7ee60baab46fd5a7146c28aaab58976016fe85))
* **deps-dev:** ajout des mises à jour manquantes de dependabot ([#5844](https://github.com/betagouv/ma-cantine/issues/5844)) ([05e0611](https://github.com/betagouv/ma-cantine/commit/05e06114b8a90124f08c5c13edb88c3990823801))
* **deps-dev:** bump @rushstack/eslint-patch in /2024-frontend ([b62aa60](https://github.com/betagouv/ma-cantine/commit/b62aa60acb53cab4f5d078005f9167b124a66150))
* **deps-dev:** bump @vitejs/plugin-vue in /2024-frontend ([27f809f](https://github.com/betagouv/ma-cantine/commit/27f809f21490d62476bcdf11e5702126f09d5d6d))
* **deps-dev:** bump eslint from 9.32.0 to 9.39.0 in /2024-frontend ([8a04d23](https://github.com/betagouv/ma-cantine/commit/8a04d23a7aa981d2176a6bee761a86da79f70c14))
* **deps-dev:** bump prettier from 3.5.3 to 3.6.2 in /2024-frontend ([fb9739a](https://github.com/betagouv/ma-cantine/commit/fb9739a380fba5b06dc74e62f453377311802cbb))
* **deps-dev:** bump vite from 6.3.6 to 7.1.12 in /2024-frontend ([422166c](https://github.com/betagouv/ma-cantine/commit/422166c2b04b84d0a099456834ee29e28ea74082))
* **deps:** bump @gouvminint/vue-dsfr in /2024-frontend ([b19c448](https://github.com/betagouv/ma-cantine/commit/b19c448fcdedbc7c9563f60bcb7d904d791982b6))
* **deps:** bump django-vite-plugin from 4.1.0 to 4.1.2 ([cc17d4d](https://github.com/betagouv/ma-cantine/commit/cc17d4d7ae35303fa065788be3657fc8038b4a3c))
* **deps:** bump django-vite-plugin in /2024-frontend ([bd55d57](https://github.com/betagouv/ma-cantine/commit/bd55d5736b0594af6574200fa507186c660e5aec))
* **deps:** bump vue-router from 4.5.1 to 4.6.3 in /2024-frontend ([8934d3d](https://github.com/betagouv/ma-cantine/commit/8934d3d1bd3b67fa63f6986bd5fa35be4b4e5c30))
* **Diagnostic:** basculer les validations dans un fichier dédié ([#5832](https://github.com/betagouv/ma-cantine/issues/5832)) ([caa764c](https://github.com/betagouv/ma-cantine/commit/caa764c2659e910d40b2e759e37ad1be24ab7d0c))
* **Tests:** basculer 'assert_import_failure_created' dans utils ([#5834](https://github.com/betagouv/ma-cantine/issues/5834)) ([51da402](https://github.com/betagouv/ma-cantine/commit/51da4029ba3159045eabf9ca49fb3b1d8323a927))
* **Tests:** ne plus faire d'imports relatifs (utils) ([#5835](https://github.com/betagouv/ma-cantine/issues/5835)) ([7c7be4d](https://github.com/betagouv/ma-cantine/commit/7c7be4d5ed79aed6513ef280bc9ceda32e05fbbc))

## [2025.36.0](https://github.com/betagouv/ma-cantine/compare/v2025.35.0...v2025.36.0) (2025-10-31)


### Nouveautés

* **Tableau de bord:** ajout du menu déroulant "Paramètres" pour chaque ligne ([#5810](https://github.com/betagouv/ma-cantine/issues/5810)) ([94415f3](https://github.com/betagouv/ma-cantine/commit/94415f3a9b4b4492ef99752ede871c5fb10e458b))
* **Tableau de bord:** intégration de la vue tableau sans les actions ([#5808](https://github.com/betagouv/ma-cantine/issues/5808)) ([927bfca](https://github.com/betagouv/ma-cantine/commit/927bfca86521fe80e6b851f4896c0c4e8551681e))


### Améliorations

* **Cantines:** Règles métiers: règles spécifiques aux cantines satellites (siret CC doit appartenir à une cantine) (à la création) ([#5817](https://github.com/betagouv/ma-cantine/issues/5817)) ([c5899af](https://github.com/betagouv/ma-cantine/commit/c5899af4ed87333681a6d42c927d2d2822324406))
* **Cantines:** Règles métiers: règles spécifiques aux cantines satellites (siret CC doit appartenir à une centrale) (à la création)  ([#5800](https://github.com/betagouv/ma-cantine/issues/5800)) ([4ab63d2](https://github.com/betagouv/ma-cantine/commit/4ab63d2141160e42f12b5554bd074529eb4097c5))
* **Cantines:** Règles métiers: rendre le champ 'nombre de satellites' obligatoire si CC ([#5793](https://github.com/betagouv/ma-cantine/issues/5793)) ([edef7ec](https://github.com/betagouv/ma-cantine/commit/edef7ec5f8a792b82e11fcf298cd78501aad939e))
* **Imports:** Cantines: ajout du champ nombre_satellites (nécessaire pour les CC) ([#5803](https://github.com/betagouv/ma-cantine/issues/5803)) ([57f2825](https://github.com/betagouv/ma-cantine/commit/57f28255ec3333818d4346085b4b138739d54cd1))
* **Tableau de bord:** ré-organisation du code ([#5807](https://github.com/betagouv/ma-cantine/issues/5807)) ([c1561db](https://github.com/betagouv/ma-cantine/commit/c1561db2965716bcbaec9d49c29896782f3f8ce2))


### Corrections (bugs, typos...)

* **Imports:** pointer vers la bonne URL du schéma suite au merge de [#5803](https://github.com/betagouv/ma-cantine/issues/5803) ([3751d0f](https://github.com/betagouv/ma-cantine/commit/3751d0f5a86f634306a2830c9328ad29595c0d46))


### Technique

* **pre-commit:** ignorer les fichiers de tests avec encodage complexes (utf-16, windows) ([#5816](https://github.com/betagouv/ma-cantine/issues/5816)) ([524f8fd](https://github.com/betagouv/ma-cantine/commit/524f8fd1852f7e4cd85df9c9191e2ef2a8b78aae))
* **PRs:** auto-assign même sur les PR en draft ([#5815](https://github.com/betagouv/ma-cantine/issues/5815)) ([728e241](https://github.com/betagouv/ma-cantine/commit/728e24146d210abcbe03e2c1d53d0781f719e089))
* **PRs:** basculer la GA auto-reviewer sur ubuntu-slim ([#5813](https://github.com/betagouv/ma-cantine/issues/5813)) ([fdba8c3](https://github.com/betagouv/ma-cantine/commit/fdba8c3ed9d28115ddfbfa5f217a56e8e7a6be1a))
* **release-please:** basculer sur ubuntu-slim ([#5812](https://github.com/betagouv/ma-cantine/issues/5812)) ([18c26fb](https://github.com/betagouv/ma-cantine/commit/18c26fb8437efe86f717d530ba418b7224dd6104))

## [2025.35.0](https://github.com/betagouv/ma-cantine/compare/v2025.34.1...v2025.35.0) (2025-10-29)


### Nouveautés

* **Tableau de bord:** création de la page vue3 (cachée aux utilisateurs) ([#5784](https://github.com/betagouv/ma-cantine/issues/5784)) ([c4dfd58](https://github.com/betagouv/ma-cantine/commit/c4dfd58ed080032a98a161d87e81dce9e4afcaa3))
* **Tableau de bord:** intégration de la vue pour un utilisateur sans cantine ([#5785](https://github.com/betagouv/ma-cantine/issues/5785)) ([e1c7498](https://github.com/betagouv/ma-cantine/commit/e1c74986ae52de149f762e8c0fb516d9430ea026))


### Améliorations

* **Cantines:** Règles métiers: le SIRET doit être unique (à la création) ([#5797](https://github.com/betagouv/ma-cantine/issues/5797)) ([72ce192](https://github.com/betagouv/ma-cantine/commit/72ce1921fd37fdcb9b61b1379762310e06fefc0e))
* **Cantines:** Règles métiers: nombre de repas annuels &gt; nombre de repas quotidien ([#5796](https://github.com/betagouv/ma-cantine/issues/5796)) ([bb2df2e](https://github.com/betagouv/ma-cantine/commit/bb2df2e7aa25dfeb6d9b5fcecb20668e383690af))
* **Cantines:** Règles métiers: règles spécifiques aux cantines satellites (siret CC doit être différent de siret SAT) (à la création) ([#5801](https://github.com/betagouv/ma-cantine/issues/5801)) ([d8b3281](https://github.com/betagouv/ma-cantine/commit/d8b328156a634e0d7046565580f209950c0b30de))
* **Cantines:** Règles métiers: règles spécifiques aux cantines satellites (siret CC obligatoire) (à la création) ([#5794](https://github.com/betagouv/ma-cantine/issues/5794)) ([714cc75](https://github.com/betagouv/ma-cantine/commit/714cc751cb5a4c8aaa96a6dc1ae444e942f29f6e))


### Corrections (bugs, typos...)

* **Tableau de bord:** correctifs du recettage lot 1 ([#5799](https://github.com/betagouv/ma-cantine/issues/5799)) ([7a3440d](https://github.com/betagouv/ma-cantine/commit/7a3440d0c4d4998afd808138b4f188d90587b99b))


### Technique

* **Imports:** petit ménage suite à l'ajout des règles métiers récentes ([#5802](https://github.com/betagouv/ma-cantine/issues/5802)) ([d928df3](https://github.com/betagouv/ma-cantine/commit/d928df31e37ccfba1599b7bd7caf5b61d113fa12))
* **Linting:** ajout de ruff (pour remplacer flake8, black & isort) ([#5806](https://github.com/betagouv/ma-cantine/issues/5806)) ([ea56ee7](https://github.com/betagouv/ma-cantine/commit/ea56ee76e33be4289671a4a4adddbf235a539019))
* **pre-commit:** mise à jour des versions (avant ruff) ([#5805](https://github.com/betagouv/ma-cantine/issues/5805)) ([abca0e6](https://github.com/betagouv/ma-cantine/commit/abca0e65a1cfbf818b89bdd09cf3cbcdca3ab08e))
* **release-please:** maj de la config à la v4 (depuis la v3) ([#5804](https://github.com/betagouv/ma-cantine/issues/5804)) ([bdf0c69](https://github.com/betagouv/ma-cantine/commit/bdf0c699b043c37f76b2c762d6aa3a8d33188fdc))

## [2025.34.1](https://github.com/betagouv/ma-cantine/compare/v2025.34.0...v2025.34.1) (2025-10-21)


### Améliorations

* **Cantines:** Imports: autorise le type "nombre" et "texte" pour les valeurs de siret ([#5783](https://github.com/betagouv/ma-cantine/issues/5783)) ([c329cdb](https://github.com/betagouv/ma-cantine/commit/c329cdbc7439ecca8db915aee49ad9a66d52d33e))
* **Cantines:** Règles métiers: rendre le champ siret (ou siren) obligatoire ([#5789](https://github.com/betagouv/ma-cantine/issues/5789)) ([fa6bc7d](https://github.com/betagouv/ma-cantine/commit/fa6bc7da0fdb18f127f48ba1e53b652c585918b2))
* **Cantines:** Règles métiers: rendre le champ siret obligatoire si cuisine centrale ([#5792](https://github.com/betagouv/ma-cantine/issues/5792)) ([45b94c9](https://github.com/betagouv/ma-cantine/commit/45b94c98c9c3cb85c42e44b1761df25b85f30d84))
* **Contact:** ajout de champs au formulaire de contact et suppression bandeau email ([#5786](https://github.com/betagouv/ma-cantine/issues/5786)) ([5897dad](https://github.com/betagouv/ma-cantine/commit/5897dad61c1e4d8ff2e908e9c986e3b5b8420312))
* **Imports:** améliore le tracking pour différencier les fichiers csv des excels ([#5782](https://github.com/betagouv/ma-cantine/issues/5782)) ([8c0ea8e](https://github.com/betagouv/ma-cantine/commit/8c0ea8ef1f52062689f708eb7c49e6449a46765a))


### Technique

* **Cantines:** Règles métiers: autoriser les nombres pour les champs siret & siren ([#5790](https://github.com/betagouv/ma-cantine/issues/5790)) ([ceb8d06](https://github.com/betagouv/ma-cantine/commit/ceb8d060f7bbba083fddb3c2d49aad88cfccd25d))
* **deps-dev:** bump @rushstack/eslint-patch in /2024-frontend ([2e7e3f4](https://github.com/betagouv/ma-cantine/commit/2e7e3f481bb552f0a4652365a8e5cc86bc9fa19d))
* **deps:** bump vue from 3.5.20 to 3.5.22 in /2024-frontend ([21a8ebe](https://github.com/betagouv/ma-cantine/commit/21a8ebe6b06296b7dba2a7f40476e5dff90ffeb4))
* **deps:** bump vue-i18n from 11.1.10 to 11.1.12 in /2024-frontend ([2cc5c25](https://github.com/betagouv/ma-cantine/commit/2cc5c256844325d38de307ae12f8661e1d8cd6cc))

## [2025.34.0](https://github.com/betagouv/ma-cantine/compare/v2025.33.2...v2025.34.0) (2025-10-17)


### Nouveautés

* **Imports cantines:** autorise l'import de fichiers au format Excel (.xlsx) ([#5755](https://github.com/betagouv/ma-cantine/issues/5755)) ([29ea842](https://github.com/betagouv/ma-cantine/commit/29ea8426576e375f62d548bd486d2d5b5d183acb))


### Améliorations

* **Bilans:** Imports: rend obligatoires la colonne 'modèle économique' ([#5778](https://github.com/betagouv/ma-cantine/issues/5778)) ([fd6415a](https://github.com/betagouv/ma-cantine/commit/fd6415aea343f48d8cd518727de216a18034442d))
* **Cantines:** Imports: rend obligatoires les colonnes 'modèle économique' (tout le monde) et 'source des données' (admin) ([#5776](https://github.com/betagouv/ma-cantine/issues/5776)) ([5e76244](https://github.com/betagouv/ma-cantine/commit/5e76244ff96c4fbe2fa17a4853fe7602b567d62a))
* **Cantines:** Règles métiers: au moment du save, vérifier les règles déjà présentes sur le modèle au moment (nom, siret, siren, choices...) ([#5770](https://github.com/betagouv/ma-cantine/issues/5770)) ([79657e4](https://github.com/betagouv/ma-cantine/commit/79657e42d9b3c58b9e57320a7e182eeb82877726))
* **Cantines:** Règles métiers: rendre les champs daily_meal_count & yearly_meal_count obligatoires ([#5773](https://github.com/betagouv/ma-cantine/issues/5773)) ([4bd8f19](https://github.com/betagouv/ma-cantine/commit/4bd8f19a6cc3069b3345621586a69a4af5191ea4))
* **Cantines:** Règles métiers: rendre les champs management_type, production_type & economic_model obligatoires ([#5772](https://github.com/betagouv/ma-cantine/issues/5772)) ([c3564a4](https://github.com/betagouv/ma-cantine/commit/c3564a4741a122c64088b0e74d74c7ba6776ca7c))
* **Statistiques:** Ajout du lien vers le dashboard Metabase 'stats publique' dans le footer ([#5771](https://github.com/betagouv/ma-cantine/issues/5771)) ([6f1c9e6](https://github.com/betagouv/ma-cantine/commit/6f1c9e6d12ad2b67a5f1dd62476634a808da8689))


### Corrections (bugs, typos...)

* **Cantines:** Règles métiers: répare les tests (atomicité) ([#5779](https://github.com/betagouv/ma-cantine/issues/5779)) ([7edfe74](https://github.com/betagouv/ma-cantine/commit/7edfe74e145656d1adc1c1135086bca55446c566))
* **Ministère:** changement du nom du ministère et de la marianne ([#5775](https://github.com/betagouv/ma-cantine/issues/5775)) ([a023706](https://github.com/betagouv/ma-cantine/commit/a0237065f9abaa6aa097b9592892da271c78b4a7))
* **Restaurants satelllites:** mise à jour des terminologie oubliées ([#5777](https://github.com/betagouv/ma-cantine/issues/5777)) ([8a01ef9](https://github.com/betagouv/ma-cantine/commit/8a01ef93f1155abae7b3396bc2ca8be595845263))


### Technique

* **Cantines:** Metabase: utiliser source au lieu de SerializerMethodField ([#5766](https://github.com/betagouv/ma-cantine/issues/5766)) ([be9148b](https://github.com/betagouv/ma-cantine/commit/be9148b9b4c91573c3aa23a035d9c7167de8df98))
* **Cantines:** Règles métiers: cleaner les tests avant les modifs ([#5768](https://github.com/betagouv/ma-cantine/issues/5768)) ([baa6f15](https://github.com/betagouv/ma-cantine/commit/baa6f15284f08c1c574da04bac7f8be35a8dce24))
* **deps:** bump django from 5.1.10 to 5.1.13 ([#5740](https://github.com/betagouv/ma-cantine/issues/5740)) ([7c513f4](https://github.com/betagouv/ma-cantine/commit/7c513f434bbaef0375733c9f261fdfa48e479517))
* **Statistiques:** enlever le lien vers 'Indicateurs clés' dans le header ([#5774](https://github.com/betagouv/ma-cantine/issues/5774)) ([e77bc66](https://github.com/betagouv/ma-cantine/commit/e77bc66c6fa340d68a1fa42ba6f6e2e57bc29960))
* **Tests:** paramètre pour pouvoir ignorer les tests nécessitant internet ([#5780](https://github.com/betagouv/ma-cantine/issues/5780)) ([fc443dd](https://github.com/betagouv/ma-cantine/commit/fc443ddf3df9be3b85b2a79187798b113ab9599e))

## [2025.33.2](https://github.com/betagouv/ma-cantine/compare/v2025.33.1...v2025.33.2) (2025-10-13)


### Améliorations

* **Homogénéisation terminologie:** homogénéisation du terme "Cuisine centrale" ([#5722](https://github.com/betagouv/ma-cantine/issues/5722)) ([b93c43d](https://github.com/betagouv/ma-cantine/commit/b93c43d45704de1f217ae54c37916ad0aa520791))
* **Homogénéisation terminologie:** homogénéisation du terme "Restaurant avec cuisine sur place" ([#5762](https://github.com/betagouv/ma-cantine/issues/5762)) ([2039878](https://github.com/betagouv/ma-cantine/commit/2039878885d75aee9e84dd9440292ba6b2ff3301))
* **Homogénéisation terminologie:** homogénéisation du terme "Restaurant satellite" ([#5719](https://github.com/betagouv/ma-cantine/issues/5719)) ([b60ae55](https://github.com/betagouv/ma-cantine/commit/b60ae5517c6bf65534997321dd16163f27979dbe))
* **Imports:** utilise Validata pour vérifier le fichier et son format ([#5742](https://github.com/betagouv/ma-cantine/issues/5742)) ([60df3c0](https://github.com/betagouv/ma-cantine/commit/60df3c086152f2acb79c915d75a637ce8a5ae705))
* **Modèle économique:** homogénéisation de la terminologie affichée à l'utilisateur ([#5759](https://github.com/betagouv/ma-cantine/issues/5759)) ([7405025](https://github.com/betagouv/ma-cantine/commit/740502520a11f161c7e50abfd3d6ae303a2bf566))
* **Modèle économique:** mise à jour de la terminologie dans le backend ([#5764](https://github.com/betagouv/ma-cantine/issues/5764)) ([6737cae](https://github.com/betagouv/ma-cantine/commit/6737caee7c9acb046b747859d670861b17edefcf))


### Corrections (bugs, typos...)

* **Terminologies:** divers correctifs d'homogénéisation ([#5760](https://github.com/betagouv/ma-cantine/issues/5760)) ([9c1c490](https://github.com/betagouv/ma-cantine/commit/9c1c490e2b50bcf9ed359e5da94aa2253100f466))
* **Url:** encode les urls pour ne plus avoir de "page non trouvée" pour les cantines avec des caractères spéciaux ([#5765](https://github.com/betagouv/ma-cantine/issues/5765)) ([ce499d6](https://github.com/betagouv/ma-cantine/commit/ce499d67133c614a28a88e16a786fa8182676c29))


### Technique

* **Cantines:** Script pour créer les quelques cantines satellites hard-supprimées qui apparraissent dans les TD [1TD1Site] ([#5751](https://github.com/betagouv/ma-cantine/issues/5751)) ([9e77e8a](https://github.com/betagouv/ma-cantine/commit/9e77e8ab20997494e34238809c03fc309e98cee0))
* **Diagnostics:** 2 TD de 2022 étaient filtrées dans l'export open data. Les filtrer partout (chaîne de traitement) ([#5744](https://github.com/betagouv/ma-cantine/issues/5744)) ([11a33e0](https://github.com/betagouv/ma-cantine/commit/11a33e08ffc3a1f32481dda6975d6b1037d3daae))
* **Management Commands:** renommer pour clarifier (prefix avec le nom du modèle concerné) ([#5750](https://github.com/betagouv/ma-cantine/issues/5750)) ([630fdac](https://github.com/betagouv/ma-cantine/commit/630fdac51233a6a3d106ca380d166b9e3feb4a52))
* **Metabase:** Cantines: ordonner par date de création ([#5748](https://github.com/betagouv/ma-cantine/issues/5748)) ([88721ae](https://github.com/betagouv/ma-cantine/commit/88721ae0705d41db8b91f6eacf8ac8ba58827154))
* **Open Data:** Cantines: ordonner l'export par date de création ([#5745](https://github.com/betagouv/ma-cantine/issues/5745)) ([069d0aa](https://github.com/betagouv/ma-cantine/commit/069d0aa6135c88e5096bfe2f443cf84a5ac55450))
* **Teledeclaration:** indiquer la version dans un fichier de config dédié ([#5717](https://github.com/betagouv/ma-cantine/issues/5717)) ([d73d926](https://github.com/betagouv/ma-cantine/commit/d73d926d1c37bac96fc30b501b8ea2494355883a))

## [2025.33.1](https://github.com/betagouv/ma-cantine/compare/v2025.33.0...v2025.33.1) (2025-10-06)


### Corrections (bugs, typos...)

* **Celery:** ajouter les paramètres manquant pour les exports ([#5746](https://github.com/betagouv/ma-cantine/issues/5746)) ([b1e16e0](https://github.com/betagouv/ma-cantine/commit/b1e16e0c7b26f2ddbfb45a0e7f9cef1ac18c25c8))


### Technique

* **Diagnostic:** migrer les views Open Data & Metabase [1TD1Site] ([#5743](https://github.com/betagouv/ma-cantine/issues/5743)) ([f589b86](https://github.com/betagouv/ma-cantine/commit/f589b8627077a4587321cb75f2715d6a30f38154))
* **Metabase:** extraire les données à partir de la table Diagnostic au lieu de Teledeclaration [1TD1Site] ([#5676](https://github.com/betagouv/ma-cantine/issues/5676)) ([97b3156](https://github.com/betagouv/ma-cantine/commit/97b315606e9e3d2f920985dd27174b4b091aa0dd))

## [2025.33.0](https://github.com/betagouv/ma-cantine/compare/v2025.32.1...v2025.33.0) (2025-10-02)


### Nouveautés

* **Gérer mes satellites:** migration de la page en vue3 ([#5713](https://github.com/betagouv/ma-cantine/issues/5713)) ([b1dca8c](https://github.com/betagouv/ma-cantine/commit/b1dca8cda08022929e30a9bb12c59b33433a2916))
* **Gérer mes satellites:** remplace l'url de la page pour la nouvelle ([#5714](https://github.com/betagouv/ma-cantine/issues/5714)) ([e5b2d76](https://github.com/betagouv/ma-cantine/commit/e5b2d76291be90bd2f54380d36fec3ffc23912be))
* **Gestion cantine:** création d'une page pour voir les informations enregistrées de mon établissement ([#5702](https://github.com/betagouv/ma-cantine/issues/5702)) ([e57ea95](https://github.com/betagouv/ma-cantine/commit/e57ea950c59afd4b42e7e3ae1bc56b7bc3142d6a))


### Améliorations

* **Gérer mes satellites:** ajout du lien vers la page d'import des cantines ([#5741](https://github.com/betagouv/ma-cantine/issues/5741)) ([49d2558](https://github.com/betagouv/ma-cantine/commit/49d2558a07c506b219768873c34305016ebd4ffa))


### Corrections (bugs, typos...)

* **Diagnostics:** script pour ajouter le canteen_id manquant dans les premières versions de TD (avant v4, 2020-2021) ([#5711](https://github.com/betagouv/ma-cantine/issues/5711)) ([c64731d](https://github.com/betagouv/ma-cantine/commit/c64731d64d35fd101e3759558a5a86e5ecdfa1ff))
* **Progression:** corrige l'affichage des cantines satellites dans la prévisualisation ([#5718](https://github.com/betagouv/ma-cantine/issues/5718)) ([f8aec50](https://github.com/betagouv/ma-cantine/commit/f8aec50837c3996292e8c3719eed308b486e321d))


### Documentation

* **Teledeclaration:** Fichier dédié pour expliquer les différentes versions au cours des années ([#5673](https://github.com/betagouv/ma-cantine/issues/5673)) ([ba6809a](https://github.com/betagouv/ma-cantine/commit/ba6809ace67a0b38054584873c0ed90fc4eef49b))


### Technique

* **Admin:** Cantines: accélérer le chargement de la page (section dédiée aux gestionnaires) ([#5739](https://github.com/betagouv/ma-cantine/issues/5739)) ([8b8661e](https://github.com/betagouv/ma-cantine/commit/8b8661e7df9495e3ffe86e1d4c0f77f5693a7cdc))
* **Admin:** Utilisateurs: répare et améliore la section dédiée aux cantines gérées ([#5738](https://github.com/betagouv/ma-cantine/issues/5738)) ([556adc5](https://github.com/betagouv/ma-cantine/commit/556adc55991b2448d173bc623fe92f887e0fcc8f))
* **API Recherche Entreprise:** ajout d'un paramètre Matomo pour leur suivi ([#5710](https://github.com/betagouv/ma-cantine/issues/5710)) ([9ed3a20](https://github.com/betagouv/ma-cantine/commit/9ed3a20f74cb65377b5d93ee1036b48035cc3759))
* **Open Data:** indiquer explicitement les identifiants des jeux de données ([#5709](https://github.com/betagouv/ma-cantine/issues/5709)) ([cb31a52](https://github.com/betagouv/ma-cantine/commit/cb31a524ec47b7dcffa73cb8d97671527cd42a40))

## [2025.32.1](https://github.com/betagouv/ma-cantine/compare/v2025.32.0...v2025.32.1) (2025-09-23)


### Améliorations

* **Diagnostic:** nouveau champ pour stocker la valeur annuelle totale des achats egalim hors bio (aggrégées si TD détaillée) [1TD1Site] ([#5677](https://github.com/betagouv/ma-cantine/issues/5677)) ([79acdb9](https://github.com/betagouv/ma-cantine/commit/79acdb96609c81b373b1d94c6e7054d2843a8b80))
* **Diagnostics:** API : une fois le diagnostic télédéclaré, le mettre en lecture-seule [1TD1Site] ([#5707](https://github.com/betagouv/ma-cantine/issues/5707)) ([f91efde](https://github.com/betagouv/ma-cantine/commit/f91efde26d3d5af885aac803437edfa999bd256c))
* **Diagnostics:** Imports : une fois le diagnostic télédéclaré, le mettre en lecture-seule [1TD1Site] ([#5706](https://github.com/betagouv/ma-cantine/issues/5706)) ([98e29d6](https://github.com/betagouv/ma-cantine/commit/98e29d61c32f3dcdaa16cd1f247e369d2caefc6a))


### Corrections (bugs, typos...)

* **Admin:** permet de supprimer en rapidemment les cantines d'un gestionnaire ([#5701](https://github.com/betagouv/ma-cantine/issues/5701)) ([c2f8900](https://github.com/betagouv/ma-cantine/commit/c2f89008ea449d7a01b63f3c225531535fdaef3c))
* **Cantines:** Commande pour remplir le champ declaration_donnees_YEAR: prendre en compte les cantines supprimées ([#5674](https://github.com/betagouv/ma-cantine/issues/5674)) ([a8d4bc9](https://github.com/betagouv/ma-cantine/commit/a8d4bc900353a95fb643ad407a85006bd3f159fd))


### Technique

* **Admin:** permettre de chercher par ID les cantines, diagnostics & users ([#5704](https://github.com/betagouv/ma-cantine/issues/5704)) ([5e1f1e2](https://github.com/betagouv/ma-cantine/commit/5e1f1e204136e0a851097298e70f939f862b3ad3))
* **Cantines:** helper method pour réinitialiser les données geo (et permettre de relancer le geo bot) ([#5695](https://github.com/betagouv/ma-cantine/issues/5695)) ([11d1cb6](https://github.com/betagouv/ma-cantine/commit/11d1cb65e1f1453e86d4b307245a48402f6d070d))
* **Open Data:** Cantines : bouger la requête dans une ViewSet dédié pour homogénéiser avec les autres exports ([#5697](https://github.com/betagouv/ma-cantine/issues/5697)) ([ae65f1e](https://github.com/betagouv/ma-cantine/commit/ae65f1efcdd8d3e8007146638fd4f3fd1c3d7467))
* **Open Data:** clarifier la commande export_dataset ([#5699](https://github.com/betagouv/ma-cantine/issues/5699)) ([ca7a127](https://github.com/betagouv/ma-cantine/commit/ca7a127348434a63b4d180bcd306ed7c18a6da58))
* **Open Data:** lancer l'export le weekend et après le geo bot ([#5703](https://github.com/betagouv/ma-cantine/issues/5703)) ([7661074](https://github.com/betagouv/ma-cantine/commit/7661074cdf7287437c7875cb50ad79c74dc5310a))

## [2025.32.0](https://github.com/betagouv/ma-cantine/compare/v2025.31.0...v2025.32.0) (2025-09-12)


### Nouveautés

* **Création cantine:** redirige la cantine centrale vers la page de gestion des satellites après sa création ([#5687](https://github.com/betagouv/ma-cantine/issues/5687)) ([2d5d17b](https://github.com/betagouv/ma-cantine/commit/2d5d17ba3485bf19133eb18358aa05ebd77e1337))
* **Création satellite:** ajout du formulaire ([#5685](https://github.com/betagouv/ma-cantine/issues/5685)) ([d1614c4](https://github.com/betagouv/ma-cantine/commit/d1614c4739fefa9328821c567e6b34e14873e28c))
* **Création satellites:** nouvelle page vue3 ([#5684](https://github.com/betagouv/ma-cantine/issues/5684)) ([c37eea0](https://github.com/betagouv/ma-cantine/commit/c37eea0f89981382959d216aeab50202547fd33a))
* **Création satellite:** suppression de l'ancien formulaire ([#5689](https://github.com/betagouv/ma-cantine/issues/5689)) ([fe6f4a9](https://github.com/betagouv/ma-cantine/commit/fe6f4a9f62f06a077949efe5b6cf078e2c0d7ff4))
* **Modification cantine:** vérifie les champs au pré-remplissage ([#5694](https://github.com/betagouv/ma-cantine/issues/5694)) ([8d2cb27](https://github.com/betagouv/ma-cantine/commit/8d2cb2708858a4a19114823a02b4540186dc60a8))


### Améliorations

* **Diagnostic:** nouveau champ pour stocker l'ID historique de la TD [1TD1site] ([#5686](https://github.com/betagouv/ma-cantine/issues/5686)) ([677a5d3](https://github.com/betagouv/ma-cantine/commit/677a5d3c646e2f9d984b338f508b65e998a15861))
* **Noms des pages:** organise la structure des urls des pages d'une cantine ([#5682](https://github.com/betagouv/ma-cantine/issues/5682)) ([d9d8ae6](https://github.com/betagouv/ma-cantine/commit/d9d8ae68488473e92e3698b7e32a34a05bbfbbd4))
* **Open Data:** nouvelle colonne teledeclaration_id ([#5691](https://github.com/betagouv/ma-cantine/issues/5691)) ([bee6bec](https://github.com/betagouv/ma-cantine/commit/bee6bec12e7140144bac2b3f033cdc47fec8d191))
* **Open Data:** ordonner les exports par date de télédéclaration ([#5690](https://github.com/betagouv/ma-cantine/issues/5690)) ([1f61ece](https://github.com/betagouv/ma-cantine/commit/1f61eced3ce8e16e847eb8599a926d82120d38af))


### Corrections (bugs, typos...)

* **Cantines:** corrige les urls de redirection lors de la création d'une cantine ([#5693](https://github.com/betagouv/ma-cantine/issues/5693)) ([209cdd0](https://github.com/betagouv/ma-cantine/commit/209cdd00f9e5917ddd7fb44139359b73a946e541))
* **Création de cantine:** correction bug d'affichage du sélecteur de la cantine centrale ([#5692](https://github.com/betagouv/ma-cantine/issues/5692)) ([ea2e8af](https://github.com/betagouv/ma-cantine/commit/ea2e8af0de1ed2eb69c877a4cda9c7821358c82f))


### Technique

* **API Stats:** calculer les statistiques sur le modèle Diagnostic au lieu de Teledeclaration [1TD1Site] ([#5643](https://github.com/betagouv/ma-cantine/issues/5643)) ([098439b](https://github.com/betagouv/ma-cantine/commit/098439b8d39ca6460eb74b37ac92e42ac83c5cc4))
* **Open Data:** extraire les données à partir de la table Diagnostic au lieu de Teledeclaration [1TD1Site] ([#5667](https://github.com/betagouv/ma-cantine/issues/5667)) ([47bb432](https://github.com/betagouv/ma-cantine/commit/47bb4321031bb3873ffbd9287597898278dcbc09))

## [2025.31.0](https://github.com/betagouv/ma-cantine/compare/v2025.30.0...v2025.31.0) (2025-09-11)


### Nouveautés

* **Création de cantine:** ajout du champ "nombre de repas par jour" pour les cuisines centrales ([#5662](https://github.com/betagouv/ma-cantine/issues/5662)) ([e835eda](https://github.com/betagouv/ma-cantine/commit/e835eda51c8e01cdcb997ae207ff29da4a580988))
* **Création de cantine:** ajoute une description dans le sélecteur de mode de production pour les cuisines centrales ([#5664](https://github.com/betagouv/ma-cantine/issues/5664)) ([621fc02](https://github.com/betagouv/ma-cantine/commit/621fc0218381bc99b6ce0dd8d3073a2e2811b27a))
* **Création de cantine:** ajoute une limite de 3 secteurs maximum ([#5668](https://github.com/betagouv/ma-cantine/issues/5668)) ([74cbb82](https://github.com/betagouv/ma-cantine/commit/74cbb82a48f62b099361205e03ed3a39b669c82f))
* **Création de cantine:** le champ SIRET du livreur devient un sélecteur ([#5650](https://github.com/betagouv/ma-cantine/issues/5650)) ([2af9ef5](https://github.com/betagouv/ma-cantine/commit/2af9ef5102c7d043500d0c586fdaa03924f4a501))
* **Open Data:** stocker les fichiers csv dans Github ([#5681](https://github.com/betagouv/ma-cantine/issues/5681)) ([64c2ce0](https://github.com/betagouv/ma-cantine/commit/64c2ce0ced6fe8f6d3fab439631f462494c63b16))
* **Télédéclaration:** autorise une cantine centrale à télédéclarer dès que une cantine SAT lui est rattaché ([#5666](https://github.com/betagouv/ma-cantine/issues/5666)) ([edc1b6d](https://github.com/betagouv/ma-cantine/commit/edc1b6dd8fde99ebccde43a43c98e9888ad8cb6e))
* **Télédéclaration:** bloque la télédéclaration pour les cantines sites ayant plus de 3 secteurs ([#5675](https://github.com/betagouv/ma-cantine/issues/5675)) ([8c288e0](https://github.com/betagouv/ma-cantine/commit/8c288e0e80a18d33cb49d2e6c97fea2c65f3d432))


### Améliorations

* **Admin:** Cantines & Achats: changer le comportement du bouton Supprimer (soft delete au lieu de hard delete) ([#5296](https://github.com/betagouv/ma-cantine/issues/5296)) ([d9341bb](https://github.com/betagouv/ma-cantine/commit/d9341bb1b8cfd1ba824b3b0d4d5d881b54b4cae1))
* **Admin:** Cantines: cacher le bouton Supprimer ([#5683](https://github.com/betagouv/ma-cantine/issues/5683)) ([9d3d311](https://github.com/betagouv/ma-cantine/commit/9d3d3115e5a91debb705d5c745fe33d6a5f3746f))
* **Diagnostic:** nouveau champ pour stocker la version au moment de la TD [1TD1site] ([#5672](https://github.com/betagouv/ma-cantine/issues/5672)) ([5d95bb0](https://github.com/betagouv/ma-cantine/commit/5d95bb010bfbd20ebb68bcc50d2ecb2c3e5b17e4))
* **Diagnostic:** nouveau champ pour stocker le déclarant au moment de la TD [1TD1site] ([#5670](https://github.com/betagouv/ma-cantine/issues/5670)) ([6c3f600](https://github.com/betagouv/ma-cantine/commit/6c3f600837e476cac0cb322489bbe6334e1f6d02))


### Corrections (bugs, typos...)

* **Diagnostic:** si une cantine est supprimée, ne plus supprimer ses bilans [1TD1Site] ([#5671](https://github.com/betagouv/ma-cantine/issues/5671)) ([03addc3](https://github.com/betagouv/ma-cantine/commit/03addc31f47a8616c2210e4b8d4cae4ec861d2e1))
* **Teledeclaration:** petit fix sur le filtre des valeurs aberrantes [1TD1Site] ([#5663](https://github.com/betagouv/ma-cantine/issues/5663)) ([121f65c](https://github.com/betagouv/ma-cantine/commit/121f65c02c6096151164974f3f9e83d660937bbf))


### Technique

* **deps:** corrige la différence de version de vite ([#5680](https://github.com/betagouv/ma-cantine/issues/5680)) ([18c1b04](https://github.com/betagouv/ma-cantine/commit/18c1b04c151c6d8c176e8b65327dc3a4f976ee73))
* **Diagnostic:** filtre cantine avec siret ou siren_unite_legale: utiliser canteen_snapshot [1TD1Site] ([#5669](https://github.com/betagouv/ma-cantine/issues/5669)) ([521d548](https://github.com/betagouv/ma-cantine/commit/521d54865a276b3b43a4a17fc47e44b95094ffd2))

## [2025.30.0](https://github.com/betagouv/ma-cantine/compare/v2025.29.0...v2025.30.0) (2025-09-04)


### Nouveautés

* **Observatoire:** ajout du lien pour comprendre le calcul des chiffres ([#5660](https://github.com/betagouv/ma-cantine/issues/5660)) ([76f6457](https://github.com/betagouv/ma-cantine/commit/76f64574b94bbd251f23e9211cda6abe6f067f07))


### Corrections (bugs, typos...)

* **API Stats:** Corrige les taux de viande egalim, viande france & aquaculture egalim (pour les diagnostics détaillés) ([#5658](https://github.com/betagouv/ma-cantine/issues/5658)) ([c6c1c89](https://github.com/betagouv/ma-cantine/commit/c6c1c89ce3ac9076d5a684125ff32c2cf01f25a5))


### Technique

* **Diagnostic:** clarifie le queryset valid_td_by_year ([#5656](https://github.com/betagouv/ma-cantine/issues/5656)) ([a54765a](https://github.com/betagouv/ma-cantine/commit/a54765a3ffa2db1bab0e51a4b1955682bc171ee6))
* **Django:** installe ipython + basculer le shell_plus dessus ([#5659](https://github.com/betagouv/ma-cantine/issues/5659)) ([7ce7432](https://github.com/betagouv/ma-cantine/commit/7ce7432ea0f7048c218098e263a1bb26efa38fe7))

## [2025.29.0](https://github.com/betagouv/ma-cantine/compare/v2025.28.1...v2025.29.0) (2025-09-02)


### Nouveautés

* **Création de cantine:** autorise la télédéclaration pour les cantines centrales sans secteur ([#5642](https://github.com/betagouv/ma-cantine/issues/5642)) ([8a7df34](https://github.com/betagouv/ma-cantine/commit/8a7df340d3d57f4c994fe0b6565c2a56ddbb2cae))
* **Creation de cantine:** les secteurs ne sont pas obligatoires pour les cuisines centrales ([#5638](https://github.com/betagouv/ma-cantine/issues/5638)) ([91904d2](https://github.com/betagouv/ma-cantine/commit/91904d27bcc922483893bad1fcc0fe3a75e27358))


### Corrections (bugs, typos...)

* **Creation de cantine:** changement url schemas imports ([#5639](https://github.com/betagouv/ma-cantine/issues/5639)) ([1623c7a](https://github.com/betagouv/ma-cantine/commit/1623c7a2345a10ad0832377fc1f0f1c161ab9474))
* **Observatoire:** corrige l'affichage des filtres sur mobile ([#5652](https://github.com/betagouv/ma-cantine/issues/5652)) ([6145e4b](https://github.com/betagouv/ma-cantine/commit/6145e4b928b7f4400bfb91ee79199f6d9bb024e6))
* **Open Data:** Répare le calcul de la colonne teledeclaration_ratio_egalim_hors_bio ([#5641](https://github.com/betagouv/ma-cantine/issues/5641)) ([2312480](https://github.com/betagouv/ma-cantine/commit/23124803977f8c4310b42a2f37938f38f6867f15))


### Technique

* **deps-dev:** bump eslint from 9.30.0 to 9.32.0 in /2024-frontend ([0b6e3ae](https://github.com/betagouv/ma-cantine/commit/0b6e3aea60820ec12f16bcb526180915589292fc))
* **deps-dev:** bump vite from 6.3.5 to 7.0.6 in /2024-frontend ([998ccd4](https://github.com/betagouv/ma-cantine/commit/998ccd45a31af7e658d8ce8e9bd68d6dabaed5b7))
* **deps:** bump @gouvminint/vue-dsfr in /2024-frontend ([2e60603](https://github.com/betagouv/ma-cantine/commit/2e60603e288d0d17615875328540bcb93bb5c075))
* **deps:** bump @intlify/core-base and vue-i18n in /2024-frontend ([4d850b6](https://github.com/betagouv/ma-cantine/commit/4d850b65ab72d20ae4751aa1d944ed3be87ec9c2))
* **deps:** bump @vueuse/core from 13.3.0 to 13.6.0 in /2024-frontend ([7aab924](https://github.com/betagouv/ma-cantine/commit/7aab92427f88c161cd26a3ee0c565e502720b4f5))
* **deps:** bump cssbeautifier from 1.15.1 to 1.15.4 ([8ca73a4](https://github.com/betagouv/ma-cantine/commit/8ca73a4c1c93b83ce25bc9ca4beff1e7c6d69fc2))
* **deps:** bump django from 5.1.0 to 5.1.10 ([05e790d](https://github.com/betagouv/ma-cantine/commit/05e790d4818f190fca45fd38d922256db8e51a3f))
* **deps:** bump pipdeptree from 2.26.1 to 2.28.0 ([#5566](https://github.com/betagouv/ma-cantine/issues/5566)) ([04edc91](https://github.com/betagouv/ma-cantine/commit/04edc91068651726fcb0a2a10b4ff734d8832595))
* **deps:** bump vue from 3.5.16 to 3.5.18 in /2024-frontend ([422055b](https://github.com/betagouv/ma-cantine/commit/422055b41cf6e20622a6eeb82b8532bc7299d436))
* **deps:** Retour en arrière version incompatible avec django-vite-plugin ([#5649](https://github.com/betagouv/ma-cantine/issues/5649)) ([12a0930](https://github.com/betagouv/ma-cantine/commit/12a093061dff59cc293b85f203074b4af9896ddb))

## [2025.28.1](https://github.com/betagouv/ma-cantine/compare/v2025.28.0...v2025.28.1) (2025-08-29)


### Améliorations

* **Diagnostic:** dans la méthode pour télédéclarer, ajouter le paramètre applicant [1TD1Site] ([#5644](https://github.com/betagouv/ma-cantine/issues/5644)) ([a70035f](https://github.com/betagouv/ma-cantine/commit/a70035f563e47d1f9f3de979aaaca80ab8df17e0))
* **Diagnostic:** dans la méthode pour télédéclarer, vérifier qu'on est en campagne [1TD1Site] ([#5630](https://github.com/betagouv/ma-cantine/issues/5630)) ([8da0c4c](https://github.com/betagouv/ma-cantine/commit/8da0c4ccfc5f01f6fa01601a0fdbb93ac380d77f))
* **Diagnostic:** nouveau champ pour stocker le mode de télédéclaration au moment de la TD [1TD1site] ([#5636](https://github.com/betagouv/ma-cantine/issues/5636)) ([eab404d](https://github.com/betagouv/ma-cantine/commit/eab404d30a64e4c70f4bfe695939dd2a3cf28f87))
* **Diagnostic:** nouveau champ pour stocker un snapshot des satellites au moment de la TD [1TD1site] ([#5623](https://github.com/betagouv/ma-cantine/issues/5623)) ([c4a8b27](https://github.com/betagouv/ma-cantine/commit/c4a8b27a66cf707fadd1b5b71494f412911e9729))
* **Diagnostic:** nouveaux champs pour stocker la valeurs annuelles totales (aggrégées si TD détaillée) [1TD1Site] ([#5625](https://github.com/betagouv/ma-cantine/issues/5625)) ([801f895](https://github.com/betagouv/ma-cantine/commit/801f8950d38ff19abbba05335bcc428ca7b99d52))
* **Diagnostic:** nouvelle méthode pour annuler une télédéclaration [1TD1Site] ([#5631](https://github.com/betagouv/ma-cantine/issues/5631)) ([3769602](https://github.com/betagouv/ma-cantine/commit/3769602897550d06c59e9c2391b094d3ed42c7a7))
* **Diagnostic:** nouvelle méthode pour télédéclarer (modifie le status, date, snapshots) [1TD1Site] ([#5618](https://github.com/betagouv/ma-cantine/issues/5618)) ([fadc8ce](https://github.com/betagouv/ma-cantine/commit/fadc8ce5a614fbbc5df867258b3bf3fa00a65792))


### Corrections (bugs, typos...)

* **Création cantine:** changement de wording ([#5632](https://github.com/betagouv/ma-cantine/issues/5632)) ([132358d](https://github.com/betagouv/ma-cantine/commit/132358da66edb72b0156f646cd80fa5f80964825))
* **Création de cantine:** clarifie le sélecteur multiple des secteurs ([#5624](https://github.com/betagouv/ma-cantine/issues/5624)) ([c982cfb](https://github.com/betagouv/ma-cantine/commit/c982cfbf4209c5918f0a5a0b86b53635ecfcbaed))
* **Création de cantine:** empêche un livreur de repas de s'enregistrer via SIREN ([#5628](https://github.com/betagouv/ma-cantine/issues/5628)) ([6b18cd8](https://github.com/betagouv/ma-cantine/commit/6b18cd890a7f0b997b86e313718495f844552bd2))
* **Création de cantine:** ré-organisation du formulaire ([#5626](https://github.com/betagouv/ma-cantine/issues/5626)) ([9de8751](https://github.com/betagouv/ma-cantine/commit/9de8751fce115822f29df99123ebe11ede8a377e))
* **Diagnostic:** autoriser seulement les bilans de l'année correspondant à la campagne de télédéclarer [1TD1site] ([#5637](https://github.com/betagouv/ma-cantine/issues/5637)) ([e00d719](https://github.com/betagouv/ma-cantine/commit/e00d71902d9f5d53ffe63f14e842b4b158a77dc3))
* **Diagnostic:** corrige la migration des valeurs des nouveaux champs qui stockent les valeurs annuelles totales ([#5640](https://github.com/betagouv/ma-cantine/issues/5640)) ([811fe11](https://github.com/betagouv/ma-cantine/commit/811fe1118b43d9740ee23bc94d185f59255135bf))
* **Diagnostic:** corrige une migration qui ajoutait l'historisation de satellites_snapshot (pas besoin) [1TD1Site] ([#5645](https://github.com/betagouv/ma-cantine/issues/5645)) ([6797ab0](https://github.com/betagouv/ma-cantine/commit/6797ab0eab246c3cfd7ccf7b1b0fc8a9bd517217))


### Technique

* **Canteen:** renommer le queryset is_filled en filled ([#5622](https://github.com/betagouv/ma-cantine/issues/5622)) ([74b422c](https://github.com/betagouv/ma-cantine/commit/74b422c3e4b0660817c1664da0e39b011aa2d38d))
* **Diagnostic:** dupliquer (et adapter) les queryset depuis Teledeclaration vers Diagnostic (2/3) [1TD1Site] ([#5617](https://github.com/betagouv/ma-cantine/issues/5617)) ([1773404](https://github.com/betagouv/ma-cantine/commit/177340495c887fad889fcf53e36adc167ba3c9ae))
* **Diagnostic:** dupliquer (et adapter) les queryset depuis Teledeclaration vers Diagnostic (3/4) [1TD1Site] ([#5629](https://github.com/betagouv/ma-cantine/issues/5629)) ([5217ee9](https://github.com/betagouv/ma-cantine/commit/5217ee94c87ef8551b2dc30aad75b8ec3f20ba23))
* **Diagnostic:** dupliquer (et adapter) les queryset depuis Teledeclaration vers Diagnostic (4/4) [1TD1Site] ([#5635](https://github.com/betagouv/ma-cantine/issues/5635)) ([db2d573](https://github.com/betagouv/ma-cantine/commit/db2d57331950873400b1211e4b1853cbe96bf37a))
* **Diagnostic:** renommer le queryset is_filled en filled ([#5621](https://github.com/betagouv/ma-cantine/issues/5621)) ([e984eaf](https://github.com/betagouv/ma-cantine/commit/e984eaf6e4dd77bc7723cb41919e02a30b27e663))
* enlève Quentin de la liste des auto-reviewers ([#5646](https://github.com/betagouv/ma-cantine/issues/5646)) ([78ee56f](https://github.com/betagouv/ma-cantine/commit/78ee56f5af918f8afcf88d7ccd9cfb19421933fa))

## [2025.28.0](https://github.com/betagouv/ma-cantine/compare/v2025.27.0...v2025.28.0) (2025-08-14)


### Nouveautés

* **Observatoire:** indique le chargement des données ([#5612](https://github.com/betagouv/ma-cantine/issues/5612)) ([29c4749](https://github.com/betagouv/ma-cantine/commit/29c4749b76e4d24542287eb2b8b3ee23f0903212))
* **Observatoire:** remplace l'ancienne url par la nouvelle ([#5619](https://github.com/betagouv/ma-cantine/issues/5619)) ([d33f018](https://github.com/betagouv/ma-cantine/commit/d33f018a331605d85bd3da33211d1279109af4cc))


### Améliorations

* **Diagnostic:** nouveau champ pour stocker la date au moment de la TD [1TD1site] ([#5601](https://github.com/betagouv/ma-cantine/issues/5601)) ([06035d9](https://github.com/betagouv/ma-cantine/commit/06035d990ab39531b0e17f678ed5e3589b9b54c0))
* **Diagnostic:** nouveau champ pour stocker un snapshot de la cantine au moment de la TD [1TD1site] ([#5599](https://github.com/betagouv/ma-cantine/issues/5599)) ([ccf04fb](https://github.com/betagouv/ma-cantine/commit/ccf04fb6fb887452223f9376acced6d8e383b7ed))
* **Diagnostic:** nouveau champ pour stocker un snapshot du demandeur au moment de la TD [1TD1site] ([#5600](https://github.com/betagouv/ma-cantine/issues/5600)) ([43ad4cc](https://github.com/betagouv/ma-cantine/commit/43ad4cc22353834df616e87576be61e69cbb0821))
* **Observatoire:** améliore l'affichage du bloc "Je donne mon avis" ([#5610](https://github.com/betagouv/ma-cantine/issues/5610)) ([f26be51](https://github.com/betagouv/ma-cantine/commit/f26be517146976900a6604685ea5d9df96c403a7))


### Corrections (bugs, typos...)

* **Observatoire:** change l'affichage de "Objectif EGalim" ([#5614](https://github.com/betagouv/ma-cantine/issues/5614)) ([e83499d](https://github.com/betagouv/ma-cantine/commit/e83499dcaeda25819464902c428958343b3277f6))
* **Observatoire:** change la tuile pour accéder aux rapports ([#5611](https://github.com/betagouv/ma-cantine/issues/5611)) ([7dde305](https://github.com/betagouv/ma-cantine/commit/7dde3056b3415fa0ca4e5750675cff50630a610d))
* **Observatoire:** corrections de wordings ([#5615](https://github.com/betagouv/ma-cantine/issues/5615)) ([5896c5b](https://github.com/betagouv/ma-cantine/commit/5896c5ba07502d987ab9cee61a7f0cd9df801bc6))
* **Observatoire:** divers correctifs ([#5608](https://github.com/betagouv/ma-cantine/issues/5608)) ([48b879d](https://github.com/betagouv/ma-cantine/commit/48b879d8df76ab02b34da93cd86c219ae1d60704))
* **Observatoire:** petites corrections de style ([#5616](https://github.com/betagouv/ma-cantine/issues/5616)) ([031be0f](https://github.com/betagouv/ma-cantine/commit/031be0f6cb49000c4ca6e13882d78e3076e8de71))


### Technique

* **Diagnostic:** dupliquer (et adapter) les queryset depuis Teledeclaration vers Diagnostic (1/3) ([#5613](https://github.com/betagouv/ma-cantine/issues/5613)) ([58abbd6](https://github.com/betagouv/ma-cantine/commit/58abbd6771d566a5dce25580499ddc5d964fcc46))
* **Diagnostic:** quelques petites améliorations admin (vitesse, nouveau champ status) ([#5603](https://github.com/betagouv/ma-cantine/issues/5603)) ([e3dcfe7](https://github.com/betagouv/ma-cantine/commit/e3dcfe76094294d6cb8c662158dbfe1c749d66b5))
* **Diagnostic:** ramener la liste des champs séralizés au niveau du modèle ([#5602](https://github.com/betagouv/ma-cantine/issues/5602)) ([83ba1ad](https://github.com/betagouv/ma-cantine/commit/83ba1ad8c27b041e395ff8cec44b066c86bdeb71))
* **Diagnostic:** se référer au status pour savoir si il a été télédéclaré ([#5609](https://github.com/betagouv/ma-cantine/issues/5609)) ([aa93f5d](https://github.com/betagouv/ma-cantine/commit/aa93f5d3e6e470a930ecd4acb0a5523a10d8f199))
* **ETL:** Open Data: filter les cantines armées dans la queryset au lieu de pandas ([#5606](https://github.com/betagouv/ma-cantine/issues/5606)) ([42b2d2f](https://github.com/betagouv/ma-cantine/commit/42b2d2f68a77db04ba5b3126688f4526541293c2))

## [2025.27.0](https://github.com/betagouv/ma-cantine/compare/v2025.26.0...v2025.27.0) (2025-08-11)


### Nouveautés

* **Observatoire:** affiche le graphique Mode de production ([#5591](https://github.com/betagouv/ma-cantine/issues/5591)) ([dc59097](https://github.com/betagouv/ma-cantine/commit/dc59097f486d5955044cad6d25992fed844acd37))
* **Observatoire:** ajout du bouton "Copier l'url" ([#5596](https://github.com/betagouv/ma-cantine/issues/5596)) ([dbbc2a4](https://github.com/betagouv/ma-cantine/commit/dbbc2a4f7c79f29d4e4a28f79f47b29246dc45f9))
* **Observatoire:** ajout du module "Je donne mon avis" ([#5597](https://github.com/betagouv/ma-cantine/issues/5597)) ([b0a60dd](https://github.com/betagouv/ma-cantine/commit/b0a60dd5f11b80935ffae947e49e3597e3c1718c))
* **Observatoire:** ajoute le graphique des secteurs ([#5593](https://github.com/betagouv/ma-cantine/issues/5593)) ([c4d19d5](https://github.com/betagouv/ma-cantine/commit/c4d19d569405533422136f32446b90985c556063))
* **Observatoire:** ajoute le graphique du nombre de télédéclarations qui ont réussi l'objectif EGalim ([#5585](https://github.com/betagouv/ma-cantine/issues/5585)) ([2a92602](https://github.com/betagouv/ma-cantine/commit/2a9260250c04691c0ab226f402e124376ef43de6))
* **Observatoire:** ajoute les graphiques "type d'établissement" et "mode de gestion" à la page ([#5592](https://github.com/betagouv/ma-cantine/issues/5592)) ([14d8e7d](https://github.com/betagouv/ma-cantine/commit/14d8e7d21ed6aa490e6a199bf0c6d5106a511b70))
* **Observatoire:** ajouter dans l'url les filtres sélectionnés ([#5595](https://github.com/betagouv/ma-cantine/issues/5595)) ([0bb1cc0](https://github.com/betagouv/ma-cantine/commit/0bb1cc0bb001483a58e2fbe3d85990adacefbe91))
* **Observatoire:** création du bloc pour afficher les graphiques des cantines ([#5587](https://github.com/betagouv/ma-cantine/issues/5587)) ([9e28b2c](https://github.com/betagouv/ma-cantine/commit/9e28b2ca2d90fb5fa90ba4e50a377528119340c3))


### Améliorations

* **Admin:** permet la suppression du cache depuis l'admin ([#5586](https://github.com/betagouv/ma-cantine/issues/5586)) ([8296442](https://github.com/betagouv/ma-cantine/commit/829644258c8f48aeda2d0e47f0ea47cc55c3628b))
* **API Stats:** renvoyer les objectifs EGalim DROM si une region correspond ([#5590](https://github.com/betagouv/ma-cantine/issues/5590)) ([e5bb9d4](https://github.com/betagouv/ma-cantine/commit/e5bb9d47796ed2eb4ae63cd93e7c93a531440cbc))


### Corrections (bugs, typos...)

* **CI:** répare la récuparation du language-pack-fr pour les tests ([#5584](https://github.com/betagouv/ma-cantine/issues/5584)) ([3935a1f](https://github.com/betagouv/ma-cantine/commit/3935a1f265a8a48f4161e398d336033a24293dfb))
* **Observatoire:** améliore l'affichage des graphiques des cantines ([#5594](https://github.com/betagouv/ma-cantine/issues/5594)) ([cd7ac50](https://github.com/betagouv/ma-cantine/commit/cd7ac50f982198e428dd1bac8dd3435a1d2a487f))
* **Observatoire:** mise à jour des jeux de données géographiques ([#5598](https://github.com/betagouv/ma-cantine/issues/5598)) ([f0f53c5](https://github.com/betagouv/ma-cantine/commit/f0f53c5d4558e6d53f1636bb26d168531b5c38e9))


### Technique

* **Objectifs EGalim:** enrichir l'objet EGALIM_OBJECTIVES avec les chiffres des DROM ([#5589](https://github.com/betagouv/ma-cantine/issues/5589)) ([7bbaf00](https://github.com/betagouv/ma-cantine/commit/7bbaf0051340be5563641f6e7c016c1e2bae06c8))
* **Télédéclaration:** déplacer le queryset pourcentage bio & egalim des achats dans le modèle + tests ([#5582](https://github.com/betagouv/ma-cantine/issues/5582)) ([d4a7579](https://github.com/betagouv/ma-cantine/commit/d4a7579379544cd4f6eb3b8e93f474d2b0ee9f5c))

## [2025.26.0](https://github.com/betagouv/ma-cantine/compare/v2025.25.0...v2025.26.0) (2025-08-05)


### Nouveautés

* **Observatoire:** affiche un message d'erreur si pas de filtres ([#5553](https://github.com/betagouv/ma-cantine/issues/5553)) ([1cbab5a](https://github.com/betagouv/ma-cantine/commit/1cbab5a38ee1f8adc587b079c24c53e687bad474))
* **Observatoire:** ajout d'une description au graphique produit de qualité dont bio ([#5573](https://github.com/betagouv/ma-cantine/issues/5573)) ([00dab60](https://github.com/betagouv/ma-cantine/commit/00dab60d44848232e6f4be7f162dda2dcb594fc5))
* **Observatoire:** ajout du graphique des viandes origine France ([#5578](https://github.com/betagouv/ma-cantine/issues/5578)) ([e992cc0](https://github.com/betagouv/ma-cantine/commit/e992cc034d63821773f1514b7957de35809fd28b))
* **Observatoire:** ajoute le graphique des viandes et poissons EGalim ([#5577](https://github.com/betagouv/ma-cantine/issues/5577)) ([b5e31f2](https://github.com/betagouv/ma-cantine/commit/b5e31f2f0c443308fe8164f3996d3af89e8024b3))
* **Observatoire:** création du bloc pour afficher les graphiques des produits durables et de qualité ([#5556](https://github.com/betagouv/ma-cantine/issues/5556)) ([2815c6b](https://github.com/betagouv/ma-cantine/commit/2815c6b1e8e079d33f996901e86a4795bcfad3f6))
* **Observatoire:** intégration et redesign du graphique "Produits durables et de qualité" en jauge ([#5570](https://github.com/betagouv/ma-cantine/issues/5570)) ([f397dde](https://github.com/betagouv/ma-cantine/commit/f397ddee4790a4cdd80dd90ca373ec35cf2de929))
* **Observatoire:** intègre les notes renvoyées par l'api ([#5581](https://github.com/betagouv/ma-cantine/issues/5581)) ([afac570](https://github.com/betagouv/ma-cantine/commit/afac570572af47f9cc8fed94837266639de6c92d))


### Améliorations

* **API Stats:** mettre de la documentation sous forme de notes dans la réponse API (cas des armée, canteen_count date) ([#5542](https://github.com/betagouv/ma-cantine/issues/5542)) ([500f731](https://github.com/betagouv/ma-cantine/commit/500f7314a488b782dd4ef1085c3535295bc1f251))
* **API Stats:** ne pas renvoyer les stats détaillées TD si le rapport pour l'année en cours n'a pas été publié ([#5580](https://github.com/betagouv/ma-cantine/issues/5580)) ([4383f41](https://github.com/betagouv/ma-cantine/commit/4383f410df5f06cb9c6af95cef563a870d339f81))
* **API Stats:** renvoyer les objectifs EGalim sous forme de notes ([#5572](https://github.com/betagouv/ma-cantine/issues/5572)) ([b16ae97](https://github.com/betagouv/ma-cantine/commit/b16ae9734a4502ca3b58ed825bcadd782b8d52d5))
* **Cantines:** nouveau queryset pour exclure facilement les livreurs de repas (avec ou sans convives) ([#5574](https://github.com/betagouv/ma-cantine/issues/5574)) ([fcc3103](https://github.com/betagouv/ma-cantine/commit/fcc3103d3f106e60ed2b88ce7b650041307ab85a))
* **Dates de campagne:** ajout du lien vers le rapport annuel ([#5552](https://github.com/betagouv/ma-cantine/issues/5552)) ([b829a43](https://github.com/betagouv/ma-cantine/commit/b829a43eadf1ac89af3b5b785b2b841001310d8a))
* **Diagnostic:** nouveau champ pour stocker le status [#1](https://github.com/betagouv/ma-cantine/issues/1)TD1site ([#5571](https://github.com/betagouv/ma-cantine/issues/5571)) ([3fa62e5](https://github.com/betagouv/ma-cantine/commit/3fa62e51f87df641d503a907d95287281ec1a708))
* **Metabase:** Ajouts des champs gaspis dans l'extraction des Teledeclarations ([#5547](https://github.com/betagouv/ma-cantine/issues/5547)) ([da36d1d](https://github.com/betagouv/ma-cantine/commit/da36d1df5147c01c391c41501ca405a7fdfc889e))


### Corrections (bugs, typos...)

* **ETL:** Gestions des valeurs None pour l'Analysis TD ([#5558](https://github.com/betagouv/ma-cantine/issues/5558)) ([1c34aca](https://github.com/betagouv/ma-cantine/commit/1c34acafd799f485227e62e3f1ec2afc6a7f27ed))
* **Observatoire:** améliorations diverses ([#5579](https://github.com/betagouv/ma-cantine/issues/5579)) ([2d41acb](https://github.com/betagouv/ma-cantine/commit/2d41acb282744e92a82a22dac763c8277fbb42a9))
* **Observatoire:** corrige l'affichage des 3 premiers blocs des résultats ([#5550](https://github.com/betagouv/ma-cantine/issues/5550)) ([a0e8eda](https://github.com/betagouv/ma-cantine/commit/a0e8eda2225f68119a04a977b246362670616c6e))
* **Observatoire:** le chiffre des pourcentages de produits de durables inclu le bio ([#5575](https://github.com/betagouv/ma-cantine/issues/5575)) ([ccd65a4](https://github.com/betagouv/ma-cantine/commit/ccd65a4424ece83842494f35546331e84fff19cd))


### Technique

* **Observatoire:** renomme les composants ([#5557](https://github.com/betagouv/ma-cantine/issues/5557)) ([65acb74](https://github.com/betagouv/ma-cantine/commit/65acb742c8b766de43cbcd5bcc1b0886503ed1cb))

## [2025.25.0](https://github.com/betagouv/ma-cantine/compare/v2025.24.2...v2025.25.0) (2025-07-30)


### Nouveautés

* **API Stats:** le nombre de cantines est maintenant filtré par leur année de création ([#5536](https://github.com/betagouv/ma-cantine/issues/5536)) ([4048df9](https://github.com/betagouv/ma-cantine/commit/4048df9b97c5d3ad6f0f10de2a8d15dd14309be1))
* **Bilans annuels:** héberge les bilans annuels sur l'application  ([#5549](https://github.com/betagouv/ma-cantine/issues/5549)) ([6e549fc](https://github.com/betagouv/ma-cantine/commit/6e549fc30c9b74f77a56d2509f0cdc486869c438))
* **Cantines:** nouveau queryset pour filtrer par année de création (à la date de fin de la campagne) ([#5535](https://github.com/betagouv/ma-cantine/issues/5535)) ([c355ee9](https://github.com/betagouv/ma-cantine/commit/c355ee97f643b94dd2082a469121273268aa42a6))
* **Observatoire:** affichage des filtres ([#5528](https://github.com/betagouv/ma-cantine/issues/5528)) ([9b9ab99](https://github.com/betagouv/ma-cantine/commit/9b9ab9989901a7f3fd2a98a6ff0c2ca17adc0df1))
* **Observatoire:** affiche le bandeau d'information des armées ([#5539](https://github.com/betagouv/ma-cantine/issues/5539)) ([db9ad5f](https://github.com/betagouv/ma-cantine/commit/db9ad5fd01c1af2dcbea6a0e3f5d7a45520666b0))
* **Observatoire:** affiche les filtres sélectionnés ([#5538](https://github.com/betagouv/ma-cantine/issues/5538)) ([7b5b682](https://github.com/betagouv/ma-cantine/commit/7b5b682efafc3368a73f952e29784bb0753beded))
* **Observatoire:** affiche nombre de cantines, nombre de télédéclarations et le lien pour retrouver les cantines ([#5546](https://github.com/betagouv/ma-cantine/issues/5546)) ([8133ced](https://github.com/betagouv/ma-cantine/commit/8133ced6eff20ee9c7067b2946de5d64fcffeff0))
* **Observatoire:** ajoute les contenus de l'en-tête de page ([#5530](https://github.com/betagouv/ma-cantine/issues/5530)) ([ca6a3e8](https://github.com/betagouv/ma-cantine/commit/ca6a3e8e31f875596fca5b325e0cd169f52148c8))
* **Observatoire:** connecte les filtres à l'API ([#5543](https://github.com/betagouv/ma-cantine/issues/5543)) ([57df665](https://github.com/betagouv/ma-cantine/commit/57df665fff6fb802a2f211c3c713dc87427c6417))


### Améliorations

* **Cantines:** Admin: utiliser declaration_donnees_YEAR pour la colonne 'Télédéclarée' ([#5524](https://github.com/betagouv/ma-cantine/issues/5524)) ([1b06b60](https://github.com/betagouv/ma-cantine/commit/1b06b604650a8fb6837533873116e93c3a94bb1b))
* **ETL:** Ajout des champs declaration_campagne_YEAR dans TD analysis ([#5529](https://github.com/betagouv/ma-cantine/issues/5529)) ([0d66ed8](https://github.com/betagouv/ma-cantine/commit/0d66ed8551ced1944b78f0525c55675cdb5f493c))
* **ETL:** Extraire les secteurs/categories depuis declared_data ([#5523](https://github.com/betagouv/ma-cantine/issues/5523)) ([cfdc8f2](https://github.com/betagouv/ma-cantine/commit/cfdc8f20f318fdcbfa9ccd323d4fd0c15362e65f))
* **ETL:** TD analysis: Ajout du champ creation_source (à partir du Diagnostic) ([#5540](https://github.com/betagouv/ma-cantine/issues/5540)) ([95f4526](https://github.com/betagouv/ma-cantine/commit/95f452613cf6b491286f360c4e1b080a4b623190))


### Corrections (bugs, typos...)

* **Cantines:** Admin: typo qui provoquait une erreur pour l'affichage de 'Télédéclarée' ([#5545](https://github.com/betagouv/ma-cantine/issues/5545)) ([30b8d5c](https://github.com/betagouv/ma-cantine/commit/30b8d5cc8d25382b1a9b93d110d019c3dc822ba5))
* **Cantines:** répare la commande qui remplit le champ declaration_donnees_YEAR (suite à la valeur par défaut à False) + ajout de tests ([#5526](https://github.com/betagouv/ma-cantine/issues/5526)) ([59ebf46](https://github.com/betagouv/ma-cantine/commit/59ebf4678249e69d08aba9bd4c0831bd6672a136))
* **ETL:** Enlever la TD d'un satellite en cas de doublon avec cuisine centrale ([#5533](https://github.com/betagouv/ma-cantine/issues/5533)) ([471d6eb](https://github.com/betagouv/ma-cantine/commit/471d6eb91fd9f3755226ecb9ad0662c095355bc0))
* **Observatoire:** différents correctifs et améliorations sur le comportement des filtres ([#5548](https://github.com/betagouv/ma-cantine/issues/5548)) ([bc52229](https://github.com/betagouv/ma-cantine/commit/bc522296cc6824411c9a73cbb1782c9de641ff22))
* **Observatoire:** petits correctifs sur l'affichage des filtres et refactoring du code ([#5541](https://github.com/betagouv/ma-cantine/issues/5541)) ([6565c2e](https://github.com/betagouv/ma-cantine/commit/6565c2ead2b6f119cc8c828af611ba9476dda0d3))
* **Utilisateur:** Admin: mettre le champ last_login en lecture-seule ([#5544](https://github.com/betagouv/ma-cantine/issues/5544)) ([38b8086](https://github.com/betagouv/ma-cantine/commit/38b8086e394b967e85512566f6206a11beae819f))


### Technique

* **API Stats:** Réorganise un peu les tests ([#5537](https://github.com/betagouv/ma-cantine/issues/5537)) ([99a9d53](https://github.com/betagouv/ma-cantine/commit/99a9d534b51b289db65cae3c83361d92b81af8c2))
* **Geo:** script pour générer la liste des régions, départements, pat, epci et communes en fichier JSON ([#5521](https://github.com/betagouv/ma-cantine/issues/5521)) ([9eb6a4a](https://github.com/betagouv/ma-cantine/commit/9eb6a4ab43cefb6b4d8ce4d8c50e055e895a845e))

## [2025.24.2](https://github.com/betagouv/ma-cantine/compare/v2025.24.1...v2025.24.2) (2025-07-11)


### Améliorations

* **API Stats:** TD: renvoyer le taux de viande egalim, viande france & aquaculture egalim ([#5506](https://github.com/betagouv/ma-cantine/issues/5506)) ([d806ecd](https://github.com/betagouv/ma-cantine/commit/d806ecdddb472ff7e9119417dd8500a2e11a8520))


### Corrections (bugs, typos...)

* **Cantines:** initialiser les nouveaux champs declaration_donnees_YEAR à False pour les nouvelles cantines ([#5519](https://github.com/betagouv/ma-cantine/issues/5519)) ([2242979](https://github.com/betagouv/ma-cantine/commit/2242979d06ee09c3d2a2452e8b0c43b002aedc9d))
* **Open Data:** TD: renomme declaration_donnees_2024_en_cours en declaration_donnees_2024 ([#5517](https://github.com/betagouv/ma-cantine/issues/5517)) ([c8fa897](https://github.com/betagouv/ma-cantine/commit/c8fa8971d658210680909a5989a49ab0972ff117))


### Technique

* **Cantines:** enlever le code obsolète lié à la logique "publication" (PUBLISH_BY_DEFAULT) ([#5502](https://github.com/betagouv/ma-cantine/issues/5502)) ([7df379e](https://github.com/betagouv/ma-cantine/commit/7df379e1148fd40abb665dd05d329e3cf0dcaada))
* **Cantines:** enlever le code obsolète lié à la logique publication (champ DB publication_status) ([#5507](https://github.com/betagouv/ma-cantine/issues/5507)) ([d7cd50f](https://github.com/betagouv/ma-cantine/commit/d7cd50f9ec06a06fb88fbb09e8618f1e87cbb55a))
* créer la table de cache avec une migration ([#5525](https://github.com/betagouv/ma-cantine/issues/5525)) ([5d98215](https://github.com/betagouv/ma-cantine/commit/5d98215fe431858f1bd43df628ce39b3ac4f7dbe))
* stocker le cache en DB au lieu de mémoire ([#5518](https://github.com/betagouv/ma-cantine/issues/5518)) ([1a5ef8e](https://github.com/betagouv/ma-cantine/commit/1a5ef8e54fa44682e9a64222a03cc37782e0ccd8))

## [2025.24.1](https://github.com/betagouv/ma-cantine/compare/v2025.24.0...v2025.24.1) (2025-07-09)


### Améliorations

* **Metabase:** ajoute le champ spe dans les exports TD ([#5426](https://github.com/betagouv/ma-cantine/issues/5426)) ([1b04bb9](https://github.com/betagouv/ma-cantine/commit/1b04bb9fe224d98758fa2bc7e45cd98c7e2cf246))


### Documentation

* mise à jour de la doc Vue3 et Makefile ([#5515](https://github.com/betagouv/ma-cantine/issues/5515)) ([3a772ea](https://github.com/betagouv/ma-cantine/commit/3a772ead81f0296bc77f93221eaea9fce1988cf3))


### Technique

* **API Stats:** mettre en place un cache pour accélérer le chargement de la page (sans filtre sélectionné) ([#5482](https://github.com/betagouv/ma-cantine/issues/5482)) ([30f5a15](https://github.com/betagouv/ma-cantine/commit/30f5a153fc5b2d32c1e748dcb6571546e018990d))
* **deps:** Maj Django 5.0.1 -&gt; Django 5.1.0 ([#5501](https://github.com/betagouv/ma-cantine/issues/5501)) ([c6ee0d3](https://github.com/betagouv/ma-cantine/commit/c6ee0d3b8b64f815b9ab18404ceaf26dfb2e52ba))
* **Vue 3:** renomme les pages ([#5508](https://github.com/betagouv/ma-cantine/issues/5508)) ([f9d1175](https://github.com/betagouv/ma-cantine/commit/f9d1175f143bb6f40168b074df0f6e73dd7293ce))

## [2025.24.0](https://github.com/betagouv/ma-cantine/compare/v2025.23.2...v2025.24.0) (2025-07-07)


### Nouveautés

* **Cantines:** nouveaux champs declaration_donnees_YEAR pour stocker l'info si la cantine a télédéclarée pour cette année là ([#5416](https://github.com/betagouv/ma-cantine/issues/5416)) ([a7b431f](https://github.com/betagouv/ma-cantine/commit/a7b431ffe58709399b6758d33f246c4acbe9e47d))


### Améliorations

* **API Stats:** TD: renvoyer le taux egalim des achats (somme de bio + durable) ([#5504](https://github.com/betagouv/ma-cantine/issues/5504)) ([d9b736c](https://github.com/betagouv/ma-cantine/commit/d9b736cf75c8cdfcfaf6e7a6f6077513583482b7))
* **Cantines:** Commande pour remplir le champ declaration_donnees_YEAR ([#5450](https://github.com/betagouv/ma-cantine/issues/5450)) ([976bd77](https://github.com/betagouv/ma-cantine/commit/976bd771482223b1290d65c9748ac671e032e593))
* **Django:** Préparer la migration vers Django 5.1 en corrigeant les éléments dépréciés ([#5485](https://github.com/betagouv/ma-cantine/issues/5485)) ([b9dc65a](https://github.com/betagouv/ma-cantine/commit/b9dc65aa43c089ed23c683c7e7000a910678e197))
* **Metabase:** Cantines: ajout des nouveaux champs declaration_donnees_YEAR dans l'export ([#5449](https://github.com/betagouv/ma-cantine/issues/5449)) ([bc0399b](https://github.com/betagouv/ma-cantine/commit/bc0399b58507a9aaaa37f5824174c5b0f08e01c5))
* **Open Data:** Cantines: maj des champs declaration_donnees_YEAR dans l'export ([#5460](https://github.com/betagouv/ma-cantine/issues/5460)) ([790d68e](https://github.com/betagouv/ma-cantine/commit/790d68e223362bc37259db100f55ec14de78f20d))


### Corrections (bugs, typos...)

* **ETL:** Maintenir les valeurs égales à 0 au lieu de les transformer en null ([#5484](https://github.com/betagouv/ma-cantine/issues/5484)) ([f2015c2](https://github.com/betagouv/ma-cantine/commit/f2015c24219e000a77e390da66abfc372fffc2fa))
* **ETL:** Ne plus ecraser les valeurs égales à 0 par None pour les champs issus du declared data ([#5511](https://github.com/betagouv/ma-cantine/issues/5511)) ([a685327](https://github.com/betagouv/ma-cantine/commit/a685327df7b6188d14ea98aebe2a1354860b827c))


### Technique

* **API Stats:** TD: petit ménage avant d'ajouter de nouvelles stats ([#5503](https://github.com/betagouv/ma-cantine/issues/5503)) ([235da94](https://github.com/betagouv/ma-cantine/commit/235da940d59dc49265c120dd077c9e0c991291ef))
* **deps-dev:** bump @vitejs/plugin-vue in /2024-frontend ([7503985](https://github.com/betagouv/ma-cantine/commit/75039852ca76340583db4b2f593241844e8ec98d))
* **deps-dev:** bump eslint from 9.28.0 to 9.30.0 in /2024-frontend ([aeaabc4](https://github.com/betagouv/ma-cantine/commit/aeaabc4b3945a9919731a722779024ce5ffb5b0a))
* **deps:** bump factory-boy from 3.3.1 to 3.3.3 ([#5487](https://github.com/betagouv/ma-cantine/issues/5487)) ([0ad0469](https://github.com/betagouv/ma-cantine/commit/0ad0469bdd6a4c214b1e9347ea46325f5adf47d2))
* **deps:** bump pinia from 3.0.2 to 3.0.3 in /2024-frontend ([7db4cd9](https://github.com/betagouv/ma-cantine/commit/7db4cd9c6eeb1def09f6bc2b51ff22354aa48b65))
* **deps:** bump pipdeptree from 2.23.4 to 2.26.1 ([#5492](https://github.com/betagouv/ma-cantine/issues/5492)) ([ba9a14a](https://github.com/betagouv/ma-cantine/commit/ba9a14ab476c8fa0f4c28ab3837133f2beadbad1))
* **deps:** bump six from 1.16.0 to 1.17.0 ([#5497](https://github.com/betagouv/ma-cantine/issues/5497)) ([fc641c8](https://github.com/betagouv/ma-cantine/commit/fc641c864434579cc3ce93e641f87071f8520260))
* **deps:** bump vue-i18n from 11.1.5 to 11.1.7 in /2024-frontend ([#5488](https://github.com/betagouv/ma-cantine/issues/5488)) ([d041d96](https://github.com/betagouv/ma-cantine/commit/d041d964e7f35c13411be309820f4420f4efee65))
* **deps:** bump wrapt from 1.17.0 to 1.17.2 ([#5491](https://github.com/betagouv/ma-cantine/issues/5491)) ([1889436](https://github.com/betagouv/ma-cantine/commit/188943670cf4e139a92f2b7ca0e75ff01b83f03f))
* **Storage:** ATTENTION CHANGEMENT VARENV CC Uniformiser la variable du storage backend S3 ([#5513](https://github.com/betagouv/ma-cantine/issues/5513)) ([ab9fcfe](https://github.com/betagouv/ma-cantine/commit/ab9fcfed48e7e02353c9d154696c2c70bac45365))
* **Tests:** enlever les warning '_date received a naive datetime' ([#5512](https://github.com/betagouv/ma-cantine/issues/5512)) ([c0c90a5](https://github.com/betagouv/ma-cantine/commit/c0c90a5eaf4387673304ee7a954ea26121096046))
* **Tests:** enlever les warning 'min_value should be a Decimal instance' ([#5514](https://github.com/betagouv/ma-cantine/issues/5514)) ([0e7cbfa](https://github.com/betagouv/ma-cantine/commit/0e7cbfa221d8ab6af8fd7243d058930c86a090d4))

## [2025.23.2](https://github.com/betagouv/ma-cantine/compare/v2025.23.1...v2025.23.2) (2025-06-30)


### Technique

* **uv:** ajoute uv comme gestionnaire de dépendances pour Python ([#5437](https://github.com/betagouv/ma-cantine/issues/5437)) ([696f02e](https://github.com/betagouv/ma-cantine/commit/696f02ea12e536e5ccf7a21fe6006ed52e0f2476))

## [2025.23.1](https://github.com/betagouv/ma-cantine/compare/v2025.23.0...v2025.23.1) (2025-06-27)


### Améliorations

* **Admin:** améliore la recherche dans la page des cantines ([#5479](https://github.com/betagouv/ma-cantine/issues/5479)) ([78eb4fb](https://github.com/betagouv/ma-cantine/commit/78eb4fb5495c647af14c97d66b755ece5db66bd2))
* **Admin:** facilite la suppression d'un lien cantine - gestionnaire ([#5477](https://github.com/betagouv/ma-cantine/issues/5477)) ([266eca6](https://github.com/betagouv/ma-cantine/commit/266eca68928b1666b36b87f416a5286d63468a79))


### Corrections (bugs, typos...)

* **Gaspillage alimentaire:** corrige l'affichage des vues graphiques ([#5480](https://github.com/betagouv/ma-cantine/issues/5480)) ([4504226](https://github.com/betagouv/ma-cantine/commit/4504226bf3af35bdd749f4941beda8cc960250a5))


### Technique

* **API Stats:** gros refactoring sur la view et le serializer ([#5478](https://github.com/betagouv/ma-cantine/issues/5478)) ([5069ea2](https://github.com/betagouv/ma-cantine/commit/5069ea21ba6a9b3e2d1640401667229a353e1378))

## [2025.23.0](https://github.com/betagouv/ma-cantine/compare/v2025.22.0...v2025.23.0) (2025-06-24)


### Nouveautés

* **API Stats:** nouveau filtre par commune(s) ([#5424](https://github.com/betagouv/ma-cantine/issues/5424)) ([d867f65](https://github.com/betagouv/ma-cantine/commit/d867f655f2d770234d80b12c0e4cba50f98104f9))
* **API Stats:** nouvelles stats avec la répartition du nombre de cantines par mode de gestion ([#5469](https://github.com/betagouv/ma-cantine/issues/5469)) ([1ccafb5](https://github.com/betagouv/ma-cantine/commit/1ccafb5a724811df414a27a22f58e6b9735aeddb))
* **API Stats:** nouvelles stats avec la répartition du nombre de cantines par mode de production ([#5472](https://github.com/betagouv/ma-cantine/issues/5472)) ([047d7be](https://github.com/betagouv/ma-cantine/commit/047d7befd2fd8f56082e3e1a68044fe0c313cf64))
* **API Stats:** nouvelles stats avec la répartition du nombre de cantines par secteur économique ([#5473](https://github.com/betagouv/ma-cantine/issues/5473)) ([4913509](https://github.com/betagouv/ma-cantine/commit/491350941d860f2a289fa83e6399a22b6704306d))


### Améliorations

* **Admin:** ajoute les liens des cantines satellites depuis la page de la cuisine centrale ([#5471](https://github.com/betagouv/ma-cantine/issues/5471)) ([cafaa57](https://github.com/betagouv/ma-cantine/commit/cafaa57d87c26cd116904ca62b3b142fb45902d8))
* **API Stats:** Filter les cantines rattachées au ministère de tutelle ARMEE ([#5468](https://github.com/betagouv/ma-cantine/issues/5468)) ([5f0ae80](https://github.com/betagouv/ma-cantine/commit/5f0ae80e4a8939f8a605f428b00f2746d07c51d3))
* **ETL:** Réconcilier les noms historiques et actuels des secteurs ([#5475](https://github.com/betagouv/ma-cantine/issues/5475)) ([c9ba00e](https://github.com/betagouv/ma-cantine/commit/c9ba00e0d451b5d5ba80216762a23ffba346148d))


### Corrections (bugs, typos...)

* **ETL:** Utiliser le yearly meal count de la cc ([#5470](https://github.com/betagouv/ma-cantine/issues/5470)) ([5881437](https://github.com/betagouv/ma-cantine/commit/58814377bdae3f7d23da089809dbd03a68e2570a))


### Documentation

* Ajoute 3 documents (Gitbook &gt; Guide d'aide) ([#5476](https://github.com/betagouv/ma-cantine/issues/5476)) ([89305ee](https://github.com/betagouv/ma-cantine/commit/89305ee12428fc72459bb76daed44144e6f6f376))
* **API:** Clarifier l'accessibilité des endpoint publics/privés ([#5465](https://github.com/betagouv/ma-cantine/issues/5465)) ([8a52ed2](https://github.com/betagouv/ma-cantine/commit/8a52ed2adf6d5e8061370ae4070a9aa7ce0777ca))


### Technique

* **deps:** bump requests from 2.32.3 to 2.32.4 ([#5438](https://github.com/betagouv/ma-cantine/issues/5438)) ([2a427dc](https://github.com/betagouv/ma-cantine/commit/2a427dcda865ea47786bb5e53601ca66511251b2))
* **Télédéclarations:** Nouveau queryset publicly_visible. Ajout de tests ([#5467](https://github.com/betagouv/ma-cantine/issues/5467)) ([887ba5b](https://github.com/betagouv/ma-cantine/commit/887ba5bf1e87fa59c25f8d5545021b2ac519a248))

## [2025.22.0](https://github.com/betagouv/ma-cantine/compare/v2025.21.1...v2025.22.0) (2025-06-23)


### Nouveautés

* **API Stats:** nouveau filtre par mode(s) de gestion ([#5463](https://github.com/betagouv/ma-cantine/issues/5463)) ([4309a8b](https://github.com/betagouv/ma-cantine/commit/4309a8b547d71b5952cedff8899a45cdcaa5bd1e))
* **API Stats:** nouveau filtre par mode(s) de production ([#5462](https://github.com/betagouv/ma-cantine/issues/5462)) ([c62612c](https://github.com/betagouv/ma-cantine/commit/c62612c0c132c52d219959586297815affe48129))
* **API Stats:** nouveau filtre par secteur(s) économique ([#5464](https://github.com/betagouv/ma-cantine/issues/5464)) ([838dfe2](https://github.com/betagouv/ma-cantine/commit/838dfe2c447dd8261e198300916eda7bc9de682a))
* **Statistiques des cantines:** création de la future page de statistiques en vue3 ([#5447](https://github.com/betagouv/ma-cantine/issues/5447)) ([b381a2e](https://github.com/betagouv/ma-cantine/commit/b381a2e5eda45026c95e3984151633cca1930402))


### Améliorations

* **Admin:** Pretty json pour le champ declared_data dans Teledeclaration 🔥 ([#5456](https://github.com/betagouv/ma-cantine/issues/5456)) ([7882cc2](https://github.com/betagouv/ma-cantine/commit/7882cc24c12009c41f2c25cdec3318bec02c0169))
* **API Stats:** optimise le calcul du nombre de cantines par catégorie de secteur ([#5448](https://github.com/betagouv/ma-cantine/issues/5448)) ([b5216b4](https://github.com/betagouv/ma-cantine/commit/b5216b4ed20215878fc0434294e6813b9b22266d))
* **ETL:** Convertir les valeurs numériques issues du champ declared_data en float ([#5455](https://github.com/betagouv/ma-cantine/issues/5455)) ([1d97c99](https://github.com/betagouv/ma-cantine/commit/1d97c993bf953d2e963533333d12a60232bddead))
* **ETL:** Remplir les champs vides de diagnostic_type par la valeur SIMPLE ([#5452](https://github.com/betagouv/ma-cantine/issues/5452)) ([e570cac](https://github.com/betagouv/ma-cantine/commit/e570cac0052e402394902d3ea76fdef8361f58a4))


### Corrections (bugs, typos...)

* **ETL:** Corriger col genere_par_cuisine_centrale ([#5451](https://github.com/betagouv/ma-cantine/issues/5451)) ([89ed13c](https://github.com/betagouv/ma-cantine/commit/89ed13ce831ae26d5d313012ea953fe39932bc28))
* **ETL:** Les valeurs yearly_meal_count vides des satelittes étaient remplacées par la valeur de la CC  ([#5461](https://github.com/betagouv/ma-cantine/issues/5461)) ([84f027e](https://github.com/betagouv/ma-cantine/commit/84f027ee4d4d83fafaf7fed94110292b7274bfc2))
* **ETL:** Suppression doublons TD CC & CSAT ([#5459](https://github.com/betagouv/ma-cantine/issues/5459)) ([2242bf3](https://github.com/betagouv/ma-cantine/commit/2242bf364231a65954c3c5ea8cc9335de3a6c424))
* **Statistiques des cantines:** corrige l'affichage du pictogramme dans la tuile téléchargement ([#5454](https://github.com/betagouv/ma-cantine/issues/5454)) ([0144d1a](https://github.com/betagouv/ma-cantine/commit/0144d1a9ebc49cc438ce437ffedce9477fecc551))


### Technique

* **API Stats:** réorganise un peu les tests ([#5446](https://github.com/betagouv/ma-cantine/issues/5446)) ([4c930ea](https://github.com/betagouv/ma-cantine/commit/4c930ea8477734725af0d96b4d7ba87d0a2770b6))

## [2025.21.1](https://github.com/betagouv/ma-cantine/compare/v2025.21.0...v2025.21.1) (2025-06-16)


### Améliorations

* **ETL:** Ajout colonne mode de télédéclaration dans Analysis TD ([#5445](https://github.com/betagouv/ma-cantine/issues/5445)) ([e4a4074](https://github.com/betagouv/ma-cantine/commit/e4a4074e9c7161bd82e0d8bab8da0f4b3df2abee))


### Corrections (bugs, typos...)

* **API Stats:** améliore la documentation du filtre PAT ([#5439](https://github.com/betagouv/ma-cantine/issues/5439)) ([99d650e](https://github.com/betagouv/ma-cantine/commit/99d650e37b503ca1144f841878ae46942a460d39))
* **ETL:** Corriger le champ diagnostic_type ([#5444](https://github.com/betagouv/ma-cantine/issues/5444)) ([bbd81fa](https://github.com/betagouv/ma-cantine/commit/bbd81fac9ba4fb402ee45d4c09e54b511d92249c))
* **ETL:** Ne pas filtrer les cantines sur le secteur armee/police/gendarmerie pour export open-data des cantines ([#5443](https://github.com/betagouv/ma-cantine/issues/5443)) ([b3f1ae6](https://github.com/betagouv/ma-cantine/commit/b3f1ae661bc38567dc715763ecd18a9587ec9b42))
* **ETL:** remet une ligne commentée qui empêchait l'export ([#5440](https://github.com/betagouv/ma-cantine/issues/5440)) ([79352e3](https://github.com/betagouv/ma-cantine/commit/79352e3bbcbeb66dfc8cd9e9d63b750111761807))
* **Foire aux questions:** corrige les accordéons qui ne s'ouvrent plus ([#5442](https://github.com/betagouv/ma-cantine/issues/5442)) ([84c9569](https://github.com/betagouv/ma-cantine/commit/84c9569e61e89816d05c87317f9bd7450412a751))
* **Imports:** Cantines: corrige le format SIRET du fichier d'exemple ([#5441](https://github.com/betagouv/ma-cantine/issues/5441)) ([a82275e](https://github.com/betagouv/ma-cantine/commit/a82275e8213e97a8a5aa91558f221aed593ca9db))
* **Tableau de bord:** corrige la recherche par nom de cantine ([#5430](https://github.com/betagouv/ma-cantine/issues/5430)) ([55f382b](https://github.com/betagouv/ma-cantine/commit/55f382bd06723a12ecda34729eca27b22e28e002))
* **Tableau de bord:** permet de rechercher une cantine par numéro siret ou siren uniquement en vue carte ([#5436](https://github.com/betagouv/ma-cantine/issues/5436)) ([4bd4a67](https://github.com/betagouv/ma-cantine/commit/4bd4a67b446d4bb7bb6d689917b6993167f191f1))
* **Trouver une cantine:** corrige le filtre par donnée d'approvisionnement ([#5434](https://github.com/betagouv/ma-cantine/issues/5434)) ([5aeb6e3](https://github.com/betagouv/ma-cantine/commit/5aeb6e335ecbd1ecc95ec6d751265f900522e47e))


### Technique

* **deps:** bump freezegun from 1.5.1 to 1.5.2 ([#5392](https://github.com/betagouv/ma-cantine/issues/5392)) ([d1d94c2](https://github.com/betagouv/ma-cantine/commit/d1d94c27328e51121e998f408f8b1e3b1964f03d))

## [2025.21.0](https://github.com/betagouv/ma-cantine/compare/v2025.20.0...v2025.21.0) (2025-06-05)


### Nouveautés

* **API Stats:** nouveau filtre par PAT(s) ([#5423](https://github.com/betagouv/ma-cantine/issues/5423)) ([cd3e523](https://github.com/betagouv/ma-cantine/commit/cd3e5232d94f7215eab6a77336607b181680751d))


### Améliorations

* **API Stats:** mieux documenter la possibilité de faire des filtres multiples ([#5419](https://github.com/betagouv/ma-cantine/issues/5419)) ([69190cd](https://github.com/betagouv/ma-cantine/commit/69190cd17f490b2bba1d1b69a13173bf2b41e609))
* **API Stats:** simplifier la façon de filter par EPCI(s) ([#5422](https://github.com/betagouv/ma-cantine/issues/5422)) ([1a8bbe7](https://github.com/betagouv/ma-cantine/commit/1a8bbe7e0ff60f9fbdea0f81299b539250d7bbdd))
* **ETL:** Ajout champ SIREN unite legale ([#5428](https://github.com/betagouv/ma-cantine/issues/5428)) ([2a772b1](https://github.com/betagouv/ma-cantine/commit/2a772b19fae5cbb7153acfd396c0778ca0a5218a))


### Corrections (bugs, typos...)

* **API Stats:** typo sur le nom des filtres dans la doc ([#5418](https://github.com/betagouv/ma-cantine/issues/5418)) ([9a6ba6d](https://github.com/betagouv/ma-cantine/commit/9a6ba6d0857cc3ba45da26f3cf0ee8d897824840))
* **Cantines:** basculer la notion de SPE sur les line_ministry au lieu des sectors ([#5346](https://github.com/betagouv/ma-cantine/issues/5346)) ([8285e4d](https://github.com/betagouv/ma-cantine/commit/8285e4da46277f14191de998a7c083639d8f5431))
* **ETL:** Changer en int le selector de l'argument dans la commande ([#5432](https://github.com/betagouv/ma-cantine/issues/5432)) ([932718a](https://github.com/betagouv/ma-cantine/commit/932718a44dd1e1ba6550376da4073004196d9b83))
* **Header:** corrige l'affichage étiré du logo dans le header sur safari ([#5431](https://github.com/betagouv/ma-cantine/issues/5431)) ([6deaac2](https://github.com/betagouv/ma-cantine/commit/6deaac220eca90521a2df02d0aaf8c8c77fd2ce5))
* **Metabase:** répare les tests suite aux modifs sur le calcul du champ SPE ([#5425](https://github.com/betagouv/ma-cantine/issues/5425)) ([59ad0a7](https://github.com/betagouv/ma-cantine/commit/59ad0a7b5ca05be40c635d6e4f39019ff1713906))


### Technique

* **API Stats:** réorganise un peu les tests ([#5427](https://github.com/betagouv/ma-cantine/issues/5427)) ([c648617](https://github.com/betagouv/ma-cantine/commit/c648617ed05977590a1edae0afee84e1a2904026))
* **Metabase:** homogénéise le nommage à Analysis ([#5429](https://github.com/betagouv/ma-cantine/issues/5429)) ([c6f681d](https://github.com/betagouv/ma-cantine/commit/c6f681d44b319ff25e40e27e9e1429beef6fac21))

## [2025.20.0](https://github.com/betagouv/ma-cantine/compare/v2025.19.0...v2025.20.0) (2025-06-04)


### Nouveautés

* **Geo Bot:** ajouter la liste des PAT aux cantines correspondantes ([#5409](https://github.com/betagouv/ma-cantine/issues/5409)) ([a0e0e9b](https://github.com/betagouv/ma-cantine/commit/a0e0e9bc57b1ecfa1ab3cb4cbadafb4dba90111f))


### Améliorations

* **ETL:** Ajout du champ service type ([#5415](https://github.com/betagouv/ma-cantine/issues/5415)) ([9715549](https://github.com/betagouv/ma-cantine/commit/97155497cc5b9066095fe1b06ff92b14f99a9086))
* **ETL:** Ajouts des lignes en base par chunks pour éviter les timeout ([#5417](https://github.com/betagouv/ma-cantine/issues/5417)) ([7e071d8](https://github.com/betagouv/ma-cantine/commit/7e071d8eda4a11021c70fc0fae639aa395ebd9b6))
* **Metabase:** Cantines: ajout des nouveaux champs pat_list & pat_lib_list dans l'export ([#5410](https://github.com/betagouv/ma-cantine/issues/5410)) ([d32a547](https://github.com/betagouv/ma-cantine/commit/d32a5474bb689e6a7cf674cbc7c1a2a086cc6ebd))
* **Open Data:** Cantines: ajout des nouveaux champs pat_list & pat_lib_list dans l'export ([#5411](https://github.com/betagouv/ma-cantine/issues/5411)) ([97b6a26](https://github.com/betagouv/ma-cantine/commit/97b6a26c4f62786e1ead8bd7cdee2b9cead128e2))


### Corrections (bugs, typos...)

* **ETL:** Corriger les valeurs alimentaires des satellites des cc central serving ([#5420](https://github.com/betagouv/ma-cantine/issues/5420)) ([57edf83](https://github.com/betagouv/ma-cantine/commit/57edf83f7a0ffd36b81d8612aa565ac9a7425bfd))
* **Télédéclaration:** répare la façon dont on va chercher certaines infos géographiques ([#5406](https://github.com/betagouv/ma-cantine/issues/5406)) ([891111b](https://github.com/betagouv/ma-cantine/commit/891111b2dc196ca5c1070b4dd60dfc65cbac6f09))


### Technique

* **ETL:** Concat toutes les lignes des satellites dans le dataframe en une fois ([#5412](https://github.com/betagouv/ma-cantine/issues/5412)) ([342d512](https://github.com/betagouv/ma-cantine/commit/342d512c82c09a0aa5d54462c44fd70d7f4e6d6f))
* **ETL:** Supprimer les colonnes campagnes_&lt;ANNEE&gt; ([#5413](https://github.com/betagouv/ma-cantine/issues/5413)) ([5760552](https://github.com/betagouv/ma-cantine/commit/5760552aecff30c88d1a382cbe8d688d0915244b))

## [2025.19.0](https://github.com/betagouv/ma-cantine/compare/v2025.18.1...v2025.19.0) (2025-06-03)


### Nouveautés

* **Cantines:** nouveaux champs pour stocker le nom et l'id des PAT ([#5362](https://github.com/betagouv/ma-cantine/issues/5362)) ([94c5e56](https://github.com/betagouv/ma-cantine/commit/94c5e563f01383c6a771279adfe9f10ed8b59e40))
* **DataGouv:** méthode pour récupérer les PAT depuis l'API ([#5365](https://github.com/betagouv/ma-cantine/issues/5365)) ([3a9b0dd](https://github.com/betagouv/ma-cantine/commit/3a9b0ddbb4657b7602f31b128fc60267b4440ac0))
* **Plan du site:** migration de la page vers vue3 ([#5389](https://github.com/betagouv/ma-cantine/issues/5389)) ([d7492c5](https://github.com/betagouv/ma-cantine/commit/d7492c5d032fd0c65e573f177d7de8c712c78a4c))
* **Télédéclaration:** 1 TD par cantine ([#5403](https://github.com/betagouv/ma-cantine/issues/5403)) ([f37b951](https://github.com/betagouv/ma-cantine/commit/f37b951d13099b74ca20d1217fbc7653f361a9dc))


### Améliorations

* **ETL:** Ajout prefetch sur le queryset ([#5401](https://github.com/betagouv/ma-cantine/issues/5401)) ([4a746f2](https://github.com/betagouv/ma-cantine/commit/4a746f23a9e8677ce39e63976b60134b7129475a))
* **Pages du footer:** homogénéise l'affichage entre les pages ([#5391](https://github.com/betagouv/ma-cantine/issues/5391)) ([bb6e3fa](https://github.com/betagouv/ma-cantine/commit/bb6e3fa732edb7a761550a71ecb27f7eabfac52b))
* **Télédéclaration:** pour 2021 et 2022, enrichir les cantines de leur département & région ([#5405](https://github.com/betagouv/ma-cantine/issues/5405)) ([08f81ec](https://github.com/betagouv/ma-cantine/commit/08f81ec287f88e2bcedbcc5243da4828d9c379a1))


### Corrections (bugs, typos...)

* **Gestion des cookies:** corrige les liens cassés ou non présents dans les footer ([#5388](https://github.com/betagouv/ma-cantine/issues/5388)) ([eddbc48](https://github.com/betagouv/ma-cantine/commit/eddbc48af0776c809032c78d4917abb3b9392d92))
* **Mesures de notre impact:** supprime la page obsolète ([#5390](https://github.com/betagouv/ma-cantine/issues/5390)) ([8ce35ec](https://github.com/betagouv/ma-cantine/commit/8ce35ec6fa1e09c892ce410a228e66b1ef8fb467))


### Technique

* **ETL:** Suite transfert de transform() pour TeledeclarationAnalysis ([#5384](https://github.com/betagouv/ma-cantine/issues/5384)) ([a336e33](https://github.com/betagouv/ma-cantine/commit/a336e3396fcac651dbfa79e168d69925c6d8b314))
* **Pre-commit:** mise à jour des plugins utilisés pour les vérifications ([#5400](https://github.com/betagouv/ma-cantine/issues/5400)) ([0bb8875](https://github.com/betagouv/ma-cantine/commit/0bb8875d67b40523afe9677dfdd3c4c2742dde05))
* **Vue3:** mise à jour des packages ([#5404](https://github.com/betagouv/ma-cantine/issues/5404)) ([bbcd5f1](https://github.com/betagouv/ma-cantine/commit/bbcd5f183c2e91611d104b48d85a45f8e7f21104))

## [2025.18.1](https://github.com/betagouv/ma-cantine/compare/v2025.18.0...v2025.18.1) (2025-05-28)


### Améliorations

* **ETL:** Affiner le scope des fonctions d'export ([#5374](https://github.com/betagouv/ma-cantine/issues/5374)) ([c366fcf](https://github.com/betagouv/ma-cantine/commit/c366fcf9b06d264caaa64616aa2f6d372d55f3fe))
* **Metabase:** Cantines: ne plus renvoyer 'inconnu' quand le champ est vide (modele eco, type gestion, type prod, min tutelle) ([#5345](https://github.com/betagouv/ma-cantine/issues/5345)) ([2965066](https://github.com/betagouv/ma-cantine/commit/2965066b1fbd1062024c9e2a9317fde6e2cd6858))


### Corrections (bugs, typos...)

* **ETL:** corrige une typo dans la tâche d'export quotidien ([#5382](https://github.com/betagouv/ma-cantine/issues/5382)) ([1c9ef28](https://github.com/betagouv/ma-cantine/commit/1c9ef2841d66ce67504176186cec4fedd63a6715))
* **ETL:** Vérifier existence colonne pour calcul cout denrees ([#5370](https://github.com/betagouv/ma-cantine/issues/5370)) ([3124ed1](https://github.com/betagouv/ma-cantine/commit/3124ed11f950296cf519db2ac04bc295b6f29807))
* **Gaspillage alimentaire:** corrige condition pour une valeur vide ([#5387](https://github.com/betagouv/ma-cantine/issues/5387)) ([7f4b09a](https://github.com/betagouv/ma-cantine/commit/7f4b09a2913b85b8b61bd538630fc6f0094b2b63))
* **Gaspillage alimentaire:** le graphique "part de comestible" ne s'affiche pas si un des totaux mesuré est égale à zéro ([#5385](https://github.com/betagouv/ma-cantine/issues/5385)) ([d7ba37c](https://github.com/betagouv/ma-cantine/commit/d7ba37cb0fa116180f5428ffea91105083cc309a))
* **Geo Bot:** rajoute les départements et régions d'outre-mer manquants ([#5369](https://github.com/betagouv/ma-cantine/issues/5369)) ([eca431a](https://github.com/betagouv/ma-cantine/commit/eca431adb6d63beb4919307d3016d27668873c93))
* **Synthèse approvisionnement:** la valeur bio est renseignée à vide au lieu de zéro ([#5386](https://github.com/betagouv/ma-cantine/issues/5386)) ([880455e](https://github.com/betagouv/ma-cantine/commit/880455eae2c24ac92447b9e6b7b0eb1cd2eafd39))


### Documentation

* **Geo Bot:** documenter comment nous gérons les données géographiques ([#5377](https://github.com/betagouv/ma-cantine/issues/5377)) ([21f3f7f](https://github.com/betagouv/ma-cantine/commit/21f3f7f33feb3a41abf6c5063cfea75a5e0ab27d))
* **Open Data:** corrige quelques typos dans la doc du schéma ([#5372](https://github.com/betagouv/ma-cantine/issues/5372)) ([2a58141](https://github.com/betagouv/ma-cantine/commit/2a5814167f31a4e07fd216f46fd8986fd767906f))


### Technique

* **DataGouv:** fichier dédié pour intéragir avec l'API ([#5363](https://github.com/betagouv/ma-cantine/issues/5363)) ([c26cee6](https://github.com/betagouv/ma-cantine/commit/c26cee67a7187d681de13e9ce6c940165e34767c))
* **ETL:** Factoriser la méthode extract_dataset()  ([#5376](https://github.com/betagouv/ma-cantine/issues/5376)) ([9c40c6e](https://github.com/betagouv/ma-cantine/commit/9c40c6ee9202bfdc3e786a6e879c09f2dcdeadc2))
* **ETL:** Remplacer l'extraction des requêtes TD par queryset/serializer au lieu de pandas ([#5378](https://github.com/betagouv/ma-cantine/issues/5378)) ([9bc7593](https://github.com/betagouv/ma-cantine/commit/9bc7593bfaea1200f789b257e2652eb2a709ef9f))
* **ETL:** Transférer la transformation des colonnes caractéristiques cantines dans le serializer AnalysisTeledeclaration ([#5383](https://github.com/betagouv/ma-cantine/issues/5383)) ([53dad12](https://github.com/betagouv/ma-cantine/commit/53dad12c22b5bacd6c4f813b433b289e8990f2cb))
* **ETL:** Utilisation d'un queryset à la place de pandas pour recuperer les TD historiques ([#5375](https://github.com/betagouv/ma-cantine/issues/5375)) ([6b6cfa2](https://github.com/betagouv/ma-cantine/commit/6b6cfa2e1013621432439161ee2e13789a421c19))
* **Geo Bot:** avoir les résultats des tâches dans l'admin ([#5381](https://github.com/betagouv/ma-cantine/issues/5381)) ([172851a](https://github.com/betagouv/ma-cantine/commit/172851a254c2887a5e2a693a08f6acb37a40c4ed))
* **Geo Bot:** bouger la logique dans une fonction dédiée pour pouvoir l'appeler d'ailleurs ([#5380](https://github.com/betagouv/ma-cantine/issues/5380)) ([82f024d](https://github.com/betagouv/ma-cantine/commit/82f024d9e56a8a8f8706273ce68a3a89350ff16c))
* **Geo Bot:** évite de sauvegarder la cantine si aucun changement n'a été effectué ([#5371](https://github.com/betagouv/ma-cantine/issues/5371)) ([b7acbe3](https://github.com/betagouv/ma-cantine/commit/b7acbe313e2dbfff1bd0006af4ead52044d4d998))
* **Geo Bot:** récupérer seulement le code Insee à partir du Siret ([#5379](https://github.com/betagouv/ma-cantine/issues/5379)) ([52a5934](https://github.com/betagouv/ma-cantine/commit/52a593490b6ffa49c6edae43d7682d3bda5f725c))

## [2025.18.0](https://github.com/betagouv/ma-cantine/compare/v2025.17.0...v2025.18.0) (2025-05-22)


### Nouveautés

* **ETL:** Commande de comparaison de deux versions d'un jeu de données ([#5367](https://github.com/betagouv/ma-cantine/issues/5367)) ([0fc255a](https://github.com/betagouv/ma-cantine/commit/0fc255a8e02e5b1eac90387fa0ec09d61a699720))


### Améliorations

* **ETL:** Versionner le jeu de données analysis des TD ([#5364](https://github.com/betagouv/ma-cantine/issues/5364)) ([c60afc2](https://github.com/betagouv/ma-cantine/commit/c60afc2810101b8bab2872f2c2f3342a376b5ee2))


### Corrections (bugs, typos...)

* **Geo Bot:** certains départements n'ont pas de régions (e.g. 988) ([#5366](https://github.com/betagouv/ma-cantine/issues/5366)) ([acf476f](https://github.com/betagouv/ma-cantine/commit/acf476f83b9ee3dfcd9a00d19b0558df3a47cdb9))

## [2025.17.0](https://github.com/betagouv/ma-cantine/compare/v2025.16.0...v2025.17.0) (2025-05-21)


### Nouveautés

* **Cantines:** nouveau champ epci_lib pour stocker le libellé de l'EPCI ([#5349](https://github.com/betagouv/ma-cantine/issues/5349)) ([afe6996](https://github.com/betagouv/ma-cantine/commit/afe6996b629c4cae0f792586eee8ffd3ae4bedb3))
* **Cantines:** nouveau champs department_lib & region_lib pour stocker le libellé des Départements & Régions ([#5351](https://github.com/betagouv/ma-cantine/issues/5351)) ([ad36314](https://github.com/betagouv/ma-cantine/commit/ad363148438b13d4315c113cbf4c951bea52d130))
* **Geo Bot:** Cantines: remplir les nouveaux champs grâce à l'API Découpage Administratif ([#5358](https://github.com/betagouv/ma-cantine/issues/5358)) ([7bf6716](https://github.com/betagouv/ma-cantine/commit/7bf67161552f1460fdb38239da50d51926630b68))


### Améliorations

* **Geo Bot:** Cantines: prendre seulement le code INSEE comme pivot (ignorer le code postal) ([#5354](https://github.com/betagouv/ma-cantine/issues/5354)) ([c558096](https://github.com/betagouv/ma-cantine/commit/c55809600b2768e1a2d00cc2a53a282e6390b57a))
* **Geo Bot:** Cantines: récupérer l'epci si il est manquant ([#5348](https://github.com/betagouv/ma-cantine/issues/5348)) ([05e8020](https://github.com/betagouv/ma-cantine/commit/05e8020c1aacdb6a16d4e2ed4311a1fdf0a1c236))


### Corrections (bugs, typos...)

* **Geo Bot:** change la requête pour inclure les codes INSEE des arrondissements des villes de Paris, Lyon & Marseille ([#5361](https://github.com/betagouv/ma-cantine/issues/5361)) ([a355c73](https://github.com/betagouv/ma-cantine/commit/a355c7344617eaabfeb774997def28fc5ff0ea06))


### Technique

* **API Decoupage Administratif:** bouger la logique de transformation vers un seul fichier ([#5357](https://github.com/betagouv/ma-cantine/issues/5357)) ([995e76a](https://github.com/betagouv/ma-cantine/commit/995e76a4d3e0b5cb875df2b278e8abf0d523d624))
* **Geo Bot:** Cantines: mieux filtrer sur les champs manquants à remplir ([#5355](https://github.com/betagouv/ma-cantine/issues/5355)) ([b3e3880](https://github.com/betagouv/ma-cantine/commit/b3e3880de8c179545fe9cd36b2140daf540e17d8))
* **Open Data:** utiliser les nouveaux champ Canteen epci & epci_lib au lieu de le récupérer via API ([#5347](https://github.com/betagouv/ma-cantine/issues/5347)) ([951338c](https://github.com/betagouv/ma-cantine/commit/951338cf17279e49a8c36ac7f3b724a59091852d))

## [2025.16.0](https://github.com/betagouv/ma-cantine/compare/v2025.15.0...v2025.16.0) (2025-05-14)


### Nouveautés

* **Données personnelles:** migration de la page en vue3 ([#5342](https://github.com/betagouv/ma-cantine/issues/5342)) ([717c06b](https://github.com/betagouv/ma-cantine/commit/717c06be2a60da6048b9b26ed1987c6505783f3f))


### Améliorations

* **Imports:** Cantines: utilise le libellé complet du ministère de tutelle (au lieu du nom interne) ([#5343](https://github.com/betagouv/ma-cantine/issues/5343)) ([778fabd](https://github.com/betagouv/ma-cantine/commit/778fabd3fef681c67767f6f4cbb1b99b2bb8da37))
* **Open Data:** afficher le libellé complet du ministère de tutelle des cantines (au lieu du nom interne) ([#5339](https://github.com/betagouv/ma-cantine/issues/5339)) ([51f9134](https://github.com/betagouv/ma-cantine/commit/51f9134c0ba275111476711793fddde57fb69206))


### Technique

* **Open Data:** ajout de tests dans l'ETL ([#5341](https://github.com/betagouv/ma-cantine/issues/5341)) ([2bff8b5](https://github.com/betagouv/ma-cantine/commit/2bff8b51cad9269ae2f89c95c838aa5022118d31))

## [2025.15.0](https://github.com/betagouv/ma-cantine/compare/v2025.14.8...v2025.15.0) (2025-05-13)


### Nouveautés

* **Cantines:** nouveau champ epci ([#5333](https://github.com/betagouv/ma-cantine/issues/5333)) ([175b2c0](https://github.com/betagouv/ma-cantine/commit/175b2c00dfd9896be78c76816089694223ad3929))


### Améliorations

* **Metabase:** ajout du nouveau champ Canteen.epci dans l'export ([#5337](https://github.com/betagouv/ma-cantine/issues/5337)) ([17f1945](https://github.com/betagouv/ma-cantine/commit/17f1945206a38100a18589cb49b82c01116ea239))
* **Metabase:** Cantines: afficher la valeur du ministère de tutelle (au lieu du champ en DB) ([#5329](https://github.com/betagouv/ma-cantine/issues/5329)) ([ba447c8](https://github.com/betagouv/ma-cantine/commit/ba447c8fa478e66087a2ab5df043af78c8fa3bcc))
* **Recherche:** réduit le temps de chargement de la page (30 -&gt; 15) et indique aux utilisateurs une temporalité ([#5340](https://github.com/betagouv/ma-cantine/issues/5340)) ([892d00a](https://github.com/betagouv/ma-cantine/commit/892d00a791beda6dad6280407efde4860e41511a))


### Corrections (bugs, typos...)

* **Metabase:** Corriger la colonne objectif_zone_geo ([#5332](https://github.com/betagouv/ma-cantine/issues/5332)) ([6a209e4](https://github.com/betagouv/ma-cantine/commit/6a209e46cf04785b3869216c8e28a21c94833679))
* **Recherche:** augmente le nombre de cantine renvoyées par page (3 -&gt; 30) ([#5338](https://github.com/betagouv/ma-cantine/issues/5338)) ([b7a770a](https://github.com/betagouv/ma-cantine/commit/b7a770ae71347bcc566adcf50c430f0c038886d6))


### Technique

* **API Adresse:** gérer tous les appels à l'API dans un même fichier ([#5335](https://github.com/betagouv/ma-cantine/issues/5335)) ([1202c41](https://github.com/betagouv/ma-cantine/commit/1202c412c76c62d3f69219084466f7bb2a4c6a26))
* **API Decoupage Administratif:** nouveau fichier pour centraliser les appels à cet API externe ([#5336](https://github.com/betagouv/ma-cantine/issues/5336)) ([8e246d5](https://github.com/betagouv/ma-cantine/commit/8e246d5de107d64944a1557ab55f8b8b1c13ad5e))
* **API Recherche Entreprise:** renvoyer aussi l'EPCI et la region ([#5334](https://github.com/betagouv/ma-cantine/issues/5334)) ([ccaed00](https://github.com/betagouv/ma-cantine/commit/ccaed001ba853f18f3579c154a201a4450e5c68d))
* **Secteurs:** bouge le filtrage SPE dans une queryset dédiée ([#5330](https://github.com/betagouv/ma-cantine/issues/5330)) ([5d8bded](https://github.com/betagouv/ma-cantine/commit/5d8bded322fd57ebd914b6bc53b5ef6f9e5f98ef))

## [2025.14.8](https://github.com/betagouv/ma-cantine/compare/v2025.14.7...v2025.14.8) (2025-05-07)


### Corrections (bugs, typos...)

* **Badges:** homogénisation de l'affichage des badges pour les CSAT avec des CC en déclaration complète ([#5302](https://github.com/betagouv/ma-cantine/issues/5302)) ([6a81163](https://github.com/betagouv/ma-cantine/commit/6a81163c409fe94234f2a3ba1acd0e65b559c7f2))
* **Cantines:** répare la migration qui remplit l'historique du creation_source. ref [#5325](https://github.com/betagouv/ma-cantine/issues/5325) ([c9a935b](https://github.com/betagouv/ma-cantine/commit/c9a935b52daaa070d8953956e831e007554986ed))
* **GeoBot:** Augmenter la valeur du Geolocation Bot Attempt ([#5324](https://github.com/betagouv/ma-cantine/issues/5324)) ([1762093](https://github.com/betagouv/ma-cantine/commit/17620939ea747dd8e7f4fd88d27337f9c543e1b8))
* **Télédéclaration:** simplifie la vérification des données d'approvisionnement en utilisant l'api ([#5303](https://github.com/betagouv/ma-cantine/issues/5303)) ([6cde131](https://github.com/betagouv/ma-cantine/commit/6cde1314c2606a771461ebee429a65ed91b8eb6d))
* **Tests:** fige les dates des tests dans une période où la télédéclaration est permise ([#5323](https://github.com/betagouv/ma-cantine/issues/5323)) ([d74121f](https://github.com/betagouv/ma-cantine/commit/d74121fac5e6880bd32cc77ef85e727f5186c6c8))


### Documentation

* **Open-Data:** Rectifier ressource -&gt; dataset ([#5295](https://github.com/betagouv/ma-cantine/issues/5295)) ([3f97334](https://github.com/betagouv/ma-cantine/commit/3f97334345124bf921b9af15d6b594f93eba6ece))


### Technique

* **Achats:** source de création: enlève une property obsolète ([#5322](https://github.com/betagouv/ma-cantine/issues/5322)) ([0d5a16e](https://github.com/betagouv/ma-cantine/commit/0d5a16e906f5524e46409640947aabe9424b0b66))
* **Achats:** source de création: script pour remplir (une partie de) l'historique ([#5321](https://github.com/betagouv/ma-cantine/issues/5321)) ([8ba9796](https://github.com/betagouv/ma-cantine/commit/8ba9796172b798608ca2a8abf6c4ebf48be3ac19))
* **Cantines:** source de création: script pour remplir (une partie de) l'historique ([#5325](https://github.com/betagouv/ma-cantine/issues/5325)) ([7226bc0](https://github.com/betagouv/ma-cantine/commit/7226bc0a74b54b013ff208bcc3bd30753c308a13))
* **deps:** bump django-extensions from 3.2.3 to 4.1 ([#5314](https://github.com/betagouv/ma-cantine/issues/5314)) ([11c72cb](https://github.com/betagouv/ma-cantine/commit/11c72cb6a60346bc80dff7b6c11202a719d0f6e4))
* **Diagnostics:** source de création: script pour remplir (une partie de) l'historique ([#5326](https://github.com/betagouv/ma-cantine/issues/5326)) ([5fd8ff2](https://github.com/betagouv/ma-cantine/commit/5fd8ff261f2a1dda822b6d72bb60b1d6604c773e))

## [2025.14.7](https://github.com/betagouv/ma-cantine/compare/v2025.14.6...v2025.14.7) (2025-04-29)


### Améliorations

* **Achats:** Renomme la famille Boulangerie/Pâtisserie (ajoute 'surgelées') ([#5294](https://github.com/betagouv/ma-cantine/issues/5294)) ([f532785](https://github.com/betagouv/ma-cantine/commit/f532785ae306a15ce28091189f65a1b53152ab17))
* **Cantines:** Admin: cacher la colonne 'Visible au public' dans la vue liste. L'afficher dans la vue détails. ([#5288](https://github.com/betagouv/ma-cantine/issues/5288)) ([989f207](https://github.com/betagouv/ma-cantine/commit/989f207e598309d3e7e1574c7b84cdf3ad6369e9))
* **Cantines:** Ministères de tutelle: supprimer l'option 'Outre-mer' ([#5298](https://github.com/betagouv/ma-cantine/issues/5298)) ([41b5e61](https://github.com/betagouv/ma-cantine/commit/41b5e6104a35a11f7f550178ed84cffd260ca3a9))


### Technique

* **Celery:** modifier la configuration pour avoir le nom de la tâche ([#5297](https://github.com/betagouv/ma-cantine/issues/5297)) ([4b7bf88](https://github.com/betagouv/ma-cantine/commit/4b7bf88440e0d116b9871f137bc4d5f7d48e85f7))
* **Source de création:** renommer la source TUNNEL en APP ([#5300](https://github.com/betagouv/ma-cantine/issues/5300)) ([dcc1ddd](https://github.com/betagouv/ma-cantine/commit/dcc1ddddde15b453a7b1fe52e9c5fead7d83a11d))

## [2025.14.6](https://github.com/betagouv/ma-cantine/compare/v2025.14.5...v2025.14.6) (2025-04-24)


### Améliorations

* **Cantines:** Admin: nouvelle colonne "Siret (ou Siren)" ([#5286](https://github.com/betagouv/ma-cantine/issues/5286)) ([5348b21](https://github.com/betagouv/ma-cantine/commit/5348b21415b05a12f5ed9b578a1dbb64b3c3ce0e))
* **Cantines:** Ministères de tutelle: supprimer l'option 'Autre' ([#5291](https://github.com/betagouv/ma-cantine/issues/5291)) ([d2e76a4](https://github.com/betagouv/ma-cantine/commit/d2e76a4949617e0fac46a9a2ad6fe5f93a28c870))


### Corrections (bugs, typos...)

* **Open-Data:** Corriger la mise à jour d'explore (NECESSITE MAJ ENV VAR) ([#5292](https://github.com/betagouv/ma-cantine/issues/5292)) ([002ffb0](https://github.com/betagouv/ma-cantine/commit/002ffb0998eaf6c24edea0b10547d2b3900074c2))


### Technique

* **Achats:** stocker la source de création (API, IMPORT, ADMIN, TUNNEL) ([#5293](https://github.com/betagouv/ma-cantine/issues/5293)) ([7fbbda2](https://github.com/betagouv/ma-cantine/commit/7fbbda2645f108d63dca4eeb4812a3ff94e43b5c))
* **Cantines:** Script pour supprimer une liste de cantines ([#5289](https://github.com/betagouv/ma-cantine/issues/5289)) ([513833a](https://github.com/betagouv/ma-cantine/commit/513833abfc8ad6aa6b332966dabc4c0bf2c9a500))
* **Cantines:** stocker la source de création (API, IMPORT, ADMIN, TUNNEL) ([#5290](https://github.com/betagouv/ma-cantine/issues/5290)) ([b0be3f4](https://github.com/betagouv/ma-cantine/commit/b0be3f438101724768ea27ab5d766e9888a562e4))
* **Diagnostic:** nouvelles sources de création (API, IMPORT, ADMIN) ([#5218](https://github.com/betagouv/ma-cantine/issues/5218)) ([dfe05ce](https://github.com/betagouv/ma-cantine/commit/dfe05cea79f1bcb147db726e4736825704941c3c))
* **Télédéclaration:** enlève le check doublonné sur l'unicité de la TD par cantine et par année ([#5285](https://github.com/betagouv/ma-cantine/issues/5285)) ([6183eb7](https://github.com/betagouv/ma-cantine/commit/6183eb79f6673fbccfad14ef3dc7c51044efc306))
* **Tests:** Ajouter explicitement le manager lors de l'appel à CanteenFactory ([#5267](https://github.com/betagouv/ma-cantine/issues/5267)) ([77834ab](https://github.com/betagouv/ma-cantine/commit/77834abec6e9a04e9796c77c45b586b2f7404698))

## [2025.14.5](https://github.com/betagouv/ma-cantine/compare/v2025.14.4...v2025.14.5) (2025-04-18)


### Corrections (bugs, typos...)

* **Badge:** ajoute le champ secteurs aux champs obligatoires pour télédéclarer ([#5279](https://github.com/betagouv/ma-cantine/issues/5279)) ([164227d](https://github.com/betagouv/ma-cantine/commit/164227d5d7c6efd2982b162d7be962044ce57007))
* **Cantines:** Actions: typo dans le nom d'une des actions ([#5283](https://github.com/betagouv/ma-cantine/issues/5283)) ([fcf478e](https://github.com/betagouv/ma-cantine/commit/fcf478e71e22eb14a7f0da24e82b640d344c30c1))
* **Teledeclaration:** Gérer le cas des TD sans appro pour le calcul du cout denrees ([#5282](https://github.com/betagouv/ma-cantine/issues/5282)) ([9a5c039](https://github.com/betagouv/ma-cantine/commit/9a5c03994d67b66ea7e7199b626d80dd428091d2))


### Technique

* **Diagnostic:** wording: corrige un 'complet' (remplacé par 'détaillé') oublié ([#5281](https://github.com/betagouv/ma-cantine/issues/5281)) ([eac7ab0](https://github.com/betagouv/ma-cantine/commit/eac7ab0ed5dda4ae6828307faaf58298ebe6b2b9))

## [2025.14.4](https://github.com/betagouv/ma-cantine/compare/v2025.14.3...v2025.14.4) (2025-04-17)


### Corrections (bugs, typos...)

* **Campagne de correction:** corrige le nombre de télédéclarations en masse disponibles ([#5278](https://github.com/betagouv/ma-cantine/issues/5278)) ([397244f](https://github.com/betagouv/ma-cantine/commit/397244f7583599382a5a9e4165ee24059fcc8e29))
* **Campagne de correction:** ne pas afficher les boutons "télédéclarer" si aucun bilan n'a été déclaré ([#5277](https://github.com/betagouv/ma-cantine/issues/5277)) ([554c14b](https://github.com/betagouv/ma-cantine/commit/554c14bcfdd7d159f57d21f0e0d576f3ed179a35))


### Technique

* **Campagne de correction:** Intégrer les TD crées lors de la campagne de correction dans le queryset données officielles ([#5269](https://github.com/betagouv/ma-cantine/issues/5269)) ([b03784b](https://github.com/betagouv/ma-cantine/commit/b03784b9721d04d4e73b3f4c9fb25f36c2190513))
* **Diagnostic:** homogénéiser le nommage de COMPLETE en 'détaillée' (au lieu de 'complète') ([#5259](https://github.com/betagouv/ma-cantine/issues/5259)) ([d63a92c](https://github.com/betagouv/ma-cantine/commit/d63a92c80bf4ac4b27e142d324dc2ed4b08a98cd))
* **Télédéclaration:** créer une méthode dédiée pour annuler une TD ([#5273](https://github.com/betagouv/ma-cantine/issues/5273)) ([70add4e](https://github.com/betagouv/ma-cantine/commit/70add4e397be86708093e7b728d3e4554a85ab8d))
* **Télédéclaration:** la méthode create_from_diagnostic ne doit servir qu'à submit ([#5275](https://github.com/betagouv/ma-cantine/issues/5275)) ([91eebd7](https://github.com/betagouv/ma-cantine/commit/91eebd72ee697768873cd4fed21b9c686cec04f5))
* **Télédéclaration:** Script pour re-TD une liste de cantines pour une année donnée ([#5276](https://github.com/betagouv/ma-cantine/issues/5276)) ([d10e4ca](https://github.com/betagouv/ma-cantine/commit/d10e4cab5688efe80f305e3bcedcff5cfa84b795))

## [2025.14.3](https://github.com/betagouv/ma-cantine/compare/v2025.14.2...v2025.14.3) (2025-04-14)


### Corrections (bugs, typos...)

* **Badge:** Corrige les erreurs d'affichage du badge NEUTRAL ([#5271](https://github.com/betagouv/ma-cantine/issues/5271)) ([1750780](https://github.com/betagouv/ma-cantine/commit/1750780bf4de202bdd82e66a7a7899400efeebc3))
* **Campagne de correction:** autoriser les cantines qui ont fait une correction à re-télédéclarer ([#5270](https://github.com/betagouv/ma-cantine/issues/5270)) ([ee175c0](https://github.com/betagouv/ma-cantine/commit/ee175c04a811e01be020652fea4843fe876506a6))


### Technique

* **Cantines:** action: mieux gérer le cas des cantines qui ont une TD avant la campagne de correction ([#5268](https://github.com/betagouv/ma-cantine/issues/5268)) ([439f56d](https://github.com/betagouv/ma-cantine/commit/439f56db1e205c24414bd22d0a394826893d6833))

## [2025.14.2](https://github.com/betagouv/ma-cantine/compare/v2025.14.1...v2025.14.2) (2025-04-11)


### Corrections (bugs, typos...)

* **Sur Mon Territoire:** Renommer diagnostics count en teledeleclaration count ([#5265](https://github.com/betagouv/ma-cantine/issues/5265)) ([21c9e7c](https://github.com/betagouv/ma-cantine/commit/21c9e7c3da4d250705b45a1b2b09ed1badbc7852))

## [2025.14.1](https://github.com/betagouv/ma-cantine/compare/v2025.14.0...v2025.14.1) (2025-04-11)


### Corrections (bugs, typos...)

* **Statistiques:** Filter les TD dont les valeurs totales d achats sont arrondies à 0 ([#5262](https://github.com/betagouv/ma-cantine/issues/5262)) ([f8fb98f](https://github.com/betagouv/ma-cantine/commit/f8fb98f183feee63445009640985ac984c41fdf5))


### Documentation

* **README:** mise à jour des liens. Ajout de la migration vue3 ([#5260](https://github.com/betagouv/ma-cantine/issues/5260)) ([38aa025](https://github.com/betagouv/ma-cantine/commit/38aa0256f2c52f2cca537078431dc47797050550))


### Technique

* **Dates de campagnes:** renommer les variables d'env avec OVERRIDE pour être d'avantage explicite ([#5261](https://github.com/betagouv/ma-cantine/issues/5261)) ([ceabca4](https://github.com/betagouv/ma-cantine/commit/ceabca491abe2346357970b2e50a4867f740d3bd))
* **Tests:** Rendre déterministe des test liés à la cantines ([#5264](https://github.com/betagouv/ma-cantine/issues/5264)) ([21767dd](https://github.com/betagouv/ma-cantine/commit/21767dd09f2217efb298c280588da688b280c36f))

## [2025.14.0](https://github.com/betagouv/ma-cantine/compare/v2025.13.0...v2025.14.0) (2025-04-11)


### Nouveautés

* **Tableau de bord:** affiche dans la vue liste des cantines un message pour modifier son bilan ([#5247](https://github.com/betagouv/ma-cantine/issues/5247)) ([8267983](https://github.com/betagouv/ma-cantine/commit/82679833a519a05116bf78fc8e23ca9f7eff85d1))
* **Tableau de bord:** affiche les badges dans le tableau de actions ([#5245](https://github.com/betagouv/ma-cantine/issues/5245)) ([b854532](https://github.com/betagouv/ma-cantine/commit/b854532f1f9bd0c4c3045376f97ef64a4cd72812))


### Améliorations

* **Bandeau de communication:** mise à jour du texte pour informer sur la campagne de correction ([#5258](https://github.com/betagouv/ma-cantine/issues/5258)) ([ab53493](https://github.com/betagouv/ma-cantine/commit/ab53493608b85809487401e545c08d84786a7f50))
* **Télédéclaration:** autoriser la TD pendant la campagne de correction (seulement si une TD a été créé pendant la campagne de TD) ([#5256](https://github.com/betagouv/ma-cantine/issues/5256)) ([3d8fb4e](https://github.com/betagouv/ma-cantine/commit/3d8fb4eb543e1dd4b0366596eb4a6646c0121f13))
* **Télédéclaration:** utiliser les Dates de campagnes pour autoriser la création et l'annulation ([#5253](https://github.com/betagouv/ma-cantine/issues/5253)) ([59f06bc](https://github.com/betagouv/ma-cantine/commit/59f06bcba5964f8f8bb3f6db8999285f18d0e42b))


### Corrections (bugs, typos...)

* **Badge:** change la couleur du badge "Bilan non télédéclaré" de rouge à gris ([#5250](https://github.com/betagouv/ma-cantine/issues/5250)) ([ff94770](https://github.com/betagouv/ma-cantine/commit/ff9477077edea1d2d0a0bb9227d7e668e5212f13))
* **Tableau de bord:** homogénéise le badge affiché de la cantine en vue liste ou carte ([#5248](https://github.com/betagouv/ma-cantine/issues/5248)) ([e3a6510](https://github.com/betagouv/ma-cantine/commit/e3a6510efaf55ce8daffd13869c333a64a477103))
* **Teledeclaration:** Se baser sur les Teledeclaration et plus les Diagnostics afin d'extraire les données officielles ([#5246](https://github.com/betagouv/ma-cantine/issues/5246)) ([d96a0df](https://github.com/betagouv/ma-cantine/commit/d96a0dffbb05f045ba15e4321be8fa0504779e10))


### Technique

* **Cantines:** rajouter des champs dans CanteenActionsSerializer ([#5252](https://github.com/betagouv/ma-cantine/issues/5252)) ([281f93f](https://github.com/betagouv/ma-cantine/commit/281f93fe68efc42357b759c344b491aa51fcd489))
* **Cantines:** supprime le composant CentralKitchenCard qui faisait doublon ([#5251](https://github.com/betagouv/ma-cantine/issues/5251)) ([a0bf24d](https://github.com/betagouv/ma-cantine/commit/a0bf24de73dac465db0bdf7a31f3e83b770b6369))
* **Dates de campagnes:** Pas besoin de fournir l'année. Ajout de tests. ([#5254](https://github.com/betagouv/ma-cantine/issues/5254)) ([81b77b7](https://github.com/betagouv/ma-cantine/commit/81b77b7ba5d6ad5b86f47309f2bbf0bae78804f8))
* **Statistics:** enlever certaines stats non utilisées (et fausses) ([#5257](https://github.com/betagouv/ma-cantine/issues/5257)) ([eb08548](https://github.com/betagouv/ma-cantine/commit/eb085481fe56bd3410451610495087b72939a065))
* **Télédéclaration:** réorganise les tests (1 class par endpoint) ([#5255](https://github.com/betagouv/ma-cantine/issues/5255)) ([d30fd8c](https://github.com/betagouv/ma-cantine/commit/d30fd8cee6f844893a86ebb46cdc97a609bcf1e8))

## [2025.13.0](https://github.com/betagouv/ma-cantine/compare/v2025.12.1...v2025.13.0) (2025-04-08)


### Nouveautés

* **Bandeau de communication:** mise à jour du texte pour informer sur la campagne de correction ([#5244](https://github.com/betagouv/ma-cantine/issues/5244)) ([a3d314c](https://github.com/betagouv/ma-cantine/commit/a3d314c3d1a17d3cd5d7fa52bbce4420d066db8c))
* **Campagne de correction:** affiche le bouton de modification si la campagne de correction est ouverte ([#5243](https://github.com/betagouv/ma-cantine/issues/5243)) ([ff76a56](https://github.com/betagouv/ma-cantine/commit/ff76a56b91d9efa7052046a68f8da696374f0366))
* **Campagne de correction:** création d'un bandeau dédié pour les campagnes de télédéclaration et de correction ([#5237](https://github.com/betagouv/ma-cantine/issues/5237)) ([0d684c0](https://github.com/betagouv/ma-cantine/commit/0d684c0bd3cd7fe969c17979bff3cbc2490b3164))
* **Dates de campagnes:** API: nouvel endpoint pour récupérer les dates d'une campagne par son année ([#5238](https://github.com/betagouv/ma-cantine/issues/5238)) ([5c48e73](https://github.com/betagouv/ma-cantine/commit/5c48e73adb328c327f519da350d11d63dd43db05))


### Améliorations

* **Cantines:** nouveau badge 'Bilan non télédéclaré' pour indiquer que la cantine n'a pas TD (si en dehors des dates de campagne) ([#5242](https://github.com/betagouv/ma-cantine/issues/5242)) ([3dc356b](https://github.com/betagouv/ma-cantine/commit/3dc356b9cca8f50dffc47a858af072cb5d2bf426))

## [2025.12.1](https://github.com/betagouv/ma-cantine/compare/v2025.12.0...v2025.12.1) (2025-04-07)


### Corrections (bugs, typos...)

* **Teledeclaration:** Ajout somme integer et null sur ligne manquante ([#5239](https://github.com/betagouv/ma-cantine/issues/5239)) ([fad0204](https://github.com/betagouv/ma-cantine/commit/fad0204bf12960c254200485b99a4541c4ee0752))

## [2025.12.0](https://github.com/betagouv/ma-cantine/compare/v2025.11.10...v2025.12.0) (2025-04-07)


### Nouveautés

* **Dates de campaignes:** API: nouvel endpoint pour récupérer toutes les campagnes ([#5234](https://github.com/betagouv/ma-cantine/issues/5234)) ([b123a1e](https://github.com/betagouv/ma-cantine/commit/b123a1ed6d76286ebccd1d62bc9c9b821fe069ec))
* **Foire aux questions:** mise à jour de la page et migration vers vue3 ([#5228](https://github.com/betagouv/ma-cantine/issues/5228)) ([68ff740](https://github.com/betagouv/ma-cantine/commit/68ff740a93611e8e32439a62337a2c68645f82f4))


### Corrections (bugs, typos...)

* **Dates de campagnes:** répare les quelques tests qui cassent suite à la fin de la campagne ([#5230](https://github.com/betagouv/ma-cantine/issues/5230)) ([6149e4f](https://github.com/betagouv/ma-cantine/commit/6149e4f441f81052dde0572d34717b6909b434fb))
* **Foire aux questions:** corrige erreur lors du build dû à l'asset introuvable par vite ([#5232](https://github.com/betagouv/ma-cantine/issues/5232)) ([62b77b8](https://github.com/betagouv/ma-cantine/commit/62b77b8986b8bd6655a9948eea9db4ca104f8722))
* **Teledeclaration:** Une somme de valeurs nulles est égale à null et non pas à 0 ([#5236](https://github.com/betagouv/ma-cantine/issues/5236)) ([d003d04](https://github.com/betagouv/ma-cantine/commit/d003d04484f3665b999d9f59b473875c4ebfa23a))
* **Télédéclaration:** utilise la même fonction pour le calcul du badge "complété" des approvisionnements et le bouton "Télédéclarer" ([#5226](https://github.com/betagouv/ma-cantine/issues/5226)) ([f2944b7](https://github.com/betagouv/ma-cantine/commit/f2944b7ecac2620022627916fc12aa1588f337db))


### Documentation

* **Onboarding:** Ajout de NODE_OPTIONS pour lancer le front ([#5225](https://github.com/betagouv/ma-cantine/issues/5225)) ([4bc0422](https://github.com/betagouv/ma-cantine/commit/4bc042230f5d5232cd4f6d564e814e6cfd98098e))


### Technique

* **Dates de campagnes:** ajout des dates de correction pour la campagne de 2024 ([#5229](https://github.com/betagouv/ma-cantine/issues/5229)) ([0e16dd7](https://github.com/betagouv/ma-cantine/commit/0e16dd7a1c6dd37da3896cea142b4deed1d71cb6))
* **Dates de campagnes:** basculer les end dates sur 23:59 du jour d'avant ([#5235](https://github.com/betagouv/ma-cantine/issues/5235)) ([db819a6](https://github.com/betagouv/ma-cantine/commit/db819a699b10749bbeb43d4ce7a6d351f1ab5f5f))
* **Dates de campagnes:** enlève la variable d'env TELEDECLARATION_CORRECTION_CAMPAIGN (pas utilisée) ([#5233](https://github.com/betagouv/ma-cantine/issues/5233)) ([eab055b](https://github.com/betagouv/ma-cantine/commit/eab055bdd34676ae3a62af3ffe7406ee507f7499))
* **Dates de campagnes:** nouvelles variables d'env pour permettre de les overrider ([#5231](https://github.com/betagouv/ma-cantine/issues/5231)) ([e226d65](https://github.com/betagouv/ma-cantine/commit/e226d6570da40a207197dc4504457f33bd7108f1))

## [2025.11.10](https://github.com/betagouv/ma-cantine/compare/v2025.11.9...v2025.11.10) (2025-04-03)


### Corrections (bugs, typos...)

* **Teledeclaration:** Exclure les TD sans diag de la migration ([#5223](https://github.com/betagouv/ma-cantine/issues/5223)) ([3f65253](https://github.com/betagouv/ma-cantine/commit/3f65253b8eebfd510071c65893aa6b7304fa5200))


### Technique

* **Geobot:** CRON pour le lancer toutes les heures (pour corriger les cantines sans code INSEE) ([#5221](https://github.com/betagouv/ma-cantine/issues/5221)) ([2a70831](https://github.com/betagouv/ma-cantine/commit/2a70831a07f68872ad9087f4256a5bd8930007a1))

## [2025.11.9](https://github.com/betagouv/ma-cantine/compare/v2025.11.8...v2025.11.9) (2025-04-03)


### Améliorations

* **Fixtures:** Ajout de donnés initiales pour déploiements en local ([#5182](https://github.com/betagouv/ma-cantine/issues/5182)) ([fd9cadf](https://github.com/betagouv/ma-cantine/commit/fd9cadf0d35d8c5b287ee97b97161d462a9221de))
* **Télédéclaration:** améliore les messages pour les cuisines satellites ([#5220](https://github.com/betagouv/ma-cantine/issues/5220)) ([3c5b129](https://github.com/betagouv/ma-cantine/commit/3c5b129560deff63a4f4e42b95b602abf75f05fb))
* **Télédéclaration:** Améliorer encore le wording du badge indiquant que la cantine satellite n'a rien à faire ([#5211](https://github.com/betagouv/ma-cantine/issues/5211)) ([2c6d7e7](https://github.com/betagouv/ma-cantine/commit/2c6d7e7cc90ae81b569736c10969cdb89e9c1d32))


### Corrections (bugs, typos...)

* **Tableau de bord:** Vue actions: répare l'occurence de doublons ([#5214](https://github.com/betagouv/ma-cantine/issues/5214)) ([e8c5a06](https://github.com/betagouv/ma-cantine/commit/e8c5a068e2300e6ff1eb98f11aa09da08ebe9be0))
* **Teledeclaration:** Nouvelle migration de données ([#5212](https://github.com/betagouv/ma-cantine/issues/5212)) ([8653102](https://github.com/betagouv/ma-cantine/commit/8653102c9932e1222b29af0621e952a33be78dd5))


### Technique

* **Cantines:** bouger le queryset 'annotate actions' dans le modèle ([#5215](https://github.com/betagouv/ma-cantine/issues/5215)) ([76fd144](https://github.com/betagouv/ma-cantine/commit/76fd144aeb2bc6604c6d951089e7bf537c5b3a65))
* **Cantines:** renommer 'complete' en 'filled' pour clarifier ([#5217](https://github.com/betagouv/ma-cantine/issues/5217)) ([797e3c3](https://github.com/betagouv/ma-cantine/commit/797e3c3733ac74311c2ee7841488979b8c001b3f))
* **Diagnostic:** continuer à renommer completed en filled ([#5219](https://github.com/betagouv/ma-cantine/issues/5219)) ([313f2a1](https://github.com/betagouv/ma-cantine/commit/313f2a102b0a097291bf66f8c6883d2f23ce75dc))
* **Diagnostic:** Nouveau queryset is_filled. Renommer 'completed' par 'filled' pour clarifier ([#5216](https://github.com/betagouv/ma-cantine/issues/5216)) ([0791fa8](https://github.com/betagouv/ma-cantine/commit/0791fa83f4a031b8da66b0d4193652f1875e4eb9))

## [2025.11.8](https://github.com/betagouv/ma-cantine/compare/v2025.11.7...v2025.11.8) (2025-04-01)


### Améliorations

* **Télédéclaration:** Améliorer le wording du badge indiquant que la cantine satellite n'a rien à faire ([#5210](https://github.com/betagouv/ma-cantine/issues/5210)) ([2ae45fd](https://github.com/betagouv/ma-cantine/commit/2ae45fddcf24940ab2f279f719549a7b44527986))
* **Télédéclaration:** Nouveau badge pour indiquer que la cantine satellite n'a rien à faire ([#5191](https://github.com/betagouv/ma-cantine/issues/5191)) ([0d8ca74](https://github.com/betagouv/ma-cantine/commit/0d8ca74ca1c46c8983d940b7808dd19ab246d09c))
* **Tunnel:** Gaspillage: ajustement de wordings (déchets alimentaires issues de la préparation) ([#5176](https://github.com/betagouv/ma-cantine/issues/5176)) ([5360ee4](https://github.com/betagouv/ma-cantine/commit/5360ee43270f6cbec364ae45b1085e1cc28dc3a2))


### Corrections (bugs, typos...)

* **Télédéclaration:** corrige les badges de progression de la télédéclaration ([#5186](https://github.com/betagouv/ma-cantine/issues/5186)) ([e593611](https://github.com/betagouv/ma-cantine/commit/e593611419047bbb92a6be42e2a946c77f7f5b84))
* **Teledeclaration:** Corriger les valeurs aggrégées pour les TD simples ([#5202](https://github.com/betagouv/ma-cantine/issues/5202)) ([5b3c09c](https://github.com/betagouv/ma-cantine/commit/5b3c09cf9eb872cb5dc0e7cba3b10218f43d6a3e))
* **Télédéclaration:** homogénéise les badges utilisés dans la page progression et la télédéclaration ([#5189](https://github.com/betagouv/ma-cantine/issues/5189)) ([1016c27](https://github.com/betagouv/ma-cantine/commit/1016c27610111d7bb001636c330417bbd53d187a))


### Technique

* **Admin:** Filtrer par diagnostic type les objets diagnostics ([#5194](https://github.com/betagouv/ma-cantine/issues/5194)) ([963a129](https://github.com/betagouv/ma-cantine/commit/963a129871e1e15f4a29b7941ecfc32d1a9b8f5f))
* **Django:** Ajout du package django extensions ([#5192](https://github.com/betagouv/ma-cantine/issues/5192)) ([19602dc](https://github.com/betagouv/ma-cantine/commit/19602dc4451a932ccccd2117d4a11261137c3061))
* **Tableau de bord:** récupérer le badge à l'aide de l'API actionableCanteens (au lieu de le recalculer dans le frontend) ([#5185](https://github.com/betagouv/ma-cantine/issues/5185)) ([2724c15](https://github.com/betagouv/ma-cantine/commit/2724c15aa09402a6144fbc681fe7cc5acdcd9e6a))
* **Télédéclaration:** récupérer le badge à l'aide de l'API actionableCanteens (au lieu de le recalculer dans le frontend) ([#5190](https://github.com/betagouv/ma-cantine/issues/5190)) ([d3a0d90](https://github.com/betagouv/ma-cantine/commit/d3a0d905f2ead8a7cb96d7254a0a322586555339))

## [2025.11.7](https://github.com/betagouv/ma-cantine/compare/v2025.11.6...v2025.11.7) (2025-03-31)


### Améliorations

* **Cantines:** gérer le nouveau champ siren_unite_legale dans les TD (stats) ([#5125](https://github.com/betagouv/ma-cantine/issues/5125)) ([352c49d](https://github.com/betagouv/ma-cantine/commit/352c49de8790235360bcf8db23b272667d12ab21))
* **Télédéclaration:** mise à jour du texte du bandeau informatif ([#5184](https://github.com/betagouv/ma-cantine/issues/5184)) ([394ee36](https://github.com/betagouv/ma-cantine/commit/394ee36317127e49b0ce2518dcfce2d050a5d242))


### Corrections (bugs, typos...)

* **Metabase:** Supprimer les nouvelles colonnes _agg lors de l'export pour ne pas créer une double aggrégation ([#5180](https://github.com/betagouv/ma-cantine/issues/5180)) ([8c1c74b](https://github.com/betagouv/ma-cantine/commit/8c1c74b0479053c486a4860e4924290facedd948))


### Technique

* **Cantines:** Nouvelle querysets pour mieux documenter les règles concernant les cantines centrales & satellites ([#5179](https://github.com/betagouv/ma-cantine/issues/5179)) ([9d45e4f](https://github.com/betagouv/ma-cantine/commit/9d45e4f1bfd99d60eefd6ee2d05451bb750f78a3))
* **Télédéclaration:** ne plus utiliser la factory lors de la création à partir du Diagnostic ([#5183](https://github.com/betagouv/ma-cantine/issues/5183)) ([b6acf8e](https://github.com/betagouv/ma-cantine/commit/b6acf8ef95187b14d8209628e8e49d8d56dd2d80))

## [2025.11.6](https://github.com/betagouv/ma-cantine/compare/v2025.11.5...v2025.11.6) (2025-03-28)


### Documentation

* **Celery:** Lancer une tâche manuellement ([#5175](https://github.com/betagouv/ma-cantine/issues/5175)) ([329ef4b](https://github.com/betagouv/ma-cantine/commit/329ef4b93f8a5b2107e12740c7e8994a5c56eb72))

## [2025.11.5](https://github.com/betagouv/ma-cantine/compare/v2025.11.4...v2025.11.5) (2025-03-27)


### Améliorations

* **Geobot:** Ajout de logs ([#5173](https://github.com/betagouv/ma-cantine/issues/5173)) ([aa94cc1](https://github.com/betagouv/ma-cantine/commit/aa94cc11e75c29a923fa1db94c5e3146273e9d23))
* **Geobot:** inclut les code insee vides en plus des null pour la recherche par SIRET ([#5169](https://github.com/betagouv/ma-cantine/issues/5169)) ([153ec07](https://github.com/betagouv/ma-cantine/commit/153ec0744ba67ec395b2089994a5037daaf51f6b))
* **Geobot:** Sleep d'une minute tous les 200 appels a l'API recherche entreprises ([#5172](https://github.com/betagouv/ma-cantine/issues/5172)) ([0c59ea3](https://github.com/betagouv/ma-cantine/commit/0c59ea36537f5b7dcc1151d8bd55b78b3378e157))


### Technique

* **Cantines:** Actions: gère les cantines sans siret (v2) ([#5171](https://github.com/betagouv/ma-cantine/issues/5171)) ([1aa25f8](https://github.com/betagouv/ma-cantine/commit/1aa25f865028915d8ab4de350627f0aaa64f045e))

## [2025.11.4](https://github.com/betagouv/ma-cantine/compare/v2025.11.3...v2025.11.4) (2025-03-27)


### Corrections (bugs, typos...)

* **Teledeclaration:** Remove problematic and uselesss cout denrees ([#5167](https://github.com/betagouv/ma-cantine/issues/5167)) ([32b0b79](https://github.com/betagouv/ma-cantine/commit/32b0b794edf470e98ac90b1eb79c7fbabc3c283c))

## [2025.11.3](https://github.com/betagouv/ma-cantine/compare/v2025.11.2...v2025.11.3) (2025-03-27)


### Améliorations

* **Modifier mon établissement:** ajoute un lien pour accéder à la page de suppression de l'établissement ([#5164](https://github.com/betagouv/ma-cantine/issues/5164)) ([67541ef](https://github.com/betagouv/ma-cantine/commit/67541efb2eed0bc94343b17fcc4375d17ec96c3e))
* **Statistiques:** Renommer la stats 'Cantines qui ont télédéclaré' en 'Bilans télédéclarés' ([#5166](https://github.com/betagouv/ma-cantine/issues/5166)) ([e233419](https://github.com/betagouv/ma-cantine/commit/e233419b1ef2271d35be62803c3c668d0e03c827))
* **Teledeclaration:** Ajout de champs exploitables pour les données alimentaires les plus importante ([#5159](https://github.com/betagouv/ma-cantine/issues/5159)) ([5659bbf](https://github.com/betagouv/ma-cantine/commit/5659bbff8882f57474fee3114c2f4ec0b6f03780))
* **Télédéclaration:** prolonge la campagne de télédéclaration jusqu'au 6 avril ([#5162](https://github.com/betagouv/ma-cantine/issues/5162)) ([d4c68a7](https://github.com/betagouv/ma-cantine/commit/d4c68a773cc3fb0c2d0b5d99f93c5bbc0246c623))


### Corrections (bugs, typos...)

* **Badge menus végétariens:** modification du calcul d'obtention du badge ([#5156](https://github.com/betagouv/ma-cantine/issues/5156)) ([049e4d6](https://github.com/betagouv/ma-cantine/commit/049e4d6dd195da9d83d4363866a4204d5ef75bdf))


### Technique

* **Cantines:** Actions: gère les cantines sans siret ([#5163](https://github.com/betagouv/ma-cantine/issues/5163)) ([03da60c](https://github.com/betagouv/ma-cantine/commit/03da60c372b5a737f4f84dd13aa276a027f459a3))
* **Cantines:** Actions: pour les cantines satellites, regarder si la CC n'a pas déjà un bilan complet ([#5160](https://github.com/betagouv/ma-cantine/issues/5160)) ([9a12368](https://github.com/betagouv/ma-cantine/commit/9a12368b794dfbcc439d67f2ebe72ee3298bd26b))

## [2025.11.2](https://github.com/betagouv/ma-cantine/compare/v2025.11.1...v2025.11.2) (2025-03-25)


### Corrections (bugs, typos...)

* **Ajouter et modifier une cantine:** corrige la valeur minimale attendue pour être supérieure à zéro ([#5152](https://github.com/betagouv/ma-cantine/issues/5152)) ([4beedf5](https://github.com/betagouv/ma-cantine/commit/4beedf560d58b180821e02f2084284b48704876e))
* **Cantine:** affiche toutes années dans le comparateur "qualité des produits" ([#5153](https://github.com/betagouv/ma-cantine/issues/5153)) ([2918ea7](https://github.com/betagouv/ma-cantine/commit/2918ea775bbbab0dc47ed8d6690fb5dfe20db96a))
* **Cantines:** le champ line_ministry n'est pas obligatoire pour les établissements privés ([#5158](https://github.com/betagouv/ma-cantine/issues/5158)) ([7879f84](https://github.com/betagouv/ma-cantine/commit/7879f847364a310f00e834292c609ff219e1128d))
* **ETL:** Gérer le cas où la cantine d un diagnostic à renseignée un yearly_meal_count à 0 ([#5157](https://github.com/betagouv/ma-cantine/issues/5157)) ([1795728](https://github.com/betagouv/ma-cantine/commit/1795728f19773342cdf196d7d72eb5c2ec956d14))


### Technique

* **Cantines:** le champ daily_meal_count n'est pas obligatoire pour les cantines centrales sans lieu de consommation ([#5150](https://github.com/betagouv/ma-cantine/issues/5150)) ([9ceb864](https://github.com/betagouv/ma-cantine/commit/9ceb8649832af642d09238191832ef63fec74f1d))
* **Cantines:** nouveau queryset pour savoir si il manque des infos ([#5155](https://github.com/betagouv/ma-cantine/issues/5155)) ([cc3dde7](https://github.com/betagouv/ma-cantine/commit/cc3dde7654131f59a93b107f933884f55ea52966))
* **Cantines:** nouvelle property pour savoir si il manque des infos ([#5148](https://github.com/betagouv/ma-cantine/issues/5148)) ([240ce8b](https://github.com/betagouv/ma-cantine/commit/240ce8b171d5c68874db94c1e88538fa5b57f3b3))

## [2025.11.1](https://github.com/betagouv/ma-cantine/compare/v2025.11.0...v2025.11.1) (2025-03-25)


### Technique

* **Sentry:** ajout de config pour monitorer la performance ([#5149](https://github.com/betagouv/ma-cantine/issues/5149)) ([438d342](https://github.com/betagouv/ma-cantine/commit/438d342b1e16a72c2962a165fb1bd9a449cc4acd))

## [2025.11.0](https://github.com/betagouv/ma-cantine/compare/v2025.10.0...v2025.11.0) (2025-03-21)


### Nouveautés

* **Modifier une cantine:** redesign et migration de la page en vue3 ([#5145](https://github.com/betagouv/ma-cantine/issues/5145)) ([1846e86](https://github.com/betagouv/ma-cantine/commit/1846e8624a57d06e7edc95a1117aa954cc6e3f10))


### Corrections (bugs, typos...)

* **Ajouter une cantine:** corrige le département manquant dans la réponse api de la recherche d'un l'établissement via SIRET ou SIREN ([#5146](https://github.com/betagouv/ma-cantine/issues/5146)) ([3d98886](https://github.com/betagouv/ma-cantine/commit/3d988865e97f30a5574c072c1f2dafd1fe2db23b))
* **Imports Cantines:** Corriger l'apostrophe de la regex pour le secteur RIA ([#5136](https://github.com/betagouv/ma-cantine/issues/5136)) ([a9d49aa](https://github.com/betagouv/ma-cantine/commit/a9d49aac1470bd0ed94279c33cb5f4847af1f105))

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
