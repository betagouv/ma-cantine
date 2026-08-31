/* Components */
import GestionnaireCantine from "@/views/GestionnaireCantine.vue"
import GestionnaireCantineGroupe from "@/views/GestionnaireCantineGroupe.vue"
import GestionnaireCantineTeledeclarationEnCours from "@/views/GestionnaireCantineTeledeclarationEnCours.vue"
import GestionnaireCantineTeledeclarations from "@/views/GestionnaireCantineTeledeclarations.vue"
import GestionnaireCantineGestionnaires from "@/views/GestionnaireCantineGestionnaires.vue"
import GestionnaireCantinePagePublique from "@/views/GestionnaireCantinePagePublique.vue"

import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"

/* Route */
const currentYear = new Date().getFullYear()
const cantineRoutes = {
  path: "",
  component: LayoutSidebarCanteen,
  meta: {
    storesRequired: ["canteen"],
  },
  children: [
    {
      path: "",
      name: "GestionnaireCantine",
      component: GestionnaireCantine,
      meta: {
        title: "Informations",
        breadcrumbs: [{ to: { name: "GestionnaireTableauDeBord" }, title: "Mon tableau de bord" }],
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
}

export default cantineRoutes
