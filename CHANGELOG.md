# Journal des modifications

Ressources :
- [CHANGELOG recommendations](https://keepachangelog.com/)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [release-please](https://github.com/google-github-actions/release-please-action) (automated releases)
- [Semantic Versioning](https://semver.org/) & [Calendar Versioning](https://calver.org/)

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
