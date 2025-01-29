import { createRouter, createWebHistory } from "vue-router"
import WasteMeasurementTunnel from "@/views/WasteMeasurementTunnel"
import ImportSelection from "@/views/ImportSelection"
import WasteMeasurements from "@/views/WasteMeasurements"
import LegalNotices from "@/views/LegalNotices"
import AccessibilityDeclaration from "@/views/AccessibilityDeclaration"
import CGU from "@/views/CGU"
import ContactPage from "@/views/ContactPage"
import ImportPurchases from "@/views/ImportPurchases"
import ImportCanteens from "@/views/ImportCanteens"
import { useRootStore } from "@/stores/root"

const routes = [
  {
    path: "/evaluation-gaspillage-alimentaire/:canteenUrlComponent/:id?",
    name: "WasteMeasurementTunnel",
    component: WasteMeasurementTunnel,
    props: (route) => ({ ...route.query, ...route.params }),
    meta: {
      title: "Évaluation déchets alimentaires",
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
      title: "Déchets alimentaires",
      authenticationRequired: true,
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "DashboardManager" }, useCanteenName: true },
      ],
    },
  },
  {
    path: "/mentions-legales",
    name: "LegalNotices",
    component: LegalNotices,
    meta: {
      title: "Mentions légales",
    },
  },
  {
    path: "/accessibilite",
    name: "AccessibilityDeclaration",
    component: AccessibilityDeclaration,
    meta: {
      title: "Déclaration d'accessibilité",
    },
  },
  {
    path: "/cgu",
    name: "CGU",
    component: CGU,
    meta: {
      title: "Conditions générales d'utilisation",
    },
  },
  {
    path: "/contact",
    name: "ContactPage",
    component: ContactPage,
    meta: {
      title: "Contactez-nous",
    },
  },
  {
    path: "/importer-des-donnees/achats",
    name: "ImportPurchases",
    component: ImportPurchases,
    meta: {
      title: "Importer des achats",
      authenticationRequired: true,
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "ImportSelection" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "/importer-des-donnees/cantines",
    name: "ImportCanteens",
    component: ImportCanteens,
    meta: {
      title: "Importer des cantines",
      authenticationRequired: true,
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "ImportSelection" }, title: "Importer des données" },
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
    path: "/faq/",
    name: "FaqPage",
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
]
routes.push(...vue2Routes)

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    const scrollTo = to.hash || "#app"
    return { el: scrollTo }
  },
})

router.beforeEach(async (to) => {
  if (!to.path.startsWith(VUE3_PREFIX)) {
    location.href = location.origin + to.fullPath
    return false
  }
  const store = useRootStore()
  if (!store.initialDataLoaded) {
    await store.fetchInitialData()
  }
  if (!store.loggedUser && to.meta.authenticationRequired) {
    return { name: "Vue2Home", replace: true }
  }
})

export { router, routes }
