import Vue from "vue"
import VueRouter from "vue-router"
import store from "@/store/index"
import LandingPage from "@/views/LandingPage"
import DiagnosticPage from "@/views/DiagnosticPage"
import KeyMeasuresPage from "@/views/KeyMeasuresPage"
import KeyMeasuresHome from "@/views/KeyMeasuresPage/KeyMeasuresHome"
import KeyMeasurePage from "@/views/KeyMeasuresPage/KeyMeasurePage"
import GeneratePosterPage from "@/views/GeneratePosterPage"
import CanteensPage from "@/views/CanteensPage"
import CanteensHome from "@/views/CanteensPage/CanteensHome"
import CanteenPage from "@/views/CanteensPage/CanteenPage"
import LegalNotices from "@/views/LegalNotices"
import AccountSummaryPage from "@/views/AccountSummaryPage"
import AccountEditor from "@/views/AccountSummaryPage/AccountEditor"
import PasswordChangeEditor from "@/views/AccountSummaryPage/PasswordChangeEditor"
import AccountDeletion from "@/views/AccountSummaryPage/AccountDeletion"
import BlogsPage from "@/views/BlogsPage"
import BlogsHome from "@/views/BlogsPage/BlogsHome"
import BlogPage from "@/views/BlogsPage/BlogPage"
import NotFound from "@/views/NotFound"
import TesterParticipation from "@/views/TesterParticipation"
import CGU from "@/views/CGU.vue"
import ManagementPage from "@/views/ManagementPage"
import CanteenEditor from "@/views/CanteenEditor"
import CanteenForm from "@/views/CanteenEditor/CanteenForm"
import DiagnosticList from "@/views/CanteenEditor/DiagnosticList"
import CanteenManagers from "@/views/CanteenEditor/CanteenManagers"
import CanteenDeletion from "@/views/CanteenEditor/CanteenDeletion"
import DiagnosticEditor from "@/views/DiagnosticEditor"
import DiagnosticsImporter from "@/views/DiagnosticsImporter"
import AccessibilityDeclaration from "@/views/AccessibilityDeclaration"

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
    path: "/mon-compte",
    name: "AccountSummaryPage",
    component: AccountSummaryPage,
    meta: {
      title: "Mon compte",
      authenticationRequired: true,
    },
    redirect: { name: "AccountEditor" },
    children: [
      {
        path: "profil",
        name: "AccountEditor",
        component: AccountEditor,
      },
      {
        path: "mot-de-passe",
        name: "PasswordChange",
        component: PasswordChangeEditor,
      },
      {
        path: "supprimer-mon-compte",
        name: "AccountDeletion",
        component: AccountDeletion,
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
    meta: {
      title: "Les 5 mesures phares de la loi EGAlim",
    },
    children: [
      {
        path: "",
        name: "KeyMeasuresHome",
        component: KeyMeasuresHome,
        beforeEnter: (route, _, next) => {
          store.state.loggedUser
            ? next({
                name: "KeyMeasurePage",
                params: {
                  id: "qualite-des-produits",
                },
              })
            : next()
        },
      },
      {
        path: ":id",
        name: "KeyMeasurePage",
        component: KeyMeasurePage,
        props: true,
      },
    ],
  },
  {
    path: "/nos-cantines",
    name: "CanteensPage",
    component: CanteensPage,
    children: [
      {
        path: "",
        name: "CanteensHome",
        component: CanteensHome,
        meta: {
          title: "Nos cantines",
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
    path: "/mentions-legales",
    name: "LegalNotices",
    component: LegalNotices,
  },
  {
    path: "/blog",
    name: "BlogsPage",
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
    path: "/devenir-testeur",
    name: "TesterParticipation",
    component: TesterParticipation,
    meta: {
      title: "Devenir Testeur",
    },
  },
  {
    path: "/cgu",
    name: "CGU",
    component: CGU,
  },
  {
    path: "/gestion",
    name: "ManagementPage",
    component: ManagementPage,
    meta: {
      title: "Gérer mes cantines",
      authenticationRequired: true,
    },
  },
  {
    path: "/nouvelle-cantine",
    name: "NewCanteen",
    component: CanteenForm,
    props: {
      canteenUrlComponent: null,
    },
    meta: {
      title: "Ajouter une nouvelle cantine",
      authenticationRequired: true,
    },
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent",
    name: "CanteenModification",
    component: CanteenEditor,
    props: true,
    meta: {
      authenticationRequired: true,
    },
    redirect: { name: "CanteenForm" },
    children: [
      {
        path: "modifier",
        name: "CanteenForm",
        component: CanteenForm,
      },
      {
        path: "diagnostics",
        name: "DiagnosticList",
        component: DiagnosticList,
      },
      {
        path: "gestionnaires",
        name: "CanteenManagers",
        component: CanteenManagers,
      },
      {
        path: "supprimer",
        name: "CanteenDeletion",
        component: CanteenDeletion,
      },
    ],
  },
  {
    path: "/modifier-mon-diagnostic/:canteenUrlComponent/:year",
    name: "DiagnosticModification",
    component: DiagnosticEditor,
    props: true,
    meta: {
      title: "Modifier mon diagnostic",
      authenticationRequired: true,
    },
  },
  {
    path: "/nouveau-diagnostic",
    name: "NewDiagnostic",
    component: DiagnosticEditor,
    props: {
      canteenUrlComponent: null,
      year: null,
    },
    meta: {
      title: "Ajouter un nouveau diagnostic",
      authenticationRequired: true,
    },
  },
  {
    path: "/nouveau-diagnostic/:canteenUrlComponent",
    name: "NewDiagnosticForCanteen",
    component: DiagnosticEditor,
    props: true,
    meta: {
      title: "Ajouter un nouveau diagnostic",
      authenticationRequired: true,
    },
  },
  {
    path: "/importer-diagnostics",
    name: "DiagnosticsImporter",
    component: DiagnosticsImporter,
    meta: {
      title: "Importer des diagnostics",
      authenticationRequired: true,
    },
  },
  {
    path: "/declaration-d-accessibilite",
    name: "AccessibilityDeclaration",
    component: AccessibilityDeclaration,
    meta: {
      title: "Déclaration d'accessibility",
    },
  },
  {
    path: "/:catchAll(.*)",
    component: NotFound,
    name: "NotFound",
  },
]

const router = new VueRouter({
  mode: "history",
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) return { selector: to.hash, offset: { y: 90 } }
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
    if (to.meta.home && store.state.loggedUser) next({ name: "ManagementPage" })
    else if (to.meta.home) next({ name: "LandingPage" })
    else if (!to.meta.authenticationRequired || store.state.loggedUser) next()
    else next({ name: "NotFound" })
  }
}

router.beforeEach((to, from, next) => {
  chooseAuthorisedRoute(to, from, next)
})

export default router
