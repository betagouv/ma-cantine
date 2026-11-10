<script setup>
import { ref, computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import diagnosticsMacaron from "@/services/diagnosticsMacaron.js"
import DiagnosticSummaryTile from "@/components/DiagnosticSummaryTile.vue"
import DiagnosticSummaryAccordions from "@/components/DiagnosticSummaryAccordions.vue"
import IconMacaronAppro from "@/components/IconMacaronAppro.vue"
import IconMacaronInfo from "@/components/IconMacaronInfo.vue"
import IconMacaronWaste from "@/components/IconMacaronWaste.vue"
import IconMacaronDiversification from "@/components/IconMacaronDiversification.vue"
import IconMacaronPlastic from "@/components/IconMacaronPlastic.vue"

const anchorName = "accordeons"
const openedAccordion = ref(-1)

/* Diagnostic */
const teledeclarationStore = useStoreTeledeclaration()
const { isTeledeclared, hasErrors, hasDiagnostic, diagnoticCheck, diagnosticRecap } = storeToRefs(teledeclarationStore)

/* Get data */
const getIsStarted = (key) => {
  if (key === "appro") return hasDiagnostic.value
  else return false
}

const getSentence = (key) => {
  const isStarted = getIsStarted(key)
  if (!isStarted) return "Volet non renseigné."
  if (key === "appro") return hasErrors.value ? "Volet en attente de correction." : "Volet non télédéclaré."
  return isTeledeclared.value ? "Volet non télédéclaré." : "Volet non renseigné."
}

/* Volets */
const macaronsStatus = computed(() => diagnosticsMacaron.getMacaronsStatus(isTeledeclared.value, diagnoticCheck.value, diagnosticRecap.value))

const volets = computed(() => {
  return [
    {
      isAppro: true,
      key: "appro",
      title: "Approvisionnements",
      macaron: IconMacaronAppro,
      sentence: getSentence("appro"),
      status: macaronsStatus.value.appro,
      page: { name: "GestionnaireTunnelApproRecapitulatif" },
      displayErrors: teledeclarationStore.hasVoletErrors("appro")
    },
    {
      key: "info",
      title: "Information des convives",
      shortTitle: "Information convives",
      macaron: IconMacaronInfo,
      sentence: getSentence("info"),
      status: macaronsStatus.value.info,
      page: { name: "GestionnaireTunnelConvives" },
      displayErrors: teledeclarationStore.hasVoletErrors("info")
    },
    {
      key: "waste",
      title: "Lutte contre le gaspillage alimentaire",
      shortTitle: "Gaspillage alimentaire",
      macaron: IconMacaronWaste,
      sentence: getSentence("waste"),
      status: macaronsStatus.value.waste,
      page: { name: "GestionnaireTunnelGaspillage" },
      displayErrors: teledeclarationStore.hasVoletErrors("waste")
    },
    {
      key: "diversification",
      title: "Diversification des sources de protéines et menus végétariens",
      shortTitle: "Menus végétariens",
      macaron: IconMacaronDiversification,
      sentence: getSentence("diversification"),
      status: macaronsStatus.value.diversification,
      page: { name: "GestionnaireTunnelVegetarien" },
      displayErrors: teledeclarationStore.hasVoletErrors("diversification")
    },
    {
      key: "plastic",
      title: "Substitution du plastique",
      shortTitle: "Substitution plastique",
      macaron: IconMacaronPlastic,
      sentence: getSentence("plastic"),
      status: macaronsStatus.value.plastic,
      page: { name: "GestionnaireTunnelPlastique" },
      displayErrors: teledeclarationStore.hasVoletErrors("plastic")
    }
  ]
})

</script>

<template>
  <div v-if="hasDiagnostic">
    <DiagnosticSummaryTile
      class="fr-mb-5w"
      :volets="volets"
      :anchor-name="anchorName"
      :is-teledeclared="isTeledeclared"
      :diagnostic-recap="diagnosticRecap"
      @openAccordion="openedAccordion = $event"
    />
    <DiagnosticSummaryAccordions
      :volets="volets"
      :anchor-name="anchorName"
      :is-teledeclared="isTeledeclared"
      :diagnostic-recap="diagnosticRecap"
      :open="openedAccordion"
    />
  </div>
</template>
