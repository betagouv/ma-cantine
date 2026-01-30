# Changelog

Tous les changements notables apportés aux jeux de données exposés sur data.gouv.fr vont être documentés ici.

## 2026-01-30

### Modification

* La colonne `teledeclaration_id` est supprimée (il y a déjà `id`)

## 2025-12-23

### Modification

* La colonne `canteen_sectors` est renommée à `canteen_sector_list`, et renvoie maintenant une liste de secteurs sous forme de chaine de caractères séparés par une virgule

## 2025-05-14

### Modification

- La colonne 'canteen_line_ministry' renvoie maintenant le libellé complet du ministère de tutelle de la cantine (au lieu de son nom interne)

## 2024-04-03

### Ajouts

* Jeu de données télédéclaration 2022

### Modification

* Amélioration du remplissage des données `department` et `region` pour les jeux de données télédéclaration
* Uniformisation du nom de colonnes :
    * `cantine_central_kitchen_siret` => `canteen_central_kitchen_siret`
    * `cantine_satellite_canteens_count` => `canteen_satellite_canteens_count`
    * `cantine_management_type` => `canteen_management_type`
    * `cantine_production_type` => `canteen_production_type`

## 2024-03-29

### Modification

* Renommage des colonnes commençants pas 'cantine_' en 'canteen_'
* Colonne 'canteen_sectors' : le format passe de `[{'id': 27, 'name': 'Secondaire lycée agricole', 'category': 'education', 'hasLineMinistry': False}, {'id': 87, 'name': 'Ecole primaire (maternelle et élémentaire)', 'category': 'education', 'hasLineMinistry': False}]` à `"[""Secondaire lycées agricole"", ""Ecole primaire (maternelle et élémentaire""]"` afin d'être compatible au format et alléger la colonne
