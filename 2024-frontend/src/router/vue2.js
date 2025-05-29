const vue2routes = [
  {
    path: "/",
    name: "Vue2Home",
  },
  {
    path: "/accueil",
    name: "LandingPage",
  },
  {
    path: "/ma-progression/:canteenUrlComponent/:year/:measureId",
    name: "MyProgress",
  },
  {
    path: "/dashboard/:canteenUrlComponent",
    name: "DashboardManager",
  },
  {
    path: "/gestion",
    name: "ManagementPage",
  },
  {
    path: "/mes-achats",
    name: "PurchasesHome",
  },
  {
    path: "/diagnostic",
    name: "DiagnosticPage",
  },
  {
    path: "/nos-cantines",
    name: "CanteensHome",
  },
  {
    path: "/mesures-phares/:id",
    name: "KeyMeasurePage",
  },
  {
    path: "/acteurs-de-l-eco-systeme",
    name: "PartnersHome",
  },
  {
    path: "/creation-affiche",
    name: "GeneratePosterPage",
  },
  {
    path: "/communaute",
    name: "CommunityPage",
  },
  {
    path: "/blog",
    name: "BlogsHome",
  },
  {
    path: "/les-cantines-de-mon-territoire",
    name: "TerritoryCanteens",
  },
  {
    path: "/trouver-une-cantine",
    name: "CanteenSearchLanding",
  },
  {
    path: "/statistiques-regionales",
    name: "PublicCanteenStatisticsPage",
  },
  {
    path: "/mon-compte",
    name: "AccountSummaryPage",
  },
  {
    path: "/plan-du-site/",
    name: "SiteMap",
  },
  {
    path: "/actions-anti-gaspi",
    name: "WasteActionsHome",
  },
  {
    path: "/importer-diagnostics/:importUrlSlug",
    name: "DiagnosticImportPage",
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent/supprimer",
    name: "CanteenDeletion",
  },
]

export default vue2routes
