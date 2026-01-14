# Données géographiques

## Quelles données ?

Le modèle `Canteen` stock un certain nombre de données géographiques.

|Nom|Type|Description|Exemple|
|-|-|-|-|
|city_insee_code|chaîne de caractères|Code Insee de la ville dans laquelle se trouve la cantine|38185|
|city|chaîne de caractères|Ville dans laquelle se trouve la cantine|Grenoble|
|postal_code|chaîne de caractères|Code postal de la ville dans laquelle se trouve la cantine|38000|
|epci|chaîne de caractères|Code EPCI dans lequel se trouve la cantine|200040715|
|epci_lib|chaîne de caractères|Libellé de l'EPCI dans lequel se trouve la cantine|Grenoble-Alpes-Métropole|
|pat_list|liste de chaînes de caractères|||
|pat_lib_list|liste de chaînes de caractères|||
|department|chaîne de caractères|Code Insee du département dans lequel se trouve la cantine|38|
|department_lib|chaîne de caractères|Libellé du département dans lequel se trouve la cantine|Isère|
|region|chaîne de caractères|Code Insee de la région dans lequel se trouve la cantine|84|
|region_lib|chaîne de caractères|Libellé de la région dans lequel se trouve la cantine|Auvergne-Rhône-Alpes|

Le "pivot" est le champ `city_insee_code`. De là en découle, grâce aux APIs, tous les autres champs.

## Quelles API ?

La principale API utilisée est `Découpage Administratif`. Elle nous permet de récupérer l'ensemble des communes, epci, départements & régions. Plus d'infos dans [common/api/decoupage_administratif.py](../common/api/decoupage_administratif.py). En ajoutant des paramètres à l'API, on peut récupérer des données supplémentaires comme les arrondissements (Paris, Lyon, Marseille), ou certains départments & régions d'outre-mer.

On stock actuellement en dure la liste des départements ([data/department_choices.py](../data/department_choices.py)) et des régions ([data/region_choices.py](../data/region_choices.py)).

## Comment ça marche ?

* Si la cantine n'a pas de code Insee (champ `city_insee_code` vide), on tente de le récupérer grâce à sont Siret
    * grâce à une tâche asynchrone
    * `fill_missing_insee_code_using_siret()`
    * fréquence : toutes les heures
    * API : Recherche Entreprises
* Pour les cantines avec `city_insee_code`, mais dont au moins un des champs géographiques est manquante, on tente de les compléter
    * grâce à une tâche asynchrone
    * `fill_missing_geolocation_data_using_insee_code()`
    * fréquence : toutes les nuits
    * API : Découpage Administratif

## FAQ

### Pourquoi stocker les libellés ?

* Pour éviter de devoir stocker l'ensemble des données et faire des mapping à la volée
* Pour avoir les même données disponibles partout (App, Admin, Metabase, Open Data)

### Pourquoi stocker les départements et les régions, mais pas les communes et les epcis ?

* Choix historique
* Parce que ça ne change pas souvent
* Pas besoin d'appel API pour récupérer le libellé
* Il y a un mapping entre départements et régions

### Comment gérer la MAJ annuelle des communes et EPCI ?

à compléter

### Et les PAT ?

à venir
