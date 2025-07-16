import { sectionId } from "@/constants/site-map.js"

/* Components */
import Accessibilite from "@/views/Accessibilite.vue"
import ConditionsGeneralesUtilisation from "@/views/ConditionsGeneralesUtilisation.vue"
import Contact from "@/views/Contact.vue"
import Developpeurs from "@/views/Developpeurs.vue"
import DonneesPersonnelles from "@/views/DonneesPersonnelles.vue"
import FoireAuxQuestions from "@/views/FoireAuxQuestions.vue"
import MentionsLegales from "@/views/MentionsLegales.vue"
import Observatoire from "@/views/Observatoire.vue"
import PlanDuSite from "@/views/PlanDuSite.vue"

/* Sitemap section id */
const { action, site } = sectionId

/* Routes */
const routes = [
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
    name: "MentionsLegales",
    component: MentionsLegales,
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
    name: "ConditionsGeneralesUtilisation",
    component: ConditionsGeneralesUtilisation,
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
    name: "DonneesPersonnelles",
    component: DonneesPersonnelles,
    meta: {
      title: "Données personnelles",
      siteMap: site,
    },
  },
  {
    path: "/plan-du-site",
    name: "PlanDuSite",
    component: PlanDuSite,
    meta: {
      title: "Plan du site",
    },
  },
  {
    path: "/observatoire",
    name: "Observatoire",
    component: Observatoire,
    meta: {
      title: "Observatoire EGalim en restauration collective",
    },
  },
]

export default routes
