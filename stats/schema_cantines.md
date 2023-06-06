
### Modèle de données

|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|id (Identifiant)|nombre entier|Identifiant Unique de la Cantine|71331||
|name (Nom)|chaîne de caractères|Nom la Cantine|Restaurant Scolaire de Marigny-le-Lozon||
|siret (Siret)|chaîne de caractères|Identifiant du [Système d'Identification du Répertoire des Etablissements](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27identification_du_r%C3%A9pertoire_des_%C3%A9tablissements) (SIRET) qui identifie la cantine|20005822000092||
|city (Ville)|chaîne de caractères|Ville dans laquelle se trouve la cantine|Marigny-Le-Lozon||
|city_insee_code (Code INSEE ville)|chaîne de caractères|Code INSEE de la ville dans laquelle se trouve la cantine|50292||
|postal_code (Code postal)|chaîne de caractères|Code postal de la ville dans laquelle se trouve la cantine|50570||
|department (Code Département)|chaîne de caractères|Code INSEE du département dans lequel se trouve la cantine|50||
|region (Code Département)|chaîne de caractères|Code INSEE de la région dans lequel se trouve la cantine|28||
|economic_model (Modèle Economique)|chaîne de caractères|Modèle économique de la cantine. Il existe 2 types différents : public (cantine publique), private (cantine privée).|public||
|management_type (Type de Management)|chaîne de caractères|Gestionnaire de la cantine. La cantine peut-être gérée directement ou de manière concédée|conceded||
|production_type (Type de Production)|chaîne de caractères|Lieu de production et de service des repas. Il existe 4 types différents : central (cuisine centrale sans lieu de consommation), central_serving (cuisine centrale qui accueille aussi des convives sur place), site (cantine qui produit les repas sur place), site_cooked_elsewhere (cantine qui sert des repas preparés par une cuisine centrale, appelé également satellite). Dans ce dernier cas, le champ central_producer_siret renseigne l'identifiant SIRET de la cuisine préparant les repas. Dans le cas d'une cantine qui cuisine pour d'autres cantines, le champ satellite_canteens_count renseigne le nombre de cantines satellites.|central||
|satellite_canteens_count (Nombre de cantines satellites)|nombre réel|Gestionnaire de la cantine. La cantine peut-être gérée directement ou de manière concédée|0||
|central_producer_siret (SIRET de la cantine centrale)|chaîne de caractères|Identifiant du [Système d'Identification du Répertoire des Etablissements](https://fr.wikipedia.org/wiki/Syst%C3%A8me_d%27identification_du_r%C3%A9pertoire_des_%C3%A9tablissements) (SIRET) qui identifie la cantine ayant produit les repas|||

### Modèle de données (a valider)
|Nom|Type|Description|Exemple|Propriétés|
|-|-|-|-|-|
|vegetarian_expe_participant|chaîne de caractères|||
|creation_mtm_medium|chaîne de caractères|||
|email_no_diagnostic_first_reminder|chaîne de caractères|||
|creation_date|chaîne de caractères|||
|creation_mtm_source|chaîne de caractères|||
|daily_meal_count|nombre réel|||
|deletion_date|chaîne de caractères|||
|line_ministry|chaîne de caractères|||
|diversification_comments|chaîne de caractères|||
|yearly_meal_count|nombre réel|||
|creation_mtm_campaign|chaîne de caractères|||
|modification_date|chaîne de caractères|||
|logo|chaîne de caractères|||
|publication_comments|chaîne de caractères|||
|plastics_comments|chaîne de caractères|||
|has_been_claimed|booléen|||
|import_source|chaîne de caractères|||
|publication_status|chaîne de caractères|||
