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

const teledeclarationStore = useStoreTeledeclaration()
const { isTeledeclared, hasDiagnostic, diagnoticCheck, diagnosticRecap } = storeToRefs(teledeclarationStore)
const macaronsStatus = computed(() => diagnosticsMacaron.getMacaronsStatus(isTeledeclared.value, diagnoticCheck.value, diagnosticRecap.value))

/* Volets */
const volets = computed(() => {
  return [
    {
      isAppro: true,
      key: "appro",
      title: "Approvisionnements",
      macaron: IconMacaronAppro,
      status: macaronsStatus.value.appro,
      hasErrors: teledeclarationStore.hasVoletErrors("appro"),
      isFilled: teledeclarationStore.isVoletFilled("approvisionnement"),
      page: { name: "GestionnaireTunnelApproRecapitulatif" }
    },
    {
      key: "info",
      title: "Information des convives",
      shortTitle: "Information convives",
      macaron: IconMacaronInfo,
      status: macaronsStatus.value.info,
      hasErrors: teledeclarationStore.hasVoletErrors("info"),
      isFilled: teledeclarationStore.isVoletFilled("information"),
      page: { name: "GestionnaireTunnelConvives" }
    },
    {
      key: "waste",
      title: "Lutte contre le gaspillage alimentaire",
      shortTitle: "Gaspillage alimentaire",
      macaron: IconMacaronWaste,
      status: macaronsStatus.value.waste,
      hasErrors: teledeclarationStore.hasVoletErrors("waste"),
      isFilled: teledeclarationStore.isVoletFilled("gaspillage"),
      page: { name: "GestionnaireTunnelGaspillage" }
    },
    {
      key: "diversification",
      title: "Diversification des sources de protéines et menus végétariens",
      shortTitle: "Menus végétariens",
      macaron: IconMacaronDiversification,
      status: macaronsStatus.value.diversification,
      hasErrors: teledeclarationStore.hasVoletErrors("diversification"),
      isFilled: teledeclarationStore.isVoletFilled("diversification"),
      page: { name: "GestionnaireTunnelVegetarien" }
    },
    {
      key: "plastic",
      title: "Substitution du plastique",
      shortTitle: "Substitution plastique",
      macaron: IconMacaronPlastic,
      status: macaronsStatus.value.plastic,
      hasErrors: teledeclarationStore.hasVoletErrors("plastic"),
      isFilled: teledeclarationStore.isVoletFilled("plastique"),
      page: { name: "GestionnaireTunnelPlastique" }
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
