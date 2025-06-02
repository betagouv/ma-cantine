import { sectionId } from "@/constants/site-map.js"
const { law, diag, action } = sectionId

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
      authenticationRequired: true,
    },
  },
  {
    path: "/nouvel-achat/",
    name: "NewPurchase",
    meta: {
      title: "Nouvel achat",
      siteMap: diag,
      authenticationRequired: true,
    },
  },
  {
    path: "/synthese-achats",
    name: "PurchasesSummary",
    meta: {
      title: "Synthèse des achats",
      siteMap: diag,
      authenticationRequired: true,
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
    meta: {
      title: "Acteurs de l'éco-système",
      siteMap: action,
    },
  },
  {
    path: "/nouveau-acteur-de-l-ecosysteme",
    name: "NewPartner",
    meta: {
      title: "Nouvel acteur de l'éco-système",
      siteMap: action,
    },
  },
  {
    path: "/creation-affiche",
    name: "GeneratePosterPage",
    meta: {
      title: "Affiche convives",
      siteMap: action,
    },
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
      authenticationRequired: true,
    },
  },
  {
    path: "/trouver-une-cantine",
    name: "CanteenSearchLanding",
    meta: {
      title: "Trouver une cantine",
      siteMap: action,
    },
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
    path: "/actions-anti-gaspi",
    name: "WasteActionsHome",
    meta: {
      title: "Actions anti-gaspi",
      siteMap: action,
    },
  },
  {
    path: "/importer-diagnostics/:importUrlSlug",
    name: "DiagnosticImportPage",
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent/supprimer",
    name: "CanteenDeletion",
  },
  {
    path: "/actions-en-attente",
    name: "PendingActions",
    meta: {
      title: "Actions en attente",
      siteMap: diag,
      authenticationRequired: true,
    },
  },
]

export default vue2routes
