import { createRouter, createWebHistory } from "vue-router"
import WasteMeasurementTunnel from "@/views/WasteMeasurementTunnel"
import ImportSelection from "@/views/ImportSelection"
import WasteMeasurements from "@/views/WasteMeasurements"
import { useRootStore } from "@/stores/root"

const routes = [
  {
    path: "/evaluation-gaspillage-alimentaire/:canteenUrlComponent/:id?",
    name: "WasteMeasurementTunnel",
    component: WasteMeasurementTunnel,
    props: (route) => ({ ...route.query, ...route.params }),
    meta: {
      title: "Évaluation gaspillage alimentaire",
      authenticationRequired: true,
      fullscreen: true,
    },
  },
  {
    path: "/importer-des-donnees",
    name: "ImportSelection",
    component: ImportSelection,
    meta: {
      title: "Importer des données",
      authenticationRequired: true,
    },
  },
  {
    path: "/gaspillage-alimentaire/:canteenUrlComponent",
    name: "WasteMeasurements",
    component: WasteMeasurements,
    props: (route) => ({ ...route.params }),
    meta: {
      title: "Gaspillage alimentaire",
      authenticationRequired: true,
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "DashboardManager" }, useCanteenName: true },
      ],
    },
  },
]

const VUE3_PREFIX = "/v2"
routes.forEach((r) => {
  r.path = VUE3_PREFIX + r.path
})

const vue2Routes = [
  {
    path: "/",
    name: "Vue2Home",
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
    path: "/developpement-et-apis",
    name: "DeveloperPage",
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
    path: "/faq/",
    name: "FaqPage",
  },
  {
    path: "/contact",
    name: "ContactPage",
  },
  {
    path: "/mon-compte",
    name: "AccountSummaryPage",
  },
  {
    path: "/accessibilite",
    name: "AccessibilityDeclaration",
  },
  {
    path: "/plan-du-site/",
    name: "SiteMap",
  },
  {
    path: "/politique-de-confidentialite",
    name: "PrivacyPolicy",
  },
  {
    path: "/politique-de-confidentialite#cookies",
    name: "Cookies",
  },
  {
    path: "/actions-anti-gaspi",
    name: "WasteActionsHome",
  },
  {
    path: "/nouvelle-cantine",
    name: "NewCanteen",
  },
  {
    path: "/importer-diagnostics/:importUrlSlug",
    name: "DiagnosticImportPage",
  },
  {
    path: "/importer-achats",
    name: "PurchasesImporter",
  },
]
routes.push(...vue2Routes)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  if (!to.path.startsWith(VUE3_PREFIX)) {
    location.href = location.origin + to.path
    return false
  }
  if (!to.meta.authenticationRequired) return
  const store = useRootStore()
  if (!store.initialDataLoaded) {
    await store.fetchInitialData()
  }
  if (!store.loggedUser) {
    return { name: "Vue2Home", replace: true }
  }
})

export { router, routes }
