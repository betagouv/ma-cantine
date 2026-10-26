# ETL

L'ETL extrait les données de la plateforme vers deux destinations :

* **data.gouv.fr** : ouverture des données en open data (cf `open_data.py`)
* **le data warehouse** : copie brute des tables, utilisée comme source par dbt, pour l'analyse et les indicateurs (cf `analysis.py`)

| Tâche celery | Classe | Planification | Résultat |
|---|---|---|---|
| `export_dataset_raw_analysis` | `ETL_ANALYSIS_RAW` | toutes les nuits (prod) | tables `*_raw` dans le data warehouse |
| `export_dataset_canteen_opendata` | `ETL_OPEN_DATA_CANTEEN` | toutes les nuits (prod) | `registre_cantines.csv/.xlsx` |
| `export_dataset_td_opendata` | `ETL_OPEN_DATA_TELEDECLARATIONS` | manuelle, une fois par campagne | `campagne_td_{année}.csv/.xlsx` |

Les planifications sont dans `macantine/celery.py`. Pour lancer un export manuellement :

```sh
python manage.py export_dataset --model Raw --destination analysis
python manage.py export_dataset --model Canteen --destination opendata
python manage.py export_dataset --model Teledeclaration --destination opendata
```

## Open Data

Deux jeux de données sont publiés :

* [Registre national des cantines](https://www.data.gouv.fr/datasets/registre-national-des-cantines/) : les cantines (hors groupes et cantines des armées)
* [Résultats de campagnes de télédéclaration](https://www.data.gouv.fr/datasets/resultats-de-campagnes-de-teledeclaration-des-cantines/) : les télédéclarations retenues pour les statistiques, un fichier par année

Fonctionnement :

1. **Extraction** : queryset + serializer (`CanteenOpenDataSerializer`, `DiagnosticTeledeclaredOpenDataSerializer`) dans un dataframe pandas
2. **Transformation** : les colonnes sont alignées sur le schéma du jeu de données (`data/schemas/export_opendata/`). Attention : une colonne absente du schéma n'est pas exportée
3. **Validation** : le fichier est validé par [Validata](https://validata.fr) avec le schéma publié sur Github. S'il est invalide, il n'est pas publié
4. **Chargement** : les fichiers CSV et XLSX sont stockés sur notre S3 (`open_data/`)
5. **Notification** : l'API de data.gouv.fr est appelée pour mettre à jour l'URL des ressources, afin qu'elles affichent la bonne date de mise à jour (variable d'environnement `DATAGOUV_API_KEY`)

Les fichiers sont référencés depuis l'interface d'administration de data.gouv.fr (compte perso, affiliation nécessaire à l'organisme MASA). Voir aussi `opendata/README.md`.

Lors d'une nouvelle campagne : ajouter l'année dans `get_teledeclaration_opendata_datasets()` (`macantine/etl/datasets.py`, une fois le rapport publié), ainsi que la colonne `declaration_donnees_{année}` dans le serializer et le schéma des cantines.

## Data Warehouse

Les tables sont copiées telles quelles (`ETL_ANALYSIS_RAW`), avec un `COPY` Postgres, sans pandas. Les transformations (traductions, libellés géographiques, indicateurs...) sont faites ensuite par dbt (tâche `dbt_run`, cf `dbt/README.md`), et les tables générées sont utilisées dans Metabase.

* les cantines, diagnostics et achats supprimés (soft delete) sont inclus (cf `deletion_date`)
* les colonnes de type tableau sont converties en `jsonb`
* les données sensibles ne sont pas exportées (cf `exclude_columns` : mots de passe, secrets et tokens OAuth2)
* à chaque export, la table est vidée puis rechargée, ce qui conserve les vues dbt qui en dépendent. Si une colonne a été supprimée ou a changé de type, la table est recréée (les vues dépendantes sont supprimées, `dbt run` les recrée)

Pour exporter une nouvelle table : l'ajouter dans `get_raw_analysis_datasets()` (`macantine/etl/datasets.py`), puis la déclarer comme source dans `dbt/models/staging/sources.yml`.

Connexion : variables d'environnement `DATA_WARE_HOUSE_HOST`, `DATA_WARE_HOUSE_PORT`, `DATA_WARE_HOUSE_DB`, `DATA_WARE_HOUSE_USER` et `DATA_WARE_HOUSE_PASSWORD`.
