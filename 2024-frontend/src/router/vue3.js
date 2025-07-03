import { sectionId } from "@/constants/site-map.js"

/* Components */
import WasteMeasurementTunnel from "@/views/WasteMeasurementTunnel.vue"
import WasteMeasurements from "@/views/WasteMeasurements.vue"
import ImportSelection from "@/views/ImportSelection.vue"
import Developpeurs from "@/views/Developpeurs.vue"
import LegalNotices from "@/views/LegalNotices.vue"
import Accessibilite from "@/views/Accessibilite.vue"
import CGU from "@/views/CGU.vue"
import Contact from "@/views/Contact.vue"
import GestionnaireImportsAchat from "@/views/GestionnaireImportsAchat.vue"
import GestionnaireImportsCantine from "@/views/GestionnaireImportsCantine.vue"
import GestionnaireCantineAjouter from "@/views/GestionnaireCantineAjouter.vue"
import GestionnaireCantineModifier from "@/views/GestionnaireCantineModifier.vue"
import FoireAuxQuestions from "@/views/FoireAuxQuestions.vue"
import PersonalData from "@/views/PersonalData.vue"
import SiteMap from "@/views/SiteMap.vue"
import StatisticsCanteens from "@/views/StatisticsCanteens.vue"

/* Sitemap section id */
const { diag, action, site } = sectionId

/* Routes */
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
      siteMap: diag,
    },
  },
  {
    path: "/developpement-et-apis",
    name: "Developpeurs",
    component: Developpeurs,
    meta: {
      title: "Développement et APIs",
      siteMap: action,
    },
  },
  {
    path: "/mentions-legales",
    name: "LegalNotices",
    component: LegalNotices,
    meta: {
      title: "Mentions légales",
      siteMap: site,
    },
  },
  {
    path: "/accessibilite",
    name: "Accessibilite",
    component: Accessibilite,
    meta: {
      title: "Déclaration d'accessibilité",
      siteMap: site,
    },
  },
  {
    path: "/cgu",
    name: "CGU",
    component: CGU,
    meta: {
      title: "Conditions générales d'utilisation",
      siteMap: site,
    },
  },
  {
    path: "/contact",
    name: "Contact",
    component: Contact,
    meta: {
      title: "Contactez-nous",
      siteMap: site,
    },
  },
  {
    path: "/importer-des-donnees/achats",
    name: "GestionnaireImportsAchat",
    component: GestionnaireImportsAchat,
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
    name: "GestionnaireImportsCantine",
    component: GestionnaireImportsCantine,
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
    name: "GestionnaireCantineAjouter",
    component: GestionnaireCantineAjouter,
    meta: {
      authenticationRequired: true,
      title: "Ajouter une cantine",
      breadcrumbs: [{ to: { name: "ManagementPage" }, title: "Mon tableau de bord" }],
      siteMap: action,
    },
  },
  {
    path: "/modifier-ma-cantine/:canteenUrlComponent",
    children: [
      {
        path: "etablissement",
        name: "GestionnaireCantineModifier",
        component: GestionnaireCantineModifier,
        meta: {
          authenticationRequired: true,
          title: "Modifier mon établissement",
          breadcrumbs: [
            { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
          ],
        },
      },
    ],
  },
  {
    path: "/foire-aux-questions",
    name: "FoireAuxQuestions",
    component: FoireAuxQuestions,
    meta: {
      title: "Foire aux questions",
      siteMap: site,
    },
  },
  {
    path: "/donnees-personnelles",
    name: "PersonalData",
    component: PersonalData,
    meta: {
      title: "Données personnelles",
      siteMap: site,
    },
  },
  {
    path: "/plan-du-site",
    name: "SiteMap",
    component: SiteMap,
    meta: {
      title: "Plan du site",
    },
  },
  {
    path: "/statistiques-cantines",
    name: "StatisticsCanteens",
    component: StatisticsCanteens,
    meta: {
      title: "Statistiques cantines (nom à revoir)",
    },
  },
]

export default vue3routes
