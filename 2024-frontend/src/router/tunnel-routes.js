/* Components */
import GestionnaireTunnelApproInformations from "@/views/GestionnaireTunnelApproInformations.vue"
import GestionnaireTunnelApproCouverts from "@/views/GestionnaireTunnelApproCouverts.vue"
import GestionnaireTunnelApproCouvertsGroupe from "@/views/GestionnaireTunnelApproCouvertsGroupe.vue"
import GestionnaireTunnelApproSaisie from "@/views/GestionnaireTunnelApproSaisie.vue"
import GestionnaireTunnelApproEgalim from "@/views/GestionnaireTunnelApproEgalim.vue"
import GestionnaireTunnelApproOrigine from "@/views/GestionnaireTunnelApproOrigine.vue"
import GestionnaireTunnelApproLocalCircuitCourt from "@/views/GestionnaireTunnelApproLocalCircuitCourt.vue"
import GestionnaireTunnelApproRecapitulatif from "@/views/GestionnaireTunnelApproRecapitulatif.vue"
import GestionnaireTunnelApproTeledeclares from "@/views/GestionnaireTunnelApproTeledeclares.vue"
import GestionnaireTunnelConvives from "@/views/GestionnaireTunnelConvives.vue"
import GestionnaireTunnelGaspillage from "@/views/GestionnaireTunnelGaspillage.vue"
import GestionnaireTunnelVegetarien from "@/views/GestionnaireTunnelVegetarien.vue"
import GestionnaireTunnelPlastique from "@/views/GestionnaireTunnelPlastique.vue"

import LayoutTunnelTeledeclaration from "@/layouts/LayoutTunnelTeledeclaration.vue"

/* Redirections */
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { useStoreCanteen } from "@/stores/canteen"

const redirectIfTeledeclared = (to) => {
  const teledeclarationStore = useStoreTeledeclaration()
  if (!teledeclarationStore.isTeledeclared) return true
  return { name: "GestionnaireTunnelApproTeledeclares", params: to.params }
}

const redirectIfNotTeledeclared = (to) => {
  const teledeclarationStore = useStoreTeledeclaration()
  if (teledeclarationStore.isTeledeclared) return true
  return { name: "GestionnaireTunnelApproRecapitulatif", params: to.params }
}

const redirectCouvertsIfNotGroupe = (to) => {
  const canteenStore = useStoreCanteen()
  if (canteenStore.canteenInformations.isGroupe) return true
  return { name: "GestionnaireTunnelApproCouverts", params: to.params }
}

const redirectCouvertsIfIsGroupe = (to) => {
  const canteenStore = useStoreCanteen()
  if (!canteenStore.canteenInformations.isGroupe) return true
  return { name: "GestionnaireTunnelApproCouvertsGroupe", params: to.params }
}

/* Route */
const tunnelRoutes = {
  path: "teledeclaration",
  component: LayoutTunnelTeledeclaration,
  meta: {
    isTunnel: true,
    storesRequired: ["teledeclaration", "canteen", "purchaseSummary", "campaignDates"],
  },
  children: [
    {
      path: "approvisionnements",
      meta: {
        topNav: "approvisionnements",
      },
      children: [
        {
          path: "informations",
          name: "GestionnaireTunnelApproInformations",
          component: GestionnaireTunnelApproInformations,
          beforeEnter: redirectIfTeledeclared,
          meta: {
            slug: "informations",
            title: "Informations",
            next: "GestionnaireTunnelApproCouverts",
            volet: "approvisionnement",
          },
        },
        {
          path: "couverts-annuels",
          name: "GestionnaireTunnelApproCouverts",
          component: GestionnaireTunnelApproCouverts,
          beforeEnter: [redirectIfTeledeclared, redirectCouvertsIfIsGroupe],
          meta: {
            slug: "couverts",
            title: "Couverts annuels",
            previous: "GestionnaireTunnelApproInformations",
            next: "GestionnaireTunnelApproSaisie",
            volet: "approvisionnement",
          },
        },
        {
          path: "couverts-annuels-groupe",
          name: "GestionnaireTunnelApproCouvertsGroupe",
          component: GestionnaireTunnelApproCouvertsGroupe,
          beforeEnter: [redirectIfTeledeclared, redirectCouvertsIfNotGroupe],
          meta: {
            slug: "couverts-groupe",
            title: "Couverts de mon groupe",
            previous: "GestionnaireTunnelApproInformations",
            next: "GestionnaireTunnelApproSaisie",
            volet: "approvisionnement",
          },
        },
        {
          path: "mode-saisie",
          name: "GestionnaireTunnelApproSaisie",
          component: GestionnaireTunnelApproSaisie,
          beforeEnter: redirectIfTeledeclared,
          meta: {
            slug: "saisie",
            title: "Mode de saisie",
            previous: "GestionnaireTunnelApproCouverts",
            next: "GestionnaireTunnelApproEgalim",
            volet: "approvisionnement",
          },
        },
        {
          path: "egalim",
          name: "GestionnaireTunnelApproEgalim",
          component: GestionnaireTunnelApproEgalim,
          beforeEnter: redirectIfTeledeclared,
          meta: {
            slug: "egalim",
            title: "EGalim",
            previous: "GestionnaireTunnelApproSaisie",
            next: "GestionnaireTunnelApproOrigine",
            volet: "approvisionnement",
          },
        },
        {
          path: "origine-france-union-europeenne",
          name: "GestionnaireTunnelApproOrigine",
          component: GestionnaireTunnelApproOrigine,
          beforeEnter: redirectIfTeledeclared,
          meta: {
            slug: "origine",
            title: "Origine France et UE",
            previous: "GestionnaireTunnelApproEgalim",
            next: "GestionnaireTunnelApproLocalCircuitCourt",
            volet: "approvisionnement",
          },
        },
        {
          path: "local-circuit-court",
          name: "GestionnaireTunnelApproLocalCircuitCourt",
          component: GestionnaireTunnelApproLocalCircuitCourt,
          beforeEnter: redirectIfTeledeclared,
          meta: {
            slug: "localCircuitCourt",
            title: "« Local » et circuit court",
            previous: "GestionnaireTunnelApproOrigine",
            next: "GestionnaireTunnelApproRecapitulatif",
            volet: "approvisionnement",
          },
        },
        {
          path: "recapitulatif",
          name: "GestionnaireTunnelApproRecapitulatif",
          component: GestionnaireTunnelApproRecapitulatif,
          beforeEnter: redirectIfTeledeclared,
          meta: {
            title: "Recapitulatif des approvisionnements",
            previous: "GestionnaireTunnelApproLocalCircuitCourt",
            volet: "approvisionnement",
          },
        },
        {
          path: "teledeclares",
          name: "GestionnaireTunnelApproTeledeclares",
          component: GestionnaireTunnelApproTeledeclares,
          beforeEnter: redirectIfNotTeledeclared,
          meta: {
            title: "Approvisionnements téléclarés",
            hideTopNav: true,
          },
        },
      ]
    },
    {
      path: "volets-thematiques",
      meta: {
        topNav: "thematiques",
      },
      children: [
        {
          path: "informations-convives",
          name: "GestionnaireTunnelConvives",
          component: GestionnaireTunnelConvives,
          meta: {
            title: "Information des convives",
            volet: "information",
            next: "GestionnaireTunnelGaspillage",
          },
        },
        {
          path: "gaspillage",
          name: "GestionnaireTunnelGaspillage",
          component: GestionnaireTunnelGaspillage,
          meta: {
            title: "Lutte contre le gaspillage alimentaire",
            volet: "gaspillage",
            next: "GestionnaireTunnelVegetarien",
          },
        },
        {
          path: "menus-vegetariens",
          name: "GestionnaireTunnelVegetarien",
          component: GestionnaireTunnelVegetarien,
          meta: {
            title: "Menus végétariens",
            volet: "diversification",
            next: "GestionnaireTunnelPlastique",
          },
        },
        {
          path: "substitutions-plastiques",
          name: "GestionnaireTunnelPlastique",
          component: GestionnaireTunnelPlastique,
          meta: {
            title: "Substitution du plastique",
            volet: "plastique",
            isLast: true,
          },
        },
      ]
    },
  ],
}

export default tunnelRoutes
