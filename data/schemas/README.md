# Général

Dans ce dossier sont traités les schémas de données utilisés pour publier les jeux de données suivants en open_data :
* Registre des cantines : schema_cantine.json
* Résultats des campagnes de télédéclaration : schema_teledeclaration.json

Les fichiers de

# Documentation

La documentation est générée depuis les fichiers `.json` et est stockée dans le dossier docs/, au format `.md`

Afin de regénérer la documentation, utilisez [table-schema-to-markdown](https://pypi.org/project/table-schema-to-markdown/)

# Paramètres non retenus

Pour chaque schema, il existe un fichier `param_non_retenus_<NOM_DU_JEU>.json`
L'objectif est de s'assurer qu'au aucun oublie n'a été fait dans la liste des paramètres présents dans les bases de données. 
