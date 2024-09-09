<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import keyMeasures from "@/data/key-measures.json"

const store = useRootStore()

const logoText = ["Ministère", "de l’Agriculture", "et de la Souveraineté", "Alimentaire"]

const quickLinks = computed(() => {
  if (!store.loggedUser) {
    const login = { to: "/s-identifier", label: "S'identifier" }
    const signup = { to: "/creer-mon-compte", label: "Créer mon compte" }
    return [login, signup]
  }
  // TODO: logout action
  if (store.loggedUser.isDev) {
    const apis = { to: { name: "DeveloperPage" }, label: "Développement et APIs" }
    return [apis]
  }
  const mesCantines = { to: { name: "ManagementPage" }, label: "Mon tableau de bord" }
  return [mesCantines]
})

const navItems = [
  {
    text: "Mon tableau de bord",
    to: { name: "ManagementPage" },
    authenticationState: true,
  },
  {
    text: "Mes achats",
    to: { name: "PurchasesHome" },
    authenticationState: true,
  },
  {
    text: "M'auto-évaluer",
    to: { name: "DiagnosticPage" },
    authenticationState: false,
  },
  {
    title: "M'améliorer",
    links: [
      {
        text: "Acteurs de l'éco-système",
        to: { name: "PartnersHome" },
      },
      {
        text: "Générer mon affiche",
        to: { name: "GeneratePosterPage" },
      },
      {
        text: "Webinaires",
        to: { name: "CommunityPage" },
      },
      {
        text: "Blog",
        to: { name: "BlogsHome" },
      },
      {
        text: "Pour aller plus loin",
        to: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
        target: "_blank",
        rel: "noopener external",
      },
    ],
  },
  {
    title: "Toutes les cantines",
    links: [
      {
        text: "Dans mon territoire",
        to: { name: "TerritoryCanteens" },
        forElected: true,
      },
      {
        text: "Trouver une cantine",
        to: { name: "CanteenSearchLanding" },
      },
      {
        text: "Dans ma collectivité",
        to: { name: "PublicCanteenStatisticsPage" },
      },
      {
        text: "Indicateurs clés",
        to: "https://ma-cantine-metabase.cleverapps.io/public/dashboard/3dab8a21-c4b9-46e1-84fa-7ba485ddfbbb",
        target: "_blank",
        rel: "noopener external",
      },
    ],
  },
  {
    title: "Comprendre mes obligations",
    // TODO: get active()
    links: [
      ...keyMeasures.map((x) => ({
        text: x.shortTitle,
        to: { name: "KeyMeasurePage", params: { id: x.id } },
      })),
      ...[
        {
          text: "Pour aller plus loin",
          to: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
          target: "_blank",
          rel: "noopener external",
        },
      ],
    ],
  },
  {
    title: "Aide",
    links: [
      {
        text: "Foire aux questions",
        to: { name: "FaqPage" },
      },
      {
        text: "Importer un fichier",
        to: { name: "ImportSelection" },
      },
      {
        text: "Contactez-nous",
        to: { name: "ContactPage" },
      },
      {
        text: "Documentation",
        to: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
        target: "_blank",
        rel: "noopener external",
      },
    ],
  },
  {
    text: "Mon compte",
    to: { name: "AccountSummaryPage" },
    authenticationState: true,
  },
]

const navItemsForUser = computed(() => {
  const userLinks = navItems.filter((parentItem) => {
    if (parentItem.authenticationState) return !!store.loggedUser
    else if (parentItem.authenticationState === false) return !store.loggedUser
    return true
  })
  userLinks.forEach((parentGroup) => {
    if (parentGroup.links && !store.loggedUser?.isElectedOfficial) {
      parentGroup.links = parentGroup.links.filter((childLink) =>
        childLink.forElected ? !!store.loggedUser?.isElectedOfficial : true
      )
    }
  })
  return userLinks
})
</script>

<template>
  <DsfrHeader
    :logo-text
    operatorImgSrc="/static/images/ma-cantine-logo-light.jpg"
    operatorImgAlt="ma cantine"
    operatorImgStyle="height: 65px;"
    :quickLinks
  >
    <template #mainnav>
      <DsfrNavigation :nav-items="navItemsForUser" />
    </template>
  </DsfrHeader>
</template>
