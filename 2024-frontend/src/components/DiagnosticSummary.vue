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
      key: "approvisionnement",
      title: "Approvisionnements",
      macaron: IconMacaronAppro,
      status: macaronsStatus.value.approvisionnement,
      hasErrors: teledeclarationStore.hasVoletErrors("approvisionnement"),
      isFilled: teledeclarationStore.isVoletFilled("approvisionnement"),
      page: { name: "GestionnaireTunnelApproRecapitulatif" }
    },
    {
      key: "information",
      title: "Information des convives",
      shortTitle: "Information convives",
      macaron: IconMacaronInfo,
      status: macaronsStatus.value.information,
      hasErrors: teledeclarationStore.hasVoletErrors("information"),
      isFilled: teledeclarationStore.isVoletFilled("information"),
      page: { name: "GestionnaireTunnelConvives" }
    },
    {
      key: "gaspillage",
      title: "Lutte contre le gaspillage alimentaire",
      shortTitle: "Gaspillage alimentaire",
      macaron: IconMacaronWaste,
      status: macaronsStatus.value.gaspillage,
      hasErrors: teledeclarationStore.hasVoletErrors("gaspillage"),
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
      key: "plastique",
      title: "Substitution du plastique",
      shortTitle: "Substitution plastique",
      macaron: IconMacaronPlastic,
      status: macaronsStatus.value.plastique,
      hasErrors: teledeclarationStore.hasVoletErrors("plastique"),
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
