# Journal des modifications

Ressources :
- [CHANGELOG recommendations](https://keepachangelog.com/)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [release-please](https://github.com/google-github-actions/release-please-action) (automated releases)
- [Semantic Versioning](https://semver.org/) & [Calendar Versioning](https://calver.org/)

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
