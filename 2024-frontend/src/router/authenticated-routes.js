import { sectionId } from "@/constants/site-map.js"

/* Components */
import GestionnaireAchatsAjouter from "@/views/GestionnaireAchatsAjouter.vue"
import GestionnaireAchatsModifier from "@/views/GestionnaireAchatsModifier.vue"
import GestionnaireCantineGroupeAjouter from "@/views/GestionnaireCantineGroupeAjouter.vue"
import GestionnaireCantineGroupeModifier from "@/views/GestionnaireCantineGroupeModifier.vue"
import GestionnaireCantineRestaurantAjouter from "@/views/GestionnaireCantineRestaurantAjouter.vue"
import GestionnaireCantineRestaurantModifier from "@/views/GestionnaireCantineRestaurantModifier.vue"
import GestionnaireCantineArchiver from "@/views/GestionnaireCantineArchiver.vue"
import GestionnaireGaspillageAlimentaire from "@/views/GestionnaireGaspillageAlimentaire.vue"
import GestionnaireGaspillageAlimentaireModifier from "@/views/GestionnaireGaspillageAlimentaireModifier.vue"
import GestionnaireTableauDeBord from "@/views/GestionnaireTableauDeBord.vue"

/* Sub routes */
import canteenRoutes from "./canteen-routes"
import tunnelRoutes from "./tunnel-routes"
import importsRoutes from "./imports-routes"

/* Sitemap section id */
const { action } = sectionId

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
    path: "/gaspillage-alimentaire/:canteenUrlComponent?",
    name: "GestionnaireGaspillageAlimentaire",
    component: GestionnaireGaspillageAlimentaire,
    props: (route) => ({ ...route.params }),
    meta: {
      title: "Outil Suivi Anti-Gaspi",
      breadcrumbs: [{ to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" }],
      forceActiveNav: "GestionnaireGaspillageAlimentaire",
    },
  },
  {
    path: "/tableau-de-bord/",
    name: "GestionnaireTableauDeBord",
    component: GestionnaireTableauDeBord,
    meta: {
      title: "Mon tableau de bord",
      storesRequired: ["campaignDates"],
    },
  },
  {
    path: "/tableau-de-bord/imports/",
    children: importsRoutes,
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
      canteenRoutes,
      tunnelRoutes,
      {
        path: "archiver",
        name: "GestionnaireCantineArchiver",
        component: GestionnaireCantineArchiver,
        meta: {
          title: "Archiver mon établissement",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireCantine" }, useCanteenName: true },
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
            { to: { name: "GestionnaireCantine" }, useCanteenName: true },
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
            { to: { name: "GestionnaireCantine" }, useCanteenName: true },
          ],
        },
      },
      {
        path: "achats/ajouter",
        name: "GestionnaireAchatsAjouter",
        component: GestionnaireAchatsAjouter,
        meta: {
          title: "Ajouter un achat",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireCantine" }, useCanteenName: true },
            { to: { name: "PurchasesHome" }, title: "Outil Suivi des Achats"},
          ],
          forceActiveNav: "PurchasesHome",
          storesRequired: ["canteen"],
        },
      },
      {
        path: "achats/:id/modifier",
        name: "GestionnaireAchatsModifier",
        component: GestionnaireAchatsModifier,
        meta: {
          title: "Modifier l'achat",
          breadcrumbs: [
            { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
            { to: { name: "GestionnaireCantine" }, useCanteenName: true },
            { to: { name: "PurchasesHome" }, title: "Outil Suivi des Achats" },
          ],
          forceActiveNav: "PurchasesHome",
          storesRequired: ["canteen"],
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
