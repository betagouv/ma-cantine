<script setup>
import { ref, computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import DiagnosticSummaryTile from "@/components/DiagnosticSummaryTile.vue"
import DiagnosticSummaryAccordions from "@/components/DiagnosticSummaryAccordions.vue"

const anchorName = "accordeons"
const openedAccordion = ref(-1)

/* Diagnostic */
const teledeclarationStore = useStoreTeledeclaration()
const { isTeledeclared, hasErrors, hasDiagnostic } = storeToRefs(teledeclarationStore)

/* Get data */
const getIsStarted = (key) => {
  if (key === "appro") return hasDiagnostic.value
  else return false
}

const getImage = (key) => {
  return `/static/images/badges/badge-${key}-disabled.svg`
}

const getSentence = (key) => {
  const isStarted = getIsStarted(key)
  if (!isStarted) return "Volet non renseigné."
  if (key === "appro") return hasErrors.value ? "Volet en attente de correction." : "Volet non télédéclaré."
  return isTeledeclared.value ? "Volet non télédéclaré." : "Volet non renseigné."
}

/* Volets */
const volets = computed(() => {
  return [
    {
      title: "Approvisionnements",
      image: getImage("appro"),
      sentence: getSentence("appro"),
      page: { name: "GestionnaireTunnelApproRecapitulatif" },
      displayErrors: hasErrors.value
    },
    {
      title: "Informations convives",
      shortTitle: "Infos convives",
      image: getImage("info"),
      sentence: getSentence("info"),
      page: { name: "GestionnaireTunnelConvives" }
    },
    {
      title: "Lutte contre le gaspillage alimentaire",
      shortTitle: "Gaspillage",
      image: getImage("waste"),
      sentence: getSentence("waste"),
      page: { name: "GestionnaireTunnelGaspillage" }
    },
    {
      title: "Diversification des sources de protéines et menus végétariens",
      shortTitle: "Menus végétariens",
      image: getImage("diversification"),
      sentence: getSentence("diversification"),
      page: { name: "GestionnaireTunnelVegetarien" }
    },
    {
      title: "Substitutions plastiques",
      shortTitle: "Substitutions plastiques",
      image: getImage("plastic"),
      sentence: getSentence("plastic"),
      page: { name: "GestionnaireTunnelPlastique" }
    }
  ]
})

/* Volets thematiques : tous les volets sauf les approvisionnements */
const thematiques = computed(() => volets.value.slice(1))
</script>

<template>
  <div v-if="hasDiagnostic">
    <DiagnosticSummaryTile
      class="fr-mb-5w"
      :thematiques="thematiques"
      :anchor-name="anchorName"
      :is-teledeclared="isTeledeclared"
      @openAccordion="openedAccordion = $event"
    />
    <DiagnosticSummaryAccordions
      :volets="volets"
      :anchor-name="anchorName"
      :is-teledeclared="isTeledeclared"
      :open="openedAccordion"
    />
  </div>
</template>
