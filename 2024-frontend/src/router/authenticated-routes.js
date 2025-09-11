import { sectionId } from "@/constants/site-map.js"

/* Components */
import GestionnaireCantineAjouter from "@/views/GestionnaireCantineAjouter.vue"
import GestionnaireCantineModifier from "@/views/GestionnaireCantineModifier.vue"
import GestionnaireCantineSatellitesAjouter from "@/views/GestionnaireCantineSatellitesAjouter.vue"
import GestionnaireGaspillageAlimentaire from "@/views/GestionnaireGaspillageAlimentaire.vue"
import GestionnaireGaspillageAlimentaireModifier from "@/views/GestionnaireGaspillageAlimentaireModifier.vue"
import GestionnaireImport from "@/views/GestionnaireImport.vue"
import GestionnaireImportAchats from "@/views/GestionnaireImportAchats.vue"
import GestionnaireImportCantines from "@/views/GestionnaireImportCantines.vue"

/* Sitemap section id */
const { diag, action } = sectionId

/* Routes */
const routes = [
  // TODO: refactor "GaspillageAlimentaire" path
  {
    path: "/evaluation-gaspillage-alimentaire/:canteenUrlComponent/:id?",
    name: "GestionnaireGaspillageAlimentaireModifier",
    component: GestionnaireGaspillageAlimentaireModifier,
    props: (route) => ({ ...route.query, ...route.params }),
    meta: {
      title: "Évaluation déchets alimentaires",
      fullscreen: true,
    },
  },
  {
    path: "/gaspillage-alimentaire/:canteenUrlComponent",
    name: "GestionnaireGaspillageAlimentaire",
    component: GestionnaireGaspillageAlimentaire,
    props: (route) => ({ ...route.params }),
    meta: {
      title: "Déchets alimentaires",
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "DashboardManager" }, useCanteenName: true },
      ],
    },
  },
  {
    path: "/gestion/imports",
    name: "GestionnaireImport",
    component: GestionnaireImport,
    meta: {
      title: "Importer des données",
      siteMap: diag,
    },
  },
  {
    path: "/gestion/imports/achats",
    name: "GestionnaireImportAchats",
    component: GestionnaireImportAchats,
    meta: {
      title: "Importer des achats",
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "/gestion/imports/cantines",
    name: "GestionnaireImportCantines",
    component: GestionnaireImportCantines,
    meta: {
      title: "Importer des cantines",
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "/gestion/cantines/ajouter",
    name: "GestionnaireCantineAjouter",
    component: GestionnaireCantineAjouter,
    meta: {
      title: "Ajouter une cantine",
      breadcrumbs: [{ to: { name: "ManagementPage" }, title: "Mon tableau de bord" }],
      siteMap: action,
    },
  },
  {
    path: "/gestion/cantines/:canteenUrlComponent/",
    children: [
      {
        path: "modifier",
        name: "GestionnaireCantineModifier",
        component: GestionnaireCantineModifier,
        meta: {
          title: "Modifier mon établissement",
          breadcrumbs: [
            { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
          ],
        },
      },
      {
        path: "satellites/ajouter",
        name: "GestionnaireCantineSatellitesAjouter",
        component: GestionnaireCantineSatellitesAjouter,
        meta: {
          title: "Ajouter un satellite",
          breadcrumbs: [
            { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
            { to: { name: "SatelliteManagement" }, title: "Gérer mes satellites" },
          ],
        },
      },
    ],
  },
]

routes.forEach((route) => {
  if (route.meta) route.meta.authenticationRequired = true
  else if (route.children) {
    route.children.forEach((child) => {
      child.meta.authenticationRequired = true
    })
  }
})

export default routes
