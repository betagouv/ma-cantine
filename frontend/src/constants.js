export default Object.freeze({
  LoadingStatus: {
    LOADING: 1,
    SUCCESS: 2,
    ERROR: 3,
    IDLE: 4,
  },
  DefaultDiagnostics: {
    id: null,
    year: null,
    valueBioHt: null,
    valueSustainableHt: null,
    valueTotalHt: null,
    hasWasteDiagnostic: null,
    hasWastePlan: null,
    wasteActions: [],
    hasDonationAgreement: null,
    hasDiversificationPlan: null,
    vegetarianWeeklyRecurrence: null,
    vegetarianMenuType: null,
    vegetarianMenuBases: [],
    cookingPlasticSubstituted: null,
    servingPlasticSubstituted: null,
    plasticBottlesSubstituted: null,
    plasticTablewareSubstituted: null,
    communicationSupports: [],
    communicationSupportUrl: null,
    communicatesOnFoodPlan: null,
  },
  ManagementTypes: [
    {
      text: "Directe",
      value: "direct",
    },
    {
      text: "Concédée",
      value: "conceded",
    },
  ],
  ProductionTypes: [
    {
      text: "Livreurs des repas",
      value: "central,central_serving",
    },
    {
      text: "Restaurants satellites et autogérés",
      value: "site,site_cooked_elsewhere",
    },
  ],
  ProductionTypesDetailed: [
    {
      title: "produit sur place les repas qu'il sert à ses convives",
      body: "Mon établissement prépare ce qu'il sert à ses convives",
      value: "site",
    },
    {
      title: "sert des repas preparés par un autre établissement",
      body: "Les repas que mon établissement sert à ses convives sont cuisinés ailleurs",
      value: "site_cooked_elsewhere",
    },
    {
      title: "livre des repas mais n'a pas de lieu de service en propre",
      body: "Mon établissement livre des repas mais n'a pas de lieu de service en propre",
      value: "central",
    },
    {
      title: "livre des repas et accueille aussi des convives sur place",
      body: "Mon établissement livre des repas et accueille aussi des convives sur place",
      value: "central_serving",
    },
  ],
  EconomicModels: [
    { text: "Public", value: "public" },
    { text: "Privé", value: "private" },
  ],
  ProductFamilies: {
    VIANDES_VOLAILLES: {
      text: "Viandes et volailles fraîches et surgelées",
      shortText: "viandes et volailles",
      color: "pink darken-4",
    },
    CHARCUTERIE: {
      text: "Charcuterie",
      shortText: "charcuterie",
      color: "pink darken-4",
    },
    PRODUITS_DE_LA_MER: {
      text: "Produits de la mer et aquaculture frais et surgelés",
      shortText: "produits de la mer et aquaculture",
      color: "blue darken-3",
    },
    FRUITS_ET_LEGUMES: {
      text: "Fruits et légumes frais et surgelés",
      shortText: "fruits et légumes",
      color: "green darken-3",
    },
    PRODUITS_LAITIERS: {
      text: "BOF (Produits laitiers, beurre et œufs)",
      shortText: "BOF",
      color: "deep-orange darken-4",
    },
    BOULANGERIE: {
      text: "Boulangerie / Pâtisserie fraîches et surgelées",
      shortText: "boulangerie / pâtisserie",
      color: "deep-purple darken-3",
    },
    BOISSONS: {
      text: "Boissons",
      shortText: "boissons",
      color: "green darken-4",
    },
    AUTRES: {
      text: "Autres produits frais, surgelés et d’épicerie",
      shortText: "autres produits",
      color: "grey darken-3",
    },
  },
  Characteristics: {
    // NB: the order of these keys reflects the priority of the label in EGalim sum calculations
    // NB: the order of these can affect the aesthetics of the display on PurchasePage, esp for long texts
    BIO: { text: "Bio" },
    LABEL_ROUGE: { text: "Label rouge" },
    AOCAOP: { text: "AOC / AOP", longText: "Appellation d'origine (AOC / AOP)" },
    IGP: { text: "IGP", longText: "Indication géographique protégée (IGP)" },
    STG: { text: "STG", longText: "Spécialité traditionnelle garantie (STG)" },
    HVE: { text: "HVE", longText: "Certification environnementale de niveau 2 ou HVE" },
    PECHE_DURABLE: { text: "Écolabel pêche durable" },
    RUP: { text: "RUP", longText: "Région ultrapériphérique (RUP)" },
    COMMERCE_EQUITABLE: { text: "Commerce équitable" },
    FERMIER: { text: "Fermier", longText: "Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »" },
    EXTERNALITES: {
      text: "Externalités environnementales",
      longText:
        "Produits acquis prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
    },
    PERFORMANCE: {
      text: "Performance environnementale",
      longText: "Produits acquis sur la base de leurs performances en matière environnementale",
    },
    FRANCE: { text: "Provenance France" },
    SHORT_DISTRIBUTION: { text: "Circuit-court" },
    LOCAL: { text: "Local" },
  },
  TeledeclarationCharacteristics: {
    // NB: the order of these can affect the aesthetics of the display on PurchasePage, esp for long texts
    BIO: { text: "Bio", color: "green" },
    LABEL_ROUGE: { text: "Label rouge", color: "red lighten-1" },
    AOCAOP_IGP_STG: {
      text: "AOC / AOP / IGP / STG",
      longText: "AOC / AOP / IGP / STG",
      color: "indigo",
    },
    PECHE_DURABLE: { text: "Écolabel pêche durable", color: "blue" },
    RUP: { text: "RUP", longText: "Région ultrapériphérique (RUP)", color: "brown" },
    COMMERCE_EQUITABLE: { text: "Commerce équitable", color: "lime darken-2" },
    HVE: {
      text: "Certification environnementale de niveau 2 ou HVE",
      longText: "Certification environnementale de niveau 2 ou HVE",
      color: "purple",
    },
    FERMIER: {
      text: "Fermier",
      longText: "Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »",
      color: "orange",
    },
    EXTERNALITES: {
      text: "Externalités environnementales",
      longText:
        "Produits acquis prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie",
      color: "teal",
    },
    PERFORMANCE: {
      text: "Performance environnementale",
      longText: "Produits acquis sur la base de leurs performances en matière environnementale",
      color: "pink",
    },
    NON_EGALIM: { text: "Non-EGalim", color: "blue-grey lighten-2" },
    FRANCE: { text: "Provenance France", additional: true },
    SHORT_DISTRIBUTION: { text: "Circuit-court", additional: true },
    LOCAL: { text: "Local", additional: true },
  },
  LocalDefinitions: {
    AUTOUR_SERVICE: { text: "200 km autour du lieu de service", value: "AUTOUR_SERVICE" },
    DEPARTMENT: { text: "Provenant du même département", value: "DEPARTMENT" },
    REGION: { text: "Provenant de la même région", value: "REGION" },
    AUTRE: { text: "Autre", value: "AUTRE" },
  },
  TeledeclarationCharacteristicGroups: {
    egalim: {
      text:
        "Pour la saisie, vous ne devez affecter le produit qu'une dans une seule catégorie. Par exemple, un produit à la fois biologique et label rouge sera comptabilisé que dans la catégorie 'bio'.",
      characteristics: [
        "BIO",
        "LABEL_ROUGE",
        "AOCAOP_IGP_STG",
        "HVE",
        "PECHE_DURABLE",
        "RUP",
        "COMMERCE_EQUITABLE",
        "FERMIER",
        "EXTERNALITES",
        "PERFORMANCE",
      ],
      fields: [
        "valueViandesVolaillesBio",
        "valueProduitsDeLaMerBio",
        "valueFruitsEtLegumesBio",
        "valueCharcuterieBio",
        "valueProduitsLaitiersBio",
        "valueBoulangerieBio",
        "valueBoissonsBio",
        "valueAutresBio",
        "valueViandesVolaillesLabelRouge",
        "valueProduitsDeLaMerLabelRouge",
        "valueFruitsEtLegumesLabelRouge",
        "valueCharcuterieLabelRouge",
        "valueProduitsLaitiersLabelRouge",
        "valueBoulangerieLabelRouge",
        "valueBoissonsLabelRouge",
        "valueAutresLabelRouge",
        "valueViandesVolaillesAocaopIgpStg",
        "valueProduitsDeLaMerAocaopIgpStg",
        "valueFruitsEtLegumesAocaopIgpStg",
        "valueCharcuterieAocaopIgpStg",
        "valueProduitsLaitiersAocaopIgpStg",
        "valueBoulangerieAocaopIgpStg",
        "valueBoissonsAocaopIgpStg",
        "valueAutresAocaopIgpStg",
        "valueViandesVolaillesHve",
        "valueProduitsDeLaMerHve",
        "valueFruitsEtLegumesHve",
        "valueCharcuterieHve",
        "valueProduitsLaitiersHve",
        "valueBoulangerieHve",
        "valueBoissonsHve",
        "valueAutresHve",
        "valueViandesVolaillesPecheDurable",
        "valueProduitsDeLaMerPecheDurable",
        "valueFruitsEtLegumesPecheDurable",
        "valueCharcuteriePecheDurable",
        "valueProduitsLaitiersPecheDurable",
        "valueBoulangeriePecheDurable",
        "valueBoissonsPecheDurable",
        "valueAutresPecheDurable",
        "valueViandesVolaillesRup",
        "valueProduitsDeLaMerRup",
        "valueFruitsEtLegumesRup",
        "valueCharcuterieRup",
        "valueProduitsLaitiersRup",
        "valueBoulangerieRup",
        "valueBoissonsRup",
        "valueAutresRup",
        "valueViandesVolaillesFermier",
        "valueProduitsDeLaMerFermier",
        "valueFruitsEtLegumesFermier",
        "valueCharcuterieFermier",
        "valueProduitsLaitiersFermier",
        "valueBoulangerieFermier",
        "valueBoissonsFermier",
        "valueAutresFermier",
        "valueViandesVolaillesExternalites",
        "valueProduitsDeLaMerExternalites",
        "valueFruitsEtLegumesExternalites",
        "valueCharcuterieExternalites",
        "valueProduitsLaitiersExternalites",
        "valueBoulangerieExternalites",
        "valueBoissonsExternalites",
        "valueAutresExternalites",
        "valueViandesVolaillesCommerceEquitable",
        "valueProduitsDeLaMerCommerceEquitable",
        "valueFruitsEtLegumesCommerceEquitable",
        "valueCharcuterieCommerceEquitable",
        "valueProduitsLaitiersCommerceEquitable",
        "valueBoulangerieCommerceEquitable",
        "valueBoissonsCommerceEquitable",
        "valueAutresCommerceEquitable",
        "valueViandesVolaillesPerformance",
        "valueProduitsDeLaMerPerformance",
        "valueFruitsEtLegumesPerformance",
        "valueCharcuteriePerformance",
        "valueProduitsLaitiersPerformance",
        "valueBoulangeriePerformance",
        "valueBoissonsPerformance",
        "valueAutresPerformance",
      ],
    },
    nonEgalim: {
      text: "Merci de renseigner les montants des produits hors EGalim",
      characteristics: ["NON_EGALIM"],
      fields: [
        "valueViandesVolaillesNonEgalim",
        "valueProduitsDeLaMerNonEgalim",
        "valueFruitsEtLegumesNonEgalim",
        "valueCharcuterieNonEgalim",
        "valueProduitsLaitiersNonEgalim",
        "valueBoulangerieNonEgalim",
        "valueBoissonsNonEgalim",
        "valueAutresNonEgalim",
      ],
    },
    outsideLaw: {
      text:
        "Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique et local pourra être comptabilisé dans les deux champs 'bio' et 'local'.",
      characteristics: ["FRANCE", "SHORT_DISTRIBUTION", "LOCAL"],
      fields: [
        "valueViandesVolaillesFrance",
        "valueProduitsDeLaMerFrance",
        "valueFruitsEtLegumesFrance",
        "valueCharcuterieFrance",
        "valueProduitsLaitiersFrance",
        "valueBoulangerieFrance",
        "valueBoissonsFrance",
        "valueAutresFrance",
        "valueViandesVolaillesShortDistribution",
        "valueProduitsDeLaMerShortDistribution",
        "valueFruitsEtLegumesShortDistribution",
        "valueCharcuterieShortDistribution",
        "valueProduitsLaitiersShortDistribution",
        "valueBoulangerieShortDistribution",
        "valueBoissonsShortDistribution",
        "valueAutresShortDistribution",
        "valueViandesVolaillesLocal",
        "valueProduitsDeLaMerLocal",
        "valueFruitsEtLegumesLocal",
        "valueCharcuterieLocal",
        "valueProduitsLaitiersLocal",
        "valueBoulangerieLocal",
        "valueBoissonsLocal",
        "valueAutresLocal",
      ],
    },
  },
  CharacteristicFamilyExceptions: {
    BIO: [],
    LABEL_ROUGE: ["BOISSONS"],
    AOCAOP_IGP_STG: [],
    HVE: [],
    PECHE_DURABLE: [
      "FRUITS_ET_LEGUMES",
      "CHARCUTERIE",
      "VIANDES_VOLAILLES",
      "PRODUITS_LAITIERS",
      "BOULANGERIE",
      "AUTRES",
      "BOISSONS",
    ],
    RUP: ["PRODUITS_DE_LA_MER"],
    COMMERCE_EQUITABLE: [],
    FERMIER: ["FRUITS_ET_LEGUMES", "PRODUITS_DE_LA_MER", "BOULANGERIE", "AUTRES", "BOISSONS"],
    EXTERNALITES: [],
    PERFORMANCE: [],
    NON_EGALIM: [],
  },
  TrackingParams: ["mtm_source", "mtm_campaign", "mtm_medium"],
  Jobs: [
    {
      text: "Gestionnaire d'établissement",
      value: "ESTABLISHMENT_MANAGER",
    },
    {
      text: "Direction achat société de restauration",
      value: "CATERING_PURCHASES_MANAGER",
    },
    {
      text: "Responsable d'achats en gestion directe",
      value: "DIRECT_PURCHASES_MANAGER",
    },
    {
      text: "Responsable de plusieurs établissements (type cuisine centrale)",
      value: "CENTRAL_MANAGER",
    },
    {
      text: "Responsable de plusieurs établissements (SRC)",
      value: "MANY_ESTABLISHMENTS_MANAGER",
    },
    {
      text: "Développement logiciel, analyse de données ou autre rôle technique",
      value: "TECHNICAL",
    },
    {
      text: "Autre (spécifiez)",
      value: "OTHER",
    },
  ],
  UserSources: [
    {
      text: "Webinaire",
      value: "WEBINAIRE",
    },
    {
      text: "Recherche web",
      value: "WEB_SEARCH",
    },
    {
      text: "Communication institutionnelle (DRAAF, association régionale)",
      value: "INSTITUTION",
    },
    {
      text: "Bouche à oreille",
      value: "WORD_OF_MOUTH",
    },
    {
      text: "Réseaux sociaux",
      value: "SOCIAL_MEDIA",
    },
    {
      text: "Autre (spécifiez)",
      value: "OTHER",
    },
  ],
  DiagnosticImportLevels: [
    {
      key: "SIMPLE",
      urlSlug: "cantines-et-diagnostics-simples",
      title: "Importer des cantines et bilans simples",
      label: "Diagnostic simple",
      help: "Vous connaissez les valeurs totales de vos achats bio et de qualité",
      icon: "$bar-chart-box-fill",
    },
    {
      key: "COMPLETE",
      urlSlug: "cantines-et-diagnostics-complets",
      title: "Importer des cantines et bilans complets",
      label: "Diagnostic complet",
      help: "Vous connaissez les labels et les familles de produits de vos achats",
      icon: "$checkbox-circle-fill",
    },
  ],
  CentralKitchenImportLevels: [
    {
      key: "CC_SIMPLE",
      urlSlug: "cuisine-centrale-diagnostics-simples",
      title: "Importer des bilans simples centralisés",
      description:
        "Ce type de fichier vous permet de renseigner vos données d'approvisionnement simplifiées au niveau de la cuisine centrale et de lister vos restaurants satellites seulement avec leurs données d'établissement. Les données d'approvisionnement sont donc rentrées une fois au niveau du livreur.",
      label: "Livreur avec bilan simple",
      help:
        "Vous voulez renseigner vos restaurants satellites et vous connaissez les valeurs totaux, bio, et de qualité et durable",
      icon: "$bar-chart-box-fill",
    },
    {
      key: "CC_COMPLETE",
      urlSlug: "cuisine-centrale-diagnostics-complets",
      title: "Importer des bilans complets centralisés",
      description:
        "Ce type de fichier vous permet de renseigner vos données d'approvisionnement détaillées au niveau de la cuisine centrale et de lister vos restaurants satellites seulement avec leurs données d'établissement. Les données d'approvisionnement sont donc rentrées une fois au niveau du livreur.",
      label: "Livreur avec bilan complet",
      help:
        "Vous voulez renseigner vos restaurants satellites et vous connaissez les labels et les familles de produits de vos achats",
      icon: "$checkbox-circle-fill",
    },
  ],
  MiscLabelIcons: {
    FERMIER: {
      icon: "mdi-cow",
      color: "brown",
    },
    EXTERNALITES: {
      icon: "mdi-flower-tulip-outline",
      color: "purple",
    },
    PERFORMANCE: {
      icon: "mdi-chart-line",
      color: "green",
    },
    NON_EGALIM: {
      icon: "mdi-dots-horizontal",
      color: "grey",
    },
    FRANCE: {
      icon: "$france-line",
      color: "indigo",
    },
    SHORT_DISTRIBUTION: {
      icon: "mdi-chart-timeline-variant",
      color: "pink",
    },
    LOCAL: {
      icon: "mdi-map-marker-outline",
      color: "blue",
    },
  },
  CentralKitchenDiagnosticModes: [
    {
      key: "ALL",
      label: "Je rentre les données concernant toutes les mesures EGalim pour mes restaurants satellites",
      shortLabel: "Les données sur l’ensemble des mesures EGalim",
    },
    {
      key: "APPRO",
      label: "Je rentre seulement les données d'approvisionnement pour mes restaurants satellites",
      shortLabel: "Les données d’approvisionnement seulement",
    },
  ],
  SectorCategoryTranslations: {
    education: "Enseignement",
    health: "Santé",
    autres: "Autre",
    social: "Social et Médico-Social",
    administration: "Administration",
    leisure: "Loisirs",
    enterprise: "Entreprise",
    inconnu: "Inconnu",
  },
  Levels: {
    UNKNOWN: {
      text: "INCONNU",
      colorClass: "grey--text text--darken-2",
    },
    BEGINNER: {
      text: "NOVICE",
      colorClass: "grey--text text--darken-2",
    },
    ADVANCED: {
      text: "AVANCÉ",
      colorClass: "blue--text text--darken-3",
    },
    EXPERT: {
      text: "EXPERT",
      colorClass: "green--text text--darken-4",
    },
  },
  WasteActions: [
    {
      label: "Pré-inscription des convives obligatoire",
      value: "INSCRIPTION",
    },
    {
      label: "Sensibilisation par affichage ou autre média",
      value: "AWARENESS",
    },
    {
      label: "Formation / information du personnel de restauration",
      value: "TRAINING",
    },
    {
      label: "Réorganisation de la distribution des composantes du repas",
      value: "DISTRIBUTION",
    },
    {
      label: "Choix des portions (grande faim, petite faim)",
      value: "PORTIONS",
    },
    {
      label: "Réutilisation des restes de préparation / surplus",
      value: "REUSE",
    },
  ],
  DiversificationMeasureStep: {
    hasDiversificationPlan: {
      title:
        "J'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de protéines végétales",
      false:
        "Je n'ai pas mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de protéines végétales",
      empty:
        "Avez-vous mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de protéines végétales ?",
    },
    diversificationPlanActions: {
      title: "Ce plan comporte, par exemple, les actions suivantes (voir guide du CNRC) :",
      items: [
        {
          label:
            "Agir sur les plats et les produits (diversification, gestion des quantités, recette traditionnelle, gout...)",
          value: "PRODUCTS",
        },
        {
          label: "Agir sur la manière dont les aliments sont présentés aux convives (visuellement attrayants)",
          value: "PRESENTATION",
        },
        {
          label: "Agir sur la manière dont les menus sont conçus en soulignant attributs positifs des plats",
          value: "MENU",
        },
        {
          label: "Agir sur la mise en avant des produits (plats recommandés, dégustation, mode de production...)",
          value: "PROMOTION",
        },
        {
          label:
            "Agir sur la formation du personnel, la sensibilisation des convives, l’investissement dans de nouveaux équipements de cuisine...",
          value: "TRAINING",
        },
      ],
      empty: "Aucune action du plan renseignée",
    },
    serviceType: {
      title: "Le service est en :",
      items: [
        {
          label: "Menu unique",
          value: "UNIQUE",
        },
        {
          label: "Choix multiple en libre-service",
          value: "MULTIPLE_SELF",
        },
        {
          label: "Choix multiple avec réservation à l’avance au jour le jour",
          value: "MULTIPLE_RESERVATION",
        },
      ],
      empty: "Je n'ai pas renseigné le type de service",
    },
    vegetarianWeeklyRecurrence: {
      title: "J'ai mis en place un menu végétarien :",
      items: [
        {
          label: "De façon quotidienne",
          value: "DAILY",
        },
        {
          label: "Plus d'une fois par semaine",
          value: "HIGH",
        },
        {
          label: "Une fois par semaine",
          value: "MID",
        },
        {
          label: "Moins d'une fois par semaine",
          value: "LOW",
        },
        {
          label: "Je ne propose pas de menu végétarien",
          value: "NEVER",
        },
      ],
      empty: "Je n'ai pas renseigné la périodicité du menu végétarien",
    },
    vegetarianMenuType: {
      title: "Le menu végétarien proposé est :",
      items: [
        {
          label: "Un menu végétarien en plat unique, sans choix",
          value: "UNIQUE",
        },
        {
          label: "Un menu végétarien composé de plusieurs choix de plats végétariens",
          value: "SEVERAL",
        },
        {
          label: "Un menu végétarien au choix, en plus d'autres plats non végétariens",
          value: "ALTERNATIVES",
        },
      ],
      empty: "Je n'ai pas renseigné le type de menu végétarien servi",
    },
    vegetarianMenuBases: {
      title: "Le plat principal de mon menu végétarien est majoritairement à base de :",
      items: [
        {
          label: "De céréales et/ou les légumes secs (hors soja)",
          value: "GRAIN",
        },
        {
          label: "De soja",
          value: "SOY",
        },
        {
          label: "De fromage",
          value: "CHEESE",
        },
        {
          label: "D’œufs",
          value: "EGG",
        },
        {
          label: "De plats transformés prêts à l'emploi",
          value: "READYMADE",
        },
      ],
      empty: "Je n'ai pas renseigné les bases utilisées pour mon menu végétarien",
    },
  },
  CommunicationFrequencies: [
    {
      label: "Régulièrement au cours de l’année",
      value: "REGULARLY",
    },
    {
      label: "Une fois par an",
      value: "YEARLY",
    },
    {
      label: "Moins d'une fois par an",
      value: "LESS_THAN_YEARLY",
    },
  ],
  CommunicationSupports: [
    {
      label: "Par affichage sur le lieu de restauration",
      value: "DISPLAY",
    },
    {
      label: "Par voie électronique (envoi d’e-mail aux convives, sur site internet ou intranet (mairie, pronote))",
      value: "DIGITAL",
    },
  ],
  DiagnosticTypes: [
    {
      key: "SIMPLE",
      label: "Télédéclaration - saisie simplifiée",
      help: "Vous connaissez les valeurs totales de vos achats bio et de qualité",
    },
    {
      key: "COMPLETE",
      label: "Télédéclaration - saisie détaillée",
      help: "Vous connaissez les labels et les familles de produits de vos achats",
    },
  ],
  WasteActionEffortLevels: [
    {
      value: "SMALL",
      text: "Petit pas",
      description: "Investissement financier et humain modéré, mais impact limité.",
      icon: "$progress-2-line",
    },
    {
      value: "MEDIUM",
      text: "Moyen",
      description: "Investissement financier et humain relativement important, impact moyen.",
      icon: "$progress-4-line",
    },
    {
      value: "LARGE",
      text: "Grand projet",
      description: "Investissement financier et humain important, impact fort.",
      icon: "$progress-6-line",
    },
  ],
  WasteActionOrigins: [
    {
      value: "PREP",
      text: "Préparation",
      icon: "$slice-line",
    },
    {
      value: "UNSERVED",
      text: "Non servi",
      icon: "$bowl-line",
    },
    {
      value: "PLATE",
      text: "Retour assiette",
      icon: "$restaurant-line",
    },
  ],
})
