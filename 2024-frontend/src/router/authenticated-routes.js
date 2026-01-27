import { sectionId } from "@/constants/site-map.js"

/* Components */
import GestionnaireCantineGerer from "@/views/GestionnaireCantineGerer.vue"
import GestionnaireCantineGroupeAjouter from "@/views/GestionnaireCantineGroupeAjouter.vue"
import GestionnaireCantineGroupeModifier from "@/views/GestionnaireCantineGroupeModifier.vue"
import GestionnaireCantineGroupeSatellites from "@/views/GestionnaireCantineGroupeSatellites.vue"
import GestionnaireCantineRestaurantAjouter from "@/views/GestionnaireCantineRestaurantAjouter.vue"
import GestionnaireCantineRestaurantModifier from "@/views/GestionnaireCantineRestaurantModifier.vue"
import GestionnaireCantineSupprimer from "@/views/GestionnaireCantineSupprimer.vue"
import GestionnaireGaspillageAlimentaire from "@/views/GestionnaireGaspillageAlimentaire.vue"
import GestionnaireGaspillageAlimentaireModifier from "@/views/GestionnaireGaspillageAlimentaireModifier.vue"
import GestionnaireImport from "@/views/GestionnaireImport.vue"
import GestionnaireImportAchats from "@/views/GestionnaireImportAchats.vue"
import GestionnaireImportAchatsSIRET from "@/views/GestionnaireImportAchatsSIRET.vue"
import GestionnaireImportBilansSimples from "@/views/GestionnaireImportBilansSimples.vue"
import GestionnaireImportCantines from "@/views/GestionnaireImportCantines.vue"
import GestionnaireTableauDeBord from "@/views/GestionnaireTableauDeBord.vue"

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
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "DashboardManager" }, useCanteenName: true },
      ],
    },
  },
  {
    path: "/tableau-de-bord/",
    name: "GestionnaireTableauDeBord",
    component: GestionnaireTableauDeBord,
    meta: {
      title: "Mon tableau de bord",
    },
  },
  {
    path: "/tableau-de-bord/imports/",
    children: [
      {
        path: "",
        name: "GestionnaireImport",
        component: GestionnaireImport,
        meta: {
          title: "Importer des données",
          siteMap: diag,
          breadcrumbs: [{ to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" }],
        },
      },
      {
        path: "achats",
        name: "GestionnaireImportAchats",
        component: GestionnaireImportAchats,
        meta: {
          title: "Importer des achats via ID",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireImport" }, title: "Importer des données" },
          ],
        },
      },
      {
        path: "achats-siret",
        name: "GestionnaireImportAchatsSIRET",
        component: GestionnaireImportAchatsSIRET,
        meta: {
          title: "Importer des achats via SIRET",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireImport" }, title: "Importer des données" },
          ],
        },
      },
      {
        path: "bilans-simples",
        name: "GestionnaireImportBilansSimples",
        component: GestionnaireImportBilansSimples,
        meta: {
          title: "Importer des bilans simples",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireImport" }, title: "Importer des données" },
          ],
        },
      },
      {
        path: "cantines",
        name: "GestionnaireImportCantines",
        component: GestionnaireImportCantines,
        meta: {
          title: "Importer des cantines",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireImport" }, title: "Importer des données" },
          ],
        },
      },
    ],
  },
  {
    path: "/tableau-de-bord/cantines/ajouter",
    name: "GestionnaireCantineRestaurantAjouter",
    component: GestionnaireCantineRestaurantAjouter,
    meta: {
      title: "Ajouter une cantine",
      breadcrumbs: [{ to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" }],
      siteMap: action,
    },
  },
  {
    path: "/tableau-de-bord/cantines/ajouter-groupe",
    name: "GestionnaireCantineGroupeAjouter",
    component: GestionnaireCantineGroupeAjouter,
    meta: {
      title: "Ajouter un groupe de restaurants satellites",
      breadcrumbs: [{ to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" }],
      siteMap: action,
    },
  },
  {
    path: "/tableau-de-bord/cantines/:canteenUrlComponent/",
    children: [
      {
        path: "gerer",
        name: "GestionnaireCantineGerer",
        component: GestionnaireCantineGerer,
        meta: {
          title: "Gérer mon établissement",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
          ],
        },
      },
      {
        path: "supprimer",
        name: "GestionnaireCantineSupprimer",
        component: GestionnaireCantineSupprimer,
        meta: {
          title: "Supprimer mon établissement",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
            { to: { name: "GestionnaireCantineGerer" }, title: "Gérer mon établissement" },
          ],
        },
      },
      {
        path: "modifier",
        name: "GestionnaireCantineRestaurantModifier",
        component: GestionnaireCantineRestaurantModifier,
        meta: {
          title: "Modifier mon établissement",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
            { to: { name: "GestionnaireCantineGerer" }, title: "Gérer mon établissement" },
          ],
        },
      },
      {
        path: "satellites",
        name: "GestionnaireCantineGroupeSatellites",
        component: GestionnaireCantineGroupeSatellites,
        meta: {
          title: "Gérer les restaurants satellites",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
          ],
        },
      },
      {
        path: "modifier-groupe",
        name: "GestionnaireCantineGroupeModifier",
        component: GestionnaireCantineGroupeModifier,
        meta: {
          title: "Modifier mon groupe de restaurants satellites",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "DashboardManager" }, useCanteenName: true },
            { to: { name: "GestionnaireCantineGerer" }, title: "Gérer mon établissement" },
          ],
        },
      },
    ],
  },
]

const addAuthentificationRequired = (route) => {
  if (route.meta) route.meta.authenticationRequired = true
  if (route.children) {
    route.children.forEach((child) => {
      addAuthentificationRequired(child)
    })
  }
}

routes.forEach((route) => addAuthentificationRequired(route))

export default routes
