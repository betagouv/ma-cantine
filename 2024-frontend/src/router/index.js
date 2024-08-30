import { createRouter, createWebHistory } from "vue-router"
import DiagnosticTunnel from "@/views/DiagnosticTunnel"
import ImportSelection from "@/views/ImportSelection"
import WasteMeasurements from "@/views/WasteMeasurements"
import { useRootStore } from "@/stores/root"

const routes = [
  {
    path: "/diagnostic-tunnel/:canteenUrlComponent/:year/:measureId",
    name: "DiagnosticTunnel",
    component: DiagnosticTunnel,
    props: (route) => ({ ...route.query, ...route.params }),
    meta: {
      title: "Bilan",
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
]
routes.push(...vue2Routes)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (!to.path.startsWith(VUE3_PREFIX)) {
    location.href = location.origin + to.path
    return
  }
  const store = useRootStore()
  if (!store.initialDataLoaded) {
    store.fetchInitialData().then(() => {
      if (!store.loggedUser && to.meta.authenticationRequired) {
        next({ name: "Vue2Home", replace: true })
      } else {
        next()
      }
    })
  }
})

export { router, routes }
