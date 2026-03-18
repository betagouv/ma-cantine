# Télédéclarations : détails des versions

Actuellement les dates sont celles des 1ères créations de TD avec la version concernée.

|Version|Année(s) concernée(s)|Date première TD|Date dernière TD|Nombre de TDs|Changements|
|-|-|-|-|-|-|
|16.2|||||- Ajout des champs Canteen.epci et Canteen.pat_list|
|16.1|||||- Enlève les anciens sectors (M2M)<br>- Ajout des champs Canteen.groupe_id et Canteen.is_filled|
|16|2025|12/01/2026||en cours|- Nouveaux champs simplifiée et détaillée<br>- Renommer 'value' en 'valeur', enlever 'ht'<br>- Traduit certains champs en français<br>- Ajout de champs supplémentaires dans les snapshot 'canteen' et 'satellites' (sector_list entre autre)|
|15||||0|- Modifications sur la façon de stocker Canteen.line_ministry|
|14|2024|17/03/2025|30/04/2025|15436|- Ajout du champ Canteen.canteen_siren_unite_legale|
|13|2024|05/03/2025|17/03/2025|3371|- Ajout du champ Canteen.sectors.category_name|
|12|2024|07/01/2025|05/03/2025|4879|- Nouveau champ Diagnostic.service_type (et arrêter de remplir Diagnostic.vegetarian_menu_type)|
|11||||0|- Check pour s'assurer que Diagnostic.declaration_mode est rempli pour les cuisines centrales|
|10|2022, 2023|26/06/2023|11/06/2024|12123|- Ajout du champ Canteen.department<br>- Ajout du champ Canteen.region|
|9|2022|13/02/2023|26/06/2023|4724|- Suppression de certains champs : Diagnostic.value_pat_ht, Diagnostic.value_label_hve, Diagnostic.value_label_rouge, Diagnostic.value_label_aoc_igp, Diagnostic.value_pat_ht<br>- Ajout des champs Declared data>teledeclaration>Year, Gaspi & Vege<br>- Ajout de satellites_snapshot (id, name, siret, sectors, daily_meal_count, yearly_meal_count)|
|8||||0||
|7||||0||
|6||||0||
|5|2021|05/09/2022|05/12/2022|3204|- De nombreux champs (meat/poultry, fish..) devenus obligatoires (plus de valeurs vides)|
|4|2021|29/08/2022|30/08/2022|14|- Ajout du champ canteen.id|
|3|2021|26/07/2022|26/08/2022|64|- Nouveaux champs du diagnostic complet|
|2|2021|21/07/2022|21/07/2022|1|- Nouveaux champs version simplifiée|
|1||||0||
|None|2020, 2021|13/09/2021|19/07/2022|239|- Toutes les TD créées avant la v2|
