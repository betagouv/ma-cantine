# Général

L'ETL permet d'extraire des données issues de la plateforme vers :
* data.gouv.fr : pour l'ouverture en open-data (cf `ETL_OPEN_DATA`)
* un data wharehouse : pour l'analyse et la création d'indicateurs (cf `ETL_ANALYSIS`)

Pour chaque destination, deux jeux de données sont édités et publiés :

* cantines (cf cf `ETL_OPEN_DATA_CANTEENS` et `ETL_ANLYSIS_CANTEENS`)
* télédéclarations (cf cf `ETL_OPEN_DATA_TD` et `ETL_ANLYSIS_TD`)

## Open Data

Les données sont stockées sur notre S3 puis référencées depuis l'intertace d'administration de data.gouv.fr (compte perso, affiliation nécessaire à l'organisme MASA).

L'API de data.gouv.fr est utilisée afin de "notifier" data.gouv.fr des mises à jour de fichier et ainsi permettre d'afficher les informatiojns correctes sur lma fréquence de mise à jour ainsi que la date de la dernière modification.

Nous validons les jeux de données en couplant l'outil validata avec le schéma de donnée de chaque jeu.

Les résutats des campagnes des TD sont millisimés (un fichier par année)

## Data Warehouse

Les données sont exportées dans un postgres.
Parmis les transformations apportées, nous :

* traduisons les champs en français (car à destination des équipes métiers)
* apportons plus d'informations géographiques (libellés des départemets/régions, epci...)

Nous connectons l'outil de dataviz à ce postgres afin de construire nos indicateurs.
