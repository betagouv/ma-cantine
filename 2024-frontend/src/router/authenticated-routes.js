import { sectionId } from "@/constants/site-map.js"

/* Components */
import GestionnaireAchatsAjouter from "@/views/GestionnaireAchatsAjouter.vue"
import GestionnaireAchatsModifier from "@/views/GestionnaireAchatsModifier.vue"
import GestionnaireCantine from "@/views/GestionnaireCantine.vue"
import GestionnaireCantineGroupeAjouter from "@/views/GestionnaireCantineGroupeAjouter.vue"
import GestionnaireCantineGroupeModifier from "@/views/GestionnaireCantineGroupeModifier.vue"
import GestionnaireCantineGroupe from "@/views/GestionnaireCantineGroupe.vue"
import GestionnaireCantineRestaurantAjouter from "@/views/GestionnaireCantineRestaurantAjouter.vue"
import GestionnaireCantineRestaurantModifier from "@/views/GestionnaireCantineRestaurantModifier.vue"
import GestionnaireCantineTeledeclarationEnCours from "@/views/GestionnaireCantineTeledeclarationEnCours.vue"
import GestionnaireCantineTeledeclarations from "@/views/GestionnaireCantineTeledeclarations.vue"
import GestionnaireCantineArchiver from "@/views/GestionnaireCantineArchiver.vue"
import GestionnaireCantineGestionnaires from "@/views/GestionnaireCantineGestionnaires.vue"
import GestionnaireCantinePagePublique from "@/views/GestionnaireCantinePagePublique.vue"
import GestionnaireGaspillageAlimentaire from "@/views/GestionnaireGaspillageAlimentaire.vue"
import GestionnaireGaspillageAlimentaireModifier from "@/views/GestionnaireGaspillageAlimentaireModifier.vue"
import GestionnaireImportAchatsID from "@/views/GestionnaireImportAchatsID.vue"
import GestionnaireImportAchatsSIRET from "@/views/GestionnaireImportAchatsSIRET.vue"
import GestionnaireImport from "@/views/GestionnaireImport.vue"
import GestionnaireImportAchatsIDOld from "@/views/GestionnaireImportAchatsIDOld.vue"
import GestionnaireImportAchatsSIRETOld from "@/views/GestionnaireImportAchatsSIRETOld.vue"
import GestionnaireImportBilansSimples from "@/views/GestionnaireImportBilansSimples.vue"
import GestionnaireImportBilansDetailles from "@/views/GestionnaireImportBilansDetailles.vue"
import GestionnaireImportBilansSimplesSIRET from "@/views/GestionnaireImportBilansSimplesSIRET.vue"
import GestionnaireImportCantinesCreer from "@/views/GestionnaireImportCantinesCreer.vue"
import GestionnaireImportCantinesModifier from "@/views/GestionnaireImportCantinesModifier.vue"
import GestionnaireImportCantinesGestionnaires from "@/views/GestionnaireImportCantinesGestionnaires.vue"
import GestionnaireTableauDeBord from "@/views/GestionnaireTableauDeBord.vue"
import GestionnaireTunnelApproInformations from "@/views/GestionnaireTunnelApproInformations.vue"
import GestionnaireTunnelApproCouverts from "@/views/GestionnaireTunnelApproCouverts.vue"
import GestionnaireTunnelApproSaisie from "@/views/GestionnaireTunnelApproSaisie.vue"
import GestionnaireTunnelApproEgalim from "@/views/GestionnaireTunnelApproEgalim.vue"
import GestionnaireTunnelApproOrigine from "@/views/GestionnaireTunnelApproOrigine.vue"
import GestionnaireTunnelApproLocalCircuitCourt from "@/views/GestionnaireTunnelApproLocalCircuitCourt.vue"
import GestionnaireTunnelConvives from "@/views/GestionnaireTunnelConvives.vue"
import GestionnaireTunnelGaspillage from "@/views/GestionnaireTunnelGaspillage.vue"
import GestionnaireTunnelVegetarien from "@/views/GestionnaireTunnelVegetarien.vue"
import GestionnaireTunnelPlastique from "@/views/GestionnaireTunnelPlastique.vue"
import GestionnaireTunnelApproRecapitulatif from "@/views/GestionnaireTunnelApproRecapitulatif.vue"

import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"
import LayoutTunnelTeledeclaration from "@/layouts/LayoutTunnelTeledeclaration.vue"

/* Sitemap section id */
const { diag, action } = sectionId

/* Routes */
const currentYear = new Date().getFullYear()
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
        { to: { name: "GestionnaireCantine" }, useCanteenName: true },
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
        path: "bilans-simples",
        name: "GestionnaireImportBilansSimples",
        component: GestionnaireImportBilansSimples,
        meta: {
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
        meta: {
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
        meta: {
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
        path: "",
        component: LayoutSidebarCanteen,
        children: [
          {
            path: "",
            name: "GestionnaireCantine",
            component: GestionnaireCantine,
            meta: {
              title: "Informations",
              breadcrumbs: [
                { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
              ],
            },
          },
          {
            path: "cantines-groupe",
            name: "GestionnaireCantineGroupe",
            component: GestionnaireCantineGroupe,
            meta: {
              title: "Cantines du groupe",
              breadcrumbs: [
                { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
                { to: { name: "GestionnaireCantine" }, useCanteenName: true },
              ],
            },
          },
          {
            path: "teledeclaration",
            name: "GestionnaireCantineTeledeclarationEnCours",
            component: GestionnaireCantineTeledeclarationEnCours,
            meta: {
              title: `Ma télédéclaration ${currentYear}`,
              breadcrumbs: [
                { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
                { to: { name: "GestionnaireCantine" }, useCanteenName: true },
              ],
            },
          },
          {
            path: "toutes-teledeclarations",
            name: "GestionnaireCantineTeledeclarations",
            component: GestionnaireCantineTeledeclarations,
            meta: {
              title: "Toutes les télédéclarations",
              breadcrumbs: [
                { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
                { to: { name: "GestionnaireCantine" }, useCanteenName: true },
              ],
            },
          },
          {
            path: "gestionnaires",
            name: "GestionnaireCantineGestionnaires",
            component: GestionnaireCantineGestionnaires,
            meta: {
              title: "Gestionnaires",
              breadcrumbs: [
                { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
                { to: { name: "GestionnaireCantine" }, useCanteenName: true },
              ],
            },
          },
          {
            path: "page-publique",
            name: "GestionnaireCantinePagePublique",
            component: GestionnaireCantinePagePublique,
            meta: {
              title: "Page publique et affiche à imprimer",
              breadcrumbs: [
                { to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" },
                { to: { name: "GestionnaireCantine" }, useCanteenName: true },
              ],
            },
          },
        ],
      },
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
            { to: { name: "PurchasesHome" }, title: "Mes achats"},
          ],
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
            { to: { name: "PurchasesHome" }, title: "Mes achats" },
          ],
        },
      },
      {
        path: "teledeclaration",
        component: LayoutTunnelTeledeclaration,
        meta: {
          isTunnel: true,
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
