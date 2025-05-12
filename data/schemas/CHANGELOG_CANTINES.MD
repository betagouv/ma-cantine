# Changelog

Tous les changements notables apportés aux jeux de données exposés sur data.gouv.fr vont être documentés ici.

## 2025-05-12

### Modification
- La colonne 'line_ministry' renvoie maintenant le libellé complet du ministère de tutelle (au lieu du code interne)

## 2025-02-07

### Ajout
* Colonne 'declaration_donnees_2024_en_cours'

### Modification
* La colonne 'declaration_donnees_2023_en_cours' est renommée en 'declaration_donnees_2023'

## 2024-07-25

### Suppression
* Colonne 'publication_status' : Depuis fin mai, toutes les cantines sont maintenant publiées sur la plateforme ma-cantine. Ce champ est désormais obsolète.

## 2024-03-29

### Modification
* Colonne 'sectors' : le format passe de `[{'id': 27, 'name': 'Secondaire lycée agricole', 'category': 'education', 'hasLineMinistry': False}, {'id': 87, 'name': 'Ecole primaire (maternelle et élémentaire)', 'category': 'education', 'hasLineMinistry': False}]` à `"[""Secondaire lycées agricole"", ""Ecole primaire (maternelle et élémentaire""]"` afin d'être compatible au format et alléger la colonne

## 2024-02-16

### Ajout
* Colonne 'epci_lib': Libellé de l'EPCI

## 2024-02-13

### Ajout
* Fichier au format parquet
* Fichier au format xlsx

## 2024-02-07

### Ajout
* Colonne 'declaration_donnees_2022'
* Colonne 'declaration_donnees_2023_en_cours'
