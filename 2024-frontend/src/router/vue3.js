import WasteMeasurementTunnel from "@/views/WasteMeasurementTunnel.vue"
import WasteMeasurements from "@/views/WasteMeasurements.vue"
import ImportSelection from "@/views/ImportSelection.vue"
import DeveloperAPI from "@/views/DeveloperAPI.vue"
import LegalNotices from "@/views/LegalNotices.vue"
import AccessibilityDeclaration from "@/views/AccessibilityDeclaration.vue"
import CGU from "@/views/CGU.vue"
import ContactPage from "@/views/ContactPage.vue"
import ImportPurchases from "@/views/ImportPurchases.vue"
import ImportCanteens from "@/views/ImportCanteens.vue"
import CanteenCreation from "@/views/CanteenCreation.vue"

const vue3routes = [
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
    path: "/importer-des-donnees",
    name: "ImportSelection",
    component: ImportSelection,
    meta: {
      title: "Importer des données",
      authenticationRequired: true,
    },
  },
  {
    path: "/developpement-et-apis-2",
    name: "DeveloperAPI",
    component: DeveloperAPI,
    meta: {
      title: "Développement et APIs",
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
  {
    path: "/ajouter-une-cantine",
    name: "CanteenCreation",
    component: CanteenCreation,
    meta: {
      title: "Ajouter une cantine",
      breadcrumbs: [{ to: { name: "ManagementPage" }, title: "Mon tableau de bord" }],
    },
  },
]

export default vue3routes
