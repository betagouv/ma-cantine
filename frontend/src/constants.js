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
  Categories: {
    VIANDES_VOLAILLES: { text: "Viandes, volailles", color: "red darken-4" },
    PRODUITS_DE_LA_MER: { text: "Produits de la mer", color: "pink darken-4" },
    FRUITS_ET_LEGUMES: {
      text: "Fruits, légumes, légumineuses et oléagineux",
      color: "purple darken-4",
    },
    PRODUITS_CEREALIERS: { text: "Produits céréaliers", color: "deep-purple darken-4" },
    ENTREES: { text: "Entrées et plats composés", color: "indigo darken-4" },
    PRODUITS_LAITIERS: { text: "Lait et produits laitiers", color: "blue darken-4" },
    BOISSONS: { text: "Boissons", color: "light-blue darken-4" },
    AIDES: { text: "Aides culinaires et ingrédients divers", color: "cyan darken-4" },
    BEURRE_OEUF_FROMAGE: { text: "Beurre, oeuf, fromage", color: "teal darken-4" },
    PRODUITS_SUCRES: { text: "Produits sucrés", color: "green darken-4" },
    ALIMENTS_INFANTILES: { text: "Aliments infantiles", color: "light-green darken-4" },
    GLACES_SORBETS: { text: "Glaces et sorbets", color: "blue-grey darken-4" },
    AUTRES: { text: "Autres", color: "brown darken-4" },
  },
  Characteristics: {
    // NB: the order of these can affect the aesthetics of the display on PurchasePage, esp for long texts
    BIO: { text: "Bio" },
    CONVERSION_BIO: { text: "En conversion bio" },
    LABEL_ROUGE: { text: "Label rouge" },
    AOCAOP: { text: "AOC / AOP", longText: "Appellation d'origine (AOC / AOP)" },
    ICP: { text: "IGP", longText: "Indication géographique protégée (IGP)" },
    STG: { text: "STG", longText: "Spécialité traditionnelle garantie (STG)" },
    PECHE_DURABLE: { text: "Pêche durable" },
    RUP: { text: "RUP", longText: "Région ultrapériphérique (RUP)" },
    COMMERCE_EQUITABLE: { text: "Commerce équitable" },
    HVE: { text: "HVE", longText: "HVE ou certification environnementale de niveau 2" },
    FERMIER: { text: "Fermier", longText: "Mention « fermier » ou « produit de la ferme » ou « produit à la ferme »" },
    EQUIVALENTS: {
      text: "Produits équivalents",
      longText: "Produits équivalents aux produits bénéficiant de ces mentions ou labels",
    },
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
  LocalDefinitions: {
    AUTOUR_SERVICE: { text: "200 km autour du lieu de service", value: "AUTOUR_SERVICE" },
    DEPARTMENT: { text: "Provenant du même département", value: "DEPARTMENT" },
    REGION: { text: "Provenant de la même région", value: "REGION" },
    AUTRE: { text: "Autre", value: "AUTRE" },
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
})
