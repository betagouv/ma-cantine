import Vue from "vue"
import VueRouter from "vue-router"
import store from "@/store/index"
import LandingPage from "@/views/LandingPage"
import ManagerLanding from "@/views/ManagerLanding"
import DiagnosticPage from "@/views/DiagnosticPage"
import KeyMeasuresPage from "@/views/KeyMeasuresPage"
import KeyMeasuresHome from "@/views/KeyMeasuresPage/KeyMeasuresHome"
import KeyMeasurePage from "@/views/KeyMeasuresPage/KeyMeasurePage"
import GeneratePosterPage from "@/views/GeneratePosterPage"
import CanteensPage from "@/views/CanteensPage"
import CanteenWidget from "@/views/CanteensPage/CanteenWidget"
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
import PartnersPage from "@/views/PartnersPage"
import PartnersHome from "@/views/PartnersPage/PartnersHome"
import PartnerPage from "@/views/PartnersPage/PartnerPage"
import NewPartner from "@/views/NewPartner"
import NotFound from "@/views/NotFound"
import CGU from "@/views/CGU.vue"
import PrivacyPolicy from "@/views/PrivacyPolicy.vue"
import ManagementPage from "@/views/ManagementPage"
import PendingActions from "@/views/PendingActions"
import CanteenEditor from "@/views/CanteenEditor"
import CanteenForm from "@/views/CanteenEditor/CanteenForm"
import SatelliteManagement from "@/views/CanteenEditor/SatelliteManagement"
import DiagnosticList from "@/views/CanteenEditor/DiagnosticList"
import CanteenManagers from "@/views/CanteenEditor/CanteenManagers"
import CanteenGeneratePoster from "@/views/CanteenEditor/CanteenGeneratePoster"
import CanteenDeletion from "@/views/CanteenEditor/CanteenDeletion"
import PublicationForm from "@/views/CanteenEditor/PublicationForm"
import PublishSatellites from "@/views/CanteenEditor/PublishSatellites"
import DashboardPage from "@/views/CanteenEditor/DashboardPage"
import DiagnosticEditor from "@/views/DiagnosticEditor"
import DiagnosticsImporter from "@/views/DiagnosticsImporter"
import DiagnosticImportPage from "@/views/DiagnosticsImporter/DiagnosticImportPage"
import PublicCanteenStatisticsPage from "@/views/PublicCanteenStatisticsPage"
import AccessibilityDeclaration from "@/views/AccessibilityDeclaration"
import ContactPage from "@/views/ContactPage"
import PurchasesHome from "@/views/PurchasesHome"
import PurchasePage from "@/views/PurchasePage"
import PurchasesImporter from "@/views/PurchasesImporter"
import PurchasesSummary from "@/views/PurchasesSummary"
import CommunityPage from "@/views/CommunityPage"
import FaqPage from "@/views/FaqPage"
import SiteMap from "@/views/SiteMap"
import DeveloperPage from "@/views/DeveloperPage"
import ImpactMeasuresPage from "@/views/ImpactMeasuresPage"
import DashboardManager from "@/views/DashboardManager"
import TerritoryCanteens from "@/views/TerritoryCanteens"
import VideoTutorial from "@/views/VideoTutorial"
import MyProgress from "@/views/MyProgress"
import Constants from "@/constants"

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
        sitemapGroup: Constants.SitemapGroups.SITE,
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
    sitemapGroup: Constants.SitemapGroups.DIAG,
  },
  {
    path: "/creation-affiche",
    name: "GeneratePosterPage",
    component: GeneratePosterPage,
    meta: {
      title: "Affiche convives",
    },
    sitemapGroup: Constants.SitemapGroups.ACTION,
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
    meta: {
      title: "Les mesures phares",
    },
    sitemapGroup: Constants.SitemapGroups.LAW,
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
          title: "Nos cantines",
        },
        sitemapGroup: Constants.SitemapGroups.LAW,
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
    path: "/mentions-legales",
    name: "LegalNotices",
    component: LegalNotices,
    meta: {
      title: "Mentions légales",
    },
    sitemapGroup: Constants.SitemapGroups.SITE,
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
        sitemapGroup: Constants.SitemapGroups.LAW,
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
        sitemapGroup: Constants.SitemapGroups.ACTION,
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
    sitemapGroup: Constants.SitemapGroups.ACTION,
  },
  {
    path: "/cgu",
    name: "CGU",
    component: CGU,
    meta: {
      title: "Conditions générales d'utilisation",
    },
    sitemapGroup: Constants.SitemapGroups.SITE,
  },
  {
    path: "/politique-de-confidentialite",
    name: "PrivacyPolicy",
    component: PrivacyPolicy,
    meta: {
      title: "Politique de confidentialité",
    },
    sitemapGroup: Constants.SitemapGroups.SITE,
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
    path: "/actions-en-attente",
    name: "PendingActions",
    component: PendingActions,
    meta: {
      title: "Actions en attente",
      authenticationRequired: true,
    },
  },
  {
    path: "/nouvelle-cantine",
    name: "NewCanteen",
    component: CanteenEditor,
    redirect: { name: "NewCanteenForm" },
    children: [
      {
        path: "",
        name: "NewCanteenForm",
        component: CanteenForm,
        meta: {
          title: "Ajouter ma cantine",
          authenticationRequired: true,
        },
        sitemapGroup: Constants.SitemapGroups.ACTION,
      },
    ],
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent",
    name: "CanteenModification",
    props: true,
    component: CanteenEditor,
    redirect: { name: "CanteenForm" },
    children: [
      {
        path: "modifier",
        name: "CanteenForm",
        props: true,
        component: CanteenForm,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "satellites",
        name: "SatelliteManagement",
        component: SatelliteManagement,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "diagnostics",
        name: "DiagnosticList",
        component: DiagnosticList,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "gestionnaires",
        name: "CanteenManagers",
        component: CanteenManagers,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "generer-mon-affiche",
        name: "CanteenGeneratePoster",
        component: CanteenGeneratePoster,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "supprimer",
        name: "CanteenDeletion",
        component: CanteenDeletion,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "publier",
        name: "PublicationForm",
        component: PublicationForm,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "publier-mes-satellites",
        name: "PublishSatellites",
        component: PublishSatellites,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "ameliorer",
        name: "DashboardPage",
        component: DashboardPage,
        meta: {
          authenticationRequired: true,
        },
      },
      {
        path: "modifier-mon-diagnostic/:year",
        name: "DiagnosticModification",
        component: DiagnosticEditor,
        props: true,
        meta: {
          title: "Modifier mon diagnostic",
          authenticationRequired: true,
        },
      },
      {
        path: "nouveau-diagnostic",
        name: "NewDiagnosticForCanteen",
        component: DiagnosticEditor,
        props: true,
        meta: {
          title: "Ajouter un nouveau diagnostic",
          authenticationRequired: true,
        },
      },
    ],
  },
  {
    path: "/modifier-mon-diagnostic/:canteenUrlComponent/:year",
    props: true,
    redirect: { name: "DiagnosticModification" },
  },
  {
    path: "/nouveau-diagnostic/:canteenUrlComponent",
    props: true,
    redirect: { name: "NewDiagnosticForCanteen" },
  },
  {
    path: "/importer-diagnostics",
    name: "DiagnosticsImporter",
    component: DiagnosticsImporter,
    meta: {
      title: "Importer des diagnostics",
      authenticationRequired: true,
    },
    sitemapGroup: Constants.SitemapGroups.DIAG,
  },
  {
    path: "/importer-diagnostics/:importUrlSlug",
    name: "DiagnosticImportPage",
    component: DiagnosticImportPage,
    props: true,
  },
  {
    path: "/statistiques-regionales",
    name: "PublicCanteenStatisticsPage",
    component: PublicCanteenStatisticsPage,
    meta: {
      title: "Les cantines dans ma collectivité",
    },
    sitemapGroup: Constants.SitemapGroups.LAW,
  },
  {
    path: "/accessibilite",
    name: "AccessibilityDeclaration",
    component: AccessibilityDeclaration,
    meta: {
      title: "Déclaration d'accessibilité",
    },
    sitemapGroup: Constants.SitemapGroups.SITE,
  },
  {
    path: "/contact",
    name: "ContactPage",
    component: ContactPage,
    meta: {
      title: "Contactez-nous",
    },
    sitemapGroup: Constants.SitemapGroups.SITE,
  },
  {
    path: "/mes-achats",
    name: "PurchasesHome",
    component: PurchasesHome,
    meta: {
      title: "Mes achats",
      authenticationRequired: true,
    },
    sitemapGroup: Constants.SitemapGroups.DIAG,
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
    sitemapGroup: Constants.SitemapGroups.DIAG,
  },
  {
    path: "/importer-achats",
    name: "PurchasesImporter",
    component: PurchasesImporter,
    meta: {
      title: "Importer des achats",
      authenticationRequired: true,
    },
    sitemapGroup: Constants.SitemapGroups.DIAG,
  },
  {
    path: "/synthese-achats",
    name: "PurchasesSummary",
    component: PurchasesSummary,
    meta: {
      title: "Synthèse des achats",
      authenticationRequired: true,
    },
    sitemapGroup: Constants.SitemapGroups.DIAG,
  },
  {
    path: "/communaute/",
    name: "CommunityPage",
    component: CommunityPage,
    meta: {
      title: "Webinaires",
    },
    sitemapGroup: Constants.SitemapGroups.LAW,
  },
  {
    path: "/faq/",
    name: "FaqPage",
    component: FaqPage,
    meta: {
      title: "Foire aux questions",
    },
    sitemapGroup: Constants.SitemapGroups.SITE,
  },
  {
    path: "/plan-du-site/",
    name: "SiteMap",
    component: SiteMap,
    meta: {
      title: "Plan du site",
    },
  },
  {
    path: "/developpement-et-apis/",
    name: "DeveloperPage",
    component: DeveloperPage,
    meta: {
      title: "Développement et APIs",
    },
  },
  {
    path: "/statistiques-plateforme/",
    name: "ImpactMeasuresPage",
    component: ImpactMeasuresPage,
    meta: {
      title: "Mesures de notre impact",
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
    path: "/dashboard",
    name: "DashboardManager",
    component: DashboardManager,
    meta: {
      title: "Tableau de bord",
      authenticationRequired: true,
    },
    sitemapGroup: Constants.SitemapGroups.DIAG,
  })
  routes.push({
    path: "/ma-progression/:canteenUrlComponent/:year/:measure",
    name: "MyProgress",
    component: MyProgress,
    props: true,
    meta: {
      title: "Ma Progression",
      authenticationRequired: true,
    },
    sitemapGroup: Constants.SitemapGroups.DIAG,
  })
}

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
    else if (to.meta.home && store.state.loggedUser && store.state.loggedUser.isDev) next({ name: "DeveloperPage" })
    else if (to.meta.home) next({ name: "LandingPage" })
    else if (!to.meta.authenticationRequired || store.state.loggedUser) next()
    else window.location.href = `/s-identifier?next=${to.path}`
  }
}

router.beforeEach((to, from, next) => {
  chooseAuthorisedRoute(to, from, next)
})

export { router, routes }
