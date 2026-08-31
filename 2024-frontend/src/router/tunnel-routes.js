/* Components */
import GestionnaireTunnelApproInformations from "@/views/GestionnaireTunnelApproInformations.vue"
import GestionnaireTunnelApproCouverts from "@/views/GestionnaireTunnelApproCouverts.vue"
import GestionnaireTunnelApproSaisie from "@/views/GestionnaireTunnelApproSaisie.vue"
import GestionnaireTunnelApproEgalim from "@/views/GestionnaireTunnelApproEgalim.vue"
import GestionnaireTunnelApproOrigine from "@/views/GestionnaireTunnelApproOrigine.vue"
import GestionnaireTunnelApproLocalCircuitCourt from "@/views/GestionnaireTunnelApproLocalCircuitCourt.vue"
import GestionnaireTunnelApproRecapitulatif from "@/views/GestionnaireTunnelApproRecapitulatif.vue"
import GestionnaireTunnelConvives from "@/views/GestionnaireTunnelConvives.vue"
import GestionnaireTunnelGaspillage from "@/views/GestionnaireTunnelGaspillage.vue"
import GestionnaireTunnelVegetarien from "@/views/GestionnaireTunnelVegetarien.vue"
import GestionnaireTunnelPlastique from "@/views/GestionnaireTunnelPlastique.vue"

import LayoutTunnelTeledeclaration from "@/layouts/LayoutTunnelTeledeclaration.vue"

/* Route */
const tunnelRoutes = {
  path: "teledeclaration",
  component: LayoutTunnelTeledeclaration,
  meta: {
    isTunnel: true,
    storesRequired: ["diagnostic", "canteen", "purchaseSummary"],
    nav: {
      approvisionnements: [
        { to: { name: "GestionnaireTunnelApproInformations" }, title: "Informations" },
        { to: { name: "GestionnaireTunnelApproCouverts" }, title: "Couverts annuels" },
        { to: { name: "GestionnaireTunnelApproSaisie" }, title: "Mode de saisie" },
        { to: { name: "GestionnaireTunnelApproEgalim" }, title: "EGalim" },
        { to: { name: "GestionnaireTunnelApproOrigine" }, title: "Origine France et UE" },
        { to: { name: "GestionnaireTunnelApproLocalCircuitCourt" }, title: "« Local » et circuit court" },
        { to: { name: "GestionnaireTunnelApproRecapitulatif" }, title: "Récapitulatif", icon: "fr-icon-flag-fill" },
      ],
      thematiques: [
        { to: { name: "GestionnaireTunnelConvives" }, title: "Infos convives" },
        { to: { name: "GestionnaireTunnelGaspillage" }, title: "Gaspillage" },
        { to: { name: "GestionnaireTunnelVegetarien" }, title: "Menus végétariens" },
        { to: { name: "GestionnaireTunnelPlastique" }, title: "Substitutions plastiques" },
      ]
    }
  },
  children: [
    {
      path: "approvisionnements",
      children: [
        {
          path: "informations",
          name: "GestionnaireTunnelApproInformations",
          component: GestionnaireTunnelApproInformations,
          meta: {
            title: "Informations",
            next: "GestionnaireTunnelApproCouverts",
            stepper: "approvisionnements",
          },
        },
        {
          path: "couverts-annuels",
          name: "GestionnaireTunnelApproCouverts",
          component: GestionnaireTunnelApproCouverts,
          meta: {
            title: "Couverts annuels",
            previous: "GestionnaireTunnelApproInformations",
            next: "GestionnaireTunnelApproSaisie",
            stepper: "approvisionnements",
          },
        },
        {
          path: "mode-saisie",
          name: "GestionnaireTunnelApproSaisie",
          component: GestionnaireTunnelApproSaisie,
          meta: {
            title: "Mes approvisionnements : mode de saisie",
            previous: "GestionnaireTunnelApproCouverts",
            next: "GestionnaireTunnelApproEgalim",
            stepper: "approvisionnements",
          },
        },
        {
          path: "egalim",
          name: "GestionnaireTunnelApproEgalim",
          component: GestionnaireTunnelApproEgalim,
          meta: {
            title: "EGalim",
            previous: "GestionnaireTunnelApproSaisie",
            next: "GestionnaireTunnelApproOrigine",
            stepper: "approvisionnements",
          },
        },
        {
          path: "origine-france-union-europeenne",
          name: "GestionnaireTunnelApproOrigine",
          component: GestionnaireTunnelApproOrigine,
          meta: {
            title: "Origine France et UE",
            previous: "GestionnaireTunnelApproEgalim",
            next: "GestionnaireTunnelApproLocalCircuitCourt",
            stepper: "approvisionnements",
          },
        },
        {
          path: "local-circuit-court",
          name: "GestionnaireTunnelApproLocalCircuitCourt",
          component: GestionnaireTunnelApproLocalCircuitCourt,
          meta: {
            title: "« Local » et circuit court",
            previous: "GestionnaireTunnelApproOrigine",
            next: "GestionnaireTunnelApproRecapitulatif",
            stepper: "approvisionnements",
          },
        },
        {
          path: "recapitulatif",
          name: "GestionnaireTunnelApproRecapitulatif",
          component: GestionnaireTunnelApproRecapitulatif,
          meta: {
            title: "Recapitulatif des approvisionnements",
            previous: "GestionnaireTunnelApproLocalCircuitCourt",
            stepper: "approvisionnements",
          },
        },
      ]
    },
    {
      path: "volets-thematiques",
      children: [
        {
          path: "informations-convives",
          name: "GestionnaireTunnelConvives",
          component: GestionnaireTunnelConvives,
          meta: {
            title: "Infos convives",
            next: "GestionnaireTunnelGaspillage",
          },
        },
        {
          path: "gaspillage",
          name: "GestionnaireTunnelGaspillage",
          component: GestionnaireTunnelGaspillage,
          meta: {
            title: "Gaspillage",
            previous: "GestionnaireTunnelConvives",
            next: "GestionnaireTunnelVegetarien",
          },
        },
        {
          path: "menus-vegetariens",
          name: "GestionnaireTunnelVegetarien",
          component: GestionnaireTunnelVegetarien,
          meta: {
            title: "Menus végétariens",
            previous: "GestionnaireTunnelGaspillage",
            next: "GestionnaireTunnelPlastique",
          },
        },
        {
          path: "substitutions-plastiques",
          name: "GestionnaireTunnelPlastique",
          component: GestionnaireTunnelPlastique,
          meta: {
            title: "Substitutions plastiques",
            previous: "GestionnaireTunnelVegetarien"
          },
        },
      ]
    },
  ],
}

export default tunnelRoutes
