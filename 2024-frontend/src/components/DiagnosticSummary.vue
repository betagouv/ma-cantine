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

defineProps(["diagnosticRecap"])
const anchorName = "accordeons"
const openedAccordion = ref(-1)

/* Diagnostic */
const teledeclarationStore = useStoreTeledeclaration()
const { isTeledeclared, hasErrors, hasDiagnostic, diagnoticCheck } = storeToRefs(teledeclarationStore)

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
const macaronsStatus = computed(() => diagnosticsMacaron.getMacaronsStatus(isTeledeclared.value, diagnoticCheck.value))
const volets = computed(() => {
  return [
    {
      title: "Approvisionnements",
      macaron: IconMacaronAppro,
      sentence: getSentence("appro"),
      status: macaronsStatus.value.appro,
      page: { name: "GestionnaireTunnelApproRecapitulatif" },
      displayErrors: hasErrors.value
    },
    {
      title: "Information des convives",
      shortTitle: "Information convives",
      macaron: IconMacaronInfo,
      sentence: getSentence("info"),
      status: macaronsStatus.value.info,
      page: { name: "GestionnaireTunnelConvives" }
    },
    {
      title: "Lutte contre le gaspillage alimentaire",
      shortTitle: "Gaspillage alimentaire",
      macaron: IconMacaronWaste,
      sentence: getSentence("waste"),
      status: macaronsStatus.value.waste,
      page: { name: "GestionnaireTunnelGaspillage" }
    },
    {
      title: "Diversification des sources de protéines et menus végétariens",
      shortTitle: "Menus végétariens",
      macaron: IconMacaronDiversification,
      sentence: getSentence("diversification"),
      status: macaronsStatus.value.diversification,
      page: { name: "GestionnaireTunnelVegetarien" }
    },
    {
      title: "Substitution du plastique",
      shortTitle: "Substitution plastique",
      macaron: IconMacaronPlastic,
      sentence: getSentence("plastic"),
      status: macaronsStatus.value.plastic,
      page: { name: "GestionnaireTunnelPlastique" }
    }
  ]
})

/* Volets thematiques : tous les volets sauf les approvisionnements */
const thematiques = computed(() => volets.value.slice(1))
const appro = computed(() => volets.value[0])
</script>

<template>
  <div v-if="hasDiagnostic">
    <DiagnosticSummaryTile
      class="fr-mb-5w"
      :thematiques="thematiques"
      :appro="appro"
      :anchor-name="anchorName"
      :is-teledeclared="isTeledeclared"
      :diagnostic-recap="diagnosticRecap"
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
