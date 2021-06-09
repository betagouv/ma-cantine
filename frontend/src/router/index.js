import Vue from "vue"
import VueRouter from "vue-router"
import store from "@/store/index"
import LandingPage from "@/views/LandingPage"
import DiagnosticPage from "@/views/DiagnosticPage"
import KeyMeasuresPage from "@/views/KeyMeasuresPage"
import PublishPage from "@/views/PublishPage"
import CanteenInfo from "@/views/PublishPage/CanteenInfo"
import PublishMeasurePage from "@/views/PublishPage/PublishMeasurePage"
import SubmitPublicationPage from "@/views/PublishPage/SubmitPublicationPage"
import KeyMeasuresHome from "@/views/KeyMeasuresPage/KeyMeasuresHome"
import KeyMeasurePage from "@/views/KeyMeasuresPage/KeyMeasurePage"
import GeneratePosterPage from "@/views/GeneratePosterPage"
import CanteensPage from "@/views/CanteensPage"
import CanteensHome from "@/views/CanteensPage/CanteensHome"
import CanteenPage from "@/views/CanteensPage/CanteenPage"
import LegalNotices from "@/views/LegalNotices"
import AccountSummaryPage from "@/views/AccountSummaryPage"
import BlogsPage from "@/views/BlogsPage"
import BlogsHome from "@/views/BlogsPage/BlogsHome"
import BlogPage from "@/views/BlogsPage/BlogPage"
import StatsPage from "@/views/StatsPage"
import NotFound from "@/views/NotFound"
import TesterParticipation from "@/views/TesterParticipation"
import CGU from "@/views/CGU.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/mon-compte",
    name: "AccountSummaryPage",
    component: AccountSummaryPage,
    meta: {
      title: "Mon compte",
    },
  },
  {
    path: "/diagnostic",
    name: "DiagnosticPage",
    component: DiagnosticPage,
    meta: {
      title: "M'auto-évaluer",
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
    path: "/publication",
    name: "PublishPage",
    component: PublishPage,
    beforeEnter: (route, _, next) => {
      store.state.loggedUser ? next() : next({ name: "LandingPage" })
    },
    children: [
      {
        path: "",
        name: "CanteenInfo",
        component: CanteenInfo,
        meta: {
          title: "Cantine information - Publication",
        },
      },
      {
        path: "validation",
        name: "SubmitPublicationPage",
        component: SubmitPublicationPage,
        meta: {
          title: "Validation - Publication",
        },
      },
      {
        path: ":id",
        name: "PublishMeasurePage",
        component: PublishMeasurePage,
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
      },
      {
        path: ":id",
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
    meta: {
      title: "Blog",
    },
    children: [
      {
        path: "",
        name: "BlogsHome",
        component: BlogsHome,
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
    path: "/stats",
    name: "StatsPage",
    component: StatsPage,
    meta: {
      title: "Statistiques",
    },
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
    path: "/:catchAll(.*)",
    component: NotFound,
    name: "NotFound",
  },
]

const router = new VueRouter({
  mode: "history",
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 }
  },
})

router.beforeEach((to, from, next) => {
  if (store.state.initialDataLoaded) {
    next()
    return
  }

  store
    .dispatch("fetchInitialData")
    .then(next)
    .catch((e) => {
      console.error(`An error ocurred: ${e}`)
      next(e)
    })
})

export default router
