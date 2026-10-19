<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"

defineProps(["showNav"])
const store = useRootStore()
const route = useRoute()
const logoText = ["République", "française"]

const quickLinks = computed(() => {
  if (!store.loggedUser) {
    const login = { to: "/s-identifier", label: "S'identifier" }
    const signup = { to: "/creer-mon-compte", label: "Créer mon compte" }
    return [login, signup]
  }
  // TODO: logout action
  const monCompte = { to: { name: "AccountSummaryPage" }, label: "Mon compte" }
  return [monCompte]
})

const hasForceActive = (routeName) => (route.meta?.forceActiveNav === routeName ? "page" : undefined)
const navItems = computed(() => [
  {
    text: "Mon tableau de bord",
    to: { name: "GestionnaireTableauDeBord" },
    authenticationState: true,
  },
  {
    text: "Outil Suivi des Achats",
    to: { name: "PurchasesHome" },
    authenticationState: true,
    "aria-current": hasForceActive("PurchasesHome"),
  },
  {
    text: "Outil Suivi Anti-Gaspi",
    to: { name: "GestionnaireGaspillageAlimentaire" },
    authenticationState: true,
    "aria-current": hasForceActive("GestionnaireGaspillageAlimentaire"),
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
])

const navItemsForUser = computed(() => {
  const userLinks = navItems.value.filter((parentItem) => {
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
      <DsfrNavigation v-if="showNav" :nav-items="navItemsForUser" />
    </template>
  </DsfrHeader>
</template>
