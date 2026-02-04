### Modèle de données

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|id (Identifiant)|nombre entier|Identifiant unique de la cantine|71331||
|name (Nom)|chaîne de caractères|Nom la cantine|Restaurant Scolaire de Marigny-le-Lozon||
|siret (Siret)|chaîne de caractères|Identifiant du [Système d'Identification du Répertoire des Etablissements](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27identification_du_r%C3%A9pertoire_des_%C3%A9tablissements) (SIRET) qui identifie la cantine|20005822000092||
|city (Ville)|chaîne de caractères|Ville dans laquelle se trouve la cantine|Marigny-Le-Lozon||
|city_insee_code (Code Insee ville)|chaîne de caractères|Code Insee de la ville dans laquelle se trouve la cantine|50292||
|postal_code (Code postal)|chaîne de caractères|Code postal de la ville dans laquelle se trouve la cantine|50570||
|department (Code Département)|chaîne de caractères|Code Insee du département dans lequel se trouve la cantine|29||
|department_lib (Département Libellé)|chaîne de caractères|Libellé du département dans lequel se trouve la cantine|Finistère||
|region (Code Région)|chaîne de caractères|Code Insee de la région dans lequel se trouve la cantine|53||
|region_lib (Région libellé)|chaîne de caractères|Libellé de la région dans lequel se trouve la cantine|Bretagne||
|economic_model (Modèle Economique)|chaîne de caractères|Modèle économique de la cantine. Il existe 2 types différents : public (cantine publique), private (cantine privée).|public||
|management_type (Type de Management)|chaîne de caractères|Gestionnaire de la cantine. La cantine peut être gérée directement ('direct') ou de manière concédée ('conceded'). Si de manière concédée, la délégation peut être totale ou partielle.|conceded||
|production_type (Type de Production)|chaîne de caractères|Lieu de production et de service des repas. Il existe 4 types différents : central (cuisine centrale sans lieu de consommation), central_serving (cuisine centrale qui accueille aussi des convives sur place), site (cantine qui produit les repas sur place), site_cooked_elsewhere (cantine qui sert des repas preparés par une cuisine centrale, appelé également restaurant satellite). Dans ce dernier cas, le champ central_producer_siret renseigne l'identifiant SIRET de la cuisine préparant les repas. Dans le cas d'une cantine qui cuisine pour d'autres cantines, le champ satellite_canteens_count renseigne le nombre de restaurants satellites.|central||
|satellite_canteens_count (Nombre de restaurants satellites)|nombre entier|Nombre de restaurants satellites pour une cuisine centrale|0||
|central_producer_siret (SIRET de la cantine centrale)|chaîne de caractères|Identifiant du [Système d'Identification du Répertoire des Etablissements](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27identification_du_r%C3%A9pertoire_des_%C3%A9tablissements) (SIRET) qui identifie la cantine ayant produit les repas|||
|creation_date (Date de création)|chaîne de caractères|Date de création de la cantine au format ISO 8601|2018-01-01||
|daily_meal_count (Nombre de repas par jour)|nombre entier|Nombre de repas servis, en moyenne, par jour dans la cantine|100||
|yearly_meal_count (Nombre de repas par an)|nombre entier|Nombre de repas servis, en moyenne, par an dans la cantine|20000||
|line_ministry (Ministère de tutelle)|chaîne de caractères|Ministère de tutelle de la cantine, s'il y en a un|Ministère de l'Education Nationale||
|modification_date (Date de modification)|chaîne de caractères|Date de dernière modification de la cantine au format ISO 8601|2018-01-01||
|logo (Logo)|chaîne de caractères|Logo de la cantine|https://www.mangerlocal.fr/static/img/logo.png||
|sectors (Secteurs)|liste|Liste définissant les secteurs d'activités de la cantine. Chaque élément de cette liste est défini par quatre paramètres :  id, name, category, has_line_ministry (ministère de tutelle).|["{'id': 12, 'name': 'Ecole primaire (maternelle et élémentaire)', 'category': 'education', 'has_line_ministry': false}"]||
|active_on_ma_cantine (Actif sur Ma Cantine)|booléen|A un gestionnaire sur (email) et a fais au moins une action (à définir) - Indique si la cantine est active sur l'apllication Ma Cantine ou si elle a été importée via une source de données externe|true||
