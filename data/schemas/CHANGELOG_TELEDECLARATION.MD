# Changelog

Tous les changements notables apportés aux jeux de données exposés sur data.gouv.fr vont être documentés ici.

## 2024-03-29

### Modification

* Renommage des colonnes commençants pas 'cantine_' en 'canteen_'
* Colonne 'canteen_sectors' : le format passe de `[{'id': 27, 'name': 'Secondaire lycée agricole', 'category': 'education', 'hasLineMinistry': False}, {'id': 87, 'name': 'Ecole primaire (maternelle et élémentaire)', 'category': 'education', 'hasLineMinistry': False}]` à `"[""Secondaire lycées agricole"", ""Ecole primaire (maternelle et élémentaire""]"` afin d'être compatible au format et alléger la colonne
