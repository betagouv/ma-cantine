import Vue from "vue"
import VueRouter from "vue-router"
import store from "@/store/index"
import LandingPage from "@/views/LandingPage"
import ManagerLanding from "@/views/ManagerLanding"
import DiagnosticPage from "@/views/DiagnosticPage"
import KeyMeasuresPage from "@/views/KeyMeasuresPage"
import KeyMeasuresHome from "@/views/KeyMeasuresPage/KeyMeasuresHome"
import GeneratePosterPage from "@/views/GeneratePosterPage"
import CanteensPage from "@/views/CanteensPage"
import CanteenWidget from "@/views/CanteensPage/CanteenWidget"
import CanteenSearchLanding from "@/views/CanteenSearchLanding"
import CanteensHome from "@/views/CanteensPage/CanteensHome"
import CanteenPage from "@/views/CanteensPage/CanteenPage"
import AccountSummaryPage from "@/views/AccountSummaryPage"
import AccountEditor from "@/views/AccountSummaryPage/AccountEditor"
import PasswordChangeEditor from "@/views/AccountSummaryPage/PasswordChangeEditor"
import AccountDeletion from "@/views/AccountSummaryPage/AccountDeletion"
import BlogsPage from "@/views/BlogsPage"
import BlogsHome from "@/views/BlogsPage/BlogsHome"
import BlogPage from "@/views/BlogsPage/BlogPage"
import WasteActionsPage from "@/views/WasteActionsPage"
import WasteActionsHome from "@/views/WasteActionsPage/WasteActionsHome.vue"
import WasteActionPage from "@/views/WasteActionsPage/WasteActionPage.vue"
import PartnersPage from "@/views/PartnersPage"
import PartnersHome from "@/views/PartnersPage/PartnersHome"
import PartnerPage from "@/views/PartnersPage/PartnerPage"
import NewPartner from "@/views/NewPartner"
import NotFound from "@/views/NotFound"
import ManagementPage from "@/views/ManagementPage"
import PendingActions from "@/views/PendingActions"
import CanteenEditor from "@/views/CanteenEditor"
import SatelliteManagement from "@/views/CanteenEditor/SatelliteManagement"
import CanteenManagers from "@/views/CanteenEditor/CanteenManagers"
import CanteenGeneratePoster from "@/views/CanteenEditor/CanteenGeneratePoster"
import CanteenDeletion from "@/views/CanteenEditor/CanteenDeletion"
import PublicationForm from "@/views/CanteenEditor/PublicationForm"
import DiagnosticTunnel from "@/views/DiagnosticTunnel"
import DiagnosticImportPage from "@/views/DiagnosticsImporter/DiagnosticImportPage"
import PublicCanteenStatisticsPage from "@/views/PublicCanteenStatisticsPage"
import PurchasesHome from "@/views/PurchasesHome"
import PurchasePage from "@/views/PurchasePage"
import PurchasesSummary from "@/views/PurchasesSummary"
import CommunityPage from "@/views/CommunityPage"
import DashboardManager from "@/views/DashboardManager"
import TerritoryCanteens from "@/views/TerritoryCanteens"
import VideoTutorial from "@/views/VideoTutorial"
import MyProgress from "@/views/MyProgress"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    meta: {
      home: true,
    },
  },
  {
    path: "/accueil",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/accueil-gestionnaire",
    name: "ManagerLanding",
    component: ManagerLanding,
    beforeEnter: (_to, _from, next) => {
      store.state.loggedUser ? next({ name: "ManagementPage" }) : next()
    },
  },
  {
    path: "/mon-compte",
    name: "AccountSummaryPage",
    component: AccountSummaryPage,
    redirect: { name: "AccountEditor" },
    children: [
      {
        path: "profil",
        name: "AccountEditor",
        component: AccountEditor,
        meta: {
          authenticationRequired: true,
          title: "Mon compte",
        },
      },
      {
        path: "mot-de-passe",
        name: "PasswordChange",
        component: PasswordChangeEditor,
        meta: {
          authenticationRequired: true,
          title: "Changer mon mot de passe",
        },
      },
      {
        path: "supprimer-mon-compte",
        name: "AccountDeletion",
        component: AccountDeletion,
        meta: {
          authenticationRequired: true,
          title: "Supprimer mon compte",
        },
      },
    ],
  },
  {
    path: "/diagnostic",
    name: "DiagnosticPage",
    component: DiagnosticPage,
    meta: {
      title: "M'auto-évaluer",
    },
    beforeEnter: (_to, _from, next) => {
      store.state.loggedUser ? next({ name: "ManagementPage" }) : next()
    },
  },
  {
    path: "/creation-affiche",
    name: "GeneratePosterPage",
    component: GeneratePosterPage,
    meta: {
      title: "Affiche convives",
    },
  },
  {
    path: "/mesures-phares",
    name: "KeyMeasuresPage",
    component: KeyMeasuresPage,
    redirect: { name: "KeyMeasuresHome" },
    children: [
      {
        path: "",
        name: "KeyMeasuresHome",
        component: KeyMeasuresHome,
        meta: {
          title: "Tableau de bord",
        },
        beforeEnter: (route, _, next) => {
          store.state.loggedUser
            ? next({
                name: "UnderstandingLaw",
              })
            : next()
        },
      },
    ],
    meta: {
      title: "Les mesures phares",
    },
  },
  {
    path: "/trouver-une-cantine",
    name: "CanteenSearchLanding",
    component: CanteenSearchLanding,
    meta: {
      title: "Trouver une cantine",
    },
  },
  {
    // if you change this path, update the visitor view count logic in the publication widget
    path: "/nos-cantines",
    component: CanteensPage,
    children: [
      {
        path: "",
        name: "CanteensHome",
        component: CanteensHome,
        meta: {
          title: "Les cantines",
        },
      },
      {
        path: ":canteenUrlComponent",
        name: "CanteenPage",
        component: CanteenPage,
        props: true,
      },
    ],
  },
  {
    path: "/widgets/nos-cantines/:canteenUrlComponent",
    name: "CanteenWidget",
    component: CanteenWidget,
    props: true,
  },
  {
    path: "/blog",
    component: BlogsPage,
    children: [
      {
        path: "",
        name: "BlogsHome",
        component: BlogsHome,
        meta: {
          title: "Blog",
        },
      },
      {
        path: ":id",
        name: "BlogPage",
        component: BlogPage,
        props: true,
      },
    ],
  },
  {
    path: "/actions-anti-gaspi",
    component: WasteActionsPage,
    children: [
      {
        path: "",
        name: "WasteActionsHome",
        component: WasteActionsHome,
        meta: {
          title: "Actions anti-gaspi",
        },
      },
      {
        path: ":id",
        name: "WasteActionPage",
        component: WasteActionPage,
        props: true,
      },
    ],
  },
  {
    path: "/partenaires",
    redirect: "/acteurs-de-l-eco-systeme",
  },
  {
    path: "/acteurs-de-l-eco-systeme",
    component: PartnersPage,
    children: [
      {
        path: "",
        name: "PartnersHome",
        component: PartnersHome,
        meta: {
          title: "Acteurs de l'éco-système",
        },
      },
      {
        path: ":partnerUrlComponent",
        name: "PartnerPage",
        component: PartnerPage,
        props: true,
      },
    ],
  },
  {
    path: "/nouveau-acteur-de-l-ecosysteme",
    name: "NewPartner",
    component: NewPartner,
    meta: {
      title: "Nouvel acteur de l'éco-système",
    },
  },
  {
    path: "/gestion",
    name: "ManagementPage",
    component: ManagementPage,
    meta: {
      title: "Mon tableau de bord",
      authenticationRequired: true,
    },
  },
  {
    path: "/actions-en-attente",
    name: "PendingActions",
    component: PendingActions,
    meta: {
      title: "Actions en attente",
      authenticationRequired: true,
    },
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent",
    name: "GestionnaireCantineModifier",
    props: true,
    component: CanteenEditor,
    redirect: { name: "CanteenForm" },
    children: [
      {
        path: "satellites",
        name: "SatelliteManagement",
        component: SatelliteManagement,
        meta: {
          authenticationRequired: true,
          title: "Gérer mes satellites",
        },
      },
      {
        path: "gestionnaires",
        name: "CanteenManagers",
        component: CanteenManagers,
        meta: {
          authenticationRequired: true,
          title: "Gérer mon équipe",
        },
      },
      {
        path: "generer-mon-affiche",
        name: "CanteenGeneratePoster",
        component: CanteenGeneratePoster,
        meta: {
          authenticationRequired: true,
          title: "Générer mon affiche",
        },
      },
      {
        path: "supprimer",
        name: "CanteenDeletion",
        component: CanteenDeletion,
        meta: {
          authenticationRequired: true,
          title: "Supprimer ma cantine",
        },
      },
      {
        path: "publier",
        name: "PublicationForm",
        component: PublicationForm,
        meta: {
          authenticationRequired: true,
          title: "Éditer mon affiche",
        },
      },
    ],
  },
  {
    path: "/diagnostic-tunnel/:canteenUrlComponent/:year/:measureId",
    name: "DiagnosticTunnel",
    component: DiagnosticTunnel,
    props: true,
    meta: {
      title: "Bilan",
      authenticationRequired: true,
      fullscreen: true,
    },
  },
  {
    path: "/importer-diagnostics/:importUrlSlug",
    name: "DiagnosticImportPage",
    component: DiagnosticImportPage,
    props: true,
    beforeEnter: (to, _from, next) => {
      if (to.params.importUrlSlug === "cantines-seules") next({ name: "GestionnaireImportCantines" })
      else next()
    },
  },
  {
    path: "/statistiques-regionales",
    name: "PublicCanteenStatisticsPage",
    component: PublicCanteenStatisticsPage,
    meta: {
      title: "Sur mon territoire",
    },
  },
  {
    path: "/mes-achats",
    name: "PurchasesHome",
    component: PurchasesHome,
    meta: {
      title: "Mes achats",
      authenticationRequired: true,
    },
  },
  {
    path: "/mes-achats/:id",
    name: "PurchasePage",
    component: PurchasePage,
    props: true,
    meta: {
      title: "Modifier mon achat",
      authenticationRequired: true,
    },
  },
  {
    path: "/nouvel-achat/",
    name: "NewPurchase",
    component: PurchasePage,
    meta: {
      title: "Nouvel achat",
      authenticationRequired: true,
    },
  },
  {
    path: "/synthese-achats",
    name: "PurchasesSummary",
    component: PurchasesSummary,
    meta: {
      title: "Synthèse des achats",
      authenticationRequired: true,
    },
  },
  {
    path: "/communaute/",
    name: "CommunityPage",
    component: CommunityPage,
    meta: {
      title: "Webinaires",
    },
  },
  {
    path: "/webinaires/:webinaireUrlComponent",
    name: "VideoTutorial",
    component: VideoTutorial,
    props: true,
  },
  {
    path: "/les-cantines-de-mon-territoire",
    name: "TerritoryCanteens",
    component: TerritoryCanteens,
    meta: {
      title: "Les cantines de mon territoire",
      authenticationRequired: true,
    },
    beforeEnter: (_to, _from, next) => {
      store.state.loggedUser?.isElectedOfficial ? next() : next({ name: "ManagementPage" })
    },
  },
]

if (window.ENABLE_DASHBOARD) {
  routes.push({
    path: "/dashboard/:canteenUrlComponent",
    name: "DashboardManager",
    component: DashboardManager,
    props: true,
    meta: {
      title: "Tableau de bord",
      authenticationRequired: true,
    },
  })
  routes.push({
    path: "/ma-progression/:canteenUrlComponent/:year/:measure",
    name: "MyProgress",
    component: MyProgress,
    props: true,
    meta: {
      title: "Mon bilan annuel",
      authenticationRequired: true,
    },
  })
}

const vue3Routes = [
  {
    path: "/gaspillage-alimentaire/:canteenUrlComponent",
    name: "GestionnaireGaspillageAlimentaire",
  },
  {
    path: "/evaluation-gaspillage-alimentaire/:canteenUrlComponent/:id?",
    name: "GestionnaireGaspillageAlimentaireModifier",
  },
  {
    path: "/importer-des-donnees",
    name: "GestionnaireImport",
    meta: {
      title: "Importer des données",
    },
  },
  {
    path: "/developpement-et-apis",
    name: "Developpeurs",
  },
  {
    path: "/mentions-legales",
    name: "MentionsLegales",
  },
  {
    path: "/accessibilite",
    name: "Accessibilite",
  },
  {
    path: "/cgu",
    name: "ConditionsGeneralesUtilisation",
  },
  {
    path: "/contact",
    name: "Contact",
  },
  {
    path: "/importer-des-donnees/achats",
    name: "GestionnaireImportAchats",
  },
  {
    path: "/importer-des-donnees/cantines",
    name: "GestionnaireImportCantines",
  },
  {
    path: "/ajouter-une-cantine",
    name: "GestionnaireCantineAjouter",
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent/etablissement",
    name: "CanteenForm",
  },
  {
    path: "/foire-aux-questions/",
    name: "FoireAuxQuestions",
  },
  {
    path: "/donnees-personnelles",
    name: "DonneesPersonnelles",
  },
  {
    path: "/plan-du-site/",
    name: "PlanDuSite",
  },
  {
    path: "/comprendre-mes-obligations",
    name: "UnderstandingLaw",
  },
]
const VUE3_PREFIX = "/v2"
vue3Routes.forEach((r) => {
  r.path = VUE3_PREFIX + r.path
})
routes.push(...vue3Routes)

routes.push({
  path: "/importer-achats",
  redirect: { name: "GestionnaireImportAchats" },
})

routes.push({
  path: "/nouvelle-cantine",
  redirect: { name: "GestionnaireCantineAjouter" },
})

routes.push({
  path: "/politique-de-confidentialite",
  redirect: { name: "DonneesPersonnelles" },
})

routes.push({
  path: "/:catchAll(.*)",
  component: NotFound,
  name: "NotFound",
})

const router = new VueRouter({
  mode: "history",
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) return { selector: to.hash, offset: { y: 200 } }
    if (to.name === from.name && this.app.$vuetify.breakpoint.mdAndUp) return savedPosition
    return { x: 0, y: 0 }
  },
})

function chooseAuthorisedRoute(to, from, next) {
  if (!store.state.initialDataLoaded) {
    store
      .dispatch("fetchInitialData")
      .then(() => chooseAuthorisedRoute(to, from, next))
      .catch((e) => {
        console.error(`An error occurred: ${e}`)
        next({ name: "LandingPage" })
      })
  } else {
    if (to.meta.home && store.state.loggedUser && !store.state.loggedUser.isDev) next({ name: "ManagementPage" })
    else if (to.meta.home && store.state.loggedUser && store.state.loggedUser.isDev) next({ name: "Developpeurs" })
    else if (to.meta.home) next({ name: "LandingPage" })
    else if (!to.meta.authenticationRequired || store.state.loggedUser) next()
    else window.location.href = `/s-identifier?next=${to.path}`
  }
}

function handleVue3(to) {
  if (to.path.startsWith(VUE3_PREFIX)) {
    window.location.href = location.origin + to.fullPath
  }
}

router.beforeEach((to, from, next) => {
  store.dispatch("removeNotifications")
  handleVue3(to)
  // TODO: audit code to check that notifies are placed after redirects
  // TODO: check the tunnel to see if the change of step also clears notifications
  chooseAuthorisedRoute(to, from, next)
})

export { router, routes }
