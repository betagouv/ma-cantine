<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"

const store = useRootStore()

const logoText = ["République", "française"]

const quickLinks = computed(() => {
  if (!store.loggedUser) {
    const login = { to: "/s-identifier", label: "S'identifier" }
    const signup = { to: "/creer-mon-compte", label: "Créer mon compte" }
    return [login, signup]
  }
  // TODO: logout action
  if (store.loggedUser.isDev) {
    const apis = { to: { name: "Developpeurs" }, label: "Développement et APIs" }
    return [apis]
  }
  const mesCantines = { to: { name: "GestionnaireTableauDeBord" }, label: "Mon tableau de bord" }
  return [mesCantines]
})

const navItems = [
  {
    text: "Mon tableau de bord",
    to: { name: "GestionnaireTableauDeBord" },
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
        text: "Actions anti-gaspi",
        to: { name: "WasteActionsHome" },
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
        text: "Observatoire EGalim",
        to: { name: "Observatoire" },
      },
    ],
  },
  {
    text: "Comprendre mes obligations",
    to: { name: "ComprendreMesObligations" },
  },
  {
    title: "Aide",
    links: [
      {
        text: "Contactez-nous",
        to: { name: "Contact" },
      },
      {
        text: "Documentation",
        to: documentation.accueil,
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
    operatorImgSrc="/static/images/ma-cantine-logo-light.svg"
    operatorImgAlt="ma cantine"
    operatorImgStyle="max-width: 15rem"
    :quickLinks
  >
    <template #mainnav>
      <DsfrNavigation :nav-items="navItemsForUser" />
    </template>
  </DsfrHeader>
</template>
