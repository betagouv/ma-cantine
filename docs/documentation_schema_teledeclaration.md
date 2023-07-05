> :warning: FICHIER GENERE AUTOMATIQUEMENT. NE PAS MODIFIER. POUR TOUTE MODIFICATION, EDITEZ LE FICHIER schema_teledeclaration.json /////


### Modèle de données

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|id (Identifiant Télédéclaration)|nombre entier|Identifiant unique de la télédéclaration|15572||
|applicant_id (Identifiant de)|nombre entier|Identifiant unique de la personne ayant télédéclaré. Cette personne est rattachée à la cantine référencée par le champ 'canteen_id'|2717||
|teledeclaration_mode (Mode de télédéclaration)|chaîne de caractères|Mode de télédéclaration. Il existe 4 types différents : CENTRAL_APPRO (cuisine centrale déclarant les données d'appro pour ses cuisines satellites), CENTRAL_ALL (cuisine centrale déclarant toutes les données EGAlim pour ses cuisines satellites), SITE (cantine déclarant ses propres données), SATELLITE_WITHOUT_APPRO (cantine satellite dont les données d'appro sont déclarées par la cuisine centrale). Dans ce dernier cas, le champ central_producer_siret renseigne l'identifiant SIRET de la cuisine préparant les repas. Dans le cas d'une cantine qui cuisine pour d'autres cantines, le champ satellite_canteens_count renseigne le nombre de cantines satellites.|SITE||
|creation_date (Date de création)|chaîne de caractères|Date de création de la télédéclaration|2019-04-01T00:00:00.000Z||
|year (Année)|nombre entier|Année de la télédéclaration|2022||
|version (Version)|chaîne de caractères|Version de la télédéclaration|9||
|canteen_id (Identifiant Cantine)|nombre entier|Identifiant unique de la cantine ayant télédéclaré|15572||
|canteen_siret (Identifiant de)|chaîne de caractères|Identifiant du [Système d'Identification du Répertoire des Etablissements](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27identification_du_r%C3%A9pertoire_des_%C3%A9tablissements) (SIRET) qui identifie la cantine ayant télédéclaré|78542453200014||
|canteen_name (Nom de la cantine)|chaîne de caractères|Nom de la cantine ayant télédéclaré|ASS GEST STE FOY INSTIT ST DOMINIQUE||
|cantine_central_kitchen_siret (Identifiant de la cuisine centrale)|chaîne de caractères|Identifiant du [Système d'Identification du Répertoire des Etablissements](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27identification_du_r%C3%A9pertoire_des_%C3%A9tablissements) (SIRET) qui identifie la cuisine centrale a la quelle la cantine est rattachée|||
|canteen_department (Code Département)|chaîne de caractères|Code Insee du département dans lequel se trouve la cantine|50||
|canteen_region (Code Département)|chaîne de caractères|Code Insee de la région dans lequel se trouve la cantine|28||
|cantine_satellite_canteens_count (Nombre de cantines satellites)|nombre entier|Nombre de cantines satellites pour une cantine qui produit les repas sur place|0||
|cantine_economic_model (Modèle Economique de la cantine)|chaîne de caractères|Modèle économique de la cantine. Il existe 2 types différents : public (cantine publique), private (cantine privée).|public||
|cantine_management_type (Type de Management de la cantine)|chaîne de caractères|Gestionnaire de la cantine. La cantine peut-être gérée directement ou de manière concédée. Si la valeur est 'concédée', la délégation peut être totale ou partielle|conceded||
|cantine_production_type (Type de Production de la cantine)|chaîne de caractères|Lieu de production et de service des repas. Il existe 4 types différents : central (cuisine centrale sans lieu de consommation), central_serving (cuisine centrale qui accueille aussi des convives sur place), site (cantine qui produit les repas sur place), site_cooked_elsewhere (cantine qui sert des repas preparés par une cuisine centrale, appelé également satellite). Dans ce dernier cas, le champ central_producer_siret renseigne l'identifiant SIRET de la cuisine préparant les repas. Dans le cas d'une cantine qui cuisine pour d'autres cantines, le champ satellite_canteens_count renseigne le nombre de cantines satellites.|central||
|canteen_sectors (Secteurs)|liste|Liste définissant les secteurs d'activités concernés par le télédéclaration. Chaque élément de cette liste est défini par quatre paramètres :  id, name, category, has_line_ministry (ministère de tutelle).|[{'id': 12, 'name': 'Ecole primaire (maternelle et élémentaire)', 'category': 'education', 'has_line_ministry': false}]||
|canteen_line_ministry (Ministère de tutelle)|chaîne de caractères|Ministère de tutelle de la cantine, s'il y en a un|Ministère de l'Education Nationale||
|teledeclaration_ratio_bio (Télédéclaration Ratio Bio)|float|Part du bio dans les achats alimentaires de l'année (ratio basé sur le montant des achats en € HT)|0.1||
|teledeclaration_ratio_egalim_hors_bio (Télédéclaration Ratio Bio)|float|Part du bio dans les achats alimentaires de l'année|0.1||
