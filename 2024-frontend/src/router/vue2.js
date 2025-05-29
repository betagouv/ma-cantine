import { sectionId } from "@/constants/site-map.js"
const { law, diag } = sectionId

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
    meta: {
      title: "Mes achats",
      siteMap: diag,
    },
  },
  {
    path: "/nouvel-achat/",
    name: "NewPurchase",
    meta: {
      title: "Nouvel achat",
      siteMap: diag,
    },
  },
  {
    path: "/synthese-achats",
    name: "PurchasesSummary",
    meta: {
      title: "Synthèse des achats",
      siteMap: diag,
    },
  },
  {
    path: "/diagnostic",
    name: "DiagnosticPage",
    meta: {
      title: "M'auto-évaluer",
      siteMap: diag,
    },
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
    meta: {
      title: "Webinaires",
      siteMap: law,
    },
  },
  {
    path: "/blog",
    name: "BlogsHome",
    meta: {
      title: "Blog",
      siteMap: law,
    },
  },
  {
    path: "/les-cantines-de-mon-territoire",
    name: "TerritoryCanteens",
    meta: {
      title: "Les cantines de mon territoire",
      siteMap: diag,
    },
  },
  {
    path: "/trouver-une-cantine",
    name: "CanteenSearchLanding",
  },
  {
    path: "/statistiques-regionales",
    name: "PublicCanteenStatisticsPage",
    meta: {
      title: "Sur mon territoire",
      siteMap: law,
    },
  },
  {
    path: "/mon-compte",
    name: "AccountSummaryPage",
  },
  {
    path: "/donnees-personnelles#cookies",
    name: "Cookies",
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
