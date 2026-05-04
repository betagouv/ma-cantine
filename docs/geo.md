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

### Recherche Entreprises

Elle nous permet de récupérer, à partir d'un Siret, le code Insee d'une cantine. Mais aussi d'autres informations géographiques et administratives.

Plus d'infos dans [common/api/recherche_entreprises.py](../common/api/recherche_entreprises.py).

### Découpage Administratif

Elle nous permet de récupérer l'ensemble des communes (dont les arrondissements), epci, départements & régions.

Plus d'infos dans [common/api/decoupage_administratif.py](../common/api/decoupage_administratif.py).

### Data Gouv

Elle nous permet de récupérer l'ensemble des PAT (Projets Alimentaires Territoriaux).

Plus d'infos dans [common/api/datagouv.py](../common/api/datagouv.py).

### Autres

On stock actuellement en dure la liste des départements ([data/department_choices.py](../data/department_choices.py)) et des régions ([data/region_choices.py](../data/region_choices.py)).

## Comment ça marche ?

* Un signal `post_save` est envoyé à chaque fois qu'une cantine est créée ou mise à jour
* Si la cantine a un `siret` mais pas de `city_insee_code`, on appelle `update_canteen_geo_fields_from_siret`
* Si la cantine a un `siren_unite_legale` et un `city_insee_code` mais pas de données géographiques, on appelle `update_canteen_geo_data_from_insee_code`

## FAQ

### Pourquoi stocker les libellés ?

* Pour éviter de devoir stocker l'ensemble des données et faire des mapping à la volée
* Pour avoir les même données disponibles partout (App, Admin, Metabase, Open Data)

### Pourquoi stocker les départements et les régions, mais pas les communes et les epcis ?

* Choix historique
* Parce que ça ne change pas souvent
* Pas besoin d'appel API pour récupérer le libellé
* Il y a un mapping entre départements et régions

### Pourquoi on utilise du cache ?

* Pour éviter de faire des appels API à chaque fois qu'on a besoin de récupérer les données géographiques
* Vu que les données géo "Découpage Administratif" et "PAT" ne changent (quasiment) jamais

### Comment gérer la MAJ annuelle des communes et EPCI ?

voir [common/api/decoupage_administratif.py](../common/api/decoupage_administratif.py)

à compléter

### Comment gérer la MAJ annuelle des PAT ?

voir [common/api/datagouv.py](../common/api/datagouv.py)

à compléter
