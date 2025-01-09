# Général

Dans ce dossier sont traités les schémas de données utilisés pour publier les jeux de données suivants en open_data :
* Registre des cantines : `schema_cantine.json`
* Résultats des campagnes de télédéclaration : `schema_teledeclaration.json`

## Documentation

La documentation est générée depuis les fichiers `.json` et est stockée dans le dossier docs/, au format `.md`

Afin de regénérer la documentation, utilisez [table-schema-to-markdown](https://pypi.org/project/table-schema-to-markdown/)

## Paramètres non retenus

Pour chaque schema, il existe un fichier `param_non_retenus_<NOM_DU_JEU>.json`
L'objectif est de s'assurer qu'au aucun oublie n'a été fait dans la liste des paramètres présents dans les bases de données.

## Imports

|Schema|Fichier|URL|
|---|---|---|
|Cantines|[`imports/cantines.json`](https://github.com/betagouv/ma-cantine/blob/main/data/schemas/imports/cantines.json)|[/importer-diagnostics/cantines-seules](https://ma-cantine.agriculture.gouv.fr/importer-diagnostics/cantines-seules)|
|Cantine(s) et bilan(s) simple(s)|[`imports/diagnostics.json`](https://github.com/betagouv/ma-cantine/blob/main/data/schemas/imports/diagnostics.json)|[/importer-diagnostics/cantines-et-diagnostics-simples](https://ma-cantine.agriculture.gouv.fr/importer-diagnostics/cantines-et-diagnostics-simples)|
|Cantine(s) et bilan(s) détaillé(s)|[`imports/diagnostics_complets.json`](https://github.com/betagouv/ma-cantine/blob/main/data/schemas/imports/diagnostics_complets.json)|[/importer-diagnostics/cantines-et-diagnostics-complets](https://ma-cantine.agriculture.gouv.fr/importer-diagnostics/cantines-et-diagnostics-complets)|
|Cuisine centrale et bilan(s) simple(s)|[`imports/diagnostics_cc.json`](https://github.com/betagouv/ma-cantine/blob/main/data/schemas/imports/diagnostics_cc.json)|[/importer-diagnostics/cuisine-centrale-diagnostics-simples](https://ma-cantine.agriculture.gouv.fr/importer-diagnostics/cuisine-centrale-diagnostics-simples)|
|Cuisine centrale et bilan(s) détaillé(s)|[`imports/diagnostics_complets_cc.json`](https://github.com/betagouv/ma-cantine/blob/main/data/schemas/imports/diagnostics_complets_cc.json)|[/importer-diagnostics/cuisine-centrale-diagnostics-complets](https://ma-cantine.agriculture.gouv.fr/importer-diagnostics/cuisine-centrale-diagnostics-complets)|
|Achats|[`imports/achats.json`](https://github.com/betagouv/ma-cantine/blob/main/data/schemas/imports/achats.json)|[/importer-achats](https://ma-cantine.agriculture.gouv.fr/importer-achats/)|
