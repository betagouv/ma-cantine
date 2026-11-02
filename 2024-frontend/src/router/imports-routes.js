import { sectionId } from "@/constants/site-map.js"

/* Components */
import GestionnaireImportAchatsID from "@/views/GestionnaireImportAchatsID.vue"
import GestionnaireImportAchatsSIRET from "@/views/GestionnaireImportAchatsSIRET.vue"
import GestionnaireImport from "@/views/GestionnaireImport.vue"
import GestionnaireImportAchatsIDOld from "@/views/GestionnaireImportAchatsIDOld.vue"
import GestionnaireImportAchatsSIRETOld from "@/views/GestionnaireImportAchatsSIRETOld.vue"
import GestionnaireImportBilansSimplesOld from "@/views/GestionnaireImportBilansSimplesOld.vue"
import GestionnaireImportBilansDetaillesOld from "@/views/GestionnaireImportBilansDetaillesOld.vue"
import GestionnaireImportBilansSimplesSIRETOld from "@/views/GestionnaireImportBilansSimplesSIRETOld.vue"
import GestionnaireImportBilansSimples from "@/views/GestionnaireImportBilansSimples.vue"
import GestionnaireImportBilansDetailles from "@/views/GestionnaireImportBilansDetailles.vue"
import GestionnaireImportBilansSimplesSIRET from "@/views/GestionnaireImportBilansSimplesSIRET.vue"
import GestionnaireImportCantinesCreer from "@/views/GestionnaireImportCantinesCreer.vue"
import GestionnaireImportCantinesModifier from "@/views/GestionnaireImportCantinesModifier.vue"
import GestionnaireImportCantinesGestionnaires from "@/views/GestionnaireImportCantinesGestionnaires.vue"

/* Stores */
import { useStoreCampaignDates } from "@/stores/campaignDates"

/* Sitemap section id */
const { diag } = sectionId

/* Redirections */
const redirectIfCampaignIsClosed = () => {
  const campaignDatesStore = useStoreCampaignDates()
  if (campaignDatesStore.currentCampaignIsOpen) return true
  return { name: "GestionnaireImport" }
}

/* Route */
const importsRoutes = [
  {
    path: "",
    name: "GestionnaireImport",
    component: GestionnaireImport,
    meta: {
      title: "Importer des données",
      siteMap: diag,
      storesRequired: ["campaignDates"],
      breadcrumbs: [{ to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" }],
    },
  },
  {
    path: "achats-ancien-format",
    name: "GestionnaireImportAchatsIDOld",
    component: GestionnaireImportAchatsIDOld,
    meta: {
      title: "Ajouter des achats via l'ID de la cantine (ancien format)",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "achats-siret-ancien-format",
    name: "GestionnaireImportAchatsSIRETOld",
    component: GestionnaireImportAchatsSIRETOld,
    meta: {
      title: "Ajouter des achats via le SIRET de la cantine (ancien format)",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "achats-id",
    name: "GestionnaireImportAchatsID",
    component: GestionnaireImportAchatsID,
    meta: {
      title: "Ajouter des achats via l'ID de la cantine",
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
      title: "Ajouter des achats via le SIRET de la cantine",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "bilans-simples-ancien-format",
    name: "GestionnaireImportBilansSimplesOld",
    component: GestionnaireImportBilansSimplesOld,
    beforeEnter: redirectIfCampaignIsClosed,
    meta: {
      storesRequired: ["campaignDates"],
      title: "Créer ou modifier des bilans simples via l'ID de la cantine (ancien format)",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "bilans-simples-siret-ancien-format",
    name: "GestionnaireImportBilansSimplesSIRETOld",
    component: GestionnaireImportBilansSimplesSIRETOld,
    beforeEnter: redirectIfCampaignIsClosed,
    meta: {
      storesRequired: ["campaignDates"],
      title: "Créer ou modifier des bilans simples via le SIRET de la cantine (ancien format)",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "bilans-detailles-ancien-format",
    name: "GestionnaireImportBilansDetaillesOld",
    component: GestionnaireImportBilansDetaillesOld,
    beforeEnter: redirectIfCampaignIsClosed,
    meta: {
      storesRequired: ["campaignDates"],
      title: "Créer ou modifier des bilans détaillés (ancien format)",
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
    beforeEnter: redirectIfCampaignIsClosed,
    meta: {
      storesRequired: ["campaignDates"],
      title: "Créer ou modifier des bilans simples via l'ID de la cantine",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "bilans-simples-siret",
    name: "GestionnaireImportBilansSimplesSIRET",
    component: GestionnaireImportBilansSimplesSIRET,
    beforeEnter: redirectIfCampaignIsClosed,
    meta: {
      storesRequired: ["campaignDates"],
      title: "Créer ou modifier des bilans simples via le SIRET de la cantine",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "bilans-detailles",
    name: "GestionnaireImportBilansDetailles",
    component: GestionnaireImportBilansDetailles,
    beforeEnter: redirectIfCampaignIsClosed,
    meta: {
      storesRequired: ["campaignDates"],
      title: "Créer ou modifier des bilans détaillés",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "cantines-creer",
    name: "GestionnaireImportCantinesCreer",
    component: GestionnaireImportCantinesCreer,
    meta: {
      title: "Créer des cantines",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "cantines-modifier",
    name: "GestionnaireImportCantinesModifier",
    component: GestionnaireImportCantinesModifier,
    meta: {
      title: "Modifier des cantines",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
  {
    path: "cantines-gestionnaires",
    name: "GestionnaireImportCantinesGestionnaires",
    component: GestionnaireImportCantinesGestionnaires,
    meta: {
      title: "Ajouter des gestionnaires en masse via le SIRET des cantines",
      breadcrumbs: [
        { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
        { to: { name: "GestionnaireImport" }, title: "Importer des données" },
      ],
    },
  },
]

export default importsRoutes
