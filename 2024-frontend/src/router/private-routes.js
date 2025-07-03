import { sectionId } from "@/constants/site-map.js"

/* Components */
import GestionnaireCantineAjouter from "@/views/GestionnaireCantineAjouter.vue"
import GestionnaireCantineModifier from "@/views/GestionnaireCantineModifier.vue"
import GestionnaireGaspillageAlimentaire from "@/views/GestionnaireGaspillageAlimentaire.vue"
import GestionnaireGaspillageAlimentaireModifier from "@/views/GestionnaireGaspillageAlimentaireModifier.vue"
import GestionnaireImports from "@/views/GestionnaireImports.vue"
import GestionnaireImportsAchat from "@/views/GestionnaireImportsAchat.vue"
import GestionnaireImportsCantine from "@/views/GestionnaireImportsCantine.vue"

/* Sitemap section id */
const { diag, action } = sectionId

/* Routes */
const routes = [
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
    path: "/importer-des-donnees",
    name: "GestionnaireImports",
    component: GestionnaireImports,
    meta: {
      title: "Importer des données",
      siteMap: diag,
    },
  },
  {
    path: "/importer-des-donnees/achats",
    name: "GestionnaireImportsAchat",
    component: GestionnaireImportsAchat,
    meta: {
      title: "Importer des achats",
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImports" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "/importer-des-donnees/cantines",
    name: "GestionnaireImportsCantine",
    component: GestionnaireImportsCantine,
    meta: {
      title: "Importer des cantines",
      breadcrumbs: [
        { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImports" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "/ajouter-une-cantine",
    name: "GestionnaireCantineAjouter",
    component: GestionnaireCantineAjouter,
    meta: {
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
          title: "Modifier mon établissement",
          breadcrumbs: [
            { to: { name: "ManagementPage" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
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
