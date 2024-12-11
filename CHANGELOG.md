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
* **ETL:** Implementation des champs cantines analyses ([#4538](https://github.com/betagouv/ma-cantine/issues/4538)) ([54217c9](https://github.com/betagouv/ma-cantine/commit/54217c92a1a0bf835674ffed46f8d3c3711d5e35))


### Corrections (bugs, typos...)

* **Achats:** Corrige une erreur d'ortographe dans une notification ([#4592](https://github.com/betagouv/ma-cantine/issues/4592)) ([24bd684](https://github.com/betagouv/ma-cantine/commit/24bd68491c2986426f23bb6857073cd51629b921))
* **Affiche:** répare une erreur dans la console pour certaines cantines ([#4594](https://github.com/betagouv/ma-cantine/issues/4594)) ([596cb1b](https://github.com/betagouv/ma-cantine/commit/596cb1bc4b47d5c0db35cc845dd49dc3e0d80b11))
* Corriger types pour certaines colonnes dans schema ([9f80f23](https://github.com/betagouv/ma-cantine/commit/9f80f239f661626d92dc8580e9cdef4138c9f6f0))
* **Imports:** Mini ajustements sur le wording simples/détaillés ([#4593](https://github.com/betagouv/ma-cantine/issues/4593)) ([9e12c13](https://github.com/betagouv/ma-cantine/commit/9e12c133b86169df641fc96c43ac76b3a6f1b8f9))
* **Tunnel Diagnostique:** Gaspillage: répare la fermeture de la modale XP réservation ([#4734](https://github.com/betagouv/ma-cantine/issues/4734)) ([d55a3f4](https://github.com/betagouv/ma-cantine/commit/d55a3f4e95565d4f0ffe1cb6537627b2869ed20a))
* Utilisaiton de la variable token dans test ([30751a4](https://github.com/betagouv/ma-cantine/commit/30751a45c39421d7bbe13fbe7a6e50ec8d994464))


### Technique

* add isort to the pre-commit config ([cdb02da](https://github.com/betagouv/ma-cantine/commit/cdb02daa55c490612abc1c26ea18748107fa7131))
* Ajoute un nouveau type 'improve' dans la config release-please ([#4758](https://github.com/betagouv/ma-cantine/issues/4758)) ([db97d73](https://github.com/betagouv/ma-cantine/commit/db97d73118315feca91e88fdab83da56dcdb6692))
* auto-add reviewers to new PRs ([607cec8](https://github.com/betagouv/ma-cantine/commit/607cec8eb41f3cce3fe990e214be8021a3ee4a78))
* **Diagnostique:** renomme les enum végé (MenuType & MenuFrequency) pour clarifier ([#4717](https://github.com/betagouv/ma-cantine/issues/4717)) ([b64642c](https://github.com/betagouv/ma-cantine/commit/b64642c53f3700770d213def830bd6dd382b6ef5))
* Github Action pour checker que le nom des PR respecte le format Conventional Commits ([#4700](https://github.com/betagouv/ma-cantine/issues/4700)) ([adbec3c](https://github.com/betagouv/ma-cantine/commit/adbec3cae0518426c853730148a27446b4108bd8))
* Github Action pour lancer release-please ([#4701](https://github.com/betagouv/ma-cantine/issues/4701)) ([2ab220b](https://github.com/betagouv/ma-cantine/commit/2ab220b5d01440f33d815396239de08565d754b6))
* **Mentions légales:** Migration de la page sur vue 3 ([#4725](https://github.com/betagouv/ma-cantine/issues/4725)) ([74ad0c2](https://github.com/betagouv/ma-cantine/commit/74ad0c2203b8575be8efa0547e9bc3e77aba290a))
* refactor pre-commit by moviing repo & rev keys up ([560db84](https://github.com/betagouv/ma-cantine/commit/560db84a6bad96f3690b5be4ee579dea03989e8f))
* release 2024.12.0 ([c6b2432](https://github.com/betagouv/ma-cantine/commit/c6b24329615b438279a8dea56557523e111fa284))

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
