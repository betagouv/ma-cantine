# Open Data

## Fichiers disponibles

### Registre national des cantines

https://www.data.gouv.fr/datasets/registre-national-des-cantines/

### Résultats de campagnes de télédéclaration des cantines

https://www.data.gouv.fr/datasets/resultats-de-campagnes-de-teledeclaration-des-cantines/

### Schémas

Pour chacun des fichiers (cantines & télédéclarations), un schéma au format JSON est disponible.

### Stockage

- les fichiers de données sont stockés sur Clever Cloud
- les schémas sont stockés sur Github

## Ajouter un fichier

1. Générer le fichier et le stocker sur Clever Cloud (ou Github)
2. Se connecter à l'interface admin de data.gouv
3. Cliquer sur "Ajouter des fichiers" et remplir le formulaire

## Stocker une copie sur Github

1. avoir récupéré en local le backup de la nuit
2. modifier `macantine/etl/open_data.py` : dans `load_dataset`, mettre `datagouv=False` (pour éviter de pusher)
3. lancer les exports
```
python manage.py export_dataset --model Canteen --destination opendata
python manage.py export_dataset --model Teledeclaration --destination opendata
```
4. copier les données dans le dossier opendata
```
cp media/open_data/registre_cantines.csv opendata/registre_cantines.csv
cp media/open_data/campagne_td_2021.csv opendata/campagne_td_2021.csv
cp media/open_data/campagne_td_2022.csv opendata/campagne_td_2022.csv
cp media/open_data/campagne_td_2023.csv opendata/campagne_td_2023.csv
cp media/open_data/campagne_td_2024.csv opendata/campagne_td_2024.csv
```
